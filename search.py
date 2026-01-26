from sentence_transformers import SentenceTransformer, CrossEncoder
from transformers import pipeline
import faiss
import json
import logging
from autocorrect import Speller

from utils.improve_query import improve_query

logging.basicConfig(
    level=logging.WARNING,
    format="%(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

print("loading data...")

embedding_model = SentenceTransformer("dangvantuan/sentence-camembert-base")
index = faiss.read_index("data/tags.index")
spell = Speller('fr')

with open("data/tags_list.json", "r") as f:
  tags = json.load(f)

# Charger les descriptions
with open("data/fr-improved.json", "r") as f:
  tags_data = json.load(f)

reranker = CrossEncoder("cross-encoder/nli-deberta-v3-small")
#classifier = pipeline("zero-shot-classification", model="MoritzLaurer/bge-m3-zeroshot-v2.0")
generator = pipeline("text-generation", model="mistralai/Ministral-3-3B-Instruct-2512", max_new_tokens=10)


def detect_category(query: str) -> list[str]:
    messages = [
        {
            "role": "user",
            "content": f"""Réponds UNIQUEMENT par "poi" ou "attribute".

poi = lieu générique (restaurant, boulangerie, aéroport, pizzeria, café)
attribute = type/style spécifique (indien, pizza, football, italien)

Exemples:
"où manger" → poi
"restaurant" → poi
"boulangerie" → poi
"aéroport" → poi
"cuisine indienne" → attribute
"sport football" → attribute
"pizza" → attribute
"pizzeria" → poi
"boulangerie" → poi
"pain" → attribute
"restaurant" → poi
"restaurant indien" → attribute
"indien" → attribute
"café" → poi
"expresso" → attribute"""
        },
        {"role": "assistant", "content":"ok"},
        {"role": "user", "content":query}
    ]

    result = generator(messages, max_new_tokens=3)
    logger.debug(f"category output: {result}")
    response = result[0]["generated_text"][-1]["content"].strip().lower()

    if "attribute" in response:
        return ["attribute"]
    elif "poi" in response:
        return ["poi"]
    return ["poi", "attribute"]
# def detect_category(query: str) -> str:
#     prompt = """Tu classes des requêtes de recherche.

# RÈGLE:
# - "poi" = recherche d'un lieu SANS précision de type/style (restaurant, boulangerie, aéroport, où manger)
# - "attribute" = recherche avec un TYPE SPÉCIFIQUE, une cuisine, un style, une caractéristique (indien, pizza, italien, football)

# Si la requête contient une spécificité (cuisine, style, sport...) → attribute
# Si c'est juste un lieu générique → poi

# Exemples:
# "où manger" → poi
# "restaurant" → poi
# "boulangerie" → poi
# "aéroport" → poi
# "cuisine indienne" → attribute
# "sport football" → attribute
# "pizza" → attribute
# "pizzeria" → poi
# "boulangerie" → poi
# "pain" → attribute
# "restaurant" → poi
# "restaurant indien" → attribute
# "indien" → attribute
# "café" → poi
# "expresso" → attribute



# "{query}" →
# """
    
#     result = generator(prompt.format(query=query))[0]["generated_text"]
#     logger.debug(f"category output: {result}")
#     if "poi" in result.split("Réponse:")[-1].lower():
#         return ["poi"]
#     elif "attribute" in result.split("Réponse:")[-1].lower():
#         return ["attribute"]
#     return ["poi", "attribute"]

# category_descriptions = {
#     "poi": "lieu, endroit, où aller, bâtiment, commerce, magasin, restaurant, gare, aéroport",
#     "attribute": "type de cuisine, caractéristique, spécialité, sport pratiqué, régime alimentaire"
# }
# category_names = list(category_descriptions.keys())
# category_embeddings = embedding_model.encode(
#     list(category_descriptions.values()), 
#     normalize_embeddings=True
# )
# def detect_category(query: str, threshold: float = 0.3) -> list[str]:
#     query_embedding = embedding_model.encode([query], normalize_embeddings=True)
    
#     scores = query_embedding @ category_embeddings.T
#     scores = scores[0]
    
#     # Retourne les catégories au-dessus du seuil
#     results = []
#     for name, score in zip(category_names, scores):
#         if score > threshold:
#             results.append((name, score))
    
#     # Si rien au-dessus du seuil, retourne les deux
#     if not results:
#         return ["poi", "attribute"]
    
#     # Trie par score et retourne les noms
#     results.sort(key=lambda x: x[1], reverse=True)
#     return [name for name, score in results]

# category_names = list(category_descriptions.keys())
# category_embeddings = embedding_model.encode(
#     list(category_descriptions.values()), 
#     normalize_embeddings=True
# )
# def detect_category(query: str) -> list[str]:
#     result = classifier(
#         query,
#         candidate_labels=["lieu où aller", "caractéristique d'un lieu"],
#         multi_label=True
#     )
    
#     categories = []
#     for label, score in zip(result["labels"], result["scores"]):
#         if score > 0.5:
#             cat = "poi" if "lieu où" in label else "attribute"
#             categories.append(cat)
    
#     return categories if categories else ["poi", "attribute"]


def get_description(tag: str, tags_data) -> str:
    return tags_data.get(tag, {}).get("improved-message", tag)

def quickSelectionTop50(query, tags):
  query_embedding = embedding_model.encode([improve_query(query)], normalize_embeddings=True).astype("float32")

  scores, indices = index.search(query_embedding, 50)

  tagsWithScores = [(tags[idx], score) for idx, score in zip(indices[0], scores[0])]
  logger.debug(f"Top 50 candidats: {tagsWithScores}")
  tags = [tags[idx] for idx in indices[0]]
  return tags


def rerank(query: str, candidates: list[str], tags_data, top_k: int = 5) -> list[tuple[str, float]]:

  descriptions = [get_description(tag, tags_data) for tag in candidates]
  pairs = [[query, desc] for desc in descriptions]

  
  scores = reranker.predict(pairs)

  entailment_scores = scores[:, 2]
  
  # On retourne les tags originaux avec leurs scores
  results = list(zip(candidates, entailment_scores))
  results.sort(key=lambda x: x[1], reverse=True)
  
  return results[:top_k]

query = "a"
while query != "":
  query = input("recherche ? ")

  if query:
    query_corrected = spell(query)  # "où manger", #"endroit pour manger une pizza rapidement"
    logger.debug(f"Corrected to {query_corrected}")
    print(detect_category(query_corrected))
    #print(rerank(query_corrected, quickSelectionTop50(query_corrected, tags), tags_data))
  else:
    print("bye")