#!/usr/bin/env python3
"""
Fetch French translations from OSM wiki FR: pages.
Focuses on the most important/popular tags.
"""

import json
import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import quote
import re

WIKI_BASE = "https://wiki.openstreetmap.org"
HEADERS = {"User-Agent": "OSM-FR-Scraper/1.0"}
INPUT_FILE = "data/osm_tags_complete.json"
OUTPUT_FILE = "data/osm_tags_complete.json"


def fetch_fr_tag(key, value):
    """Fetch French description for a tag."""
    url = f"{WIKI_BASE}/wiki/FR:Tag:{quote(key)}%3D{quote(value)}"
    try:
        time.sleep(0.15)
        resp = requests.get(url, headers=HEADERS, timeout=15)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            content = soup.find('div', {'id': 'mw-content-text'})
            if content:
                # Get first paragraph
                p = content.find('p')
                if p:
                    text = p.get_text(strip=True)
                    text = re.sub(r'\s+', ' ', text)
                    if text and len(text) > 3:
                        return text[:250]
    except:
        pass
    return None


def main():
    print("=== Fetching French translations from wiki ===\n")

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    # Priority keys for POIs and attributes
    priority_keys = [
        'amenity', 'shop', 'tourism', 'leisure', 'office', 'craft',
        'cuisine', 'sport', 'healthcare', 'emergency', 'historic',
        'diet', 'payment', 'wheelchair', 'smoking', 'takeaway',
        'vending', 'attraction', 'information'
    ]

    total_fetched = 0
    total_found = 0

    for key in priority_keys:
        if key not in data:
            continue

        print(f"Processing {key}...", end=" ", flush=True)
        key_fetched = 0
        key_found = 0

        # Get values sorted by usage
        values = sorted(
            data[key]['values'].items(),
            key=lambda x: x[1].get('usage_count', 0),
            reverse=True
        )

        # Fetch top 50 values per key
        for value, vd in values[:50]:
            if vd.get('description_fr') and len(vd['description_fr']) > 5:
                continue  # Already have French

            fr_desc = fetch_fr_tag(key, value)
            key_fetched += 1

            if fr_desc:
                data[key]['values'][value]['description_fr'] = fr_desc
                key_found += 1

        total_fetched += key_fetched
        total_found += key_found
        print(f"{key_found}/{key_fetched} found")

        # Save progress
        with open(OUTPUT_FILE, 'w') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nTotal: {total_found}/{total_fetched} French descriptions found")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
