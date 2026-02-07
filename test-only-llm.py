from transformers import pipeline
import json

# === CONFIG ===
MODEL = "google/gemma-3-1b-it"  # ou 1b-it si RAM limitée
INPUT_FILE = "data/osm_wiki_tags_cleaned.json"

# === CHARGER LES POI ===
with open(INPUT_FILE, "r") as f:
    data = json.load(f)

poi_list = []
for key, key_data in data.items():
    for value, value_data in key_data.get("values", {}).items():
        if value_data.get("category") == "poi":
            tag = f"{key}={value}"
            desc = value_data.get("description_enriched", "")
            poi_list.append(f"{tag}: {desc}")

poi_text = "\n".join(poi_list)
print(f"POI: {len(poi_list)} tags")

# === PIPELINE ===
generator = pipeline("text-generation", model=MODEL, device_map="auto")

# === RECHERCHE ===
def search(query: str):
    prompt = f"""Voici la liste des tags OpenStreetMap:
{poi_text}

Question: {query}
Réponds UNIQUEMENT avec les 5 tags les plus pertinents, un par ligne, sans explication."""

    result = generator(prompt, max_new_tokens=100)
    return result[0]["generated_text"]

# === TEST ===
print(search("où manger chinois"))