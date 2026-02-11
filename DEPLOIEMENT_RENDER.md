# 🚀 Guide de Déploiement sur Render

## 📋 Architecture

- **Application**: Render (Web Service)
- **Base de données**: Neon (PostgreSQL)
- **Authentification**: Firebase
- **Fichiers statiques**: WhiteNoise

---

## 🎯 Prérequis

### 1. Compte Render
- Créez un compte sur: https://render.com/
- Connectez votre compte GitHub

### 2. Base de Données Neon
- ✅ Déjà configurée
- Récupérez votre `DATABASE_URL` depuis: https://console.neon.tech/

### 3. Firebase
- ✅ Déjà configuré
- Téléchargez le fichier `firebase-credentials.json`

### 4. Code sur GitHub
- ✅ Déjà fait: https://github.com/Louistatch/SE-promsat

---

## 🔧 Étape 1: Préparer les Credentials Firebase

Firebase credentials doivent être encodés en base64 pour Render:

### Sur Windows (PowerShell):

```powershell
# Encoder le fichier en base64
$content = Get-Content -Path "firebase-credentials.json" -Raw
$bytes = [System.Text.Encoding]::UTF8.GetBytes($content)
$base64 = [Convert]::ToBase64String($bytes)
$base64 | Set-Clipboard
Write-Host "✅ Credentials copiés dans le presse-papiers!"
```

### Alternative (en ligne):
1. Ouvrez `firebase-credentials.json`
2. Copiez tout le contenu
3. Allez sur: https://www.base64encode.org/
4. Collez le contenu et cliquez sur "Encode"
5. Copiez le résultat

---

## 🚀 Étape 2: Créer le Web Service sur Render

### 2.1 Connexion

1. Allez sur: https://dashboard.render.com/
2. Cliquez sur **"New +"** → **"Web Service"**

### 2.2 Connecter le Dépôt

1. Sélectionnez **"Build and deploy from a Git repository"**
2. Cliquez sur **"Connect account"** (si nécessaire)
3. Cherchez et sélectionnez: **Louistatch/SE-promsat**
4. Cliquez sur **"Connect"**

### 2.3 Configuration du Service

Remplissez les informations:

**Basic:**
- **Name**: `prosmat` (ou `prosmat-togo`)
- **Region**: `Frankfurt (EU Central)` (plus proche du Togo)
- **Branch**: `main`
- **Root Directory**: (laisser vide)

**Build & Deploy:**
- **Runtime**: `Python 3`
- **Build Command**: `./build.sh`
- **Start Command**: `gunicorn config.wsgi:application`

**Plan:**
- Sélectionnez **"Free"** (pour commencer)
- Ou **"Starter"** ($7/mois) pour de meilleures performances

---

## 🔐 Étape 3: Configurer les Variables d'Environnement

Cliquez sur **"Advanced"** puis ajoutez ces variables:

### Variables Obligatoires

| Variable | Valeur | Description |
|----------|--------|-------------|
| `PYTHON_VERSION` | `3.10.0` | Version Python |
| `DEBUG` | `False` | Mode debug désactivé |
| `SECRET_KEY` | (généré auto) | Clé secrète Django |
| `DATABASE_URL` | `postgresql://...` | URL Neon PostgreSQL |

### Variables Firebase

| Variable | Valeur | Où trouver |
|----------|--------|------------|
| `FIREBASE_API_KEY` | `AIza...` | Firebase Console → Project Settings |
| `FIREBASE_AUTH_DOMAIN` | `prosmat-auth.firebaseapp.com` | Firebase Console |
| `FIREBASE_PROJECT_ID` | `prosmat-auth` | Firebase Console |
| `FIREBASE_STORAGE_BUCKET` | `prosmat-auth.appspot.com` | Firebase Console |
| `FIREBASE_MESSAGING_SENDER_ID` | `123456789` | Firebase Console |
| `FIREBASE_APP_ID` | `1:123:web:abc` | Firebase Console |
| `FIREBASE_MEASUREMENT_ID` | `G-XXXXXXX` | Firebase Console (optionnel) |
| `FIREBASE_CREDENTIALS_BASE64` | (base64 du fichier) | Étape 1 |

