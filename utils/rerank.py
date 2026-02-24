from dataclasses import replace

from .types import Candidate


def rerank(query: str, candidates: list[Candidate], settings: dict) -> list[Candidate]:
    """
    Re-rank candidates using the configured score_fn.
    Scores POI and attributes separately with adapted instructions,
    then returns top_k popular + top_k niche per category.

    Args:
        query: Requête en français
        candidates: Candidats scorés (sortie de search)
        settings: dict with "score_fn", "task_instructions", "top_k",
                  "usage_count_threshold", plus model-specific keys
    """
    top_k = settings.get("top_k", 5)
    usage_count_threshold = settings.get("usage_count_threshold", 10_000)
    task_instructions = settings["task_instructions"]
    score_fn = settings["score_fn"]

    # Séparer par catégorie et scorer avec l'instruction adaptée
    poi_candidates = [c for c in candidates if c.category == "poi"]
    attr_candidates = [c for c in candidates if c.category == "attribute"]

    poi_scored = score_fn(query, poi_candidates, task_instructions["poi"], settings)
    attr_scored = score_fn(query, attr_candidates, task_instructions["attribute"], settings)

    # Split popular/niche par catégorie, top_k de chaque groupe
    def _split_and_top(scored, top_k):
        popular = sorted([c for c in scored if c.usage_count >= usage_count_threshold], key=lambda c: c.score, reverse=True)[:top_k]
        niche = sorted([c for c in scored if c.usage_count < usage_count_threshold], key=lambda c: c.score, reverse=True)[:top_k]
        popular = [replace(c, visibility="popular") for c in popular]
        niche = [replace(c, visibility="niche") for c in niche]
        return popular + niche

    return _split_and_top(poi_scored, top_k) + _split_and_top(attr_scored, top_k)
