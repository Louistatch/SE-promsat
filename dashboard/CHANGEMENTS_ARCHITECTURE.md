# Changements d'Architecture - Préfecture et Commune

## Résumé des modifications

Le fichier Excel `MISSION_DE_SUIVI_cleaned.xlsx` a été mis à jour avec une nouvelle architecture géographique :

### Anciennes colonnes
- `2.4. Canton` → utilisée pour les subdivisions administratives

### Nouvelles colonnes
- `prefectures` → niveau administratif 2 (préfecture)
- `Commune` → niveau administratif 3 (commune)

## Modifications apportées au code

### 1. dashboard_sig_streamlit.py

#### Mapping des colonnes (ligne ~183)
```python
column_mapping = {
 '2.1. Région': 'region',
 'prefectures': 'prefecture', # NOUVELLE COLONNE
 'Commune': 'commune', # NOUVELLE COLONNE
 '2.4. Canton': 'canton', # Ancienne colonne (pour compatibilité)
 ...
}
```

#### Colonnes requises (ligne ~213)
Ajout de `'prefecture'` et `'commune'` dans la liste des colonnes requises.

#### Popup de la carte Folium (ligne ~366)
Ajout de l'affichage de la préfecture et de la commune dans les popups des marqueurs.

#### Statistiques par préfecture (lignes ~448, ~777, ~834, ~1169, ~1621)
Remplacement de `groupby('canton')` par `groupby('prefecture')` pour calculer les statistiques.

#### Filtres de la sidebar (ligne ~1307)
- Remplacement du filtre "Canton" par "Commune"
- Variable `selected_canton` → `selected_commune`
- Logique de filtrage adaptée pour utiliser la colonne `'commune'`

#### Application des filtres (ligne ~1387)
Remplacement de `df_filtered['canton']` par `df_filtered['commune']`

#### Tableaux d'affichage (lignes ~1650, ~1915)
- Ajout des colonnes `'prefecture'` et `'commune'` dans les tableaux
- Remplacement de `'canton'` par `'prefecture'` et `'commune'`

#### Graphiques interactifs (lignes ~1732, ~1901)
- Scatter plot : ajout de `'prefecture'` et `'commune'` dans hover_data
- Sunburst : hiérarchie mise à jour : `['region', 'prefecture', 'commune', 'cooperative']`

#### Statistiques de téléchargement (ligne ~1955)
Ajout de `"Préfectures"` et `"Communes"` dans les statistiques JSON.

## État des données

### Préfectures dans le fichier Excel
16 préfectures uniques :
- Agoé-Nyivé, Assoli, Bas-Mono, Blitta, Cinkassé, Dankpen, Danyi, Est-Mono, Golfe, Kozah, Lacs, Ogou, Tandjoaré, Tchamba, Tchaoudjo, Tône

### Communes dans le fichier Excel
38 communes uniques (certaines valeurs sont NaN)

### Correspondance avec GADM
 Attention : Il y a des différences d'orthographe entre les préfectures du fichier Excel et celles du fichier GADM :
- Excel: "Agoé-Nyivé" vs GADM: "Agoe-Nyive"
- Excel: "Tchaoudjo" vs GADM: "Tchaudjo"

Ces différences peuvent affecter les jointures spatiales et les statistiques par préfecture basées sur GADM.

## Compatibilité

Le code conserve la colonne `'canton'` dans le mapping pour assurer la compatibilité avec d'anciennes versions du fichier Excel, mais elle n'est plus utilisée dans les filtres et affichages principaux.

## Tests recommandés

1. Vérifier que tous les filtres fonctionnent correctement
2. Vérifier que les statistiques par préfecture s'affichent correctement
3. Vérifier que les popups de la carte affichent bien préfecture et commune
4. Vérifier que les graphiques interactifs incluent les nouvelles colonnes
5. Tester le téléchargement des données filtrées

## Date de modification
11 février 2026
