# Dashboard SIG ProSMAT - Coopératives Agricoles du Togo

## Description

Dashboard interactif de visualisation et d'analyse des données des coopératives agricoles au Togo dans le cadre du projet ProSMAT (Projet de Soutien aux Marchés Agricoles du Togo).

## Fonctionnalités Principales

### Visualisations Cartographiques
- **Carte Folium Interactive**: Navigation fluide avec zoom, couches multiples et popups détaillés
- **Cartes SIG Statiques**: Visualisations professionnelles avec matplotlib/geopandas
- **Système de Zoom Avancé**: 3 modes de zoom (automatique, région, personnalisé)

### Filtres Hiérarchiques
- **Localisation**: Région → Préfecture → Canton → Village
- **Agent de Terrain**: Filtrage par CRP
- **Statuts**: Immatriculation, Formation, Engagement, Parcelle, Production
- **Effectifs**: Slider pour filtrer par taille de coopérative

### Analyses et Statistiques
- **KPIs en Temps Réel**: Indicateurs clés avec visualisations colorées
- **Analyses Data Science**: Distribution, corrélations, tendances
- **Export de Données**: Téléchargement des cartes et tableaux

## Installation

### Prérequis
- Python 3.11+
- pip ou conda

### Installation des Dépendances

```bash
pip install -r requirements.txt
```

### Fichiers Requis
- `MISSION_DE_SUIVI_cleaned.xlsx`: Données des coopératives
- `gadm41_TGO.gpkg`: Données géographiques du Togo (GADM)
- `logo.jfif`: Logo ProSMAT

## Utilisation

### Lancement du Dashboard

```bash
streamlit run dashboard_sig_streamlit.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à l'adresse `http://localhost:8501`

### Navigation

#### 1. Filtres (Sidebar)
- Sélectionnez vos critères de filtrage
- Les filtres sont hiérarchiques et dynamiques
- Utilisez "Réinitialiser tous les filtres" pour revenir à la vue complète

#### 2. Onglets Principaux

**Carte Folium Interactive**
- Carte interactive avec zoom et pan
- Couches multiples (OpenStreetMap, Satellite, Mode Sombre)
- Choroplèthe par région
- Marqueurs colorés par région
- Carte de chaleur optionnelle

**Carte SIG Statique**
- 13 types de cartes différentes
- Système de zoom à 5 niveaux
- Zoom personnalisé avec coordonnées
- Export haute résolution (200 DPI)

**Analyses Data Science**
- Distribution des données
- Corrélations entre variables
- Indicateurs de performance
- Tendances temporelles

**Données**
- Tableau filtrable et triable
- Recherche par coopérative
- Export CSV

## Structure du Projet

```
.
 dashboard_sig_streamlit.py # Application principale
 map_styles.py # Configuration des styles de cartes
 requirements.txt # Dépendances Python
 logo.jfif # Logo ProSMAT
 MISSION_DE_SUIVI_cleaned.xlsx # Données des coopératives
 gadm41_TGO.gpkg # Données géographiques
 GUIDE_ZOOM.md # Guide d'utilisation du zoom
 README_DASHBOARD.md # Ce fichier
```

## Personnalisation

### Modifier les Couleurs
Éditez `map_styles.py` pour changer:
- Couleurs des régions
- Palettes choroplèthes
- Styles de marqueurs

### Modifier le Style CSS
Éditez la section CSS dans `dashboard_sig_streamlit.py` (lignes 30-150)

## Types de Cartes Disponibles

1. **Localisation**: Points colorés par région
2. **Choroplèthe - Coopératives**: Intensité par nombre
3. **Choroplèthe - Effectif**: Intensité par effectif total
4. **Choroplèthe - Femmes**: Intensité par nombre de femmes
5. **Choroplèthe - Jeunes**: Intensité par nombre de jeunes
6. **Choroplèthe - Handicap**: Intensité par personnes handicapées
7. **Détail par Préfecture**: Vue détaillée des préfectures
8. **Statut Immatriculation**: Visualisation du statut
9. **Engagement Agroécologique**: Visualisation de l'engagement
10. **Parcelle d'Apprentissage**: Visualisation du choix de parcelle
11. **Matériel de Production**: Visualisation de la réception
12. **Taille Proportionnelle**: Points proportionnels à l'effectif
13. **Zoom Personnalisé**: Zone définie par l'utilisateur

## Dépannage

### Le dashboard ne démarre pas
- Vérifiez que toutes les dépendances sont installées
- Vérifiez que les fichiers de données sont présents
- Consultez les logs d'erreur dans le terminal

### Les cartes ne s'affichent pas
- Vérifiez que les coordonnées GPS sont valides
- Assurez-vous que le fichier GADM est présent
- Vérifiez les filtres appliqués

### Performances lentes
- Réduisez le nombre de données affichées avec les filtres
- Fermez les autres onglets du navigateur
- Redémarrez l'application

## Notes Techniques

### Système de Coordonnées
- CRS: EPSG:4326 (WGS84)
- Limites du Togo: Lon [-1, 2], Lat [6, 11]

### Filtrage Spatial
Le filtre par préfecture utilise une jointure spatiale (spatial join) pour déterminer dans quelle préfecture administrative se trouve chaque coopérative basée sur ses coordonnées GPS.

### Performance
- Cache Streamlit activé pour le chargement des données
- Optimisation des requêtes géospatiales
- Rendu progressif des cartes

## Contribution

Pour contribuer au projet:
1. Créez une branche pour votre fonctionnalité
2. Testez vos modifications
3. Documentez les changements
4. Soumettez une pull request

## Support

Pour toute question ou problème:
- Consultez le `GUIDE_ZOOM.md` pour l'utilisation du zoom
- Vérifiez la section "Informations" dans la sidebar
- Contactez l'équipe ProSMAT

## Licence

© 2025 ProSMAT - Tous droits réservés

## Remerciements

- Données: Mission de Suivi ProSMAT
- Données géographiques: GADM (Global Administrative Areas)
- Technologies: Streamlit, Folium, GeoPandas, Plotly
