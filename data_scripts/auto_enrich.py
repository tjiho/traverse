#!/usr/bin/env python3
"""
Automatic enrichment based on patterns and category knowledge.
Generates rich descriptions for tags without good enrichments.
"""

import json
import re

INPUT_FILE = "data/osm_tags_enriched_final.json"
OUTPUT_FILE = "data/osm_tags_enriched_final.json"

# Category-based templates for generating enrichments
TEMPLATES = {
    'cuisine': {
        'pattern': lambda v: f"Cuisine {v.replace('_', ' ')}.",
        'suffix': "Spécialités, plats typiques, gastronomie, saveurs."
    },
    'sport': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()}.",
        'suffix': "Sport, activité physique, club, entraînement, compétition."
    },
    'shop': {
        'pattern': lambda v: f"Magasin {v.replace('_', ' ')}.",
        'suffix': "Commerce, acheter, boutique, vente."
    },
    'office': {
        'pattern': lambda v: f"Bureau {v.replace('_', ' ')}.",
        'suffix': "Services professionnels, entreprise, conseil."
    },
    'craft': {
        'pattern': lambda v: f"Artisan {v.replace('_', ' ')}.",
        'suffix': "Métier, artisanat, savoir-faire, fabrication."
    },
    'healthcare': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()}.",
        'suffix': "Santé, soins, médical, consultation, traitement."
    },
    'amenity': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()}.",
        'suffix': "Service, équipement, infrastructure."
    },
    'leisure': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()}.",
        'suffix': "Loisirs, détente, activité, sortie."
    },
    'tourism': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()}.",
        'suffix': "Tourisme, visite, hébergement, vacances."
    },
    'building': {
        'pattern': lambda v: f"Bâtiment {v.replace('_', ' ')}.",
        'suffix': "Construction, édifice, architecture."
    },
    'historic': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()} historique.",
        'suffix': "Patrimoine, histoire, monument, visite culturelle."
    },
    'natural': {
        'pattern': lambda v: f"{v.replace('_', ' ').title()}.",
        'suffix': "Nature, environnement, paysage, géographie."
    },
    'landuse': {
        'pattern': lambda v: f"Zone {v.replace('_', ' ')}.",
        'suffix': "Occupation du sol, terrain, aménagement."
    },
}

