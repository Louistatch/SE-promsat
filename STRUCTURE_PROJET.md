# 📁 Structure du Projet ProSMAT

## Vue d'Ensemble

```
prosmat_se/
├── 📁 accounts/              # Application de gestion des utilisateurs
├── 📁 dashboard/             # Application tableau de bord
├── 📁 monitoring/            # Application suivi-évaluation
├── 📁 config/                # Configuration Django
├── 📁 templates/             # Templates HTML
├── 📁 static/                # Fichiers statiques (CSS, JS)
├── 📁 media/                 # Fichiers uploadés (créé automatiquement)
├── 📁 venv/ ou venv_new/     # Environnement virtuel Python
├── 📄 manage.py              # Script de gestion Django
├── 📄 requirements.txt       # Dépendances Python
├── 📄 README.md              # Documentation principale
├── 📄 install.bat            # Script d'installation
└── 📄 start_new.bat          # Script de démarrage
```

## 📂 Détail des Applications

### 1. accounts/ - Gestion des Utilisateurs

```
accounts/
├── models.py           # Modèle User personnalisé
│   └── User            # Utilisateur avec rôle et région
├── views.py            # Vues d'authentification
│   ├── login_view      # Connexion
│   ├── logout_view     # Déconnexion
│   └── profile_view    # Profil utilisateur
├── admin.py            # Configuration admin Django
├── urls.py             # Routes URL
└── apps.py             # Configuration de l'app
```

**Modèles:**
- `User` - Utilisateur avec rôles (Chargé de Projet, Coordonnateur, Évaluateur, Admin) et région

**Rôles:**
- `CHARGE_PROJET` - Accès limité à sa région
- `COORDONNATEUR` - Vue d'ensemble nationale
- `EVALUATEUR` - Validation et suivi
- `ADMIN` - Accès complet

### 2. dashboard/ - Tableau de Bord

```
dashboard/
├── views.py                # Vues du tableau de bord
│   ├── home_view           # Page d'accueil
│   ├── statistiques_view   # Statistiques
│   ├── indicateurs_view    # Liste des indicateurs
│   └── activites_view      # Liste des activités
├── urls.py                 # Routes URL
└── apps.py                 # Configuration de l'app
```

**Fonctionnalités:**
- Vue d'ensemble des statistiques
- Dernières réalisations
- Activités récentes
- Graphiques et indicateurs clés

### 3. monitoring/ - Suivi & Évaluation

```
monitoring/
├── models.py                    # Modèles de données
│   ├── Composante               # Composantes du projet
│   ├── SousComposante           # Sous-composantes
│   ├── Indicateur               # Indicateurs de performance
│   ├── Periode                  # Périodes de reporting
│   ├── Realisation              # Réalisations saisies
│   ├── Activite                 # Activités du projet
│   └── Rapport                  # Rapports générés
├── views.py                     # Vues de suivi
│   ├── saisie_realisation_view  # Saisie de données
│   ├── liste_realisations_view  # Liste des réalisations
│   ├── modifier_realisation_view # Modification
│   ├── valider_realisation_view # Validation
│   └── liste_rapports_view      # Rapports
├── admin.py                     # Interface admin complète
├── urls.py                      # Routes URL
└── management/                  # Commandes personnalisées
    └── commands/
        └── init_prosmat.py      # Initialisation des données
```

**Modèles Principaux:**

#### Composante
- Organisation hiérarchique du projet
- Ordre d'affichage

#### SousComposante
- Subdivision des composantes
- Lien avec les indicateurs

#### Indicateur
- Code unique
- Libellé descriptif
- Type: Quantitatif/Qualitatif
- Niveau: Impact/Effet/Extrant
- Unité de mesure
- Valeur de référence
- Cible finale
- Source de vérification
- Fréquence de collecte

#### Periode
- Année
- Trimestre (T1, T2, T3, T4)
- Dates de début et fin
- Statut de clôture

#### Realisation
- Lien avec indicateur et période
- Région concernée
- Valeur réalisée
- Commentaire
- Fichier justificatif
- Statut de validation
- Traçabilité (qui, quand)

#### Activite
- Titre et description
- Dates prévues et réelles
- Budget prévu et exécuté
- Région
- Statut (Planifié, En cours, Terminé, etc.)
- Responsable

#### Rapport
- Type (Trimestriel, Annuel, Mission)
- Période et région
- Contenu
- Fichier PDF/Word
- Auteur et dates

### 4. config/ - Configuration

```
config/
├── settings.py         # Configuration Django
│   ├── INSTALLED_APPS  # Applications installées
│   ├── DATABASES       # Configuration BDD
│   ├── AUTH_USER_MODEL # Modèle utilisateur personnalisé
│   └── STATIC/MEDIA    # Fichiers statiques et médias
├── urls.py             # Routes principales
├── wsgi.py             # Configuration WSGI
└── asgi.py             # Configuration ASGI
```

### 5. templates/ - Templates HTML

