import json
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from .types import TagItem

# === CONFIG ===
RERANKER_MODEL = "Qwen/Qwen3-Reranker-0.6B"
NATURAL_DESC_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "osm_wiki_tags_natural_desc.json")
TAGS_DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "osm_wiki_tags_cleaned.json")
TASK_INSTRUCTION = "Given a French natural language query about a place or service, determine if the document describes a matching OpenStreetMap tag."
USAGE_COUNT_THRESHOLD = 10_000

# === CHARGEMENT ===
tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL, padding_side='left')
model = AutoModelForCausalLM.from_pretrained(
    RERANKER_MODEL,
    torch_dtype=torch.float16,
).cuda().eval()

token_false_id = tokenizer.convert_tokens_to_ids("no")
token_true_id = tokenizer.convert_tokens_to_ids("yes")
max_length = 8192

prefix = "<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be \"yes\" or \"no\".<|im_end|>\n<|im_start|>user\n"
suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"
prefix_tokens = tokenizer.encode(prefix, add_special_tokens=False)
suffix_tokens = tokenizer.encode(suffix, add_special_tokens=False)

# Charger les descriptions naturelles pour le reranking
_natural_descriptions = {}
if os.path.exists(NATURAL_DESC_FILE):
    with open(NATURAL_DESC_FILE, "r", encoding="utf-8") as f:
        _natural_descriptions = json.load(f)

# Charger les usage_count et description_fr
_usage_counts = {}
_descriptions_fr = {}
if os.path.exists(TAGS_DATA_FILE):
    with open(TAGS_DATA_FILE, "r", encoding="utf-8") as f:
        _tags_data = json.load(f)
    for key, key_data in _tags_data.items():
        for value, value_data in key_data.get("values", {}).items():
            tag = f"{key}={value}"
            _usage_counts[tag] = value_data.get("usage_count", 0)
            _descriptions_fr[tag] = value_data.get("description_fr", "")


def _format_pair(query: str, doc: str) -> str:
    return f"<Instruct>: {TASK_INSTRUCTION}\n<Query>: {query}\n<Document>: {doc}"


def _process_inputs(pairs: list[str]):
    inputs = tokenizer(
        pairs, padding=False, truncation='longest_first',
        return_attention_mask=False, max_length=max_length - len(prefix_tokens) - len(suffix_tokens)
    )
    for i, ele in enumerate(inputs['input_ids']):
        inputs['input_ids'][i] = prefix_tokens + ele + suffix_tokens
    inputs = tokenizer.pad(inputs, padding=True, return_tensors="pt", max_length=max_length)
    for key in inputs:
        inputs[key] = inputs[key].to(model.device)
    return inputs


@torch.no_grad()
def _compute_scores(inputs) -> list[float]:
    batch_scores = model(**inputs).logits[:, -1, :]
    true_vector = batch_scores[:, token_true_id]
    false_vector = batch_scores[:, token_false_id]
    batch_scores = torch.stack([false_vector, true_vector], dim=1)
    batch_scores = torch.nn.functional.log_softmax(batch_scores, dim=1)
    scores = batch_scores[:, 1].exp().tolist()
    return scores


def rerank(query: str, candidates: list[TagItem], top_k: int = 5, batch_size: int = 10) -> list[TagItem]:
    """Re-rank avec Qwen3-Reranker, par petits batches pour éviter l'OOM.
    Retourne top_k tags populaires + top_k tags niche, fusionnés."""
    pairs = []
    for item in candidates:
        desc = _natural_descriptions.get(item['tag'], item['description'])
        name_fr = _descriptions_fr.get(item['tag'], "")
        doc = f"{item['tag']} ({name_fr}): {desc}" if name_fr else f"{item['tag']}: {desc}"
        pairs.append(_format_pair(query, doc))

    # Traiter par batches
    all_scores = []
    for i in range(0, len(pairs), batch_size):
        batch = pairs[i:i + batch_size]
        inputs = _process_inputs(batch)
        scores = _compute_scores(inputs)
        all_scores.extend(scores)

    # Séparer populaires et niche
    popular = []
    niche = []
    for item, score in zip(candidates, all_scores):
        usage = _usage_counts.get(item['tag'], 0)
        entry = {"tag": item['tag'], "description": item['description'], "score": float(score), "category": item.get('category', 'poi'), "usage_count": usage}
        if usage >= USAGE_COUNT_THRESHOLD:
            popular.append(entry)
        else:
            niche.append(entry)

    # Top k de chaque groupe, triés par score reranker
    popular.sort(key=lambda x: x['score'], reverse=True)
    niche.sort(key=lambda x: x['score'], reverse=True)

    # Fusionner : populaires d'abord, puis niche
    results = popular[:top_k] + niche[:top_k]
    return results
