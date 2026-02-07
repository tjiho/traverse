"""
Script d'évaluation de la recherche de tags
"""

import json
import faiss
from utils.embedding_search import search_multi
from utils.rerank_with_crossencoder import rerank

# Charger les index POI
poi_index = faiss.read_index("data/poi.index")
with open("data/poi_list.json", "r", encoding="utf-8") as f:
    poi_tags = json.load(f)
with open("data/poi_list_desc.json", "r", encoding="utf-8") as f:
    poi_descriptions = json.load(f)

# Charger les index Attributs
attr_index = faiss.read_index("data/attributes.index")
with open("data/attributes_list.json", "r", encoding="utf-8") as f:
    attr_tags = json.load(f)
with open("data/attributes_list_desc.json", "r", encoding="utf-8") as f:
    attr_descriptions = json.load(f)

# Config pour search_multi
INDEXES = [
    {"index": poi_index, "tags": poi_tags, "descriptions": poi_descriptions, "category": "poi"},
    {"index": attr_index, "tags": attr_tags, "descriptions": attr_descriptions, "category": "attribute"},
]


def compute_metrics(expected: set, found_tags: list) -> tuple[float, float]:
    """Calcule recall et MRR"""
    found_set = set(found_tags)
    hits = expected & found_set
    recall = len(hits) / len(expected) if expected else 1.0

    mrr = 0.0
    for i, tag in enumerate(found_tags):
        if tag in expected:
            mrr = 1.0 / (i + 1)
            break

    return recall, mrr


def evaluate(test_file: str = "data/search_cases.json", search_top_k_per_index: int = 30, search_top_k_total: int = 50, rerank_top_k: int = 10):
    """
    Évalue la recherche sur les cas de tests

    Deux étapes:
    1. Search (embedding) - récupère search_top_k candidats
    2. Rerank (cross-encoder) - garde rerank_top_k résultats

    Métriques:
    - Recall: proportion des tags attendus trouvés
    - MRR: Mean Reciprocal Rank (position moyenne du premier tag correct)
    """
    with open(test_file, "r", encoding="utf-8") as f:
        cases = json.load(f)

    # Accumulateurs pour les deux étapes
    search_recall_total = 0
    search_mrr_total = 0
    rerank_recall_total = 0
    rerank_mrr_total = 0

    for case in cases:
        query = case["query"]
        expected = set(case["expected"])

        # Convertir format "tag:amenity=restaurant" → "amenity=restaurant"
        expected = {tag[4:] if tag.startswith("tag:") else tag for tag in expected}

        # Étape 1: Search (embedding) dans POI + Attributs
        search_results = search_multi(query, INDEXES, top_k_per_index=search_top_k_per_index, top_k_total=search_top_k_total, min_score=0.0)
        search_tags = [r["tag"] for r in search_results]
        search_recall, search_mrr = compute_metrics(expected, search_tags)
        search_recall_total += search_recall
        search_mrr_total += search_mrr

        # Étape 2: Rerank
        rerank_results = rerank(query, search_results, top_k=rerank_top_k)
        rerank_tags = [r["tag"] for r in rerank_results]
        rerank_recall, rerank_mrr = compute_metrics(expected, rerank_tags)
        rerank_recall_total += rerank_recall
        rerank_mrr_total += rerank_mrr

        # Status (basé sur rerank)
        if rerank_recall == 1.0:
            status = "✓"
        elif rerank_recall > 0:
            status = "~"
        else:
            status = "✗"

        print(f"{status} '{query}'")
        print(f"    Search:  recall={search_recall:.0%} mrr={search_mrr:.2f} | Rerank: recall={rerank_recall:.0%} mrr={rerank_mrr:.2f}")
        if rerank_recall < 1.0:
            print(f"    Expected: {expected}")
            print(f"    Rerank top 5: {rerank_tags[:5]}")

    # Moyennes
    n = len(cases)

    print(f"\n{'='*60}")
    print(f"RÉSULTATS ({n} cas)")
    print(f"{'='*60}")
    print(f"{'Étape':<15} {'Recall':>10} {'MRR':>10}")
    print(f"{'-'*60}")
    print(f"{'Search':<15} {search_recall_total/n:>10.1%} {search_mrr_total/n:>10.2f}")
    print(f"{'Rerank':<15} {rerank_recall_total/n:>10.1%} {rerank_mrr_total/n:>10.2f}")

    return {
        "search": {"recall": search_recall_total/n, "mrr": search_mrr_total/n},
        "rerank": {"recall": rerank_recall_total/n, "mrr": rerank_mrr_total/n},
    }


if __name__ == "__main__":
    evaluate()
