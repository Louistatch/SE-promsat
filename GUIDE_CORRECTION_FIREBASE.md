# Guide de Correction Firebase - Étapes Pratiques

## 🚀 Démarrage Rapide

### 1. Vérifier la Configuration

```bash
python test_firebase_auth.py
```

Ce script vérifie:
- ✅ Variables d'environnement Firebase
- ✅ Initialisation Firebase Admin SDK
- ✅ Backends d'authentification
- ✅ Configuration de logging
- ✅ Cache pour rate limiting
- ✅ Sécurité des sessions

### 2. Configurer les Variables d'Environnement

Si le test échoue, créez votre fichier `.env`:

```bash
copy .env.example .env
```

Puis éditez `.env` avec vos vraies valeurs Firebase:

```env
# Firebase Configuration
FIREBASE_API_KEY=AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
FIREBASE_AUTH_DOMAIN=votre-projet.firebaseapp.com
FIREBASE_PROJECT_ID=votre-projet-id
FIREBASE_STORAGE_BUCKET=votre-projet.appspot.com
FIREBASE_MESSAGING_SENDER_ID=123456789012
FIREBASE_APP_ID=1:123456789012:web:abcdef123456
FIREBASE_MEASUREMENT_ID=G-XXXXXXXXXX
```

### 3. Obtenir les Credentials Firebase

#### Option A: Configuration Web (Recommandé)
1. Allez sur https://console.firebase.google.com
2. Sélectionnez votre projet
3. Cliquez sur l'icône ⚙️ > Paramètres du projet
4. Descendez à "Vos applications" > SDK Firebase
5. Copiez les valeurs dans votre `.env`

#### Option B: Service Account (Pour Admin SDK)
1. Console Firebase > ⚙️ > Paramètres du projet
2. Onglet "Comptes de service"
3. Cliquez "Générer une nouvelle clé privée"
4. Sauvegardez le fichier JSON comme `firebase-credentials.json`
5. Placez-le à la racine du projet

⚠️ **IMPORTANT**: Ajoutez `firebase-credentials.json` au `.gitignore`!

### 4. Activer l'Authentification Firebase

1. Console Firebase > Authentication
2. Onglet "Sign-in method"
3. Activez "Email/Password"
4. Activez "Google" (pour OAuth)
5. Ajoutez vos domaines autorisés:
   - `localhost`
   - `127.0.0.1`
   - Votre domaine ngrok (ex: `abc123.ngrok-free.app`)
   - Votre domaine de production

### 5. Tester l'Authentification

```bash
# Démarrer le serveur
python manage.py runserver

# Ouvrir dans le navigateur
http://localhost:8000/accounts/login/
```

## 🔍 Diagnostic des Problèmes

### Problème: "Firebase Admin SDK n'est pas initialisé"

**Solution:**
1. Vérifiez que `firebase-admin` est installé:
   ```bash
   pip install firebase-admin==6.4.0
   ```

2. Vérifiez les logs:
   ```bash
   type logs\django.log
   ```

3. Vérifiez que le fichier `firebase-credentials.json` existe OU que les credentials par défaut sont configurés

### Problème: "Token manquant" ou "Token invalide"

**Solution:**
1. Vérifiez la configuration Firebase dans le template:
   - Ouvrez `templates/accounts/login_firebase.html`
   - Vérifiez que `{{ firebase_config.apiKey }}` affiche une valeur

2. Testez dans la console du navigateur (F12):
   ```javascript
   console.log(firebase.auth().currentUser);
   ```

3. Vérifiez que le domaine est autorisé dans Firebase Console

### Problème: "Trop de tentatives"

**Solution:**
Le rate limiting est actif (10 tentatives/minute). Attendez 1 minute ou:

```python
# Dans le shell Django
python manage.py shell

from django.core.cache import cache
cache.clear()
```

### Problème: "Popup bloquée" (Google OAuth)

**Solution:**
1. Autorisez les popups pour localhost dans votre navigateur
2. Ou utilisez `signInWithRedirect` au lieu de `signInWithPopup`

### Problème: Logs non créés

**Solution:**
```bash
# Créer le dossier logs
mkdir logs

# Vérifier les permissions
icacls logs
```

## 📊 Vérification des Logs

### Voir les logs en temps réel

```bash
# Windows
Get-Content logs\django.log -Wait -Tail 50

# Ou simplement
type logs\django.log
```

