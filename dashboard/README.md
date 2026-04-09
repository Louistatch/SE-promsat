# Dashboard SIG ProSMAT v3.0 🗺️

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Proprietary-yellow.svg)]()
[![Status](https://img.shields.io/badge/Status-Production%20Ready-green.svg)]()

Dashboard interactif avancé pour l'analyse et la visualisation des coopératives agricoles au Togo avec cartographie SIG et data science.

![Dashboard Preview](https://img.shields.io/badge/Dashboard-Interactive-brightgreen)

## 🎯 Objectif

Fournir un outil d'analyse géospatiale et statistique pour le suivi des coopératives agricoles dans le cadre du projet ProSMAT au Togo.

## ✨ Fonctionnalités Principales

### 📊 5 Onglets d'Analyse

1. **Carte Folium Interactive**
   - Carte interactive avec clusters dynamiques
   - Heatmap de densité
   - Popups détaillés par coopérative
   - Contrôles de couches multiples

2. **Cartes SIG Statiques**
   - 13 types de cartes thématiques
   - Zoom par région avec détails préfectures
   - Export PNG haute résolution (200 DPI)
   - Choroplèthes et cartes de localisation

3. **Analyses Data Science**
   - Distribution et corrélations
   - Indicateurs de performance (jauges)
   - Graphiques radar par région
   - Matrices de dispersion

4. **Marché Agroécologique**
   - Top 10 coopératives par région (scoring multi-critères)
   - Analyse de 89 cultures (668 mentions)
   - Export Excel multi-feuilles
   - Recommandations stratégiques

5. **Données**
   - Tableau filtré et recherche
   - Export CSV
   - Statistiques résumées

### 🔍 Filtres Avancés

- **Géographiques**: Région → Préfecture → Commune → Village
- **Agent CRP**: Suivi par agent terrain
- **Statuts**: Immatriculation, Formation, Engagement, Parcelle, Production
- **Effectifs**: Slider pour filtrer par taille

### 📈 Analyses Avancées

- **Corrélations**: Matrice de corrélation avec interprétation automatique
- **Indicateurs**: Taux d'immatriculation, engagement agroécologique, restitution
- **Scoring**: 8 critères pondérés (0-100) pour identifier les coopératives à fort potentiel
- **Cultures**: Analyse des cultures dominantes par région

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.8+
- pip

### Installation

```bash
# Cloner le dépôt
git clone https://github.com/Louistatch/ProSMAT-TogoDashboard.git
cd ProSMAT-TogoDashboard

# Installer les dépendances
pip install -r requirements.txt

# Lancer le dashboard
streamlit run dashboard_sig_streamlit.py
```

Le dashboard s'ouvre automatiquement dans votre navigateur à `http://localhost:8501`

## 📦 Dépendances

```
streamlit>=1.28.0
pandas>=2.0.0
geopandas>=0.13.0
folium>=0.14.0
streamlit-folium>=0.13.0
plotly>=5.14.0
matplotlib>=3.7.0
seaborn>=0.12.0
openpyxl>=3.1.0
```

## 📁 Structure du Projet

```
ProSMAT-TogoDashboard/
├── dashboard_sig_streamlit.py    # Application principale
├── map_styles.py                 # Configuration des styles de cartes
├── map_utils.py                  # Utilitaires cartographiques
├── requirements.txt              # Dépendances Python
├── MISSION_DE_SUIVI_cleaned.xlsx # Données des coopératives
├── gadm41_TGO.gpkg              # Données géographiques GADM
├── logo.jfif                     # Logo du projet
├── README.md                     # Documentation principale
├── LISEZ_MOI_DABORD.md          # Guide de démarrage
├── GUIDE_DEMARRAGE_RAPIDE.md    # Guide rapide
├── GUIDE_UTILISATION_ZOOM.md    # Guide zoom région
├── GUIDE_MARCHE_AGROECOLOGIQUE.md # Guide marché agroécologique
└── test_*.py                     # Scripts de test
```

## 📊 Données

### Sources
- **Coopératives**: 232 coopératives agricoles au Togo
- **Géographie**: Données GADM41 (5 régions, 16 préfectures, 37 communes)
- **Effectifs**: 5,948 membres (3,630 femmes, 2,393 jeunes)

### Régions Couvertes
- Centre: 32 coopératives
- Kara: 40 coopératives
- Maritime: 40 coopératives
- Plateaux: 60 coopératives
- Savanes: 60 coopératives

## 🎨 Captures d'Écran

### Carte Interactive
![Carte Folium](https://via.placeholder.com/800x400?text=Carte+Interactive+Folium)

### Analyses Data Science
![Analyses](https://via.placeholder.com/800x400?text=Analyses+Data+Science)

### Marché Agroécologique
![Marché](https://via.placeholder.com/800x400?text=Marché+Agroécologique)

## 📖 Documentation

- **[LISEZ_MOI_DABORD.md](LISEZ_MOI_DABORD.md)** - Point de départ
- **[GUIDE_DEMARRAGE_RAPIDE.md](GUIDE_DEMARRAGE_RAPIDE.md)** - Installation et lancement
- **[README_COMPLET.md](README_COMPLET.md)** - Documentation technique complète
- **[CHANGELOG_V3.md](CHANGELOG_V3.md)** - Nouveautés version 3.0
- **[SYNTHESE_FINALE_V3.md](SYNTHESE_FINALE_V3.md)** - Synthèse technique

## 🧪 Tests

```bash
# Test complet
python test_final.py

# Test architecture
python test_architecture.py

# Test zoom région
python test_zoom_region.py

# Test marché agroécologique
python test_marche_top10_regions.py
```

## 🔧 Configuration

Le dashboard est prêt à l'emploi sans configuration supplémentaire. Les fichiers de données doivent être présents :
- `MISSION_DE_SUIVI_cleaned.xlsx`
- `gadm41_TGO.gpkg`

## 📈 Nouveautés v3.0

### Onglet Marché Agroécologique
- Top 10 par région avec scoring multi-critères
- Export Excel multi-feuilles (1 par région)
- Analyse de 89 cultures uniques
- Recommandations stratégiques

### Zoom Région Amélioré
- Carte choroplèthe par préfecture
- 7 nouveaux graphiques et tableaux
- Indicateurs de performance détaillés
- Graphiques radar Top 5

### Architecture Hiérarchique
- 4 niveaux: Région → Préfecture → Commune → Village
- Filtres dynamiques en cascade
- 16 préfectures, 37 communes

### Analyses Data Science
- Guides d'interprétation des corrélations
- Légendes explicatives pour les indicateurs
- Interprétations automatiques
- Messages contextuels

## 🤝 Contribution

Ce projet est développé pour ProSMAT. Pour toute suggestion ou amélioration, veuillez contacter le développeur.

## 👨‍💻 Développeur

**TATCHIDA Louis**
- MSc Agronomie
- MSc Ingénierie Financière adaptée à l'Agriculture
- Data Analyst

## 📄 Licence

Dashboard développé pour ProSMAT - Mission de Suivi des Coopératives Agricoles au Togo

© 2025 - Tous droits réservés

## 🙏 Remerciements

- ProSMAT pour le projet
- GADM pour les données géographiques
- Communauté Streamlit pour les outils

## 📞 Support

Pour toute question ou problème:
1. Consultez la documentation dans le dossier
2. Vérifiez les fichiers de test
3. Contactez le développeur

---

**Version**: 3.0  
**Date**: Février 2025  
**Statut**: Production Ready

⭐ Si ce projet vous est utile, n'hésitez pas à lui donner une étoile!
