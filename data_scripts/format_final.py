#!/usr/bin/env python3
"""
Format the enriched OSM tags into the final desired JSON structure.
"""

import json
import re


def clean_description(text):
    """Clean wiki markup artifacts from description."""
    if not text:
        return ""
    # Remove wiki link artifacts
    text = re.sub(r'\[\[.*?\|(.*?)\]\]', r'\1', text)
    text = re.sub(r'\[\[(.*?)\]\]', r'\1', text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Clean multiple spaces
    text = re.sub(r'\s+', ' ', text)
    # Remove artifacts like "amenity=xxx"
    text = re.sub(r'[a-z_]+=[a-z_]+', '', text)
    # Limit length
    return text.strip()[:300]


def main():
    # Load enriched data
    with open('data/osm_tags_enriched.json', 'r') as f:
        data = json.load(f)

    # Format into final structure
    result = {}

    for key, key_data in data.items():
        # Clean key description
        key_desc = clean_description(key_data.get('description', f'Key: {key}'))
        if not key_desc or key_desc.startswith('=*'):
            key_desc = f"Clé {key}"

        key_entry = {
            'description': key_desc,
            'values': {}
        }

        for value, vd in key_data['values'].items():
            # Skip empty or user-defined values
            if not value or value in ['*', 'user_defined', 'User defined']:
                continue

            # Build value entry
            entry = {
                'description_fr': vd.get('description_fr', ''),
                'description_enriched': vd.get('description_enriched', ''),
                'category': vd.get('category', 'other')
            }

            # Add usage_count if present
            if 'usage_count' in vd and vd['usage_count']:
                entry['usage_count'] = vd['usage_count']

            key_entry['values'][value] = entry

        # Only add keys with values
        if key_entry['values']:
            result[key] = key_entry

    # Save final result
    output_file = 'data/osm_tags_final.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Print stats
    print(f"=== Final OSM Tags File ===")
    print(f"Output: {output_file}")
    print(f"Total keys: {len(result)}")
    total_values = sum(len(v['values']) for v in result.values())
    print(f"Total values: {total_values}")

    # Show category breakdown
    categories = {'poi': 0, 'attribute': 0, 'other': 0}
    for key_data in result.values():
        for vd in key_data['values'].values():
            cat = vd.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1

    print(f"\nCategories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")


if __name__ == '__main__':
    main()