### Logs importants à surveiller

```
INFO accounts.firebase_auth Utilisateur trouvé: user@example.com
INFO accounts.views_firebase Authentification réussie pour: user@example.com
WARNING accounts.firebase_auth Email non vérifié pour user@example.com
ERROR accounts.firebase_auth Token Firebase invalide: ...
```

## 🔒 Checklist de Sécurité

Avant de déployer en production:

- [ ] `DEBUG=False` dans `.env`
- [ ] `SECRET_KEY` unique et sécurisée
- [ ] HTTPS activé (certificat SSL)
- [ ] `SESSION_COOKIE_SECURE=True`
- [ ] `CSRF_COOKIE_SECURE=True`
- [ ] Domaines autorisés configurés dans Firebase
- [ ] Rate limiting testé
- [ ] Logs configurés et surveillés
- [ ] Backup de la base de données
- [ ] Variables d'environnement sécurisées (pas dans git)

## 🧪 Tests Manuels

### Test 1: Connexion Email/Password

1. Créez un utilisateur dans Firebase Console
2. Allez sur `/accounts/login/`
3. Entrez email et mot de passe
4. Vérifiez la redirection vers `/dashboard/`
5. Vérifiez les logs: `type logs\django.log`

### Test 2: Connexion Google OAuth

1. Cliquez sur "Continuer avec Google"
2. Sélectionnez un compte Google
3. Vérifiez la création automatique du compte Django
4. Vérifiez dans l'admin Django: `/admin/accounts/user/`

### Test 3: Rate Limiting

1. Entrez 10 fois un mauvais mot de passe rapidement
2. Vérifiez le message "Trop de tentatives"
3. Attendez 1 minute
4. Réessayez (devrait fonctionner)

### Test 4: Mot de Passe Oublié

1. Entrez votre email
2. Cliquez "Mot de passe oublié?"
3. Vérifiez l'email de réinitialisation
4. Suivez le lien et changez le mot de passe

### Test 5: Déconnexion

1. Connectez-vous
2. Allez sur `/accounts/logout/`
3. Vérifiez la redirection vers `/accounts/login/`
4. Vérifiez que vous ne pouvez plus accéder au dashboard

## 📈 Monitoring en Production

### Métriques à surveiller

1. **Taux de connexion réussie**
   - Logs: `grep "Authentification réussie" logs/django.log | wc -l`

2. **Tentatives échouées**
   - Logs: `grep "Authentification échouée" logs/django.log | wc -l`

3. **Rate limiting déclenché**
   - Logs: `grep "Trop de tentatives" logs/django.log`

4. **Erreurs Firebase**
   - Logs: `grep "ERROR.*firebase" logs/django.log`

### Alertes recommandées

- Plus de 10 échecs de connexion en 5 minutes
- Rate limiting déclenché plus de 5 fois en 1 heure
- Erreur d'initialisation Firebase
- Token expiré fréquemment

## 🆘 Support

### Ressources

- Documentation Firebase: https://firebase.google.com/docs/auth
- Documentation Django: https://docs.djangoproject.com/
- Logs du projet: `logs/django.log`
- Tests: `python test_firebase_auth.py`

### En cas de problème

1. Vérifiez les logs: `type logs\django.log`
2. Lancez les tests: `python test_firebase_auth.py`
3. Vérifiez la console Firebase
4. Activez `DEBUG=True` temporairement
5. Consultez `CORRECTIONS_FIREBASE_AUTHENTIFICATION.md`

## ✅ Validation Finale

Avant de considérer que tout fonctionne:

```bash
# 1. Tests automatiques
python test_firebase_auth.py

# 2. Vérifier les migrations
python manage.py makemigrations
python manage.py migrate

# 3. Créer un superuser (si nécessaire)
python manage.py createsuperuser

# 4. Collecter les fichiers statiques
python manage.py collectstatic --noinput

# 5. Démarrer le serveur
python manage.py runserver
```

Puis testez manuellement:
- ✅ Connexion email/password
- ✅ Connexion Google OAuth
- ✅ Création automatique de compte
- ✅ Déconnexion
- ✅ Mot de passe oublié
- ✅ Rate limiting
- ✅ Logs générés

Si tous les tests passent: **🎉 Félicitations! Votre système Firebase est opérationnel!**
