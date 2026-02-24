"""
Fonctions de démarrage : chargement des données, modèles et index.
"""

import json
import os
import faiss
import torch
from sentence_transformers import SentenceTransformer

from .types import Candidate

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Modèles
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"
QWEN3_RERANKER_MODEL = "Qwen/Qwen3-Reranker-0.6B"
DEFAULT_CROSSENCODER_MODEL = "mixedbread-ai/mxbai-rerank-base-v2"

# Reranker config
TASK_INSTRUCTION_POI = (
    "Given a French natural language query about a place or service, "
    "determine if the document describes a matching OpenStreetMap tag."
)
TASK_INSTRUCTION_ATTRIBUTE = (
    "Given a French natural language query, determine if the document "
    "describes a characteristic or attribute that matches what the user is looking for."
)


def load_candidates(data_dir: str = DATA_DIR) -> list[Candidate]:
    """
    Charge les données et construit la liste de candidats.
    L'ordre d'itération est identique à create-index.py pour que
    les positions correspondent aux index FAISS.
    """
    with open(os.path.join(data_dir, "osm_wiki_tags_cleaned.json"), "r", encoding="utf-8") as f:
        tags_data = json.load(f)

    natural_desc_path = os.path.join(data_dir, "osm_wiki_tags_natural_desc.json")
    if os.path.exists(natural_desc_path):
        with open(natural_desc_path, "r", encoding="utf-8") as f:
            natural_descriptions = json.load(f)
    else:
        natural_descriptions = {}

    candidates = []
    for key, key_data in tags_data.items():
        for value, value_data in key_data.get("values", {}).items():
            tag = f"{key}={value}"
            category = value_data.get("category", "other")
            if category not in ("poi", "attribute"):
                continue

            description_fr = value_data.get("description_fr", "")
            description_natural = natural_descriptions.get(
                tag,
                value_data.get("description_enriched", value_data.get("description_fr", ""))
            )

            candidates.append(Candidate(
                tag=tag,
                description_fr=description_fr,
                description_natural=description_natural,
                category=category,
                usage_count=value_data.get("usage_count", 0),
            ))

    return candidates


def load_search_settings(data_dir: str = DATA_DIR) -> dict:
    """Charge le modèle d'embedding et les index FAISS."""
    model = SentenceTransformer(EMBEDDING_MODEL)

    poi_index = faiss.read_index(os.path.join(data_dir, "poi.index"))
    attr_index = faiss.read_index(os.path.join(data_dir, "attributes.index"))

    return {
        "model": model,
        "indexes": [
            {"index": poi_index, "category": "poi"},
            {"index": attr_index, "category": "attribute"},
        ],
        "top_k_per_index": 30,
        "top_k_total": 50,
        "min_score": 0.0,
    }


def _load_qwen3_rerank_settings() -> dict:
    """Charge le modèle Qwen3-Reranker (LLM génératif)."""
    from transformers import AutoTokenizer, AutoModelForCausalLM
    from .rerank_with_crossencoder import score_candidates

    tokenizer = AutoTokenizer.from_pretrained(QWEN3_RERANKER_MODEL, padding_side='left')
    model = AutoModelForCausalLM.from_pretrained(
        QWEN3_RERANKER_MODEL,
        torch_dtype=torch.float16,
    ).cuda().eval()

    prefix = '<|im_start|>system\nJudge whether the Document meets the requirements based on the Query and the Instruct provided. Note that the answer can only be "yes" or "no".<|im_end|>\n<|im_start|>user\n'
    suffix = "<|im_end|>\n<|im_start|>assistant\n<think>\n\n</think>\n\n"

    return {
        "model": model,
        "tokenizer": tokenizer,
        "token_true_id": tokenizer.convert_tokens_to_ids("yes"),
        "token_false_id": tokenizer.convert_tokens_to_ids("no"),
        "prefix_tokens": tokenizer.encode(prefix, add_special_tokens=False),
        "suffix_tokens": tokenizer.encode(suffix, add_special_tokens=False),
        "max_length": 8192,
        "batch_size": 10,
        "score_fn": score_candidates,
    }


def _load_crossencoder_rerank_settings(model_name: str) -> dict:
    """Charge un CrossEncoder léger (Jina v2, MixedBread v2, etc.)."""
    from .rerank_with_sentence_transformer import load_settings, score_candidates

    model_settings = load_settings(model_name)
    return {
        **model_settings,
        "score_fn": score_candidates,
    }


def load_rerank_settings() -> dict:
    """
    Charge le reranker selon les variables d'environnement.

    RERANKER: "qwen3" (défaut) ou "crossencoder"
    RERANKER_MODEL: modèle CrossEncoder (défaut: jina-reranker-v2-base-multilingual)
    """
    reranker = os.environ.get("RERANKER", "qwen3").lower()

    if reranker == "crossencoder":
        model_name = os.environ.get("RERANKER_MODEL", DEFAULT_CROSSENCODER_MODEL)
        print(f"Reranker: CrossEncoder ({model_name})")
        settings = _load_crossencoder_rerank_settings(model_name)
    else:
        print(f"Reranker: Qwen3 ({QWEN3_RERANKER_MODEL})")
        settings = _load_qwen3_rerank_settings()

    settings.update({
        "task_instructions": {
            "poi": TASK_INSTRUCTION_POI,
            "attribute": TASK_INSTRUCTION_ATTRIBUTE,
        },
        "top_k": 5,
        "usage_count_threshold": 10_000,
    })

    return settings


def prepare(data_dir: str = DATA_DIR) -> tuple[list[Candidate], dict, dict]:
    """
    Fonction de démarrage complète.
    Retourne (candidates, search_settings, rerank_settings).
    """
    candidates = load_candidates(data_dir)
    search_settings = load_search_settings(data_dir)
    rerank_settings = load_rerank_settings()

    print(f"POI: {sum(1 for c in candidates if c.category == 'poi')} tags")
    print(f"Attributes: {sum(1 for c in candidates if c.category == 'attribute')} tags")
    print("Prêt.\n")

    return candidates, search_settings, rerank_settings
