# Traverse

Recherche sémantique de tags OpenStreetMap en langage naturel français.

Transforme des requêtes comme "où manger", "parking vélo", "pharmacie ouverte" en tags OSM correspondants (`amenity=restaurant`, `amenity=bicycle_parking`, `amenity=pharmacy`).

## Fonctionnement

Pipeline en 2 étapes :

1. **Embedding search** - Recherche sémantique avec `intfloat/multilingual-e5-base`
2. **Reranking** - Affinement avec cross-encoder `BAAI/bge-reranker-v2-m3`

Performance : **98.8% recall** sur 100 cas de test.

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
uv run test/evaluate.py
```

## Structure

```
├── search.py              # CLI de recherche
├── create-index.py        # Génération des index FAISS
├── utils/
│   ├── embedding_search.py    # Recherche par embedding
│   ├── rerank_with_crossencoder.py  # Reranking
│   └── query_expansion.py     # Expansion de requête (expérimental)
├── data/
│   ├── osm_wiki_tags_cleaned.json  # Tags OSM enrichis
│   ├── poi.index / attributes.index  # Index FAISS
│   └── search_cases.json       # Cas de test
└── test/
    └── evaluate.py        # Script d'évaluation
```

## Roadmap

- [ ] API REST (FastAPI)
- [ ] Détection automatique POI vs attribut
- [ ] Support multilingue
