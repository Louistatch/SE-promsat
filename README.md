# 🌾 ProSMAT - Système de Suivi & Évaluation

![Django](https://img.shields.io/badge/Django-6.0-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Firebase](https://img.shields.io/badge/Firebase-Auth-orange.svg)
![License](https://img.shields.io/badge/License-Proprietary-red.svg)

Système de Suivi-Évaluation pour le Projet de Sécurité Alimentaire et Nutritionnelle (ProSMAT) au Togo, financé par GAFSP/FIDA.

## 📋 Table des Matières

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Technologies](#technologies)
- [Installation](#installation)
- [Configuration](#configuration)
- [Utilisation](#utilisation)
- [Structure du Projet](#structure-du-projet)
- [Documentation](#documentation)
- [Contribution](#contribution)
- [Licence](#licence)

## 🎯 Aperçu

ProSMAT est une application web Django complète pour le suivi et l'évaluation des indicateurs de performance du projet de sécurité alimentaire. Elle permet:

- 📊 Suivi des indicateurs de performance (KPI)
- 👥 Gestion des utilisateurs avec rôles et régions
- 📈 Tableaux de bord interactifs
- 📄 Génération automatique de rapports
- 🔐 Authentification Firebase
- 🌍 Couverture de 5 régions du Togo
- 📱 Interface responsive et moderne

## ✨ Fonctionnalités

### Authentification & Sécurité
- 🔥 Authentification Firebase (Email/Password + Google OAuth)
- 🔐 Authentification Django (backup)
- 👤 Gestion des rôles (Chargé de Projet, Coordonnateur, Évaluateur, Admin)
- 🌍 Gestion des régions (Maritime, Plateaux, Centrale, Kara, Savanes)
- 🛡️ Rate limiting et sécurité renforcée

### Suivi & Évaluation
- 📊 Saisie des réalisations par indicateur
- ✅ Validation des données
- 🚨 Contrôle qualité automatique avec alertes
- 📈 Désagrégation par genre (Hommes/Femmes)
- 📎 Pièces justificatives
- 🔍 Recherche et filtrage avancés

### Tableaux de Bord
- 📊 Dashboard principal avec statistiques
- 🎯 Dashboard exécutif avec KPI
- 📈 Graphiques interactifs
- 🗺️ Vue par région
- 📅 Évolution temporelle

### Rapports
- 📄 Génération automatique de rapports
- 📊 Rapports trimestriels, annuels, de mission
- 🔍 Filtres avancés (type, région, période)
- 📥 Export Excel et PDF
- 🖨️ Impression optimisée

### Administration
- 👥 Gestion des utilisateurs
- 🎨 Interface admin personnalisée
- 📊 Actions en masse
- 🔧 Configuration système

## 🛠️ Technologies

### Backend
- **Django 6.0** - Framework web Python
- **Django REST Framework** - API REST
- **Firebase Admin SDK** - Authentification
- **PostgreSQL** - Base de données (production)
- **SQLite** - Base de données (développement)

### Frontend
- **Bootstrap 5** - Framework CSS
- **Bootstrap Icons** - Icônes
- **Font Awesome** - Icônes supplémentaires
- **Chart.js** - Graphiques (via CDN)

### Déploiement
- **Neon** - Base de données PostgreSQL serverless
- **WhiteNoise** - Fichiers statiques
- **Gunicorn** - Serveur WSGI

## 📦 Installation

### Prérequis

- Python 3.10 ou supérieur
- pip (gestionnaire de paquets Python)
- Git
- Compte Firebase (pour l'authentification)
- Compte Neon (pour la base de données en production)

### Étapes d'Installation

1. **Cloner le dépôt**
```bash
git clone https://github.com/votre-username/prosmat.git
cd prosmat
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer les variables d'environnement**
```bash
# Copier le fichier d'exemple
copy .env.example .env

# Éditer .env avec vos valeurs
```

5. **Configurer Firebase**
- Télécharger le fichier de credentials Firebase
- Le placer à la racine du projet: `firebase-credentials.json`
- Mettre à jour les variables Firebase dans `.env`

6. **Effectuer les migrations**
```bash
python manage.py migrate
```

7. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

8. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic --noinput
```

9. **Lancer le serveur de développement**
```bash
python manage.py runserver
```

10. **Accéder à l'application**
- Application: http://127.0.0.1:8000/
- Admin: http://127.0.0.1:8000/admin/

## ⚙️ Configuration

### Variables d'Environnement

Créez un fichier `.env` à la racine du projet:

```env
# Django
SECRET_KEY=votre-secret-key-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Base de données (Production)
DATABASE_URL=postgresql://user:password@host:5432/database

# Firebase
FIREBASE_API_KEY=votre-api-key
FIREBASE_AUTH_DOMAIN=votre-projet.firebaseapp.com
FIREBASE_PROJECT_ID=votre-projet-id
FIREBASE_STORAGE_BUCKET=votre-projet.appspot.com
FIREBASE_MESSAGING_SENDER_ID=votre-sender-id
FIREBASE_APP_ID=votre-app-id
FIREBASE_MEASUREMENT_ID=votre-measurement-id
```

### Firebase Configuration

1. Créer un projet Firebase: https://console.firebase.google.com/
2. Activer Authentication (Email/Password + Google)
3. Télécharger le fichier de credentials Admin SDK
4. Configurer les domaines autorisés

Voir: [CONFIGURATION_GOOGLE_SIGNIN.txt](CONFIGURATION_GOOGLE_SIGNIN.txt)

### Base de Données

**Développement:** SQLite (par défaut)

**Production:** PostgreSQL via Neon
```bash
# Migrer vers Neon
python migrer_vers_neon.py
```

Voir: [GUIDE_NEON_FIREBASE.md](GUIDE_NEON_FIREBASE.md)

## 🚀 Utilisation

### Connexion

1. Accédez à http://127.0.0.1:8000/accounts/login/
2. Connectez-vous avec:
   - Email/Password Firebase
   - Google OAuth
   - Compte Django (backup)

### Gestion des Rôles

**Via Interface Web (Admin uniquement):**
```
http://127.0.0.1:8000/accounts/manage-users/
```

**Via Script Python:**
```bash
python attribuer_roles.py
```

**Via Django Admin:**
```
http://127.0.0.1:8000/admin/accounts/user/
```

Voir: [GUIDE_COMPLET_ROLES.md](GUIDE_COMPLET_ROLES.md)

### Saisie des Réalisations

1. Menu: **Saisie**
2. Sélectionner l'indicateur et la période
3. Saisir les valeurs (total, hommes, femmes)
4. Ajouter un commentaire et une pièce justificative
5. Enregistrer

### Génération de Rapports

1. Menu: **Rapports**
2. Cliquer sur **Générer un rapport**
3. Sélectionner type, période, région
4. Le rapport est généré automatiquement

Voir: [AMELIORATIONS_RAPPORTS.md](AMELIORATIONS_RAPPORTS.md)

## 📁 Structure du Projet

```
prosmat/
├── accounts/              # Application utilisateurs
│   ├── firebase_auth.py   # Backend Firebase
│   ├── views.py           # Vues
│   ├── views_firebase.py  # Vues Firebase
│   └── models.py          # Modèle User
├── dashboard/             # Application tableaux de bord
│   ├── views.py           # Vues dashboard
│   └── urls.py            # Routes
├── monitoring/            # Application suivi-évaluation
│   ├── models.py          # Modèles (Indicateur, Realisation, etc.)
│   ├── views.py           # Vues
│   ├── api_views.py       # API REST
│   └── utils.py           # Utilitaires
├── config/                # Configuration Django
│   ├── settings.py        # Paramètres
│   ├── urls.py            # Routes principales
│   └── wsgi.py            # WSGI
├── templates/             # Templates HTML
│   ├── base.html          # Template de base
│   ├── accounts/          # Templates authentification
│   ├── dashboard/         # Templates dashboard
│   └── monitoring/        # Templates monitoring
├── static/                # Fichiers statiques
│   ├── css/               # Styles CSS
│   ├── js/                # Scripts JavaScript
│   └── images/            # Images (logo, etc.)
├── media/                 # Fichiers uploadés
├── logs/                  # Logs Django
├── .env                   # Variables d'environnement (non versionné)
├── .gitignore             # Fichiers ignorés par Git
├── requirements.txt       # Dépendances Python
├── manage.py              # Script Django
└── README.md              # Ce fichier
```

## 📚 Documentation

### Guides Principaux
- [GUIDE_COMPLET_ROLES.md](GUIDE_COMPLET_ROLES.md) - Gestion des rôles
- [GUIDE_NEON_FIREBASE.md](GUIDE_NEON_FIREBASE.md) - Configuration Neon + Firebase
- [AMELIORATIONS_RAPPORTS.md](AMELIORATIONS_RAPPORTS.md) - Section Rapports
- [SYSTEME_ROLES_PRET.md](SYSTEME_ROLES_PRET.md) - Système de rôles

### Guides Rapides
- [ACCES_RAPIDE_ROLES.txt](ACCES_RAPIDE_ROLES.txt) - Référence rapide rôles
- [DEMARRAGE_RAPIDE_FIREBASE.txt](DEMARRAGE_RAPIDE_FIREBASE.txt) - Démarrage Firebase
- [COMMANDES_RAPIDES.md](COMMANDES_RAPIDES.md) - Commandes utiles

### Scripts Utiles
- `attribuer_roles.py` - Attribuer des rôles aux utilisateurs
- `tester_roles.py` - Tester le système de rôles
- `donner_admin.py` - Donner le rôle admin
- `migrer_vers_neon.py` - Migration vers Neon
- `verifier_firebase.py` - Vérifier Firebase

## 👥 Rôles et Permissions

| Rôle | Accès Région | Dashboard Exécutif | Gestion Users | Exports |
|------|--------------|-------------------|---------------|---------|
| **Chargé de Projet** | Sa région uniquement | ❌ | ❌ | ❌ |
| **Coordonnateur** | Toutes les régions | ✅ | ❌ | ✅ |
| **Évaluateur** | Toutes les régions | ✅ | ❌ | ✅ |
| **Admin** | Toutes les régions | ✅ | ✅ | ✅ |

## 🧪 Tests

```bash
# Vérifier la configuration
python manage.py check

# Tester Firebase
python verifier_firebase.py

# Tester les rôles
python tester_roles.py

# Lancer les tests Django
python manage.py test
```

## 🚀 Déploiement

### Production avec Neon + Render/Railway

1. **Préparer la base de données**
```bash
python migrer_vers_neon.py
```

2. **Configurer les variables d'environnement**
- `SECRET_KEY` (générer une nouvelle clé)
- `DEBUG=False`
- `DATABASE_URL` (Neon)
- Variables Firebase

3. **Collecter les fichiers statiques**
```bash
python manage.py collectstatic --noinput
```

4. **Déployer**
- Render: Connecter le dépôt GitHub
- Railway: `railway up`
- Heroku: `git push heroku main`

Voir: [GUIDE_NEON_FIREBASE.md](GUIDE_NEON_FIREBASE.md)

## 🔒 Sécurité

- ✅ Authentification Firebase sécurisée
- ✅ Rate limiting (10 tentatives/minute)
- ✅ Sessions sécurisées (HttpOnly, Secure, SameSite)
- ✅ CSRF protection
- ✅ Validation des données
- ✅ Logs structurés
- ✅ Fichiers sensibles exclus (.gitignore)

## 🤝 Contribution

Ce projet est propriétaire et destiné au Projet ProSMAT - Togo.

Pour toute question ou suggestion:
- Email: prosmat@example.com
- Documentation: Voir les fichiers .md dans le projet

## 📄 Licence

Propriétaire - Tous droits réservés

© 2026 ProSMAT - Projet de Sécurité Alimentaire et Nutritionnelle
Financé par GAFSP & FIDA - République du Togo

## 🙏 Remerciements

- **GAFSP** - Global Agriculture and Food Security Program
- **FIDA** - Fonds International de Développement Agricole
- **Gouvernement du Togo** - Ministère de l'Agriculture
- **Équipe ProSMAT** - Pour leur collaboration

## 📞 Support

Pour toute assistance:
1. Consultez la documentation dans le dossier du projet
2. Exécutez les scripts de diagnostic
3. Vérifiez les logs: `logs/django.log`
4. Contactez l'administrateur système

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Dernière mise à jour: Février 2026*
