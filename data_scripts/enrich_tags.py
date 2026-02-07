#!/usr/bin/env python3
"""
Enrich OSM tags with French translations and keyword-rich descriptions.
Uses existing fr.json translations and generates enriched descriptions.
"""

import json
import re

# Common French translations for tag components
TRANSLATIONS = {
    # Amenity types
    'restaurant': 'restaurant',
    'cafe': 'café',
    'bar': 'bar',
    'pub': 'pub',
    'fast_food': 'restauration rapide',
    'food_court': 'aire de restauration',
    'ice_cream': 'glacier',
    'biergarten': 'jardin à bière',
    'bank': 'banque',
    'atm': 'distributeur automatique',
    'pharmacy': 'pharmacie',
    'hospital': 'hôpital',
    'clinic': 'clinique',
    'doctors': 'médecin',
    'dentist': 'dentiste',
    'veterinary': 'vétérinaire',
    'school': 'école',
    'kindergarten': 'maternelle',
    'college': 'lycée',
    'university': 'université',
    'library': 'bibliothèque',
    'parking': 'parking',
    'fuel': 'station-service',
    'charging_station': 'borne de recharge',
    'bicycle_parking': 'parking vélo',
    'toilet': 'toilettes',
    'toilets': 'toilettes',
    'bench': 'banc',
    'drinking_water': 'eau potable',
    'fountain': 'fontaine',
    'post_office': 'bureau de poste',
    'police': 'police',
    'fire_station': 'caserne de pompiers',
    'townhall': 'mairie',
    'community_centre': 'centre communautaire',
    'cinema': 'cinéma',
    'theatre': 'théâtre',
    'nightclub': 'discothèque',
    'casino': 'casino',
    'arts_centre': 'centre artistique',
    'place_of_worship': 'lieu de culte',
    'marketplace': 'marché',

    # Shop types
    'supermarket': 'supermarché',
    'convenience': 'supérette',
    'bakery': 'boulangerie',
    'butcher': 'boucherie',
    'greengrocer': 'primeur',
    'seafood': 'poissonnerie',
    'cheese': 'fromagerie',
    'wine': 'cave à vin',
    'alcohol': 'vente d\'alcool',
    'clothes': 'vêtements',
    'shoes': 'chaussures',
    'jewelry': 'bijouterie',
    'beauty': 'institut de beauté',
    'hairdresser': 'coiffeur',
    'optician': 'opticien',
    'electronics': 'électronique',
    'mobile_phone': 'téléphonie mobile',
    'computer': 'informatique',
    'hardware': 'quincaillerie',
    'furniture': 'meubles',
    'florist': 'fleuriste',
    'books': 'librairie',
    'toys': 'jouets',
    'sports': 'articles de sport',
    'bicycle': 'vélo',
    'car': 'automobile',
    'car_repair': 'garage auto',
    'car_parts': 'pièces auto',
    'pet': 'animalerie',
    'kiosk': 'kiosque',
    'newsagent': 'presse',
    'tobacco': 'tabac',
    'gift': 'cadeaux',
    'stationery': 'papeterie',
    'copyshop': 'reprographie',
    'laundry': 'laverie',
    'dry_cleaning': 'pressing',

    # Tourism
    'hotel': 'hôtel',
    'motel': 'motel',
    'hostel': 'auberge de jeunesse',
    'guest_house': 'chambre d\'hôtes',
    'camp_site': 'camping',
    'caravan_site': 'aire de camping-car',
    'apartment': 'appartement',
    'museum': 'musée',
    'gallery': 'galerie',
    'zoo': 'zoo',
    'aquarium': 'aquarium',
    'theme_park': 'parc d\'attractions',
    'viewpoint': 'point de vue',
    'picnic_site': 'aire de pique-nique',
    'information': 'information',
    'attraction': 'attraction',

    # Leisure
    'park': 'parc',
    'garden': 'jardin',
    'playground': 'aire de jeux',
    'pitch': 'terrain',
    'sports_centre': 'centre sportif',
    'stadium': 'stade',
    'swimming_pool': 'piscine',
    'fitness_centre': 'salle de sport',
    'golf_course': 'golf',
    'miniature_golf': 'mini-golf',
    'bowling_alley': 'bowling',
    'ice_rink': 'patinoire',
    'sauna': 'sauna',
    'beach_resort': 'plage',
    'nature_reserve': 'réserve naturelle',

    # Cuisine types
    'italian': 'italien',
    'french': 'français',
    'chinese': 'chinois',
    'japanese': 'japonais',
    'indian': 'indien',
    'thai': 'thaïlandais',
    'vietnamese': 'vietnamien',
    'korean': 'coréen',
    'mexican': 'mexicain',
    'american': 'américain',
    'greek': 'grec',
    'turkish': 'turc',
    'lebanese': 'libanais',
    'moroccan': 'marocain',
    'spanish': 'espagnol',
    'portuguese': 'portugais',
    'german': 'allemand',
    'british': 'britannique',
    'african': 'africain',
    'asian': 'asiatique',
    'mediterranean': 'méditerranéen',
    'regional': 'régional',
    'pizza': 'pizza',
    'burger': 'burger',
    'sushi': 'sushi',
    'ramen': 'ramen',
    'kebab': 'kebab',
    'sandwich': 'sandwich',
    'salad': 'salade',
    'seafood': 'fruits de mer',
    'steak_house': 'steakhouse',
    'vegetarian': 'végétarien',
    'vegan': 'végétalien',
    'coffee_shop': 'salon de café',
    'ice_cream': 'glaces',
    'crepe': 'crêperie',
    'tapas': 'tapas',

    # Sports
    'soccer': 'football',
    'football': 'football américain',
    'basketball': 'basketball',
    'tennis': 'tennis',
    'volleyball': 'volleyball',
    'handball': 'handball',
    'rugby': 'rugby',
    'hockey': 'hockey',
    'baseball': 'baseball',
    'golf': 'golf',
    'swimming': 'natation',
    'cycling': 'cyclisme',
    'running': 'course à pied',
    'athletics': 'athlétisme',
    'gymnastics': 'gymnastique',
    'fitness': 'fitness',
    'yoga': 'yoga',
    'martial_arts': 'arts martiaux',
    'boxing': 'boxe',
    'climbing': 'escalade',
    'skiing': 'ski',
    'skateboard': 'skateboard',
    'equestrian': 'équitation',
    'boules': 'pétanque',

    # Buildings
    'residential': 'résidentiel',
    'commercial': 'commercial',
    'industrial': 'industriel',
    'retail': 'commerce',
    'office': 'bureau',
    'apartments': 'appartements',
    'house': 'maison',
    'detached': 'maison individuelle',
    'terrace': 'maison mitoyenne',
    'church': 'église',
    'cathedral': 'cathédrale',
    'chapel': 'chapelle',
    'mosque': 'mosquée',
    'synagogue': 'synagogue',
    'temple': 'temple',
    'warehouse': 'entrepôt',
    'garage': 'garage',
    'shed': 'cabanon',
    'roof': 'toit',

    # Natural
    'tree': 'arbre',
    'wood': 'bois',
    'forest': 'forêt',
    'water': 'eau',
    'lake': 'lac',
    'river': 'rivière',
    'stream': 'ruisseau',
    'beach': 'plage',
    'cliff': 'falaise',
    'peak': 'sommet',
    'valley': 'vallée',
    'grassland': 'prairie',
    'wetland': 'zone humide',

    # Access/attributes
    'yes': 'oui',
    'no': 'non',
    'limited': 'limité',
    'private': 'privé',
    'public': 'public',
    'customers': 'clients',
    'permissive': 'toléré',
    'designated': 'désigné',
    'wlan': 'wifi',
    'wifi': 'wifi',
    'free': 'gratuit',
    'fee': 'payant',
}

