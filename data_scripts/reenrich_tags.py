#!/usr/bin/env python3
"""
Re-enrich tags listed in tags_to_reenrich.txt with proper French descriptions.
Replace generic "Service, équipement, infrastructure" with useful descriptions.
"""

import json

INPUT_FILE = "data/osm_wiki_tags_cleaned.json"
OUTPUT_FILE = "data/osm_wiki_tags_cleaned.json"
TAGS_FILE = "data/tags_to_reenrich.txt"

# Complete enrichment dictionary
ENRICHMENTS = {
    # =====================
    # AMENITY
    # =====================
    ('amenity', 'buildings'): ('Bâtiments', 'Ensemble de bâtiments. Immeubles, constructions, complexe.'),
    ('amenity', 'art_school'): ('École d\'art', 'École d\'art, beaux-arts. Peinture, dessin, sculpture, cours artistiques.'),
    ('amenity', 'rescue_station'): ('Station de secours', 'Station de secours, sauvetage. Plage, montagne, premiers secours.'),
    ('amenity', 'storage'): ('Stockage', 'Espace de stockage, garde-meuble. Entreposer, box, location.'),
    ('amenity', 'sanitary_dump_station'): ('Station de vidange', 'Aire de vidange camping-car. Eaux usées, WC chimique, aire service.'),
    ('amenity', 'reception_desk'): ('Réception', 'Bureau d\'accueil, réception. Accueil visiteurs, information.'),
    ('amenity', 'Comercio'): ('Commerce', 'Commerce, boutique. Magasin, achats.'),
    ('amenity', 'loading_dock'): ('Quai de chargement', 'Quai de chargement, livraison. Camions, marchandises, dock.'),
    ('amenity', 'electricite'): ('Électricité', 'Installation électrique. Courant, branchement.'),
    ('amenity', 'boathouse'): ('Hangar à bateaux', 'Hangar à bateaux, abri nautique. Stockage embarcations, canoës, aviron.'),
    ('amenity', 'vending_machine;waste_basket'): ('Distributeur et poubelle', 'Distributeur automatique avec poubelle. Snacks, boissons, déchets.'),
    ('amenity', 'library_dropoff'): ('Boîte retour livres', 'Boîte de retour bibliothèque. Rendre livres 24h/24, dépôt.'),
    ('amenity', 'parking_exit'): ('Sortie parking', 'Sortie de parking. Quitter stationnement, barrière sortie.'),
    ('amenity', 'church'): ('Église', 'Église, lieu de culte chrétien. Messe, paroisse, catholique, protestant.'),
    ('amenity', 'animal_training'): ('Dressage animaux', 'Centre de dressage, éducation canine. Chien, obéissance, comportementaliste.'),
    ('amenity', 'love_hotel'): ('Love hotel', 'Love hotel, hôtel de charme. Chambre à l\'heure, couple, discret, intimité.'),
    ('amenity', 'health_centre'): ('Centre de santé', 'Centre de santé, maison médicale. Médecins, consultations, soins.'),
    ('amenity', 'concert_hall'): ('Salle de concert', 'Salle de concert, auditorium. Musique live, spectacles, orchestre.'),
    ('amenity', 'commercial'): ('Zone commerciale', 'Zone commerciale, centre commercial. Magasins, boutiques, shopping.'),
    ('amenity', 'food'): ('Alimentation', 'Point alimentation, nourriture. Manger, repas.'),
    ('amenity', 'animal_boarding'): ('Pension animaux', 'Pension pour animaux, garde. Chien, chat, vacances, chenil, chatterie.'),
    ('amenity', 'funeral_home'): ('Pompes funèbres', 'Pompes funèbres, funérarium. Obsèques, décès, cercueil, enterrement.'),
    ('amenity', 'building'): ('Bâtiment', 'Bâtiment, construction. Édifice, immeuble.'),
    ('amenity', 'auditorium'): ('Auditorium', 'Auditorium, salle conférence. Événements, présentations, assemblée.'),
    ('amenity', 'tourist_bus_parking'): ('Parking cars tourisme', 'Parking autocars, bus touristiques. Stationnement groupes.'),
    ('amenity', 'customs'): ('Douane', 'Bureau de douane, poste frontière. Déclaration, contrôle, import, export.'),
    ('amenity', 'cemetery'): ('Cimetière', 'Cimetière, nécropole. Tombes, funérailles, recueillement, défunts.'),
    ('amenity', 'waiting_room'): ('Salle d\'attente', 'Salle d\'attente. Patienter, attendre son tour.'),
    ('amenity', 'game_feeding'): ('Nourrissage gibier', 'Point de nourrissage gibier. Affouragement, sangliers, cerfs.'),
    ('amenity', 'stage'): ('Scène', 'Scène, estrade. Spectacles, concerts, représentations.'),
    ('amenity', 'laboratory'): ('Laboratoire', 'Laboratoire d\'analyses. Prise de sang, examens médicaux, résultats.'),
    ('amenity', 'mobility_hub'): ('Pôle mobilité', 'Pôle d\'échange multimodal. Bus, vélo, covoiturage, transports.'),
    ('amenity', 'first_aid_school'): ('École secourisme', 'Formation premiers secours. PSC1, sauveteur, BAFA, Croix-Rouge.'),
    ('amenity', 'washing_place'): ('Lavoir', 'Lavoir public, buanderie. Laver linge, ancien lavoir.'),
    ('amenity', 'proposed'): ('Projet', 'Équipement en projet, prévu. Construction future.'),
    ('amenity', 'lifeboat'): ('Canot sauvetage', 'Station canot de sauvetage. SNSM, secours en mer.'),
    ('amenity', 'retail shops'): ('Commerces', 'Commerces de détail, boutiques. Magasins, achats.'),
    ('amenity', 'seat'): ('Siège', 'Siège, banc public. S\'asseoir, repos.'),
    ('amenity', 'garages'): ('Garages', 'Garages, boxes. Stationnement couvert, voiture.'),
    ('amenity', 'lost_property_office'): ('Objets trouvés', 'Bureau des objets trouvés. Récupérer affaires perdues.'),
    ('amenity', 'sign'): ('Panneau', 'Panneau d\'information, signalétique.'),
    ('amenity', 'mobile_library'): ('Bibliobus', 'Bibliothèque mobile, bibliobus. Livres villages, tournée.'),
    ('amenity', 'meeting_point'): ('Point de rencontre', 'Point de rencontre, rendez-vous. Retrouver quelqu\'un.'),
    ('amenity', 'prison'): ('Prison', 'Prison, établissement pénitentiaire. Maison d\'arrêt, détention.'),
    ('amenity', 'vehicle_ramp'): ('Rampe véhicules', 'Rampe pour véhicules. Monter, descendre, accès.'),
    ('amenity', 'surf_school'): ('École de surf', 'École de surf, cours. Planche, vagues, apprendre, moniteur.'),
    ('amenity', 'sanatorium'): ('Sanatorium', 'Sanatorium, maison de repos. Convalescence, cure, soins.'),
    ('amenity', 'greenhouse'): ('Serre', 'Serre, jardin d\'hiver. Plantes, culture.'),
    ('amenity', 'bicycle_wash'): ('Lavage vélo', 'Station lavage vélo. Nettoyer bicyclette, VTT.'),
    ('amenity', 'traffic_park'): ('Parc sécurité routière', 'Parc éducation routière. Apprendre code, enfants, piste.'),
    ('amenity', 'mounting_block'): ('Montoir', 'Montoir à cheval. Monter en selle, équitation.'),
    ('amenity', 'sacco'): ('Sacco', 'Coopérative d\'épargne-crédit. Mutuelle, microfinance.'),
    ('amenity', 'social_centre'): ('Centre social', 'Centre social, MJC. Activités, associations, quartier.'),
    ('amenity', 'animal_hitch'): ('Attache animaux', 'Anneau d\'attache animaux. Chien, cheval, laisse.'),
    ('amenity', 'exhibition_centre'): ('Centre expositions', 'Parc des expositions, centre congrès. Salons, foires, événements.'),
    ('amenity', 'mobile_money_agent'): ('Agent mobile money', 'Agent transfert d\'argent mobile. Envoyer, recevoir argent, Orange Money.'),
    ('amenity', 'luggage_locker'): ('Consigne bagages', 'Consigne à bagages. Casiers, gare, aéroport, sécurisé.'),
    ('amenity', 'boat_sharing'): ('Bateau partagé', 'Service bateau partagé. Location, navigation, conavigation.'),
    ('amenity', 'boat_storage'): ('Stockage bateaux', 'Stockage bateaux, hivernage. Gardiennage, cale sèche.'),
    ('amenity', 'polling_station'): ('Bureau de vote', 'Bureau de vote. Élections, voter, scrutin, urne.'),
    ('amenity', 'general'): ('Général', 'Équipement général, divers.'),
    ('amenity', 'security_control'): ('Contrôle sécurité', 'Poste contrôle sécurité. Fouille, scanner, aéroport.'),
    ('amenity', 'residence'): ('Résidence', 'Résidence, logements. Habitat, appartements.'),
    ('amenity', 'clothes_dryer'): ('Sèche-linge', 'Sèche-linge public. Sécher vêtements, laverie.'),
    ('amenity', 'exhibition_hall'): ('Hall d\'exposition', 'Salle d\'exposition, galerie. Art, événements, présentation.'),
    ('amenity', 'printer'): ('Imprimante', 'Imprimante publique. Imprimer documents, photocopies.'),
    ('amenity', 'carpet_washing'): ('Lavage tapis', 'Station lavage tapis, moquettes. Nettoyage.'),
    ('amenity', 'feeding_place'): ('Point nourrissage', 'Point de nourrissage animaux. Distribution, faune.'),
    ('amenity', 'sport'): ('Sport', 'Installation sportive. Activités physiques.'),
    ('amenity', 'Speed bump'): ('Ralentisseur', 'Dos d\'âne, ralentisseur. Limitation vitesse.'),
    ('amenity', 'blood_bank'): ('Banque de sang', 'Centre don du sang, EFS. Donner son sang, transfusion.'),
    ('amenity', 'flight_school'): ('École pilotage', 'Aéroclub, école de pilotage. Avion, ULM, brevet pilote.'),
    ('amenity', 'office'): ('Bureau', 'Bureau, local administratif.'),
    ('amenity', 'table'): ('Table', 'Table publique. Pique-nique, aire repos.'),
    ('amenity', 'internet_access'): ('Accès internet', 'Point accès internet, wifi public. Connexion, cyber.'),
    ('amenity', 'public'): ('Public', 'Équipement public. Tous usagers.'),
    ('amenity', 'left_luggage'): ('Consigne', 'Consigne bagages. Déposer valises, casiers.'),
    ('amenity', 'stadium_seating'): ('Tribunes stade', 'Tribunes, gradins. Places assises, supporters.'),
    ('amenity', 'reuse'): ('Point réemploi', 'Espace réemploi, recyclerie. Donner objets, seconde vie.'),
    ('amenity', 'security_booth'): ('Guérite sécurité', 'Guérite gardien, poste sécurité. Vigile, surveillance.'),
    ('amenity', 'sports_viewing_centre'): ('Centre retransmission', 'Centre retransmission sportive. Écran géant, match, supporters.'),
    ('amenity', 'animal_breeding'): ('Élevage', 'Élevage d\'animaux. Reproduction, ferme.'),
    ('amenity', 'watering_place'): ('Abreuvoir', 'Abreuvoir animaux, point d\'eau. Chevaux, bétail.'),
    ('amenity', 'residential'): ('Résidentiel', 'Zone résidentielle. Logements, habitations.'),
    ('amenity', 'reception_area'): ('Zone accueil', 'Espace d\'accueil, réception. Visiteurs, attente.'),
    ('amenity', 'Point de dechet'): ('Point déchets', 'Point de collecte déchets. Poubelles, tri.'),
    ('amenity', 'clothing_donation'): ('Don vêtements', 'Conteneur don vêtements. Croix-Rouge, Emmaüs, recycler.'),
    ('amenity', 'private_toilet'): ('Toilettes privées', 'Toilettes privées, accès restreint. WC, sanitaires.'),
    ('amenity', 'payment_centre'): ('Centre paiement', 'Centre de paiement, encaissement. Factures, règlement.'),
    ('amenity', 'kick-scooter_parking'): ('Parking trottinettes', 'Stationnement trottinettes. Attacher, garer trottinette.'),
    ('amenity', 'vacant'): ('Vacant', 'Local vacant, vide. Libre, disponible.'),
    ('amenity', 'camping'): ('Camping', 'Aire de camping, bivouac. Tentes, caravanes, plein air.'),
    ('amenity', 'fraternity'): ('Fraternité', 'Maison de fraternité, confrérie. Association étudiante.'),
    ('amenity', 'financial_advice'): ('Conseil financier', 'Cabinet conseil financier. Gestion patrimoine, investissement.'),
    ('amenity', 'mountain_rescue'): ('Secours montagne', 'Secours en montagne, PGHM. Sauvetage, accident, randonnée.'),
    ('amenity', 'driver_training'): ('Auto-école', 'Auto-école, formation conduite. Permis voiture, code.'),
    ('amenity', 'whirlpool'): ('Jacuzzi', 'Bain à remous, jacuzzi. Spa, bulles, détente.'),
    ('amenity', 'ticket_validator'): ('Valideur titres', 'Composteur, valideur de titres. Transport, ticket.'),
    ('amenity', 'bts'): ('Antenne BTS', 'Antenne téléphonique, relais mobile. Réseau GSM.'),
    ('amenity', 'refugee_housing'): ('Hébergement réfugiés', 'Centre accueil réfugiés. CADA, demandeurs asile.'),
    ('amenity', 'canal'): ('Canal', 'Canal navigable. Voie d\'eau, péniche.'),
    ('amenity', 'events_centre'): ('Centre événements', 'Centre d\'événements, salle des fêtes. Réceptions, cérémonies.'),
    ('amenity', 'animal_shelter'): ('Refuge animaux', 'Refuge animaux, SPA. Adoption chien, chat, abandon.'),
    ('amenity', 'dormitory'): ('Dortoir', 'Dortoir, hébergement collectif. Internat, auberge jeunesse.'),
    ('amenity', 'warehouse'): ('Entrepôt', 'Entrepôt, hangar. Stockage, logistique.'),
    ('amenity', 'madrasa'): ('Madrasa', 'École coranique, madrasa. Enseignement islamique.'),
    ('amenity', 'beachhut'): ('Cabane plage', 'Cabine de plage, cabanon. Bord de mer, bains.'),
    ('amenity', 'market'): ('Marché', 'Marché couvert, halle. Fruits, légumes, fromage, producteurs.'),
    ('amenity', 'gambling'): ('Jeux d\'argent', 'Salle de jeux, casino. Paris, machines à sous.'),
    ('amenity', 'hydrant'): ('Bouche incendie', 'Poteau incendie, borne. Pompiers, eau.'),
    ('amenity', 'dog_parking'): ('Parking chiens', 'Attache chiens. Laisser son chien, laisse, anneau.'),
    ('amenity', 'device_charging_station'): ('Borne recharge', 'Borne recharge appareils. Téléphone, batterie, USB.'),
    ('amenity', 'convent'): ('Couvent', 'Couvent, monastère. Religieux, abbaye, communauté.'),
    ('amenity', 'trailer_park'): ('Parc caravanes', 'Terrain caravanes, camping-cars. Résidentiel.'),
    ('amenity', 'food_sharing'): ('Frigo solidaire', 'Partage alimentaire, frigo solidaire. Anti-gaspi, gratuit.'),
    ('amenity', 'place_of_mourning'): ('Lieu de recueillement', 'Chambre funéraire, funérarium. Veillée, défunt.'),
    ('amenity', 'clubhouse'): ('Club house', 'Local associatif, club house. Réunions, vestiaires.'),
    ('amenity', 'trolley_bay'): ('Parc chariots', 'Zone retour caddies. Supermarché, chariots.'),
    ('amenity', 'health_post'): ('Poste de santé', 'Dispensaire, poste de santé. Soins premiers, infirmerie.'),
    ('amenity', 'relay_box'): ('Point relais', 'Casier point relais. Colis, livraison.'),
    ('amenity', 'barefootpath'): ('Sentier pieds nus', 'Parcours pieds nus, sentier sensoriel. Détente, nature.'),
    ('amenity', 'border_control'): ('Contrôle frontière', 'Poste frontière, douane. Passeport, contrôle.'),
    ('amenity', 'car_pooling'): ('Covoiturage', 'Aire de covoiturage. Partage trajet, parking.'),
    ('amenity', 'hookah_lounge'): ('Bar à chicha', 'Bar à chicha, narguilé. Salon, fumer, thé.'),
    ('amenity', 'house'): ('Maison', 'Maison, habitation. Logement, résidence.'),
    ('amenity', 'court_yard'): ('Cour', 'Cour intérieure, patio. Espace extérieur.'),
    ('amenity', 'bear_box'): ('Coffre anti-ours', 'Container anti-ours. Stockage nourriture, camping, sécurité.'),
    ('amenity', 'social_club'): ('Club social', 'Club social, amicale. Association, réunions.'),
    ('amenity', 'scout_hut'): ('Local scout', 'Local scout, cabane. Éclaireurs, mouvements jeunesse.'),
    ('amenity', 'veterinary_pharmacy'): ('Pharmacie vétérinaire', 'Pharmacie pour animaux. Médicaments, soins.'),
    ('amenity', 'threshing_floor'): ('Aire de battage', 'Aire de battage, blé. Agriculture traditionnelle.'),
    ('amenity', 'ranger_station'): ('Maison forestière', 'Poste garde forestier. Parc naturel, surveillance.'),
    ('amenity', 'small_electric_vehicle_parking'): ('Parking véhicules électriques', 'Stationnement petits véhicules électriques. Scooters, vélos.'),
    ('amenity', 'first_aid'): ('Premiers secours', 'Poste premiers secours. Infirmerie, soins urgents.'),
    ('amenity', 'scooter_parking'): ('Parking scooters', 'Stationnement scooters, motos. Deux-roues.'),
    ('amenity', 'bbq'): ('Barbecue', 'Barbecue public, grillades. Pique-nique, cuisson.'),
    ('amenity', 'club'): ('Club', 'Club, association. Loisirs, activités, membres.'),
    ('amenity', 'festival_grounds'): ('Terrain festival', 'Site festival, concerts. Événements plein air.'),
    ('amenity', 'parish_hall'): ('Salle paroissiale', 'Salle paroissiale, patronage. Église, réunions.'),
    ('amenity', 'waste_basket;recycling'): ('Poubelle tri', 'Poubelle avec tri sélectif. Recyclage, déchets.'),
    ('amenity', 'street_lamp'): ('Lampadaire', 'Lampadaire, éclairage public. Lumière, réverbère.'),
    ('amenity', 'public_office'): ('Bureau public', 'Bureau service public. Administration, guichet.'),
    ('amenity', 'tap'): ('Robinet', 'Robinet d\'eau, fontaine. Point d\'eau potable.'),
    ('amenity', 'stables'): ('Écuries', 'Écuries, boxes chevaux. Équitation, pension.'),
    ('amenity', 'waste_dump_site'): ('Déchetterie', 'Déchetterie, décharge. Encombrants, recyclage.'),
    ('amenity', 'disused'): ('Désaffecté', 'Lieu désaffecté, abandonné. Plus en service.'),
    ('amenity', 'mobile_money'): ('Mobile money', 'Service paiement mobile. Transfert argent, téléphone.'),
    ('amenity', 'workshop'): ('Atelier', 'Atelier, bricolage. Fablab, réparation, création.'),
    ('amenity', 'retirement_home'): ('Maison retraite', 'Maison de retraite, EHPAD. Personnes âgées, résidence seniors.'),
    ('amenity', 'ski_school'): ('École de ski', 'École de ski, ESF. Cours, moniteur, débutants.'),
    ('amenity', 'stripclub'): ('Club de strip-tease', 'Club de strip-tease, bar hôtesses. Adultes.'),
    ('amenity', 'money_transfer'): ('Transfert argent', 'Agence transfert d\'argent. Western Union, envoi.'),
    ('amenity', 'licensed_club'): ('Club privé', 'Club privé, membres. Bar, adhérents.'),
    ('amenity', 'waste_basket;vending_machine'): ('Poubelle distributeur', 'Poubelle et distributeur automatique. Snacks, déchets.'),
    ('amenity', 'marae'): ('Marae', 'Marae, lieu sacré polynésien. Temple, Tahiti, culture.'),
    ('amenity', 'foot_shower'): ('Douche pieds', 'Rince-pieds, douche plage. Sable, piscine.'),
    ('amenity', 'cook_stove'): ('Poêle cuisine', 'Poêle à bois, cuisinière. Cuisson traditionnelle.'),
    ('amenity', 'lounge'): ('Salon', 'Salon, espace détente. Attente, repos.'),
    ('amenity', 'boat_rental'): ('Location bateaux', 'Location de bateaux. Pédalo, barque, nautisme.'),
    ('amenity', 'apartment'): ('Appartement', 'Appartement, logement. Résidence, immeuble.'),
    ('amenity', 'nameplate'): ('Plaque', 'Plaque signalétique, nom.'),
    ('amenity', 'smoking_area'): ('Zone fumeurs', 'Espace fumeurs autorisé. Cigarette, extérieur.'),
    ('amenity', 'security'): ('Sécurité', 'Poste de sécurité, surveillance. Gardiennage.'),
    ('amenity', 'fixme'): ('À corriger', 'Donnée à vérifier, corriger.'),
    ('amenity', 'shelf'): ('Étagère', 'Étagère publique, boîte à livres. Partage, gratuit.'),
    ('amenity', 'public_facility'): ('Équipement public', 'Installation publique. Services collectifs.'),
    ('amenity', 'trade_school'): ('École professionnelle', 'Lycée professionnel, CFA. Formation métier, apprentissage.'),
    ('amenity', 'cooking_school'): ('École cuisine', 'École de cuisine, cours culinaires. Apprendre cuisiner.'),
    ('amenity', 'service'): ('Service', 'Point de service, prestation.'),
    ('amenity', 'beer_garden'): ('Terrasse brasserie', 'Biergarten, terrasse bière. Plein air, brasserie.'),
    ('amenity', 'shared_taxi'): ('Taxi collectif', 'Taxi partagé, navette. Transport commun.'),
    ('amenity', 'bell'): ('Cloche', 'Cloche, sonnette. Signal, église.'),
    ('amenity', 'waiting_area'): ('Zone attente', 'Zone d\'attente. Patienter, sièges.'),
    ('amenity', 'washing_machine'): ('Lave-linge', 'Machine à laver publique. Laverie, buanderie.'),
    ('amenity', 'checkpoint'): ('Point contrôle', 'Checkpoint, contrôle. Accès, vérification.'),
    ('amenity', 'archive'): ('Archives', 'Centre d\'archives. Documents, histoire, consultation.'),
    ('amenity', 'hitching_post'): ('Poteau attache', 'Poteau attache chevaux. Anneau, équitation.'),
    ('amenity', 'power_supply'): ('Alimentation électrique', 'Borne électrique. Branchement, courant.'),
    ('amenity', 'bus_stop'): ('Arrêt de bus', 'Arrêt de bus, abribus. Transport en commun.'),
    ('amenity', 'sailing_school'): ('École de voile', 'École de voile, centre nautique. Catamaran, optimist.'),
    ('amenity', 'prep_school'): ('Cours préparatoire', 'Prépa, classe préparatoire. Études supérieures.'),
    ('amenity', 'binoculars'): ('Jumelles', 'Jumelles panoramiques, longue-vue. Point de vue, observation.'),
    ('amenity', 'vivienda'): ('Logement', 'Logement, habitation.'),
    ('amenity', 'shop'): ('Boutique', 'Boutique, commerce. Magasin.'),
    ('amenity', 'fish_cleaning'): ('Nettoyage poisson', 'Station nettoyage poisson. Pêcheurs, éviscérer.'),
    ('amenity', 'harbourmaster'): ('Capitainerie', 'Capitainerie, bureau du port. Marina, bateaux.'),
    ('amenity', 'dressing_room'): ('Vestiaire', 'Vestiaire, cabine. Changer, essayage.'),
    ('amenity', 'place'): ('Lieu', 'Lieu, endroit. Place, emplacement.'),
    ('amenity', 'community_hall'): ('Salle communale', 'Salle polyvalente, salle des fêtes. Réunions, événements.'),
    ('amenity', 'juice_bar'): ('Bar à jus', 'Bar à jus, smoothies. Fruits frais, healthy.'),
    ('amenity', 'research_institute'): ('Institut recherche', 'Institut de recherche, laboratoire. Sciences, études.'),
    ('amenity', 'ski_rental'): ('Location ski', 'Location ski, matériel. Skis, chaussures, bâtons.'),
    ('amenity', 'commerce'): ('Commerce', 'Commerce, boutique. Magasin, vente.'),
    ('amenity', 'student_accommodation'): ('Résidence étudiante', 'Résidence universitaire, cité U. Logement étudiant, chambre.'),
    ('amenity', 'motorcycle_rental'): ('Location moto', 'Location motos, scooters. Deux-roues, louer.'),
    ('amenity', 'industrial'): ('Industriel', 'Zone industrielle. Usines, manufactures.'),
    ('amenity', 'locker'): ('Casier', 'Casier, consigne. Rangement sécurisé.'),
    ('amenity', 'mist_spraying_cooler'): ('Brumisateur', 'Brumisateur public. Rafraîchir, canicule.'),
    ('amenity', 'mailroom'): ('Salle courrier', 'Local courrier, boîtes aux lettres. Distribution.'),
    ('amenity', 'Vivienda'): ('Logement', 'Logement, habitation.'),
    ('amenity', 'building_yard'): ('Cour bâtiment', 'Cour, espace extérieur. Bâtiment.'),
    ('amenity', 'water'): ('Eau', 'Point d\'eau. Fontaine, source.'),
    ('amenity', 'construction'): ('Construction', 'Chantier, construction. Travaux.'),
    ('amenity', 'chair'): ('Chaise', 'Chaise publique. S\'asseoir, mobilier.'),
    ('amenity', 'healthcare'): ('Santé', 'Établissement de santé. Soins, médical.'),
    ('amenity', 'public_service'): ('Service public', 'Service public, administration. Guichet.'),
    ('amenity', 'piano'): ('Piano', 'Piano public. Jouer musique, libre-service.'),
    ('amenity', 'kick-scooter_rental'): ('Location trottinettes', 'Location trottinettes électriques. Lime, Bird, mobilité.'),
    ('amenity', 'rv_storage'): ('Stockage camping-cars', 'Garage camping-cars, caravanes. Hivernage, gardiennage.'),
    ('amenity', 'letter_box'): ('Boîte aux lettres', 'Boîte aux lettres. Courrier, recevoir.'),

    # =====================
    # SHOP
    # =====================
    ('shop', 'vending_machine'): ('Distributeur', 'Distributeur automatique, machine. Snacks, boissons, 24h.'),
    ('shop', 'glaziery'): ('Vitrerie', 'Vitrier, miroitier. Vitres, fenêtres, réparation.'),
    ('shop', 'food'): ('Alimentation', 'Magasin alimentaire. Épicerie, nourriture.'),
    ('shop', 'caravan'): ('Caravanes', 'Vendeur caravanes, camping-cars. Mobil-home.'),
    ('shop', 'photo'): ('Photo', 'Magasin photo. Tirages, développement, appareils.'),
    ('shop', 'country_store'): ('Magasin rural', 'Quincaillerie rurale, alimentation animaux. Ferme, jardin.'),
    ('shop', 'point_of_sale'): ('Point de vente', 'Point de vente, boutique. Commerce.'),
    ('shop', 'surf'): ('Surf', 'Magasin de surf. Planches, combinaisons, glisse.'),
    ('shop', 'collector'): ('Collection', 'Boutique collection. Timbres, pièces, antiquités.'),
    ('shop', 'herbalist'): ('Herboristerie', 'Herboristerie, plantes médicinales. Tisanes, naturel.'),
    ('shop', 'printer_ink'): ('Cartouches encre', 'Cartouches imprimante, toner. Recharge, recyclage.'),
    ('shop', 'wool'): ('Laine', 'Mercerie laine, tricot. Fils, pelotes, couture.'),
    ('shop', 'lottery'): ('Loterie', 'Point loto, jeux hasard. Grattage, Française des Jeux.'),
    ('shop', 'bookmaker'): ('Paris sportifs', 'Bookmaker, paris sportifs. PMU, courses, pronostics.'),
    ('shop', 'pet_grooming'): ('Toilettage animaux', 'Toiletteur chien, chat. Coupe, bain, soins.'),
    ('shop', 'brewing_supplies'): ('Brassage maison', 'Matériel brassage bière. Homebrew, malt, houblon.'),
    ('shop', 'pyrotechnics'): ('Feux artifice', 'Magasin pyrotechnie. Pétards, fusées, fête.'),
    ('shop', 'military_surplus'): ('Surplus militaire', 'Surplus armée, équipement. Treillis, rangers.'),

    # =====================
    # LEISURE
    # =====================
    ('leisure', 'sunbathing'): ('Bain de soleil', 'Aire bronzage, solarium. Transat, plage.'),

    # =====================
    # HEALTHCARE
    # =====================
    ('healthcare', 'healthcare=blood_bank'): ('Banque de sang', 'Don du sang, EFS. Transfusion, donneur.'),
    ('healthcare', 'healthcare=doctor'): ('Médecin', 'Cabinet médecin. Consultation, ordonnance.'),
    ('healthcare', 'healthcare=clinic'): ('Clinique', 'Clinique privée. Soins, hospitalisation.'),
    ('healthcare', 'healthcare=midwife'): ('Sage-femme', 'Cabinet sage-femme. Grossesse, accouchement.'),
    ('healthcare', 'healthcare=rehabilitation'): ('Rééducation', 'Centre rééducation. Kinésithérapie, convalescence.'),
    ('healthcare', 'healthcare=postpartum_care'): ('Soins post-partum', 'Suivi après accouchement. Maternité.'),
    ('healthcare', 'healthcare=hospice'): ('Hospice', 'Maison soins palliatifs. Fin de vie, accompagnement.'),
    ('healthcare', 'healthcare=centre'): ('Centre de santé', 'Centre médical. Consultations, soins.'),
    ('healthcare', 'healthcare=hospital'): ('Hôpital', 'Hôpital, CHU. Urgences, soins, chirurgie.'),
    ('healthcare', 'healthcare=occupational_therapist'): ('Ergothérapeute', 'Cabinet ergothérapie. Autonomie, rééducation.'),
    ('healthcare', 'healthcare=pharmacy'): ('Pharmacie', 'Pharmacie, officine. Médicaments, ordonnance.'),
    ('healthcare', 'healthcare=dialysis'): ('Dialyse', 'Centre de dialyse. Insuffisance rénale, traitement.'),
    ('healthcare', 'healthcare=podiatrist'): ('Podologue', 'Cabinet podologie. Pieds, semelles, soins.'),
    ('healthcare', 'healthcare=psychotherapist'): ('Psychothérapeute', 'Cabinet psychothérapie. Thérapie, accompagnement.'),
    ('healthcare', 'healthcare=dentist'): ('Dentiste', 'Cabinet dentaire. Soins dents, détartrage.'),

    # =====================
    # EMERGENCY
    # =====================
    ('emergency', 'key_depot'): ('Dépôt clés', 'Coffre à clés pompiers. Accès secours, bâtiment.'),
    ('emergency', 'exit'): ('Sortie secours', 'Issue de secours, évacuation. Urgence, sécurité.'),
    ('emergency', 'first_aid'): ('Premiers secours', 'Poste premiers secours. Infirmerie, soins urgents.'),
    ('emergency', 'designated'): ('Zone désignée', 'Zone urgence désignée. Point rassemblement.'),
    ('emergency', 'destination'): ('Destination secours', 'Point évacuation. Rassemblement.'),
    ('emergency', 'slipway'): ('Cale mise eau', 'Cale de mise à l\'eau. Bateau secours, SNSM.'),
    ('emergency', 'fire_alarm_box'): ('Déclencheur alarme', 'Boîtier alarme incendie. Briser vitre, alerte.'),
    ('emergency', 'bleed_control_kit'): ('Kit hémorragie', 'Trousse contrôle hémorragie. Garrot, compresses.'),
    ('emergency', 'fire_service_inlet'): ('Prise pompiers', 'Colonne sèche, raccord. Alimentation eau.'),
    ('emergency', 'fire_hydrant_sign'): ('Panneau bouche incendie', 'Signalisation borne incendie. Pompiers.'),
    ('emergency', 'control_centre'): ('Centre contrôle', 'Centre commandement secours. Coordination, 15, 18.'),
    ('emergency', 'water_rescue_station'): ('Station sauvetage aquatique', 'Poste secours nautique. Noyade, plage.'),
    ('emergency', 'disaster_help_point'): ('Point aide catastrophe', 'Point assistance sinistre. Crise, accueil.'),
    ('emergency', 'dry_riser_inlet'): ('Colonne sèche', 'Raccord colonne sèche. Alimentation pompiers.'),
    ('emergency', 'water_rescue'): ('Sauvetage aquatique', 'Secours nautique, SNSM. Noyade, mer.'),
    ('emergency', 'fire_water_pond'): ('Réserve incendie', 'Réserve d\'eau pompiers. Bassin, citerne.'),
    ('emergency', 'psap'): ('Centre 112', 'Centre appels urgence 112. Régulation, dispatch.'),
    ('emergency', 'fire_detection_system'): ('Détection incendie', 'Système détection feu. Alarme, sécurité.'),
    ('emergency', 'official'): ('Officiel', 'Point urgence officiel. Autorités.'),
    ('emergency', 'lifeguard_tower'): ('Tour surveillant', 'Poste MNS, surveillance baignade. Plage, piscine.'),
    ('emergency', 'emergency_ward_entrance'): ('Entrée urgences', 'Accès service urgences. Hôpital, SAMU.'),
    ('emergency', 'disaster_response'): ('Réponse catastrophe', 'Centre gestion crise. Protection civile.'),
    ('emergency', 'marine_rescue'): ('Sauvetage mer', 'SNSM, secours maritime. Côte, bateau.'),
    ('emergency', 'fire_flapper'): ('Battoir incendie', 'Outil extinction feu forêt. Flammes, braises.'),
    ('emergency', 'evacuation_centre'): ('Centre évacuation', 'Centre hébergement d\'urgence. Sinistrés, abri.'),
    ('emergency', 'first_aid_kit'): ('Trousse secours', 'Boîte premiers soins. Pansements, désinfectant.'),
    ('emergency', 'air_rescue_service'): ('Secours aérien', 'Hélicoptère secours, héliSMUR. Montagne, accident.'),
    ('emergency', 'lifeguard_base'): ('Base sauveteurs', 'Poste surveillants baignade. Plage, MNS.'),
    ('emergency', 'ladder_site'): ('Point échelle', 'Accès échelle pompiers. Immeuble, intervention.'),
    ('emergency', 'fire_lookout'): ('Tour guet incendie', 'Vigie feux forêt. Surveillance, prévention.'),

    # =====================
    # HISTORIC
    # =====================
    ('historic', 'coat_of_arms'): ('Blason', 'Blason, armoiries. Héraldique, commune.'),

    # =====================
    # MAN_MADE
    # =====================
    ('man_made', 'environmental_hazard'): ('Risque environnemental', 'Zone pollution, contamination. Danger, toxique.'),
    ('man_made', 'compressor'): ('Compresseur', 'Station compresseur. Air comprimé, gonflage.'),
    ('man_made', 'beacon'): ('Balise', 'Balise maritime ou aérienne. Signal, navigation.'),
    ('man_made', 'clarifier'): ('Clarificateur', 'Bassin décantation. Épuration, traitement eau.'),
    ('man_made', 'shooting_butt'): ('Butte de tir', 'Butte pare-balles. Stand tir, sécurité.'),
    ('man_made', 'unprotected_well'): ('Puits non protégé', 'Puits ouvert, non sécurisé. Eau, danger.'),
    ('man_made', 'bore'): ('Forage', 'Puits foré. Eau souterraine, sondage.'),
    ('man_made', 'tensoring_cable'): ('Câble hauban', 'Câble de tension. Pylône, antenne.'),
    ('man_made', 'gas_well'): ('Puits de gaz', 'Forage gazier. Extraction, gisement.'),
    ('man_made', 'pumping_rig'): ('Pompe pétrolière', 'Balancier extraction pétrole. Chevalet.'),
    ('man_made', 'storage'): ('Stockage', 'Structure stockage. Entrepôt, réserve.'),
    ('man_made', 'prospect'): ('Prospection', 'Site prospection minière. Recherche, forage.'),
    ('man_made', 'forester\'s_lodge'): ('Maison forestière', 'Logement garde forestier. Forêt, ONF.'),
    ('man_made', 'buoy'): ('Bouée', 'Bouée maritime, balisage. Navigation, chenal.'),
    ('man_made', 'wall'): ('Mur', 'Mur, muret. Clôture, pierre.'),
    ('man_made', 'fuel_column'): ('Colonne carburant', 'Distributeur carburant. Station essence.'),
    ('man_made', 'pagoda'): ('Pagode', 'Pagode, temple asiatique. Bouddhiste.'),
    ('man_made', 'excavation'): ('Excavation', 'Fouille, creusement. Chantier, archéologie.'),
    ('man_made', 'fish_flake'): ('Séchoir poisson', 'Claie séchage poisson. Morue, traditionnel.'),
    ('man_made', 'latrines'): ('Latrines', 'Toilettes extérieures, feuillées. WC basiques.'),
    ('man_made', 'corral'): ('Corral', 'Enclos bétail. Chevaux, rassemblement.'),
    ('man_made', 'arch'): ('Arc', 'Arc, arche. Monument, architecture.'),
    ('man_made', 'tar_kiln'): ('Four à goudron', 'Four production goudron. Pin, résine.'),
    ('man_made', 'MDF'): ('Point distribution', 'NRA, point distribution fibre. Télécom.'),
    ('man_made', 'soccer_goal'): ('Cage foot', 'But football, cage. Terrain, sport.'),
    ('man_made', 'reservoir'): ('Réservoir', 'Réservoir d\'eau. Stockage, château d\'eau.'),
    ('man_made', 'tombstone'): ('Pierre tombale', 'Pierre tombale, stèle. Cimetière, sépulture.'),
    ('man_made', 'Yes'): ('Structure artificielle', 'Construction humaine. Ouvrage.'),
    ('man_made', 'yes'): ('Structure artificielle', 'Construction humaine. Ouvrage.'),
    ('man_made', 'mounting_eye'): ('Anneau fixation', 'Point d\'ancrage, amarrage. Attache.'),
    ('man_made', 'building'): ('Bâtiment', 'Construction, édifice. Immeuble.'),
    ('man_made', 'loudspeaker'): ('Haut-parleur', 'Haut-parleur public. Annonces, alerte.'),
    ('man_made', 'paifang'): ('Paifang', 'Portique chinois traditionnel. Quartier, entrée.'),
    ('man_made', 'paint'): ('Peinture', 'Marquage peinture. Sol, route.'),
    ('man_made', 'telephone_box'): ('Cabine téléphonique', 'Cabine téléphone. Appeler, booth.'),
    ('man_made', 'handpump'): ('Pompe manuelle', 'Pompe à bras, eau. Puits, village.'),
    ('man_made', 'catch_basin'): ('Regard avaloir', 'Bouche égout, grille. Eaux pluviales.'),
    ('man_made', 'basin'): ('Bassin', 'Bassin d\'eau, retenue. Réserve.'),
    ('man_made', 'fishing_peg'): ('Poste pêche', 'Emplacement pêche numéroté. Étang, concours.'),
    ('man_made', 'peat_edge'): ('Lisière tourbe', 'Bord tourbière. Extraction, marais.'),
    ('man_made', 'sign'): ('Panneau', 'Panneau signalisation. Information, direction.'),
    ('man_made', 'snow_cannon'): ('Canon à neige', 'Enneigeur artificiel. Ski, station.'),
    ('man_made', 'mussel_raft'): ('Bouchot', 'Parc à moules, élevage. Mytiliculture.'),
    ('man_made', 'wayside_cross'): ('Croix chemin', 'Croix calvaire, oratoire. Religieux.'),
    ('man_made', 'storm_drain'): ('Égout pluvial', 'Drain eaux pluie. Évacuation.'),
    ('man_made', 'collecting_chute'): ('Goulotte collecte', 'Toboggan tri, déchets. Collecte.'),
    ('man_made', 'summit_board'): ('Panneau sommet', 'Table orientation sommet. Vue, montagne.'),
    ('man_made', 'wire'): ('Fil', 'Câble, fil métallique. Ligne.'),
    ('man_made', 'covered_reservoir'): ('Réservoir couvert', 'Citerne enterrée. Eau potable.'),
    ('man_made', 'peat_heap'): ('Tas tourbe', 'Amas tourbe extraite. Séchage.'),
    ('man_made', 'apiary'): ('Rucher', 'Ruches, abeilles. Apiculture, miel.'),
    ('man_made', 'communications_transponder'): ('Transpondeur', 'Relais communication. Signal, répéteur.'),
    ('man_made', 'video_wall'): ('Écran géant', 'Mur vidéo, affichage. Pub, info.'),
    ('man_made', 'slurry_tank'): ('Fosse lisier', 'Cuve lisier, purin. Agricole.'),
    ('man_made', 'water_canal'): ('Canal eau', 'Canal irrigation. Acheminement eau.'),
    ('man_made', 'Sohlrampe'): ('Seuil rivière', 'Rampe de fond, seuil. Cours d\'eau.'),
    ('man_made', 'crop_marking'): ('Marque culture', 'Trace archéologique aérienne. Végétation.'),
    ('man_made', 'mill'): ('Moulin', 'Moulin eau ou vent. Farine, historique.'),
    ('man_made', 'sewer_vent'): ('Évent égout', 'Cheminée aération égout. Ventilation.'),
    ('man_made', 'buttress'): ('Contrefort', 'Contrefort, arc-boutant. Soutien, mur.'),
    ('man_made', 'pier'): ('Jetée', 'Jetée, ponton. Promenade, port.'),
    ('man_made', 'marsh_terrace'): ('Terrasse marais', 'Aménagement zone humide. Observation.'),
    ('man_made', 'waterway'): ('Voie eau', 'Cours d\'eau artificiel. Canal.'),
    ('man_made', 'snow_net'): ('Filet pare-neige', 'Protection avalanche. Montagne, ski.'),
    ('man_made', 'sprinkler'): ('Arroseur', 'Système arrosage automatique. Irrigation.'),
    ('man_made', 'lamp'): ('Lampe', 'Éclairage, lampadaire. Lumière.'),
    ('man_made', 'post'): ('Poteau', 'Poteau, piquet. Support.'),
    ('man_made', 'flowerbed'): ('Parterre fleuri', 'Massif fleurs, jardinage. Décoration.'),
    ('man_made', 'stone'): ('Pierre', 'Pierre dressée, rocher. Borne.'),
    ('man_made', 'artwork'): ('Oeuvre art', 'Sculpture, installation artistique. Public.'),
    ('man_made', 'cave_entrance'): ('Entrée grotte', 'Accès cavité, spéléologie. Souterrain.'),
    ('man_made', 'slurry_basin'): ('Bassin lisier', 'Lagune stockage effluents. Agricole.'),
    ('man_made', 'bridge'): ('Pont', 'Pont, passerelle. Franchissement.'),
    ('man_made', 'tank'): ('Cuve', 'Réservoir, citerne. Stockage liquide.'),
    ('man_made', 'variable_message_sign'): ('Panneau message variable', 'PMV, affichage dynamique. Info trafic.'),
    ('man_made', 'tower'): ('Tour', 'Tour, beffroi. Construction haute.'),
    ('man_made', 'cattle_chute'): ('Couloir bétail', 'Cage contention, vaccinodrome. Élevage.'),
    ('man_made', 'rainwater'): ('Eau pluie', 'Récupération eau pluviale. Citerne.'),
    ('man_made', 'pillar'): ('Pilier', 'Colonne, pilier. Soutien, monument.'),
    ('man_made', 'foundations'): ('Fondations', 'Soubassements, base. Construction.'),
    ('man_made', 'portal'): ('Portail', 'Entrée monumentale, porche.'),
    ('man_made', 'bore_hole'): ('Forage', 'Puits foré, sondage. Eau, pétrole.'),
    ('man_made', 'hongsalmun'): ('Hongsalmun', 'Portique coréen traditionnel. Temple, entrée.'),
    ('man_made', 'piste:halfpipe'): ('Half-pipe', 'Rampe ski, snowboard. Acrobaties.'),
    ('man_made', 'grave'): ('Tombe', 'Sépulture, tombe. Cimetière.'),
    ('man_made', 'bladder'): ('Citerne souple', 'Réservoir flexible, poche. Eau, carburant.'),
    ('man_made', 'torii'): ('Torii', 'Portique shinto japonais. Temple, sacré.'),
    ('man_made', 'beam'): ('Poutre', 'Poutre, traverse. Construction.'),
    ('man_made', 'maypole'): ('Mât de mai', 'Arbre de mai, fête. Tradition, village.'),
    ('man_made', 'windpump'): ('Éolienne pompage', 'Moulin pompe eau. Irrigation, élevage.'),
    ('man_made', 'tell'): ('Tell', 'Tertre archéologique. Colline artificielle, ruines.'),
    ('man_made', 'mound'): ('Butte', 'Monticule, tertre. Relief artificiel.'),
    ('man_made', 'coal_pile'): ('Stock charbon', 'Tas de charbon. Centrale, chauffage.'),
    ('man_made', 'sheepfold'): ('Bergerie', 'Enclos moutons, bergerie. Élevage ovin.'),
    ('man_made', 'pump'): ('Pompe', 'Station pompage. Eau, liquide.'),
    ('man_made', 'oil_gas_separator'): ('Séparateur pétrole-gaz', 'Installation séparation. Raffinerie.'),
    ('man_made', 'insect_hotel'): ('Hôtel insectes', 'Abri insectes, biodiversité. Jardin, pollinisateurs.'),
    ('man_made', 'pipeline_marker'): ('Balise pipeline', 'Marqueur canalisation. Gaz, pétrole.'),
    ('man_made', 'cutting'): ('Déblai', 'Tranchée, passage creusé. Route, train.'),
    ('man_made', 'heat_exchange_station'): ('Sous-station chauffage', 'Échangeur chaleur urbain. Réseau chaleur.'),
    ('man_made', 'snow_fence'): ('Barrière neige', 'Pare-neige, congère. Protection route.'),
    ('man_made', 'mine'): ('Mine', 'Mine, extraction. Charbon, minerai.'),
    ('man_made', 'spring_box'): ('Captage source', 'Chambre captage eau. Source, réservoir.'),
    ('man_made', 'nozzle'): ('Buse', 'Buse, sortie eau. Jet, fontaine.'),
    ('man_made', 'stele'): ('Stèle', 'Monument commémoratif. Pierre dressée.'),
    ('man_made', 'conveyor_belt'): ('Tapis roulant', 'Convoyeur, bande. Transport matériaux.'),
    ('man_made', 'wastewater_tank'): ('Cuve eaux usées', 'Réservoir assainissement. Fosse septique.'),
    ('man_made', 'service_area_interface'): ('Interface aire service', 'Borne services aire autoroute.'),
    ('man_made', 'standpipe'): ('Colonne montante', 'Conduite verticale eau. Pompiers.'),
    ('man_made', 'patio'): ('Terrasse', 'Patio, cour dallée. Extérieur.'),
    ('man_made', 'campanile'): ('Campanile', 'Clocher isolé. Église, tour.'),
    ('man_made', 'surveillance'): ('Surveillance', 'Caméra surveillance, vidéoprotection. Sécurité.'),
    ('man_made', 'grouse_butt'): ('Abri tir grouse', 'Poste chasse tétras. Angleterre.'),
    ('man_made', 'dolphin'): ('Duc d\'Albe', 'Pieu amarrage portuaire. Bateau, quai.'),
    ('man_made', 'city_wall'): ('Rempart', 'Fortifications, muraille. Ville médiévale.'),
    ('man_made', 'spillway'): ('Déversoir', 'Évacuateur crue, barrage. Trop-plein.'),
    ('man_made', 'stupa'): ('Stupa', 'Monument bouddhiste. Reliques, sacré.'),
    ('man_made', 'village_sign'): ('Panneau village', 'Entrée localité. Nom commune.'),
    ('man_made', 'pumpjack'): ('Pompe pétrole', 'Chevalet extraction, balancier. Puits.'),
    ('man_made', 'shaft'): ('Puits mine', 'Galerie verticale. Accès souterrain.'),
    ('man_made', 'oven'): ('Four', 'Four extérieur, à pain. Cuisson.'),
    ('man_made', 'levee'): ('Digue', 'Levée, protection inondation. Cours d\'eau.'),
    ('man_made', 'communications_dish'): ('Parabole', 'Antenne satellite, réception. Télécom.'),
    ('man_made', 'canopy'): ('Auvent', 'Abri couvert, marquise. Protection.'),
    ('man_made', 'pond'): ('Étang', 'Mare artificielle, bassin. Jardin.'),
    ('man_made', 'drill_hole'): ('Trou forage', 'Sondage, exploration. Géologie.'),
    ('man_made', 'water_tank'): ('Réservoir eau', 'Château d\'eau, citerne. Stockage.'),
    ('man_made', 'outfall'): ('Exutoire', 'Sortie égout, rejet. Cours d\'eau.'),
    ('man_made', 'dam'): ('Barrage', 'Barrage, retenue. Hydroélectricité.'),
    ('man_made', 'public_borehole'): ('Forage public', 'Puits communautaire. Eau potable.'),
    ('man_made', 'shade'): ('Ombrage', 'Structure ombrage. Protection soleil.'),
    ('man_made', 'trace_control_strip'): ('Bande contrôle', 'Zone frontière, traces. Surveillance.'),
    ('man_made', 'trough'): ('Auge', 'Abreuvoir, bac. Animaux, eau.'),
    ('man_made', 'marker'): ('Borne', 'Repère, marqueur. Limite, topographie.'),
    ('man_made', 'man_made'): ('Construction', 'Ouvrage artificiel. Structure humaine.'),
    ('man_made', 'billboard'): ('Panneau pub', 'Affiche publicitaire, 4x3. Réclame.'),
    ('man_made', 'container_terminal'): ('Terminal conteneurs', 'Port conteneurs. Fret, manutention.'),
    ('man_made', 'mast'): ('Mât', 'Mât, pylône. Antenne, éolienne.'),
    ('man_made', 'protected_well'): ('Puits protégé', 'Puits avec margelle. Eau sécurisé.'),
    ('man_made', 'raccard'): ('Raccard', 'Grenier suisse, chalet. Valais, stockage.'),
    ('man_made', 'water_tower'): ('Château d\'eau', 'Réservoir surélevé. Distribution eau.'),
    ('man_made', 'conveyor'): ('Convoyeur', 'Tapis roulant, transport. Matériaux.'),
    ('man_made', 'cistern'): ('Citerne', 'Cuve eau, réservoir. Stockage.'),
    ('man_made', 'reinforced_slope'): ('Talus renforcé', 'Pente stabilisée. Génie civil.'),
    ('man_made', 'borehole'): ('Forage', 'Puits foré. Eau, sondage.'),
    ('man_made', 'crane_rail'): ('Rail grue', 'Voie portique, pont roulant. Levage.'),
    ('man_made', 'drinking_fountain'): ('Fontaine potable', 'Point eau potable. Boire, rafraîchir.'),
    ('man_made', 'utility'): ('Réseau', 'Infrastructure technique. Câbles, tuyaux.'),
    ('man_made', 'street_lamp'): ('Lampadaire', 'Éclairage public, réverbère. Lumière rue.'),
    ('man_made', 'oxidation_ditch'): ('Fossé oxydation', 'Bassin épuration biologique. Station.'),
    ('man_made', 'tap'): ('Robinet', 'Point d\'eau, robinet. Source.'),
    ('man_made', 'wildlife_opening'): ('Passage faune', 'Ouverture animaux, clôture. Écoduc.'),
    ('man_made', 'tunnel'): ('Tunnel', 'Galerie souterraine. Passage, circulation.'),
    ('man_made', 'charge_point'): ('Borne recharge', 'Point charge véhicule électrique.'),
    ('man_made', 'foundation'): ('Fondation', 'Base construction. Soubassement.'),
    ('man_made', 'air_vent'): ('Aération', 'Bouche ventilation. Air, souterrain.'),
    ('man_made', 'milk_churn_stand'): ('Plateforme lait', 'Support bidons lait. Collecte.'),
    ('man_made', 'cooling'): ('Refroidissement', 'Système refroidissement. Tour, échangeur.'),
    ('man_made', 'bird_feeder'): ('Mangeoire oiseaux', 'Distributeur graines. Jardin, hiver.'),
    ('man_made', 'logway'): ('Glissière bois', 'Chemin billes, exploitation forestière.'),
    ('man_made', 'planter'): ('Jardinière', 'Bac plantes, pot. Végétalisation.'),
    ('man_made', 'guard_stone'): ('Chasse-roue', 'Pierre protection angle. Borne, mur.'),
    ('man_made', 'pit'): ('Fosse', 'Trou, excavation. Extraction.'),
    ('man_made', 'platform'): ('Plateforme', 'Surface aménagée. Quai, terrasse.'),
    ('man_made', 'clear_cut'): ('Coupe rase', 'Zone déboisée. Exploitation forêt.'),
    ('man_made', 'silo'): ('Silo', 'Silo agricole. Stockage grain, fourrage.'),
    ('man_made', 'fuel_storage_tank'): ('Cuve carburant', 'Réservoir combustible. Station, stockage.'),
    ('man_made', 'solar_panel'): ('Panneau solaire', 'Installation photovoltaïque. Énergie renouvelable.'),
    ('man_made', 'ski_jump'): ('Tremplin ski', 'Saut à ski. Compétition, envol.'),
    ('man_made', 'oil_well'): ('Puits pétrole', 'Forage pétrolier. Extraction, derrick.'),
    ('man_made', 'pole'): ('Poteau', 'Mât, support. Électricité, téléphone.'),
    ('man_made', 'ceremonial_gate'): ('Porte cérémoniale', 'Entrée monumentale. Sacré, tradition.'),
    ('man_made', 'quay'): ('Quai', 'Quai portuaire. Accostage, bateau.'),
    ('man_made', 'water_wello'): ('Puits eau', 'Puits, source. Eau souterraine.'),
    ('man_made', 'chinese_fishing_net'): ('Filet chinois', 'Carrelet, filet levant. Pêche, Inde.'),
    ('man_made', 'water_pump'): ('Pompe eau', 'Station pompage. Puits, irrigation.'),
    ('man_made', 'telephone_office'): ('Central téléphonique', 'NRA, standard. Télécom.'),
    ('man_made', 'footwear_decontamination'): ('Désinfection chaussures', 'Pédiluve, nettoyage. Biosécurité.'),
    ('man_made', 'tomb'): ('Tombeau', 'Sépulture, mausolée. Cimetière.'),
    ('man_made', 'storage_tank'): ('Cuve stockage', 'Réservoir, citerne. Liquide, gaz.'),
    ('man_made', 'oil_tank'): ('Cuve pétrole', 'Réservoir fioul. Chauffage, stockage.'),
    ('man_made', 'traffic_signals'): ('Feux tricolores', 'Signalisation lumineuse. Carrefour.'),
    ('man_made', 'kraal'): ('Kraal', 'Enclos bétail africain. Village, protection.'),
    ('man_made', 'tailings_pond'): ('Bassin résidus', 'Lagune minière, stériles. Décantation.'),
    ('man_made', 'expansion_joint'): ('Joint dilatation', 'Raccord pont, bâtiment. Mouvement.'),
    ('man_made', 'birdhouse'): ('Nichoir', 'Maison oiseaux. Jardin, nidification.'),
    ('man_made', 'species_protection_tower'): ('Tour protection espèces', 'Abri faune, cigogne. Conservation.'),
    ('man_made', 'motorized_borehole'): ('Forage motorisé', 'Pompe électrique, puits. Eau.'),
    ('man_made', 'submarine_cable'): ('Câble sous-marin', 'Fibre optique mer. Télécom.'),
    ('man_made', 'heap'): ('Terril', 'Tas déblais, mine. Résidus.'),
    ('man_made', 'ice_house'): ('Glacière', 'Réserve glace ancienne. Conservation froid.'),
    ('man_made', 'guy_wire_anchor'): ('Ancrage hauban', 'Point fixation câble. Tension.'),
    ('man_made', 'gantry'): ('Portique', 'Pont roulant, grue. Chargement.'),
    ('man_made', 'bunker_silo'): ('Silo couloir', 'Stockage fourrage ouvert. Ensilage.'),
    ('man_made', 'survey_point'): ('Point géodésique', 'Borne IGN, triangulation. Topographie.'),
    ('man_made', 'flower_bed'): ('Massif fleuri', 'Parterre jardin. Fleurs, décoration.'),
    ('man_made', 'well'): ('Puits', 'Puits d\'eau. Source, margelle.'),
    ('man_made', 'chiller'): ('Groupe froid', 'Climatisation, refroidissement. Industrie.'),
    ('man_made', 'column'): ('Colonne', 'Pilier, poteau. Monument, soutien.'),
    ('man_made', 'composting_plant'): ('Centre compostage', 'Plateforme déchets verts. Recyclage.'),
    ('man_made', 'wastewater_basin'): ('Bassin épuration', 'Lagune traitement eaux usées.'),
    ('man_made', 'bioswale'): ('Noue', 'Fossé végétalisé. Gestion eaux pluviales.'),
    ('man_made', 'guy_anchor'): ('Ancrage', 'Point fixation hauban. Câble, tension.'),
    ('man_made', 'graduation_tower'): ('Tour graduation', 'Saline, évaporation. Sel, cure.'),
    ('man_made', 'water'): ('Eau', 'Point d\'eau artificiel. Source.'),
    ('man_made', 'construction'): ('Construction', 'Chantier, travaux. Bâtiment.'),
    ('man_made', 'clothes_line'): ('Étendoir', 'Fil à linge. Séchage vêtements.'),
    ('man_made', 'culvert'): ('Buse', 'Passage busé, canalisation. Ruisseau, route.'),
    ('man_made', 'wildlife_crossing'): ('Passage faune', 'Écoduc, pont animaux. Autoroute.'),
    ('man_made', 'gully'): ('Caniveau', 'Rigole, avaloir. Écoulement eau.'),
    ('man_made', 'protected_spring'): ('Source captée', 'Captage protégé. Eau potable.'),
    ('man_made', 'dew_pond'): ('Mare à rosée', 'Bassin collecte rosée. Abreuvoir.'),
    ('man_made', 'fire_break'): ('Coupe-feu', 'Pare-feu forestier. Incendie, prévention.'),
    ('man_made', 'feedlot'): ('Parc engraissement', 'Élevage intensif. Bétail.'),

    # =====================
    # CLUB
    # =====================
    ('club', 'politics'): ('Club politique', 'Association politique. Parti, militantisme.'),
    ('club', 'culture'): ('Club culturel', 'Association culturelle. Art, patrimoine, échanges.'),
    ('club', 'freemasonry'): ('Loge maçonnique', 'Franc-maçonnerie, temple. Initiation, fraternité.'),
    ('club', 'birds'): ('Club ornithologie', 'Association oiseaux. Observation, LPO, jumelles.'),
    ('club', 'dog'): ('Club canin', 'Association chiens. Dressage, élevage, concours.'),
    ('club', 'hunting'): ('Société chasse', 'Association chasseurs. Permis, battue, gibier.'),
    ('club', 'baduk'): ('Club de go', 'Association jeu de go. Baduk, wei-chi, plateau.'),
    ('club', 'aviation'): ('Aéroclub', 'Club aviation. Pilotage, ULM, avion.'),
    ('club', 'smoke'): ('Club fumeurs', 'Association amateurs cigares. Tabac, dégustation.'),
    ('club', 'scout'): ('Scouts', 'Groupe scout. Jeunesse, camp, nature, badges.'),
    ('club', 'filmmaking'): ('Club cinéma', 'Association cinéastes amateurs. Courts-métrages.'),
    ('club', 'youth_movement'): ('Mouvement jeunesse', 'Association jeunes. Éducation, loisirs.'),
    ('club', 'photography'): ('Club photo', 'Association photographes. Expositions, sorties.'),
    ('club', 'woodworking'): ('Club menuiserie', 'Atelier bois. Ébénisterie, bricolage.'),
    ('club', 'sailing'): ('Club voile', 'École de voile. Navigation, régate.'),
    ('club', 'amateur_radio'): ('Club radioamateur', 'Association radio. Émission, antenne.'),
    ('club', 'charity'): ('Association caritative', 'Bénévoles, entraide. Secours, aide.'),
    ('club', 'sport'): ('Club sportif', 'Association sportive. Entraînement, compétition.'),
    ('club', 'société_de_boule_de_fort'): ('Boule de fort', 'Jeu traditionnel Anjou. Pétanque locale.'),
    ('club', 'fishing'): ('Club pêche', 'Association pêcheurs. Permis, rivière, étang.'),
    ('club', 'motorcycle'): ('Club moto', 'Association motards. Balades, rassemblements.'),
    ('club', 'shooting'): ('Club de tir', 'Stand de tir sportif. Armes, compétition.'),
    ('club', 'art'): ('Club art', 'Association artistique. Peinture, dessin, expo.'),
    ('club', 'gardening'): ('Club jardinage', 'Association jardiniers. Potager, conseils.'),
    ('club', 'automobile'): ('Club automobile', 'Association voitures. Collection, rallye.'),
    ('club', 'tourism'): ('Club tourisme', 'Association voyages. Excursions, découverte.'),
    ('club', 'local_food'): ('Club gastronomie', 'Association produits locaux. Terroir, goût.'),
    ('club', 'anarchist'): ('Club anarchiste', 'Association libertaire. Politique, militantisme.'),
    ('club', 'social'): ('Club social', 'Association entraide. Rencontres, solidarité.'),
    ('club', 'nudism'): ('Club naturiste', 'Association nudistes. FKK, camping naturiste.'),
    ('club', 'game'): ('Club jeux', 'Association jeux société. Soirées, plateau, cartes.'),
    ('club', 'hackerspace'): ('Hackerspace', 'Fablab, makerspace. Électronique, code, création.'),
    ('club', 'fan'): ('Club fans', 'Association supporters. Groupe, passion.'),
    ('club', 'yachting'): ('Club nautique', 'Yacht club. Voiliers, régates.'),
    ('club', 'model_railway'): ('Club train miniature', 'Association modélisme ferroviaire. Maquettes.'),
    ('club', 'card_games'): ('Club jeux cartes', 'Association bridge, belote, tarot. Tournois.'),
    ('club', 'cooking'): ('Club cuisine', 'Association gastronomique. Recettes, ateliers.'),
    ('club', 'student'): ('Club étudiant', 'Association étudiants, BDE. Campus, soirées.'),
    ('club', 'aeronautical'): ('Club aéronautique', 'Association aviation. Pilotage, construction.'),
    ('club', 'astronomy'): ('Club astronomie', 'Association astronomes. Télescope, étoiles.'),
    ('club', 'linux'): ('Club Linux', 'Association informatique libre. Open source.'),
    ('club', 'fraternity'): ('Confrérie', 'Association fraternelle. Tradition, initiation.'),
    ('club', 'computer'): ('Club informatique', 'Association ordinateurs. Programmation, aide.'),
    ('club', 'youth'): ('Club jeunes', 'Maison des jeunes. MJC, activités, ados.'),
    ('club', 'cannabis'): ('Cannabis social club', 'Association cannabis. Usage collectif.'),
    ('club', 'veterans'): ('Anciens combattants', 'Association vétérans. Mémoire, entraide.'),
    ('club', 'chess'): ('Club échecs', 'Association échiquéenne. Tournois, parties.'),
    ('club', 'allotments'): ('Jardins familiaux', 'Association jardins ouvriers. Parcelles, potager.'),
    ('club', 'cadet'): ('Cadets', 'Formation jeunesse. Préparation militaire.'),
    ('club', 'scuba_diving'): ('Club plongée', 'Association plongée sous-marine. PADI, FFESSM.'),
    ('club', 'juggling'): ('Club jonglerie', 'Association jongleurs. Cirque, balles.'),

    # =====================
    # DIET
    # =====================
    ('diet', 'no lactose in food'): ('Sans lactose', 'Cuisine sans lactose. Intolérance, produits laitiers.'),
    ('diet', 'full-fat food with little to no carbs, and 0 added sugar'): ('Régime cétogène', 'Cuisine keto, low carb. Gras, sans sucre.'),
    ('diet', 'kosher food, permissible for observant Jews'): ('Casher', 'Nourriture casher. Juif, religion, certifié.'),
    ('diet', 'no gluten in food'): ('Sans gluten', 'Cuisine sans gluten. Cœliaque, intolérance.'),
    ('diet', 'no fish or meat, synonym for ovo-lacto-vegetarian'): ('Végétarien', 'Sans viande ni poisson. Œufs, lait acceptés.'),
    ('diet', 'halal food, permissible for consumption by Muslims'): ('Halal', 'Nourriture halal. Musulman, religion, certifié.'),

    # =====================
    # PAYMENT
    # =====================
    ('payment', 'If you can pay with notes (paper money).'): ('Billets acceptés', 'Paiement en espèces, billets. Cash, liquide.'),
    ('payment', 'Used to indicate that a venue has \'contactless\' (only RFID/NFC-based) payment options'): ('Sans contact', 'Paiement sans contact. NFC, CB, Apple Pay.'),
    ('payment', 'Common credit cards'): ('Cartes crédit', 'Visa, Mastercard, American Express. CB.'),
    ('payment', 'none'): ('Gratuit', 'Aucun paiement requis. Service gratuit.'),
    ('payment', 'Payment by card (of any type). Should only be used to specify that cards arenotaccepted[1]'): ('Carte', 'Paiement par carte. CB, débit, crédit.'),
    ('payment', 'Payment can be done in cash (coins or notes) of the locally common currency'): ('Espèces', 'Paiement cash, argent liquide. Pièces, billets.'),
    ('payment', 'Common debit cards'): ('Cartes débit', 'Carte bancaire débit. CB, Maestro.'),
    ('payment', 'Payment options where you scan a QR code with your mobile device'): ('QR code', 'Paiement QR code. Téléphone, scan, mobile.'),

    # =====================
    # WHEELCHAIR
    # =====================
    ('wheelchair', '1'): ('Accessible', 'Accès fauteuil roulant possible.'),
    ('wheelchair', 'unknown'): ('Accessibilité inconnue', 'Information accessibilité non renseignée.'),
    ('wheelchair', 'wheelchair_access'): ('Accès PMR', 'Accessible fauteuils roulants. Handicapé.'),
    ('wheelchair', 'destination'): ('Accès destination', 'Accessible à destination finale.'),
    ('wheelchair', 'official'): ('Officiellement accessible', 'Accessibilité officielle PMR.'),
    ('wheelchair', 'half'): ('Partiellement accessible', 'Accès PMR partiel. Aide nécessaire.'),
    ('wheelchair', 'designated'): ('Espace désigné', 'Place réservée handicapé.'),
    ('wheelchair', 'bad'): ('Mal accessible', 'Difficile fauteuil roulant. Obstacles.'),

    # =====================
    # INTERNET_ACCESS
    # =====================
    ('internet_access', 'wlan;terminal'): ('Wifi et terminal', 'Wifi et ordinateur disponibles. Accès internet.'),
    ('internet_access', 'terminal;wlan'): ('Terminal et wifi', 'Ordinateur et wifi disponibles. Internet.'),

    # =====================
    # SMOKING
    # =====================
    ('smoking', 'yes'): ('Fumeurs acceptés', 'Zone fumeurs autorisée. Cigarette permise.'),
    ('smoking', 'separated'): ('Zone séparée', 'Espace fumeurs isolé. Section distincte.'),
    ('smoking', 'designated'): ('Zone désignée', 'Espace fumeurs défini. Coin cigarette.'),

    # =====================
    # OUTDOOR_SEATING
    # =====================
    ('outdoor_seating', 'balcony'): ('Balcon', 'Places assises balcon. Vue, extérieur.'),
    ('outdoor_seating', 'pedestrian_zone'): ('Zone piétonne', 'Terrasse zone piétonne. Rue, plein air.'),
    ('outdoor_seating', 'street'): ('Rue', 'Terrasse sur rue. Trottoir, extérieur.'),
    ('outdoor_seating', 'veranda'): ('Véranda', 'Places sous véranda. Couvert, vue.'),
    ('outdoor_seating', 'sidewalk;street'): ('Trottoir et rue', 'Terrasse trottoir et rue.'),
    ('outdoor_seating', 'terrace'): ('Terrasse', 'Terrasse extérieure. Tables dehors, soleil.'),
    ('outdoor_seating', 'only'): ('Uniquement extérieur', 'Places extérieures seulement. Terrasse.'),
    ('outdoor_seating', 'beach'): ('Plage', 'Terrasse sur plage. Sable, mer.'),
    ('outdoor_seating', 'patio'): ('Patio', 'Cour intérieure. Jardin, calme.'),
    ('outdoor_seating', 'sidewalk'): ('Trottoir', 'Terrasse trottoir. Rue, passants.'),
    ('outdoor_seating', 'roof'): ('Toit', 'Rooftop, terrasse toit. Vue panoramique.'),
    ('outdoor_seating', 'parklet'): ('Parklet', 'Terrasse sur parking. Extension rue.'),

    # =====================
    # TAKEAWAY
    # =====================
    ('takeaway', 'no'): ('Pas d\'emporter', 'Sur place uniquement. Pas de vente à emporter.'),
    ('takeaway', 'only'): ('Emporter seulement', 'Vente à emporter uniquement. Pas sur place.'),

    # =====================
    # DELIVERY
    # =====================
    ('delivery', 'only'): ('Livraison seule', 'Uniquement en livraison. Pas sur place.'),

    # =====================
    # DRIVE_THROUGH
    # =====================
    ('drive_through', 'only'): ('Drive uniquement', 'Service au volant seulement.'),

    # =====================
    # RESERVATION
    # =====================
    ('reservation', 'accepted'): ('Réservation acceptée', 'Possibilité de réserver. Conseillé.'),
    ('reservation', 'required'): ('Réservation obligatoire', 'Réserver impérativement. Sur rendez-vous.'),
    ('reservation', 'members_only'): ('Membres seulement', 'Réservation adhérents uniquement.'),
    ('reservation', 'only'): ('Sur réservation', 'Uniquement sur réservation préalable.'),
    ('reservation', 'recommended'): ('Réservation conseillée', 'Mieux vaut réserver. Recommandé.'),

    # =====================
    # SELF_SERVICE
    # =====================
    ('self_service', 'partially'): ('Self partiel', 'Libre-service partiel. Assistance disponible.'),
    ('self_service', 'only'): ('Self uniquement', 'Libre-service uniquement. Autonome.'),

    # =====================
    # BULK/SECOND_HAND
    # =====================
    ('bulk_purchase', 'only'): ('Vrac uniquement', 'Vente en vrac seulement. Sans emballage.'),
    ('second_hand', 'only'): ('Occasion seulement', 'Uniquement articles d\'occasion. Seconde main.'),

    # =====================
    # DRINK/BREWERY
    # =====================
    ('drink', 'beer'): ('Bière', 'Bière servie. Pression, bouteille.'),
    ('drink', 'water'): ('Eau', 'Eau disponible. Carafe, bouteille.'),
    ('drink', 'wine'): ('Vin', 'Vin servi. Rouge, blanc, rosé.'),
    ('brewery', 'yes;various'): ('Plusieurs brasseries', 'Bières de plusieurs brasseries.'),
    ('brewery', 'various;yes'): ('Brasseries diverses', 'Choix de brasseries variées.'),
    ('brewery', 'various'): ('Brasseries variées', 'Différentes brasseries représentées.'),
    ('brewery', 'Krombacher'): ('Krombacher', 'Bière Krombacher allemande.'),
    ('brewery', 'Augustiner Bräu München'): ('Augustiner', 'Brasserie Augustiner Munich.'),
    ('brewery', 'Guinness'): ('Guinness', 'Bière Guinness irlandaise. Stout.'),

    # =====================
    # BREAKFAST/LUNCH
    # =====================
    ('breakfast', 'buffet'): ('Petit-déjeuner buffet', 'Buffet petit-déjeuner. À volonté.'),
    ('lunch', 'menu'): ('Menu déjeuner', 'Formule midi. Plat du jour.'),

    # =====================
    # FITNESS_STATION
    # =====================
    ('fitness_station', 'Other'): ('Autre équipement', 'Autre appareil fitness. Exercice extérieur.'),
    ('fitness_station', 'parallel_bars'): ('Barres parallèles', 'Barres parallèles, dips. Musculation bras, épaules.'),
    ('fitness_station', 'horizontal_bar'): ('Barre fixe', 'Barre fixe, tractions. Pull-ups, musculation dos.'),
    ('fitness_station', 'push-up'): ('Push-up', 'Support pompes. Musculation pectoraux, bras.'),
    ('fitness_station', 'rower'): ('Rameur', 'Rameur extérieur. Cardio, aviron, dos.'),
    ('fitness_station', 'rings'): ('Anneaux', 'Anneaux gymnastique. Suspension, musculation.'),
    ('fitness_station', 'Legs'): ('Jambes', 'Appareil jambes. Cuisses, mollets.'),
    ('fitness_station', 'Core'): ('Abdos', 'Appareil abdominaux. Gainage, core.'),
    ('fitness_station', 'leg_press'): ('Presse jambes', 'Presse à jambes. Cuisses, fessiers.'),
    ('fitness_station', 'stretch_bars'): ('Barres étirement', 'Barres pour étirements. Souplesse.'),
    ('fitness_station', 'stepping_stone'): ('Pas japonais', 'Pierres de passage. Équilibre.'),
    ('fitness_station', 'balance_beam'): ('Poutre équilibre', 'Poutre d\'équilibre. Coordination.'),
    ('fitness_station', 'sign'): ('Panneau', 'Panneau instructions. Exercices, consignes.'),
    ('fitness_station', 'fitness_station'): ('Station fitness', 'Équipement sport extérieur. Exercices.'),
    ('fitness_station', 'Stretching'): ('Étirements', 'Zone étirements. Souplesse, récupération.'),
    ('fitness_station', 'beam_jump'): ('Sauts poutre', 'Poutre pour sauts. Coordination, équilibre.'),
    ('fitness_station', 'Push'): ('Poussée', 'Exercice poussée. Pompes, pectoraux.'),
    ('fitness_station', 'stairs'): ('Escaliers', 'Escaliers exercice. Cardio, jambes.'),
    ('fitness_station', 'steering_wheel'): ('Roue', 'Roue d\'exercice. Épaules, mobilité.'),
    ('fitness_station', 'sit-up'): ('Abdominaux', 'Banc abdos, sit-ups. Crunch, gainage.'),
    ('fitness_station', 'ab_twist'): ('Rotation tronc', 'Appareil rotation abdos. Obliques, taille.'),
    ('fitness_station', 'hyperextension'): ('Hyperextension', 'Banc lombaires. Dos, renforcement.'),
    ('fitness_station', 'exercise_bike'): ('Vélo', 'Vélo d\'exercice extérieur. Cardio, jambes.'),
    ('fitness_station', 'wall_bars'): ('Espalier', 'Espalier, échelle murale. Étirements, suspension.'),
    ('fitness_station', 'box'): ('Box', 'Boîte saut, step. Pliométrie.'),
    ('fitness_station', 'chest_press'): ('Développé couché', 'Appareil pectoraux. Poitrine, triceps.'),
    ('fitness_station', 'captains_chair'): ('Chaise romaine', 'Chaise capitaine. Abdos, jambes.'),
    ('fitness_station', 'elliptical_trainer'): ('Elliptique', 'Vélo elliptique extérieur. Cardio complet.'),
    ('fitness_station', 'horizontal_ladder'): ('Échelle horizontale', 'Échelle suspendue. Bras, grip.'),
    ('fitness_station', 'slalom'): ('Slalom', 'Parcours slalom. Agilité, coordination.'),
    ('fitness_station', 'slackline'): ('Slackline', 'Sangle équilibre. Balance, concentration.'),
    ('fitness_station', 'Pull'): ('Traction', 'Exercice traction. Dos, biceps.'),
    ('fitness_station', 'air_walker'): ('Simulateur marche', 'Air walker, marcheur. Cardio, jambes.'),

    # =====================
    # BUILDING (additional)
    # =====================
    ('building', 'windmill'): ('Moulin à vent', 'Moulin à vent. Historique, patrimoine.'),
    ('building', 'yes'): ('Bâtiment', 'Bâtiment, construction. Édifice quelconque.'),
    ('building', 'quonset_hut'): ('Hangar Quonset', 'Hangar demi-cylindre. Militaire, stockage.'),
    ('building', 'outbuilding'): ('Dépendance', 'Annexe, dépendance. Remise, abri.'),
    ('building', 'kingdom_hall'): ('Salle du Royaume', 'Salle Témoins de Jéhovah. Culte.'),
    ('building', 'container'): ('Container', 'Conteneur aménagé. Bureau, local.'),
    ('building', 'triumphal_arch'): ('Arc de triomphe', 'Arc monumental. Victoire, monument.'),
    ('building', 'ship'): ('Navire', 'Bateau musée, navire-bâtiment. Maritime.'),
    ('building', 'allotment_house'): ('Abri de jardin', 'Cabanon jardin ouvrier. Jardins familiaux.'),
    ('building', 'digester'): ('Digesteur', 'Cuve méthanisation. Biogaz, agricole.'),
    ('building', 'stilt_house'): ('Maison pilotis', 'Maison sur pilotis. Marécage, inondation.'),

    # =====================
    # LANDUSE
    # =====================
    ('landuse', 'institutional'): ('Institutionnel', 'Zone institutionnelle. Administration, services publics.'),
    ('landuse', 'animal_keeping'): ('Élevage', 'Zone d\'élevage animaux. Ferme, pâturage.'),
    ('landuse', 'port'): ('Port', 'Zone portuaire. Quais, activité maritime.'),

    # =====================
    # NATURAL
    # =====================
    ('natural', 'isthmus'): ('Isthme', 'Isthme, bande terre. Relie deux terres.'),
    ('natural', 'shrubbery'): ('Buissons', 'Zone arbustive. Taillis, végétation basse.'),
    ('natural', 'tree_stump'): ('Souche', 'Souche d\'arbre. Arbre coupé.'),
    ('natural', 'shoal'): ('Haut-fond', 'Banc de sable, haut-fond. Danger navigation.'),
    ('natural', 'fumarole'): ('Fumerolle', 'Fumerolle volcanique. Vapeur, gaz.'),
    ('natural', 'dune'): ('Dune', 'Dune de sable. Plage, désert.'),

    # =====================
    # HIGHWAY (technical values)
    # =====================
    ('highway', 'traffic_sign'): ('Panneau routier', 'Panneau signalisation routière.'),
    ('highway', 'shared_lane'): ('Voie partagée', 'Chaussée partagée vélo-voiture.'),
    ('highway', 'ladder'): ('Échelle', 'Échelle accès. Sentier vertical.'),
    ('highway', 'bus_guideway'): ('Site propre bus', 'Voie bus guidée. BHNS, tram-bus.'),
    ('highway', 'hitchhiking'): ('Auto-stop', 'Point auto-stop. Covoiturage spontané.'),
    ('highway', 'share_busway'): ('Voie bus partagée', 'Couloir bus ouvert aux vélos.'),
    ('highway', 'opposite_lane'): ('Contresens cyclable', 'Voie vélo sens inverse. Double sens.'),
    ('highway', 'traffic_signals;crossing'): ('Feux et passage', 'Carrefour feux avec passage piéton.'),
    ('highway', 'raceway'): ('Circuit', 'Piste course automobile. Karting, rallye.'),
    ('highway', 'piste'): ('Piste ski', 'Piste de ski. Montagne, neige.'),
    ('highway', 'proposed'): ('Projet', 'Route en projet. Construction future.'),
    ('highway', 'phone'): ('Téléphone', 'Borne téléphone urgence. SOS, autoroute.'),
    ('highway', 'crossing;traffic_signals'): ('Passage avec feux', 'Passage piéton avec feux.'),
    ('highway', 'traffic_mirror'): ('Miroir routier', 'Miroir de virage. Visibilité.'),
    ('highway', 'disused'): ('Désaffecté', 'Route désaffectée. Plus utilisée.'),
    ('highway', 'traffic_island'): ('Îlot directionnel', 'Refuge piéton, îlot. Sécurité.'),
    ('highway', 'planned'): ('Planifié', 'Route planifiée. Projet.'),
    ('highway', 'stop;crossing'): ('Stop et passage', 'Stop avec passage piéton.'),
    ('highway', 'sidewalk'): ('Trottoir', 'Trottoir, accotement piéton.'),
    ('highway', 'opposite_share_busway'): ('Contresens bus', 'Couloir bus-vélo sens inverse.'),
    ('highway', 'traffic_calming'): ('Modération trafic', 'Aménagement ralentissement. Zone 30.'),
    ('highway', 'cyclist_waiting_aid'): ('Appui vélo', 'Repose-pied cycliste feu rouge.'),
    ('highway', 'toll_gantry'): ('Portique péage', 'Péage sans barrière. Flux libre.'),
    ('highway', 'scramble'): ('Passage diagonal', 'Traversée toutes directions. Shibuya.'),
    ('highway', 'dummy'): ('Factice', 'Élément fictif. Données test.'),
    ('highway', 'opposite'): ('Contresens', 'Sens inverse autorisé. Vélo.'),
    ('highway', 'corridor'): ('Couloir', 'Passage intérieur. Galerie.'),
    ('highway', 'priority'): ('Priorité', 'Voie prioritaire. Passage.'),
    ('highway', 'fake_speed_camera'): ('Radar factice', 'Faux radar, leurre. Dissuasion.'),
    ('highway', 'razed'): ('Supprimé', 'Route supprimée. Détruite.'),
    ('highway', 'abandoned'): ('Abandonné', 'Route abandonnée. Plus entretenue.'),
    ('highway', 'busway'): ('Voie bus', 'Site propre bus. BHNS.'),
    ('highway', 'speed_display'): ('Afficheur vitesse', 'Radar pédagogique. Smiley.'),
    ('highway', 'opposite_track'): ('Piste contresens', 'Piste cyclable sens inverse.'),

    # =====================
    # RAILWAY
    # =====================
    ('railway', 'beacon'): ('Balise ferroviaire', 'Balise signalisation train. KVB.'),
    ('railway', 'derail'): ('Dérailleur', 'Dispositif déraillement sécurité. Protection.'),
    ('railway', 'spur_junction'): ('Bifurcation', 'Embranchement voie ferrée. Aiguillage.'),
    ('railway', 'track_scale'): ('Pont-bascule', 'Balance ferroviaire. Pesage wagons.'),
    ('railway', 'vacancy_detection'): ('Détection présence', 'Capteur occupation voie. Signalisation.'),
    ('railway', 'rolling_highway'): ('Ferroutage', 'Transport combiné rail-route. Autoroute ferroviaire.'),
    ('railway', 'crossover'): ('Communication', 'Liaison deux voies. Changement voie.'),
    ('railway', 'station_crossing'): ('Passage en gare', 'Traversée voies en gare.'),
    ('railway', 'preheating'): ('Préchauffage', 'Installation préchauffage trains. Hiver.'),
    ('railway', 'tram_stop'): ('Arrêt tram', 'Station tramway. Transport urbain.'),
    ('railway', 'ventilation_shaft'): ('Puits ventilation', 'Aération tunnel. Métro.'),
    ('railway', 'hirail_access'): ('Accès rail-route', 'Point entrée véhicule rail-route.'),
    ('railway', 'isolated_track_section'): ('Section isolée', 'Portion voie coupure électrique.'),
    ('railway', 'disused_halt'): ('Halte désaffectée', 'Ancien arrêt. Fermé.'),
    ('railway', 'block'): ('Bloc', 'Canton signalisation. Block ferroviaire.'),
    ('railway', 'unloading_hole'): ('Trémie déchargement', 'Fosse déchargement. Vrac.'),
    ('railway', 'interlocking'): ('Poste d\'aiguillage', 'Enclenchement, PRS. Signalisation.'),
    ('railway', 'signal_box'): ('Poste signalisation', 'Cabine aiguilleur. Contrôle.'),
    ('railway', 'turntable'): ('Plaque tournante', 'Rotation locomotives. Dépôt.'),
    ('railway', 'container_terminal'): ('Terminal conteneurs', 'Plateforme intermodale. Fret.'),
    ('railway', 'car_shuttle'): ('Navette auto', 'Train auto-couchettes. Eurotunnel.'),
    ('railway', 'key_switch'): ('Interrupteur clé', 'Commande par clé. Passage niveau.'),
    ('railway', 'water_tower'): ('Château d\'eau', 'Réservoir eau locomotives vapeur.'),
    ('railway', 'loading_ramp'): ('Rampe chargement', 'Quai marchandises. Wagon.'),
    ('railway', 'traverser'): ('Chariot transbordeur', 'Pont roulant dépôt. Déplacement.'),
    ('railway', 'engine_shed'): ('Rotonde', 'Dépôt locomotives. Remise.'),
    ('railway', 'technical_station'): ('Gare technique', 'Installations maintenance. Atelier.'),
    ('railway', 'rail_brake'): ('Frein de voie', 'Ralentisseur wagons. Triage.'),
    ('railway', 'aei'): ('Détecteur boîte chaude', 'Capteur température essieux.'),
    ('railway', 'phone'): ('Téléphone voie', 'Borne appel ferroviaire.'),
    ('railway', 'demolished'): ('Démoli', 'Infrastructure détruite. Disparu.'),
    ('railway', 'border'): ('Frontière', 'Point frontière ferroviaire.'),
    ('railway', 'dismantled'): ('Démonté', 'Voie démantelée. Plus de rails.'),
    ('railway', 'platform_marker'): ('Repère quai', 'Marquage arrêt train. Position.'),
    ('railway', 'siding'): ('Voie de garage', 'Voie évitement. Stationnement.'),
    ('railway', 'disused_station'): ('Gare désaffectée', 'Ancienne gare. Fermée.'),
    ('railway', 'workshop'): ('Atelier', 'Atelier maintenance trains.'),
    ('railway', 'facility'): ('Installation', 'Équipement ferroviaire.'),
    ('railway', 'crane'): ('Grue', 'Grue ferroviaire. Manutention.'),
    ('railway', 'blockpost'): ('Poste bloc', 'Signalisation de bloc.'),
    ('railway', 'planned'): ('Planifié', 'Voie en projet. Futur.'),
    ('railway', 'pit'): ('Fosse', 'Fosse inspection, visite. Maintenance.'),
    ('railway', 'spur'): ('Embranchement', 'Voie particulière. Desserte.'),
    ('railway', 'railway_crossing'): ('Croisement voies', 'Intersection lignes ferrées.'),
    ('railway', 'train_station_entrance'): ('Entrée gare', 'Accès hall voyageurs.'),
    ('railway', 'lamp'): ('Lampe signal', 'Lanterne ferroviaire.'),
    ('railway', 'railway'): ('Voie ferrée', 'Infrastructure ferroviaire. Rails.'),
    ('railway', 'radio'): ('Radio', 'Équipement radio GSM-R.'),
    ('railway', 'unpaved'): ('Non ballasté', 'Voie sans ballast.'),
    ('railway', 'tram_crossing'): ('Croisement tram', 'Passage à niveau tramway.'),
    ('railway', 'roundhouse'): ('Rotonde', 'Dépôt circulaire. Locomotives.'),
    ('railway', 'defect_detector'): ('Détecteur défaut', 'Capteur anomalie roue, rail.'),
    ('railway', 'depot'): ('Dépôt', 'Garage trains. Maintenance, remisage.'),
    ('railway', 'hump_yard'): ('Gare de triage', 'Butte débranchement. Wagons.'),
    ('railway', 'loading_rack'): ('Portique chargement', 'Rack manutention. Conteneurs.'),
    ('railway', 'balise_group'): ('Groupe balises', 'Balises KVB, ERTMS.'),
    ('railway', 'power_supply'): ('Alimentation', 'Sous-station électrique. Traction.'),
    ('railway', 'site'): ('Site', 'Emprise ferroviaire.'),
    ('railway', 'historic'): ('Historique', 'Patrimoine ferroviaire ancien.'),
    ('railway', 'loading_tower'): ('Tour chargement', 'Silo, trémie. Vrac.'),
    ('railway', 'adjacent'): ('Adjacent', 'Voie adjacente. Parallèle.'),
    ('railway', 'service_station'): ('Gare de service', 'Installations techniques.'),
    ('railway', 'razed'): ('Rasé', 'Infrastructure détruite.'),
    ('railway', 'owner_change'): ('Changement propriétaire', 'Limite gestionnaire infrastructure.'),
    ('railway', 'tram_traffic_signals'): ('Feux tramway', 'Signalisation lumineuse tram.'),
    ('railway', 'platform_edge'): ('Bord quai', 'Limite quai, bordure.'),
    ('railway', 'track_ballast'): ('Ballast', 'Graviers voie ferrée.'),
    ('railway', 'lubricator'): ('Graisseur rail', 'Lubrification courbes.'),
    ('railway', 'junction'): ('Jonction', 'Point bifurcation. Convergence.'),

    # =====================
    # WATERWAY
    # =====================
    ('waterway', 'lock_gate'): ('Porte écluse', 'Vantail écluse. Navigation.'),
    ('waterway', 'depth'): ('Profondeur', 'Indication profondeur. Navigation.'),
    ('waterway', 'pressurised'): ('Sous pression', 'Conduite forcée. Hydraulique.'),
    ('waterway', 'hazard'): ('Danger', 'Obstacle navigation. Risque.'),
    ('waterway', 'soakhole'): ('Puisard', 'Infiltration eau. Drainage.'),
    ('waterway', 'stream_end'): ('Fin ruisseau', 'Perte cours d\'eau. Disparition.'),
    ('waterway', 'security_lock'): ('Écluse sécurité', 'Écluse protection inondation.'),
    ('waterway', 'proposed'): ('Projet', 'Voie d\'eau en projet.'),
    ('waterway', 'brook'): ('Ruisselet', 'Petit ruisseau. Filet d\'eau.'),
    ('waterway', 'milestone'): ('Borne', 'Borne kilométrique canal.'),
    ('waterway', 'drainage_channel'): ('Fossé drainage', 'Canal d\'assèchement.'),
    ('waterway', 'sanitary_dump_station'): ('Vidange bateaux', 'Station eaux usées plaisance.'),
    ('waterway', 'water_point'): ('Point d\'eau', 'Prise eau bateaux.'),
    ('waterway', 'oxbow'): ('Méandre mort', 'Bras mort, ancien lit. Oxbow.'),
    ('waterway', 'canoe_pass'): ('Passe canoë', 'Contournement barrage. Kayak.'),
    ('waterway', 'riverbed'): ('Lit rivière', 'Fond cours d\'eau.'),
    ('waterway', 'debris_screen'): ('Grille', 'Dégrilleur, filtre débris.'),
    ('waterway', 'flowline'): ('Conduite', 'Canalisation souterraine.'),
    ('waterway', 'artificial'): ('Artificiel', 'Canal artificiel. Creusé.'),
    ('waterway', 'drystream'): ('Ruisseau sec', 'Lit à sec. Intermittent.'),
    ('waterway', 'turning_point'): ('Point virage', 'Zone demi-tour bateaux.'),
    ('waterway', 'connector'): ('Liaison', 'Raccord canaux.'),
    ('waterway', 'link'): ('Lien', 'Connexion voies d\'eau.'),
    ('waterway', 'drain_inlet'): ('Avaloir', 'Entrée drain, regard.'),
    ('waterway', 'fairway'): ('Chenal', 'Chenal navigable. Balisé.'),
    ('waterway', 'access_point'): ('Point accès', 'Mise à l\'eau, embarquement.'),
    ('waterway', 'flow_control'): ('Régulation débit', 'Vannage, contrôle.'),
    ('waterway', 'dyke'): ('Digue', 'Protection inondation.'),
    ('waterway', 'floodgate'): ('Vanne crue', 'Porte inondation.'),
    ('waterway', 'floating_barrier'): ('Barrage flottant', 'Estacade, retenue flottants.'),
    ('waterway', 'sluice_gate'): ('Vanne', 'Vanne écluse. Régulation.'),
    ('waterway', 'check_dam'): ('Seuil', 'Barrage correction. Torrent.'),
    ('waterway', 'construction'): ('Construction', 'Travaux en cours.'),
    ('waterway', 'derelict_canal'): ('Canal abandonné', 'Canal en friche.'),
    ('waterway', 'confluence'): ('Confluence', 'Jonction cours d\'eau.'),
    ('waterway', 'sewer'): ('Égout', 'Collecteur eaux usées.'),
    ('waterway', 'fish_pass'): ('Passe à poissons', 'Échelle poissons, migration.'),
    ('waterway', 'ford'): ('Gué', 'Passage à gué. Traversée.'),
    ('waterway', 'swale'): ('Noue', 'Fossé végétalisé.'),
    ('waterway', 'pumping_station'): ('Station pompage', 'Pompes, relevage.'),
    ('waterway', 'drawbridge'): ('Pont-levis', 'Pont mobile, basculant.'),
    ('waterway', 'wadi'): ('Oued', 'Cours d\'eau intermittent. Désert.'),
    ('waterway', 'riverbank'): ('Berge', 'Rive, bord rivière.'),
    ('waterway', 'tidal_channel'): ('Chenal marée', 'Estran, passage tidal.'),
    ('waterway', 'sign'): ('Panneau', 'Signalisation fluviale.'),

    # =====================
    # AEROWAY
    # =====================
    ('aeroway', 'beacon'): ('Balise aéro', 'Balise navigation aérienne. VOR, NDB.'),
    ('aeroway', 'aerodrome_marking'): ('Marquage aérodrome', 'Peinture piste, taxiway.'),
    ('aeroway', 'aircraft_crossing'): ('Croisement avions', 'Passage avions, traversée.'),
    ('aeroway', 'taxilane'): ('Voie de circulation', 'Taxilane, accès hangars.'),
    ('aeroway', 'launchpad'): ('Aire décollage', 'Plateforme lancement. Hélicoptère.'),
    ('aeroway', 'marking'): ('Marquage', 'Signalétique sol aéroport.'),
    ('aeroway', 'staging_area'): ('Zone attente', 'Aire stationnement avions.'),
    ('aeroway', 'model_taxiway'): ('Taxiway modélisme', 'Piste aéromodélisme.'),
    ('aeroway', 'helipad'): ('Héliport', 'Aire hélicoptère. Atterrissage, décollage.'),
    ('aeroway', 'spaceport'): ('Spatioport', 'Base lancement spatial. Fusées.'),
    ('aeroway', 'stopway'): ('Prolongement arrêt', 'Zone décélération, sécurité piste.'),
    ('aeroway', 'model_runway'): ('Piste modélisme', 'Piste aéromodèles réduits.'),
    ('aeroway', 'construction'): ('Construction', 'Infrastructure aéroportuaire en travaux.'),
    ('aeroway', 'arresting_gear'): ('Système freinage', 'Câble arrêt avion. Militaire.'),
    ('aeroway', 'landing_light'): ('Balisage lumineux', 'Feux approche, piste.'),
    ('aeroway', 'highway_strip'): ('Piste routière', 'Section route = piste urgence.'),
    ('aeroway', 'control_center'): ('Centre contrôle', 'Tour de contrôle, ACC. ATC.'),
    ('aeroway', 'obstacle'): ('Obstacle', 'Danger aérien. Antenne, cheminée.'),
    ('aeroway', 'threshold'): ('Seuil piste', 'Début piste atterrissage.'),
    ('aeroway', 'shelter'): ('Abri', 'Hangar, protection avions.'),

    # =====================
    # BARRIER
    # =====================
    ('barrier', 'handrail'): ('Main courante', 'Rampe, garde-corps. Sécurité.'),
    ('barrier', 'water_gate'): ('Vanne', 'Porte eau, barrage mobile.'),
    ('barrier', 'door'): ('Porte', 'Porte, entrée. Accès.'),
    ('barrier', 'lock_gate'): ('Porte écluse', 'Vantail écluse navigation.'),
    ('barrier', 'motorcycle_barrier'): ('Barrière motos', 'Chicane anti-deux-roues.'),
    ('barrier', 'edging'): ('Bordure', 'Délimitation, rebord.'),
    ('barrier', 'wire_fence'): ('Clôture fil', 'Grillage, fil de fer.'),
    ('barrier', 'wicked_gate'): ('Portillon', 'Petit portail, entrée piéton.'),
    ('barrier', 'lych_gate'): ('Porche église', 'Portique cimetière. Couvert.'),
    ('barrier', 'rock'): ('Rocher', 'Bloc rocheux, obstacle.'),
    ('barrier', 'bus_trap'): ('Piège à bus', 'Écluse bus. Filtrage.'),
    ('barrier', 'central_reservation'): ('Terre-plein', 'Séparateur central, route.'),
    ('barrier', 'shelf'): ('Rebord', 'Saillie, corniche.'),
    ('barrier', 'field_boundary'): ('Limite champ', 'Bordure parcelle agricole.'),
    ('barrier', 'avalanche_protection'): ('Pare-avalanche', 'Protection avalanche. Montagne.'),
    ('barrier', 'tyres'): ('Pneus', 'Barrière pneus. Protection.'),
    ('barrier', 'sliding_beam'): ('Poutre coulissante', 'Barrière mobile, poutre.'),
    ('barrier', 'tank_trap'): ('Obstacle antichar', 'Dents de dragon. Défense.'),
    ('barrier', 'toll_booth'): ('Cabine péage', 'Guichet autoroute.'),
    ('barrier', 'stone'): ('Pierre', 'Bloc pierre, borne.'),
    ('barrier', 'coupure'): ('Coupure', 'Ouverture digue. Passage.'),
    ('barrier', 'step'): ('Marche', 'Marche, gradin. Dénivelé.'),
    ('barrier', 'horse_stile'): ('Passage chevaux', 'Barrière équestre.'),
    ('barrier', 'ditch'): ('Fossé', 'Fossé, tranchée. Obstacle.'),
    ('barrier', 'pole'): ('Poteau', 'Poteau barrière. Obstacle.'),
    ('barrier', 'border_control'): ('Contrôle frontière', 'Poste douane, passage.'),
    ('barrier', 'checkpoint'): ('Point contrôle', 'Barrage, vérification.'),
    ('barrier', 'separate'): ('Séparation', 'Élément séparateur.'),
    ('barrier', 'delineator_kerb'): ('Bordure délinéateur', 'Séparateur de voie.'),
    ('barrier', 'earthworks'): ('Terrassement', 'Remblai, talus.'),
    ('barrier', 'line'): ('Ligne', 'Marquage au sol. Limite.'),
    ('barrier', 'median'): ('Médiane', 'Séparateur central.'),
    ('barrier', 'log'): ('Rondin', 'Tronc, barrière bois.'),
    ('barrier', 'barrier'): ('Barrière', 'Obstacle, clôture.'),
    ('barrier', 'property_boundary'): ('Limite propriété', 'Bornage, délimitation.'),
    ('barrier', 'berm'): ('Berme', 'Accotement, talus.'),
    ('barrier', 'sump_buster'): ('Ralentisseur', 'Ressaut, dos d\'âne.'),
    ('barrier', 'floating_boom'): ('Barrage flottant', 'Estacade, flotteurs.'),
    ('barrier', 'sliding_gate'): ('Portail coulissant', 'Porte motorisée.'),
    ('barrier', 'wedge'): ('Coin', 'Cale, bloc.'),
    ('barrier', 'debris'): ('Débris', 'Obstacle, encombrement.'),
    ('barrier', 'height_restrictor'): ('Limiteur hauteur', 'Portique, gabarit.'),
    ('barrier', 'parking_bumper'): ('Butée parking', 'Arrêtoir véhicule.'),
    ('barrier', 'embankment'): ('Remblai', 'Talus, digue.'),
    ('barrier', 'obstacle'): ('Obstacle', 'Entrave, blocage.'),
    ('barrier', 'hampshire_gate'): ('Barrière Hampshire', 'Grille amovible. Ferme.'),
    ('barrier', 'steps'): ('Escalier', 'Marches, dénivelé.'),
    ('barrier', 'dry_bush'): ('Buisson sec', 'Végétation obstacle.'),
    ('barrier', 'wood_fence'): ('Palissade bois', 'Clôture planches.'),
    ('barrier', 'attenuator'): ('Atténuateur choc', 'Absorbeur impact. Sécurité.'),
    ('barrier', 'mound'): ('Butte', 'Monticule, talus.'),
    ('barrier', 'proposed'): ('Projet', 'Barrière prévue.'),
    ('barrier', 'footgate'): ('Portillon piéton', 'Passage piétons.'),
    ('barrier', 'rocks'): ('Rochers', 'Blocs rocheux.'),
    ('barrier', 'windfall'): ('Chablis', 'Arbre tombé. Obstacle.'),
    ('barrier', 'barricade'): ('Barricade', 'Blocage, obstacle.'),
    ('barrier', 'avalanche_barrier'): ('Barrière avalanche', 'Protection montagne.'),
    ('barrier', 'unknown'): ('Inconnu', 'Barrière non identifiée.'),
    ('barrier', 'median_strip'): ('Bande médiane', 'Séparateur voies.'),
    ('barrier', 'underground_wall'): ('Mur souterrain', 'Paroi enterrée.'),
    ('barrier', 'slide_gate'): ('Vanne', 'Porte coulissante.'),
    ('barrier', 'chicane'): ('Chicane', 'Ralentisseur en S.'),
    ('barrier', 'cliff'): ('Falaise', 'Escarpement rocheux.'),
    ('barrier', 'snow_fence'): ('Pare-neige', 'Barrière contre congères.'),
    ('barrier', 'delineators'): ('Délinéateurs', 'Balises voie.'),
    ('barrier', 'metal_bow'): ('Arceau métal', 'Barrière arche.'),
    ('barrier', 'barrier_board'): ('Panneau barrière', 'Planche obstacle.'),
    ('barrier', 'armadillo'): ('Armadillo', 'Bordure séparatrice.'),
    ('barrier', 'flowerpot'): ('Bac fleurs', 'Jardinière obstacle.'),
    ('barrier', 'wood'): ('Bois', 'Barrière bois.'),
    ('barrier', 'trench'): ('Tranchée', 'Fossé défensif.'),
    ('barrier', 'railing'): ('Rambarde', 'Garde-corps, rampe.'),
    ('barrier', 'traffic_island'): ('Îlot trafic', 'Refuge directionnel.'),
    ('barrier', 'spikes'): ('Pointes', 'Herse, anti-retour.'),
    ('barrier', 'construction'): ('Construction', 'Barrière chantier.'),
    ('barrier', 'horse_jump'): ('Obstacle équestre', 'Saut cheval.'),
    ('barrier', 'tree'): ('Arbre', 'Arbre obstacle.'),
    ('barrier', 'steeplechase_jump'): ('Obstacle steeple', 'Haie course hippique.'),
    ('barrier', 'furrow'): ('Sillon', 'Rigole, fossé.'),
    ('barrier', 'net'): ('Filet', 'Filet protection.'),
    ('barrier', 'overgrown'): ('Envahi végétation', 'Obstacle naturel.'),
    ('barrier', 'collision_protection'): ('Protection collision', 'Absorbeur choc.'),
    ('barrier', 'fallen_tree'): ('Arbre tombé', 'Chablis, obstacle.'),
    ('barrier', 'swing_gate'): ('Portail battant', 'Porte pivotante.'),
    ('barrier', 'earth_bank'): ('Talus terre', 'Remblai, levée.'),
    ('barrier', 'planter'): ('Jardinière', 'Bac plantes.'),
    ('barrier', 'kissing_gate'): ('Tourniquet', 'Portillon en V. Randonnée.'),

    # =====================
    # PUBLIC_TRANSPORT
    # =====================
    ('public_transport', 'info_board'): ('Panneau info', 'Affichage horaires transport.'),
    ('public_transport', 'train_station'): ('Gare', 'Gare ferroviaire. Trains.'),
    ('public_transport', 'bus'): ('Bus', 'Autobus, transport en commun.'),
    ('public_transport', 'stop_area_group'): ('Groupe arrêts', 'Pôle d\'échange.'),
    ('public_transport', 'entrance_pass'): ('Passage accès', 'Entrée station.'),
    ('public_transport', 'platform_section_sign'): ('Repère quai', 'Marquage position voiture.'),
    ('public_transport', '2'): ('Niveau 2', 'Deuxième niveau.'),
    ('public_transport', 'halt'): ('Halte', 'Petit arrêt ferroviaire.'),
    ('public_transport', 'waiting_room'): ('Salle attente', 'Abri voyageurs.'),
    ('public_transport', 'platform_access'): ('Accès quai', 'Entrée plateforme.'),
    ('public_transport', 'platform_edge'): ('Bord quai', 'Limite plateforme.'),
    ('public_transport', 'stop'): ('Arrêt', 'Point d\'arrêt bus, tram.'),
    ('public_transport', 'destination_display'): ('Afficheur destination', 'Girouette, écran.'),
    ('public_transport', 'service_center'): ('Centre services', 'Agence transport.'),
    ('public_transport', 'departures_board'): ('Tableau départs', 'Écran horaires.'),
    ('public_transport', 'entrance'): ('Entrée', 'Accès station, gare.'),
    ('public_transport', 'pole'): ('Poteau', 'Poteau arrêt bus.'),

    # =====================
    # PLACE
    # =====================
    ('place', 'community'): ('Communauté', 'Hameau, communauté. Petit groupe.'),
    ('place', 'island'): ('Île', 'Île, terre entourée eau.'),
    ('place', 'civil_parish'): ('Paroisse civile', 'Division administrative. Commune.'),
    ('place', 'location'): ('Lieu', 'Emplacement nommé.'),
    ('place', 'polder'): ('Polder', 'Terre gagnée sur mer. Pays-Bas.'),
    ('place', 'field'): ('Champ', 'Parcelle agricole.'),
    ('place', 'subdistrict'): ('Sous-district', 'Division administrative.'),
    ('place', 'unknown'): ('Inconnu', 'Lieu non identifié.'),
    ('place', 'municipality'): ('Municipalité', 'Commune, ville.'),
    ('place', 'subward'): ('Sous-quartier', 'Division quartier.'),
    ('place', 'subdivision'): ('Subdivision', 'Division administrative.'),
    ('place', 'ward'): ('Quartier', 'Secteur ville.'),
    ('place', 'department'): ('Département', 'Division régionale.'),
    ('place', 'city_block'): ('Pâté de maisons', 'Îlot urbain.'),
    ('place', 'block'): ('Bloc', 'Ensemble bâtiments.'),
    ('place', 'borough'): ('Arrondissement', 'Division urbaine.'),
    ('place', 'city'): ('Ville', 'Grande agglomération.'),
    ('place', 'archipelago'): ('Archipel', 'Groupe d\'îles.'),
    ('place', 'camp'): ('Camp', 'Campement, installation.'),
    ('place', 'province'): ('Province', 'Région administrative.'),
    ('place', 'Commune'): ('Commune', 'Municipalité, mairie.'),
    ('place', 'district'): ('District', 'Secteur administratif.'),

    # =====================
    # BOUNDARY
    # =====================
    ('boundary', 'barony'): ('Baronnie', 'Ancienne division féodale.'),
    ('boundary', 'local_authority'): ('Autorité locale', 'Collectivité territoriale.'),
    ('boundary', 'traditional'): ('Traditionnel', 'Limite coutumière.'),
    ('boundary', 'annexation'): ('Annexion', 'Extension territoriale.'),
    ('boundary', 'civil_parish'): ('Paroisse civile', 'Division religieuse.'),
    ('boundary', 'vice_county'): ('Vice-comté', 'Division naturaliste UK.'),
    ('boundary', 'forestry'): ('Forêt', 'Limite zone forestière.'),
    ('boundary', 'judicial'): ('Judiciaire', 'Ressort tribunal.'),
    ('boundary', 'civil'): ('Civil', 'Division civile.'),
    ('boundary', 'neighborhood'): ('Quartier', 'Limite voisinage.'),
    ('boundary', 'polling_station'): ('Bureau vote', 'Secteur électoral.'),
    ('boundary', 'environment'): ('Environnement', 'Zone protection nature.'),
    ('boundary', 'health'): ('Santé', 'Secteur sanitaire.'),
    ('boundary', 'public_transport'): ('Transport', 'Zone tarifaire.'),
    ('boundary', 'political_fraction'): ('Fraction politique', 'Division politique.'),
    ('boundary', 'natural'): ('Naturelle', 'Limite naturelle.'),
    ('boundary', 'military'): ('Militaire', 'Zone défense.'),
    ('boundary', 'marker'): ('Borne', 'Borne frontière.'),
    ('boundary', 'aboriginal_lands'): ('Terres autochtones', 'Territoire indigène.'),
    ('boundary', 'parcel'): ('Parcelle', 'Limite cadastrale.'),
    ('boundary', 'region'): ('Région', 'Limite régionale.'),
    ('boundary', 'disputed'): ('Contesté', 'Frontière litigieuse.'),
    ('boundary', 'limited_traffic_zone'): ('ZTL', 'Zone trafic limité.'),
    ('boundary', 'point'): ('Point', 'Point frontière.'),
    ('boundary', 'country_border'): ('Frontière pays', 'Limite nationale.'),
    ('boundary', 'state_border'): ('Frontière État', 'Limite fédérale.'),
    ('boundary', 'fence'): ('Clôture', 'Limite physique.'),
    ('boundary', 'town'): ('Ville', 'Limite communale.'),
    ('boundary', 'low_emission_zone'): ('ZFE', 'Zone faibles émissions.'),
    ('boundary', 'landuse'): ('Occupation sol', 'Limite zonage.'),
    ('boundary', 'legal'): ('Légal', 'Limite juridique.'),
    ('boundary', 'zone'): ('Zone', 'Périmètre défini.'),
    ('boundary', 'hazard'): ('Danger', 'Zone à risque.'),
    ('boundary', 'religious'): ('Religieux', 'Diocèse, paroisse.'),
    ('boundary', 'timezone'): ('Fuseau horaire', 'Limite horaire.'),
    ('boundary', 'fire_district'): ('Zone pompiers', 'Secteur SDIS.'),
    ('boundary', 'statistical'): ('Statistique', 'Zone INSEE, IRIS.'),
    ('boundary', 'place'): ('Lieu', 'Limite localité.'),
    ('boundary', 'border_zone'): ('Zone frontière', 'Bande frontalière.'),
    ('boundary', 'lot'): ('Lot', 'Parcelle cadastrale.'),
    ('boundary', 'perceived'): ('Perçu', 'Limite informelle.'),
    ('boundary', 'residential'): ('Résidentiel', 'Zone habitat.'),
    ('boundary', 'visible'): ('Visible', 'Limite physique.'),
    ('boundary', 'forest_planning'): ('Aménagement forêt', 'Parcelle forestière.'),
    ('boundary', 'water_distribution'): ('Distribution eau', 'Réseau AEP.'),
    ('boundary', 'plot'): ('Parcelle', 'Terrain cadastré.'),
    ('boundary', 'water_protection_area'): ('Protection eau', 'Périmètre captage.'),
    ('boundary', 'municipality'): ('Commune', 'Limite municipale.'),
    ('boundary', 'disused'): ('Désaffecté', 'Ancienne limite.'),
    ('boundary', 'special_economic_zone'): ('ZES', 'Zone économique spéciale.'),
    ('boundary', 'quarter'): ('Quartier', 'Division urbaine.'),
    ('boundary', 'neighbourhood'): ('Voisinage', 'Secteur quartier.'),
    ('boundary', 'cadastral'): ('Cadastre', 'Limite cadastrale.'),
    ('boundary', 'land_area'): ('Surface', 'Étendue terrain.'),
    ('boundary', 'claim'): ('Revendication', 'Territoire revendiqué.'),
    ('boundary', 'census'): ('Recensement', 'Zone statistique.'),
    ('boundary', 'forest_compartment'): ('Parcelle forêt', 'Division ONF.'),

    # =====================
    # MILITARY
    # =====================
    ('military', 'gun position'): ('Position artillerie', 'Emplacement canon.'),
    ('military', 'bombcrater'): ('Cratère bombe', 'Impact, explosion.'),
    ('military', 'cannon'): ('Canon', 'Pièce artillerie. Monument.'),
    ('military', 'bunker'): ('Bunker', 'Blockhaus, casemate. Défense.'),
    ('military', 'launchpad'): ('Rampe lancement', 'Base missiles.'),
    ('military', 'base'): ('Base militaire', 'Camp, garnison.'),
    ('military', 'depot'): ('Dépôt', 'Entrepôt munitions, matériel.'),
    ('military', 'abandoned'): ('Abandonné', 'Site militaire désaffecté.'),
    ('military', 'radar'): ('Radar', 'Station radar défense.'),
    ('military', 'road'): ('Route militaire', 'Voie défense.'),
    ('military', 'turret'): ('Tourelle', 'Poste tir blindé.'),
    ('military', 'barracks'): ('Caserne', 'Quartier militaire. Logements.'),
    ('military', 'casemate'): ('Casemate', 'Abri fortifié. Béton.'),
    ('military', 'embrasure'): ('Embrasure', 'Meurtrière, créneau.'),
    ('military', 'cordon'): ('Cordon', 'Périmètre sécurité.'),
    ('military', 'observation_post'): ('Poste observation', 'Guet, surveillance.'),
    ('military', 'shelter'): ('Abri', 'Refuge, protection.'),

    # =====================
    # POWER
    # =====================
    ('power', 'line_section'): ('Section ligne', 'Tronçon ligne électrique.'),
    ('power', 'anchor_block'): ('Massif ancrage', 'Fondation pylône.'),
    ('power', 'converter'): ('Convertisseur', 'Station conversion HVDC.'),
    ('power', 'street_pole'): ('Poteau rue', 'Support éclairage public.'),
    ('power', 'storage'): ('Stockage', 'Batterie, stockage énergie.'),
    ('power', 'feeder'): ('Départ', 'Ligne distribution.'),
    ('power', 'proposed'): ('Projet', 'Installation prévue.'),
    ('power', 'outlet'): ('Prise', 'Point branchement.'),
    ('power', 'bollard'): ('Borne', 'Borne électrique.'),
    ('power', 'circuit_segment'): ('Segment circuit', 'Portion réseau.'),
    ('power', 'roof_pole'): ('Poteau toit', 'Support toiture.'),
    ('power', 'circuit'): ('Circuit', 'Boucle électrique.'),
    ('power', 'capacitor_bank'): ('Batterie condensateurs', 'Compensation réactive.'),
    ('power', 'tap'): ('Dérivation', 'Prise de courant.'),
    ('power', 'razed'): ('Détruit', 'Installation démolie.'),
    ('power', 'catenary_portal'): ('Portique caténaire', 'Support ligne contact.'),
    ('power', 'cross_arm'): ('Traverse', 'Bras poteau.'),
    ('power', 'current_transformer'): ('Transformateur courant', 'TC, mesure.'),
    ('power', 'construction'): ('Construction', 'Installation en travaux.'),
    ('power', 'abandoned'): ('Abandonné', 'Plus en service.'),
    ('power', 'box'): ('Coffret', 'Armoire électrique.'),
    ('power', 'heliostat'): ('Héliostat', 'Miroir solaire orientable.'),
    ('power', 'minor_cable'): ('Câble secondaire', 'Distribution basse tension.'),
    ('power', 'transition'): ('Transition', 'Passage aérien-souterrain.'),
    ('power', 'plant'): ('Centrale', 'Centrale électrique. Production.'),
    ('power', 'cable_distribution'): ('Distribution câble', 'Réseau souterrain.'),
    ('power', 'cable_distribution_cabinet'): ('Armoire distribution', 'Coffret répartition.'),
    ('power', 'inverter'): ('Onduleur', 'Conversion DC-AC.'),
    ('power', 'branch'): ('Branchement', 'Raccordement abonné.'),

    # =====================
    # ROUTE
    # =====================
    ('route', 'trolleybus'): ('Trolleybus', 'Ligne trolley. Bus électrique.'),
    ('route', 'funicular'): ('Funiculaire', 'Ligne funiculaire. Câble.'),
    ('route', 'horse'): ('Équestre', 'Itinéraire cavalier. Chevaux.'),
    ('route', 'inline_skates'): ('Rollers', 'Parcours roller. Patins.'),
    ('route', 'canoe'): ('Canoë', 'Parcours canoë-kayak. Rivière.'),
    ('route', 'foot'): ('Piéton', 'Itinéraire pédestre. Marche.'),
    ('route', 'emergency_access'): ('Accès secours', 'Itinéraire pompiers, SAMU.'),
    ('route', 'waterway'): ('Fluvial', 'Itinéraire navigation.'),
    ('route', 'boat'): ('Bateau', 'Ligne maritime, fluviale.'),
    ('route', 'piste'): ('Piste', 'Itinéraire ski, raquettes.'),
    ('route', 'canyoning'): ('Canyoning', 'Parcours canyon. Descente.'),
    ('route', 'proposed'): ('Projet', 'Itinéraire prévu.'),
    ('route', 'monorail'): ('Monorail', 'Ligne monorail.'),
    ('route', 'railway'): ('Ferroviaire', 'Ligne train.'),
    ('route', 'share_taxi'): ('Taxi collectif', 'Ligne taxi partagé.'),
    ('route', 'tracks'): ('Voies', 'Réseau ferré.'),
    ('route', 'detour'): ('Déviation', 'Itinéraire contournement.'),
    ('route', 'pipeline'): ('Pipeline', 'Canalisation, oléoduc.'),
    ('route', 'motorboat'): ('Bateau moteur', 'Itinéraire nautique.'),
    ('route', 'evacuation'): ('Évacuation', 'Itinéraire secours.'),
    ('route', 'wheelchair'): ('Fauteuil roulant', 'Parcours PMR accessible.'),
    ('route', 'portage'): ('Portage', 'Contournement canoë.'),
    ('route', 'light_rail'): ('Métro léger', 'Ligne tramway, LRT.'),
    ('route', 'nordic_walking'): ('Marche nordique', 'Parcours bâtons.'),
    ('route', 'aerialway'): ('Téléphérique', 'Ligne câble aérien.'),
    ('route', 'construction'): ('Construction', 'Ligne en travaux.'),
    ('route', 'walking'): ('Marche', 'Parcours pédestre.'),
    ('route', 'snowmobile'): ('Motoneige', 'Piste motoneige.'),
    ('route', 'via_ferrata'): ('Via ferrata', 'Parcours équipé montagne.'),
    ('route', 'junction'): ('Jonction', 'Point intersection.'),
    ('route', 'historic_railway'): ('Chemin fer historique', 'Ancienne ligne.'),
    ('route', 'power'): ('Électrique', 'Ligne électrique.'),
    ('route', 'historic'): ('Historique', 'Itinéraire patrimoine.'),
    ('route', 'transhumance'): ('Transhumance', 'Draille, chemin troupeaux.'),
    ('route', 'worship'): ('Pèlerinage', 'Chemin religieux.'),

    # =====================
    # AERIALWAY
    # =====================
    ('aerialway', 'goods'): ('Marchandises', 'Téléphérique fret. Transport.'),

    # =====================
    # GEOLOGICAL
    # =====================
    ('geological', 'meteor_crater'): ('Cratère météorite', 'Impact extraterrestre.'),
    ('geological', 'volcanic_lava_flow'): ('Coulée lave', 'Volcan, éruption.'),
    ('geological', 'volcanic_lava_field'): ('Champ lave', 'Zone volcanique.'),
    ('geological', 'fault'): ('Faille', 'Faille tectonique. Séisme.'),
    ('geological', 'volcanic_vent'): ('Évent volcanique', 'Cheminée, cratère.'),
    ('geological', 'volcanic_caldera_rim'): ('Caldeira', 'Bord cratère effondré.'),
    ('geological', 'volcanic_lava_tube'): ('Tunnel lave', 'Grotte volcanique.'),
    ('geological', 'moraine'): ('Moraine', 'Dépôt glaciaire.'),
    ('geological', 'geotope'): ('Géotope', 'Site géologique remarquable.'),
    ('geological', 'glacial_erratic'): ('Bloc erratique', 'Rocher glaciaire.'),
    ('geological', 'nunatak'): ('Nunatak', 'Pic rocheux glacier.'),
    ('geological', 'outcrop'): ('Affleurement', 'Roche apparente.'),
    ('geological', 'landslide'): ('Glissement terrain', 'Éboulement.'),
    ('geological', 'giants_kettle'): ('Marmite géant', 'Érosion glaciaire.'),
    ('geological', 'rock_glacier'): ('Glacier rocheux', 'Formation périglaciaire.'),
    ('geological', 'palaeontological_site'): ('Site paléontologique', 'Fossiles.'),
    ('geological', 'limestone_pavement'): ('Lapiaz', 'Karst calcaire.'),

    # =====================
    # TELECOM
    # =====================
    ('telecom', 'exchange'): ('Central télécom', 'NRA, autocommutateur.'),
    ('telecom', 'line'): ('Ligne', 'Câble télécom.'),
    ('telecom', 'cable'): ('Câble', 'Fibre, cuivre.'),
    ('telecom', 'service_device'): ('Équipement', 'Boîtier, amplificateur.'),
    ('telecom', 'connection_point'): ('Point raccordement', 'PBO, branchement.'),
    ('telecom', 'antenna'): ('Antenne', 'Antenne relais, 4G, 5G.'),
    ('telecom', 'distribution_point'): ('Point distribution', 'PM, répartiteur.'),
    ('telecom', 'data_center'): ('Datacenter', 'Centre données. Serveurs.'),
    ('telecom', 'terminal'): ('Terminal', 'Équipement utilisateur.'),
    ('telecom', 'pole'): ('Poteau', 'Support câbles télécom.'),

    # =====================
    # ACCESS
    # =====================
    ('access', 'community'): ('Communauté', 'Réservé communauté locale.'),
    ('access', 'employees'): ('Employés', 'Réservé personnel.'),
    ('access', 'foot'): ('Piétons', 'Accès piéton uniquement.'),
    ('access', 'limited'): ('Limité', 'Accès restreint.'),
    ('access', 'fixme'): ('À vérifier', 'Accès à confirmer.'),
    ('access', 'restricted'): ('Restreint', 'Accès contrôlé.'),
    ('access', 'boat'): ('Bateau', 'Accès nautique.'),
    ('access', 'psv'): ('Transport public', 'Bus, taxi autorisés.'),
    ('access', 'residents'): ('Résidents', 'Riverains uniquement.'),
    ('access', 'members'): ('Membres', 'Adhérents seulement.'),
    ('access', 'home'): ('Domicile', 'Accès résidence.'),
    ('access', 'hgv'): ('Poids lourds', 'Camions autorisés.'),
    ('access', 'conditional'): ('Conditionnel', 'Selon conditions.'),
    ('access', 'service'): ('Service', 'Livraison autorisée.'),
    ('access', 'guests'): ('Invités', 'Clients, visiteurs.'),
    ('access', 'emergency'): ('Urgence', 'Secours uniquement.'),
    ('access', 'staff'): ('Personnel', 'Employés uniquement.'),
    ('access', 'military'): ('Militaire', 'Zone défense.'),
    ('access', 'disabled'): ('Handicapé', 'PMR, accessibilité.'),
    ('access', 'public'): ('Public', 'Ouvert à tous.'),
    ('access', 'charging'): ('Recharge', 'Véhicules électriques.'),
    ('access', 'seasonal'): ('Saisonnier', 'Selon saison.'),
    ('access', 'permit'): ('Autorisation', 'Permis requis.'),
    ('access', 'visitors'): ('Visiteurs', 'Touristes, passants.'),
    ('access', 'hov'): ('Covoiturage', 'Véhicules occupés.'),
    ('access', 'bus'): ('Bus', 'Autobus autorisés.'),
    ('access', 'passengers'): ('Passagers', 'Voyageurs.'),
    ('access', 'official'): ('Officiel', 'Service officiel.'),
    ('access', 'fee'): ('Payant', 'Accès tarifé.'),
    ('access', 'key'): ('Clé', 'Avec clé, code.'),
    ('access', 'license'): ('Licence', 'Permis nécessaire.'),
    ('access', 'students'): ('Étudiants', 'Scolaires, universitaires.'),

    # =====================
    # MOTOR_VEHICLE
    # =====================
    ('motor_vehicle', 'seasonal'): ('Saisonnier', 'Selon saison.'),
    ('motor_vehicle', 'designated'): ('Désigné', 'Voie véhicules.'),
    ('motor_vehicle', 'permit'): ('Autorisation', 'Permis requis.'),
    ('motor_vehicle', 'psv'): ('Transport public', 'Bus autorisés.'),
    ('motor_vehicle', 'residents'): ('Résidents', 'Riverains.'),
    ('motor_vehicle', 'atv'): ('Quad', 'Tout-terrain motorisé.'),
    ('motor_vehicle', 'unknown'): ('Inconnu', 'Non renseigné.'),
    ('motor_vehicle', 'service'): ('Service', 'Livraison.'),
    ('motor_vehicle', 'emergency'): ('Urgence', 'Secours.'),
    ('motor_vehicle', 'bus'): ('Bus', 'Autobus.'),
    ('motor_vehicle', 'official'): ('Officiel', 'Véhicules service.'),
    ('motor_vehicle', 'discouraged'): ('Déconseillé', 'Éviter.'),
    ('motor_vehicle', 'military'): ('Militaire', 'Défense.'),
    ('motor_vehicle', 'customers'): ('Clients', 'Clientèle.'),
    ('motor_vehicle', 'permissive'): ('Toléré', 'Autorisé tacite.'),
    ('motor_vehicle', 'motorcycle'): ('Moto', 'Deux-roues.'),

    # =====================
    # BICYCLE
    # =====================
    ('bicycle', 'mtb'): ('VTT', 'Vélo tout terrain.'),
    ('bicycle', 'lane'): ('Piste', 'Bande cyclable.'),
    ('bicycle', 'official'): ('Officiel', 'Itinéraire balisé.'),
    ('bicycle', 'discouraged'): ('Déconseillé', 'Dangereux vélo.'),
    ('bicycle', 'limited'): ('Limité', 'Accès restreint.'),
    ('bicycle', 'delivery'): ('Livraison', 'Vélo cargo.'),
    ('bicycle', 'permit'): ('Autorisation', 'Permis requis.'),
    ('bicycle', 'destination'): ('Destination', 'Riverains vélo.'),
    ('bicycle', 'optional_sidepath'): ('Piste facultative', 'Voie parallèle optionnelle.'),
    ('bicycle', 'undefined'): ('Indéfini', 'Non précisé.'),
    ('bicycle', 'unknown'): ('Inconnu', 'Non renseigné.'),

    # =====================
    # FOOT
    # =====================
    ('foot', 'separate'): ('Séparé', 'Trottoir distinct.'),
    ('foot', 'official'): ('Officiel', 'Chemin balisé.'),
    ('foot', 'discouraged'): ('Déconseillé', 'Éviter piéton.'),
    ('foot', 'military'): ('Militaire', 'Zone défense.'),
    ('foot', 'delivery'): ('Livraison', 'Service.'),
    ('foot', 'permit'): ('Autorisation', 'Permis requis.'),
    ('foot', 'destination'): ('Destination', 'Riverains.'),
    ('foot', 'forestry'): ('Forestier', 'Exploitation forêt.'),
    ('foot', 'impassable'): ('Infranchissable', 'Impossible.'),
    ('foot', 'unknown'): ('Inconnu', 'Non renseigné.'),
    ('foot', 'passable'): ('Praticable', 'Passage possible.'),

    # =====================
    # HORSE
    # =====================
    ('horse', 'unknown'): ('Inconnu', 'Non renseigné.'),
    ('horse', 'permit'): ('Autorisation', 'Permis équestre.'),
    ('horse', 'permissive'): ('Toléré', 'Chevaux tolérés.'),
    ('horse', 'private'): ('Privé', 'Propriété privée.'),
    ('horse', 'official'): ('Officiel', 'Chemin cavalier balisé.'),
    ('horse', 'discouraged'): ('Déconseillé', 'Éviter chevaux.'),
    ('horse', 'use_sidepath'): ('Utiliser piste', 'Chemin parallèle.'),
    ('horse', 'delivery'): ('Livraison', 'Service.'),
    ('horse', 'dismount'): ('Pied à terre', 'Descendre cheval.'),
    ('horse', 'destination'): ('Destination', 'Riverains.'),
    ('horse', 'agricultural'): ('Agricole', 'Exploitation.'),
    ('horse', 'customers'): ('Clients', 'Centre équestre.'),
    ('horse', 'forestry'): ('Forestier', 'Forêt.'),

    # =====================
    # SERVICE (road/rail)
    # =====================
    ('service', 'body'): ('Carrosserie', 'Réparation carrosserie.'),
    ('service', 'access'): ('Accès', 'Voie d\'accès.'),
    ('service', 'aircraft_control'): ('Contrôle aérien', 'Tour, radar.'),
    ('service', 'crossover'): ('Raccordement', 'Liaison voies.'),
    ('service', 'delivery'): ('Livraison', 'Accès livraisons.'),
    ('service', 'express'): ('Express', 'Service rapide.'),
    ('service', 'wheel_repair'): ('Réparation roues', 'Jantes, pneumatiques.'),
    ('service', 'slipway'): ('Cale', 'Mise à l\'eau.'),
    ('service', 'forestry'): ('Forestier', 'Exploitation forêt.'),
    ('service', 'tyres'): ('Pneus', 'Pneumatiques.'),
    ('service', 'haul_road'): ('Piste chantier', 'Route carrière.'),
    ('service', 'commuter'): ('Banlieue', 'Desserte locale.'),
    ('service', 'driving_exercise'): ('Circuit auto-école', 'Apprentissage.'),
    ('service', 'service'): ('Service', 'Voie technique.'),
    ('service', 'unpaved'): ('Non revêtu', 'Piste terre.'),
    ('service', 'long_distance'): ('Grandes lignes', 'Train longue distance.'),
    ('service', 'shared_driveway'): ('Allée partagée', 'Accès commun.'),
    ('service', 'logging'): ('Débardage', 'Exploitation bois.'),
    ('service', 'repair'): ('Réparation', 'Entretien, mécanique.'),
    ('service', 'quarry'): ('Carrière', 'Exploitation minière.'),
    ('service', 'layby'): ('Aire repos', 'Stationnement.'),
    ('service', 'dealer'): ('Concessionnaire', 'Vente véhicules.'),
    ('service', 'national'): ('National', 'Grandes lignes.'),
    ('service', 'depot'): ('Dépôt', 'Garage bus, trains.'),
    ('service', 'military'): ('Militaire', 'Défense.'),
    ('service', 'oil'): ('Huile', 'Vidange, lubrifiants.'),
    ('service', 'drinking'): ('Eau potable', 'Alimentation.'),
    ('service', 'high_speed'): ('Grande vitesse', 'TGV.'),
    ('service', 'irrigation'): ('Irrigation', 'Arrosage.'),
    ('service', 'ventilation'): ('Ventilation', 'Aération.'),
    ('service', 'living_street'): ('Zone rencontre', 'Zone 20.'),
    ('service', 'agriculture'): ('Agriculture', 'Exploitation.'),
    ('service', 'private'): ('Privé', 'Accès restreint.'),
    ('service', 'local'): ('Local', 'Desserte proximité.'),
    ('service', 'tourism'): ('Tourisme', 'Touristique.'),
    ('service', 'parking_access'): ('Accès parking', 'Entrée stationnement.'),
    ('service', 'agricultural'): ('Agricole', 'Ferme.'),
    ('service', 'parts'): ('Pièces', 'Pièces détachées.'),
    ('service', 'utility'): ('Réseaux', 'Concessionnaires.'),
    ('service', 'residential'): ('Résidentiel', 'Desserte habitat.'),
    ('service', 'rest_area'): ('Aire repos', 'Pause autoroute.'),
    ('service', 'peak'): ('Heure pointe', 'Renfort.'),
    ('service', 'industrial'): ('Industriel', 'Zone activité.'),
    ('service', 'maintenance'): ('Maintenance', 'Entretien.'),
    ('service', 'link'): ('Liaison', 'Raccordement.'),
    ('service', 'bus'): ('Bus', 'Voie bus.'),
    ('service', 'full'): ('Complet', 'Service intégral.'),
    ('service', 'city'): ('Urbain', 'Desserte ville.'),
    ('service', 'training'): ('Formation', 'Apprentissage.'),
    ('service', 'urban'): ('Urbain', 'Zone ville.'),
    ('service', 'glass'): ('Vitres', 'Pare-brise.'),
    ('service', 'busway'): ('Voie bus', 'Site propre.'),
    ('service', 'power'): ('Électricité', 'Réseau.'),
    ('service', 'allotments'): ('Jardins', 'Jardins familiaux.'),
    ('service', 'test_track'): ('Piste essai', 'Circuit test.'),
    ('service', 'electrical'): ('Électrique', 'Installation.'),
    ('service', 'live'): ('Direct', 'En service.'),

    # =====================
    # VENDING
    # =====================
    ('vending', 'bottle_return'): ('Consigne bouteilles', 'Retour bouteilles. Recyclage.'),
    ('vending', 'telephone_vouchers'): ('Cartes téléphone', 'Recharges mobiles.'),
    ('vending', 'gas'): ('Gaz', 'Bouteilles gaz. Propane.'),
    ('vending', 'subscription'): ('Abonnements', 'Cartes, pass.'),
    ('vending', 'rice_polishing'): ('Polissage riz', 'Moulin riz.'),
    ('vending', 'flowers'): ('Fleurs', 'Bouquets, fleuriste automatique.'),
    ('vending', 'tickets'): ('Tickets', 'Billets, transport, spectacle.'),
    ('vending', 'contact_lenses'): ('Lentilles', 'Optique, lentilles contact.'),
    ('vending', 'candles'): ('Bougies', 'Cierges, église.'),
    ('vending', 'chewing_gums'): ('Chewing-gum', 'Bonbons, gommes.'),
    ('vending', 'toll'): ('Péage', 'Télépéage, badge.'),
    ('vending', 'locker'): ('Consigne', 'Casiers automatiques.'),
    ('vending', 'movies'): ('Films', 'Location DVD, Blu-ray.'),
    ('vending', 'parcel_pickup'): ('Colis', 'Retrait colis. Point relais.'),
    ('vending', 'water'): ('Eau', 'Eau potable, fontaine.'),
    ('vending', 'elongated_coin'): ('Pièce souvenir', 'Pièce écrasée, souvenir.'),
    ('vending', 'admission_tickets'): ('Entrées', 'Billets musée, attraction.'),
    ('vending', 'ticket_validator'): ('Valideur', 'Composteur, validation.'),
    ('vending', 'animal_feed'): ('Nourriture animaux', 'Graines, croquettes.'),
    ('vending', 'snacks'): ('Snacks', 'Encas, friandises.'),
    ('vending', 'meat'): ('Viande', 'Distributeur viande.'),
    ('vending', 'toys'): ('Jouets', 'Capsules, figurines.'),
    ('vending', 'potatoes'): ('Pommes de terre', 'Patates, légumes.'),
    ('vending', 'art'): ('Art', 'Œuvres, reproductions.'),
    ('vending', 'chemist'): ('Pharmacie', 'Parapharmacie, soins.'),
    ('vending', 'honey'): ('Miel', 'Apiculteur, local.'),

    # =====================
    # ATM
    # =====================
    ('atm', 'separate'): ('DAB séparé', 'Distributeur isolé. Pas dans banque.'),

    # =====================
    # MONEY_TRANSFER
    # =====================
    ('money_transfer', 'unitylink'): ('UnityLink', 'Transfert argent UnityLink.'),
    ('money_transfer', 'palawan_express'): ('Palawan Express', 'Transfert Philippines.'),
    ('money_transfer', 'ria'): ('Ria', 'Envoi argent Ria.'),
    ('money_transfer', 'transfast'): ('Transfast', 'Transfert Transfast.'),
    ('money_transfer', 'palawan_pay'): ('Palawan Pay', 'Paiement Palawan.'),
    ('money_transfer', 'ml_kwarta_padala'): ('ML Kwarta Padala', 'Envoi ML.'),
    ('money_transfer', 'western_union'): ('Western Union', 'Transfert Western Union.'),
    ('money_transfer', 'rd_cash_padala'): ('RD Cash Padala', 'Envoi RD.'),
    ('money_transfer', 'altapay'): ('Altapay', 'Paiement Altapay.'),
    ('money_transfer', 'cash_padala'): ('Cash Padala', 'Envoi cash.'),
    ('money_transfer', 'zeepay'): ('Zeepay', 'Mobile money Zeepay.'),
    ('money_transfer', 'moneygram'): ('MoneyGram', 'Transfert MoneyGram.'),
    ('money_transfer', 'instant_cash_padala'): ('Instant Cash', 'Envoi instantané.'),
    ('money_transfer', 'cebuana_pera_padala'): ('Cebuana', 'Envoi Cebuana.'),

    # =====================
    # ATTRACTION
    # =====================
    ('attraction', 'winery'): ('Cave viticole', 'Domaine vinicole. Dégustation vin.'),
    ('attraction', 'tourism'): ('Tourisme', 'Attraction touristique.'),
    ('attraction', 'lazy_river'): ('Rivière paresseuse', 'Piscine courant. Détente.'),
    ('attraction', 'pendulum_ride'): ('Bateau pirate', 'Manège balançoire.'),
    ('attraction', 'boat_ride'): ('Promenade bateau', 'Balade nautique. Croisière.'),
    ('attraction', 'bungee_jumping'): ('Saut élastique', 'Bungee, sensation forte.'),
    ('attraction', 'formal_garden'): ('Jardin à la française', 'Parc ordonné. Château.'),
    ('attraction', 'kiddie_ride'): ('Manège enfants', 'Petit manège. Tout-petits.'),
    ('attraction', 'miniature_replica'): ('Maquette', 'Reproduction miniature. Monument.'),
    ('attraction', 'dark_ride'): ('Dark ride', 'Parcours scénique. Train fantôme.'),
    ('attraction', 'alpine_coaster'): ('Luge été', 'Bobsleigh montagne. Descente.'),
    ('attraction', 'slide'): ('Toboggan', 'Glissade. Aquatique, sec.'),
    ('attraction', 'theme_area'): ('Zone thématique', 'Univers parc. Décor.'),
    ('attraction', 'historic'): ('Historique', 'Site patrimoine. Visite.'),
    ('attraction', 'jet'): ('Jet', 'Fontaine jet d\'eau.'),

    # =====================
    # INFORMATION
    # =====================
    ('information', 'nature'): ('Nature', 'Info environnement, faune.'),
    ('information', 'mobile'): ('Mobile', 'Info mobile, appli.'),
    ('information', 'hikingmap'): ('Carte rando', 'Plan randonnée.'),
    ('information', 'name'): ('Nom', 'Panneau nom lieu.'),
    ('information', 'map_board'): ('Panneau carte', 'Plan affiché.'),
    ('information', 'history'): ('Histoire', 'Info patrimoine.'),
    ('information', 'citymap'): ('Plan ville', 'Carte urbaine.'),
    ('information', 'post'): ('Poteau', 'Poteau indicateur.'),
    ('information', 'sign'): ('Panneau', 'Panneau information.'),
    ('information', 'wild_life'): ('Faune', 'Info animaux sauvages.'),
    ('information', 'public_transport'): ('Transport', 'Info bus, train.'),
    ('information', 'plaque'): ('Plaque', 'Plaque commémorative.'),
    ('information', 'stele'): ('Stèle', 'Monument informatif.'),
    ('information', 'marker'): ('Repère', 'Borne, balise.'),
    ('information', 'visitor_centre'): ('Office tourisme', 'Centre visiteurs. Accueil.'),

    # =====================
    # BOARD_TYPE
    # =====================
    ('board_type', 'nature'): ('Nature', 'Panneau environnement.'),
    ('board_type', 'tourism'): ('Tourisme', 'Info touristique.'),
    ('board_type', 'plants'): ('Plantes', 'Botanique, flore.'),
    ('board_type', 'notice'): ('Avis', 'Annonces, affichage.'),
    ('board_type', 'geology'): ('Géologie', 'Roches, formation.'),
    ('board_type', 'name'): ('Nom', 'Identification lieu.'),
    ('board_type', 'history'): ('Histoire', 'Patrimoine, passé.'),
    ('board_type', 'obituary'): ('Nécrologie', 'Mémorial, défunts.'),
    ('board_type', 'wildlife'): ('Faune', 'Animaux sauvages.'),
    ('board_type', 'planet_walk'): ('Sentier planètes', 'Système solaire.'),
    ('board_type', 'public_transport'): ('Transport', 'Horaires, lignes.'),
    ('board_type', 'hiking'): ('Randonnée', 'Parcours, balisage.'),
    ('board_type', 'warning'): ('Avertissement', 'Danger, précaution.'),
    ('board_type', 'religion'): ('Religion', 'Info religieuse.'),
    ('board_type', 'rules'): ('Règlement', 'Consignes, interdictions.'),
    ('board_type', 'traffic'): ('Circulation', 'Info routière.'),
    ('board_type', 'communication'): ('Communication', 'Annonces.'),
    ('board_type', 'architecture'): ('Architecture', 'Bâtiment, style.'),
    ('board_type', 'infrastructure'): ('Infrastructure', 'Équipements, réseaux.'),
    ('board_type', 'district'): ('Quartier', 'Info secteur.'),

    # =====================
    # MAP_TYPE
    # =====================
    ('map_type', 'topo'): ('Topographique', 'Carte IGN, relief.'),
    ('map_type', 'public_transport'): ('Transport', 'Plan métro, bus.'),
    ('map_type', 'toposcope'): ('Table orientation', 'Panorama, sommet.'),
    ('map_type', 'hiking'): ('Randonnée', 'Carte sentiers.'),
    ('map_type', 'street'): ('Rue', 'Plan de ville.'),
    ('map_type', 'map'): ('Carte', 'Plan général.'),
    ('map_type', 'scheme'): ('Schéma', 'Plan simplifié.'),
    ('map_type', 'image'): ('Image', 'Photo, vue.'),
    ('map_type', 'citymap'): ('Plan ville', 'Carte urbaine.'),
    ('map_type', 'cycleway'): ('Vélo', 'Carte pistes cyclables.'),
}

