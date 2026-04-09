# 🌐 Guide d'Utilisation de Ngrok avec ProSMAT

## Qu'est-ce que Ngrok?

Ngrok crée un tunnel sécurisé qui expose votre serveur local (localhost:8000) sur Internet avec une URL publique HTTPS.

**Avantages:**
- ✅ Tester Firebase Authentication depuis n'importe où
- ✅ Partager l'application avec d'autres personnes
- ✅ Tester sur mobile
- ✅ URL HTTPS sécurisée

## Installation de Ngrok

### Si ngrok.exe n'est pas dans le dossier:

1. Télécharger depuis: https://ngrok.com/download
2. Extraire le fichier `ngrok.exe`
3. Placer `ngrok.exe` dans le dossier du projet ProSMAT

### Vérifier l'installation:

```bash
ngrok version
```

## Démarrage Rapide

### Option 1: Script automatique (Recommandé)

Double-cliquer sur: `DEMARRER_NGROK.bat`

Le script va:
1. ✅ Activer l'environnement virtuel
2. ✅ Vérifier la base de données
3. ✅ Démarrer le serveur Django
4. ✅ Démarrer ngrok

### Option 2: Manuel

```bash
# Terminal 1 - Démarrer Django
venv_prosmat\Scripts\activate
python manage.py runserver 8000

# Terminal 2 - Démarrer ngrok
ngrok http 8000
```

## Configuration après démarrage

### 1. Copier l'URL Ngrok

Quand ngrok démarre, vous verrez:

```
ngrok

Session Status                online
Account                       Free
Version                       3.x.x
Region                        United States (us)
Latency                       -
Web Interface                 http://127.0.0.1:4040
Forwarding                    https://abc123.ngrok-free.app -> http://localhost:8000

Connections                   ttl     opn     rt1     rt5     p50     p90
                              0       0       0.00    0.00    0.00    0.00
```

**Copier l'URL:** `https://abc123.ngrok-free.app`

### 2. Configurer Firebase Console

