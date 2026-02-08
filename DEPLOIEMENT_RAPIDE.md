# 🚀 DÉPLOIEMENT RAPIDE - PROSMAT

## ✅ Prérequis Vérifiés

- ✅ Code sur GitHub: https://github.com/Louistatch/SE-promsat.git
- ✅ Fichiers de déploiement créés
- ✅ Configuration production prête

---

## 🚂 OPTION 1: RAILWAY (Recommandé - 10 min)

### Étape 1: Créer un Compte
1. Visitez https://railway.app
2. Cliquez "Login" → "Login with GitHub"
3. Autorisez Railway

### Étape 2: Déployer
1. Cliquez "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. Choisissez `Louistatch/SE-promsat`
4. Railway commence le déploiement automatiquement

### Étape 3: Ajouter PostgreSQL
1. Dans votre projet, cliquez "+ New"
2. Sélectionnez "Database" → "Add PostgreSQL"
3. PostgreSQL est créé et `DATABASE_URL` est configuré automatiquement

### Étape 4: Variables d'Environnement
Cliquez sur votre service → Variables → Ajoutez:

```env
DJANGO_SETTINGS_MODULE=config.settings_deploy
SECRET_KEY=GÉNÉREZ_UNE_CLÉ_SÉCURISÉE
DEBUG=False
ALLOWED_HOSTS=.railway.app
DISABLE_COLLECTSTATIC=1
```

**Générer SECRET_KEY**:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Étape 5: Créer un Superuser
1. Allez dans Settings → Deploy
2. Ouvrez le terminal
3. Exécutez:
```bash
python manage.py createsuperuser
```

### Étape 6: Accéder à l'Application
Railway génère une URL: `https://votre-app.railway.app`

✅ **C'est en ligne!**

---

## 🌐 OPTION 2: RENDER (Gratuit - 15 min)

### Étape 1: Créer un Compte
1. Visitez https://render.com
2. Inscrivez-vous avec GitHub

### Étape 2: Créer un Web Service
1. Cliquez "New +" → "Web Service"
2. Connectez votre dépôt GitHub: `SE-promsat`
3. Configurez:
   - **Name**: prosmat-se
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn config.wsgi:application`

### Étape 3: Ajouter PostgreSQL
1. Cliquez "New +" → "PostgreSQL"
2. Créez la base de données
3. Copiez l'URL interne

### Étape 4: Variables d'Environnement
Dans votre Web Service → Environment:

```env
DJANGO_SETTINGS_MODULE=config.settings_deploy
SECRET_KEY=VOTRE_CLÉ_SÉCURISÉE
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=postgresql://...
PYTHON_VERSION=3.11.9
```

### Étape 5: Déployer
Render déploie automatiquement!

### Étape 6: Créer un Superuser
1. Allez dans Shell
2. Exécutez:
```bash
python manage.py createsuperuser
```

✅ **C'est en ligne!**

---

## 🐍 OPTION 3: PYTHONANYWHERE (Gratuit - 20 min)

### Étape 1: Créer un Compte
1. Visitez https://www.pythonanywhere.com
2. Créez un compte gratuit

### Étape 2: Cloner le Dépôt
Dans le terminal Bash:
```bash
git clone https://github.com/Louistatch/SE-promsat.git
cd SE-promsat
```

### Étape 3: Créer un Environnement Virtuel
```bash
mkvirtualenv --python=/usr/bin/python3.11 prosmat
pip install -r requirements.txt
```

### Étape 4: Configurer l'Application Web
1. Allez dans "Web" → "Add a new web app"
2. Choisissez "Manual configuration" → Python 3.11
3. Configurez:
   - **Source code**: `/home/votre-username/SE-promsat`
   - **Working directory**: `/home/votre-username/SE-promsat`
   - **Virtualenv**: `/home/votre-username/.virtualenvs/prosmat`

### Étape 5: Configurer WSGI
Éditez `/var/www/votre-username_pythonanywhere_com_wsgi.py`:

```python
import os
import sys

path = '/home/votre-username/SE-promsat'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'config.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Étape 6: Migrations et Superuser
Dans le terminal:
```bash
cd SE-promsat
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic --noinput
```

### Étape 7: Recharger
Cliquez "Reload" dans l'onglet Web

✅ **C'est en ligne!**

---

## 🔧 Variables d'Environnement Complètes

### Minimales (Requises)
```env
DJANGO_SETTINGS_MODULE=config.settings_deploy
SECRET_KEY=votre-cle-secrete-unique
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,.railway.app,.onrender.com
DATABASE_URL=postgresql://user:pass@host:5432/db
```

### Complètes (Recommandées)
```env
# Django
DJANGO_SETTINGS_MODULE=config.settings_deploy
SECRET_KEY=votre-cle-secrete-unique
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,.railway.app

# Base de données
DATABASE_URL=postgresql://user:pass@host:5432/db

# Email (optionnel)
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@prosmat.tg

# CORS (si API externe)
CORS_ALLOWED_ORIGINS=https://votre-frontend.com

# Sécurité
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## ✅ Checklist Post-Déploiement

- [ ] Application accessible via URL
- [ ] PostgreSQL connecté
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] Page de connexion fonctionne
- [ ] Dashboard accessible
- [ ] Exports Excel/PDF fonctionnent
- [ ] API REST accessible (/api/)
- [ ] Fichiers statiques chargés

---

## 🆘 Dépannage Rapide

### Erreur: "Application Error"
```bash
# Vérifiez les logs
railway logs  # Railway
# ou consultez les logs dans le dashboard Render/PythonAnywhere
```

### Erreur: "Static files not found"
```bash
python manage.py collectstatic --noinput
```

### Erreur: "Database connection failed"
Vérifiez que `DATABASE_URL` est bien configuré

### Erreur: "Bad Request (400)"
Ajoutez votre domaine dans `ALLOWED_HOSTS`

---

## 📊 Comparaison des Plateformes

| Plateforme | Gratuit | PostgreSQL | SSL | Facilité |
|------------|---------|------------|-----|----------|
| Railway | 500h/mois | ✅ | ✅ | ⭐⭐⭐⭐⭐ |
| Render | Limité | ✅ | ✅ | ⭐⭐⭐⭐ |
| PythonAnywhere | Permanent | ❌ (SQLite) | ⚠️ | ⭐⭐⭐ |
| Heroku | ❌ Payant | ✅ | ✅ | ⭐⭐⭐⭐⭐ |

**Recommandation**: Railway pour production, PythonAnywhere pour prototype

---

## 🎯 Prochaines Étapes

1. ✅ Choisissez une plateforme
2. ✅ Suivez les étapes ci-dessus
3. ✅ Testez l'application
4. ✅ Configurez les emails (optionnel)
5. ✅ Ajoutez un domaine personnalisé (optionnel)
6. ✅ Invitez votre équipe

---

**Besoin d'aide?** Consultez les guides détaillés:
- `DEPLOIEMENT_RAILWAY_GUIDE.md` - Guide Railway complet
- `DEPLOIEMENT_PRODUCTION.md` - Toutes les options
- `DEPLOIEMENT_PYTHONANYWHERE.md` - Guide PythonAnywhere

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