# Generic enrichments for capacity/rooms/beds/stars/opening_hours/fee/charge
def generate_capacity_enrichment(value):
    """Generate enrichment for capacity values."""
    try:
        num = int(value)
        if num == 0:
            return ('Aucune place', 'Capacité nulle. Pas de place disponible.')
        elif num == 1:
            return ('1 place', 'Capacité d\'une place. Individuel, unique.')
        elif num <= 5:
            return (f'{num} places', f'Capacité de {num} places. Petite capacité.')
        elif num <= 20:
            return (f'{num} places', f'Capacité de {num} places. Capacité moyenne.')
        elif num <= 100:
            return (f'{num} places', f'Capacité de {num} places. Grande capacité.')
        elif num <= 500:
            return (f'{num} places', f'Capacité de {num} places. Très grande capacité.')
        else:
            return (f'{num} places', f'Capacité de {num} places. Capacité massive.')
    except:
        return (value, f'Capacité: {value}.')

def generate_rooms_enrichment(value):
    """Generate enrichment for rooms values."""
    try:
        num = int(value)
        if num == 0:
            return ('Aucune chambre', 'Pas de chambre.')
        elif num == 1:
            return ('1 chambre', 'Une chambre. Petit établissement.')
        elif num <= 10:
            return (f'{num} chambres', f'{num} chambres. Petit hôtel, gîte.')
        elif num <= 50:
            return (f'{num} chambres', f'{num} chambres. Hôtel moyen.')
        elif num <= 100:
            return (f'{num} chambres', f'{num} chambres. Grand hôtel.')
        else:
            return (f'{num} chambres', f'{num} chambres. Très grand hôtel.')
    except:
        return (value, f'Nombre de chambres: {value}.')

