from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

from utils.prepare import load_candidates, EMBEDDING_MODEL, DATA_DIR

def index(tags, descriptions, filename):
    model = SentenceTransformer(EMBEDDING_MODEL)
    # Ajouter le préfixe "passage: " pour E5
    descriptions_with_prefix = [f"passage: {d}" for d in descriptions]
    embeddings = model.encode(descriptions_with_prefix, show_progress_bar=True, normalize_embeddings=True)

    # Construire l'index FAISS
    index = faiss.IndexFlatIP(embeddings.shape[1])
    index.add(embeddings.astype("float32"))

    # Sauvegarder l'index et les tags
    faiss.write_index(index, f"data/{filename}.index")
    with open(f"data/{filename}_list.json", "w") as f:
        json.dump(tags, f)

    with open(f"data/{filename}_list_desc.json", "w") as f:
        json.dump(descriptions, f)

candidates = load_candidates()

poi_tags = []
poi_descriptions = []
attribute_tags = []
attribute_descriptions = []

for c in candidates:
    # Construire la description indexée avec le préfixe description_fr
    desc = c.description_natural
    if c.description_fr and not desc.lower().startswith(c.description_fr.lower()):
        desc = f"{c.description_fr}. {desc}"

    if c.category == "poi":
        poi_tags.append(c.tag)
        poi_descriptions.append(desc)
    elif c.category == "attribute":
        attribute_tags.append(c.tag)
        attribute_descriptions.append(desc)

print(f"POI: {len(poi_tags)} | Attributes: {len(attribute_tags)}")

index(poi_tags, poi_descriptions, "poi")
index(attribute_tags, attribute_descriptions, "attributes")
