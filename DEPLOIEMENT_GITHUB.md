# 🚀 GUIDE DE DÉPLOIEMENT - GITHUB

## Étape 1: Initialiser Git (si pas déjà fait)

```bash
cd C:\Users\HP\Downloads\prosmat_se
git init
```

## Étape 2: Configurer Git

```bash
git config user.name "Votre Nom"
git config user.email "votre.email@example.com"
```

## Étape 3: Ajouter les Fichiers

```bash
git add .
git commit -m "Initial commit - ProSMAT Système de Suivi-Évaluation"
```

## Étape 4: Créer un Dépôt sur GitHub

1. Allez sur https://github.com
2. Cliquez sur "New repository"
3. Nom suggéré: `prosmat-suivi-evaluation`
4. Description: "Système de Suivi-Évaluation pour le Projet ProSMAT au Togo"
5. Choisissez "Private" (recommandé pour données sensibles)
6. Ne cochez PAS "Initialize with README" (vous en avez déjà un)
7. Cliquez "Create repository"

## Étape 5: Lier le Dépôt Local à GitHub

Remplacez `VOTRE-USERNAME` par votre nom d'utilisateur GitHub:

```bash
git remote add origin https://github.com/VOTRE-USERNAME/prosmat-suivi-evaluation.git
git branch -M main
git push -u origin main
```

## Étape 6: Vérification

Visitez votre dépôt sur GitHub pour vérifier que tous les fichiers sont bien uploadés.

---

## ⚠️ IMPORTANT - Sécurité

### Fichiers Exclus (.gitignore)
Les fichiers suivants sont automatiquement exclus:
- ✅ `db.sqlite3` (base de données locale)
- ✅ `venv/` et `venv_prosmat/` (environnements virtuels)
- ✅ `.env` (variables d'environnement)
- ✅ `*.xlsx` (fichiers Excel avec données sensibles)
- ✅ `media/` (uploads utilisateurs)

### Avant de Pousser sur GitHub
1. ✅ Vérifiez que `.gitignore` est bien configuré
2. ✅ Ne committez JAMAIS de mots de passe ou clés API
3. ✅ Utilisez `.env` pour les secrets (déjà dans .gitignore)

---

## 🔄 Commandes Git Utiles

### Ajouter des Modifications
```bash
git add .
git commit -m "Description des changements"
git push
```

### Voir l'État
```bash
git status
```

### Voir l'Historique
```bash
git log --oneline
```

### Créer une Branche
```bash
git checkout -b nom-de-la-branche
```

---

## 📝 Prochaines Étapes

Après avoir poussé sur GitHub, consultez:
- `DEPLOIEMENT_PRODUCTION.md` pour déployer sur Heroku/Railway/Render
- `DEPLOIEMENT_PYTHONANYWHERE.md` pour un déploiement simple et gratuit

---

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