def generate_beds_enrichment(value):
    """Generate enrichment for beds values."""
    try:
        num = int(value)
        if num == 0:
            return ('Aucun lit', 'Pas de lit.')
        elif num == 1:
            return ('1 lit', 'Un lit. Chambre simple.')
        elif num <= 5:
            return (f'{num} lits', f'{num} lits. Petite capacité.')
        elif num <= 20:
            return (f'{num} lits', f'{num} lits. Capacité moyenne.')
        elif num <= 50:
            return (f'{num} lits', f'{num} lits. Grande capacité, auberge.')
        else:
            return (f'{num} lits', f'{num} lits. Très grande capacité.')
    except:
        return (value, f'Nombre de lits: {value}.')

def generate_stars_enrichment(value):
    """Generate enrichment for stars values."""
    stars_map = {
        '0': ('Sans étoile', 'Hébergement non classé. Budget, basique.'),
        '1': ('1 étoile', 'Hôtel 1 étoile. Simple, économique.'),
        '2': ('2 étoiles', 'Hôtel 2 étoiles. Confort standard.'),
        '2.5': ('2,5 étoiles', 'Hôtel 2-3 étoiles. Bon confort.'),
        '3': ('3 étoiles', 'Hôtel 3 étoiles. Confortable, services.'),
        '3S': ('3 étoiles supérieur', 'Hôtel 3 étoiles sup. Bon standing.'),
        '3.5': ('3,5 étoiles', 'Hôtel 3-4 étoiles. Très confortable.'),
        '4': ('4 étoiles', 'Hôtel 4 étoiles. Haut de gamme.'),
        '4S': ('4 étoiles supérieur', 'Hôtel 4 étoiles sup. Luxe.'),
        '5': ('5 étoiles', 'Hôtel 5 étoiles. Palace, luxe.'),
        'Standard': ('Standard', 'Catégorie standard. Confort basique.'),
        'Comfort': ('Confort', 'Catégorie confort. Bon niveau.'),
        'Superior Comfort': ('Confort supérieur', 'Catégorie confort sup. Très bien.'),
        'First Class': ('Première classe', 'Catégorie première classe. Haut standing.'),
        'Superior First Class': ('Première classe sup', 'Première classe supérieure. Excellent.'),
        'Luxury': ('Luxe', 'Catégorie luxe. Prestige.'),
        'Superior Luxury': ('Luxe supérieur', 'Luxe supérieur. Palace.'),
        'Superior Standard': ('Standard supérieur', 'Standard sup. Bon basique.'),
        'Superior Tourist': ('Touriste supérieur', 'Touriste sup. Économique amélioré.'),
    }
    return stars_map.get(value, (value, f'Classement: {value}.'))

