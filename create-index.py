from sentence_transformers import SentenceTransformer
import faiss
import json
import numpy as np

# Charger tes tags enrichis
with open("data/fr-improved.json", "r") as f:
    data = json.load(f)

tags = list(data.keys())
descriptions = [data[tag]["improved-message"] for tag in tags]

# Encoder les descriptions
model = SentenceTransformer("dangvantuan/sentence-camembert-base")
embeddings = model.encode(descriptions, show_progress_bar=True, normalize_embeddings=True)

# Construire l'index FAISS
index = faiss.IndexFlatIP(embeddings.shape[1])
index.add(embeddings.astype("float32"))

# Sauvegarder l'index et les tags
faiss.write_index(index, "data/tags.index")
with open("data/tags_list.json", "w") as f:
    json.dump(tags, f)