```
templates/
├── base.html                           # Template de base
├── accounts/
│   ├── login.html                      # Page de connexion
│   └── profile.html                    # Profil utilisateur
├── dashboard/
│   ├── home.html                       # Tableau de bord
│   ├── statistiques.html               # Statistiques
│   ├── indicateurs.html                # Liste indicateurs
│   └── activites.html                  # Liste activités
└── monitoring/
    ├── saisie_realisation.html         # Formulaire de saisie
    ├── liste_realisations.html         # Liste des réalisations
    ├── modifier_realisation.html       # Modification
    ├── liste_rapports.html             # Liste des rapports
    └── detail_rapport.html             # Détail d'un rapport
```

### 6. static/ - Fichiers Statiques

```
static/
├── css/
│   └── style.css       # Styles personnalisés
└── js/
    └── (vide)          # Scripts JavaScript futurs
```

## 🔄 Flux de Données

### 1. Saisie de Réalisation

```
Chargé de Projet
    ↓
Sélectionne Indicateur + Période
    ↓
Saisit Valeur + Commentaire
    ↓
Upload Justificatif (optionnel)
    ↓
Enregistrement dans Realisation
    ↓
Statut: En attente de validation
```

### 2. Validation

```
Coordonnateur/Évaluateur
    ↓
Consulte Liste des Réalisations
    ↓
Vérifie les données
    ↓
Clique sur Valider
    ↓
Realisation.valide = True
    ↓
Traçabilité: valide_par + date
```

### 3. Consultation

```
Utilisateur
    ↓
Tableau de Bord
    ↓
Filtrage selon rôle:
    - Chargé: Sa région uniquement
    - Coordonnateur/Évaluateur: Toutes les régions
    ↓
Affichage des statistiques
```

## 🗄️ Base de Données

### Tables Principales

1. **accounts_user** - Utilisateurs
2. **monitoring_composante** - Composantes
3. **monitoring_souscomposante** - Sous-composantes
4. **monitoring_indicateur** - Indicateurs
5. **monitoring_periode** - Périodes
6. **monitoring_realisation** - Réalisations
7. **monitoring_activite** - Activités
8. **monitoring_rapport** - Rapports

### Relations

```
Composante (1) ──→ (N) SousComposante
SousComposante (1) ──→ (N) Indicateur
Indicateur (1) ──→ (N) Realisation
Periode (1) ──→ (N) Realisation
User (1) ──→ (N) Realisation (saisi_par)
User (1) ──→ (N) Realisation (valide_par)
```

## 🔐 Permissions

### Par Rôle

| Fonctionnalité | Chargé Projet | Coordonnateur | Évaluateur | Admin |
|----------------|---------------|---------------|------------|-------|
| Voir sa région | ✅ | ✅ | ✅ | ✅ |
| Voir toutes régions | ❌ | ✅ | ✅ | ✅ |
| Saisir réalisations | ✅ | ✅ | ✅ | ✅ |
| Valider réalisations | ❌ | ✅ | ✅ | ✅ |
| Gérer indicateurs | ❌ | ❌ | ❌ | ✅ |
| Gérer utilisateurs | ❌ | ❌ | ❌ | ✅ |
| Interface admin | ❌ | ❌ | ❌ | ✅ |

## 📊 Indicateurs Clés

### Tableau de Bord

- Total indicateurs actifs
- Total réalisations saisies
- Réalisations validées
- Activités en cours
- Activités terminées

### Statistiques

- Réalisations par région
- Réalisations par période
- Taux de validation
- Budget exécuté par région
- Taux d'exécution des activités

## 🎨 Interface Utilisateur

### Technologies

- **Bootstrap 5.3** - Framework CSS
- **Bootstrap Icons** - Icônes
- **CSS personnalisé** - Styles ProSMAT

### Thème

- Couleur primaire: Bleu (#0d6efd)
- Couleur succès: Vert (#198754)
- Couleur warning: Jaune (#ffc107)
- Couleur info: Cyan (#0dcaf0)

## 🚀 Déploiement

### Développement
```bash
python manage.py runserver
```

### Production (à configurer)
- Serveur: Gunicorn ou uWSGI
- Base de données: PostgreSQL
- Serveur web: Nginx
- HTTPS: Let's Encrypt
- Fichiers statiques: WhiteNoise ou CDN

## 📝 Commandes Personnalisées

### init_prosmat
```bash
python manage.py init_prosmat
```

Crée:
- Utilisateurs de test
- Composantes de base
- Périodes 2026

## 🔧 Maintenance

### Sauvegarde
```bash
python manage.py dumpdata > backup.json
```

### Restauration
```bash
python manage.py loaddata backup.json
```

### Nettoyage
```bash
python manage.py clearsessions
```

## 📚 Documentation Associée

- `README.md` - Vue d'ensemble
- `GUIDE_INSTALLATION.md` - Installation détaillée
- `DEMARRAGE_RAPIDE.md` - Démarrage rapide
- `STRUCTURE_PROJET.md` - Ce fichier
