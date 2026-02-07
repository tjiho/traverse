#!/usr/bin/env python3
"""
Scrape OSM Wiki Map Features to generate a structured JSON file with tags.
Uses the wiki pages + Taginfo API for usage counts.
"""

import requests
from bs4 import BeautifulSoup
import json
import re
import time
from urllib.parse import quote, unquote
from collections import defaultdict

# Configuration
WIKI_BASE = "https://wiki.openstreetmap.org"
TAGINFO_API = "https://taginfo.openstreetmap.org/api/4"
HEADERS = {
    "User-Agent": "OSM-Tag-Scraper/1.0 (traverse project; contact: scraper@example.com)"
}

# Rate limiting
REQUEST_DELAY = 0.5  # seconds between requests


def fetch_page(url):
    """Fetch a wiki page and return BeautifulSoup object."""
    time.sleep(REQUEST_DELAY)
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        return BeautifulSoup(resp.text, 'html.parser')
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return None


def get_taginfo_count(key, value=None):
    """Get usage count from Taginfo API."""
    time.sleep(REQUEST_DELAY / 2)
    try:
        if value:
            url = f"{TAGINFO_API}/tag/stats?key={quote(key)}&value={quote(value)}"
        else:
            url = f"{TAGINFO_API}/key/stats?key={quote(key)}"

        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if 'data' in data and len(data['data']) > 0:
                # Sum all counts (nodes, ways, relations)
                total = sum(item.get('count', 0) for item in data['data'])
                return total
    except Exception as e:
        print(f"Taginfo error for {key}={value}: {e}")
    return None


