# 🔍 Diagnostic de l'Erreur d'Authentification

## Erreur Rencontrée
```
Authentification échouée. Vérifiez vos identifiants.
```

## Vérifications Effectuées

### ✅ Variables Firebase Configurées
Les variables Firebase sont correctement configurées dans `.env`:
- FIREBASE_API_KEY: ✅ Présent
- FIREBASE_AUTH_DOMAIN: ✅ Présent
- FIREBASE_PROJECT_ID: ✅ Présent
- FIREBASE_STORAGE_BUCKET: ✅ Présent
- FIREBASE_MESSAGING_SENDER_ID: ✅ Présent
- FIREBASE_APP_ID: ✅ Présent

### ✅ Firebase Admin SDK Initialisé
Le backend Firebase est correctement initialisé.

## Causes Possibles

### 1. 🔑 Utilisateur Non Créé dans Firebase
**Symptôme**: Vous essayez de vous connecter avec un email qui n'existe pas dans Firebase.

**Solution**:
1. Allez sur https://console.firebase.google.com
2. Sélectionnez votre projet "prosmat-auth"
3. Allez dans Authentication > Users
4. Cliquez sur "Add user"
5. Créez un utilisateur avec email et mot de passe

### 2. 🔐 Mot de Passe Incorrect
**Symptôme**: L'email existe mais le mot de passe est incorrect.

**Solution**:
- Vérifiez que vous utilisez le bon mot de passe
- Ou réinitialisez le mot de passe via "Mot de passe oublié?"

### 3. 🚫 Email/Password Non Activé dans Firebase
**Symptôme**: La méthode d'authentification n'est pas activée.

**Solution**:
1. Console Firebase > Authentication
2. Onglet "Sign-in method"
3. Cliquez sur "Email/Password"
4. Activez "Email/Password"
5. Sauvegardez

### 4. 🌐 Domaine Non Autorisé
**Symptôme**: Le domaine depuis lequel vous vous connectez n'est pas autorisé.

**Solution**:
1. Console Firebase > Authentication
2. Onglet "Settings"
3. Section "Authorized domains"
4. Ajoutez:
   - localhost
   - 127.0.0.1
   - Votre domaine ngrok (si utilisé)

### 5. 🔥 Token Firebase Invalide ou Expiré
**Symptôme**: Le token généré par Firebase est invalide.

**Solution**:
- Videz le cache du navigateur (Ctrl+Shift+Delete)
- Réessayez la connexion
- Vérifiez la console du navigateur (F12) pour les erreurs

### 6. 📡 Problème de Réseau
**Symptôme**: Impossible de contacter Firebase.

**Solution**:
- Vérifiez votre connexion internet
- Vérifiez que Firebase n'est pas bloqué par un firewall
- Testez avec: https://firebase.google.com

## 🛠️ Actions de Dépannage

### Étape 1: Vérifier Firebase Console
```bash
# Ouvrez dans votre navigateur
https://console.firebase.google.com/project/prosmat-auth/authentication/users
```

Vérifiez:
- [ ] Le projet "prosmat-auth" existe
- [ ] Email/Password est activé
- [ ] Au moins un utilisateur existe
- [ ] Les domaines sont autorisés

### Étape 2: Créer un Utilisateur de Test
1. Console Firebase > Authentication > Users
2. Cliquez "Add user"
3. Email: test@prosmat.tg
4. Mot de passe: Test123456
5. Cliquez "Add user"

### Étape 3: Tester la Connexion
1. Allez sur http://localhost:8000/accounts/login/
2. Utilisez:
   - Email: test@prosmat.tg
   - Mot de passe: Test123456
3. Cliquez "Se connecter"

### Étape 4: Vérifier les Logs
```bash
# Voir les logs en temps réel
Get-Content logs\django.log -Wait -Tail 50
```

Recherchez:
- `ERROR` - Erreurs critiques
- `Token Firebase invalide` - Problème de token
- `Email manquant` - Problème de configuration
- `Authentification échouée` - Identifiants incorrects

