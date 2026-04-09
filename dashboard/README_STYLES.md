# Configuration des Styles pour le Dashboard SIG

## Structure des Fichiers

### `dashboard_sig_streamlit.py`
Fichier principal de l'application Streamlit contenant:
- Interface utilisateur
- Chargement des données
- Création des cartes interactives (Folium)
- Création des cartes statiques (Matplotlib)
- Analyses et visualisations

### `map_styles.py`
Module de configuration des styles pour les cartes SIG contenant:
- Palettes de couleurs pour les régions
- Styles de marqueurs (cercles, croix, carrés)
- Configuration des cartes choroplèthes
- Labels et titres standardisés
- Fonctions utilitaires pour le formatage

## Avantages de cette Architecture

1. **Séparation des préoccupations**: La logique métier est séparée de la configuration visuelle
2. **Maintenance facilitée**: Modifier les couleurs ou styles sans toucher au code principal
3. **Réutilisabilité**: Les styles peuvent être réutilisés dans d'autres projets
4. **Cohérence visuelle**: Tous les éléments visuels sont centralisés
5. **Pas de conflit**: Les deux fichiers fonctionnent ensemble sans interférence

## Personnalisation des Styles

### Modifier les Couleurs des Régions
Dans `map_styles.py`, section `REGION_COLORS`:
```python
REGION_COLORS = {
 'Centre': '#e74c3c', # Rouge
 'Kara': '#3498db', # Bleu
 'Savanes': '#2ecc71', # Vert
 'Plateaux': '#9b59b6', # Violet
 'Maritime': '#f39c12' # Orange
}
```

### Modifier les Marqueurs
Dans `map_styles.py`, section `MARKERS`:
```python
MARKERS = {
 'oui': {
 'marker': 'o', # Forme: o=cercle, s=carré, ^=triangle, etc.
 'size': 80, # Taille du marqueur
 'alpha': 0.8, # Transparence (0-1)
 'edgecolor': 'white', # Couleur du contour
 'linewidth': 1.5 # Épaisseur du contour
 }
}
```

### Modifier les Palettes Choroplèthes
Dans `map_styles.py`, section `CHOROPLETH_CMAPS`:
```python
CHOROPLETH_CMAPS = {
 'cooperatives': 'Reds', # Palette pour nombre de coopératives
 'effectif': 'Blues', # Palette pour effectif total
 'femmes': 'Purples', # Palette pour femmes
 'jeunes': 'Greens', # Palette pour jeunes
 'handicap': 'Oranges' # Palette pour personnes handicapées
}
```

Palettes disponibles: 'Reds', 'Blues', 'Greens', 'Purples', 'Oranges', 'YlOrRd', 'YlGnBu', 'RdYlGn', etc.

### Modifier les Labels
Dans `map_styles.py`, section `LABELS`:
```python
LABELS = {
 'immatriculation': {
 'oui': 'Immatricule',
 'non': 'Non immatricule',
 'non_renseigne': 'Non renseigne'
 }
}
```

## Symboles Utilisés

### Marqueurs de Statut
- **Cercle (o)**: Statut positif (Oui, Engagé, etc.)
- **Croix (X)**: Statut négatif (Non, Non engagé, etc.)
- **Carré (s)**: Non renseigné

### Abréviations sur les Cartes
- **F**: Femmes
- **J**: Jeunes
- **H**: Personnes handicapées
- **coop.**: Coopératives

## Types de Cartes Disponibles

1. **Localisation**: Points colorés par région
2. **Choroplèthe - Coopératives**: Intensité selon le nombre de coopératives
3. **Choroplèthe - Effectif**: Intensité selon l'effectif total
4. **Choroplèthe - Femmes**: Intensité selon le nombre de femmes
5. **Choroplèthe - Jeunes**: Intensité selon le nombre de jeunes
6. **Choroplèthe - Handicap**: Intensité selon le nombre de personnes handicapées
7. **Détail par Préfecture**: Vue détaillée par préfecture
8. **Statut Immatriculation**: Visualisation du statut d'immatriculation
9. **Engagement Agroécologique**: Visualisation de l'engagement
10. **Parcelle d'Apprentissage**: Visualisation du choix de parcelle
11. **Matériel de Production**: Visualisation de la réception de matériel
12. **Taille Proportionnelle**: Points proportionnels à l'effectif
13. **Zoom Région**: Vue détaillée d'une région spécifique

## Dépendances

```
streamlit
pandas
geopandas
numpy
folium
streamlit-folium
matplotlib
seaborn
plotly
openpyxl
statsmodels
scipy
```

## Lancement de l'Application

```bash
streamlit run dashboard_sig_streamlit.py
```

## Notes Techniques

- Les émoticônes ont été retirées pour éviter les problèmes d'encodage
- Les accents sont conservés dans les chaînes de caractères
- La configuration matplotlib est centralisée dans `map_styles.py`
- Les fonctions utilitaires facilitent la maintenance du code
