# Guide d'Utilisation - Zoom par Région avec Détails par Préfecture

## Vue d'Ensemble

La fonctionnalité de zoom par région a été considérablement améliorée pour offrir une analyse détaillée à plusieurs niveaux : région → préfecture → commune → coopérative.

## Comment Utiliser

### Étape 1 : Accéder au Zoom par Région

1. Lancez le dashboard : `streamlit run dashboard_sig_streamlit.py`
2. Allez dans l'onglet **"Cartes SIG"**
3. Dans le sélecteur "Type de carte", choisissez **"Zoom sur une Région"**
4. Un nouveau sélecteur apparaît : **"Région à zoomer"**
5. Choisissez la région que vous souhaitez analyser

### Étape 2 : Explorer la Carte

La carte affiche :
- **Fond coloré** : Chaque préfecture est colorée selon le nombre de coopératives (dégradé jaune-orange-rouge)
- **Points colorés** : Chaque préfecture a sa propre couleur pour ses coopératives
- **Labels** : Nom de la préfecture + nombre de coopératives
- **Légende** : Liste de toutes les préfectures avec leur nombre de coopératives

### Étape 3 : Analyser les Statistiques

#### Métriques Globales (en haut)
4 indicateurs clés pour la région :
- Nombre total de coopératives
- Effectif total
- Nombre de femmes
- Nombre de jeunes

#### Détails par Préfecture
**Tableau** (gauche) :
- Liste de toutes les préfectures
- Nombre de coopératives, effectif, femmes, jeunes, handicapés
- Trié par nombre de coopératives (décroissant)

**Graphique** (droite) :
- Barres : nombre de coopératives par préfecture
- Couleur : intensité selon l'effectif total
- Interactif : survolez pour voir les détails

#### Détails par Commune
**Filtre** :
- Sélecteur pour filtrer par préfecture
- Option "Toutes" pour voir toutes les communes

**Tableau** (gauche) :
- Hiérarchie Préfecture → Commune
- Statistiques par commune

**Graphique** (droite) :
- Top 10 des communes
- Couleur par préfecture d'appartenance

#### Indicateurs de Performance
3 graphiques côte à côte :

1. **Taux de Féminisation** (gauche)
 - % de femmes par rapport à l'effectif total
 - Échelle rouge-jaune-vert

2. **Taux de Jeunes** (centre)
 - % de jeunes (<35 ans) par rapport à l'effectif total
 - Échelle bleue

3. **Effectif Moyen** (droite)
 - Nombre moyen de membres par coopérative
 - Échelle orange

#### Liste Détaillée des Coopératives
**Filtre multi-sélection** :
- Cochez une ou plusieurs préfectures
- Le tableau se met à jour automatiquement

**Tableau complet** :
- Toutes les informations de chaque coopérative
- Colonnes : Coopérative, Préfecture, Commune, Village, Effectif, Femmes, Jeunes, Immatricule, Engagement AE

## Exemples d'Analyse

### Exemple 1 : Analyser la Région Savanes

**Résultats attendus** :
- 60 coopératives, 2230 membres
- 3 préfectures : Tône (47), Cinkassé (7), Tandjoaré (6)
- Taux de féminisation élevé : ~65%
- Taux de jeunes très élevé : ~52%
- Effectif moyen : 37 membres/coopérative

**Insights** :
- Tône domine largement avec 78% des coopératives
- Forte présence de jeunes et de femmes
- Coopératives de taille moyenne à grande

### Exemple 2 : Comparer les Préfectures de la Région Kara

**Résultats attendus** :
- Assoli : 43 coopératives (81% de la région)
- Kozah : 9 coopératives
- Dankpen : 1 coopérative

**Insights** :
- Assoli est la préfecture dominante
- Taux de féminisation très élevé à Assoli (68%)
- Effectif moyen élevé à Assoli (34.5 membres)

### Exemple 3 : Explorer les Communes de la Région Maritime

