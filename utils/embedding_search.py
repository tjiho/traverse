from dataclasses import replace

from .types import Candidate


def search(query: str, candidates: list[Candidate], settings: dict) -> list[Candidate]:
    """
    Recherche par embedding dans les index FAISS.

    Args:
        query: Requête en français
        candidates: Liste complète de candidats (même ordre que les index FAISS)
        settings: {"model", "indexes", "top_k_per_index", "top_k_total", "min_score"}

    Returns:
        Sous-ensemble de candidats avec score rempli, triés par score décroissant
    """
    model = settings["model"]
    top_k_per_index = settings.get("top_k_per_index", 30)
    top_k_total = settings.get("top_k_total", 50)
    min_score = settings.get("min_score", 0.0)

    query_embedding = model.encode(
        [f"query: {query}"], normalize_embeddings=True
    ).astype("float32")

    results = []

    for index_config in settings["indexes"]:
        index = index_config["index"]
        category = index_config["category"]

        # Filtrer les candidats de cette catégorie (même ordre que le FAISS index)
        cat_candidates = [c for c in candidates if c.category == category]

        scores, indices = index.search(query_embedding, top_k_per_index)

        for idx, score in zip(indices[0], scores[0]):
            if score >= min_score:
                results.append(replace(cat_candidates[idx], score=float(score)))

    results.sort(key=lambda c: c.score, reverse=True)
    return results[:top_k_total]
