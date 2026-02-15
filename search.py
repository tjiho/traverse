"""
Script de recherche de tags OSM
"""

import logging

from utils.prepare import prepare
from utils.embedding_search import search
from utils.rerank_with_crossencoder import rerank

# === LOGGING ===
logging.basicConfig(level=logging.WARNING)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

candidates, search_settings, rerank_settings = prepare()


def format_results(results: list) -> str:
    """Formate les résultats pour affichage"""
    lines = []
    for r in results:
        vis = f" {r.visibility}" if r.visibility else ""
        lines.append(f"  [{r.category[:3].upper()}{vis}] {r.tag} ({r.score:.2f}): {r.description_fr}")
    return "\n".join(lines)


# === MAIN ===
if __name__ == "__main__":
    while True:
        query = input("\nRecherche ? ")
        if not query:
            break

        results = search(query, candidates, search_settings)

        if results:
            print(format_results(results))

            rerank_results = rerank(query, results, rerank_settings)
            print("\n===\n")
            print(format_results(rerank_results))
        else:
            print("  Aucun résultat")
