# BIENVENUE - Dashboard SIG ProSMAT v3.0

## Vous êtes au bon endroit!

Ce dashboard vous permet d'analyser les coopératives agricoles au Togo avec des outils avancés de cartographie et de data science.

---

## DÉMARRAGE RAPIDE

### 1. Lancer le Dashboard
```bash
streamlit run dashboard_sig_streamlit.py
```

### 2. Ouvrir dans le Navigateur
Le dashboard s'ouvre automatiquement à: `http://localhost:8501`

### 3. Explorer!
- 5 onglets disponibles
- Filtres dans la barre latérale gauche
- Exports disponibles (PNG, Excel, CSV)

---

## DOCUMENTATION

### Pour Commencer
1. **GUIDE_DEMARRAGE_RAPIDE.md** - Commencez ici!
 - Lancement en 3 étapes
 - Cas d'usage courants
 - Astuces et dépannage

### Guides Utilisateur
2. **GUIDE_UTILISATION_ZOOM.md** - Comment utiliser le zoom par région
3. **GUIDE_MARCHE_AGROECOLOGIQUE.md** - Guide de l'onglet Marché (Top 10 par région)

### Documentation Complète
4. **README_COMPLET.md** - Documentation exhaustive du projet
5. **SYNTHESE_FINALE_V3.md** - Synthèse technique complète

### Notes de Version
6. **CHANGELOG_V3.md** - Nouveautés de la version 3.0

---

## NOUVEAUTÉS v3.0

### Onglet Marché Agroécologique
- **Top 10 par Région**: 5 régions × 10 coopératives = 50 coopératives identifiées
- **Scoring Multi-Critères**: 8 dimensions, score de 0 à 100
- **Exports**: Excel multi-feuilles (1 par région) + CSV
- **Analyse des Cultures**: 89 cultures uniques, 668 mentions

### Zoom Région Amélioré
- Carte choroplèthe par préfecture
- 7 nouveaux graphiques et tableaux
- Indicateurs de performance (féminisation, jeunes, effectif moyen)
- Graphiques radar pour Top 5 coopératives

### Architecture Préfecture/Commune
- Hiérarchie à 4 niveaux: Région → Préfecture → Commune → Village
- 16 préfectures, 37 communes
- Filtres adaptés

---

## FONCTIONNALITÉS PRINCIPALES

### Cartographie
- **Carte Interactive**: Folium avec clusters et heatmap
- **13 Types de Cartes**: Choroplèthe, localisation, statuts, etc.
- **Zoom Région**: Détails par préfecture et commune
- **Export PNG**: Haute résolution (200 DPI)

### Analyses
- **Distribution**: Par région, effectif, etc.
- **Corrélations**: Scatter plots, matrices
- **Indicateurs**: Jauges de performance
- **Tendances**: Graphiques radar, sunburst

### Marché Agroécologique
- **Scoring**: 8 critères pondérés
- **Top 10**: Par région avec profils détaillés
- **Cultures**: Analyse des cultures dominantes
- **Recommandations**: Stratégies pour le marché

### Exports
- **Excel**: Multi-feuilles (1 par région)
- **CSV**: Format simple
- **PNG**: Cartes haute résolution

### Filtres
- **Géographiques**: Région, Préfecture, Commune, Village
- **Statuts**: Immatriculation, Formation, Engagement, etc.
- **Effectif**: Slider pour filtrer par taille
- **Reset**: Réinitialisation rapide

---

## DONNÉES

### Coopératives
- **Total**: 232 coopératives (avec coordonnées GPS valides)
- **Régions**: 5 (Centre, Kara, Maritime, Plateaux, Savanes)
- **Préfectures**: 16
- **Communes**: 37
- **Villages**: 178

### Répartition
- **Centre**: 37 coopératives
- **Kara**: 53 coopératives
- **Maritime**: 52 coopératives
- **Plateaux**: 30 coopératives
- **Savanes**: 60 coopératives

---

## CAS D'USAGE

### 1. Identifier les Coopératives à Fort Potentiel
→ Onglet "Marché Agroécologique" → Sélectionner la région → Voir le Top 10

### 2. Analyser une Région
→ Filtrer par région → Onglet "Cartes SIG" → "Zoom sur une Région"

### 3. Exporter des Données
→ Onglet "Marché Agroécologique" → Bouton "Télécharger Excel"

### 4. Voir les Cultures Populaires
→ Onglet "Marché Agroécologique" → Section "Cultures Dominantes"

---

## PRÉREQUIS

### Fichiers Nécessaires
- `MISSION_DE_SUIVI_cleaned.xlsx` - Données des coopératives
- `gadm41_TGO.gpkg` - Données géographiques du Togo
- `logo.jfif` - Logo (optionnel)

