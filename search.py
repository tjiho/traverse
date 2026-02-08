"""
Script de recherche de tags OSM
"""

import json
import faiss
import logging

from utils.rerank_with_crossencoder import rerank
from utils.embedding_search import search, search_multi

# === LOGGING ===
logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

poi_index = faiss.read_index(f"data/poi.index")
attribute_index = faiss.read_index(f"data/attributes.index")

with open(f"data/poi_list.json", "r", encoding="utf-8") as f:
    poi_tags = json.load(f)

with open(f"data/attributes_list.json", "r", encoding="utf-8") as f:
    attribute_tags = json.load(f)

with open(f"data/poi_list_desc.json", "r", encoding="utf-8") as f:
    poi_descriptions = json.load(f)

with open(f"data/attributes_list_desc.json", "r", encoding="utf-8") as f:
    attribute_descriptions = json.load(f)

print(f"POI: {len(poi_tags)} tags")
print(f"Attributes: {len(attribute_tags)} tags")

# Config pour search_multi
INDEXES = [
    {"index": poi_index, "tags": poi_tags, "descriptions": poi_descriptions, "category": "poi"},
    #{"index": attribute_index, "tags": attribute_tags, "descriptions": attribute_descriptions, "category": "attribute"},
]

print("Prêt.\n")


def detect_category(query: str) -> list[str]:
    """Détecte si la requête cherche un POI, un attribute, ou les deux"""
    query_lower = query.lower()
    words = query_lower.split()

    # Mots indiquant une recherche de lieu
    poi_indicators = {"où", "ou", "trouver", "cherche", "aller", "proche", "près"}

    # Mots indiquant un attribut (type, caractéristique)
    attribute_indicators = {
        "indien",
        "chinois",
        "japonais",
        "italien",
        "mexicain",
        "turc",
        "thaï",
        "végétarien",
        "vegan",
        "halal",
        "casher",
        "pizza",
        "burger",
        "kebab",
        "sushi",
        "curry",
        "accessible",
        "fauteuil",
        "roulant",
        "handicapé",
        "pmr",
        "ouvert",
        "dimanche",
        "nuit",
        "24h",
        "wifi",
        "terrasse",
        "parking",
        "football",
        "tennis",
        "basket",
        "natation",
    }

    has_poi_indicator = any(w in poi_indicators for w in words)
    has_attribute_indicator = any(w in attribute_indicators for w in words)

    # "où manger chinois" → les deux
    if has_poi_indicator and has_attribute_indicator:
        return ["poi", "attribute"]

    # "cuisine indienne" → attribute
    if has_attribute_indicator:
        return ["attribute"]

    # "où manger", "restaurant" → poi
    if has_poi_indicator:
        return ["poi"]

    # Par défaut, chercher dans les deux
    return ["poi", "attribute"]


def format_results(results: list[dict]) -> str:
    """Formate les résultats pour affichage"""
    lines = []
    for r in results:
        lines.append(f"  [{r['category'][:3].upper()}] {r['tag']} ({r['score']:.2f}): {r['description']}")
    return "\n".join(lines)


# === MAIN ===
if __name__ == "__main__":
    while True:
        query = input("\nRecherche ? ")
        if not query:
            break

        results = search_results = search_multi(
            query, 
            INDEXES, 
            top_k_per_index=30, 
            top_k_total=50, 
            min_score=0.0
        ) #search(query, poi_index, poi_tags, poi_descriptions, top_k=50, min_score=0.3)

        if results:
            print(format_results(results))

            rerank_results = rerank(query, results)
            print("\n===\n")
            print(format_results(rerank_results))
        else:
            print("  Aucun résultat")