### Étape 5: Vérifier la Console du Navigateur
1. Ouvrez la page de connexion
2. Appuyez sur F12 (DevTools)
3. Onglet "Console"
4. Tentez de vous connecter
5. Regardez les erreurs en rouge

Erreurs courantes:
- `auth/user-not-found` → Utilisateur n'existe pas
- `auth/wrong-password` → Mot de passe incorrect
- `auth/invalid-email` → Email invalide
- `auth/user-disabled` → Compte désactivé
- `auth/network-request-failed` → Problème réseau

## 🔧 Solutions Rapides

### Solution 1: Créer un Utilisateur Admin
```bash
# Dans le terminal Django
python manage.py shell
```

```python
from accounts.models import User
from django.contrib.auth.hashers import make_password

# Créer un utilisateur Django
user = User.objects.create(
    username='admin',
    email='admin@prosmat.tg',
    first_name='Admin',
    last_name='ProSMAT',
    role='ADMIN',
    is_staff=True,
    is_superuser=True
)
user.set_password('Admin123456')
user.save()

print(f"Utilisateur créé: {user.email}")
```

Ensuite, créez le même utilisateur dans Firebase Console.

### Solution 2: Utiliser la Connexion Django Classique
Si Firebase ne fonctionne pas, utilisez la connexion Django:
```
http://localhost:8000/accounts/login-django/
```

### Solution 3: Réinitialiser Firebase
Si tout échoue:
1. Supprimez tous les utilisateurs dans Firebase Console
2. Recréez un utilisateur de test
3. Videz le cache du navigateur
4. Réessayez

## 📊 Checklist de Diagnostic

Cochez au fur et à mesure:

**Configuration Firebase**:
- [ ] Projet Firebase existe
- [ ] Email/Password activé
- [ ] Google OAuth activé (optionnel)
- [ ] Domaines autorisés configurés
- [ ] Au moins un utilisateur créé

**Configuration Django**:
- [ ] Variables .env correctes
- [ ] Firebase Admin SDK initialisé
- [ ] Logs activés
- [ ] Serveur Django démarré

**Test de Connexion**:
- [ ] Page de connexion accessible
- [ ] Formulaire s'affiche correctement
- [ ] Pas d'erreur dans la console navigateur
- [ ] Logs Django montrent les tentatives

**Réseau**:
- [ ] Internet fonctionne
- [ ] Firebase accessible
- [ ] Pas de firewall bloquant

## 🎯 Test Complet

Exécutez ce test pour vérifier tout le système:

```bash
# 1. Vérifier les variables
python manage.py shell -c "from django.conf import settings; print('Firebase OK' if settings.FIREBASE_CONFIG['apiKey'] else 'Firebase KO')"

# 2. Vérifier Firebase Admin SDK
python -c "import firebase_admin; print('Firebase Admin OK' if firebase_admin._apps else 'Firebase Admin KO')"

# 3. Démarrer le serveur
python manage.py runserver

# 4. Dans un autre terminal, vérifier les logs
Get-Content logs\django.log -Wait -Tail 50
```

## 📞 Besoin d'Aide Supplémentaire?

Si le problème persiste:

1. **Copiez les logs**:
   ```bash
   Get-Content logs\django.log -Tail 100 > erreur_auth.txt
   ```

2. **Copiez les erreurs de la console navigateur** (F12)

3. **Vérifiez Firebase Console**:
   - Nombre d'utilisateurs
   - Méthodes d'authentification activées
   - Domaines autorisés

4. **Testez avec curl**:
   ```bash
   curl -X POST http://localhost:8000/accounts/firebase-login/ -H "Content-Type: application/json" -d "{\"idToken\":\"test\"}"
   ```

## ✅ Solution la Plus Probable

**90% des cas**: L'utilisateur n'existe pas dans Firebase Console.

**Action immédiate**:
1. Allez sur https://console.firebase.google.com/project/prosmat-auth/authentication/users
2. Créez un utilisateur avec l'email que vous essayez d'utiliser
3. Réessayez la connexion

---

**Date**: 11 février 2026
**Projet**: ProSMAT
**Statut**: En diagnostic
