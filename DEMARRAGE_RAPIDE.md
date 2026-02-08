# 🚀 Démarrage Rapide - ProSMAT

## ⚠️ Prérequis

Avant de commencer, assurez-vous d'avoir:
- **Python 3.10 ou supérieur** installé
- **pip** (gestionnaire de paquets Python)

### Vérifier Python
```bash
python --version
```
ou
```bash
python3 --version
```

Si Python n'est pas installé, téléchargez-le depuis: https://www.python.org/downloads/

## 📦 Installation

### Option 1: Installation Automatique (Recommandé)

1. **Ouvrez PowerShell dans le dossier du projet**
   ```powershell
   cd C:\Users\HP\Downloads\prosmat_se
   ```

2. **Exécutez le script d'installation**
   ```powershell
   .\install.bat
   ```

### Option 2: Installation Manuelle

#### Étape 1: Créer un environnement virtuel
```powershell
python -m venv venv_new
```

#### Étape 2: Activer l'environnement virtuel
```powershell
.\venv_new\Scripts\activate
```

Vous devriez voir `(venv_new)` au début de votre ligne de commande.

#### Étape 3: Installer les dépendances
```powershell
pip install -r requirements.txt
```

#### Étape 4: Créer la base de données
```powershell
python manage.py makemigrations
python manage.py migrate
```

#### Étape 5: Initialiser les données
```powershell
python manage.py init_prosmat
```

Cette commande crée:
- ✅ Compte administrateur
- ✅ Comptes pour les 5 régions
- ✅ Compte coordonnateur
- ✅ Compte évaluateur
- ✅ Composantes de base
- ✅ Périodes 2026

#### Étape 6: Créer un superutilisateur (optionnel)
```powershell
python manage.py createsuperuser
```

#### Étape 7: Lancer le serveur
```powershell
python manage.py runserver
```

## 🌐 Accès à l'Application

Une fois le serveur démarré, ouvrez votre navigateur:

- **Application principale:** http://localhost:8000
- **Interface d'administration:** http://localhost:8000/admin

## 👤 Comptes de Test

### Administrateur
```
Username: admin
Password: admin123
```

### Coordonnateur
```
Username: coordonnateur
Password: prosmat2026
```

### Évaluateur
```
Username: evaluateur
Password: prosmat2026
```

### Chargés de Projet (par région)

| Région | Username | Password |
|--------|----------|----------|
| Maritime | charge_maritime | prosmat2026 |
| Plateaux | charge_plateaux | prosmat2026 |
| Centrale | charge_centrale | prosmat2026 |
| Kara | charge_kara | prosmat2026 |
| Savanes | charge_savanes | prosmat2026 |

## 📝 Premiers Pas

### 1. Connexion
- Allez sur http://localhost:8000
- Connectez-vous avec un des comptes ci-dessus

### 2. Configuration des Indicateurs (Admin)
- Connectez-vous à http://localhost:8000/admin avec admin/admin123
- Allez dans "Indicateurs"
- Cliquez sur "Ajouter indicateur"
- Remplissez les informations

### 3. Saisie de Réalisations (Chargé de Projet)
- Connectez-vous avec un compte régional
- Menu "Saisie"
- Sélectionnez un indicateur et une période
- Entrez la valeur réalisée

### 4. Validation (Coordonnateur/Évaluateur)
- Connectez-vous avec coordonnateur ou evaluateur
- Menu "Réalisations"
- Cliquez sur le bouton ✓ pour valider

## 🔧 Commandes Utiles

### Créer des migrations
```powershell
python manage.py makemigrations
```

### Appliquer les migrations
```powershell
python manage.py migrate
```

### Créer un superutilisateur
```powershell
python manage.py createsuperuser
```

### Collecter les fichiers statiques
```powershell
python manage.py collectstatic
```

### Lancer le serveur
```powershell
python manage.py runserver
```

### Lancer sur un port différent
```powershell
python manage.py runserver 8001
```

## 🐛 Dépannage

### Problème: "Python n'est pas reconnu"
**Solution:** Installez Python depuis https://www.python.org/downloads/
Cochez "Add Python to PATH" pendant l'installation.

### Problème: "pip n'est pas reconnu"
**Solution:**
```powershell
python -m ensurepip --upgrade
```

### Problème: "Module 'django' not found"
**Solution:**
```powershell
pip install -r requirements.txt
```

### Problème: "Table doesn't exist"
**Solution:**
```powershell
python manage.py migrate
```

### Problème: "Port 8000 already in use"
**Solution:**
```powershell
python manage.py runserver 8001
```

### Réinitialiser complètement
```powershell
# Supprimer la base de données
del db.sqlite3

# Recréer tout
python manage.py migrate
python manage.py init_prosmat
```

## 📚 Documentation Complète

Pour plus de détails, consultez:
- `README.md` - Vue d'ensemble du projet
- `GUIDE_INSTALLATION.md` - Guide d'installation détaillé

## 🆘 Support

En cas de problème:
1. Vérifiez que Python est bien installé
2. Vérifiez que l'environnement virtuel est activé
3. Consultez les logs dans la console
4. Contactez l'équipe technique ProSMAT

## ✅ Checklist de Démarrage

- [ ] Python installé (version 3.10+)
- [ ] Environnement virtuel créé et activé
- [ ] Dépendances installées
- [ ] Base de données créée (migrate)
- [ ] Données initiales chargées (init_prosmat)
- [ ] Serveur lancé
- [ ] Connexion réussie à l'application
- [ ] Test de saisie d'une réalisation

Bon travail avec ProSMAT! 🎉