### Modules Python
- `dashboard_sig_streamlit.py` - Application principale
- `map_styles.py` - Styles et couleurs
- `map_utils.py` - Utilitaires cartographiques

### Packages
Voir `requirements.txt` pour la liste complète:
- streamlit
- pandas
- geopandas
- folium
- plotly
- matplotlib
- seaborn

---

## TESTS

### Lancer les Tests
```bash
# Test global
python test_final.py

# Test Marché Agroécologique
python test_marche_top10_regions.py
```

### Fichiers de Test
- `test_final.py` - Test global du dashboard
- `test_marche_top10_regions.py` - Test Top 10 par région
- `test_architecture.py` - Test architecture Préfecture/Commune
- `test_zoom_region.py` - Test zoom région

### Résultats Attendus
 Tous les tests doivent passer
 Fichiers générés: `test_export_top10_regions.xlsx` et `.csv`

---

## ASTUCES

### Performance
- Les données sont mises en cache → Rechargement rapide
- Utilisez les filtres pour réduire le nombre de coopératives
- Les graphiques Plotly sont interactifs

### Navigation
- Les KPIs en haut se mettent à jour avec les filtres
- Le compteur dans la sidebar montre le nombre de coopératives filtrées
- Les onglets gardent leur état

### Exports
- **PNG**: Pour rapports et présentations
- **Excel**: Pour analyse approfondie (6 feuilles)
- **CSV**: Pour import dans d'autres outils

---

## AIDE

### Problèmes Courants

#### Le dashboard ne se lance pas
```bash
# Vérifier le dossier
cd "D:\ProSMAT\Analyse projet"

# Activer l'environnement
.venv\Scripts\activate

# Lancer
streamlit run dashboard_sig_streamlit.py
```

#### Erreur "Module not found"
```bash
pip install -r requirements.txt
```

#### Les données ne s'affichent pas
- Vérifier que les fichiers Excel et GPKG sont présents
- Réinitialiser les filtres (bouton "Reset")
- Vérifier les coordonnées GPS

### Documentation
- **GUIDE_DEMARRAGE_RAPIDE.md** - Guide complet
- **README_COMPLET.md** - Documentation exhaustive
- **SYNTHESE_FINALE_V3.md** - Synthèse technique

---

## SUPPORT

### Fichiers de Documentation (19 fichiers)
1. LISEZ_MOI_DABORD.md (ce fichier)
2. GUIDE_DEMARRAGE_RAPIDE.md
3. GUIDE_UTILISATION_ZOOM.md
4. GUIDE_MARCHE_AGROECOLOGIQUE.md
5. README_COMPLET.md
6. SYNTHESE_FINALE_V3.md
7. CHANGELOG_V3.md
8. CHANGEMENTS_ARCHITECTURE.md
9. AMELIORATIONS_ZOOM_REGION.md
10. CORRECTIONS_FINALES.md
11. CORRECTION_SUNBURST.md
12. CORRECTION_IMPORT_PX.md
13. RESUME_ONGLET_MARCHE.md
14. RESUME_ADAPTATION.md
15. RESUME_FINAL.md
16. NOTES_VERSION.md
17. README_DASHBOARD.md
18. README_STYLES.md
19. AMELIORATIONS_CARTE_SIG.md

### Fichiers de Test (4 fichiers)
1. test_final.py
2. test_marche_top10_regions.py
3. test_architecture.py
4. test_zoom_region.py

---

## CHECKLIST DE DÉMARRAGE

- [ ] Fichiers présents: `MISSION_DE_SUIVI_cleaned.xlsx` et `gadm41_TGO.gpkg`
- [ ] Packages installés: `pip install -r requirements.txt`
- [ ] Dashboard lancé: `streamlit run dashboard_sig_streamlit.py`
- [ ] Navigateur ouvert: `http://localhost:8501`
- [ ] Filtres testés dans la sidebar
- [ ] Onglets explorés (5 onglets)
- [ ] Export testé (Excel ou CSV)

---

## PRÊT À COMMENCER!

1. **Lisez** le GUIDE_DEMARRAGE_RAPIDE.md
2. **Lancez** le dashboard avec `streamlit run dashboard_sig_streamlit.py`
3. **Explorez** les 5 onglets
4. **Filtrez** les données dans la sidebar
5. **Exportez** vos résultats (Excel, CSV, PNG)

---

**Version**: 3.0  
**Date**: 11 février 2026  
**Statut**: Production Ready

---

## DÉVELOPPEUR

**TATCHIDA Louis**
- MSc Agronomie
- MSc Ingénierie Financière adaptée à l'Agriculture
- Data Analyst

Dashboard développé pour ProSMAT - Mission de Suivi des Coopératives Agricoles au Togo

© 2025 - Tous droits réservés

---

**Bon usage du Dashboard SIG ProSMAT!**