def generate_fee_enrichment(value):
    """Generate enrichment for fee values."""
    fee_map = {
        'yes': ('Payant', 'Entrée payante. Tarif, prix.'),
        'no': ('Gratuit', 'Accès gratuit. Sans frais.'),
        'donation': ('Participation libre', 'Prix libre, donation. Selon volonté.'),
        'varies': ('Variable', 'Tarif variable. Selon conditions.'),
        'some': ('Parfois payant', 'Partiellement payant. Certaines conditions.'),
        'conditional': ('Conditionnel', 'Payant selon conditions.'),
        'unknown': ('Inconnu', 'Tarification non renseignée.'),
    }
    if value in fee_map:
        return fee_map[value]
    # Horaires
    if 'Mo' in value or '-' in value and ':' in value:
        return ('Payant selon horaires', f'Payant aux horaires: {value}.')
    return (value, f'Tarification: {value}.')

def generate_opening_hours_enrichment(value):
    """Generate enrichment for opening_hours values."""
    special = {
        '24/7': ('24h/24 7j/7', 'Ouvert en permanence. Toujours accessible.'),
        'Mo-Su': ('7j/7', 'Ouvert tous les jours.'),
        'Mo-Fr': ('Lundi-vendredi', 'Ouvert en semaine.'),
        'Mo-Sa': ('Lundi-samedi', 'Ouvert sauf dimanche.'),
        'sunrise-sunset': ('Lever-coucher soleil', 'Ouvert du lever au coucher du soleil.'),
        'sunset-sunrise': ('Nuit', 'Ouvert la nuit.'),
        'dawn-dusk': ('Aube-crépuscule', 'Ouvert du matin au soir.'),
        'dusk-dawn': ('Nuit', 'Ouvert la nuit seulement.'),
        'closed': ('Fermé', 'Actuellement fermé.'),
        'off': ('Fermé', 'Non ouvert actuellement.'),
        'unknown': ('Horaires inconnus', 'Heures d\'ouverture non renseignées.'),
        'Monday': ('Lundi', 'Ouvert le lundi.'),
        'Tuesday': ('Mardi', 'Ouvert le mardi.'),
        'Wednesday': ('Mercredi', 'Ouvert le mercredi.'),
        'Thursday': ('Jeudi', 'Ouvert le jeudi.'),
        'Friday': ('Vendredi', 'Ouvert le vendredi.'),
        'Saturday': ('Samedi', 'Ouvert le samedi.'),
        'Sunday': ('Dimanche', 'Ouvert le dimanche.'),
    }
    if value in special:
        return special[value]
    # Parse common patterns
    if value.startswith('Mo-Su '):
        hours = value[6:]
        return (f'7j/7 {hours}', f'Ouvert tous les jours {hours}.')
    if value.startswith('Mo-Fr '):
        hours = value[6:]
        return (f'Semaine {hours}', f'Ouvert lundi-vendredi {hours}.')
    if value.startswith('Mo-Sa '):
        hours = value[6:]
        return (f'Lun-sam {hours}', f'Ouvert lundi-samedi {hours}.')
    if value == '00:00-24:00':
        return ('24h/24', 'Ouvert 24 heures.')
    return (f'Horaires: {value[:15]}...', f'Horaires d\'ouverture: {value}.')

