# Dashboard SIG ProSMAT - Documentation Complète

## Vue d'Ensemble

Dashboard interactif de suivi des coopératives agricoles au Togo avec analyses avancées de data science pour le développement du marché agroécologique.

**Version** : 3.0 
**Date** : 11 février 2026 
**Statut** : Production Ready 

---

## Données

- **232 coopératives** géolocalisées
- **5 régions** : Centre, Kara, Maritime, Plateaux, Savanes
- **16 préfectures** actives
- **37 communes** actives
- **178 villages** uniques
- **6173 membres** au total

---

## Installation et Lancement

### Prérequis
```bash
Python 3.8+
pip install -r requirements.txt
```

### Lancement
```bash
streamlit run dashboard_sig_streamlit.py
```

Le dashboard s'ouvrira automatiquement dans votre navigateur à `http://localhost:8501`

---

## Fonctionnalités

### Onglet 1 : Carte Folium Interactive
- Carte interactive avec marqueurs par région
- Clusters de coopératives
- Carte de chaleur
- Popups détaillés
- Contrôles de couches
- Export possible

### Onglet 2 : Cartes SIG Statiques (13 types)
1. **Localisation** - Points des coopératives
2. **Choroplèthe Coopératives** - Nombre par région
3. **Choroplèthe Effectif** - Effectif total par région
4. **Choroplèthe Femmes** - Nombre de femmes par région
5. **Choroplèthe Jeunes** - Nombre de jeunes par région
6. **Choroplèthe Handicapés** - Personnes handicapées par région
7. **Immatriculation** - Statut d'immatriculation
8. **Engagement Agroécologique** - Engagement des coopératives
9. **Parcelle d'Apprentissage** - Parcelles choisies
10. **Matériel de Production** - Matériel reçu
11. **Taille Proportionnelle** - Effectif visualisé par taille
12. **Zoom sur Région** - Détails par préfecture et commune
13. **Zoom Personnalisé** - Zoom manuel

### Onglet 3 : Analyses Data Science
- **Distribution** : Graphiques de répartition
- **Corrélations** : Matrices de corrélation
- **Indicateurs** : KPIs et métriques
- **Tendances** : Graphique Sunburst hiérarchique

### Onglet 4 : Marché Agroécologique NOUVEAU
- **Top 10 Coopératives** : Scoring multi-critères (0-100)
- **Cultures Dominantes** : 89 cultures identifiées
- **Analyse par Région** : Top 5 cultures par région
- **Recommandations** : Stratégies de développement
- **Export CSV** : Résultats téléchargeables

### Onglet 5 : Données
- Tableau filtrable
- Recherche par coopérative
- Export CSV
- Statistiques résumées

---

## Onglet Marché Agroécologique - Guide Rapide

### Scoring Multi-Critères

**8 Critères Évalués** :
1. Engagement agroécologique (20%)
2. Effectif total (15%)
3. Immatriculation (15%)
4. Restitution formation (15%)
5. Parcelle d'apprentissage (10%)
6. Production contre-saison (10%)
7. Taux de féminisation (7.5%)
8. Taux de jeunes (7.5%)

**Score Total** : 0-100 (moyenne pondérée)

### Cultures Dominantes

**Top 10 Cultures** :
1. Gombo - 97 mentions
2. Gboma - 58 mentions
3. Tomate/Tomates - 94 mentions
4. Oignons - 38 mentions
5. Piment - 71 mentions
6. Choux - 26 mentions
7. Ademe - 23 mentions
8. Laitue - 23 mentions
9. Carottes - 15 mentions
10. Concombre - 12 mentions

### Utilisation

1. **Identifier les coopératives prioritaires**
 - Consulter le Top 10
 - Vérifier les scores >70
 - Analyser les profils détaillés

2. **Planifier les cultures**
 - Consulter "Cultures par Région"
 - Identifier les 3 cultures dominantes
 - Planifier les formations

3. **Exporter les résultats**
 - Télécharger Top 10 (CSV)
 - Télécharger Cultures (CSV)
 - Utiliser pour reporting

---

## Zoom par Région - Guide Rapide

