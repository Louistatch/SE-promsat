# Guide - Onglet Marché Agroécologique

## Vue d'Ensemble

L'onglet "Marché Agroécologique" utilise des techniques avancées de data science pour :
1. **Identifier les 10 coopératives à fort potentiel** pour intégrer un marché agroécologique
2. **Analyser les cultures dominantes** que les producteurs souhaitent produire
3. **Fournir des recommandations stratégiques** pour le développement du marché

## Section 1 : Top 10 Coopératives à Fort Potentiel

### Méthodologie de Scoring

Le système de scoring évalue chaque coopérative sur 8 critères pondérés :

#### Critères et Pondérations

1. **Engagement Agroécologique (20%)**
 - Oui = 100 points
 - Non = 0 point
 - Critère le plus important car indique la volonté

2. **Effectif Total (15%)**
 - Normalisé sur 100 (max = 100 points)
 - Indique la capacité de production

3. **Immatriculation (15%)**
 - Oui = 100 points
 - Non = 0 point
 - Structure légale formalisée

4. **Restitution Formation (15%)**
 - Oui = 100 points
 - Non = 0 point
 - Transfert de connaissances effectué

5. **Parcelle d'Apprentissage (10%)**
 - Oui = 100 points
 - Non = 0 point
 - Infrastructure de formation disponible

6. **Production Contre-Saison (10%)**
 - Oui = 100 points
 - Non = 0 point
 - Capacité de production diversifiée

7. **Taux de Féminisation (7.5%)**
 - >50% = 100 points
 - <50% = taux × 2
 - Bonus pour l'inclusion des femmes

8. **Taux de Jeunes (7.5%)**
 - >30% = 100 points
 - <30% = taux × 3.33
 - Bonus pour le dynamisme

### Score Total

**Formule** : Moyenne pondérée de 0 à 100

```
Score = (Engagement × 0.20) + (Effectif × 0.15) + (Immat × 0.15) + 
 (Formation × 0.15) + (Parcelle × 0.10) + (Production × 0.10) + 
 (Femmes × 0.075) + (Jeunes × 0.075)
```

### Interprétation des Scores

- **90-100** : Excellent potentiel - Prêt pour le marché
- **70-89** : Bon potentiel - Accompagnement léger nécessaire
- **50-69** : Potentiel moyen - Renforcement des capacités requis
- **<50** : Potentiel faible - Formation intensive nécessaire

### Affichage des Résultats

#### Tableau Top 10
- Rang (1-10)
- Nom de la coopérative
- Région
- Préfecture
- Effectif
- Score total

#### Graphique en Barres
- Visualisation horizontale des scores
- Échelle de couleur Viridis (bleu → jaune → vert)
- Tri par score décroissant

#### Profils Détaillés
Pour chaque coopérative du Top 10 :

**Métriques Clés** :
- Score total /100
- Effectif
- Nombre et % de femmes
- Nombre et % de jeunes
- Localisation (région, préfecture)
- Statuts (engagement, immatriculation, formation)

**Graphique Radar** :
- Visualisation des 8 critères
- Permet d'identifier les forces et faiblesses
- Échelle 0-100 pour chaque axe

## Section 2 : Cultures Dominantes et Tendances

### Analyse des Cultures

Le système analyse la colonne "Cultures en contre-saison" pour :
- Extraire toutes les cultures mentionnées
- Compter les occurrences
- Identifier les tendances

### Traitement des Données

1. **Extraction** : Séparation par virgules
2. **Nettoyage** : Suppression des espaces, mise en majuscules
3. **Comptage** : Agrégation des occurrences
4. **Classement** : Tri par popularité

### Visualisations

#### Top 20 Cultures
**Tableau** :
- Culture
- Nombre de mentions

**Graphique en Barres** :
- Top 15 cultures
- Orientation horizontale
- Échelle de couleur verte (Greens)

#### Nuage de Cultures
**Graphique de Bulles** :
- Taille = fréquence de mention
- Couleur = intensité (Viridis)
- Permet de voir d'un coup d'œil les cultures dominantes

#### Cultures par Région
**Analyse Géographique** :
- Top 5 cultures par région
- Permet d'identifier les spécificités régionales
- Aide à la planification logistique

### Cultures Typiques Identifiées

D'après l'analyse des données :

1. **Tomates** - Culture la plus demandée
2. **Piment** (vert, rouge, long)
3. **Gombo**
4. **Gboma** (légume-feuille local)
5. **Adémè** (légume-feuille local)
6. **Oignons**
7. **Choux**
8. **Laitue**
9. **Carottes**
10. **Concombre**

## Section 3 : Recommandations Stratégiques

### Pour le Marché Agroécologique

**Actions Prioritaires** :

1. **Accompagner les Top 10** (score >70)
 - Mise en relation avec acheteurs
 - Certification agroécologique
 - Appui technique spécialisé

2. **Renforcer les coopératives moyennes** (score 50-70)
 - Formation complémentaire
 - Appui organisationnel
 - Développement de parcelles

