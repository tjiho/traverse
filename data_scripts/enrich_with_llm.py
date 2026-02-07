#!/usr/bin/env python3
"""
Enrich OSM tags with LLM-generated French descriptions.
Uses Claude API or falls back to rule-based enrichment.

The goal is to create descriptions rich enough for a smaller language model
to understand and match user queries.
"""

import json
import os
import re
import time
from typing import Optional

# Try to import anthropic
try:
    import anthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False
    print("Warning: anthropic package not installed. Using rule-based enrichment only.")

INPUT_FILE = "data/osm_tags_complete.json"
OUTPUT_FILE = "data/osm_tags_enriched_llm.json"
EXISTING_FR_FILE = "data/fr-improved.json"

# Batch size for LLM calls
BATCH_SIZE = 30

# System prompt for enrichment
SYSTEM_PROMPT = """Tu es un expert OpenStreetMap qui génère des descriptions enrichies pour des tags OSM.

Pour chaque tag, tu dois générer:
1. description_fr: Une traduction française courte et claire (2-5 mots)
2. description_enriched: Une description riche en mots-clés et synonymes (30-80 mots)

La description_enriched doit contenir:
- Le terme principal en français
- Des synonymes courants
- Des exemples concrets si pertinent
- Des mots-clés que les utilisateurs pourraient chercher
- Le contexte d'utilisation

Exemples de bonnes descriptions enrichies:
- amenity=restaurant: "Restaurant. Manger, dîner, déjeuner, repas, table, serveur, menu, plat du jour, cuisine, gastronomie, salle à manger."
- shop=bakery: "Boulangerie. Pain, baguette, croissant, viennoiseries, pâtisserie, gâteaux, tartes, brioche, pain de campagne, artisan boulanger."
- cuisine=indian: "Cuisine indienne. Curry, tandoori, naan, samosa, biryani, tikka masala, épices, piment, végétarien, lassi, chapati."
- wheelchair=yes: "Accessible en fauteuil roulant. PMR, handicap, rampe d'accès, ascenseur, mobilité réduite, accessibilité."

Réponds en JSON avec ce format exact:
{"tags": [{"key": "...", "value": "...", "description_fr": "...", "description_enriched": "..."}]}"""


def load_existing_enrichments():
    """Load existing French enrichments from fr-improved.json."""
    enrichments = {}
    if os.path.exists(EXISTING_FR_FILE):
        with open(EXISTING_FR_FILE, 'r') as f:
            data = json.load(f)
            for tag_key, tag_data in data.items():
                if tag_key.startswith('tag:'):
                    # Parse tag:key=value
                    parts = tag_key[4:].split('=', 1)
                    if len(parts) == 2:
                        key, value = parts
                        enrichments[(key, value)] = {
                            'description_fr': tag_data.get('message', ''),
                            'description_enriched': tag_data.get('improved-message', '')
                        }
    return enrichments