def get_taginfo_key_values(key, min_count=100):
    """Get all values for a key from Taginfo with their counts."""
    time.sleep(REQUEST_DELAY)
    try:
        url = f"{TAGINFO_API}/key/values?key={quote(key)}&page=1&rp=500&sortname=count&sortorder=desc"
        resp = requests.get(url, headers=HEADERS, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            values = {}
            for item in data.get('data', []):
                if item.get('count', 0) >= min_count:
                    values[item['value']] = {
                        'count': item['count'],
                        'fraction': item.get('fraction', 0)
                    }
            return values
    except Exception as e:
        print(f"Taginfo key values error for {key}: {e}")
    return {}


def parse_map_features_page():
    """Parse the main Map features page to get all key categories."""
    url = f"{WIKI_BASE}/wiki/Map_features"
    soup = fetch_page(url)
    if not soup:
        return []

    keys = []
    # Find all links to Key: pages
    for link in soup.find_all('a', href=True):
        href = link['href']
        if '/wiki/Key:' in href:
            key_name = href.split('/wiki/Key:')[-1]
            key_name = unquote(key_name)
            if key_name and key_name not in keys:
                keys.append(key_name)

    return keys


def parse_key_page(key):
    """Parse a Key:xxx page to get all values and their descriptions."""
    url = f"{WIKI_BASE}/wiki/Key:{quote(key)}"
    soup = fetch_page(url)
    if not soup:
        return None, {}

    # Get key description from first paragraph
    key_description = ""
    content = soup.find('div', {'id': 'mw-content-text'})
    if content:
        first_p = content.find('p')
        if first_p:
            key_description = first_p.get_text(strip=True)

    values = {}

    # Find main wikitable (Key, Value, Element, Comment structure)
    table = soup.find('table', class_='wikitable')
    if not table:
        return key_description, values

    rows = table.find_all('tr')

    # Detect column structure from header
    header_row = rows[0] if rows else None
    value_col = 1  # Default: second column
    comment_col = 3  # Default: fourth column

    if header_row:
        headers = [th.get_text(strip=True).lower() for th in header_row.find_all(['th', 'td'])]
        if 'value' in headers:
            value_col = headers.index('value')
        if 'comment' in headers:
            comment_col = headers.index('comment')
        elif 'description' in headers:
            comment_col = headers.index('description')

    for row in rows[1:]:  # Skip header
        cells = row.find_all(['td', 'th'])
        if len(cells) > max(value_col, comment_col):
            # Get value from value column
            value_cell = cells[value_col]
            value_text = value_cell.get_text(strip=True)

            # Clean up value text (remove wiki markup artifacts)
            value_text = re.sub(r'\s+', ' ', value_text).strip()

            # Get description from comment column
            comment_cell = cells[comment_col] if comment_col < len(cells) else None
            description = ""
            if comment_cell:
                description = comment_cell.get_text(strip=True)
                # Clean up description
                description = re.sub(r'\s+', ' ', description).strip()

            if value_text and value_text not in ['*', 'user defined', 'User defined', '']:
                values[value_text] = {
                    'description_en': description
                }

    return key_description, values


def get_wiki_translation(key, value=None, lang='fr'):
    """Try to get French translation from wiki."""
    time.sleep(REQUEST_DELAY)
    try:
        if value:
            url = f"{WIKI_BASE}/wiki/{lang.upper()}:Tag:{quote(key)}={quote(value)}"
        else:
            url = f"{WIKI_BASE}/wiki/{lang.upper()}:Key:{quote(key)}"

        resp = requests.get(url, headers=HEADERS, timeout=10)
        if resp.status_code == 200:
            soup = BeautifulSoup(resp.text, 'html.parser')
            content = soup.find('div', {'id': 'mw-content-text'})
            if content:
                first_p = content.find('p')
                if first_p:
                    return first_p.get_text(strip=True)
    except:
        pass
    return None


def classify_tag(key, value):
    """Classify a tag as 'poi', 'attribute', or 'other'."""
    # POI keys - things that represent places/points of interest
    poi_keys = {
        'amenity', 'shop', 'tourism', 'leisure', 'office', 'craft',
        'healthcare', 'emergency', 'historic', 'man_made', 'military',
        'aeroway', 'railway', 'public_transport', 'sport'
    }

    # Attribute keys - things that describe other features
    attribute_keys = {
        'cuisine', 'diet', 'payment', 'opening_hours', 'wheelchair',
        'internet_access', 'smoking', 'outdoor_seating', 'takeaway',
        'delivery', 'drive_through', 'reservation', 'capacity',
        'fee', 'charge', 'access', 'service', 'operator', 'brand',
        'network', 'ref', 'name', 'alt_name', 'description',
        'website', 'phone', 'email', 'fax', 'contact', 'social',
        'image', 'source', 'note', 'fixme', 'check_date'
    }

    if key in poi_keys:
        return 'poi'
    elif key in attribute_keys:
        return 'attribute'
    elif ':' in key:
        base_key = key.split(':')[0]
        if base_key in attribute_keys:
            return 'attribute'

    return 'other'


def enrich_description(key, value, description_en):
    """Create an enriched French description with synonyms and keywords."""
    # This is a placeholder - in production you might use:
    # - Translation API
    # - LLM for generating synonyms
    # - Pre-built dictionary

    # For now, return a basic enriched version
    base = description_en or f"{key}={value}"
    return base


def main():
    print("=== OSM Wiki Scraper ===\n")

    # Step 1: Get all keys from Map features page
    print("1. Fetching main Map features page...")
    keys = parse_map_features_page()
    print(f"   Found {len(keys)} keys\n")

    # Filter to most important keys for initial scrape
    # POI-centric keys first
    priority_keys = [
        # Primary POI types
        'amenity', 'shop', 'tourism', 'leisure', 'office', 'craft',
        'healthcare', 'emergency', 'historic', 'man_made',
        # Attributes for POIs
        'cuisine', 'diet', 'payment', 'wheelchair', 'internet_access',
        'smoking', 'outdoor_seating', 'takeaway', 'delivery',
        'drive_through', 'reservation', 'sport', 'cafe',
        # Infrastructure
        'building', 'landuse', 'natural', 'highway', 'railway',
        'waterway', 'aeroway', 'barrier', 'public_transport',
        'place', 'boundary', 'military', 'power', 'route'
    ]

    # Use priority keys that exist in our scraped list
    keys_to_process = [k for k in priority_keys if k in keys]
    print(f"   Processing {len(keys_to_process)} priority keys\n")

    result = {}

    # Step 2: For each key, get values from wiki and taginfo
    for i, key in enumerate(keys_to_process):
        print(f"\n[{i+1}/{len(keys_to_process)}] Processing: {key}")

        # Get wiki data
        key_desc, wiki_values = parse_key_page(key)
        print(f"   Wiki: {len(wiki_values)} values")

        # Get taginfo data for more complete coverage
        taginfo_values = get_taginfo_key_values(key, min_count=500)
        print(f"   Taginfo: {len(taginfo_values)} values (count>=500)")

        # Merge data sources
        all_values = set(wiki_values.keys()) | set(taginfo_values.keys())

        if not all_values:
            print(f"   No values found, skipping")
            continue

        key_data = {
            'description': key_desc[:200] if key_desc else f"Key: {key}",
            'values': {}
        }

        for value in sorted(all_values):
            # Get description from wiki
            desc_en = wiki_values.get(value, {}).get('description_en', '')

            # Get usage count from taginfo
            usage_count = None
            if value in taginfo_values:
                usage_count = taginfo_values[value]['count']

            # Classify
            category = classify_tag(key, value)

            # Build value entry - skip French translation for now (too slow)
            # Will be enriched later with LLM or translation API
            value_data = {
                'description_en': desc_en[:300] if desc_en else '',
                'description_fr': '',  # To be filled later
                'description_enriched': '',  # To be filled later
                'category': category
            }

            if usage_count:
                value_data['usage_count'] = usage_count

            key_data['values'][value] = value_data

        result[key] = key_data
        print(f"   Total: {len(key_data['values'])} values added")

        # Save progress periodically
        if (i + 1) % 5 == 0:
            with open('data/osm_tags_scraped.json', 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
            print(f"   [Progress saved]")

    # Step 3: Save final result
    output_file = 'data/osm_tags_scraped.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"\n=== Done! Saved to {output_file} ===")
    print(f"Total keys: {len(result)}")
    total_values = sum(len(v['values']) for v in result.values())
    print(f"Total values: {total_values}")


if __name__ == '__main__':
    main()