# Word translations for common terms
WORD_TRANS = {
    # General
    'yes': 'oui', 'no': 'non', 'limited': 'limité', 'only': 'uniquement',
    'free': 'gratuit', 'private': 'privé', 'public': 'public',

    # Building types
    'residential': 'résidentiel', 'commercial': 'commercial', 'industrial': 'industriel',
    'retail': 'commerce', 'office': 'bureau', 'warehouse': 'entrepôt',
    'garage': 'garage', 'shed': 'cabanon', 'barn': 'grange', 'farm': 'ferme',
    'church': 'église', 'chapel': 'chapelle', 'mosque': 'mosquée', 'temple': 'temple',
    'school': 'école', 'university': 'université', 'hospital': 'hôpital',
    'hotel': 'hôtel', 'apartments': 'appartements', 'house': 'maison',
    'detached': 'individuelle', 'terrace': 'mitoyenne', 'dormitory': 'dortoir',
    'civic': 'civique', 'government': 'gouvernement', 'public': 'public',
    'train_station': 'gare', 'transportation': 'transport', 'hangar': 'hangar',
    'greenhouse': 'serre', 'stable': 'écurie', 'sty': 'porcherie',
    'roof': 'toit', 'ruins': 'ruines', 'construction': 'construction',

    # Natural
    'water': 'eau', 'wood': 'bois', 'forest': 'forêt', 'tree': 'arbre',
    'grass': 'herbe', 'meadow': 'prairie', 'scrub': 'broussailles',
    'heath': 'lande', 'wetland': 'marais', 'beach': 'plage', 'sand': 'sable',
    'cliff': 'falaise', 'rock': 'rocher', 'peak': 'sommet', 'valley': 'vallée',
    'ridge': 'crête', 'saddle': 'col', 'volcano': 'volcan', 'glacier': 'glacier',
    'spring': 'source', 'hot_spring': 'source chaude', 'geyser': 'geyser',
    'cave_entrance': 'grotte', 'sinkhole': 'doline', 'coastline': 'côte',

    # Highway
    'motorway': 'autoroute', 'trunk': 'nationale', 'primary': 'départementale',
    'secondary': 'secondaire', 'tertiary': 'tertiaire', 'residential': 'résidentielle',
    'service': 'service', 'footway': 'piéton', 'cycleway': 'piste cyclable',
    'path': 'sentier', 'track': 'piste', 'steps': 'escalier',
    'crossing': 'passage piéton', 'traffic_signals': 'feux', 'stop': 'stop',
    'give_way': 'cédez', 'speed_camera': 'radar', 'bus_stop': 'arrêt bus',
    'turning_circle': 'demi-tour', 'street_lamp': 'lampadaire',

    # Waterway
    'river': 'rivière', 'stream': 'ruisseau', 'canal': 'canal',
    'drain': 'drain', 'ditch': 'fossé', 'waterfall': 'cascade',
    'dam': 'barrage', 'weir': 'déversoir', 'lock': 'écluse',
    'dock': 'dock', 'boatyard': 'chantier naval',

    # Railway
    'rail': 'voie ferrée', 'tram': 'tramway', 'subway': 'métro',
    'light_rail': 'métro léger', 'station': 'gare', 'halt': 'halte',
    'platform': 'quai', 'crossing': 'passage à niveau', 'signal': 'signal',
    'switch': 'aiguillage', 'turntable': 'plaque tournante',

    # Barrier
    'fence': 'clôture', 'wall': 'mur', 'hedge': 'haie', 'gate': 'portail',
    'bollard': 'borne', 'lift_gate': 'barrière', 'swing_gate': 'portillon',
    'kerb': 'bordure', 'block': 'bloc', 'chain': 'chaîne',

    # Power
    'pole': 'poteau', 'tower': 'pylône', 'line': 'ligne',
    'cable': 'câble', 'generator': 'générateur', 'substation': 'poste',
    'transformer': 'transformateur', 'plant': 'centrale',

    # Service types
    'driveway': 'allée', 'parking_aisle': 'allée parking', 'alley': 'ruelle',
    'yard': 'cour', 'spur': 'embranchement', 'siding': 'voie de garage',
    'crossover': 'croisement',

    # Sport
    'soccer': 'football', 'football': 'foot US', 'basketball': 'basket',
    'tennis': 'tennis', 'volleyball': 'volley', 'handball': 'handball',
    'rugby': 'rugby', 'baseball': 'baseball', 'cricket': 'cricket',
    'golf': 'golf', 'swimming': 'natation', 'cycling': 'cyclisme',
    'running': 'course', 'athletics': 'athlétisme', 'gymnastics': 'gym',
    'fitness': 'fitness', 'yoga': 'yoga', 'climbing': 'escalade',
    'skiing': 'ski', 'skating': 'patinage', 'equestrian': 'équitation',
    'martial_arts': 'arts martiaux', 'boxing': 'boxe', 'wrestling': 'lutte',
    'boules': 'pétanque', 'table_tennis': 'ping-pong', 'badminton': 'badminton',
    'squash': 'squash', 'padel': 'padel', 'archery': 'tir arc',
    'shooting': 'tir', 'fencing': 'escrime', 'diving': 'plongée',
    'surfing': 'surf', 'sailing': 'voile', 'canoe': 'canoë', 'kayak': 'kayak',
    'motor': 'sport auto', 'karting': 'karting', 'motocross': 'motocross',

    # Cuisine nationalities
    'afghan': 'afghane', 'african': 'africaine', 'american': 'américaine',
    'arab': 'arabe', 'asian': 'asiatique', 'australian': 'australienne',
    'austrian': 'autrichienne', 'balkan': 'balkanique', 'belgian': 'belge',
    'brazilian': 'brésilienne', 'british': 'britannique', 'burmese': 'birmane',
    'cambodian': 'cambodgienne', 'caribbean': 'caribéenne', 'chinese': 'chinoise',
    'croatian': 'croate', 'cuban': 'cubaine', 'czech': 'tchèque',
    'danish': 'danoise', 'egyptian': 'égyptienne', 'ethiopian': 'éthiopienne',
    'filipino': 'philippine', 'french': 'française', 'german': 'allemande',
    'greek': 'grecque', 'hawaiian': 'hawaïenne', 'hungarian': 'hongroise',
    'indian': 'indienne', 'indonesian': 'indonésienne', 'iranian': 'iranienne',
    'irish': 'irlandaise', 'israeli': 'israélienne', 'italian': 'italienne',
    'jamaican': 'jamaïcaine', 'japanese': 'japonaise', 'korean': 'coréenne',
    'lao': 'laotienne', 'lebanese': 'libanaise', 'malagasy': 'malgache',
    'malaysian': 'malaisienne', 'mediterranean': 'méditerranéenne',
    'mexican': 'mexicaine', 'mongolian': 'mongole', 'moroccan': 'marocaine',
    'nepalese': 'népalaise', 'pakistani': 'pakistanaise', 'peruvian': 'péruvienne',
    'polish': 'polonaise', 'portuguese': 'portugaise', 'romanian': 'roumaine',
    'russian': 'russe', 'scandinavian': 'scandinave', 'senegalese': 'sénégalaise',
    'serbian': 'serbe', 'spanish': 'espagnole', 'sri_lankan': 'sri-lankaise',
    'swedish': 'suédoise', 'swiss': 'suisse', 'syrian': 'syrienne',
    'taiwanese': 'taïwanaise', 'thai': 'thaïlandaise', 'tibetan': 'tibétaine',
    'tunisian': 'tunisienne', 'turkish': 'turque', 'ukrainian': 'ukrainienne',
    'vietnamese': 'vietnamienne', 'yemeni': 'yéménite',
    'international': 'internationale', 'regional': 'régionale', 'local': 'locale',

    # Cuisine dishes
    'pizza': 'pizza', 'burger': 'burgers', 'sushi': 'sushi', 'ramen': 'ramen',
    'kebab': 'kebab', 'gyros': 'gyros', 'falafel': 'falafel', 'tacos': 'tacos',
    'tapas': 'tapas', 'curry': 'curry', 'noodle': 'nouilles', 'pasta': 'pâtes',
    'rice': 'riz', 'soup': 'soupe', 'salad': 'salade', 'sandwich': 'sandwich',
    'crepe': 'crêpes', 'waffle': 'gaufres', 'pancake': 'pancakes',
    'ice_cream': 'glaces', 'donut': 'donuts', 'cake': 'gâteaux',
    'coffee': 'café', 'tea': 'thé', 'juice': 'jus', 'smoothie': 'smoothie',
    'breakfast': 'petit-déj', 'brunch': 'brunch', 'lunch': 'déjeuner',
    'seafood': 'fruits de mer', 'fish': 'poisson', 'chicken': 'poulet',
    'steak': 'steak', 'barbecue': 'barbecue', 'grill': 'grillade',
    'vegetarian': 'végétarien', 'vegan': 'végétalien',
}