def rule_based_enrichment(key: str, value: str, desc_en: str, desc_fr: str) -> dict:
    """Generate enrichment using rules when LLM is not available."""

    # Translation dictionary for common terms
    TRANSLATIONS = {
        # Common values
        'yes': 'oui', 'no': 'non', 'limited': 'limité', 'private': 'privé',
        'public': 'public', 'free': 'gratuit', 'customers': 'clients',

        # Amenities
        'restaurant': 'restaurant', 'cafe': 'café', 'bar': 'bar', 'pub': 'pub',
        'fast_food': 'restauration rapide', 'bank': 'banque', 'atm': 'distributeur',
        'pharmacy': 'pharmacie', 'hospital': 'hôpital', 'clinic': 'clinique',
        'school': 'école', 'university': 'université', 'library': 'bibliothèque',
        'parking': 'parking', 'fuel': 'station-service', 'toilet': 'toilettes',
        'bench': 'banc', 'post_office': 'poste', 'police': 'police',
        'cinema': 'cinéma', 'theatre': 'théâtre', 'marketplace': 'marché',

        # Shops
        'supermarket': 'supermarché', 'convenience': 'supérette', 'bakery': 'boulangerie',
        'butcher': 'boucherie', 'clothes': 'vêtements', 'shoes': 'chaussures',
        'hairdresser': 'coiffeur', 'beauty': 'beauté', 'optician': 'opticien',
        'electronics': 'électronique', 'furniture': 'meubles', 'florist': 'fleuriste',
        'books': 'librairie', 'toys': 'jouets', 'sports': 'sport', 'bicycle': 'vélo',

        # Cuisines
        'italian': 'italien', 'french': 'français', 'chinese': 'chinois',
        'japanese': 'japonais', 'indian': 'indien', 'thai': 'thaïlandais',
        'vietnamese': 'vietnamien', 'korean': 'coréen', 'mexican': 'mexicain',
        'american': 'américain', 'greek': 'grec', 'turkish': 'turc',
        'lebanese': 'libanais', 'moroccan': 'marocain', 'pizza': 'pizza',
        'burger': 'burger', 'sushi': 'sushi', 'kebab': 'kebab',
        'vegetarian': 'végétarien', 'vegan': 'végétalien', 'seafood': 'fruits de mer',

        # Tourism
        'hotel': 'hôtel', 'hostel': 'auberge', 'motel': 'motel',
        'camp_site': 'camping', 'museum': 'musée', 'gallery': 'galerie',
        'zoo': 'zoo', 'viewpoint': 'point de vue', 'information': 'information',

        # Leisure
        'park': 'parc', 'garden': 'jardin', 'playground': 'aire de jeux',
        'swimming_pool': 'piscine', 'sports_centre': 'centre sportif',
        'fitness_centre': 'salle de sport', 'stadium': 'stade',

        # Sports
        'soccer': 'football', 'tennis': 'tennis', 'basketball': 'basketball',
        'swimming': 'natation', 'cycling': 'cyclisme', 'golf': 'golf',
        'yoga': 'yoga', 'climbing': 'escalade', 'skiing': 'ski',

        # Buildings
        'residential': 'résidentiel', 'commercial': 'commercial',
        'industrial': 'industriel', 'apartment': 'appartement',
        'house': 'maison', 'church': 'église', 'mosque': 'mosquée',

        # Payment
        'cash': 'espèces', 'credit_cards': 'carte bancaire',
        'debit_cards': 'carte de débit', 'contactless': 'sans contact',
    }

    # Keyword templates for enrichment
    KEYWORDS = {
        'restaurant': 'manger, dîner, repas, cuisine, table, menu',
        'cafe': 'café, thé, petit-déjeuner, boisson chaude, pause',
        'bar': 'boire, verre, cocktail, bière, soirée, apéro',
        'bakery': 'pain, baguette, croissant, viennoiserie, pâtisserie',
        'supermarket': 'courses, alimentation, grande surface, caddie',
        'pharmacy': 'médicament, ordonnance, santé, pharmacien',
        'hospital': 'urgences, soins, médecin, santé',
        'bank': 'argent, compte, crédit, retrait',
        'hotel': 'dormir, nuit, chambre, réservation, hébergement',
        'parking': 'voiture, stationner, garer, place',
        'fuel': 'essence, diesel, carburant, gazole, plein',
        'pizza': 'pizzeria, margherita, four à bois, italien',
        'burger': 'hamburger, frites, fast-food, steak haché',
        'sushi': 'japonais, poisson cru, maki, sashimi',
        'chinese': 'wok, nouilles, riz cantonais, asiatique',
        'indian': 'curry, tandoori, naan, épices',
        'vegetarian': 'sans viande, légumes, végé',
        'vegan': 'végétalien, sans produit animal, plant-based',
    }

    # Generate description_fr
    if desc_fr:
        fr = desc_fr
    elif value in TRANSLATIONS:
        fr = TRANSLATIONS[value]
    else:
        # Convert underscore to space and capitalize
        fr = value.replace('_', ' ').title()

    # Generate enriched description
    enriched_parts = [fr]

    # Add keywords if available
    if value in KEYWORDS:
        enriched_parts.append(KEYWORDS[value])

    # Add English description snippet if useful
    if desc_en and len(desc_en) > 20:
        # Just note that we have English context
        pass

    # Build final enriched string
    enriched = '. '.join(enriched_parts) + '.'

    return {
        'description_fr': fr,
        'description_enriched': enriched
    }