# Keywords/synonyms for enriched descriptions
KEYWORDS = {
    'restaurant': 'manger, dîner, déjeuner, repas, cuisine, table',
    'cafe': 'café, thé, petit-déjeuner, snack, boisson chaude',
    'bar': 'alcool, bière, cocktail, soirée, apéro',
    'pub': 'bière, alcool, ambiance, soirée',
    'fast_food': 'rapide, emporter, burger, sandwich, frites',
    'bank': 'argent, compte, crédit, retrait, virement',
    'atm': 'retrait, argent, espèces, carte bancaire, DAB',
    'pharmacy': 'médicament, ordonnance, santé, pharmacien',
    'hospital': 'urgences, soins, médical, santé',
    'supermarket': 'courses, alimentation, grande surface',
    'bakery': 'pain, croissant, viennoiserie, pâtisserie',
    'hotel': 'dormir, nuit, chambre, hébergement, séjour',
    'parking': 'voiture, stationnement, garer',
    'fuel': 'essence, diesel, carburant, gazole',
    'pizza': 'pizzeria, italien, margherita, quatre fromages',
    'burger': 'hamburger, frites, fast-food',
    'sushi': 'japonais, poisson cru, maki, sashimi',
    'kebab': 'döner, viande, grillé, turc',
    'chinese': 'wok, nouilles, riz cantonais, asiatique',
    'indian': 'curry, naan, tandoori, épicé',
    'japanese': 'sushi, ramen, udon, bento',
    'italian': 'pasta, pâtes, pizza, risotto',
    'french': 'gastronomie, bistrot, brasserie, terroir',
    'vegetarian': 'sans viande, légumes, végé',
    'vegan': 'végétalien, sans produit animal, plant-based',
    'wifi': 'internet, connexion, réseau',
    'wheelchair': 'accessibilité, PMR, fauteuil roulant, handicap',
}


