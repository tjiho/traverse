#!/usr/bin/env python3
"""
Extended enrichment dictionary for OSM tags.
Focus on popular tags that need better descriptions.
"""

ENRICHMENTS_EXTENDED = {
    # ===== INFRASTRUCTURE - WATER =====
    'waterway=stream': "Ruisseau, cours d'eau. Petit ruisseau, torrent, ru, eau courante, nature, rivière.",
    'waterway=river': "Rivière, fleuve. Cours d'eau, berges, pont, navigation, courant, baignade.",
    'waterway=canal': "Canal. Navigation fluviale, péniches, écluses, halage, vélo, promenade.",
    'waterway=ditch': "Fossé. Drainage, irrigation, écoulement, bord de route.",
    'waterway=drain': "Drain, égout. Évacuation eaux pluviales, caniveau.",
    'natural=water': "Plan d'eau. Lac, étang, mare, bassin, baignade, pêche, nature.",

    # ===== INFRASTRUCTURE - POWER =====
    'power=pole': "Poteau électrique. Bois, béton, distribution électricité, câbles.",
    'power=tower': "Pylône électrique, pylône haute tension. Métal, lignes électriques, transmission.",
    'power=line': "Ligne électrique haute tension. Câbles, pylônes, transport électricité.",
    'power=minor_line': "Ligne électrique basse tension. Distribution, quartier, maisons.",
    'power=generator': "Générateur électrique. Production électricité, énergie, centrale.",
    'power=substation': "Poste électrique, transformateur. Conversion tension, distribution.",

    # ===== INFRASTRUCTURE - ROAD =====
    'highway=crossing': "Passage piéton. Traverser la rue, zébra, feu, piétons, sécurité.",
    'highway=turning_circle': "Rond-point, demi-tour. Faire demi-tour, impasse, voiture.",
    'highway=street_lamp': "Lampadaire, réverbère. Éclairage public, lumière, nuit.",
    'highway=traffic_signals': "Feu de signalisation, feu tricolore. Rouge, vert, orange, carrefour.",
    'highway=give_way': "Cédez le passage. Priorité, intersection, panneau.",
    'highway=stop': "Stop. Arrêt obligatoire, intersection, panneau.",
    'highway=speed_camera': "Radar de vitesse. Contrôle, flash, amende.",
    'highway=bus_stop': "Arrêt de bus. Transport en commun, attendre, horaires.",
    'highway=motorway': "Autoroute. Voie rapide, péage, sortie, aire de repos.",
    'highway=trunk': "Route nationale, voie express. Grande route, axe principal.",
    'highway=primary': "Route départementale principale. Axe important, traversée.",
    'highway=secondary': "Route secondaire, départementale. Liaison, villages.",
    'highway=tertiary': "Route tertiaire, communale. Petite route, local.",
    'highway=residential': "Rue résidentielle. Quartier, maisons, vitesse limitée.",
    'highway=service': "Voie de service. Accès, parking, arrière-cour.",
    'highway=footway': "Chemin piéton, trottoir. Piétons, marcher, accessible.",
    'highway=cycleway': "Piste cyclable, voie verte. Vélo, deux-roues, sécurité.",
    'highway=path': "Sentier, chemin. Randonnée, nature, promenade.",
    'highway=track': "Chemin agricole, piste. Tracteur, forêt, terre.",
    'highway=steps': "Escalier. Marches, monter, descendre.",

    # ===== SERVICE =====
    'service=driveway': "Allée privée, entrée de garage. Accès propriété, voiture.",
    'service=parking_aisle': "Allée de parking. Circulation parking, places.",
    'service=alley': "Ruelle, venelle. Passage étroit, arrière des bâtiments.",

    # ===== BARRIER =====
    'barrier=gate': "Portail, barrière. Entrée, clôture, accès contrôlé.",
    'barrier=bollard': "Borne, potelet. Empêcher passage voitures, piétonnier.",
    'barrier=fence': "Clôture, grillage. Délimitation, propriété.",
    'barrier=wall': "Mur. Séparation, clôture, pierre, béton.",
    'barrier=hedge': "Haie. Végétation, arbustes, délimitation.",
    'barrier=lift_gate': "Barrière levante. Parking, péage, contrôle accès.",
    'barrier=kerb': "Bordure de trottoir, rebord. Chaussée, piéton.",
    'barrier=cycle_barrier': "Chicane vélo. Ralentir cyclistes, sécurité.",

    # ===== RAILWAY =====
    'railway=rail': "Voie ferrée, rails. Train, SNCF, TGV, TER, chemin de fer.",
    'railway=switch': "Aiguillage ferroviaire. Changement de voie, bifurcation.",
    'railway=level_crossing': "Passage à niveau. Traversée voie ferrée, barrières.",
    'railway=station': "Gare ferroviaire. Train, quai, billets, SNCF.",
    'railway=halt': "Halte ferroviaire. Petit arrêt, TER, campagne.",
    'railway=tram': "Voie de tramway. Tram, transport urbain.",
    'railway=subway': "Voie de métro. Metro, transport souterrain.",
    'railway=platform': "Quai de gare. Attendre train, embarquement.",
    'railway=signal': "Signal ferroviaire. Feux, sécurité, circulation trains.",
    'railway=buffer_stop': "Butoir, heurtoir. Fin de voie, terminus.",

    # ===== PUBLIC TRANSPORT =====
    'public_transport=platform': "Quai transport en commun. Bus, tram, métro, embarquement.",
    'public_transport=stop_position': "Position d'arrêt. Où s'arrête le véhicule.",
    'public_transport=station': "Station transport en commun. Gare, métro, bus.",
    'public_transport=stop_area': "Zone d'arrêt. Regroupement arrêts, correspondance.",

    # ===== PLACE =====
    'place=hamlet': "Hameau. Petit village, quelques maisons, rural, campagne.",
    'place=village': "Village. Commune rurale, église, mairie, commerces.",
    'place=town': "Ville moyenne. Centre-ville, commerces, services.",
    'place=city': "Grande ville. Métropole, centre urbain.",
    'place=suburb': "Banlieue, faubourg. Périphérie, quartier résidentiel.",
    'place=neighbourhood': "Quartier. Voisinage, secteur, zone.",
    'place=locality': "Lieu-dit. Toponyme, endroit nommé, sans habitation.",
    'place=isolated_dwelling': "Habitation isolée. Ferme, maison seule.",

    # ===== NATURAL =====
    'natural=peak': "Sommet, pic. Montagne, point culminant, altitude, randonnée.",
    'natural=tree': "Arbre. Feuillus, conifères, ombre, nature.",
    'natural=wood': "Bois, bosquet. Arbres, forêt, nature.",
    'natural=scrub': "Broussailles, maquis. Végétation basse, garrigue.",
    'natural=grassland': "Prairie, herbage. Herbe, pâturage, nature.",
    'natural=wetland': "Zone humide. Marais, marécage, tourbière, biodiversité.",
    'natural=beach': "Plage. Sable, galets, baignade, mer, vacances.",
    'natural=cliff': "Falaise. Rocher, escarpement, danger.",
    'natural=rock': "Rocher. Pierre, bloc, escalade.",
    'natural=cave_entrance': "Entrée de grotte. Caverne, spéléologie, souterrain.",

    # ===== LANDUSE =====
    'landuse=residential': "Zone résidentielle. Maisons, appartements, habitations.",
    'landuse=commercial': "Zone commerciale. Magasins, bureaux, activités.",
    'landuse=industrial': "Zone industrielle. Usines, entrepôts, fabrication.",
    'landuse=retail': "Zone commerciale, centre commercial. Magasins, shopping.",
    'landuse=farmland': "Terres agricoles. Champs, cultures, ferme.",
    'landuse=meadow': "Prairie, pré. Herbe, pâturage, foin.",
    'landuse=orchard': "Verger. Arbres fruitiers, pommes, poires.",
    'landuse=vineyard': "Vignoble. Vigne, vin, raisin, viticulture.",
    'landuse=forest': "Forêt. Bois, arbres, nature, promenade.",
    'landuse=grass': "Pelouse, gazon. Herbe, espace vert.",
    'landuse=cemetery': "Cimetière. Tombes, défunts, recueillement.",
    'landuse=construction': "Chantier. Travaux, construction, bâtiment.",

    # ===== BUILDING =====
    'building=yes': "Bâtiment. Construction, édifice.",
    'building=residential': "Bâtiment résidentiel. Maison, appartements, habitation.",
    'building=house': "Maison individuelle. Pavillon, habitation.",
    'building=apartments': "Immeuble d'appartements. Logements, résidence.",
    'building=commercial': "Bâtiment commercial. Bureaux, magasins.",
    'building=industrial': "Bâtiment industriel. Usine, entrepôt, hangar.",
    'building=retail': "Commerce, magasin. Boutique, vente.",
    'building=garage': "Garage. Voiture, stationnement, atelier.",
    'building=shed': "Cabanon, abri. Remise, outils, jardin.",
    'building=church': "Église. Culte, messe, chrétien, clocher.",
    'building=chapel': "Chapelle. Petit lieu de culte, prière.",
    'building=mosque': "Mosquée. Islam, prière, minaret.",
    'building=synagogue': "Synagogue. Judaïsme, culte, prière.",
    'building=temple': "Temple. Bouddhiste, hindou, culte.",
    'building=school': "École. Éducation, élèves, classes.",
    'building=hospital': "Hôpital. Soins, médical, santé.",
    'building=warehouse': "Entrepôt, hangar. Stockage, logistique.",
    'building=farm': "Bâtiment agricole. Ferme, grange, étable.",

    # ===== ACCESS =====
    'access=private': "Accès privé. Réservé propriétaires, interdit au public.",
    'access=customers': "Réservé aux clients. Accès clientèle.",
    'access=permissive': "Accès toléré. Passage autorisé, propriété privée.",
    'access=yes': "Accès libre. Ouvert à tous, public.",
    'access=no': "Accès interdit. Fermé au public, privé.",
    'access=destination': "Riverains autorisés. Sauf desserte locale.",
    'foot=designated': "Voie piétonne officielle. Piétons, marche.",
    'foot=yes': "Piétons autorisés. Passage à pied.",
    'foot=no': "Interdit aux piétons. Pas à pied.",
    'bicycle=designated': "Piste cyclable officielle. Vélo, cyclistes.",
    'bicycle=yes': "Vélos autorisés. Cyclistes acceptés.",
    'bicycle=no': "Interdit aux vélos. Pas de cyclistes.",
    'motor_vehicle=no': "Interdit aux véhicules motorisés. Sans voiture.",

    # ===== BOUNDARY =====
    'boundary=administrative': "Limite administrative. Frontière, commune, département.",
    'boundary=national_park': "Parc national. Nature protégée, biodiversité.",
    'boundary=protected_area': "Zone protégée. Réserve, conservation.",

    # ===== MAN_MADE =====
    'man_made=surveillance': "Caméra de surveillance, vidéosurveillance. Sécurité, CCTV.",
    'man_made=tower': "Tour, pylône. Structure haute, antenne, observation.",
    'man_made=mast': "Mât, antenne. Télécommunications, radio.",
    'man_made=silo': "Silo. Stockage grain, agriculture, céréales.",
    'man_made=storage_tank': "Réservoir, cuve. Stockage liquide, carburant.",
    'man_made=water_tower': "Château d'eau. Réservoir surélevé, distribution eau.",
    'man_made=pier': "Jetée, ponton. Accès eau, bateaux, pêche.",
    'man_made=bridge': "Pont. Traversée, rivière, route.",
    'man_made=pipeline': "Pipeline, canalisation. Transport fluides.",
    'man_made=water_well': "Puits. Eau souterraine, source.",
    'man_made=windmill': "Moulin à vent. Énergie, patrimoine.",
    'man_made=chimney': "Cheminée industrielle. Fumée, usine.",
    'man_made=crane': "Grue. Chantier, levage, construction.",
    'man_made=works': "Usine. Industrie, fabrication, production.",
    'man_made=wastewater_plant': "Station d'épuration. Traitement eaux usées.",

    # ===== AEROWAY =====
    'aeroway=aerodrome': "Aérodrome, aéroport. Avions, vols, piste.",
    'aeroway=runway': "Piste d'atterrissage. Décollage, avion.",
    'aeroway=taxiway': "Voie de circulation aéroport. Roulage avion.",
    'aeroway=terminal': "Terminal aéroport. Embarquement, enregistrement.",
    'aeroway=helipad': "Héliport, hélistation. Hélicoptère, atterrissage.",

    # ===== VENDING =====
    'vending=parking_tickets': "Distributeur tickets parking. Horodateur, paiement.",
    'vending=drinks': "Distributeur boissons. Sodas, café, eau.",
    'vending=cigarettes': "Distributeur cigarettes. Tabac, automatique.",
    'vending=food': "Distributeur nourriture. Snacks, sandwichs.",
    'vending=coffee': "Distributeur café. Machine à café, expresso.",
    'vending=fuel': "Distributeur carburant 24h. Station automatique.",
    'vending=condoms': "Distributeur préservatifs. Contraception.",
    'vending=bicycle_tube': "Distributeur chambre à air vélo. Réparation.",

    # ===== OPERATORS =====
    'operator=Enedis': "Enedis. Réseau électrique, distribution, compteur.",
    'operator=SNCF': "SNCF. Train, gare, TGV, TER, Intercités.",
    'operator=RATP': "RATP. Métro Paris, bus, tramway, RER.",
    'operator=Orange': "Orange. Téléphone, internet, fibre, mobile.",

    # ===== CAPACITY =====
    'capacity=1': "Capacité: 1 place.",
    'capacity=2': "Capacité: 2 places.",
    'capacity=4': "Capacité: 4 places.",
    'capacity=6': "Capacité: 6 places.",
    'capacity=10': "Capacité: 10 places.",
    'capacity=20': "Capacité: 20 places.",

    # ===== HISTORIC =====
    'historic=memorial': "Mémorial. Monument commémoratif, souvenir, guerre.",
    'historic=monument': "Monument historique. Patrimoine, histoire.",
    'historic=castle': "Château. Forteresse, patrimoine, visite, médiéval.",
    'historic=ruins': "Ruines. Vestiges, archéologie, ancien.",
    'historic=archaeological_site': "Site archéologique. Fouilles, antiquité.",
    'historic=manor': "Manoir. Demeure noble, patrimoine.",
    'historic=wayside_cross': "Croix de chemin. Calvaire, religion.",
    'historic=wayside_shrine': "Oratoire, niche. Petite chapelle, prière.",
    'historic=boundary_stone': "Borne frontière. Limite, territoire.",
    'historic=tomb': "Tombe, tombeau. Sépulture, cimetière.",
    'historic=fort': "Fort, fortification. Militaire, défense, histoire.",
    'historic=city_gate': "Porte de ville. Entrée fortification, remparts.",

    # ===== EMERGENCY =====
    'emergency=fire_hydrant': "Bouche d'incendie. Pompiers, eau, secours.",
    'emergency=defibrillator': "Défibrillateur, DAE. Urgence cardiaque, premiers secours.",
    'emergency=phone': "Téléphone d'urgence. SOS, borne d'appel.",
    'emergency=assembly_point': "Point de rassemblement. Évacuation, sécurité.",
    'emergency=first_aid_kit': "Trousse de secours. Premiers soins.",

    # ===== OFFICE =====
    'office=government': "Administration, services publics. Mairie, préfecture.",
    'office=company': "Siège social, bureaux. Entreprise.",
    'office=insurance': "Assurance. Contrats, sinistres, couverture.",
    'office=estate_agent': "Agence immobilière. Vente, location, logement.",
    'office=lawyer': "Cabinet d'avocat. Juridique, droit, conseil.",
    'office=accountant': "Expert-comptable. Comptabilité, fiscalité.",
    'office=tax_advisor': "Conseiller fiscal. Impôts, déclaration.",
    'office=notary': "Notaire. Actes, immobilier, succession.",
    'office=employment_agency': "Agence pour l'emploi, Pôle Emploi. Travail, chômage.",
    'office=travel_agent': "Agence de voyage. Vacances, billets, séjours.",
    'office=telecommunication': "Opérateur télécom. Téléphone, internet, mobile.",
    'office=ngo': "ONG, association. Humanitaire, bénévolat.",

    # ===== CRAFT =====
    'craft=carpenter': "Menuisier, charpentier. Bois, meubles, construction.",
    'craft=electrician': "Électricien. Installation électrique, dépannage.",
    'craft=plumber': "Plombier. Tuyauterie, sanitaires, chauffage.",
    'craft=painter': "Peintre en bâtiment. Peinture, décoration.",
    'craft=locksmith': "Serrurier. Clés, serrures, ouverture.",
    'craft=tailor': "Tailleur, couturier. Vêtements, retouches.",
    'craft=shoemaker': "Cordonnier. Chaussures, réparation, clés.",
    'craft=baker': "Boulanger. Pain, artisan, four.",
    'craft=butcher': "Boucher. Viande, abattage, artisan.",
    'craft=brewery': "Brasserie artisanale. Bière, craft beer, houblon.",
    'craft=winery': "Domaine viticole. Vin, cave, dégustation.",
    'craft=photographer': "Photographe. Photos, portraits, studio.",
    'craft=jeweller': "Bijoutier, joaillier. Bijoux, or, réparation.",
    'craft=watchmaker': "Horloger. Montres, réparation, entretien.",

    # ===== HEALTHCARE =====
    'healthcare=doctor': "Cabinet médical. Médecin généraliste, consultation.",
    'healthcare=dentist': "Cabinet dentaire. Dents, soins dentaires.",
    'healthcare=pharmacy': "Pharmacie. Médicaments, ordonnance.",
    'healthcare=hospital': "Hôpital. Urgences, hospitalisation, soins.",
    'healthcare=clinic': "Clinique. Soins, chirurgie, consultation.",
    'healthcare=physiotherapist': "Kinésithérapeute. Kiné, rééducation, massage.",
    'healthcare=psychotherapist': "Psychothérapeute. Psychologue, thérapie, santé mentale.",
    'healthcare=optometrist': "Opticien, optométriste. Vue, lunettes, lentilles.",
    'healthcare=podiatrist': "Podologue. Pieds, semelles, soins.",
    'healthcare=laboratory': "Laboratoire d'analyses. Prise de sang, examens.",
    'healthcare=blood_donation': "Don du sang. Donner son sang, EFS.",
    'healthcare=midwife': "Sage-femme. Accouchement, grossesse, naissance.",
    'healthcare=nursing_home': "Maison de retraite, EHPAD. Personnes âgées.",
    'healthcare=rehabilitation': "Centre de rééducation. Convalescence, soins.",

    # ===== ADDITIONAL SHOPS =====
    'shop=mall': "Centre commercial, galerie marchande. Shopping, magasins.",
    'shop=department_store': "Grand magasin. Galeries Lafayette, Printemps.",
    'shop=wholesale': "Grossiste. Vente en gros, professionnels.",
    'shop=garden_centre': "Jardinerie. Plantes, jardinage, fleurs, outils.",
    'shop=car_parts': "Pièces auto. Accessoires voiture, réparation.",
    'shop=tyres': "Pneus, garage. Pneumatiques, montage, équilibrage.",
    'shop=hearing_aids': "Audioprothésiste. Appareils auditifs, surdité.",
    'shop=medical_supply': "Matériel médical. Orthopédie, fauteuil, béquilles.",
    'shop=e-cigarette': "Cigarette électronique, vapoteuse. Vape, e-liquide.",
    'shop=cannabis': "CBD, cannabis légal. Chanvre, bien-être.",
    'shop=trade': "Commerce de gros. BtoB, professionnel.",

    # ===== ADDITIONAL AMENITY =====
    'amenity=vending_machine': "Distributeur automatique. Boissons, snacks, 24h.",
    'amenity=parcel_locker': "Consigne à colis. Amazon Locker, retrait, livraison.",
    'amenity=recycling': "Point de recyclage. Tri, poubelles, verre, papier.",
    'amenity=waste_basket': "Poubelle publique. Déchets, jeter.",
    'amenity=waste_disposal': "Déchetterie. Déchets encombrants, recyclage.",
    'amenity=loading_dock': "Quai de chargement. Livraison, camions.",
    'amenity=parking_entrance': "Entrée parking. Accès souterrain, barrière.",
    'amenity=motorcycle_parking': "Parking moto. Deux-roues, stationnement.",
    'amenity=taxi': "Station de taxi. Taxis, voiture avec chauffeur.",
    'amenity=bus_station': "Gare routière. Bus longue distance, autocar.",
    'amenity=ferry_terminal': "Terminal ferry. Bateau, traversée, port.",
    'amenity=car_wash': "Station de lavage. Laver voiture, nettoyage.",
    'amenity=vehicle_inspection': "Contrôle technique. CT, véhicule, sécurité.",
    'amenity=driving_school': "Auto-école. Permis de conduire, code, leçons.",
    'amenity=language_school': "École de langues. Anglais, cours, formation.",
    'amenity=music_school': "École de musique. Conservatoire, cours, instruments.",
    'amenity=social_facility': "Établissement social. Aide sociale, CCAS.",
    'amenity=childcare': "Garde d'enfants. Crèche, nounou, garderie.",
    'amenity=events_venue': "Salle des fêtes. Événements, mariages, soirées.",
    'amenity=conference_centre': "Centre de conférences. Séminaires, congrès.",
    'amenity=exhibition_centre': "Parc des expositions. Salons, foires.",
    'amenity=public_bookcase': "Boîte à livres. Livre gratuit, échange, partage.",
    'amenity=toy_library': "Ludothèque. Jeux, jouets, emprunt.",
}


def apply_extended_enrichments():
    """Apply extended enrichments to the data file."""
    import json

    input_file = "data/osm_tags_enriched_final.json"
    output_file = "data/osm_tags_enriched_final.json"

    with open(input_file, 'r') as f:
        data = json.load(f)

    applied = 0
    for combined_key, enriched in ENRICHMENTS_EXTENDED.items():
        parts = combined_key.split('=', 1)
        if len(parts) == 2:
            key, value = parts
            if key in data and value in data[key]['values']:
                vd = data[key]['values'][value]
                # Update if current enrichment is short
                current = vd.get('description_enriched', '')
                if len(current) < len(enriched):
                    vd['description_enriched'] = enriched
                    # Also update description_fr if needed
                    fr = enriched.split('.')[0].strip()
                    if len(fr) > len(vd.get('description_fr', '')):
                        vd['description_fr'] = fr
                    applied += 1

    with open(output_file, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Applied {applied} extended enrichments")
    return applied


if __name__ == '__main__':
    apply_extended_enrichments()