def enrich_batch_with_llm(client, tags_batch: list) -> list:
    """Enrich a batch of tags using Claude API."""

    # Build prompt
    tags_text = "\n".join([
        f"- {t['key']}={t['value']}: {t.get('description_en', '')[:100]}"
        for t in tags_batch
    ])

    prompt = f"""Génère les descriptions françaises enrichies pour ces tags OSM:

{tags_text}

Réponds uniquement avec le JSON, pas d'autre texte."""

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4000,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}]
        )

        # Parse response
        text = response.content[0].text
        # Find JSON in response
        json_match = re.search(r'\{[\s\S]*\}', text)
        if json_match:
            data = json.loads(json_match.group())
            return data.get('tags', [])
    except Exception as e:
        print(f"  LLM error: {e}")

    return []


def main():
    print("=" * 60)
    print("OSM TAG ENRICHMENT WITH LLM")
    print("=" * 60)

    # Load data
    if not os.path.exists(INPUT_FILE):
        print(f"Error: {INPUT_FILE} not found. Run scrape_complete.py first.")
        return

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    print(f"Loaded {len(data)} keys")

    # Load existing enrichments
    existing = load_existing_enrichments()
    print(f"Loaded {len(existing)} existing enrichments from fr-improved.json")

    # Initialize LLM client if available
    client = None
    if HAS_ANTHROPIC and os.environ.get('ANTHROPIC_API_KEY'):
        client = anthropic.Anthropic()
        print("Using Claude API for enrichment")
    else:
        print("Using rule-based enrichment (no API key or anthropic not installed)")

    # Collect tags needing enrichment
    tags_to_enrich = []
    for key, key_data in data.items():
        for value, vd in key_data['values'].items():
            # Check if already enriched
            if (key, value) in existing:
                ex = existing[(key, value)]
                vd['description_fr'] = ex['description_fr']
                vd['description_enriched'] = ex['description_enriched']
                continue

            if vd.get('description_enriched') and len(vd['description_enriched']) > 20:
                continue

            tags_to_enrich.append({
                'key': key,
                'value': value,
                'description_en': vd.get('description_en', ''),
                'description_fr': vd.get('description_fr', ''),
                'usage_count': vd.get('usage_count', 0)
            })

    # Sort by usage count (enrich popular tags first)
    tags_to_enrich.sort(key=lambda x: x['usage_count'], reverse=True)

    print(f"Tags needing enrichment: {len(tags_to_enrich)}")

    # Enrich in batches
    enriched_count = 0

    if client:
        # Use LLM for enrichment
        for i in range(0, len(tags_to_enrich), BATCH_SIZE):
            batch = tags_to_enrich[i:i+BATCH_SIZE]
            print(f"  Processing batch {i//BATCH_SIZE + 1}/{(len(tags_to_enrich)+BATCH_SIZE-1)//BATCH_SIZE}...", end=" ", flush=True)

            results = enrich_batch_with_llm(client, batch)

            # Apply results
            for result in results:
                key = result.get('key')
                value = result.get('value')
                if key and value and key in data and value in data[key]['values']:
                    data[key]['values'][value]['description_fr'] = result.get('description_fr', '')
                    data[key]['values'][value]['description_enriched'] = result.get('description_enriched', '')
                    enriched_count += 1

            print(f"{len(results)} enriched")
            time.sleep(1)  # Rate limiting

            # Save progress every 10 batches
            if (i // BATCH_SIZE + 1) % 10 == 0:
                with open(OUTPUT_FILE, 'w') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
    else:
        # Use rule-based enrichment
        for tag in tags_to_enrich:
            key, value = tag['key'], tag['value']
            result = rule_based_enrichment(
                key, value,
                tag['description_en'],
                tag['description_fr']
            )
            data[key]['values'][value]['description_fr'] = result['description_fr']
            data[key]['values'][value]['description_enriched'] = result['description_enriched']
            enriched_count += 1

    # Save final result
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    # Stats
    print("\n" + "=" * 60)
    print("ENRICHMENT COMPLETE")
    print("=" * 60)
    print(f"Output: {OUTPUT_FILE}")
    print(f"Enriched {enriched_count} tags")

    # Coverage stats
    total = sum(len(kd['values']) for kd in data.values())
    with_enriched = sum(
        1 for kd in data.values()
        for vd in kd['values'].values()
        if vd.get('description_enriched') and len(vd['description_enriched']) > 10
    )
    print(f"Enriched descriptions: {with_enriched}/{total} ({100*with_enriched/total:.1f}%)")


if __name__ == '__main__':
    main()
