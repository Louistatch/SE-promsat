# 🚀 Déploiement sur GitHub

## 📋 Prérequis

- Compte GitHub: https://github.com/
- Git installé sur votre machine
- Accès au terminal/PowerShell

## 🔧 Étape 1: Vérifier Git

```bash
# Vérifier que Git est installé
git --version

# Si Git n'est pas installé, téléchargez-le:
# https://git-scm.com/downloads
```

## 🎯 Étape 2: Créer un Dépôt sur GitHub

1. Allez sur https://github.com/
2. Cliquez sur le bouton **"New"** (ou **"+"** en haut à droite)
3. Remplissez les informations:
   - **Repository name**: `prosmat` (ou `prosmat-togo`)
   - **Description**: "Système de Suivi-Évaluation ProSMAT - Togo"
   - **Visibility**: 
     - ✅ **Private** (recommandé pour un projet professionnel)
     - ⚠️ Public (si vous voulez le partager)
   - ❌ Ne cochez PAS "Initialize with README" (on a déjà un README)
4. Cliquez sur **"Create repository"**

## 📦 Étape 3: Initialiser Git Localement

Ouvrez PowerShell dans le dossier du projet et exécutez:

```bash
# Initialiser le dépôt Git
git init

# Vérifier le statut
git status
```

## 🔐 Étape 4: Vérifier les Fichiers Sensibles

**IMPORTANT**: Vérifiez que ces fichiers sont bien dans `.gitignore`:

```bash
# Vérifier que ces fichiers ne seront PAS envoyés sur GitHub
git status

# Ces fichiers NE DOIVENT PAS apparaître:
# - .env
# - firebase-credentials.json
# - prosmat-auth-firebase-adminsdk-*.json
# - db.sqlite3
# - __pycache__/
# - *.pyc
```

Si ces fichiers apparaissent, ils sont déjà exclus par `.gitignore` ✅

## 📝 Étape 5: Premier Commit

```bash
# Ajouter tous les fichiers
git add .

# Créer le premier commit
git commit -m "Initial commit: ProSMAT Suivi-Évaluation

- Authentification Firebase (Email/Password + Google OAuth)
- Gestion des rôles et régions
- Tableaux de bord interactifs
- Génération automatique de rapports
- Interface admin personnalisée
- Support PostgreSQL (Neon) et SQLite
- Documentation complète"

# Vérifier le commit
git log --oneline
```

## 🔗 Étape 6: Connecter au Dépôt GitHub

Remplacez `VOTRE-USERNAME` et `VOTRE-REPO` par vos valeurs:

```bash
# Ajouter le dépôt distant
git remote add origin https://github.com/VOTRE-USERNAME/VOTRE-REPO.git

# Vérifier la connexion
git remote -v
```

**Exemple:**
```bash
git remote add origin https://github.com/tatchida/prosmat.git
```

## 🚀 Étape 7: Pousser sur GitHub

```bash
# Renommer la branche en 'main' (si nécessaire)
git branch -M main

# Pousser le code sur GitHub
git push -u origin main
```

**Note**: GitHub vous demandera peut-être de vous authentifier:
- Utilisez votre nom d'utilisateur GitHub
- Pour le mot de passe, utilisez un **Personal Access Token** (pas votre mot de passe)

### Créer un Personal Access Token

1. Allez sur: https://github.com/settings/tokens
2. Cliquez sur **"Generate new token"** → **"Generate new token (classic)"**
3. Donnez un nom: "ProSMAT Deploy"
4. Cochez: `repo` (Full control of private repositories)
5. Cliquez sur **"Generate token"**
6. **COPIEZ LE TOKEN** (vous ne pourrez plus le voir!)
7. Utilisez ce token comme mot de passe lors du `git push`

## ✅ Étape 8: Vérifier sur GitHub

1. Allez sur votre dépôt: `https://github.com/VOTRE-USERNAME/VOTRE-REPO`
2. Vérifiez que tous les fichiers sont présents
3. Vérifiez que le README.md s'affiche correctement
4. **IMPORTANT**: Vérifiez que les fichiers sensibles ne sont PAS là:
   - ❌ `.env`
   - ❌ `firebase-credentials.json`
   - ❌ `db.sqlite3`

## 🔄 Étape 9: Commits Futurs

Pour les modifications futures:

```bash
# Voir les fichiers modifiés
git status

# Ajouter les fichiers modifiés
git add .

# Ou ajouter des fichiers spécifiques
git add fichier1.py fichier2.html

# Créer un commit avec un message descriptif
git commit -m "Description de vos modifications"

# Pousser sur GitHub
git push
```

### Exemples de Messages de Commit

```bash
# Nouvelle fonctionnalité
git commit -m "feat: Ajout de la génération automatique de rapports"

# Correction de bug
git commit -m "fix: Correction de l'erreur de validation des réalisations"

# Amélioration
git commit -m "improve: Amélioration de l'interface des rapports"

# Documentation
git commit -m "docs: Mise à jour du guide d'installation"

# Style/Design
git commit -m "style: Amélioration du design de la page de connexion"
```

## 🌿 Étape 10: Branches (Optionnel)

Pour travailler sur des fonctionnalités sans affecter le code principal:

```bash
# Créer une nouvelle branche
git checkout -b feature/nouvelle-fonctionnalite

# Faire vos modifications...
git add .
git commit -m "Ajout de la nouvelle fonctionnalité"

# Pousser la branche
git push -u origin feature/nouvelle-fonctionnalite

# Retourner sur main
git checkout main

# Fusionner la branche (après tests)
git merge feature/nouvelle-fonctionnalite
git push
```

## 📊 Étape 11: Ajouter des Badges (Optionnel)

Ajoutez des badges au README pour montrer le statut du projet:

```markdown
![Django](https://img.shields.io/badge/Django-5.2-green.svg)
![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
![Firebase](https://img.shields.io/badge/Firebase-Auth-orange.svg)
![Status](https://img.shields.io/badge/Status-Production-success.svg)
```

## 🔒 Sécurité: Fichiers à NE JAMAIS Commiter

**ATTENTION**: Ces fichiers contiennent des informations sensibles et ne doivent JAMAIS être sur GitHub:

❌ `.env` - Variables d'environnement (clés secrètes)
❌ `firebase-credentials.json` - Credentials Firebase
❌ `prosmat-auth-firebase-adminsdk-*.json` - Clés Firebase
❌ `db.sqlite3` - Base de données (peut contenir des données sensibles)
❌ `*.log` - Logs (peuvent contenir des informations sensibles)
❌ `media/` - Fichiers uploadés par les utilisateurs

Ces fichiers sont déjà dans `.gitignore` ✅

## 🚨 Si Vous Avez Accidentellement Commité un Fichier Sensible

**URGENT**: Si vous avez poussé un fichier sensible sur GitHub:

```bash
# 1. Supprimer le fichier du dépôt (mais le garder localement)
git rm --cached fichier-sensible.json

# 2. Commiter la suppression
git commit -m "Remove sensitive file"

# 3. Pousser
git push

# 4. IMPORTANT: Révoquer les clés/tokens exposés
# - Firebase: Régénérer les credentials
# - Django: Changer SECRET_KEY
# - Tokens: Révoquer et créer de nouveaux
```

## 📞 Support

### Problèmes Courants

**Problème**: `git: command not found`
**Solution**: Installez Git depuis https://git-scm.com/downloads

**Problème**: `Permission denied (publickey)`
**Solution**: Utilisez HTTPS au lieu de SSH, ou configurez une clé SSH

**Problème**: `rejected - non-fast-forward`
**Solution**: 
```bash
git pull origin main --rebase
git push
```

**Problème**: Fichiers sensibles apparaissent dans `git status`
**Solution**: Vérifiez `.gitignore` et ajoutez les fichiers manquants

## 🎉 Félicitations!

Votre projet ProSMAT est maintenant sur GitHub! 🚀

### Prochaines Étapes

1. ✅ Inviter des collaborateurs (Settings → Collaborators)
2. ✅ Configurer les GitHub Actions (CI/CD)
3. ✅ Ajouter une licence (Settings → Add license)
4. ✅ Créer des Issues pour suivre les tâches
5. ✅ Utiliser les Projects pour la gestion de projet

### Liens Utiles

- Votre dépôt: `https://github.com/VOTRE-USERNAME/VOTRE-REPO`
- Documentation Git: https://git-scm.com/doc
- GitHub Guides: https://guides.github.com/

---

**Développé avec ❤️ pour ProSMAT - Togo**
