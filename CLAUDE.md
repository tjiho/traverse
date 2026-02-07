# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Traverse is a semantic search tool for OpenStreetMap tags. It converts French natural language queries ("où manger", "parking vélo") into OSM tags (`amenity=restaurant`, `amenity=bicycle_parking`).

## Commands

Build search indexes (requires GPU via switcherooctl):
```bash
switcherooctl launch uv run create-index.py
```

Run interactive search:
```bash
switcherooctl launch uv run search.py
```

Run evaluation (98.8% recall on 100 test cases):
```bash
uv run test/evaluate.py
```

## Architecture

Two-stage retrieval pipeline:

1. **Embedding Search** (`utils/embedding_search.py`): Uses `intfloat/multilingual-e5-base` with "query:"/"passage:" prefixes. Searches both POI and attribute indexes, returns top candidates.

2. **Cross-Encoder Reranking** (`utils/rerank_with_crossencoder.py`): Uses `BAAI/bge-reranker-v2-m3` (multilingual) to rerank candidates. Runs on CUDA.

### Data Flow

- `data/osm_wiki_tags_cleaned.json`: Source data with OSM tags, French descriptions, and enriched descriptions
- `create-index.py`: Generates separate FAISS indexes for POI and attribute categories
- `data/poi.index`, `data/attributes.index`: FAISS vector indexes
- `data/*_list.json`, `data/*_list_desc.json`: Tag names and descriptions for lookup

### Tag Categories

- **POI**: Points of interest (restaurants, shops, etc.)
- **Attributes**: Characteristics (cuisine type, wheelchair access, etc.)

Search queries both indexes and merges results (`search_multi` function).

## Key Files

- `utils/embedding_search.py`: `search_multi()` - main search function
- `utils/rerank_with_crossencoder.py`: `rerank()` - cross-encoder reranking
- `utils/query_expansion.py`: LLM-based query expansion (experimental, not used)
- `test/evaluate.py`: Evaluation script with recall/MRR metrics
- `data/search_cases.json`: Test cases for evaluation

## Future Work

- API REST (FastAPI) - planned
- Automatic POI/attribute detection (tested, heuristics best at 87%)
- Query expansion with LLM (implemented but adds latency without improving recall)
