#!/usr/bin/env python3
"""
Fix poor descriptions for important tags.
Focus on POI and attributes that users would search for.
"""

import json

INPUT_FILE = "data/osm_wiki_tags.json"
OUTPUT_FILE = "data/osm_wiki_tags.json"

# Manual fixes for important tags with bad descriptions
FIXES = {
    # Sport
    ('sport', 'soccer'): ('Football', 'Football, foot. Match, ballon, équipe, terrain, but, Ligue 1, supporters, stade.'),
    ('sport', 'tennis'): ('Tennis', 'Tennis. Court, raquette, balle, Roland-Garros, simple, double, set.'),
    ('sport', 'basketball'): ('Basketball', 'Basketball, basket. Panier, ballon, terrain, NBA, dunk, match.'),
    ('sport', 'volleyball'): ('Volleyball', 'Volleyball, volley. Filet, ballon, équipe, beach-volley, smash.'),
    ('sport', 'swimming'): ('Natation', 'Natation. Piscine, nager, crawl, brasse, papillon, compétition.'),
    ('sport', 'golf'): ('Golf', 'Golf. Parcours, green, club, putting, trou, handicap, caddie.'),
    ('sport', 'athletics'): ('Athlétisme', 'Athlétisme. Piste, course, saut, lancer, marathon, sprint.'),
    ('sport', 'cycling'): ('Cyclisme', 'Cyclisme, vélo. Course, Tour de France, VTT, piste, vélodrome.'),
    ('sport', 'rugby'): ('Rugby', 'Rugby. Ballon ovale, essai, mêlée, Top 14, XV de France.'),
    ('sport', 'hockey'): ('Hockey', 'Hockey. Crosse, puck, patinoire, hockey sur glace, équipe.'),
    ('sport', 'baseball'): ('Baseball', 'Baseball. Batte, balle, lanceur, home run, MLB.'),
    ('sport', 'cricket'): ('Cricket', 'Cricket. Batte, guichet, lanceur, test match.'),
    ('sport', 'skateboard'): ('Skateboard', 'Skateboard, skate. Skatepark, rampe, tricks, planche.'),
    ('sport', 'ice_skating'): ('Patinage', 'Patinage sur glace. Patinoire, patins, artistique, vitesse.'),
    ('sport', 'climbing'): ('Escalade', 'Escalade. Mur, bloc, voie, grimper, salle, falaise.'),
    ('sport', 'fitness'): ('Fitness', 'Fitness, musculation. Salle de sport, cardio, machines, coach.'),
    ('sport', 'multi'): ('Multisport', 'Terrain multisport. City stade, foot, basket, plusieurs sports.'),
    ('sport', 'boules'): ('Pétanque', 'Pétanque, boules. Terrain, cochonnet, lancer, Provence, pastis.'),
    ('sport', 'table_tennis'): ('Ping-pong', 'Tennis de table, ping-pong. Raquette, table, balle.'),
    ('sport', 'equestrian'): ('Équitation', 'Équitation. Cheval, manège, cavalier, centre équestre, poney.'),
    ('sport', 'gymnastics'): ('Gymnastique', 'Gymnastique. Gym, agrès, poutre, sol, barres.'),
    ('sport', 'martial_arts'): ('Arts martiaux', 'Arts martiaux. Judo, karaté, taekwondo, dojo, ceinture.'),
    ('sport', 'boxing'): ('Boxe', 'Boxe. Ring, gants, combat, KO, entraînement.'),
    ('sport', 'archery'): ('Tir à l\'arc', 'Tir à l\'arc. Arc, flèches, cible, archerie.'),
    ('sport', 'shooting'): ('Tir sportif', 'Stand de tir, tir sportif. Armes, cibles, club.'),
    ('sport', 'badminton'): ('Badminton', 'Badminton. Raquette, volant, filet, terrain.'),
    ('sport', 'squash'): ('Squash', 'Squash. Raquette, balle, court, mur.'),
    ('sport', 'padel'): ('Padel', 'Padel. Raquette, terrain vitré, sport tendance.'),
    ('sport', 'petanque'): ('Pétanque', 'Pétanque. Boules, cochonnet, terrain, Provence.'),
    ('sport', 'fencing'): ('Escrime', 'Escrime. Épée, fleuret, sabre, assaut, touche.'),
    ('sport', 'diving'): ('Plongée', 'Plongée sous-marine. Bouteille, masque, palmes, mer.'),
    ('sport', 'sailing'): ('Voile', 'Voile, bateau. Naviguer, régate, port, mer.'),
    ('sport', 'surfing'): ('Surf', 'Surf. Planche, vagues, océan, spot, glisse.'),
    ('sport', 'kayak'): ('Kayak', 'Kayak, canoë. Pagaie, rivière, mer, randonnée nautique.'),
    ('sport', 'rowing'): ('Aviron', 'Aviron. Bateau, rames, rivière, compétition.'),

    # Route
    ('route', 'bus'): ('Ligne de bus', 'Ligne de bus. Transport en commun, arrêts, horaires, trajet.'),
    ('route', 'hiking'): ('Sentier de randonnée', 'Sentier de randonnée, GR. Marche, nature, balisage, trek, promenade.'),
    ('route', 'bicycle'): ('Itinéraire cyclable', 'Itinéraire cyclable, véloroute. Piste vélo, voie verte, cyclotourisme.'),
    ('route', 'road'): ('Route', 'Route nationale ou départementale. Axe routier, numérotation.'),
    ('route', 'train'): ('Ligne de train', 'Ligne de train, chemin de fer. SNCF, TGV, TER, gares.'),
    ('route', 'tram'): ('Ligne de tramway', 'Ligne de tramway. Tram, transport urbain, stations.'),
    ('route', 'subway'): ('Ligne de métro', 'Ligne de métro. Transport souterrain, stations, RER.'),
    ('route', 'ferry'): ('Ligne de ferry', 'Ligne de ferry, traversée maritime. Bateau, port.'),
    ('route', 'ski'): ('Piste de ski', 'Piste de ski, domaine skiable. Montagne, neige, remontées.'),
    ('route', 'mtb'): ('Parcours VTT', 'Parcours VTT, vélo tout terrain. Sentier, montagne, descente.'),
    ('route', 'running'): ('Parcours de course', 'Parcours de course à pied, running. Jogging, trail.'),
    ('route', 'fitness_trail'): ('Parcours santé', 'Parcours santé, parcours vita. Exercices, nature, sport.'),

    # Service
    ('service', 'driveway'): ('Allée privée', 'Allée privée, entrée de garage. Accès propriété, voiture, maison.'),
    ('service', 'parking_aisle'): ('Allée de parking', 'Allée de parking. Circulation dans le parking, accès places.'),
    ('service', 'alley'): ('Ruelle', 'Ruelle, venelle. Passage étroit, arrière des bâtiments.'),
    ('service', 'yard'): ('Cour', 'Cour, dépôt. Zone de manœuvre, stockage, industriel.'),
    ('service', 'spur'): ('Embranchement ferroviaire', 'Voie ferrée secondaire, embranchement. Desserte industrielle.'),
    ('service', 'siding'): ('Voie de garage', 'Voie de garage ferroviaire. Stationnement trains, évitement.'),
    ('service', 'drive-through'): ('Drive', 'Drive, service au volant. Commander sans descendre, fast-food.'),
    ('service', 'emergency_access'): ('Accès pompiers', 'Voie d\'accès pompiers, secours. Urgence, intervention.'),

    # Place
    ('place', 'isolated_dwelling'): ('Habitation isolée', 'Maison isolée, ferme. Habitation seule, campagne, écart.'),
    ('place', 'islet'): ('Îlot', 'Îlot, petite île. Rocher, récif, mer.'),
    ('place', 'neighbourhood'): ('Quartier', 'Quartier, voisinage. Secteur, zone résidentielle, nom de quartier.'),
    ('place', 'plot'): ('Parcelle', 'Parcelle, lotissement. Terrain à bâtir, division.'),
    ('place', 'farm'): ('Ferme', 'Ferme, exploitation agricole. Agriculture, bâtiments agricoles.'),
    ('place', 'allotments'): ('Jardins familiaux', 'Jardins ouvriers, jardins familiaux. Parcelles, potager, légumes.'),

    # Man_made
    ('man_made', 'manhole'): ('Regard', 'Plaque d\'égout, regard. Accès souterrain, réseau, assainissement.'),
    ('man_made', 'utility_pole'): ('Poteau', 'Poteau électrique ou téléphone. Câbles, réseau, bois.'),
    ('man_made', 'street_cabinet'): ('Armoire technique', 'Armoire technique, coffret. Électricité, télécom, fibre.'),
    ('man_made', 'pipeline'): ('Pipeline', 'Canalisation, pipeline. Transport gaz, pétrole, eau.'),
    ('man_made', 'monitoring_station'): ('Station de mesure', 'Station de mesure, capteur. Qualité air, météo, environnement.'),

    # Access
    ('motor_vehicle', 'private'): ('Interdit véhicules', 'Interdit aux véhicules motorisés sauf riverains. Voie privée.'),
    ('motor_vehicle', 'no'): ('Interdit véhicules', 'Interdit aux véhicules motorisés. Piéton, vélo uniquement.'),
    ('foot', 'use_sidepath'): ('Utiliser trottoir', 'Piétons doivent utiliser le trottoir ou chemin parallèle.'),
    ('bicycle', 'use_sidepath'): ('Utiliser piste cyclable', 'Cyclistes doivent utiliser la piste cyclable parallèle.'),
    ('bicycle', 'dismount'): ('Vélo à pied', 'Descendre de vélo, pied à terre obligatoire. Zone piétonne.'),

    # Highway links
    ('highway', 'secondary_link'): ('Bretelle secondaire', 'Bretelle vers route secondaire. Entrée, sortie, échangeur.'),
    ('highway', 'tertiary_link'): ('Bretelle tertiaire', 'Bretelle vers route tertiaire. Raccordement, accès.'),
    ('highway', 'trunk_link'): ('Bretelle voie express', 'Bretelle vers voie express. Entrée, sortie, échangeur.'),
    ('highway', 'motorway_link'): ('Bretelle autoroute', 'Bretelle d\'autoroute. Entrée, sortie, péage, aire.'),
    ('highway', 'primary_link'): ('Bretelle principale', 'Bretelle vers route principale. Raccordement, giratoire.'),

    # Opening hours
    ('opening_hours', '24/7'): ('24h/24', 'Ouvert 24h/24, 7j/7. Toujours ouvert, non-stop, nuit.'),

    # Capacity
    ('capacity', '1'): ('1 place', 'Capacité d\'une place. Parking, vélo, fauteuil.'),
    ('capacity', '2'): ('2 places', 'Capacité de deux places.'),
    ('capacity', '4'): ('4 places', 'Capacité de quatre places.'),
    ('capacity', '5'): ('5 places', 'Capacité de cinq places.'),
    ('capacity', '10'): ('10 places', 'Capacité de dix places.'),

    # Operator
    ('operator', 'SNCF Réseau'): ('SNCF Réseau', 'SNCF Réseau. Gestionnaire voies ferrées, rails, aiguillages.'),
    ('operator', 'RTE'): ('RTE', 'RTE, Réseau Transport Électricité. Lignes haute tension, pylônes.'),
    ('operator', 'Enedis'): ('Enedis', 'Enedis. Distribution électricité, compteurs, réseau basse tension.'),

    # Power
    ('power', 'catenary_mast'): ('Mât caténaire', 'Poteau de caténaire. Alimentation électrique trains, tramway.'),
}


def main():
    print("=== Fixing poor descriptions ===\n")

    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    fixed = 0
    for (key, value), (fr, enriched) in FIXES.items():
        if key in data and value in data[key]['values']:
            vd = data[key]['values'][value]
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            fixed += 1

    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Fixed {fixed} descriptions")
    print(f"Saved to {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
