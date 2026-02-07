#!/usr/bin/env python3
"""
Generate the final JSON file in the requested format.

Format:
{
  "amenity": {
    "description": "Équipements et services",
    "values": {
      "restaurant": {
        "description_fr": "Restaurant",
        "description_enriched": "Restaurant. Endroit où manger...",
        "category": "poi",
        "usage_count": 1500000
      }
    }
  }
}
"""

import json
import re

INPUT_FILE = "data/osm_tags_enriched_final.json"
OUTPUT_FILE = "data/osm_wiki_tags.json"

# French descriptions for main keys
KEY_DESCRIPTIONS = {
    'amenity': "Équipements et services publics",
    'shop': "Commerces et magasins",
    'tourism': "Tourisme et hébergement",
    'leisure': "Loisirs et détente",
    'office': "Bureaux et services professionnels",
    'craft': "Artisanat et métiers",
    'cuisine': "Type de cuisine",
    'diet': "Régimes alimentaires",
    'payment': "Modes de paiement",
    'wheelchair': "Accessibilité fauteuil roulant",
    'internet_access': "Accès internet",
    'smoking': "Politique tabac",
    'outdoor_seating': "Terrasse extérieure",
    'takeaway': "Vente à emporter",
    'delivery': "Livraison",
    'drive_through': "Service au volant",
    'reservation': "Réservation",
    'capacity': "Capacité",
    'opening_hours': "Horaires d'ouverture",
    'fee': "Tarification",
    'charge': "Frais",
    'sport': "Sports et activités sportives",
    'building': "Bâtiments",
    'landuse': "Occupation du sol",
    'natural': "Éléments naturels",
    'highway': "Routes et voies",
    'railway': "Voies ferrées",
    'waterway': "Cours d'eau",
    'aeroway': "Aérien",
    'barrier': "Barrières et obstacles",
    'public_transport': "Transport en commun",
    'place': "Lieux et localités",
    'boundary': "Limites administratives",
    'military': "Installations militaires",
    'power': "Réseau électrique",
    'route': "Itinéraires",
    'healthcare': "Santé",
    'emergency': "Urgences et secours",
    'historic': "Patrimoine historique",
    'man_made': "Structures artificielles",
    'access': "Restrictions d'accès",
    'service': "Type de service",
    'vending': "Distributeurs automatiques",
    'attraction': "Attractions",
    'information': "Points d'information",
    'brand': "Marques",
    'operator': "Opérateurs",
    'network': "Réseaux",
    'club': "Clubs et associations",
}


def clean_enriched(text):
    """Clean and validate enriched description."""
    if not text:
        return ""
    # Clean whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    # Ensure ends with period
    if text and not text.endswith('.'):
        text += '.'
    return text


def main():
    print("=== Generating Final JSON ===\n")

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    result = {}

    for key, key_data in data.items():
        # Get key description
        key_desc = KEY_DESCRIPTIONS.get(key, key_data.get('description', f"Clé {key}"))

        key_entry = {
            'description': key_desc,
            'values': {}
        }

        for value, vd in key_data['values'].items():
            # Skip invalid values
            if not value or value in ['*', 'user_defined', 'User defined', '']:
                continue

            # Build value entry
            entry = {
                'description_fr': vd.get('description_fr', value.replace('_', ' ').title()),
                'description_enriched': clean_enriched(vd.get('description_enriched', '')),
                'category': vd.get('category', 'other')
            }

            # Add usage_count if significant
            usage = vd.get('usage_count')
            if usage and usage > 0:
                entry['usage_count'] = usage

            key_entry['values'][value] = entry

        # Only add keys with values
        if key_entry['values']:
            result[key] = key_entry

    # Save result
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    # Stats
    total_keys = len(result)
    total_values = sum(len(v['values']) for v in result.values())

    categories = {}
    enriched_good = 0
    for kd in result.values():
        for vd in kd['values'].values():
            cat = vd['category']
            categories[cat] = categories.get(cat, 0) + 1
            if len(vd['description_enriched']) >= 40:
                enriched_good += 1

    print(f"Output: {OUTPUT_FILE}")
    print(f"Total keys: {total_keys}")
    print(f"Total values: {total_values}")
    print(f"\nCategories:")
    for cat, count in sorted(categories.items(), key=lambda x: -x[1]):
        print(f"  {cat}: {count}")
    print(f"\nGood enrichments (>=40 chars): {enriched_good} ({100*enriched_good/total_values:.1f}%)")


if __name__ == '__main__':
    main()
