# Traverse

Recherche sémantique de tags OpenStreetMap en langage naturel en français.

Transforme des requêtes comme "où manger", "parking vélo", "acheter du pain" en tags OSM correspondants (`amenity=restaurant`, `amenity=bicycle_parking`, `shop=bakery`).

## Fonctionnement

Pipeline en 2 étapes :

1. **Embedding search** - Recherche sémantique avec `intfloat/multilingual-e5-base` dans des index FAISS (POI + attributs). Recherche rapide pour selectionner le top 100.
2. **Reranking** - Affinement avec `Qwen/Qwen3-Reranker-0.6B`, séparant résultats populaires (tag avec plus de 10000 occurence) et niche (moins de 10000). Selectionne deux top 5 (populaire et niche)

Les modèles traitent la description du tag + la traduction française du tag + la valeur litteral du tag. 

Les données de départ sont un mélange de scrapping du wiki openstreetmap, ainsi qu'un fichier json provenant de ce repo https://github.com/plepe/openstreetmap-tag-translations. Les statistiques sur les tags proviennent de https://taginfo.openstreetmap.org/

Les descriptions des tags ont été généré par Mistral Large. Ce sont des phrases en français naturel. 



Performance : **98.4% recall** sur 100 cas de test.

## Installation

```bash
uv sync
```

## Usage

Conseillé de faire tourner ces scripts avec une carte graphique d'au moins 4gio de vram.

Construire les index :
```bash
uv run create-index.py
```

Recherche interactive :
```bash
rlwrap uv run search.py
```

Évaluation :
```bash
uv run test/evaluate.py
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
