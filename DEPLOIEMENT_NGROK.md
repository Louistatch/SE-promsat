# 🚀 DÉPLOIEMENT AVEC NGROK - GUIDE COMPLET

## ✅ Avantages de ngrok

- ✅ **Gratuit** (tier gratuit permanent)
- ✅ **SQLite** (votre base de données locale)
- ✅ **Rapide** (2 minutes de setup)
- ✅ **HTTPS automatique**
- ✅ **Contrôle total** (votre machine)
- ✅ **Pas de migration** de données
- ✅ **Parfait pour démo/test**

---

## 📋 PRÉREQUIS

✅ Projet ProSMAT fonctionnel localement
✅ Python et Django installés
✅ Utilisateurs créés (déjà fait!)

---

## 🔧 ÉTAPE 1: Installer ngrok (5 min)

### A. Télécharger ngrok

1. Allez sur https://ngrok.com
2. Cliquez "**Sign up**" (créez un compte gratuit)
3. Connectez-vous
4. Allez dans "**Your Authtoken**"
5. Téléchargez ngrok pour Windows: https://ngrok.com/download

### B. Installer ngrok

1. Extrayez `ngrok.exe` dans un dossier (ex: `C:\ngrok\`)
2. Ou placez-le directement dans votre projet: `C:\Users\HP\Downloads\prosmat_se\`

### C. Configurer l'authtoken

Ouvrez un terminal (cmd ou PowerShell) et exécutez:

```bash
cd C:\Users\HP\Downloads\prosmat_se
ngrok config add-authtoken VOTRE_TOKEN_ICI
```

**⚠️ Remplacez `VOTRE_TOKEN_ICI` par votre vrai token depuis le dashboard ngrok!**

---

## 🚀 ÉTAPE 2: Démarrer Django (1 min)

### Ouvrez un PREMIER terminal:

```bash
cd C:\Users\HP\Downloads\prosmat_se
.\venv_prosmat\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

Vous devriez voir:
```
Starting development server at http://0.0.0.0:8000/
Quit the server with CTRL-BREAK.
```

**⚠️ NE FERMEZ PAS CE TERMINAL!**

---

## 🌐 ÉTAPE 3: Démarrer ngrok (1 min)

### Ouvrez un DEUXIÈME terminal:

```bash
cd C:\Users\HP\Downloads\prosmat_se
ngrok http 8000
```

Vous verrez quelque chose comme:
```
ngrok

Session Status                online
Account                       votre-email@gmail.com
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://xxxx-xxxx-xxxx.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**🎉 Votre URL publique**: `https://xxxx-xxxx-xxxx.ngrok-free.app`

---

## ✅ ÉTAPE 4: Accéder à l'Application

1. **Copiez l'URL** `https://xxxx-xxxx-xxxx.ngrok-free.app`
2. **Ouvrez-la dans un navigateur**
3. **Cliquez sur "Visit Site"** (ngrok affiche un avertissement la première fois)
4. **Vous verrez la page de connexion ProSMAT!**

### Se Connecter:

```
Username: admin
Password: ProSMAT2026!
```

Ou utilisez un des coordinateurs régionaux:
```
Username: coord_maritime (ou coord_plateaux, etc.)
Password: ProSMAT2026!
```

---

## 🎨 ÉTAPE 5: Partager l'URL

**Partagez l'URL ngrok** avec votre équipe:
- `https://xxxx-xxxx-xxxx.ngrok-free.app`

Ils pourront accéder à l'application depuis n'importe où!

---

## 📊 ÉTAPE 6: Monitorer les Requêtes

ngrok offre une interface web pour voir toutes les requêtes:

1. Ouvrez http://127.0.0.1:4040 dans votre navigateur
2. Vous verrez toutes les requêtes HTTP en temps réel
3. Très utile pour le débogage!

---

## ⚙️ CONFIGURATION AVANCÉE

### URL Personnalisée (Payant)

Avec ngrok Pro, vous pouvez avoir une URL fixe:
```bash
ngrok http 8000 --domain=prosmat.ngrok.app
```

### Authentification

Ajouter une authentification ngrok:
```bash
ngrok http 8000 --basic-auth="user:password"
```

### Région

Choisir une région plus proche:
```bash
ngrok http 8000 --region=eu
```

---

## 🔄 REDÉMARRAGE

### Chaque fois que vous voulez exposer l'application:

**Terminal 1** (Django):
```bash
cd C:\Users\HP\Downloads\prosmat_se
.\venv_prosmat\Scripts\activate
python manage.py runserver 0.0.0.0:8000
```

**Terminal 2** (ngrok):
```bash
cd C:\Users\HP\Downloads\prosmat_se
ngrok http 8000
```

**⚠️ L'URL ngrok change à chaque redémarrage** (sauf avec un compte payant)

---

## 📋 SCRIPT DE DÉMARRAGE AUTOMATIQUE

Créez un fichier `start_ngrok.bat`:

```batch
@echo off
echo Demarrage de ProSMAT avec ngrok...

REM Demarrer Django en arriere-plan
start "Django Server" cmd /k "cd C:\Users\HP\Downloads\prosmat_se && .\venv_prosmat\Scripts\activate && python manage.py runserver 0.0.0.0:8000"

REM Attendre 5 secondes
timeout /t 5

REM Demarrer ngrok
start "ngrok" cmd /k "cd C:\Users\HP\Downloads\prosmat_se && ngrok http 8000"

echo ProSMAT demarre!
echo Consultez la fenetre ngrok pour obtenir l'URL publique.
pause
```

**Double-cliquez sur `start_ngrok.bat`** pour tout démarrer automatiquement!

---

## ⚠️ LIMITATIONS DU TIER GRATUIT

- ⚠️ **URL change** à chaque redémarrage
- ⚠️ **40 connexions/minute** maximum
- ⚠️ **Avertissement ngrok** à la première visite
- ⚠️ **Doit rester allumé** (votre PC)

**Pour lever ces limitations**: Passez à ngrok Pro ($8/mois)

---

## 🆘 DÉPANNAGE

### Erreur: "command not found: ngrok"

**Solution**: Ajoutez ngrok au PATH ou utilisez le chemin complet:
```bash
C:\ngrok\ngrok http 8000
```

### Erreur: "failed to start tunnel"

**Solution**: Vérifiez que:
1. Votre authtoken est configuré
2. Django tourne sur le port 8000
3. Vous avez une connexion Internet

### L'URL ne fonctionne pas

**Solution**:
1. Vérifiez que Django tourne (terminal 1)
2. Vérifiez que ngrok tourne (terminal 2)
3. Cliquez sur "Visit Site" sur la page d'avertissement ngrok

---

## ✅ CHECKLIST

- [ ] ngrok téléchargé et installé
- [ ] Authtoken configuré
- [ ] Django démarré (port 8000)
- [ ] ngrok démarré
- [ ] URL publique copiée
- [ ] Application accessible
- [ ] Connexion testée avec admin
- [ ] URL partagée avec l'équipe

---

## 🎯 RÉSUMÉ

**2 commandes pour exposer votre application**:

```bash
# Terminal 1
python manage.py runserver 0.0.0.0:8000

# Terminal 2
ngrok http 8000
```

**C'est tout!** Votre application est maintenant accessible sur Internet! 🌍

---

## 📞 SUPPORT

- Documentation ngrok: https://ngrok.com/docs
- Dashboard ngrok: https://dashboard.ngrok.com
- Status ngrok: https://status.ngrok.com

---

**Date**: 9 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
**Méthode**: ngrok (Gratuit + SQLite)
