# 👤 CRÉER UN ADMIN SUR RENDER

## ✅ Solution Automatique (Recommandé)

J'ai créé une commande qui crée automatiquement un admin au déploiement!

### Étape 1: Configurer les Variables d'Environnement

Sur Render, ajoutez ces variables:

```env
ADMIN_USERNAME=admin
ADMIN_EMAIL=tatchida@gmail.com
ADMIN_PASSWORD=VotreMotDePasseSecurise123!
```

**⚠️ IMPORTANT**: Choisissez un mot de passe FORT!

### Étape 2: Redéployer

1. Les modifications sont déjà sur GitHub
2. Render va redéployer automatiquement
3. L'admin sera créé automatiquement!

### Étape 3: Se Connecter

1. Allez sur votre application: `https://prosmat-se.onrender.com`
2. Connectez-vous avec:
   - **Username**: `admin` (ou celui que vous avez configuré)
   - **Password**: Le mot de passe que vous avez configuré

---

## 🔧 Solution Manuelle (Si l'automatique ne fonctionne pas)

### Via le Shell Render

1. **Allez dans votre Web Service**
2. **Cliquez sur "Shell"**
3. **Cliquez sur "Launch Shell"**
4. **Exécutez**:

```bash
python manage.py createsuperuser
```

5. **Entrez**:
   - Username: `admin`
   - Email: `tatchida@gmail.com`
   - Password: (votre mot de passe)
   - Password (again): (même mot de passe)

---

## 🆘 Si vous avez une Erreur 500

### Cause Probable: Base de Données Non Migrée

**Solution**:

1. **Dans le Shell Render**:
```bash
python manage.py migrate
```

2. **Puis créez l'admin**:
```bash
python manage.py createsuperuser
```

---

## 📋 Vérification

### Tester la Connexion

1. Allez sur: `https://prosmat-se.onrender.com/accounts/login/`
2. Entrez vos identifiants
3. Vous devriez voir le dashboard!

### Accéder à l'Admin Django

1. Allez sur: `https://prosmat-se.onrender.com/admin/`
2. Connectez-vous avec les mêmes identifiants
3. Vous pouvez créer d'autres utilisateurs ici!

---

## 👥 Créer d'Autres Utilisateurs

### Via l'Admin Django

1. Allez sur `/admin/`
2. Cliquez sur "Users" → "Add User"
3. Configurez:
   - **Username**: nom de l'utilisateur
   - **Password**: mot de passe
   - **Region**: Choisissez la région (MARITIME, PLATEAUX, etc.)
   - **Permissions**: Cochez les cases appropriées

### Types d'Utilisateurs

**Coordinateur National** (Accès complet):
- `is_staff`: ✅
- `is_superuser`: ✅
- `region`: NATIONAL

**Coordinateur Régional** (Accès à une région):
- `is_staff`: ✅
- `is_superuser`: ❌
- `region`: MARITIME, PLATEAUX, CENTRALE, KARA, ou SAVANES

**Saisisseur** (Saisie uniquement):
- `is_staff`: ❌
- `is_superuser`: ❌
- `region`: Sa région

---

## 🔐 Sécurité

### Bonnes Pratiques

1. **Mot de passe fort**: Minimum 12 caractères, majuscules, minuscules, chiffres, symboles
2. **Changez le mot de passe par défaut** après la première connexion
3. **Ne partagez pas** les identifiants admin
4. **Créez des comptes séparés** pour chaque utilisateur

### Changer le Mot de Passe

**Via l'interface**:
1. Connectez-vous
2. Allez dans "Profil"
3. Cliquez sur "Changer le mot de passe"

**Via le Shell**:
```bash
python manage.py changepassword admin
```

---

## ✅ Checklist

- [ ] Variables d'environnement configurées (ADMIN_USERNAME, ADMIN_EMAIL, ADMIN_PASSWORD)
- [ ] Code poussé sur GitHub
- [ ] Render a redéployé
- [ ] Admin créé automatiquement
- [ ] Connexion testée
- [ ] Mot de passe changé (si nécessaire)
- [ ] Autres utilisateurs créés

---

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
