from dataclasses import replace

from sentence_transformers import CrossEncoder

from .types import Candidate


def load_settings(model_name: str) -> dict:
    """Charge un CrossEncoder pour le reranking."""
    model = CrossEncoder(model_name)

    # Fix padding token pour les modèles basés sur Qwen2 (mxbai-rerank-v2)
    if model.tokenizer.pad_token is None:
        model.tokenizer.pad_token = model.tokenizer.eos_token
        model.model.config.pad_token_id = model.tokenizer.pad_token_id

    return {"model": model}


def score_candidates(query: str, candidates: list[Candidate], task_instruction: str, settings: dict) -> list[Candidate]:
    """Score candidates with a CrossEncoder. Prepends task instruction to query."""
    if not candidates:
        return []

    model = settings["model"]
    instructed_query = f"{task_instruction} {query}"

    pairs = []
    for c in candidates:
        doc = f"{c.description_fr}: {c.description_natural}" if c.description_fr else f"{c.description_natural}"
        pairs.append([instructed_query, doc])

    scores = model.predict(pairs, convert_to_numpy=True).tolist()

    return [replace(c, score=s) for c, s in zip(candidates, scores)]
