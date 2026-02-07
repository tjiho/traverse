from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

INPUT_FILE = "data/osm_wiki_tags_cleaned.json"
MODEL_NAME = "intfloat/multilingual-e5-base"

def index(tags, descriptions, filename):
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(descriptions, show_progress_bar=True, normalize_embeddings=True)

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


poi_tags = []   
poi_descriptions = []
attribute_tags = []
attribute_descriptions = []

for key, key_data in tags_data.items():
    for value, value_data in key_data.get("values", {}).items():
        tag = f"{key}={value}"
        desc = value_data.get("description_enriched", value_data.get("description_fr", ""))
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


