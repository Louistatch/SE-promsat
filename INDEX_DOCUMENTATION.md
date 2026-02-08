# 📚 Index de la Documentation ProSMAT

Bienvenue dans la documentation complète du système de Suivi & Évaluation ProSMAT !

## 🚀 Démarrage Rapide

**Vous débutez avec ProSMAT ?** Commencez ici :

1. **[DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)** ⭐
   - Installation en 5 minutes
   - Premiers pas
   - Comptes de test
   - Checklist de démarrage

2. **[README.md](README.md)**
   - Vue d'ensemble du projet
   - Fonctionnalités principales
   - Structure du projet

## 📖 Documentation Complète

### Installation et Configuration

- **[GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md)**
  - Installation détaillée pas à pas
  - Configuration des indicateurs
  - Utilisation par rôle
  - Dépannage

- **[install.bat](install.bat)**
  - Script d'installation automatique Windows
  - Crée l'environnement virtuel
  - Installe les dépendances
  - Initialise la base de données

- **[start_new.bat](start_new.bat)**
  - Script de démarrage rapide
  - Lance le serveur Django

### Architecture et Structure

- **[STRUCTURE_PROJET.md](STRUCTURE_PROJET.md)**
  - Architecture détaillée
  - Organisation des fichiers
  - Modèles de données
  - Flux de données
  - Relations entre tables
  - Permissions par rôle

- **[RESUME_PROJET.md](RESUME_PROJET.md)**
  - Résumé complet du projet
  - Ce qui a été créé
  - Fonctionnalités implémentées
  - Technologies utilisées
  - Cas d'usage

### Déploiement

- **[DEPLOIEMENT.md](DEPLOIEMENT.md)**
  - Configuration de production
  - PostgreSQL
  - Gunicorn + Nginx
  - HTTPS avec Let's Encrypt
  - Sauvegardes automatiques
  - Monitoring
  - Sécurité

- **[config/settings_production.py](config/settings_production.py)**
  - Template de configuration production
  - Variables d'environnement
  - Paramètres de sécurité

### Évolution et Améliorations

- **[FONCTIONNALITES_FUTURES.md](FONCTIONNALITES_FUTURES.md)**
  - Roadmap des fonctionnalités
  - Graphiques interactifs
  - Import/Export Excel
  - API REST
  - Application mobile
  - Notifications
  - BI et Analytics
  - Priorisation

## 📂 Par Thématique

### 👤 Gestion des Utilisateurs

**Fichiers concernés :**
- `accounts/models.py` - Modèle User personnalisé
- `accounts/views.py` - Authentification
- `accounts/admin.py` - Interface admin
- `templates/accounts/` - Templates de connexion et profil

