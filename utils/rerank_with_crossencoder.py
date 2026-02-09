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


def rerank(query: str, candidates: list[Candidate], settings: dict) -> list[Candidate]:
    """
    Re-rank avec Qwen3-Reranker, par petits batches.
    Retourne top_k tags populaires + top_k tags niche, fusionnés.

    Args:
        query: Requête en français
        candidates: Candidats scorés (sortie de search)
        settings: {"model", "tokenizer", "token_true_id", "token_false_id",
                   "prefix_tokens", "suffix_tokens", "max_length",
                   "task_instruction", "top_k", "batch_size", "usage_count_threshold"}
    """
    top_k = settings.get("top_k", 5)
    batch_size = settings.get("batch_size", 10)
    usage_count_threshold = settings.get("usage_count_threshold", 10_000)
    task_instruction = settings["task_instruction"]

    # Construire les paires query/document
    pairs = []
    for c in candidates:
        doc = f"{c.tag} ({c.description_fr}): {c.description_natural}" if c.description_fr else f"{c.tag}: {c.description_natural}"
        pairs.append(_format_pair(query, doc, task_instruction))

    # Scorer par batches pour éviter l'OOM
    all_scores = []
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i + batch_size]
        inputs = _process_inputs(batch, settings)
        scores = _compute_scores(inputs, settings)
        all_scores.extend(scores)

    # Séparer populaires et niche
    popular = []
    niche = []
    for candidate, score in zip(candidates, all_scores):
        scored = replace(candidate, score=score)
        if candidate.usage_count >= usage_count_threshold:
            popular.append(scored)
        else:
            niche.append(scored)

    popular.sort(key=lambda c: c.score, reverse=True)
    niche.sort(key=lambda c: c.score, reverse=True)

    return popular[:top_k] + niche[:top_k]