def translate_value(value):
    """Translate a value to French."""
    if value in WORD_TRANS:
        return WORD_TRANS[value]

    # Try word by word
    words = value.replace('_', ' ').split()
    translated = []
    for w in words:
        w_lower = w.lower()
        if w_lower in WORD_TRANS:
            translated.append(WORD_TRANS[w_lower])
        else:
            translated.append(w.title())

    return ' '.join(translated)


def generate_enriched(key, value, desc_en, existing_fr):
    """Generate an enriched description based on patterns."""

    # Translate value to French
    fr = existing_fr if existing_fr and len(existing_fr) > 2 else translate_value(value)

    # Apply template if available
    if key in TEMPLATES:
        tpl = TEMPLATES[key]
        base = tpl['pattern'](translate_value(value))
        suffix = tpl['suffix']
        enriched = f"{base} {suffix}"
    else:
        # Generic enrichment
        enriched = f"{fr}."

    # Add English context if available and useful
    if desc_en and len(desc_en) > 20:
        # Extract first sentence
        first = desc_en.split('.')[0].strip()
        if len(first) > 10 and len(first) < 100:
            # Don't add if it's just the tag repeated
            if value.replace('_', ' ').lower() not in first.lower()[:20]:
                enriched = f"{enriched} {first}."

    # Ensure minimum length
    if len(enriched) < 30:
        enriched = f"{fr}. Service, équipement, infrastructure."

    return fr, enriched


def main():
    print("=== Auto Enrichment ===\n")

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    enriched_count = 0

    for key, kd in data.items():
        for value, vd in kd['values'].items():
            current = vd.get('description_enriched', '')

            # Only enrich if current is poor
            if len(current) < 40:
                fr, enriched = generate_enriched(
                    key, value,
                    vd.get('description_en', ''),
                    vd.get('description_fr', '')
                )

                if len(enriched) > len(current):
                    vd['description_enriched'] = enriched
                    if len(fr) > len(vd.get('description_fr', '')):
                        vd['description_fr'] = fr
                    enriched_count += 1

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Auto-enriched {enriched_count} tags")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
