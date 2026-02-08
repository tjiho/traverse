from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

INPUT_FILE = "data/osm_wiki_tags_cleaned.json"
NATURAL_DESC_FILE = "data/osm_wiki_tags_natural_desc.json"
MODEL_NAME = "intfloat/multilingual-e5-base"

def index(tags, descriptions, filename):
    model = SentenceTransformer(MODEL_NAME)
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

# Charger tes tags enrichis
with open(INPUT_FILE, "r") as f:
    tags_data = json.load(f)

# Charger les descriptions naturelles (générées par Mistral)
with open(NATURAL_DESC_FILE, "r", encoding="utf-8") as f:
    natural_descriptions = json.load(f)

poi_tags = []
poi_descriptions = []
attribute_tags = []
attribute_descriptions = []

for key, key_data in tags_data.items():
    for value, value_data in key_data.get("values", {}).items():
        tag = f"{key}={value}"
        # Utiliser la description naturelle si disponible, sinon fallback
        desc = natural_descriptions.get(tag, value_data.get("description_enriched", value_data.get("description_fr", "")))
        # Préfixer avec le nom français pour améliorer le matching
        name_fr = value_data.get("description_fr", "")
        if name_fr and not desc.lower().startswith(name_fr.lower()):
            desc = f"{name_fr}. {desc}"
        cat = value_data.get("category", "other")

        if cat == "poi":
            poi_tags.append(tag)
            poi_descriptions.append(desc)
        elif cat == "attribute":
            attribute_tags.append(tag)
            attribute_descriptions.append(desc)
# Encoder les descriptions
print(f"POI: {len(poi_tags)} | Attributes: {len(attribute_tags)}")

index(poi_tags, poi_descriptions, "poi")
index(attribute_tags, attribute_descriptions, "attributes")