### Fonctionnalités

Quand vous zoomez sur une région :

1. **Carte Améliorée**
 - Préfectures colorées selon nb de coopératives
 - Coopératives colorées par préfecture
 - Labels enrichis
 - Légende interactive

2. **Statistiques par Préfecture**
 - Tableau détaillé
 - Graphique en barres
 - Tri par nombre de coopératives

3. **Statistiques par Commune**
 - Tableau hiérarchique
 - Filtre par préfecture
 - Top 10 communes

4. **Indicateurs de Performance**
 - Taux de féminisation (%)
 - Taux de jeunes (%)
 - Effectif moyen

5. **Liste Détaillée**
 - Toutes les coopératives
 - Filtre multi-sélection
 - Export possible

---

## Structure du Projet

```
.
 dashboard_sig_streamlit.py # Application principale
 map_styles.py # Styles des cartes
 map_utils.py # Utilitaires cartographiques
 gadm41_TGO.gpkg # Données géographiques GADM
 MISSION_DE_SUIVI_cleaned.xlsx # Données des coopératives
 requirements.txt # Dépendances Python

 Documentation/
 README_COMPLET.md # Ce fichier
 GUIDE_MARCHE_AGROECOLOGIQUE.md
 GUIDE_UTILISATION_ZOOM.md
 RESUME_FINAL.md
 CHANGELOG_V3.md
 CORRECTIONS_FINALES.md
 ...

 Tests/
 test_final.py
 test_architecture.py
 test_zoom_region.py
 test_marche_agroecologique.py
```

---

## Tests

### Exécuter Tous les Tests
```bash
python test_final.py
```

### Tests Spécifiques
```bash
# Test de l'architecture
python test_architecture.py

# Test du zoom par région
python test_zoom_region.py

# Test du marché agroécologique
python test_marche_agroecologique.py
```

### Résultats Attendus
- 232 coopératives chargées
- 16 préfectures, 37 communes
- 5 régions
- Tous les graphiques fonctionnels

---

## Documentation Détaillée

### Guides Utilisateur
- `GUIDE_MARCHE_AGROECOLOGIQUE.md` - Guide complet de l'onglet Marché
- `GUIDE_UTILISATION_ZOOM.md` - Guide du zoom par région
- `README_DASHBOARD.md` - Documentation générale

### Documentation Technique
- `CHANGEMENTS_ARCHITECTURE.md` - Changements d'architecture
- `AMELIORATIONS_ZOOM_REGION.md` - Détails du zoom
- `CORRECTIONS_FINALES.md` - Corrections apportées

### Notes de Version
- `CHANGELOG_V3.md` - Version 3.0
- `NOTES_VERSION.md` - Notes détaillées
- `RESUME_FINAL.md` - Résumé global

---

## Cas d'Usage

### 1. Sélection pour Programme Pilote

**Objectif** : Identifier 5 coopératives pour un programme pilote

**Démarche** :
1. Aller dans "Marché Agroécologique"
2. Consulter le Top 10
3. Sélectionner les 5 premières avec score >80
4. Vérifier la répartition géographique
5. Consulter les profils détaillés

### 2. Planification des Cultures

**Objectif** : Décider quelles cultures promouvoir dans une région

**Démarche** :
1. Aller dans "Marché Agroécologique"
2. Consulter "Cultures par Région"
3. Identifier les 3 cultures dominantes
4. Vérifier la demande globale (Top 20)
5. Planifier les formations

### 3. Analyse Régionale

**Objectif** : Analyser en détail une région

**Démarche** :
1. Aller dans "Cartes SIG"
2. Sélectionner "Zoom sur une Région"
3. Choisir la région
4. Explorer les statistiques par préfecture
5. Analyser les indicateurs de performance

---

## Configuration

### Filtres Disponibles

**Localisation** :
- Région
- Préfecture (GADM)
- Commune
- Village

**Agent** :
- CRP (Conseiller Rural de Proximité)

**Statuts** :
- Immatriculation
- Restitution formation
- Engagement agroécologique
- Parcelle choisie
- Production contre-saison
- Matériel reçu

### Export