**Documentation :**
- [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md#1-accounts---gestion-des-utilisateurs)
- [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md#comptes-créés-automatiquement)

**Rôles disponibles :**
- Chargé de Projet (par région)
- Coordonnateur
- Évaluateur
- Administrateur

### 📊 Tableau de Bord

**Fichiers concernés :**
- `dashboard/views.py` - Vues et statistiques
- `dashboard/urls.py` - Routes
- `templates/dashboard/` - Templates

**Documentation :**
- [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md#2-dashboard---tableau-de-bord)
- [RESUME_PROJET.md](RESUME_PROJET.md#4-interface-utilisateur-complète)

**Pages disponibles :**
- Accueil avec statistiques
- Statistiques détaillées
- Liste des indicateurs
- Liste des activités

### 📈 Suivi & Évaluation

**Fichiers concernés :**
- `monitoring/models.py` - 7 modèles de données
- `monitoring/views.py` - Saisie et validation
- `monitoring/admin.py` - Interface admin complète
- `templates/monitoring/` - Templates de saisie

**Documentation :**
- [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md#3-monitoring---suivi--évaluation)
- [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md#configuration-des-indicateurs)

**Modèles :**
- Composante
- SousComposante
- Indicateur
- Periode
- Realisation
- Activite
- Rapport

### 🎨 Interface Utilisateur

**Fichiers concernés :**
- `templates/base.html` - Template de base
- `static/css/style.css` - Styles personnalisés
- `templates/*/` - Templates par app

**Technologies :**
- Bootstrap 5.3
- Bootstrap Icons
- CSS personnalisé

**Documentation :**
- [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md#5-templates---templates-html)

## 🔍 Par Cas d'Usage

### Je veux installer ProSMAT

1. Lisez [DEMARRAGE_RAPIDE.md](DEMARRAGE_RAPIDE.md)
2. Exécutez `install.bat`
3. Lancez `start_new.bat`
4. Ouvrez http://localhost:8000

### Je veux comprendre l'architecture

1. Lisez [STRUCTURE_PROJET.md](STRUCTURE_PROJET.md)
2. Consultez [RESUME_PROJET.md](RESUME_PROJET.md)
3. Explorez les fichiers de code

### Je veux déployer en production

1. Lisez [DEPLOIEMENT.md](DEPLOIEMENT.md)
2. Configurez [settings_production.py](config/settings_production.py)
3. Suivez la checklist de sécurité

### Je veux ajouter des fonctionnalités

1. Consultez [FONCTIONNALITES_FUTURES.md](FONCTIONNALITES_FUTURES.md)
2. Choisissez une fonctionnalité
3. Suivez les guides d'implémentation

### Je veux former des utilisateurs

1. Lisez [GUIDE_INSTALLATION.md](GUIDE_INSTALLATION.md#utilisation)
2. Utilisez les comptes de test
3. Suivez les cas d'usage dans [RESUME_PROJET.md](RESUME_PROJET.md#-cas-dusage)

## 📝 Fichiers de Configuration

### Configuration Django

- **[config/settings.py](config/settings.py)**
  - Configuration principale
  - Apps installées
  - Base de données
  - Authentification
  - Fichiers statiques

- **[config/urls.py](config/urls.py)**
  - Routes principales
  - Inclusion des apps

- **[config/wsgi.py](config/wsgi.py)**
  - Configuration WSGI pour déploiement

### Dépendances

- **[requirements.txt](requirements.txt)**
  - Django 6.0.2
  - Pillow (images)
  - openpyxl (Excel)

### Scripts

- **[install.bat](install.bat)** - Installation automatique
- **[start_new.bat](start_new.bat)** - Démarrage rapide
- **[start.bat](start.bat)** - Démarrage (ancien venv)

## 🗂️ Organisation des Fichiers

```
prosmat_se/
├── 📁 accounts/              # Gestion utilisateurs
├── 📁 dashboard/             # Tableau de bord
├── 📁 monitoring/            # Suivi-évaluation
├── 📁 config/                # Configuration Django
├── 📁 templates/             # Templates HTML
├── 📁 static/                # CSS, JS
├── 📁 media/                 # Fichiers uploadés
├── 📄 manage.py              # Script Django
├── 📄 requirements.txt       # Dépendances
├── 📄 *.bat                  # Scripts Windows
└── 📄 *.md                   # Documentation
```

## 🎓 Guides par Rôle

### Pour les Chargés de Projet

**Documentation :**
- [GUIDE_INSTALLATION.md - Pour les Chargés de Projet](GUIDE_INSTALLATION.md#pour-les-chargés-de-projet)
- [RESUME_PROJET.md - Cas d'usage](RESUME_PROJET.md#chargé-de-projet---région-maritime)

**Tâches principales :**
- Saisir des réalisations
- Consulter les indicateurs
- Voir les statistiques régionales
- Générer des rapports

### Pour les Coordonnateurs/Évaluateurs

**Documentation :**
- [GUIDE_INSTALLATION.md - Pour les Coordonnateurs](GUIDE_INSTALLATION.md#pour-les-coordonnateursÉvaluateurs)
- [RESUME_PROJET.md - Cas d'usage](RESUME_PROJET.md#coordonnateur-national)

**Tâches principales :**
- Vue d'ensemble nationale
- Valider les réalisations
- Comparer les régions
- Analyser les tendances

### Pour les Administrateurs

**Documentation :**
- [GUIDE_INSTALLATION.md - Pour l'Administrateur](GUIDE_INSTALLATION.md#pour-ladministrateur)
- [STRUCTURE_PROJET.md - Interface Admin](STRUCTURE_PROJET.md#3-monitoring---suivi--évaluation)

**Tâches principales :**
- Gérer les indicateurs
- Créer des utilisateurs
- Configurer les périodes
- Superviser le système

## 🔧 Maintenance et Support

### Dépannage

**Documentation :**
- [DEMARRAGE_RAPIDE.md - Dépannage](DEMARRAGE_RAPIDE.md#-dépannage)
- [GUIDE_INSTALLATION.md - Dépannage](GUIDE_INSTALLATION.md#dépannage)
- [DEPLOIEMENT.md - Dépannage Production](DEPLOIEMENT.md#-dépannage-production)

**Problèmes courants :**
- Python non reconnu
- Module Django introuvable
- Erreurs de migration
- Port déjà utilisé

### Sauvegardes

**Documentation :**
- [DEPLOIEMENT.md - Sauvegardes](DEPLOIEMENT.md#-sauvegardes)

**Scripts :**
- Sauvegarde automatique quotidienne
- Sauvegarde base de données
- Sauvegarde fichiers media

### Logs et Monitoring

**Documentation :**
- [DEPLOIEMENT.md - Monitoring](DEPLOIEMENT.md#-monitoring)

**Fichiers de logs :**
- Django logs
- Nginx logs
- Gunicorn logs

## 📊 Données et Modèles

### Modèles de Données

**Documentation :**
- [STRUCTURE_PROJET.md - Modèles](STRUCTURE_PROJET.md#modèles-principaux)

**Fichiers :**
- `accounts/models.py` - User
- `monitoring/models.py` - 7 modèles métier

### Base de Données

**Documentation :**
- [STRUCTURE_PROJET.md - Base de Données](STRUCTURE_PROJET.md#-base-de-données)
- [DEPLOIEMENT.md - PostgreSQL](DEPLOIEMENT.md#-base-de-données-postgresql)

**Tables principales :**
- accounts_user
- monitoring_indicateur
- monitoring_realisation
- monitoring_activite

## 🎯 Feuille de Route

### Fonctionnalités Actuelles

**Documentation :**
- [RESUME_PROJET.md - Fonctionnalités](RESUME_PROJET.md#-fonctionnalités-clés)

**Implémenté :**
- ✅ Authentification multi-rôles
- ✅ Saisie de réalisations
- ✅ Validation
- ✅ Tableau de bord
- ✅ Interface admin
- ✅ Rapports

### Fonctionnalités Futures

**Documentation :**
- [FONCTIONNALITES_FUTURES.md](FONCTIONNALITES_FUTURES.md)

**Prochaines étapes :**
- Graphiques interactifs
- Export Excel
- API REST
- Application mobile
- Notifications email

## 📞 Support et Contact

### Documentation

Si vous ne trouvez pas l'information :
1. Consultez l'index (ce fichier)
2. Utilisez la recherche dans les fichiers
3. Consultez le code source

### Problèmes Techniques

1. Vérifiez les logs
2. Consultez le dépannage
3. Contactez l'équipe technique

## ✅ Checklist Complète

### Installation
- [ ] Python installé
- [ ] Environnement virtuel créé
- [ ] Dépendances installées
- [ ] Base de données créée
- [ ] Données initiales chargées
- [ ] Serveur lancé
- [ ] Connexion réussie

### Configuration
- [ ] Indicateurs créés
- [ ] Utilisateurs configurés
- [ ] Périodes définies
- [ ] Composantes ajoutées

### Utilisation
- [ ] Saisie testée
- [ ] Validation testée
- [ ] Rapports générés
- [ ] Statistiques consultées

### Production
- [ ] PostgreSQL configuré
- [ ] Nginx installé
- [ ] HTTPS activé
- [ ] Sauvegardes configurées
- [ ] Monitoring en place

## 🎉 Conclusion

Cette documentation complète couvre tous les aspects de ProSMAT :
- Installation et démarrage
- Architecture et structure
- Utilisation par rôle
- Déploiement en production
- Évolutions futures

**Bon travail avec ProSMAT !** 🚀

---

**Dernière mise à jour :** Février 2026  
**Version :** 1.0  
**Auteur :** Équipe ProSMAT
