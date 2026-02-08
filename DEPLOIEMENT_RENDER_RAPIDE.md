# 🌐 DÉPLOIEMENT SUR RENDER - GUIDE RAPIDE

## ✅ Render offre un tier GRATUIT permanent!

**Avantages**:
- ✅ Gratuit à vie (avec limitations)
- ✅ PostgreSQL gratuit
- ✅ SSL/HTTPS automatique
- ✅ Déploiement depuis GitHub
- ✅ Pas de carte bancaire requise

**Limitations du tier gratuit**:
- ⚠️ L'application "dort" après 15 min d'inactivité
- ⚠️ Redémarre en ~30 secondes à la première visite
- ⚠️ 750h/mois (suffisant pour usage normal)

---

## 🚀 ÉTAPES DE DÉPLOIEMENT (15 minutes)

### Étape 1: Créer un Compte Render (2 min)

1. Visitez https://render.com
2. Cliquez "Get Started"
3. Inscrivez-vous avec GitHub
4. Autorisez Render à accéder à vos dépôts

---

### Étape 2: Créer une Base de Données PostgreSQL (3 min)

1. Dans le dashboard Render, cliquez "New +"
2. Sélectionnez "PostgreSQL"
3. Configurez:
   - **Name**: `prosmat-db`
   - **Database**: `prosmat`
   - **User**: `prosmat_user`
   - **Region**: Choisissez le plus proche (Frankfurt pour l'Europe)
   - **Plan**: **Free** (gratuit)
4. Cliquez "Create Database"
5. **IMPORTANT**: Copiez l'URL "Internal Database URL" (commence par `postgresql://`)

---

### Étape 3: Créer le Web Service (5 min)

1. Cliquez "New +" → "Web Service"
2. Connectez votre dépôt GitHub: `Louistatch/SE-promsat`
3. Configurez:

**Basic Settings**:
- **Name**: `prosmat-se`
- **Region**: Même région que la base de données
- **Branch**: `main`
- **Root Directory**: (laisser vide)
- **Environment**: `Python 3`
- **Build Command**: 
  ```
  pip install -r requirements.txt
  ```
- **Start Command**: 
  ```
  gunicorn config.wsgi:application
  ```

**Plan**: Sélectionnez **Free** (gratuit)

4. Cliquez "Create Web Service"

---

### Étape 4: Configurer les Variables d'Environnement (3 min)

1. Dans votre Web Service, allez dans "Environment"
2. Cliquez "Add Environment Variable"
3. Ajoutez ces variables:

```env
DJANGO_SETTINGS_MODULE
config.settings_deploy

SECRET_KEY
[GÉNÉREZ UNE CLÉ - voir ci-dessous]

DEBUG
False

ALLOWED_HOSTS
.onrender.com

DATABASE_URL
[COLLEZ L'URL INTERNE DE VOTRE BASE POSTGRESQL]

PYTHON_VERSION
3.11.9
```

**Pour générer SECRET_KEY**:
Ouvrez un terminal local et exécutez:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```
Copiez le résultat et utilisez-le comme valeur pour SECRET_KEY.

4. Cliquez "Save Changes"

---

### Étape 5: Déploiement Automatique (2 min)

Render déploie automatiquement votre application!

**Suivez les logs**:
- Allez dans l'onglet "Logs"
- Vous verrez:
  - Installation des dépendances
  - Exécution des migrations
  - Démarrage du serveur

**Attendez** que le statut passe à "Live" (vert)

---

### Étape 6: Créer un Superuser (2 min)

1. Dans votre Web Service, allez dans "Shell"
2. Cliquez "Launch Shell"
3. Exécutez:
```bash
python manage.py createsuperuser
```
4. Suivez les instructions:
   - Username: `admin`
   - Email: `tatchida@gmail.com`
   - Password: (choisissez un mot de passe fort)
   - Confirmez le mot de passe

---

### Étape 7: Accéder à l'Application

1. Render génère une URL: `https://prosmat-se.onrender.com`
2. Cliquez sur l'URL dans le dashboard
3. Votre application est en ligne! 🎉

**Première visite**: Peut prendre 30 secondes (l'app démarre)

---

## 🔧 Configuration Complète des Variables

### Variables Minimales (Requises)

```env
DJANGO_SETTINGS_MODULE=config.settings_deploy
SECRET_KEY=votre-cle-secrete-unique-generee
DEBUG=False
ALLOWED_HOSTS=.onrender.com
DATABASE_URL=postgresql://prosmat_user:password@host/prosmat
PYTHON_VERSION=3.11.9
```

### Variables Optionnelles (Email)

```env
EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=votre-email@gmail.com
EMAIL_HOST_PASSWORD=votre-mot-de-passe-app
DEFAULT_FROM_EMAIL=noreply@prosmat.tg
```

---

## ✅ Checklist Post-Déploiement

- [ ] Base de données PostgreSQL créée
- [ ] Web Service créé
- [ ] Variables d'environnement configurées
- [ ] Déploiement réussi (statut "Live")
- [ ] Superuser créé
- [ ] Application accessible via URL
- [ ] Page de connexion fonctionne
- [ ] Dashboard accessible
- [ ] Exports Excel/PDF testés

---

## 🆘 Dépannage

### Erreur: "Application failed to respond"

**Vérifiez les logs**:
1. Allez dans "Logs"
2. Cherchez les erreurs

**Solutions courantes**:
- Vérifiez que `DATABASE_URL` est correct
- Vérifiez que `ALLOWED_HOSTS` contient `.onrender.com`
- Vérifiez que `SECRET_KEY` est défini

### Erreur: "Static files not found"

Render gère automatiquement les fichiers statiques avec WhiteNoise (déjà configuré).

Si problème:
```bash
# Dans le Shell Render
python manage.py collectstatic --noinput
```

### Erreur: "Database connection failed"

1. Vérifiez que la base PostgreSQL est bien créée
2. Copiez l'URL "Internal Database URL" (pas "External")
3. Collez-la dans la variable `DATABASE_URL`

### L'application est lente au premier chargement

C'est normal sur le tier gratuit! L'application "dort" après 15 min d'inactivité et redémarre en ~30 secondes.

**Solutions**:
- Utilisez un service de "ping" gratuit (UptimeRobot)
- Ou passez au plan payant ($7/mois)

---

## 💰 Tarification Render

### Free (Gratuit)
- ✅ 750h/mois
- ✅ PostgreSQL gratuit (90 jours, puis $7/mois)
- ⚠️ Application dort après 15 min
- ⚠️ 512 MB RAM
- ⚠️ Partage CPU

### Starter ($7/mois)
- ✅ Toujours actif
- ✅ 512 MB RAM
- ✅ CPU dédié

---

## 🔄 Déploiement Automatique

Render redéploie automatiquement à chaque push sur GitHub:

```bash
# Faire des modifications
git add .
git commit -m "Mise à jour"
git push

# Render redéploie automatiquement! 🚀
```

---

## 📊 Monitoring

### Logs en Temps Réel
- Allez dans "Logs"
- Logs en temps réel disponibles

### Métriques
- CPU, RAM, Requêtes dans "Metrics"

### Alertes
- Configurez des alertes email dans "Settings"

---

## 🌐 Domaine Personnalisé (Optionnel)

1. Allez dans "Settings" → "Custom Domain"
2. Ajoutez votre domaine
3. Configurez les DNS selon les instructions
4. SSL automatique!

---

## 🎯 Prochaines Étapes

1. ✅ Testez toutes les fonctionnalités
2. ✅ Configurez les emails (optionnel)
3. ✅ Ajoutez un domaine personnalisé (optionnel)
4. ✅ Invitez votre équipe
5. ✅ Importez les données initiales

---

## 📖 Ressources

- Documentation Render: https://render.com/docs
- Support: https://render.com/support
- Status: https://status.render.com

---

## ✅ RÉSUMÉ

**Votre application ProSMAT est maintenant**:
- ✅ Déployée sur Render
- ✅ Accessible via HTTPS
- ✅ Connectée à PostgreSQL
- ✅ Prête pour la production
- ✅ Gratuite!

**URL**: https://prosmat-se.onrender.com

**Prochaine étape**: Testez l'application et invitez votre équipe!

---

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
**Plateforme**: Render (Gratuit)