**Formats disponibles** :
- PNG (cartes)
- CSV (données)
- Excel (données complètes)

---

## Indicateurs Clés

### Inclusion
- **Taux de féminisation** : 58% en moyenne
- **Taux de jeunes** : 40% en moyenne
- **Personnes handicapées** : 2% de l'effectif

### Structuration
- **Immatriculées** : 62.2%
- **Restitution formation** : 95.1%
- **Production contre-saison** : 92.1%

### Taille
- **Effectif moyen** : 25.6 membres/coopérative
- **Plus petite** : 5 membres
- **Plus grande** : 80+ membres

---

## Points d'Attention

### Données Manquantes
- 3% sans préfecture (7 coopératives)
- 8.6% sans commune (20 coopératives)
- 0% sans village (toutes renseignées)

### Correspondance GADM
Différences d'orthographe pour 3 préfectures :
- Agoé-Nyivé ≠ Agoe-Nyive
- Tchaoudjo ≠ Tchaudjo
- Tandjoaré (non trouvé)

### Recommandations
1. Normaliser les noms de préfectures
2. Compléter les communes manquantes
3. Vérifier la cohérence géographique

---

## Évolutions Futures

### Court Terme
- [ ] Export PDF des cartes
- [ ] Rapports automatiques par région
- [ ] Graphiques de tendance temporelle

### Moyen Terme
- [ ] Intégration base de données
- [ ] API REST
- [ ] Dashboard mobile

### Long Terme
- [ ] Machine Learning pour prédictions
- [ ] Clustering géographique
- [ ] Système de recommandation

---

## Technologies Utilisées

- **Python 3.x** - Langage principal
- **Streamlit** - Framework web
- **Pandas** - Manipulation de données
- **GeoPandas** - Données géospatiales
- **Plotly** - Graphiques interactifs
- **Folium** - Cartes interactives
- **Matplotlib** - Visualisations statiques
- **GADM** - Données géographiques

---

## Support

### En Cas de Problème

1. **Vérifier les logs** : Consulter la console Streamlit
2. **Exécuter les tests** : `python test_final.py`
3. **Consulter la documentation** : Voir les guides `.md`
4. **Vérifier les données** : S'assurer que le fichier Excel est présent

### Erreurs Courantes

**Erreur** : Module not found 
**Solution** : `pip install -r requirements.txt`

**Erreur** : Fichier Excel non trouvé 
**Solution** : Vérifier que `MISSION_DE_SUIVI_cleaned.xlsx` est présent

**Erreur** : Fichier GADM non trouvé 
**Solution** : Vérifier que `gadm41_TGO.gpkg` est présent

---

## Contributeurs

- **Développement** : Kiro AI Assistant
- **Projet** : ProSMAT 2025
- **Date** : 11 février 2026

---

## Changelog

### Version 3.0 (11 février 2026)
- Ajout onglet Marché Agroécologique
- Scoring multi-critères des coopératives
- Analyse des cultures dominantes (89 cultures)
- Recommandations stratégiques
- Export CSV des résultats

### Version 2.0 (11 février 2026)
- Adaptation architecture Préfecture/Commune
- Amélioration zoom par région (7 graphiques)
- Correction bug Sunburst
- Documentation complète

### Version 1.0 (Avant)
- Fonctionnalités de base
- Architecture avec Canton
- Zoom simple par région

---

## Checklist de Production

Avant déploiement :

- [x] Tous les tests passent
- [x] Aucune erreur dans les logs
- [x] Tous les onglets fonctionnels
- [x] Tous les graphiques s'affichent
- [x] Filtres dynamiques opérationnels
- [x] Export CSV fonctionnel
- [x] Documentation complète
- [x] Données à jour

---

## Conclusion

Le Dashboard SIG ProSMAT Version 3.0 est un **outil complet d'aide à la décision** pour :
- Suivre les coopératives agricoles
- Identifier les coopératives à fort potentiel
- Analyser les cultures dominantes
- Planifier les interventions
- Développer le marché agroécologique

**Statut** : Production Ready 
**Le dashboard est prêt pour la production !** 

---

*Développé avec pour ProSMAT 2025*
