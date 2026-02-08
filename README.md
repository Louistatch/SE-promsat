# ProSMAT - Système de Suivi & Évaluation

Système de suivi-évaluation pour le projet ProSMAT au Togo, permettant la gestion des indicateurs, réalisations et activités par région.

## Fonctionnalités

### Gestion des Utilisateurs
- **5 Chargés de Projet** (un par région du Togo)
  - Région Maritime
  - Région des Plateaux
  - Région Centrale
  - Région de la Kara
  - Région des Savanes
- **Coordonnateur** (vue d'ensemble nationale)
- **Évaluateur** (suivi et validation)
- **Administrateur** (gestion complète)

### Modules Principaux

#### 1. Tableau de Bord
- Vue d'ensemble des statistiques
- Indicateurs clés de performance
- Dernières réalisations et activités
- Graphiques et visualisations

#### 2. Gestion des Indicateurs
- Indicateurs quantitatifs et qualitatifs
- Niveaux: Impact, Effet, Extrant
- Valeurs de référence et cibles
- Organisation par composantes et sous-composantes

#### 3. Saisie des Réalisations
- Saisie par indicateur, période et région
- Validation par les coordonnateurs/évaluateurs
- Fichiers justificatifs
- Commentaires et observations

#### 4. Suivi des Activités
- Planification et suivi budgétaire
- Statuts: Planifié, En cours, Terminé, Suspendu, Annulé
- Taux d'exécution financière
- Responsables par activité

#### 5. Rapports
- Rapports trimestriels et annuels
- Rapports de mission
- Export et archivage

## Installation

### Prérequis
- Python 3.10+
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
cd C:\Users\HP\Downloads\prosmat_se
```

2. **Activer l'environnement virtuel**
```bash
venv\Scripts\activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Créer la base de données**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Initialiser les données de base**
```bash
python manage.py init_prosmat
```

6. **Lancer le serveur**
```bash
python manage.py runserver
```

7. **Accéder à l'application**
- Application: http://localhost:8000
- Admin: http://localhost:8000/admin

## Comptes par Défaut

### Administrateur
- **Username:** admin
- **Password:** admin123

### Coordonnateur
- **Username:** coordonnateur
- **Password:** prosmat2026

### Évaluateur
- **Username:** evaluateur
- **Password:** prosmat2026

### Chargés de Projet (par région)
- **Maritime:** charge_maritime / prosmat2026
- **Plateaux:** charge_plateaux / prosmat2026
- **Centrale:** charge_centrale / prosmat2026
- **Kara:** charge_kara / prosmat2026
- **Savanes:** charge_savanes / prosmat2026

## Structure du Projet

```
prosmat_se/
├── accounts/           # Gestion des utilisateurs
├── dashboard/          # Tableau de bord
├── monitoring/         # Suivi-évaluation
├── config/            # Configuration Django
├── templates/         # Templates HTML
├── static/           # Fichiers statiques (CSS, JS)
└── media/            # Fichiers uploadés
```

## Utilisation

### Pour les Chargés de Projet
1. Se connecter avec son compte régional
2. Saisir les réalisations pour sa région
3. Consulter les indicateurs et activités
4. Générer des rapports

### Pour les Coordonnateurs/Évaluateurs
1. Vue d'ensemble de toutes les régions
2. Validation des réalisations
3. Analyse des statistiques
4. Suivi des activités nationales

### Pour l'Administrateur
1. Accès à l'interface d'administration Django
2. Gestion des utilisateurs
3. Configuration des indicateurs
4. Gestion des composantes et périodes

## Administration

L'interface d'administration Django permet de:
- Créer et gérer les indicateurs
- Définir les composantes et sous-composantes
- Gérer les périodes de reporting
- Ajouter des utilisateurs
- Configurer les activités
- Valider les réalisations

## Support

Pour toute question ou problème, contactez l'équipe technique ProSMAT.

## Licence

© 2026 ProSMAT - Tous droits réservés