def generate_charge_enrichment(value):
    """Generate enrichment for charge values."""
    # Parse currency patterns
    if 'EUR' in value:
        return (f'Tarif: {value}', f'Prix en euros: {value}.')
    if 'USD' in value:
        return (f'Tarif: {value}', f'Prix en dollars: {value}.')
    if 'CHF' in value:
        return (f'Tarif: {value}', f'Prix en francs suisses: {value}.')
    if 'GBP' in value:
        return (f'Tarif: {value}', f'Prix en livres sterling: {value}.')
    if 'CZK' in value:
        return (f'Tarif: {value}', f'Prix en couronnes tchèques: {value}.')
    if 'RUB' in value:
        return (f'Tarif: {value}', f'Prix en roubles: {value}.')
    if 'JPY' in value:
        return (f'Tarif: {value}', f'Prix en yens: {value}.')
    if 'CNY' in value or '¥' in value:
        return (f'Tarif: {value}', f'Prix en yuans: {value}.')
    if 'HKD' in value:
        return (f'Tarif: {value}', f'Prix en dollars HK: {value}.')
    if 'CAD' in value:
        return (f'Tarif: {value}', f'Prix en dollars CA: {value}.')
    if 'VND' in value:
        return (f'Tarif: {value}', f'Prix en dongs: {value}.')
    if 'XOF' in value:
        return (f'Tarif: {value}', f'Prix en francs CFA: {value}.')
    if value == '0':
        return ('Gratuit', 'Sans frais.')
    try:
        num = float(value)
        return (f'{num}', f'Tarif: {num}.')
    except:
        return (value, f'Tarification: {value}.')

