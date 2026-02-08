# 🚂 GUIDE RAPIDE - DÉPLOIEMENT SUR RAILWAY

## ⏱️ Temps Estimé: 10 Minutes

Railway est la solution recommandée pour déployer ProSMAT rapidement et gratuitement.

---

## 📋 Prérequis

✅ Projet sur GitHub: https://github.com/Louistatch/SE-promsat.git
✅ Compte GitHub actif
✅ Compte Railway (gratuit)

---

## 🚀 Étapes de Déploiement

### Étape 1: Créer un Compte Railway (2 min)

1. Visitez https://railway.app
2. Cliquez "Login" → "Login with GitHub"
3. Autorisez Railway à accéder à votre GitHub
4. Compte créé! ✅

---

### Étape 2: Créer un Nouveau Projet (3 min)

1. Cliquez "New Project"
2. Sélectionnez "Deploy from GitHub repo"
3. Cherchez et sélectionnez `SE-promsat`
4. Railway commence automatiquement le déploiement

**Railway détecte automatiquement**:
- ✅ Python/Django
- ✅ `requirements.txt`
- ✅ `Procfile`
- ✅ `runtime.txt`

---

### Étape 3: Ajouter PostgreSQL (2 min)

1. Dans votre projet, cliquez "+ New"
2. Sélectionnez "Database" → "Add PostgreSQL"
3. PostgreSQL est créé automatiquement
4. Railway configure automatiquement `DATABASE_URL`

---

### Étape 4: Configurer les Variables d'Environnement (3 min)

1. Cliquez sur votre service Django
2. Allez dans l'onglet "Variables"
3. Ajoutez ces variables:

```env
SECRET_KEY=django-insecure-CHANGEZ-MOI-EN-PRODUCTION
DEBUG=False
ALLOWED_HOSTS=.railway.app
DISABLE_COLLECTSTATIC=1
```

**Générer une SECRET_KEY sécurisée**:
```python
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### Étape 5: Exécuter les Migrations (1 min)

Railway exécute automatiquement les migrations grâce au `Procfile`:
```
release: python manage.py migrate
```

Si besoin, vous pouvez exécuter des commandes manuellement:
1. Allez dans "Settings" → "Deploy"
2. Utilisez le terminal intégré

---

### Étape 6: Créer un Superuser

**Option A: Via Terminal Railway**
1. Cliquez sur votre service
2. Allez dans "Settings"
3. Ouvrez le terminal
4. Exécutez:
```bash
python manage.py createsuperuser
```

**Option B: Via Commande Locale**
```bash
railway run python manage.py createsuperuser
```

---

### Étape 7: Accéder à l'Application

1. Railway génère automatiquement une URL
2. Format: `https://votre-app.railway.app`
3. Cliquez sur l'URL dans le dashboard
4. Votre application est en ligne! 🎉

---

## 🔧 Configuration Avancée

### Domaine Personnalisé

1. Allez dans "Settings" → "Domains"
2. Cliquez "Generate Domain" pour un sous-domaine Railway
3. Ou ajoutez votre propre domaine

### Variables d'Environnement Complètes

```env
# Django
SECRET_KEY=votre-cle-secrete-generee
DEBUG=False
ALLOWED_HOSTS=.railway.app,votre-domaine.com

# Base de données (automatique)
DATABASE_URL=postgresql://...

# Email (optionnel)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app

# Sécurité
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

---

## 📊 Monitoring

### Voir les Logs
1. Cliquez sur votre service
2. Allez dans "Deployments"
3. Cliquez sur le déploiement actif
4. Logs en temps réel disponibles

### Métriques
- CPU, RAM, Network dans l'onglet "Metrics"
- Gratuit: 500h/mois, 512MB RAM, 1GB stockage

---

## 🔄 Déploiement Automatique

Railway redéploie automatiquement à chaque push sur GitHub:

```bash
# Faire des modifications
git add .
git commit -m "Mise à jour"
git push

# Railway redéploie automatiquement! 🚀
```

---

## 🆘 Dépannage

### Erreur: "Application failed to respond"
```bash
# Vérifiez les logs
railway logs

# Vérifiez les variables d'environnement
railway variables
```

### Erreur: "Database connection failed"
- Vérifiez que PostgreSQL est bien ajouté
- Railway configure automatiquement `DATABASE_URL`

### Erreur: "Static files not found"
Ajoutez dans les variables:
```env
DISABLE_COLLECTSTATIC=1
```

Ou configurez WhiteNoise (déjà dans requirements.txt)

---

## 💰 Tarification

### Tier Gratuit (Hobby)
- ✅ 500 heures d'exécution/mois
- ✅ 512 MB RAM
- ✅ 1 GB stockage
- ✅ PostgreSQL inclus
- ✅ SSL automatique

**Suffisant pour**:
- Développement
- Tests
- Petites équipes
- Prototypes

### Tier Payant (Pro)
- $5/mois par service
- Plus de ressources
- Support prioritaire

---

## 📖 Ressources

- Documentation Railway: https://docs.railway.app
- Support: https://railway.app/help
- Discord: https://discord.gg/railway

---

## ✅ Checklist Post-Déploiement

- [ ] Application accessible via URL Railway
- [ ] PostgreSQL connecté
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] Page de connexion fonctionne
- [ ] Dashboard accessible
- [ ] Exports Excel/PDF fonctionnent
- [ ] API REST accessible

---

## 🎯 Prochaines Étapes

1. ✅ Testez toutes les fonctionnalités
2. ✅ Configurez les emails (optionnel)
3. ✅ Ajoutez un domaine personnalisé (optionnel)
4. ✅ Invitez votre équipe
5. ✅ Importez les données initiales

---

**Félicitations! Votre application ProSMAT est en ligne! 🎉**

**URL du dépôt**: https://github.com/Louistatch/SE-promsat.git
**Date**: 8 février 2026
