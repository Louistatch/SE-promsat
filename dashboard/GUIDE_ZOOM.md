# Guide d'Utilisation du Système de Zoom SIG

## Fonctionnalités de Zoom

Le dashboard SIG dispose maintenant de trois systèmes de zoom pour explorer les données géographiques:

### 1. Zoom Automatique (Slider)

**Emplacement**: Colonne de droite, slider "Niveau de zoom"

**Utilisation**:
- Niveau 1: Vue complète du Togo
- Niveau 2: Zoom léger (50% de la vue)
- Niveau 3: Zoom moyen (33% de la vue)
- Niveau 4: Zoom fort (25% de la vue)
- Niveau 5: Zoom maximum (20% de la vue)

**Fonctionnement**:
- Le zoom se centre automatiquement sur les données filtrées
- Si aucun filtre n'est appliqué, le zoom se centre sur le centre géographique du pays
- Fonctionne avec tous les types de cartes

**Exemple d'utilisation**:
1. Sélectionnez une région dans les filtres (ex: "Kara")
2. Choisissez un type de carte (ex: "Localisation des coopératives")
3. Ajustez le slider de zoom à 3 ou 4
4. La carte zoome automatiquement sur la région Kara

### 2. Zoom sur Région

**Emplacement**: Type de carte "Zoom sur une Region"

**Utilisation**:
1. Sélectionnez "Zoom sur une Region" dans le menu déroulant
2. Choisissez la région à zoomer dans le menu qui apparaît
3. La carte affiche uniquement cette région avec:
 - Les limites des préfectures
 - Les noms des préfectures
 - Les coopératives avec leurs noms
 - Statistiques détaillées en dessous

**Avantages**:
- Vue détaillée d'une région spécifique
- Affichage des noms de coopératives
- Tableau récapitulatif des coopératives de la région

### 3. Zoom Personnalisé

**Emplacement**: Type de carte "Zoom Personnalise"

**Utilisation**:
1. Sélectionnez "Zoom Personnalise" dans le menu déroulant
2. Définissez les limites géographiques:
 - **Longitude Min**: Limite ouest (ex: -1.0)
 - **Longitude Max**: Limite est (ex: 2.0)
 - **Latitude Min**: Limite sud (ex: 6.0)
 - **Latitude Max**: Limite nord (ex: 11.0)
3. La carte affiche uniquement la zone définie

**Coordonnées de référence du Togo**:
- Longitude: -1.0 à 2.0
- Latitude: 6.0 à 11.0

**Exemples de zones**:
- **Nord du Togo**: Lon: 0.0-1.5, Lat: 9.5-11.0
- **Sud du Togo**: Lon: 0.5-1.8, Lat: 6.0-7.5
- **Centre**: Lon: 0.5-1.5, Lat: 7.5-9.5

## Combinaison des Systèmes

Vous pouvez combiner les différents systèmes:

**Exemple 1: Zoom sur une ville spécifique**
1. Utilisez "Zoom Personnalise"
2. Définissez une petite zone (ex: Lon: 1.2-1.3, Lat: 6.1-6.2 pour Lomé)
3. Ajustez le slider de zoom à 5 pour un zoom maximum

**Exemple 2: Analyse régionale détaillée**
1. Filtrez par région dans la sidebar
2. Sélectionnez "Zoom sur une Region"
3. Ajustez le slider de zoom à 2 ou 3
4. Consultez les statistiques détaillées en dessous

**Exemple 3: Comparaison de zones**
1. Utilisez "Zoom Personnalise" pour une première zone
2. Téléchargez la carte (bouton "Telecharger la carte")
3. Changez les coordonnées pour une autre zone
4. Téléchargez la deuxième carte
5. Comparez les deux images

## Conseils d'Utilisation

### Pour une Exploration Générale
- Commencez avec le niveau de zoom 1 (vue complète)
- Utilisez les filtres de la sidebar pour réduire les données
- Augmentez progressivement le zoom

### Pour une Analyse Détaillée
- Utilisez "Zoom sur une Region" pour une région spécifique
- Ou utilisez "Zoom Personnalise" pour une zone précise
- Combinez avec les filtres de statut (immatriculation, engagement, etc.)

### Pour des Présentations
- Utilisez le zoom pour créer plusieurs vues
- Téléchargez chaque vue en haute résolution (200 DPI)
- Le nom du fichier inclut le niveau de zoom pour faciliter l'organisation

## Raccourcis Clavier

Aucun raccourci clavier n'est disponible, mais vous pouvez:
- Utiliser Tab pour naviguer entre les contrôles
- Utiliser les flèches pour ajuster le slider de zoom
- Utiliser Entrée pour valider les champs de coordonnées

## Résolution des Problèmes

**La carte ne zoome pas**:
- Vérifiez que des données sont affichées (nombre de coopératives > 0)
- Essayez de réinitialiser les filtres
- Vérifiez que le niveau de zoom est > 1

**La zone personnalisée est vide**:
- Vérifiez que les coordonnées sont dans les limites du Togo
- Assurez-vous que Longitude Min < Longitude Max
- Assurez-vous que Latitude Min < Latitude Max

**Les données ne sont pas centrées**:
- Le zoom automatique se centre sur les données filtrées
- Si vous voulez centrer sur une zone spécifique, utilisez "Zoom Personnalise"

## Limites Techniques

- Le zoom maximum est limité à 5x pour éviter les problèmes de performance
- Les coordonnées personnalisées doivent être dans les limites du Togo
- Le zoom ne fonctionne pas sur la carte Folium (onglet 1), uniquement sur les cartes SIG statiques (onglet 2)
