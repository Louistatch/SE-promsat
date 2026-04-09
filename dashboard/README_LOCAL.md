# Dashboard SIG ProSMAT v3.0

Dashboard interactif pour l'analyse des coopératives agricoles au Togo avec cartographie avancée et data science.

## Démarrage Rapide

```bash
streamlit run dashboard_sig_streamlit.py
```

Ouvre automatiquement dans le navigateur: `http://localhost:8501`

## Nouveautés v3.0

### Onglet Marché Agroécologique
- **Top 10 par Région**: 50 coopératives identifiées (10 par région)
- **Scoring Multi-Critères**: 8 dimensions, 0-100
- **Export Excel**: Multi-feuilles (1 par région)
- **Analyse Cultures**: 89 cultures uniques, 668 mentions

### Zoom Région Amélioré
- Carte choroplèthe par préfecture
- 7 nouveaux graphiques et tableaux
- Indicateurs de performance
- Graphiques radar Top 5

### Architecture Préfecture/Commune
- Hiérarchie 4 niveaux: Région → Préfecture → Commune → Village
- 16 préfectures, 37 communes

## Fonctionnalités

### 5 Onglets
1. **Carte Folium Interactive** - Carte interactive avec clusters et heatmap
2. **Cartes SIG Statiques** - 13 types de cartes, zoom région, export PNG
3. **Analyses Data Science** - Distribution, corrélations, indicateurs, tendances
4. **Marché Agroécologique** - Top 10 par région, scoring, cultures
5. **Données** - Tableau filtré, recherche, export CSV

### Filtres (Sidebar)
- Géographiques: Région, Préfecture, Commune, Village
- Agent CRP
- Statuts: Immatriculation, Formation, Engagement, Parcelle, Production
- Effectif: Slider
- Reset rapide

### Exports
- **PNG**: Cartes haute résolution (200 DPI)
- **Excel**: Multi-feuilles (1 par région + 1 globale)
- **CSV**: Format simple

## Données

- **232 coopératives** (avec coordonnées GPS valides)
- **5 régions**: Centre (37), Kara (53), Maritime (52), Plateaux (30), Savanes (60)
- **16 préfectures**, **37 communes**, **178 villages**

## Documentation

### Commencer
- **LISEZ_MOI_DABORD.md** - Point d'entrée
- **GUIDE_DEMARRAGE_RAPIDE.md** - Guide en 3 étapes

### Guides
- **GUIDE_UTILISATION_ZOOM.md** - Zoom par région
- **GUIDE_MARCHE_AGROECOLOGIQUE.md** - Onglet Marché

### Technique
- **README_COMPLET.md** - Documentation exhaustive
- **SYNTHESE_FINALE_V3.md** - Synthèse technique
- **CHANGELOG_V3.md** - Notes de version

## Tests

```bash
# Test global
python test_final.py

# Test Marché
python test_marche_top10_regions.py

# Vérification finale
python VERIFICATION_FINALE.py
```

## Prérequis

### Fichiers
- `MISSION_DE_SUIVI_cleaned.xlsx` - Données coopératives
- `gadm41_TGO.gpkg` - Données géographiques
- `logo.jfif` - Logo (optionnel)

### Packages
```bash
pip install -r requirements.txt
```

Packages principaux:
- streamlit
- pandas
- geopandas
- folium
- plotly
- matplotlib
- seaborn

## Structure

```
.
 dashboard_sig_streamlit.py # Application principale (124 KB)
 map_styles.py # Styles et couleurs
 map_utils.py # Utilitaires cartographiques
 requirements.txt # Dépendances Python
 MISSION_DE_SUIVI_cleaned.xlsx # Données (183 KB)
 gadm41_TGO.gpkg # Géodonnées (2.2 MB)
 logo.jfif # Logo
 test_*.py # Tests (4 fichiers)
 VERIFICATION_FINALE.py # Script de vérification
 *.md # Documentation (20 fichiers)
```

## Cas d'Usage

### Identifier les Coopératives à Fort Potentiel
Onglet "Marché Agroécologique" → Sélectionner région → Voir Top 10

### Analyser une Région
Filtrer par région → "Cartes SIG" → "Zoom sur une Région"

### Exporter des Données
Onglet "Marché Agroécologique" → "Télécharger Excel"

### Voir les Cultures Populaires
Onglet "Marché Agroécologique" → "Cultures Dominantes"

## Scoring (Marché Agroécologique)

### Critères (0-100)
1. **Engagement Agroécologique** (20%)
2. **Effectif Total** (15%)
3. **Immatriculation** (15%)
4. **Restitution Formation** (15%)
5. **Parcelle d'Apprentissage** (10%)
6. **Production Contre-Saison** (10%)
7. **Taux de Féminisation** (7.5%)
8. **Taux de Jeunes** (7.5%)

### Interprétation
- **90-100**: Excellent - Prêt pour le marché
- **70-89**: Bon - Accompagnement léger
- **50-69**: Moyen - Renforcement nécessaire
- **<50**: Faible - Formation intensive

## Dépannage

### Le dashboard ne se lance pas
```bash
cd "D:\ProSMAT\Analyse projet"
.venv\Scripts\activate
streamlit run dashboard_sig_streamlit.py
```

### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

### Les données ne s'affichent pas
- Vérifier les fichiers Excel et GPKG
- Réinitialiser les filtres (bouton "Reset")

## Support

- **Documentation**: 20 fichiers Markdown
- **Tests**: 4 fichiers Python + 1 vérification
- **Exemples**: Fichiers Excel et CSV générés

## Statut

- **Version**: 3.0
- **Date**: 11 février 2026
- **Tests**: 40/40 passés
- **Statut**: Production Ready

## Développeur

**TATCHIDA Louis**
- MSc Agronomie
- MSc Ingénierie Financière adaptée à l'Agriculture
- Data Analyst

## Licence

Dashboard développé pour ProSMAT - Mission de Suivi des Coopératives Agricoles au Togo

© 2025 - Tous droits réservés

---

**Prêt à l'emploi! Consultez LISEZ_MOI_DABORD.md pour commencer.**
