# Guide de Démarrage Rapide - Dashboard SIG ProSMAT

## En 3 Étapes

### 1⃣ Lancer le Dashboard
```bash
streamlit run dashboard_sig_streamlit.py
```

Le dashboard s'ouvre automatiquement dans votre navigateur à l'adresse: `http://localhost:8501`

### 2⃣ Explorer les Onglets

#### Carte Folium Interactive
- Carte interactive avec zoom et déplacement
- Cliquez sur les marqueurs pour voir les détails
- Utilisez le panneau de couches (en haut à droite) pour activer/désactiver les visualisations
- Cochez "Afficher carte de chaleur" pour voir la densité

#### Cartes SIG Statiques
- Sélectionnez le type de carte dans le menu déroulant
- Utilisez le slider "Niveau de zoom" pour zoomer (1-5)
- **Pour le zoom région**: Sélectionnez "Zoom sur une Région" puis choisissez la région
- Téléchargez la carte en PNG avec le bouton en bas

#### Analyses Data Science
- 4 sous-onglets: Distribution, Corrélations, Indicateurs, Tendances
- Graphiques interactifs (survolez pour voir les détails)
- Indicateurs de performance avec jauges

#### Marché Agroécologique NOUVEAU
- **Top 10 par Région**: Cliquez sur l'onglet de la région souhaitée
- **Toutes les Régions**: Vue globale avec filtres
- **Exports**: Téléchargez Excel (multi-feuilles) ou CSV
- **Cultures**: Voir les cultures dominantes et leur répartition

#### Données
- Tableau filtré avec toutes les données
- Recherche par nom de coopérative
- Export CSV

### 3⃣ Utiliser les Filtres

#### Sidebar (Barre Latérale Gauche)
1. **Localisation**: Région → Préfecture → Commune → Village
2. **Agent CRP**: Filtrer par agent de terrain
3. **Statuts**: Immatriculation, Formation, Engagement, etc.
4. **Effectif**: Slider pour filtrer par taille
5. **Reset**: Bouton pour réinitialiser tous les filtres

#### Filtres Spécifiques
- **Zoom Région**: Filtre par préfecture dans la liste des coopératives
- **Marché Agroécologique**: Filtre par région(s) et score minimum dans l'onglet "Toutes les Régions"

---

## Cas d'Usage Courants

### Trouver les Meilleures Coopératives pour le Marché
1. Aller dans l'onglet "Marché Agroécologique"
2. Cliquer sur l'onglet de la région souhaitée
3. Voir le Top 10 avec les scores
4. Cliquer sur "Voir les détails" pour les profils complets
5. Télécharger l'Excel pour partager

### Analyser une Région Spécifique
1. Dans la sidebar, sélectionner la région
2. Aller dans "Cartes SIG Statiques"
3. Sélectionner "Zoom sur une Région"
4. Explorer les statistiques par préfecture et commune
5. Télécharger la carte en PNG

### Identifier les Cultures Populaires
1. Aller dans "Marché Agroécologique"
2. Descendre jusqu'à "Cultures Dominantes et Tendances"
3. Voir le Top 20 et le graphique de bulles
4. Consulter les cultures par région
5. Télécharger le CSV des cultures

### Exporter des Données
1. **Carte**: Bouton "Télécharger la carte (PNG)" sous chaque carte SIG
2. **Top 10**: Boutons dans l'onglet "Marché Agroécologique"
 - Excel: Fichier avec 6 feuilles (1 par région + 1 globale)
 - CSV: Fichier simple pour analyse rapide
3. **Données**: Bouton "Télécharger CSV" dans l'onglet "Données"

---

## Astuces

### Performance
- Les données sont mises en cache → Rechargement rapide
- Utilisez les filtres pour réduire le nombre de coopératives affichées
- Les graphiques Plotly sont interactifs (zoom, pan, export)

### Navigation
- Les KPIs en haut se mettent à jour automatiquement avec les filtres
- Le compteur dans la sidebar montre le nombre de coopératives filtrées
- Les onglets gardent leur état lors de la navigation

### Visualisation
- **Carte Folium**: Meilleure pour l'exploration interactive
- **Cartes SIG**: Meilleures pour les exports et présentations
- **Graphiques Plotly**: Interactifs, survolez pour voir les détails

### Exports
- **PNG**: Haute résolution (200 DPI) pour rapports
- **Excel**: Multi-feuilles pour analyse approfondie
- **CSV**: Format simple pour import dans d'autres outils

---

## Dépannage

### Le dashboard ne se lance pas
```bash
# Vérifier que vous êtes dans le bon dossier
cd "D:\ProSMAT\Analyse projet"

# Activer l'environnement virtuel
.venv\Scripts\activate

# Lancer le dashboard
streamlit run dashboard_sig_streamlit.py
```

### Erreur "Module not found"
```bash
# Installer les dépendances
pip install -r requirements.txt
```

### Les données ne s'affichent pas
- Vérifier que `MISSION_DE_SUIVI_cleaned.xlsx` est dans le dossier
- Vérifier que `gadm41_TGO.gpkg` est dans le dossier
- Réinitialiser les filtres avec le bouton "Reset"

### La carte est vide
- Vérifier les filtres (peut-être trop restrictifs)
- Cliquer sur "Réinitialiser tous les filtres"
- Vérifier que les coordonnées GPS sont valides

---

## Interprétation des Scores (Marché Agroécologique)

### Score Total (0-100)
- **90-100**: Excellent potentiel - Prêt pour le marché
- **70-89**: Bon potentiel - Accompagnement léger
- **50-69**: Potentiel moyen - Renforcement nécessaire
- **<50**: Potentiel faible - Formation intensive

### Critères de Scoring
1. **Engagement Agroécologique (20%)**: Engagement ferme pris
2. **Effectif Total (15%)**: Taille de la coopérative
3. **Immatriculation (15%)**: Structure légale formalisée
4. **Restitution Formation (15%)**: Transfert de connaissances
5. **Parcelle d'Apprentissage (10%)**: Infrastructure disponible
6. **Production Contre-Saison (10%)**: Capacité diversifiée
7. **Taux de Féminisation (7.5%)**: Inclusion des femmes (>50% = bonus)
8. **Taux de Jeunes (7.5%)**: Dynamisme et relève (>30% = bonus)

---

## Aide

### Documentation Complète
- `README_COMPLET.md` - Documentation exhaustive
- `GUIDE_UTILISATION_ZOOM.md` - Guide du zoom région
- `GUIDE_MARCHE_AGROECOLOGIQUE.md` - Guide de l'onglet Marché
- `SYNTHESE_FINALE_V3.md` - Synthèse technique

### Fichiers de Test
- `test_final.py` - Test global
- `test_marche_top10_regions.py` - Test Marché

### Support Technique
- Consulter les fichiers de documentation
- Vérifier les tests pour des exemples d'utilisation
- Lire les notes de version dans `CHANGELOG_V3.md`

---

## Fonctionnalités Clés

### Cartographie
- 13 types de cartes différentes
- Zoom par région avec détails par préfecture
- Export PNG haute résolution

### Analyses
- Scoring multi-critères (8 dimensions)
- Top 10 par région (50 coopératives)
- Analyse des cultures (89 uniques)

### Exports
- Excel multi-feuilles (1 par région)
- CSV global et par culture
- PNG haute résolution

### Filtres
- Hiérarchie géographique (4 niveaux)
- Statuts multiples
- Effectif (slider)
- Reset rapide

---

** Bon usage du Dashboard SIG ProSMAT!**

Pour toute question, consulter la documentation complète ou les fichiers de test.
