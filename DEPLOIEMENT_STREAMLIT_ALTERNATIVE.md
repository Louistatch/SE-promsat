# ⚠️ IMPORTANT - À PROPOS DE STREAMLIT

## Ce Projet N'est PAS Compatible avec Streamlit

**ProSMAT** est une application **Django** complète, pas une application Streamlit.

### Différences Clés

| Caractéristique | Django (ProSMAT) | Streamlit |
|----------------|------------------|-----------|
| Type | Framework web complet | Framework dashboards simples |
| Base de données | PostgreSQL/SQLite avec ORM | Fichiers CSV/Excel |
| Authentification | Système complet intégré | Basique ou externe |
| API REST | Oui (DRF) | Non natif |
| Templates HTML | Oui | Non (Python pur) |
| Déploiement | Serveur WSGI/ASGI | Streamlit Cloud |

---

## 🚀 Options de Déploiement pour Django

### Option 1: Railway (Recommandé)
- ✅ Gratuit jusqu'à 500h/mois
- ✅ PostgreSQL inclus
- ✅ Déploiement automatique depuis GitHub
- 🔗 https://railway.app

**Étapes**:
1. Créez un compte sur Railway
2. New Project → Deploy from GitHub
3. Sélectionnez `SE-promsat`
4. Railway détecte automatiquement Django
5. Ajoutez PostgreSQL
6. Configurez les variables d'environnement
7. Déployez!

---

### Option 2: Render
- ✅ Tier gratuit disponible
- ✅ PostgreSQL gratuit
- ✅ SSL automatique
- 🔗 https://render.com

**Étapes**:
1. Créez un compte sur Render
2. New → Web Service
3. Connectez GitHub: `SE-promsat`
4. Build: `pip install -r requirements.txt`
5. Start: `gunicorn config.wsgi:application`
6. Ajoutez PostgreSQL
7. Configurez les variables d'environnement

---

### Option 3: PythonAnywhere (Gratuit - Limité)
- ✅ Tier gratuit permanent
- ✅ Interface simple
- ⚠️ Pas de HTTPS sur tier gratuit
- 🔗 https://www.pythonanywhere.com

**Guide complet**: Voir `DEPLOIEMENT_PYTHONANYWHERE.md`

---

### Option 4: Heroku (Payant)
- ⚠️ Plus de tier gratuit depuis 2022
- ✅ Très stable et mature
- 🔗 https://heroku.com

---

## 🔧 Variables d'Environnement Requises

Pour toutes les plateformes:

```env
SECRET_KEY=votre-cle-secrete-django
DEBUG=False
ALLOWED_HOSTS=votre-domaine.com
DATABASE_URL=postgresql://user:pass@host:5432/db
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
```

---

## 📋 Fichiers de Déploiement Créés

✅ `Procfile` - Configuration pour Heroku/Railway/Render
✅ `runtime.txt` - Version Python
✅ `requirements.txt` - Dépendances (avec gunicorn, psycopg2)
✅ `.env.example` - Template variables d'environnement
✅ `.gitignore` - Fichiers à exclure

---

## 🎯 Pourquoi Pas Streamlit?

Streamlit est excellent pour:
- 📊 Dashboards data science rapides
- 📈 Visualisations interactives
- 🔬 Prototypes ML/AI
- 📉 Analyses exploratoires

Mais ProSMAT nécessite:
- 👥 Système d'authentification multi-utilisateurs
- 🗄️ Base de données relationnelle complexe
- 📝 Formulaires de saisie avancés
- 📊 Exports Excel/PDF personnalisés
- 🔔 Système de notifications
- 🌐 API REST complète
- 🔒 Gestion des permissions par région

**Conclusion**: Django est le bon choix pour ProSMAT!

---

## 📖 Documentation de Déploiement

Consultez ces guides:
1. `DEPLOIEMENT_GITHUB.md` - ✅ Déjà fait!
2. `DEPLOIEMENT_PRODUCTION.md` - Guide complet
3. `DEPLOIEMENT_PYTHONANYWHERE.md` - Option gratuite

---

## 🆘 Besoin d'Aide?

Pour déployer sur Railway (recommandé):
1. Visitez https://railway.app
2. Connectez votre compte GitHub
3. Sélectionnez le dépôt `SE-promsat`
4. Suivez les instructions à l'écran

Le déploiement prend environ 5-10 minutes!

---

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation Django
