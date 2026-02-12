# ✅ Configuration Finale ProSMAT

## 🎯 Architecture Simplifiée

### Un Seul Fichier Settings
- ✅ `config/settings.py` - Utilisé partout (développement ET production)
- ❌ Supprimé: `settings_deploy.py`, `settings_neon.py`, `settings_production.py`

### Base de Données Unique
- ✅ **Neon PostgreSQL** utilisé partout
- ❌ Plus de SQLite en développement
- ✅ Même base de données en local et en production

---

## 📊 État Actuel

### Base de Données Neon
- **URL**: `postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb`
- **Composantes**: 9
- **Sous-composantes**: 6
- **Indicateurs**: 80 (importés depuis Excel)
- **Périodes**: 9 (2024-2026, trimestres)
- **Utilisateurs**: 2 (admin@prosmat.tg, tatchida@gmail.com)

### Authentification Firebase
- **Méthode principale**: Firebase (Email/Password + Google Sign-In)
- **Backup**: Django Admin
- **Admins automatiques**: 
  - tatchida@gmail.com
  - admin@prosmat.tg

### Code
- **Repository**: https://github.com/Louistatch/SE-promsat
- **Branch**: main
- **Dernier commit**: Simplification settings + 80 indicateurs

---

## 🔧 Configuration Locale

### Fichier `.env`
```env
# Django
SECRET_KEY=django-insecure-prosmat-2026-change-in-production-key-12345
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Neon PostgreSQL (utilisé partout)
DATABASE_URL=postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require

# Firebase
FIREBASE_API_KEY=AIzaSyDzRKnJR3COQgOsEH93HKAYevuwuVPaImY
FIREBASE_AUTH_DOMAIN=prosmat-auth.firebaseapp.com
FIREBASE_PROJECT_ID=prosmat-auth
FIREBASE_STORAGE_BUCKET=prosmat-auth.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=846919772188
FIREBASE_APP_ID=1:846919772188:web:e2f3867ac0772dd75fd7d9
FIREBASE_MEASUREMENT_ID=G-FTEKHPDW2V
```

### Commandes Utiles

#### Développement Local
```bash
# Activer l'environnement virtuel
venv_prosmat\Scripts\activate

# Lancer le serveur (utilise Neon)
python manage.py runserver

# Créer un superuser
python manage.py createsuperuser

# Migrations
python manage.py makemigrations
python manage.py migrate
```

#### Vérifier Neon
```bash
# Vérifier les données sur Neon
python verifier_neon.py

# Importer des indicateurs depuis Excel
python importer_tous_indicateurs.py
```

---

## 🚀 Configuration Render

### Variables d'Environnement Render

À configurer dans Render Dashboard:

```env
# Django
SECRET_KEY=<générer-une-nouvelle-clé-sécurisée>
DEBUG=False
ALLOWED_HOSTS=.onrender.com

# Neon PostgreSQL
DATABASE_URL=postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require

# Firebase (mêmes valeurs que local)
FIREBASE_API_KEY=AIzaSyDzRKnJR3COQgOsEH93HKAYevuwuVPaImY
FIREBASE_AUTH_DOMAIN=prosmat-auth.firebaseapp.com
FIREBASE_PROJECT_ID=prosmat-auth
FIREBASE_STORAGE_BUCKET=prosmat-auth.firebasestorage.app
FIREBASE_MESSAGING_SENDER_ID=846919772188
FIREBASE_APP_ID=1:846919772188:web:e2f3867ac0772dd75fd7d9
FIREBASE_MEASUREMENT_ID=G-FTEKHPDW2V

# Firebase Admin SDK (base64)
FIREBASE_CREDENTIALS_BASE64=<contenu-de-firebase-credentials-base64.txt>
```

### Fichiers Render

#### `build.sh`
```bash
#!/usr/bin/env bash
set -o errexit

echo "🚀 Début du build ProSMAT..."

# Installer les dépendances
pip install -r requirements.txt

# Décoder Firebase credentials
if [ ! -z "$FIREBASE_CREDENTIALS_BASE64" ]; then
    echo "$FIREBASE_CREDENTIALS_BASE64" | base64 -d > firebase-credentials.json
fi

# Collecter les fichiers statiques
python manage.py collectstatic --no-input

# Migrations
python manage.py migrate

# Charger les données initiales (si base vide)
python manage.py charger_donnees

echo "✅ Build terminé!"
```

#### `render.yaml`
```yaml
services:
  - type: web
    name: prosmat
    env: python
    region: frankfurt
    plan: free
    branch: main
    buildCommand: "./build.sh"
    startCommand: "gunicorn config.wsgi:application"
```

---

## 📝 Workflow de Développement

### 1. Développement Local
```bash
# Travailler en local (utilise Neon directement)
python manage.py runserver

# Tester les changements
# Faire des commits
git add .
git commit -m "feat: nouvelle fonctionnalité"
```

### 2. Déploiement
```bash
# Pousser sur GitHub
git push origin main

# Render redéploie automatiquement
# Surveiller les logs sur Render Dashboard
```

### 3. Vérification
```bash
# Vérifier que les données sont sur Neon
# Via Neon Console: https://console.neon.tech
SELECT COUNT(*) FROM monitoring_indicateur;

# Ou via l'application Render
# Se connecter avec tatchida@gmail.com
```

---

## 🔐 Sécurité

### En Production (Render)
- ✅ `DEBUG=False`
- ✅ `SECRET_KEY` unique et sécurisée
- ✅ `ALLOWED_HOSTS` restreint à `.onrender.com`
- ✅ HTTPS activé automatiquement par Render
- ✅ Firebase credentials en base64 (pas de fichier)

### En Développement (Local)
- ⚠️ `DEBUG=True` (OK pour dev)
- ⚠️ `ALLOWED_HOSTS=*` (OK pour dev)
- ✅ Même base Neon (données synchronisées)

---

## 🎉 Avantages de Cette Configuration

### Simplicité
- ✅ Un seul fichier `settings.py`
- ✅ Même base de données partout
- ✅ Pas de confusion entre environnements

### Cohérence
- ✅ Données synchronisées (local = production)
- ✅ Pas de migration de données nécessaire
- ✅ Tests sur vraies données

### Maintenance
- ✅ Moins de fichiers à gérer
- ✅ Configuration centralisée dans `.env`
- ✅ Déploiement automatique via GitHub

---

## 📚 Documentation Complémentaire

- `ADMINS_AUTOMATIQUES.md` - Gestion des admins
- `CHARGER_DONNEES_RENDER.md` - Chargement données initial
- `DEPLOIEMENT_RENDER.md` - Guide déploiement Render
- `IMPORTER_INDICATEURS.md` - Import indicateurs Excel
- `VERIFIER_NEON.md` - Vérification base Neon

---

## 🆘 Dépannage

### Problème: "No DATABASE_URL"
**Solution**: Vérifier que `.env` contient `DATABASE_URL`

### Problème: "Connection refused"
**Solution**: Vérifier que Neon est accessible (pas de firewall)

### Problème: "Indicateurs non visibles"
**Solution**: 
```bash
python verifier_neon.py
# Vérifier dans Neon Console
```

### Problème: "Admin non reconnu"
**Solution**: Vérifier que l'email est dans la liste des admins automatiques
```python
# Dans accounts/firebase_auth.py
admin_emails = ['tatchida@gmail.com', 'admin@prosmat.tg']
```

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Configuration finale - 12 février 2026*