**Résultats attendus** :
- 4 préfectures, 12 communes
- Top communes : Golfe 6 (11), Golfe 1 (9), Lacs 1 (8)
- Répartition équilibrée entre les préfectures

**Insights** :
- Golfe concentre le plus de coopératives
- Taux de féminisation très élevé à Bas-Mono (77%)
- Coopératives de petite taille (10-19 membres)

## Interprétation des Couleurs

### Sur la Carte
- **Blanc/Jaune clair** : Peu de coopératives (0-5)
- **Orange** : Nombre moyen de coopératives (5-15)
- **Rouge foncé** : Beaucoup de coopératives (>15)

### Points des Coopératives
- Chaque préfecture a une couleur unique
- Permet d'identifier rapidement l'appartenance géographique

### Graphiques d'Indicateurs
- **Taux de Féminisation** : Rouge (faible) → Jaune (moyen) → Vert (élevé)
- **Taux de Jeunes** : Bleu clair (faible) → Bleu foncé (élevé)
- **Effectif Moyen** : Orange clair (petit) → Orange foncé (grand)

## Conseils d'Utilisation

### Pour une Analyse Rapide
1. Regardez d'abord les métriques globales
2. Consultez le tableau des préfectures
3. Identifiez les préfectures dominantes

### Pour une Analyse Approfondie
1. Explorez le graphique de répartition par préfecture
2. Filtrez les communes par préfecture
3. Analysez les indicateurs de performance
4. Consultez la liste détaillée avec filtres

### Pour Comparer les Régions
1. Zoomez sur la première région
2. Notez les statistiques clés
3. Changez de région dans le sélecteur
4. Comparez les indicateurs

## Indicateurs Clés à Surveiller

### Nombre de Coopératives
- Indique la densité d'activité dans la préfecture
- Permet d'identifier les zones prioritaires

### Taux de Féminisation
- Objectif : >50% pour une bonne inclusion
- Indicateur d'équité de genre

### Taux de Jeunes
- Objectif : >30% pour assurer la relève
- Indicateur de dynamisme

### Effectif Moyen
- Petite coopérative : <20 membres
- Moyenne : 20-40 membres
- Grande : >40 membres

## Cas d'Usage Pratiques

### Planification d'Interventions
1. Identifiez les préfectures avec peu de coopératives
2. Analysez les taux de féminisation et de jeunes
3. Priorisez les zones à renforcer

### Suivi de Performance
1. Comparez les effectifs moyens entre préfectures
2. Identifiez les préfectures performantes
3. Analysez les facteurs de succès

### Reporting
1. Exportez la carte (bouton "Télécharger")
2. Copiez les tableaux de statistiques
3. Utilisez les graphiques pour les présentations

## Points d'Attention

### Données Manquantes
- 3% des coopératives sans préfecture renseignée
- 8.6% sans commune renseignée
- Ces coopératives apparaissent comme "Non renseigné"

### Correspondance GADM
Certaines préfectures ont des orthographes différentes :
- Excel : "Agoé-Nyivé" → GADM : "Agoe-Nyive"
- Excel : "Tchaoudjo" → GADM : "Tchaudjo"
- Excel : "Tandjoaré" → Non trouvé dans GADM

Cela peut affecter l'affichage sur la carte mais pas les statistiques.

## Résumé des Fonctionnalités

 Carte choroplèthe par préfecture 
 Coopératives colorées par préfecture 
 Statistiques détaillées par préfecture 
 Statistiques détaillées par commune 
 Indicateurs de performance (3 graphiques) 
 Filtres interactifs multi-niveaux 
 Liste complète avec filtres 
 Export de la carte en PNG 

## Support

Pour toute question ou suggestion d'amélioration, consultez les fichiers :
- `AMELIORATIONS_ZOOM_REGION.md` - Documentation technique
- `test_zoom_region.py` - Script de test
- `CHANGEMENTS_ARCHITECTURE.md` - Changements d'architecture

---
**Version** : 2.0 
**Date** : 11 février 2026 
**Statut** : Opérationnel
