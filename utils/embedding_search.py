from sentence_transformers import SentenceTransformer

MODEL_NAME = "intfloat/multilingual-e5-base"

model = SentenceTransformer(MODEL_NAME)


def search(query: str, index, tags, descriptions, category: str = "poi", top_k: int = 10, min_score: float = 0.3) -> list[dict]:
    """
    Recherche dans un seul index.

    Returns:
        Liste de dicts: {"tag": "...", "score": 0.85, "category": "...", "description": "..."}
    """
    query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")

    results = []
    scores, indices = index.search(query_embedding, top_k)

    for idx, score in zip(indices[0], scores[0]):
        if score >= min_score:
            results.append({
                "tag": tags[idx],
                "description": descriptions[idx],
                "score": float(score),
                "category": category,
            })

    return results


def search_multi(query: str, indexes: list[dict], top_k_per_index: int = 30, top_k_total: int = 50, min_score: float = 0.3) -> list[dict]:
    """
    Recherche dans plusieurs index et fusionne les résultats.
    Prend top_k_per_index de chaque index pour éviter qu'une catégorie domine.

    Args:
        indexes: Liste de dicts avec keys: index, tags, descriptions, category
                 Ex: [{"index": poi_index, "tags": poi_tags, "descriptions": poi_desc, "category": "poi"}, ...]
        top_k_per_index: Nombre de résultats à prendre par index
        top_k_total: Nombre total de résultats à retourner

    Returns:
        Liste fusionnée triée par score
    """
    query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")

    all_results = []

    for idx_data in indexes:
        index = idx_data["index"]
        tags = idx_data["tags"]
        descriptions = idx_data["descriptions"]
        category = idx_data["category"]

        scores, indices = index.search(query_embedding, top_k_per_index)

        for idx, score in zip(indices[0], scores[0]):
            if score >= min_score:
                all_results.append({
                    "tag": tags[idx],
                    "description": descriptions[idx],
                    "score": float(score),
                    "category": category,
                })

    # Trier par score et garder top_k_total
    all_results.sort(key=lambda x: x["score"], reverse=True)
    return all_results[:top_k_total]


# TODO: Idée future - classifier la requête en POI/attribut pour optimiser la recherche
# Options testées (voir test_category_detection.py):
# - Heuristiques basées sur mots-clés: 86.7% accuracy, 0ms
# - Embedding similarity avec prototypes: 80%, 0.5s
# - Zero-shot (mDeBERTa): 33%, 1s
# - LLM (Gemma 3 1B): 37%, 5s
# Pour l'instant on cherche partout, le reranker trie.
