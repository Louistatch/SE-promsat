# Guide d'Installation - ProSMAT

## Installation Rapide (Windows)

### Méthode 1: Script Automatique

1. **Double-cliquez sur `start.bat`**
   - Le script va automatiquement:
     - Activer l'environnement virtuel
     - Créer la base de données
     - Initialiser les données
     - Démarrer le serveur

2. **Accédez à l'application**
   - Ouvrez votre navigateur: http://localhost:8000
   - Interface admin: http://localhost:8000/admin

### Méthode 2: Installation Manuelle

#### Étape 1: Activer l'environnement virtuel
```bash
venv\Scripts\activate
```

#### Étape 2: Installer les dépendances
```bash
pip install -r requirements.txt
```

#### Étape 3: Créer la base de données
```bash
python manage.py makemigrations accounts
python manage.py makemigrations monitoring
python manage.py makemigrations dashboard
python manage.py migrate
```

#### Étape 4: Initialiser les données
```bash
python manage.py init_prosmat
```

Cette commande va créer:
- Un compte administrateur
- Des comptes pour chaque région
- Un compte coordonnateur
- Un compte évaluateur
- Les composantes de base
- Les périodes pour 2026

#### Étape 5: Lancer le serveur
```bash
python manage.py runserver
```

## Comptes Créés Automatiquement

### Administrateur
- **Username:** admin
- **Password:** admin123
- **Accès:** Complet (interface admin + application)

### Coordonnateur National
- **Username:** coordonnateur
- **Password:** prosmat2026
- **Accès:** Vue d'ensemble de toutes les régions

### Évaluateur
- **Username:** evaluateur
- **Password:** prosmat2026
- **Accès:** Validation et suivi

### Chargés de Projet par Région

| Région | Username | Password | Accès |
|--------|----------|----------|-------|
| Maritime | charge_maritime | prosmat2026 | Région Maritime uniquement |
| Plateaux | charge_plateaux | prosmat2026 | Région Plateaux uniquement |
| Centrale | charge_centrale | prosmat2026 | Région Centrale uniquement |
| Kara | charge_kara | prosmat2026 | Région Kara uniquement |
| Savanes | charge_savanes | prosmat2026 | Région Savanes uniquement |

## Configuration des Indicateurs

### Via l'Interface Admin

1. **Connectez-vous à l'admin:** http://localhost:8000/admin
   - Username: admin
   - Password: admin123

2. **Créer des Composantes**
   - Allez dans "Composantes"
   - Cliquez sur "Ajouter composante"
   - Remplissez le nom et l'ordre

3. **Créer des Sous-composantes**
   - Allez dans "Sous-composantes"
   - Sélectionnez la composante parente
   - Ajoutez le nom et l'ordre

4. **Créer des Indicateurs**
   - Allez dans "Indicateurs"
   - Remplissez tous les champs:
     - Code (ex: IND-001)
     - Libellé
     - Type (Quantitatif/Qualitatif)
     - Niveau (Impact/Effet/Extrant)
     - Unité de mesure
     - Valeur de référence
     - Cible finale
     - Source de vérification
     - Fréquence de collecte
     - Responsable

5. **Créer des Périodes**
   - Allez dans "Périodes"
   - Définissez l'année, le trimestre et les dates

## Utilisation

### Pour les Chargés de Projet

1. **Connexion**
   - Utilisez votre compte régional
   - Ex: charge_maritime / prosmat2026

2. **Saisir une Réalisation**
   - Menu: Saisie
   - Sélectionnez l'indicateur
   - Choisissez la période
   - Entrez la valeur réalisée
   - Ajoutez un commentaire
   - Joignez un justificatif (optionnel)

3. **Consulter les Données**
   - Tableau de bord: Vue d'ensemble
   - Indicateurs: Liste complète
   - Réalisations: Vos saisies
   - Activités: Activités de votre région

### Pour les Coordonnateurs/Évaluateurs

1. **Connexion**
   - coordonnateur / prosmat2026
   - OU evaluateur / prosmat2026

2. **Vue d'Ensemble**
   - Accès à toutes les régions
   - Statistiques nationales
   - Comparaisons inter-régionales

3. **Validation**
   - Menu: Réalisations
   - Cliquez sur le bouton de validation (✓)
   - Les réalisations validées sont marquées

### Pour l'Administrateur

1. **Interface Admin**
   - http://localhost:8000/admin
   - admin / admin123

2. **Gestion Complète**
   - Créer/modifier les indicateurs
   - Gérer les utilisateurs
   - Configurer les composantes
   - Définir les périodes
   - Valider les réalisations

## Dépannage

### Erreur: "No module named 'django'"
```bash
pip install -r requirements.txt
```

### Erreur: "Table doesn't exist"
```bash
python manage.py migrate
```

### Erreur: "Port already in use"
```bash
python manage.py runserver 8001
```

### Réinitialiser la Base de Données
```bash
del db.sqlite3
python manage.py migrate
python manage.py init_prosmat
```

## Support Technique

Pour toute question ou problème:
1. Consultez le fichier README.md
2. Vérifiez les logs dans la console
3. Contactez l'équipe technique ProSMAT

## Sécurité

⚠️ **IMPORTANT:**
- Changez les mots de passe par défaut en production
- Configurez `DEBUG = False` en production
- Utilisez une base de données PostgreSQL en production
- Configurez HTTPS
- Sauvegardez régulièrement la base de données
