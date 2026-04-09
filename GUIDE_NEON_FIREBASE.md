# Guide: Migration vers Neon PostgreSQL + Firebase Auth

## 🗄️ PARTIE 1: Configuration Neon PostgreSQL

### Étape 1: Créer un compte Neon

1. Aller sur: https://neon.tech
2. Cliquer sur "Sign Up"
3. Se connecter avec GitHub, Google ou Email
4. Créer un nouveau projet:
   - Nom: `prosmat-db`
   - Région: Choisir la plus proche (Europe West recommandé)
   - PostgreSQL version: 15 ou 16

### Étape 2: Récupérer les informations de connexion

Une fois le projet créé, vous verrez:
```
Connection String:
postgresql://[user]:[password]@[host]/[database]?sslmode=require
```

Exemple:
```
postgresql://prosmat_user:AbCd1234XyZ@ep-cool-name-123456.eu-central-1.aws.neon.tech/prosmat_db?sslmode=require
```

**IMPORTANT:** Copiez cette chaîne de connexion, vous en aurez besoin!

### Étape 3: Installer les dépendances PostgreSQL

```bash
pip install psycopg2-binary dj-database-url
```

### Étape 4: Configurer Django pour Neon

Créer/Modifier le fichier `.env`:
```env
# Neon PostgreSQL
DATABASE_URL=postgresql://[votre-connection-string]

# Django
SECRET_KEY=votre-secret-key-django
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Firebase (à remplir plus tard)
FIREBASE_API_KEY=
FIREBASE_AUTH_DOMAIN=
FIREBASE_PROJECT_ID=
FIREBASE_STORAGE_BUCKET=
FIREBASE_MESSAGING_SENDER_ID=
FIREBASE_APP_ID=
```

---

## 🔥 PARTIE 2: Configuration Firebase Authentication

### Étape 1: Créer un projet Firebase

1. Aller sur: https://console.firebase.google.com
2. Cliquer sur "Ajouter un projet"
3. Nom du projet: `prosmat-auth`
4. Désactiver Google Analytics (optionnel)
5. Cliquer sur "Créer le projet"

### Étape 2: Activer l'authentification

1. Dans le menu latéral, cliquer sur "Authentication"
2. Cliquer sur "Commencer"
3. Activer les méthodes de connexion:
   - ✅ Email/Mot de passe
   - ✅ Google (optionnel)
   - ✅ Anonyme (optionnel pour les tests)

### Étape 3: Créer une application Web

1. Dans "Paramètres du projet" (icône engrenage)
2. Faire défiler jusqu'à "Vos applications"
3. Cliquer sur l'icône Web `</>`
4. Nom de l'app: `ProSMAT Web`
5. Cocher "Configurer Firebase Hosting" (optionnel)
6. Cliquer sur "Enregistrer l'application"

### Étape 4: Récupérer la configuration Firebase

Vous verrez un code comme:
```javascript
const firebaseConfig = {
  apiKey: "AIzaSyXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  authDomain: "prosmat-auth.firebaseapp.com",
  projectId: "prosmat-auth",
  storageBucket: "prosmat-auth.appspot.com",
  messagingSenderId: "123456789012",
  appId: "1:123456789012:web:abcdef123456"
};
```

**Copiez ces valeurs!**

### Étape 5: Installer les dépendances Firebase

```bash
pip install firebase-admin python-decouple
```

---

## 🔧 PARTIE 3: Configuration de l'Application

### Fichiers à créer/modifier:

1. `.env` - Variables d'environnement
2. `config/settings.py` - Configuration Django
3. `accounts/firebase_auth.py` - Backend d'authentification Firebase
4. `accounts/views.py` - Vues d'authentification
5. `templates/accounts/login.html` - Page de connexion avec Firebase

---

## 📊 PARTIE 4: Migration des Données

### Étape 1: Exporter les données SQLite

```bash
python manage.py dumpdata > backup_sqlite.json
```

### Étape 2: Configurer Neon dans settings.py

### Étape 3: Créer les tables dans Neon

```bash
python manage.py migrate
```

### Étape 4: Importer les données

```bash
python manage.py loaddata backup_sqlite.json
```

### Étape 5: Réimporter les indicateurs

```bash
python import_prosmat_complet.py
```

---

## ✅ PARTIE 5: Tests

### Test 1: Connexion à Neon
```bash
python manage.py dbshell
```

### Test 2: Vérifier les données
```bash
python verifier_donnees.py
```

### Test 3: Tester l'authentification Firebase
- Créer un compte
- Se connecter
- Se déconnecter

---

## 🚀 Prochaines Étapes

Voulez-vous que je commence par:
1. Configuration de Neon PostgreSQL
2. Configuration de Firebase Auth
3. Les deux en même temps

Dites-moi et je créerai les fichiers nécessaires!
