# Traverse

Recherche sémantique de tags OpenStreetMap en langage naturel français.

Transforme des requêtes comme "où manger", "parking vélo", "acheter du pain" en tags OSM correspondants (`amenity=restaurant`, `amenity=bicycle_parking`, `shop=bakery`).

## Fonctionnement

Pipeline en 2 étapes :

1. **Embedding search** - Recherche sémantique avec `intfloat/multilingual-e5-base` dans des index FAISS (POI + attributs)
2. **Reranking** - Affinement avec `Qwen/Qwen3-Reranker-0.6B`, séparant résultats populaires et niche

Les descriptions des tags sont des phrases en français naturel générées par Mistral Large, enrichies du nom français (`description_fr`) pour un meilleur matching.

Performance : **98.4% recall** sur 100 cas de test.

## Installation

```bash
uv sync
```

## Usage

Construire les index (nécessite GPU) :
```bash
switcherooctl launch uv run create-index.py
```

Recherche interactive :
```bash
switcherooctl launch uv run search.py
```

Évaluation :
```bash
switcherooctl launch uv run test/evaluate.py
```

## Architecture

```
├── search.py                          # CLI de recherche
├── create-index.py                    # Génération des index FAISS
├── utils/
│   ├── types/__init__.py              # Candidate dataclass
│   ├── prepare.py                     # Chargement données, modèles, index
│   ├── embedding_search.py            # search(query, candidates, settings)
│   └── rerank_with_crossencoder.py    # rerank(query, candidates, settings)
├── data/
│   ├── osm_wiki_tags_cleaned.json     # Tags OSM enrichis
│   ├── osm_wiki_tags_natural_desc.json # Descriptions naturelles (Mistral)
│   ├── poi.index / attributes.index   # Index FAISS
│   └── search_cases.json             # Cas de test
└── test/
    └── evaluate.py                    # Script d'évaluation
```

Toutes les fonctions sont pures et interchangeables :

```python
candidates, search_settings, rerank_settings = prepare()

results = search(query, candidates, search_settings)    # list[Candidate] → list[Candidate]
reranked = rerank(query, results, rerank_settings)       # list[Candidate] → list[Candidate]
```

## Roadmap

- [ ] API REST (FastAPI)
- [ ] Détection automatique POI vs attribut
- [ ] Support multilingue
