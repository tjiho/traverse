"""
Fonctions de démarrage : chargement des données, modèles et index.
"""

import json
import os
import faiss
import torch
from sentence_transformers import SentenceTransformer
from transformers import AutoTokenizer, AutoModelForCausalLM

from .types import Candidate

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")

# Modèles
EMBEDDING_MODEL = "intfloat/multilingual-e5-base"
RERANKER_MODEL = "Qwen/Qwen3-Reranker-0.6B"

# Reranker config
TASK_INSTRUCTION = "Given a French natural language query about a place or service, determine if the document describes a matching OpenStreetMap tag."


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


def load_rerank_settings() -> dict:
    """Charge le modèle de reranking et prépare les tokens."""
    tokenizer = AutoTokenizer.from_pretrained(RERANKER_MODEL, padding_side='left')
    model = AutoModelForCausalLM.from_pretrained(
        RERANKER_MODEL,
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
        "task_instruction": TASK_INSTRUCTION,
        "top_k": 5,
        "batch_size": 10,
        "usage_count_threshold": 10_000,
    }


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
