# 🌐 GUIDE DE DÉPLOIEMENT EN PRODUCTION

## ⚠️ NOTE IMPORTANTE

**Ce projet est une application Django, pas Streamlit.**

Streamlit est pour des dashboards data science simples. Django est un framework web complet qui nécessite un serveur d'application.

---

## 🎯 Options de Déploiement Recommandées

### Option 1: Railway (Recommandé - Gratuit pour commencer)

**Avantages**:
- ✅ Gratuit jusqu'à 500h/mois
- ✅ Déploiement automatique depuis GitHub
- ✅ PostgreSQL inclus
- ✅ Configuration simple

**Étapes**:
1. Créez un compte sur https://railway.app
2. Cliquez "New Project" → "Deploy from GitHub repo"
3. Sélectionnez votre dépôt `prosmat-suivi-evaluation`
4. Railway détecte automatiquement Django
5. Ajoutez une base PostgreSQL
6. Configurez les variables d'environnement (voir ci-dessous)
7. Déployez!

---

### Option 2: Render (Gratuit avec limitations)

**Avantages**:
- ✅ Tier gratuit disponible
- ✅ PostgreSQL gratuit
- ✅ SSL automatique

**Étapes**:
1. Créez un compte sur https://render.com
2. New → Web Service
3. Connectez votre dépôt GitHub
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn config.wsgi:application`
6. Ajoutez PostgreSQL
7. Configurez les variables d'environnement

---

### Option 3: Heroku (Payant depuis 2022)

**Note**: Heroku n'a plus de tier gratuit depuis novembre 2022.

**Étapes**:
1. Créez un compte sur https://heroku.com
2. Installez Heroku CLI
3. ```bash
   heroku login
   heroku create prosmat-se
   heroku addons:create heroku-postgresql:mini
   git push heroku main
   heroku run python manage.py migrate
   heroku run python manage.py createsuperuser
   ```

---

### Option 4: PythonAnywhere (Gratuit - Limité)

**Avantages**:
- ✅ Tier gratuit permanent
- ✅ Parfait pour prototypes
- ✅ Interface simple

**Limitations**:
- ⚠️ Pas de HTTPS sur tier gratuit
- ⚠️ Accès limité aux sites externes
- ⚠️ Performance limitée

**Guide**: Voir `DEPLOIEMENT_PYTHONANYWHERE.md`

---

## 🔧 Variables d'Environnement à Configurer

Pour toutes les plateformes, configurez ces variables:

```
SECRET_KEY=votre-cle-secrete-generee
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com,.railway.app
DATABASE_URL=postgresql://user:pass@host:5432/db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
```

### Générer une SECRET_KEY

```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

## 📋 Checklist Avant Déploiement

- [ ] Code poussé sur GitHub
- [ ] `.gitignore` configuré correctement
- [ ] `requirements.txt` à jour
- [ ] `Procfile` créé
- [ ] `runtime.txt` créé
- [ ] Variables d'environnement configurées
- [ ] Base de données PostgreSQL créée
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] Fichiers statiques collectés

---

## 🚀 Commandes Post-Déploiement

Après le premier déploiement:

```bash
# Migrations
python manage.py migrate

# Créer superuser
python manage.py createsuperuser

# Collecter fichiers statiques
python manage.py collectstatic --noinput

# Initialiser données (si commande existe)
python manage.py init_prosmat
```

---

## 🔒 Sécurité en Production

### Dans `config/settings.py`, ajoutez:

```python
import os
from decouple import config
import dj_database_url

# Sécurité
SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='').split(',')

# Base de données
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}

# HTTPS
if not DEBUG:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Fichiers statiques
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
```

---

## 📊 Monitoring et Logs

### Railway
```bash
railway logs
```

### Render
Logs disponibles dans le dashboard

### Heroku
```bash
heroku logs --tail
```

---

## 🆘 Dépannage

### Erreur: "Application Error"
- Vérifiez les logs
- Vérifiez les variables d'environnement
- Vérifiez que les migrations sont exécutées

### Erreur: "Static files not found"
```bash
python manage.py collectstatic --noinput
```

### Erreur: "Database connection failed"
- Vérifiez DATABASE_URL
- Vérifiez que PostgreSQL est bien créé

---

## 📞 Support

Pour plus d'aide:
- Railway: https://docs.railway.app
- Render: https://render.com/docs
- Heroku: https://devcenter.heroku.com
- PythonAnywhere: https://help.pythonanywhere.com

---

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