def generate_brand_enrichment(brand):
    """Generate enrichment for brand values."""
    known_brands = {
        'McDonald\'s': ('McDonald\'s', 'McDonald\'s, fast-food. Burger, frites, Big Mac.'),
        'Burger King': ('Burger King', 'Burger King, fast-food. Whopper, burgers grillés.'),
        'Starbucks': ('Starbucks', 'Starbucks, café. Frappuccino, espresso.'),
        'KFC': ('KFC', 'Kentucky Fried Chicken. Poulet frit, bucket.'),
        'Subway': ('Subway', 'Subway, sandwiches. Sub, personnalisé.'),
        'Shell': ('Shell', 'Shell, station essence. Carburant, pétrole.'),
        'BP': ('BP', 'BP, station service. Essence, diesel.'),
        'Total': ('Total', 'Total, station service. Carburant, pétrole.'),
        'Carrefour': ('Carrefour', 'Carrefour, supermarché. Grande distribution.'),
        'Lidl': ('Lidl', 'Lidl, discounter. Hard discount, économique.'),
        'Aldi': ('Aldi', 'Aldi, discounter. Hard discount, prix bas.'),
        'Walmart': ('Walmart', 'Walmart, hypermarché. Grande surface américaine.'),
        'Amazon Locker': ('Casier Amazon', 'Amazon Locker, retrait colis. Consigne.'),
        'DHL': ('DHL', 'DHL, transporteur colis. Livraison, express.'),
        'La Poste': ('La Poste', 'La Poste, courrier. Lettres, colis, services.'),
        'SNCF': ('SNCF', 'SNCF, trains. Voyages, TGV, billetterie.'),
        'Orange': ('Orange', 'Orange, télécom. Mobile, internet, fibre.'),
        'Vodafone': ('Vodafone', 'Vodafone, téléphone. Mobile, forfait.'),
        'Tesla': ('Tesla', 'Tesla, bornes recharge. Voiture électrique.'),
        'H&M': ('H&M', 'H&M, vêtements. Mode, prêt-à-porter.'),
        'Zara': ('Zara', 'Zara, mode. Vêtements, tendances.'),
        'Decathlon': ('Decathlon', 'Decathlon, sport. Articles sportifs, équipement.'),
        'IKEA': ('IKEA', 'IKEA, meubles. Décoration, maison, suédois.'),
    }
    if brand in known_brands:
        return known_brands[brand]
    # Generic brand description
    return (brand, f'Enseigne {brand}. Marque, commerce.')