def translate_value(key, value):
    """Translate a tag value to French."""
    # Check direct translation
    if value in TRANSLATIONS:
        return TRANSLATIONS[value]

    # Handle underscores as spaces
    clean_value = value.replace('_', ' ')

    # Try to translate word by word
    words = value.split('_')
    translated_words = [TRANSLATIONS.get(w, w) for w in words]

    # If any word was translated, return the combined result
    if translated_words != words:
        return ' '.join(translated_words)

    # Capitalize and return as-is
    return clean_value.title()


def enrich_description(key, value, desc_en, desc_fr):
    """Create an enriched French description with synonyms and keywords."""
    parts = []

    # Start with French translation if available
    if desc_fr:
        parts.append(desc_fr.rstrip('.'))
    else:
        # Use translated value as base
        parts.append(translate_value(key, value))

    # Add keywords if available
    if value in KEYWORDS:
        parts.append(KEYWORDS[value])

    # Add English description summary if useful
    if desc_en and len(desc_en) > 20:
        # Extract key terms from English (first sentence)
        first_sentence = desc_en.split('.')[0]
        if len(first_sentence) < 100:
            # Skip if it's just the tag name repeated
            if value.replace('_', ' ').lower() not in first_sentence.lower()[:30]:
                pass  # Don't add, too redundant

    return '. '.join(parts)


def main():
    print("=== Enriching OSM Tags ===\n")

    # Load existing French translations
    with open('data/fr.json', 'r') as f:
        fr_data = json.load(f)

    # Load improved French data if available
    try:
        with open('data/fr-improved.json', 'r') as f:
            fr_improved = json.load(f)
    except:
        fr_improved = {}

    # Load scraped data
    with open('data/osm_tags_scraped.json', 'r') as f:
        scraped = json.load(f)

    # Enrich each tag
    stats = {'matched_fr': 0, 'matched_improved': 0, 'auto_translated': 0, 'total': 0}

    for key, key_data in scraped.items():
        for value, value_data in key_data['values'].items():
            stats['total'] += 1
            tag_key = f'tag:{key}={value}'

            # Get French translation from existing data
            desc_fr = ''
            if tag_key in fr_improved:
                desc_fr = fr_improved[tag_key].get('message', '')
                stats['matched_improved'] += 1
            elif tag_key in fr_data:
                desc_fr = fr_data[tag_key].get('message', '')
                stats['matched_fr'] += 1
            else:
                desc_fr = translate_value(key, value)
                stats['auto_translated'] += 1

            value_data['description_fr'] = desc_fr

            # Get enriched description
            desc_en = value_data.get('description_en', '')

            # Check if we have an improved message
            enriched = ''
            if tag_key in fr_improved:
                enriched = fr_improved[tag_key].get('improved-message', '')

            if not enriched:
                enriched = enrich_description(key, value, desc_en, desc_fr)

            value_data['description_enriched'] = enriched

    # Save enriched data
    output_file = 'data/osm_tags_enriched.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scraped, f, ensure_ascii=False, indent=2)

    print(f"Stats:")
    print(f"  Total values: {stats['total']}")
    print(f"  Matched from fr-improved.json: {stats['matched_improved']}")
    print(f"  Matched from fr.json: {stats['matched_fr']}")
    print(f"  Auto-translated: {stats['auto_translated']}")
    print(f"\nSaved to {output_file}")


if __name__ == '__main__':
    main()
