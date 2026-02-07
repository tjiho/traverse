#!/usr/bin/env python3
"""
Complete OSM tag scraper:
1. Scrape all keys from Map features + additional important keys
2. Get French translations from FR: wiki pages
3. Get popular tags from Taginfo API
4. Merge everything into a comprehensive dataset
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import quote, unquote
from concurrent.futures import ThreadPoolExecutor, as_completed
import os

# Configuration
WIKI_BASE = "https://wiki.openstreetmap.org"
TAGINFO_API = "https://taginfo.openstreetmap.org/api/4"
HEADERS = {
    "User-Agent": "OSM-Tag-Scraper/1.0 (traverse project)"
}
REQUEST_DELAY = 0.3
OUTPUT_FILE = "data/osm_tags_complete.json"

# All important keys to scrape
ALL_KEYS = [
    # Primary POI types
    'amenity', 'shop', 'tourism', 'leisure', 'office', 'craft',
    'healthcare', 'emergency', 'historic', 'man_made', 'club',

    # Attributes for POIs
    'cuisine', 'diet', 'payment', 'wheelchair', 'internet_access',
    'smoking', 'outdoor_seating', 'takeaway', 'delivery', 'drive_through',
    'reservation', 'capacity', 'opening_hours', 'fee', 'charge',
    'self_service', 'automated', 'bulk_purchase', 'second_hand',

    # Food & drink specific
    'drink', 'brewery', 'microbrewery', 'real_ale', 'real_cider',
    'coffee', 'breakfast', 'lunch', 'dinner', 'happy_hours',

    # Accommodation
    'rooms', 'beds', 'stars', 'accommodation',

    # Sports & activities
    'sport', 'fitness_station',

    # Infrastructure
    'building', 'landuse', 'natural', 'highway', 'railway',
    'waterway', 'aeroway', 'barrier', 'public_transport',
    'place', 'boundary', 'military', 'power', 'route',
    'aerialway', 'geological', 'telecom',

    # Access & restrictions
    'access', 'motor_vehicle', 'bicycle', 'foot', 'horse',

    # Services
    'service', 'vending', 'atm', 'money_transfer',

    # Features
    'attraction', 'information', 'board_type', 'map_type',

    # Brand & operator
    'brand', 'operator', 'network',

    # Café subtypes
    'cafe',
]


def fetch_url(url, delay=REQUEST_DELAY):
    """Fetch URL with rate limiting."""
    time.sleep(delay)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            return resp.text
    except Exception as e:
        print(f"  Error: {url} - {e}")
    return None


def get_taginfo_key_values(key, min_count=100, max_values=500):
    """Get all values for a key from Taginfo."""
    url = f"{TAGINFO_API}/key/values?key={quote(key)}&page=1&rp={max_values}&sortname=count&sortorder=desc"
    text = fetch_url(url, delay=0.2)
    if text:
        try:
            data = json.loads(text)
            values = {}
            for item in data.get('data', []):
                if item.get('count', 0) >= min_count:
                    val = item['value']
                    # Skip invalid values
                    if val and val not in ['*', 'yes', 'no', 'user defined', ''] and len(val) < 100:
                        values[val] = {
                            'count': item['count'],
                            'fraction': item.get('fraction', 0)
                        }
            return values
        except:
            pass
    return {}


def get_taginfo_popular_tags(min_count=10000):
    """Get most popular key=value combinations from Taginfo."""
    url = f"{TAGINFO_API}/tags/popular?page=1&rp=1000&sortname=count_all&sortorder=desc"
    text = fetch_url(url, delay=0.2)
    if text:
        try:
            data = json.loads(text)
            tags = []
            for item in data.get('data', []):
                if item.get('count_all', 0) >= min_count:
                    tags.append({
                        'key': item['key'],
                        'value': item['value'],
                        'count': item['count_all']
                    })
            return tags
        except:
            pass
    return []


def parse_wiki_key_page(key):
    """Parse a Key:xxx page for values and descriptions."""
    url = f"{WIKI_BASE}/wiki/Key:{quote(key)}"
    text = fetch_url(url)
    if not text:
        return None, {}

    soup = BeautifulSoup(text, 'html.parser')

    # Get key description
    key_desc = ""
    content = soup.find('div', {'id': 'mw-content-text'})
    if content:
        first_p = content.find('p')
        if first_p:
            key_desc = first_p.get_text(strip=True)[:300]

    values = {}

    # Find wikitable
    table = soup.find('table', class_='wikitable')
    if table:
        rows = table.find_all('tr')

        # Detect columns
        header = rows[0] if rows else None
        value_col, comment_col = 1, 3
        if header:
            headers = [th.get_text(strip=True).lower() for th in header.find_all(['th', 'td'])]
            if 'value' in headers:
                value_col = headers.index('value')
            if 'comment' in headers:
                comment_col = headers.index('comment')
            elif 'description' in headers:
                comment_col = headers.index('description')

        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) > value_col:
                value = cells[value_col].get_text(strip=True)
                value = re.sub(r'\s+', ' ', value).strip()

                desc = ""
                if comment_col < len(cells):
                    desc = cells[comment_col].get_text(strip=True)
                    desc = re.sub(r'\s+', ' ', desc).strip()[:300]

                if value and value not in ['*', 'user defined', 'User defined', '']:
                    values[value] = {'description_en': desc}

    return key_desc, values


def parse_wiki_fr_tag_page(key, value):
    """Get French description from FR:Tag:key=value page."""
    url = f"{WIKI_BASE}/wiki/FR:Tag:{quote(key)}%3D{quote(value)}"
    text = fetch_url(url, delay=0.15)
    if not text:
        return None

    soup = BeautifulSoup(text, 'html.parser')
    content = soup.find('div', {'id': 'mw-content-text'})
    if content:
        # Get first paragraph
        first_p = content.find('p')
        if first_p:
            text = first_p.get_text(strip=True)
            if text and len(text) > 5:
                return text[:300]
    return None


def parse_wiki_fr_key_page(key):
    """Get French key description from FR:Key:xxx page."""
    url = f"{WIKI_BASE}/wiki/FR:Key:{quote(key)}"
    text = fetch_url(url, delay=0.15)
    if not text:
        return None, {}

    soup = BeautifulSoup(text, 'html.parser')

    # Key description
    key_desc_fr = ""
    content = soup.find('div', {'id': 'mw-content-text'})
    if content:
        first_p = content.find('p')
        if first_p:
            key_desc_fr = first_p.get_text(strip=True)[:300]

    # Try to get values from French page too
    values_fr = {}
    table = soup.find('table', class_='wikitable')
    if table:
        rows = table.find_all('tr')
        for row in rows[1:]:
            cells = row.find_all(['td', 'th'])
            if len(cells) >= 2:
                # Try to find value
                value_cell = cells[1] if len(cells) > 1 else cells[0]
                value = value_cell.get_text(strip=True)

                # Find description
                desc = ""
                for cell in cells[2:]:
                    t = cell.get_text(strip=True)
                    if t and len(t) > 10:
                        desc = t[:300]
                        break

                if value and desc:
                    values_fr[value] = desc

    return key_desc_fr, values_fr


def main():
    print("=" * 60)
    print("COMPLETE OSM TAG SCRAPER")
    print("=" * 60)

    # Load existing data if available
    result = {}
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            result = json.load(f)
        print(f"\nLoaded existing data: {len(result)} keys")

    # Step 1: Get popular tags from Taginfo
    print("\n[1/4] Fetching popular tags from Taginfo...")
    popular_tags = get_taginfo_popular_tags(min_count=5000)
    print(f"  Found {len(popular_tags)} popular tag combinations")

    # Add keys from popular tags to our list
    popular_keys = set(t['key'] for t in popular_tags)
    all_keys = list(dict.fromkeys(ALL_KEYS + [k for k in popular_keys if k not in ALL_KEYS]))
    print(f"  Total keys to process: {len(all_keys)}")

    # Step 2: Process each key
    print("\n[2/4] Processing keys from wiki + Taginfo...")

    for i, key in enumerate(all_keys):
        if key in result and len(result[key].get('values', {})) > 10:
            print(f"  [{i+1}/{len(all_keys)}] {key}: already have {len(result[key]['values'])} values, skipping")
            continue

        print(f"  [{i+1}/{len(all_keys)}] {key}...", end=" ", flush=True)

        # Get wiki data (EN)
        key_desc_en, wiki_values = parse_wiki_key_page(key)

        # Get Taginfo values
        taginfo_values = get_taginfo_key_values(key, min_count=100, max_values=500)

        # Merge
        all_values = set(wiki_values.keys()) | set(taginfo_values.keys())

        if not all_values:
            print("no values found")
            continue

        key_data = {
            'description': key_desc_en or f"Key: {key}",
            'description_fr': '',
            'values': {}
        }

        for value in all_values:
            desc_en = wiki_values.get(value, {}).get('description_en', '')
            usage_count = taginfo_values.get(value, {}).get('count')

            value_data = {
                'description_en': desc_en,
                'description_fr': '',
                'description_enriched': '',
                'category': classify_tag(key, value)
            }
            if usage_count:
                value_data['usage_count'] = usage_count

            key_data['values'][value] = value_data

        result[key] = key_data
        print(f"{len(all_values)} values")

        # Save progress
        if (i + 1) % 10 == 0:
            with open(OUTPUT_FILE, 'w') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)

    # Step 3: Get French translations from wiki
    print("\n[3/4] Fetching French translations from wiki...")

    # Get FR key descriptions
    for key in list(result.keys())[:50]:  # Limit for speed
        if result[key].get('description_fr'):
            continue
        key_desc_fr, values_fr = parse_wiki_fr_key_page(key)
        if key_desc_fr:
            result[key]['description_fr'] = key_desc_fr
        # Merge FR value descriptions
        for val, desc in values_fr.items():
            if val in result[key]['values']:
                result[key]['values'][val]['description_fr'] = desc

    # Get FR tag descriptions for popular values
    print("  Fetching FR:Tag pages for popular values...")
    fr_fetch_count = 0
    for key, key_data in result.items():
        values_by_count = sorted(
            [(v, d) for v, d in key_data['values'].items() if d.get('usage_count', 0) > 1000],
            key=lambda x: x[1].get('usage_count', 0),
            reverse=True
        )[:30]  # Top 30 per key

        for value, vd in values_by_count:
            if vd.get('description_fr'):
                continue
            fr_desc = parse_wiki_fr_tag_page(key, value)
            if fr_desc:
                result[key]['values'][value]['description_fr'] = fr_desc
                fr_fetch_count += 1

        if fr_fetch_count > 500:  # Limit total FR fetches
            break

    print(f"  Fetched {fr_fetch_count} French descriptions")

    # Save final result
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Stats
    print("\n" + "=" * 60)
    print("COMPLETE!")
    print("=" * 60)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Total keys: {len(result)}")
    total_values = sum(len(v['values']) for v in result.values())
    print(f"Total values: {total_values}")

    # Category breakdown
    categories = {}
    for key_data in result.values():
        for vd in key_data['values'].values():
            cat = vd.get('category', 'other')
            categories[cat] = categories.get(cat, 0) + 1

    print(f"\nCategories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")

    # FR coverage
    with_fr = sum(1 for kd in result.values() for vd in kd['values'].values() if vd.get('description_fr'))
    print(f"\nFrench descriptions: {with_fr}/{total_values} ({100*with_fr/total_values:.1f}%)")


def classify_tag(key, value):
    """Classify a tag as 'poi', 'attribute', or 'other'."""
    poi_keys = {
        'amenity', 'shop', 'tourism', 'leisure', 'office', 'craft',
        'healthcare', 'emergency', 'historic', 'man_made', 'military',
        'aeroway', 'railway', 'public_transport', 'club', 'gambling'
    }

    attribute_keys = {
        'cuisine', 'diet', 'payment', 'opening_hours', 'wheelchair',
        'internet_access', 'smoking', 'outdoor_seating', 'takeaway',
        'delivery', 'drive_through', 'reservation', 'capacity',
        'fee', 'charge', 'access', 'service', 'operator', 'brand',
        'network', 'vending', 'drink', 'coffee', 'breakfast', 'lunch',
        'dinner', 'happy_hours', 'self_service', 'automated',
        'bulk_purchase', 'second_hand', 'attraction', 'sport',
        'cafe', 'microbrewery', 'brewery', 'real_ale'
    }

    if key in poi_keys:
        return 'poi'
    elif key in attribute_keys:
        return 'attribute'
    return 'other'


if __name__ == '__main__':
    main()