1. Aller sur: https://console.firebase.google.com
2. Sélectionner: **prosmat-auth**
3. Menu: **Authentication** → **Settings**
4. Section: **Authorized domains**
5. Cliquer: **Add domain**
6. Coller: `abc123.ngrok-free.app` (sans https://)
7. Cliquer: **Add**

### 3. Configurer Django (si nécessaire)

Le fichier `config/settings.py` est déjà configuré avec:

```python
ALLOWED_HOSTS = ['*']  # Accepte tous les domaines

CSRF_TRUSTED_ORIGINS = [
    'https://*.ngrok-free.app',
    'https://*.ngrok.io',
    'http://localhost:8000',
]
```

Si vous avez des problèmes CSRF, ajoutez votre URL spécifique:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://abc123.ngrok-free.app',  # Votre URL ngrok
    'https://*.ngrok-free.app',
    'http://localhost:8000',
]
```

### 4. Accéder à l'application

1. Ouvrir l'URL ngrok dans votre navigateur: `https://abc123.ngrok-free.app`
2. Cliquer sur **"Visit Site"** (page d'avertissement ngrok)
3. Vous verrez la page de connexion ProSMAT

## Utilisation

### Connexion locale (toujours disponible)

```
http://localhost:8000/accounts/login/
```

### Connexion via ngrok (publique)

```
https://abc123.ngrok-free.app/accounts/login/
```

### Tester sur mobile

1. Ouvrir l'URL ngrok sur votre téléphone
2. Se connecter avec Firebase
3. Tester l'application

### Partager avec d'autres

Envoyez simplement l'URL ngrok à d'autres personnes:
```
https://abc123.ngrok-free.app
```

## Interface Web Ngrok

Ngrok fournit une interface web pour voir les requêtes:

```
http://127.0.0.1:4040
```

**Fonctionnalités:**
- 📊 Voir toutes les requêtes HTTP
- 🔍 Inspecter les headers
- 📝 Voir les réponses
- 🐛 Débugger les problèmes

## Arrêter l'application

### Si lancé avec DEMARRER_NGROK.bat:

1. Appuyer sur **CTRL+C** dans la fenêtre ngrok
2. Fermer la fenêtre "Django Server"

### Si lancé manuellement:

1. **CTRL+C** dans le terminal ngrok
2. **CTRL+C** dans le terminal Django

## Problèmes courants

### Erreur: "ngrok.exe not found"

**Solution:**
1. Télécharger ngrok depuis https://ngrok.com/download
2. Placer `ngrok.exe` dans le dossier du projet

### Erreur: "Failed to complete tunnel connection"

**Solution:**
1. Vérifier votre connexion Internet
2. Réessayer dans quelques secondes
3. Redémarrer ngrok

### Erreur: "Invalid Host header"

**Solution:**
Vérifier que `ALLOWED_HOSTS = ['*']` dans `config/settings.py`

### Erreur CSRF

**Solution:**
Ajouter votre URL ngrok dans `CSRF_TRUSTED_ORIGINS`:

```python
CSRF_TRUSTED_ORIGINS = [
    'https://votre-url.ngrok-free.app',
    'https://*.ngrok-free.app',
]
```

### Page "Visit Site" à chaque fois

**Solution:**
C'est normal avec le plan gratuit de ngrok. Cliquez simplement sur "Visit Site".

### URL change à chaque redémarrage

**Solution:**
- Plan gratuit: L'URL change à chaque fois
- Plan payant: URL fixe disponible

## Ngrok gratuit vs payant

### Plan Gratuit (actuel)

✅ Tunnel HTTPS
✅ URL aléatoire
✅ Pas de limite de temps
❌ URL change à chaque redémarrage
❌ Page "Visit Site"

### Plan Payant

✅ URL fixe (ex: prosmat.ngrok.io)
✅ Pas de page "Visit Site"
✅ Plus de tunnels simultanés
✅ Support prioritaire

## Commandes utiles

### Démarrer ngrok sur un port spécifique

```bash
ngrok http 8000
```

### Démarrer avec une région spécifique

```bash
ngrok http 8000 --region eu
```

### Voir l'aide

```bash
ngrok help
```

### Voir la version

```bash
ngrok version
```

## Sécurité

### Bonnes pratiques

✅ Ne pas partager l'URL avec des personnes non autorisées
✅ Arrêter ngrok quand vous ne l'utilisez pas
✅ Utiliser des mots de passe forts
✅ Surveiller les connexions dans l'interface web (localhost:4040)

### Données sensibles

⚠️ Ngrok peut voir tout le trafic HTTP
⚠️ Utiliser uniquement pour le développement/test
⚠️ Ne pas utiliser en production

## Alternatives à Ngrok

Si ngrok ne fonctionne pas:

1. **Localtunnel**: https://localtunnel.github.io/www/
2. **Serveo**: https://serveo.net/
3. **Cloudflare Tunnel**: https://www.cloudflare.com/products/tunnel/

## Scripts disponibles

| Script | Description |
|--------|-------------|
| `DEMARRER_NGROK.bat` | Démarrage automatique complet |
| `LANCER_AVEC_NGROK.bat` | Démarrage simple |
| `LANCER_MAINTENANT.bat` | Démarrage local uniquement |

## Workflow recommandé

### Développement local

```bash
LANCER_MAINTENANT.bat
```
→ Accès: http://localhost:8000

### Test avec Firebase / Mobile

```bash
DEMARRER_NGROK.bat
```
→ Accès: https://xxxxx.ngrok-free.app

### Production

Déployer sur un serveur réel (pas ngrok)

## Résumé

**Pour démarrer:**
1. Double-cliquer sur `DEMARRER_NGROK.bat`
2. Copier l'URL ngrok
3. Ajouter dans Firebase Console (Authorized domains)
4. Ouvrir l'URL dans le navigateur
5. Cliquer sur "Visit Site"
6. Se connecter!

**Pour arrêter:**
1. CTRL+C dans la fenêtre ngrok
2. Fermer la fenêtre Django Server

**C'est tout!** 🚀

---

**Date:** 11 février 2026  
**Version:** 1.0  
**Statut:** ✅ Guide complet
