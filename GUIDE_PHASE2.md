# 📖 GUIDE RAPIDE - PHASE 2

**Version**: 2.0  
**Date**: 8 Février 2026

---

## 🎯 ACCÈS RAPIDE

### Dashboard Exécutif
**URL**: http://localhost:8000/executif/  
**Accès**: Coordonnateur, Évaluateur, Admin

### Exports
- **Excel**: http://localhost:8000/monitoring/export/excel/
- **PDF**: http://localhost:8000/monitoring/export/pdf/

---

## 📊 DASHBOARD EXÉCUTIF

### Vue d'Ensemble
Le dashboard exécutif offre une vue stratégique complète du projet avec:
- 3 KPI principaux en cartes colorées
- 3 graphiques interactifs
- Tableau de performance régionale
- Alertes récentes

### KPI Affichés

#### 1. Bénéficiaires Directs
- **Valeur**: Nombre total de bénéficiaires
- **Cible**: Objectif du projet
- **% Atteinte**: Progression vers la cible
- **Femmes**: Nombre et pourcentage de femmes

#### 2. Emplois Créés (ETP)
- **Valeur**: Total des emplois créés
- **Cible**: Objectif d'emplois
- **% Atteinte**: Progression

#### 3. Performance Globale
- **Valeur**: Moyenne de tous les indicateurs
- **Interprétation**:
  - 75-100%: Excellent ✅
  - 50-74%: Moyen ⚠️
  - 0-49%: Faible ❌

### Graphiques Interactifs

#### Graphique 1: Performance par Région
- **Type**: Barres verticales
- **Données**: % de performance de chaque région
- **Utilisation**: Comparer les régions entre elles
- **Interaction**: Survoler pour voir les détails

#### Graphique 2: Performance par Composante
- **Type**: Donut (anneau)
- **Données**: Répartition par composante (GAFSP, DEV, PROD, RES)
- **Utilisation**: Voir la contribution de chaque composante
- **Interaction**: Cliquer sur la légende pour masquer/afficher

#### Graphique 3: Évolution Temporelle
- **Type**: Ligne avec remplissage
- **Données**: Total réalisé par trimestre
- **Utilisation**: Visualiser les tendances
- **Interaction**: Survoler pour voir les valeurs exactes

### Tableau de Performance
- **Colonnes**: Région, Performance (%), Nb Réalisations, Statut
- **Couleurs**:
  - Vert: Performance ≥ 75%
  - Orange: Performance 50-74%
  - Rouge: Performance < 50%

### Alertes Récentes
- **Affichage**: 10 dernières alertes non résolues
- **Tri**: Par sévérité puis date
- **Couleurs**:
  - Rouge: Critique
  - Orange: Important
  - Bleu: Mineur

---

## 📤 EXPORT EXCEL

### Contenu du Fichier

#### Feuille "Synthese-Nationale"
Tous les indicateurs avec:
- Code et libellé
- Cible finale
- Réalisations T1, T2, T3, T4
- Total réalisé
- % Atteinte
- Écart
- Hommes, Femmes, % Femmes

#### Feuilles "Suivi-[REGION]"
5 feuilles (une par région):
- MARITIME
- PLATEAUX
- CENTRALE
- KARA
- SAVANES

Même structure que la synthèse nationale, mais données régionales uniquement.

#### Feuille "Controle-Qualite"
Toutes les alertes non résolues:
- Région
- Indicateur
- Période
- Type d'alerte
- Sévérité
- Message
- Date de détection

### Utilisation

#### Analyse dans Excel
1. Ouvrir le fichier exporté
2. Utiliser les filtres automatiques
3. Créer des tableaux croisés dynamiques
4. Ajouter vos propres graphiques
5. Partager avec l'équipe

#### Formules Excel
Le fichier contient des valeurs, pas de formules. Vous pouvez:
- Ajouter vos propres calculs
- Créer des formules personnalisées
- Lier à d'autres fichiers Excel

---

## 📄 EXPORT PDF

### Structure du Rapport

#### Section 1: Synthèse Exécutive
- Titre et date
- Tableau des KPI:
  - Nombre d'indicateurs
  - Nombre de réalisations
  - Performance globale

#### Section 2: Performance par Région
- Tableau comparatif
- Classement des régions
- Nombre de réalisations par région

#### Section 3: Top 10 Indicateurs
- Les 10 indicateurs les plus performants
- Code, libellé et % d'atteinte
- Tri décroissant par performance

#### Section 4: Alertes Qualité
- 15 alertes les plus critiques
- Région, indicateur, type, sévérité
- Recommandations d'action