### Récupérer DATABASE_URL de Neon

1. Allez sur: https://console.neon.tech/
2. Sélectionnez votre projet ProSMAT
3. Cliquez sur **"Connection Details"**
4. Copiez la **"Connection string"**
5. Format: `postgresql://user:password@host/database?sslmode=require`

---

## 📝 Étape 4: Déployer

1. Vérifiez que toutes les variables sont configurées
2. Cliquez sur **"Create Web Service"**
3. Render va:
   - Cloner votre dépôt GitHub
   - Installer les dépendances
   - Exécuter `build.sh`
   - Démarrer l'application

**Durée**: ~5-10 minutes

---

## ✅ Étape 5: Vérifier le Déploiement

### 5.1 Logs

Surveillez les logs en temps réel:
- Onglet **"Logs"** dans Render
- Vérifiez qu'il n'y a pas d'erreurs

### 5.2 Accéder à l'Application

Votre URL sera: `https://prosmat.onrender.com`

Testez:
1. Page d'accueil: `https://prosmat.onrender.com/`
2. Login: `https://prosmat.onrender.com/accounts/login/`
3. Admin: `https://prosmat.onrender.com/admin/`

### 5.3 Créer un Superuser

Dans l'onglet **"Shell"** de Render:

```bash
python manage.py createsuperuser
```

Ou utilisez le script:

```bash
python donner_admin.py
```

---

## 🔧 Étape 6: Configuration Firebase

### 6.1 Ajouter le Domaine Render

1. Allez sur: https://console.firebase.google.com/
2. Sélectionnez votre projet
3. **Authentication** → **Settings** → **Authorized domains**
4. Cliquez sur **"Add domain"**
5. Ajoutez: `prosmat.onrender.com`

### 6.2 Mettre à Jour les Redirects

Dans Firebase Console:
- **Authentication** → **Sign-in method**
- Pour chaque provider (Email, Google):
  - Ajoutez `https://prosmat.onrender.com` dans les URLs autorisées

---

## 🎨 Étape 7: Configuration Optionnelle

### 7.1 Domaine Personnalisé

Si vous avez un domaine (ex: `prosmat.tg`):

1. Dans Render: **Settings** → **Custom Domain**
2. Ajoutez votre domaine
3. Configurez les DNS selon les instructions
4. Mettez à jour `ALLOWED_HOSTS` dans les variables d'environnement

### 7.2 Activer le Plan Payant

Pour de meilleures performances:
- **Starter**: $7/mois (512 MB RAM)
- **Standard**: $25/mois (2 GB RAM)

Avantages:
- Pas de mise en veille
- Plus de RAM
- Meilleure performance
- Support prioritaire

---

## 🔄 Étape 8: Déploiements Futurs

### Déploiement Automatique

Render redéploie automatiquement à chaque push sur `main`:

```bash
# Faire des modifications
git add .
git commit -m "feat: Nouvelle fonctionnalité"
git push origin main

# Render redéploie automatiquement
```

### Déploiement Manuel

Dans Render Dashboard:
1. Allez sur votre service
2. Cliquez sur **"Manual Deploy"** → **"Deploy latest commit"**

### Rollback

Pour revenir à une version précédente:
1. **Events** → Trouvez le déploiement
2. Cliquez sur **"Rollback to this version"**

---

## 🐛 Dépannage

### Problème: Build Failed

**Solution**:
1. Vérifiez les logs dans l'onglet **"Logs"**
2. Vérifiez que `build.sh` est exécutable:
   ```bash
   git update-index --chmod=+x build.sh
   git commit -m "fix: Make build.sh executable"
   git push
   ```

