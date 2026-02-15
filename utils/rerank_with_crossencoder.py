from dataclasses import replace

import torch

from .types import Candidate


def _format_pair(query: str, doc: str, task_instruction: str) -> str:
    return f"<Instruct>: {task_instruction}\n<Query>: {query}\n<Document>: {doc}"


def _process_inputs(pairs: list[str], settings: dict):
    tokenizer = settings["tokenizer"]
    prefix_tokens = settings["prefix_tokens"]
    suffix_tokens = settings["suffix_tokens"]
    max_length = settings["max_length"]

    inputs = tokenizer(
        pairs, padding=False, truncation='longest_first',
        return_attention_mask=False,
        max_length=max_length - len(prefix_tokens) - len(suffix_tokens)
    )
    for i, ele in enumerate(inputs['input_ids']):
        inputs['input_ids'][i] = prefix_tokens + ele + suffix_tokens
    inputs = tokenizer.pad(inputs, padding=True, return_tensors="pt", max_length=max_length)
    for key in inputs:
        inputs[key] = inputs[key].to(settings["model"].device)
    return inputs


@torch.no_grad()
def _compute_scores(inputs, settings: dict) -> list[float]:
    model = settings["model"]
    batch_scores = model(**inputs).logits[:, -1, :]
    true_vector = batch_scores[:, settings["token_true_id"]]
    false_vector = batch_scores[:, settings["token_false_id"]]
    batch_scores = torch.stack([false_vector, true_vector], dim=1)
    batch_scores = torch.nn.functional.log_softmax(batch_scores, dim=1)
    return batch_scores[:, 1].exp().tolist()


def _score_candidates(query: str, candidates: list[Candidate], task_instruction: str, settings: dict) -> list[Candidate]:
    """Score une liste de candidats avec une instruction donnée. Retourne les candidats avec score."""
    if not candidates:
        return []

    batch_size = settings.get("batch_size", 10)

    pairs = []
    for c in candidates:
        doc = f"{c.description_fr}: {c.description_natural}" if c.description_fr else f"{c.description_natural}"
        pairs.append(_format_pair(query, doc, task_instruction))

    all_scores = []
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i + batch_size]
        inputs = _process_inputs(batch, settings)
        scores = _compute_scores(inputs, settings)
        all_scores.extend(scores)

    return [replace(c, score=s) for c, s in zip(candidates, all_scores)]


def rerank(query: str, candidates: list[Candidate], settings: dict) -> list[Candidate]:
    """
    Re-rank avec Qwen3-Reranker, par petits batches.
    Score les POI et attributs séparément avec des instructions adaptées,
    puis retourne top_k tags populaires + top_k tags niche.

    Args:
        query: Requête en français
        candidates: Candidats scorés (sortie de search)
        settings: {"model", "tokenizer", "token_true_id", "token_false_id",
                   "prefix_tokens", "suffix_tokens", "max_length",
                   "task_instructions", "top_k", "batch_size", "usage_count_threshold"}
    """
    top_k = settings.get("top_k", 5)
    usage_count_threshold = settings.get("usage_count_threshold", 10_000)
    task_instructions = settings["task_instructions"]

    # Séparer par catégorie et scorer avec l'instruction adaptée
    poi_candidates = [c for c in candidates if c.category == "poi"]
    attr_candidates = [c for c in candidates if c.category == "attribute"]

    poi_scored = _score_candidates(query, poi_candidates, task_instructions["poi"], settings)
    attr_scored = _score_candidates(query, attr_candidates, task_instructions["attribute"], settings)

    # Split popular/niche par catégorie, top_k de chaque groupe
    def _split_and_top(scored, top_k):
        popular = sorted([c for c in scored if c.usage_count >= usage_count_threshold], key=lambda c: c.score, reverse=True)[:top_k]
        niche = sorted([c for c in scored if c.usage_count < usage_count_threshold], key=lambda c: c.score, reverse=True)[:top_k]
        popular = [replace(c, visibility="popular") for c in popular]
        niche = [replace(c, visibility="niche") for c in niche]
        return popular + niche

    return _split_and_top(poi_scored, top_k) + _split_and_top(attr_scored, top_k)