def main():
    print("=== Re-enrichissement des tags ===\n")

    # Read tags to enrich
    with open(TAGS_FILE, 'r') as f:
        tags_to_enrich = [line.strip() for line in f if line.strip()]

    print(f"Tags à ré-enrichir: {len(tags_to_enrich)}")

    # Read current data
    with open(INPUT_FILE, 'r') as f:
        data = json.load(f)

    enriched_count = 0
    skipped_count = 0

    for tag_line in tags_to_enrich:
        if '=' not in tag_line:
            continue

        parts = tag_line.split('=', 1)
        key = parts[0]
        value = parts[1] if len(parts) > 1 else ''

        if not key or not value:
            continue

        # Check if key and value exist
        if key not in data:
            skipped_count += 1
            continue
        if value not in data[key]['values']:
            skipped_count += 1
            continue

        vd = data[key]['values'][value]

        # Check if we have a manual enrichment
        if (key, value) in ENRICHMENTS:
            fr, enriched = ENRICHMENTS[(key, value)]
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        # Generate enrichments for numeric values
        elif key == 'capacity':
            fr, enriched = generate_capacity_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'rooms':
            fr, enriched = generate_rooms_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'beds':
            fr, enriched = generate_beds_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'stars':
            fr, enriched = generate_stars_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'fee':
            fr, enriched = generate_fee_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'opening_hours':
            fr, enriched = generate_opening_hours_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'charge':
            fr, enriched = generate_charge_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        elif key == 'brand':
            fr, enriched = generate_brand_enrichment(value)
            vd['description_fr'] = fr
            vd['description_enriched'] = enriched
            enriched_count += 1
        else:
            # Keep track of unenriched
            skipped_count += 1

    # Save
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"\nEnrichis: {enriched_count}")
    print(f"Non traités: {skipped_count}")
    print(f"Sauvegardé dans {OUTPUT_FILE}")


if __name__ == '__main__':
    main()