### Utilisation

#### Impression
1. Télécharger le PDF
2. Ouvrir avec Adobe Reader ou navigateur
3. Imprimer en mode paysage (A4)
4. Qualité: Haute résolution

#### Partage
1. Envoyer par email aux parties prenantes
2. Joindre aux rapports trimestriels
3. Archiver pour historique
4. Présenter en réunion

---

## 🎨 PERSONNALISATION

### Couleurs du Dashboard
Les couleurs sont définies dans le template. Pour modifier:
1. Ouvrir `templates/dashboard/dashboard_executif.html`
2. Chercher `.kpi-card`
3. Modifier les gradients CSS

### Graphiques
Pour personnaliser les graphiques:
1. Ouvrir le même template
2. Chercher la section `<script>`
3. Modifier les options Chart.js

---

## 🔧 DÉPANNAGE

### Dashboard ne s'affiche pas
**Problème**: Page blanche ou erreur 403  
**Solution**: Vérifier que vous êtes connecté avec un compte Coordonnateur/Évaluateur/Admin

### Graphiques ne s'affichent pas
**Problème**: Espaces vides à la place des graphiques  
**Solution**: 
1. Vérifier la connexion internet (Chart.js est chargé depuis CDN)
2. Désactiver les bloqueurs de publicité
3. Vider le cache du navigateur

### Export Excel vide
**Problème**: Fichier téléchargé mais feuilles vides  
**Solution**: 
1. Vérifier qu'il y a des données dans la base
2. Exécuter `python manage.py creer_donnees_test` si nécessaire

### Export PDF erreur
**Problème**: Erreur 500 lors de la génération  
**Solution**: 
1. Vérifier que ReportLab est installé: `pip list | grep reportlab`
2. Réinstaller si nécessaire: `pip install reportlab==4.4.9`

---

## 💡 ASTUCES

### Optimiser les Performances
1. **Filtrer les données**: Utiliser les filtres de période
2. **Limiter les graphiques**: Désactiver ceux non utilisés
3. **Exporter régulièrement**: Ne pas attendre d'avoir trop de données

### Meilleures Pratiques
1. **Consulter le dashboard hebdomadairement**
2. **Exporter en Excel pour analyses détaillées**
3. **Générer des PDF pour les réunions**
4. **Surveiller les alertes quotidiennement**

### Raccourcis Clavier
- **Ctrl + P**: Imprimer le dashboard
- **Ctrl + S**: Sauvegarder la page (pour archivage)
- **F5**: Rafraîchir les données

---

## 📞 SUPPORT

### Problèmes Techniques
1. Vérifier les logs Django
2. Consulter la documentation complète (PHASE2_TERMINEE.md)
3. Contacter l'administrateur système

### Demandes de Fonctionnalités
1. Noter les besoins dans un document
2. Prioriser avec l'équipe
3. Planifier pour Phase 3

---

## 🎓 FORMATION

### Pour les Coordonnateurs
1. Comprendre les KPI
2. Interpréter les graphiques
3. Analyser les tendances
4. Prendre des décisions basées sur les données

### Pour les Évaluateurs
1. Utiliser le contrôle qualité
2. Résoudre les alertes
3. Générer des rapports
4. Valider les données

### Pour les Chargés de Projet
1. Saisir des données de qualité
2. Consulter les statistiques régionales
3. Comparer avec les autres régions
4. Améliorer les performances

---

## 📚 RESSOURCES

### Documentation
- **PHASE2_TERMINEE.md**: Documentation complète
- **STATUT_ACTUEL.md**: État du projet
- **README.md**: Vue d'ensemble

### Liens Utiles
- **Chart.js**: https://www.chartjs.org/docs/
- **ReportLab**: https://www.reportlab.com/docs/
- **Bootstrap 5**: https://getbootstrap.com/docs/5.3/

---

## ✅ CHECKLIST QUOTIDIENNE

### Pour le Coordonnateur
- [ ] Consulter le dashboard exécutif
- [ ] Vérifier les alertes récentes
- [ ] Analyser les performances régionales
- [ ] Identifier les régions en difficulté
- [ ] Planifier les actions correctives

### Pour l'Évaluateur
- [ ] Vérifier les nouvelles réalisations
- [ ] Résoudre les alertes critiques
- [ ] Valider les données saisies
- [ ] Générer un rapport si nécessaire
- [ ] Archiver les exports

---

**ProSMAT - Suivi & Évaluation Avancé** 🚀