### Problème: Application Crash

**Solution**:
1. Vérifiez les logs
2. Vérifiez `DATABASE_URL` (doit être valide)
3. Vérifiez `FIREBASE_CREDENTIALS_BASE64`
4. Testez localement avec les mêmes variables

### Problème: Static Files 404

**Solution**:
1. Vérifiez que `collectstatic` s'exécute dans `build.sh`
2. Vérifiez `STATIC_ROOT` dans settings
3. Redéployez

### Problème: Firebase Auth Failed

**Solution**:
1. Vérifiez que le domaine Render est autorisé dans Firebase
2. Vérifiez `FIREBASE_CREDENTIALS_BASE64`
3. Vérifiez les variables Firebase

### Problème: Database Connection Failed

**Solution**:
1. Vérifiez `DATABASE_URL` depuis Neon
2. Vérifiez que la base Neon est active
3. Testez la connexion depuis Neon Console

---

## 📊 Monitoring

### Logs

Surveillez les logs en temps réel:
```
Render Dashboard → Votre Service → Logs
```

### Métriques

Consultez les métriques:
- CPU usage
- Memory usage
- Request count
- Response time

### Alertes

Configurez des alertes:
1. **Settings** → **Notifications**
2. Ajoutez votre email
3. Choisissez les événements (deploy failed, service down, etc.)

---

## 💰 Coûts

### Plan Free
- **Prix**: $0/mois
- **RAM**: 512 MB
- **Limitations**:
  - Se met en veille après 15 min d'inactivité
  - 750 heures/mois
  - Redémarrage lent (~30 secondes)

### Plan Starter (Recommandé)
- **Prix**: $7/mois
- **RAM**: 512 MB
- **Avantages**:
  - Pas de mise en veille
  - Toujours actif
  - Démarrage rapide

### Plan Standard
- **Prix**: $25/mois
- **RAM**: 2 GB
- **Pour**: Production avec trafic élevé

---

## 🔒 Sécurité

### Variables Sensibles

✅ Toutes les variables sensibles sont dans Render (pas dans le code)
✅ Firebase credentials encodés en base64
✅ SECRET_KEY généré automatiquement
✅ DEBUG=False en production

### HTTPS

✅ HTTPS activé automatiquement par Render
✅ Certificat SSL gratuit
✅ Renouvellement automatique

### Backups

**Base de données Neon**:
- Backups automatiques quotidiens
- Rétention: 7 jours (plan gratuit)
- Restauration en 1 clic

---

## 📞 Support

### Render
- Documentation: https://render.com/docs
- Support: https://render.com/support
- Status: https://status.render.com/

### Neon
- Documentation: https://neon.tech/docs
- Support: https://neon.tech/docs/introduction/support

### Firebase
- Documentation: https://firebase.google.com/docs
- Support: https://firebase.google.com/support

---

## ✅ Checklist de Déploiement

- [ ] Compte Render créé
- [ ] Dépôt GitHub connecté
- [ ] DATABASE_URL récupéré depuis Neon
- [ ] Firebase credentials encodés en base64
- [ ] Toutes les variables d'environnement configurées
- [ ] Web Service créé sur Render
- [ ] Build réussi (vérifier les logs)
- [ ] Application accessible
- [ ] Domaine Render ajouté dans Firebase
- [ ] Superuser créé
- [ ] Tests de connexion Firebase
- [ ] Tests des fonctionnalités principales

---

## 🎉 Félicitations!

Votre application ProSMAT est maintenant en production sur Render!

**URL**: https://prosmat.onrender.com

**Architecture**:
- ✅ Application: Render
- ✅ Base de données: Neon PostgreSQL
- ✅ Authentification: Firebase
- ✅ Fichiers statiques: WhiteNoise
- ✅ HTTPS: Activé
- ✅ Déploiement automatique: Activé

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Guide créé le: 11 février 2026*
