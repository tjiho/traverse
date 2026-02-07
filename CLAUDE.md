# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Traverse is an OSM (OpenStreetMap) tag search tool. It enables natural language search for OSM tags in French using semantic embeddings and cross-encoder reranking.

## Commands

Build the search index (requires GPU via switcherooctl):
```bash
switcherooctl launch uv run create-index.py
```

Run the interactive search REPL:
```bash
switcherooctl launch rlwrap uv run search.py
```

Run evaluation against test cases:
```bash
uv run evaluate.py
```

## Architecture

The system uses a two-stage retrieval pipeline:

1. **Embedding Search** (`utils/embedding_search.py`): Uses `google/embeddinggemma-300m` to encode queries and search against FAISS indexes. Returns top-k candidates with cosine similarity scores.

2. **Cross-Encoder Reranking** (`utils/rerank_with_crossencoder.py`): Uses `cross-encoder/ms-marco-MiniLM-L-6-v2` to rerank candidates. Runs on CUDA.

### Data Flow

- `data/osm_wiki_tags_cleaned.json`: Source data with OSM tags, French descriptions, and enriched descriptions
- `create-index.py`: Generates separate FAISS indexes for POI and attribute categories
- `data/poi.index`, `data/attributes.index`: FAISS vector indexes
- `data/*_list.json`, `data/*_list_desc.json`: Tag names and descriptions for lookup

### Tag Categories

Tags are split into two categories:
- **POI**: Points of interest (restaurants, shops, etc.)
- **Attributes**: Characteristics (wheelchair access, cuisine type, etc.)

### Data Scripts

`data_scripts/` contains utilities for scraping, enriching, and processing OSM wiki data.

## Types

`utils/types/__init__.py` defines `TagItem` TypedDict with: `tag`, `score`, `category`, `description`.
