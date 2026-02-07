#!/usr/bin/env python3
"""
Batch enrichment of OSM tags using Claude API.
Run this script to enrich tags that still have poor descriptions.

Usage:
  export ANTHROPIC_API_KEY=your_key
  python3 enrich_llm_batch.py
"""

import json
import os
import time
import re

try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False

INPUT_FILE = "data/osm_tags_enriched_final.json"
OUTPUT_FILE = "data/osm_tags_enriched_final.json"

SYSTEM_PROMPT = """Tu génères des descriptions françaises enrichies pour des tags OpenStreetMap.

Pour chaque tag key=value, tu dois fournir:
1. description_fr: Traduction française courte (2-5 mots)
2. description_enriched: Description riche avec synonymes et mots-clés (40-80 mots)

La description_enriched doit permettre à un petit modèle de langage de matcher des requêtes utilisateur.
Elle doit contenir: le terme principal, des synonymes, des exemples concrets, des mots-clés de recherche.

Exemples:
- highway=crossing → "Passage piéton. Traverser la rue, zébra, bandes blanches, feu piéton, sécurité, carrefour."
- natural=peak → "Sommet, pic de montagne. Point culminant, altitude, randonnée, vue panoramique, alpinisme."
- service=driveway → "Allée privée, entrée de garage. Accès propriété, voiture, portail, résidentiel."

Réponds en JSON: {"tags": [{"key": "...", "value": "...", "description_fr": "...", "description_enriched": "..."}]}"""


def enrich_batch(client, tags):
    """Enrich a batch of tags using Claude."""
    tags_text = "\n".join([
        f"- {t['key']}={t['value']}" + (f" (EN: {t['desc_en'][:60]})" if t.get('desc_en') else "")
        for t in tags
    ])

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": f"Enrichis ces tags OSM:\n\n{tags_text}"}]
        )

        text = response.content[0].text
        match = re.search(r'\{[\s\S]*\}', text)
        if match:
            data = json.loads(match.group())
            return data.get('tags', [])
    except Exception as e:
        print(f"  Error: {e}")

    return []


def main():
    if not HAS_ANTHROPIC:
        print("Error: anthropic package not installed.")
        print("Install with: pip install anthropic")
        return

    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set.")
        print("Export your key: export ANTHROPIC_API_KEY=your_key")
        return

    print("=== LLM Batch Enrichment ===\n")

    client = anthropic.Anthropic(api_key=api_key)

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    # Find tags needing enrichment (popular but poor description)
    tags_to_enrich = []
    for key, kd in data.items():
        for value, vd in kd['values'].items():
            enriched = vd.get('description_enriched', '')
            usage = vd.get('usage_count', 0)
            # Poor enrichment and popular
            if len(enriched) < 40 and usage > 500:
                tags_to_enrich.append({
                    'key': key,
                    'value': value,
                    'usage': usage,
                    'desc_en': vd.get('description_en', '')
                })

    # Sort by usage
    tags_to_enrich.sort(key=lambda x: -x['usage'])

    print(f"Tags to enrich: {len(tags_to_enrich)}")

    # Process in batches
    BATCH_SIZE = 25
    total_batches = (len(tags_to_enrich) + BATCH_SIZE - 1) // BATCH_SIZE
    enriched_count = 0

    for i in range(0, len(tags_to_enrich), BATCH_SIZE):
        batch = tags_to_enrich[i:i+BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        print(f"  Batch {batch_num}/{total_batches}...", end=" ", flush=True)

        results = enrich_batch(client, batch)

        # Apply results
        for result in results:
            key = result.get('key')
            value = result.get('value')
            if key and value and key in data and value in data[key]['values']:
                vd = data[key]['values'][value]
                if result.get('description_fr'):
                    vd['description_fr'] = result['description_fr']
                if result.get('description_enriched'):
                    vd['description_enriched'] = result['description_enriched']
                    enriched_count += 1

        print(f"{len(results)} enriched")

        # Save progress
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        time.sleep(1)  # Rate limiting

        # Optional: limit total batches for testing
        # if batch_num >= 5:
        #     break

    print(f"\nDone! Enriched {enriched_count} tags")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