3. **Former les coopératives faibles** (score <50)
 - Formation de base en agroécologie
 - Accompagnement à l'immatriculation
 - Sensibilisation aux pratiques AE

4. **Créer des groupements régionaux**
 - Mutualisation des ressources
 - Économies d'échelle
 - Partage d'expériences

5. **Développer des filières**
 - Focus sur cultures dominantes
 - Circuits courts
 - Transformation locale

### Pour les Cultures

**Opportunités Identifiées** :

1. **Tomates**
 - Culture la plus demandée
 - Fort potentiel commercial
 - Marché urbain important

2. **Piment**
 - Demande élevée
 - Bonne valeur ajoutée
 - Conservation facile

3. **Gombo**
 - Culture traditionnelle
 - Marché stable
 - Résistant à la sécheresse

4. **Légumes-feuilles** (Gboma, Adémè)
 - Cultures locales
 - Valeur nutritionnelle élevée
 - Cycle court

5. **Diversification**
 - Encourager associations de cultures
 - Rotation des cultures
 - Résilience climatique

## Export des Résultats

### Fichiers Disponibles

1. **Top 10 Coopératives (CSV)**
 - Rang, Coopérative, Région, Préfecture, Effectif, Score
 - Utilisable pour reporting et suivi

2. **Analyse Cultures (CSV)**
 - Culture, Nombre de mentions
 - Utilisable pour planification

### Utilisation des Exports

**Pour le Reporting** :
- Intégrer dans rapports de mission
- Présenter aux partenaires
- Justifier les choix d'intervention

**Pour la Planification** :
- Identifier les zones prioritaires
- Planifier les formations
- Organiser les filières

## Cas d'Usage

### Cas 1 : Sélection pour un Programme Pilote

**Objectif** : Identifier 5 coopératives pour un programme pilote de marché AE

**Démarche** :
1. Consulter le Top 10
2. Sélectionner les 5 premières avec score >80
3. Vérifier la répartition géographique
4. Consulter les profils détaillés
5. Valider avec les graphiques radar

### Cas 2 : Planification des Cultures

**Objectif** : Décider quelles cultures promouvoir dans une région

**Démarche** :
1. Consulter "Cultures par Région"
2. Identifier les 3 cultures dominantes
3. Vérifier la demande globale (Top 20)
4. Croiser avec les capacités locales
5. Planifier les formations spécifiques

### Cas 3 : Évaluation d'une Coopérative

**Objectif** : Évaluer si une coopérative est prête pour le marché AE

**Démarche** :
1. Chercher la coopérative dans le Top 10
2. Si présente : consulter son profil détaillé
3. Analyser le graphique radar
4. Identifier les points faibles
5. Proposer un plan d'accompagnement

## Indicateurs de Performance

### KPIs du Marché AE

**Taux de Préparation** :
- % de coopératives avec score >70
- Objectif : >30%

**Engagement Agroécologique** :
- % de coopératives engagées
- Objectif : >50%

**Diversification** :
- Nombre moyen de cultures par coopérative
- Objectif : >3

**Structuration** :
- % de coopératives immatriculées
- Objectif : >80%

## Limites et Précautions

### Limites du Scoring

1. **Données déclaratives** : Basé sur les réponses des coopératives
2. **Critères quantitatifs** : Ne capture pas tous les aspects qualitatifs
3. **Pondérations fixes** : Peuvent être ajustées selon le contexte
4. **Snapshot** : Photo à un instant T, évolution possible

### Précautions d'Interprétation

1. **Score élevé ≠ Garantie de succès**
 - Autres facteurs à considérer (marché, logistique, etc.)

2. **Score faible ≠ Impossibilité**
 - Potentiel d'amélioration avec accompagnement

3. **Cultures populaires ≠ Cultures rentables**
 - Analyser aussi la demande du marché

4. **Analyse complémentaire nécessaire**
 - Visites terrain
 - Entretiens approfondis
 - Études de marché

## Évolutions Futures Possibles

### Améliorations du Scoring

- [ ] Intégrer des données de production réelle
- [ ] Ajouter des critères de proximité au marché
- [ ] Inclure l'historique de performance
- [ ] Pondérations adaptatives par région

### Analyses Supplémentaires

- [ ] Prédiction de rendement par culture
- [ ] Analyse de rentabilité par filière
- [ ] Clustering de coopératives similaires
- [ ] Recommandations personnalisées

### Intégrations

- [ ] Connexion avec système de suivi
- [ ] API pour mise à jour automatique
- [ ] Alertes sur changements de score
- [ ] Tableau de bord temps réel

## Références

### Méthodologie

- Scoring multi-critères
- Analyse de fréquence textuelle
- Visualisation de données
- Recommandation basée sur les données

### Technologies

- Python Pandas pour l'analyse
- Plotly pour les visualisations
- Collections Counter pour le comptage
- Streamlit pour l'interface

---

**Version** : 1.0 
**Date** : 11 février 2026 
**Statut** : Opérationnel

*Développé pour ProSMAT 2025*
