# 👑 Administrateurs Automatiques

## 🎯 Emails Admin Automatiques

Les emails suivants deviennent automatiquement **ADMIN** lors de leur première connexion Firebase:

### 1. tatchida@gmail.com
- **Rôle**: ADMIN
- **Permissions**: Superuser + Staff
- **Méthode**: Connexion Firebase (Email/Password ou Google)
- **Automatique**: ✅ Oui

### 2. admin@prosmat.tg
- **Rôle**: ADMIN
- **Permissions**: Superuser + Staff
- **Méthode**: Django Admin ou Firebase
- **Mot de passe Django**: ProSMAT2026!
- **Automatique**: ✅ Oui

---

## 🔧 Comment ça fonctionne?

### Lors de la Première Connexion Firebase

Quand un utilisateur se connecte pour la première fois via Firebase:

1. Le système vérifie si l'email est dans la liste des admins automatiques
2. Si oui:
   - Rôle: **ADMIN**
   - is_staff: **True**
   - is_superuser: **True**
3. Si non:
   - Rôle: **CHARGE_PROJET** (par défaut)
   - is_staff: **False**
   - is_superuser: **False**

### Code Source

Fichier: `accounts/firebase_auth.py`

```python
# Liste des emails qui doivent être admin automatiquement
admin_emails = ['tatchida@gmail.com', 'admin@prosmat.tg']

if email.lower() in admin_emails:
    default_role = 'ADMIN'
    is_staff = True
    is_superuser = True
else:
    default_role = 'CHARGE_PROJET'
    is_staff = False
    is_superuser = False
```

---

## ✅ Avantages

### Pour tatchida@gmail.com
- ✅ Pas besoin de créer un compte séparé
- ✅ Connexion directe avec Google
- ✅ Admin automatiquement
- ✅ Accès complet au système

### Pour admin@prosmat.tg
- ✅ Compte de secours
- ✅ Connexion Django Admin
- ✅ Mot de passe connu
- ✅ Toujours disponible

---

## 🚀 Utilisation

### Connexion avec tatchida@gmail.com

1. Allez sur: https://prosmat-togo.onrender.com/accounts/login/
2. Cliquez sur **"Sign in with Google"**
3. Sélectionnez le compte **tatchida@gmail.com**
4. Vous êtes automatiquement **ADMIN**!

### Connexion avec admin@prosmat.tg

**Via Firebase:**
1. Allez sur: https://prosmat-togo.onrender.com/accounts/login/
2. Email: admin@prosmat.tg
3. Mot de passe: (celui configuré dans Firebase)

**Via Django Admin:**
1. Allez sur: https://prosmat-togo.onrender.com/admin/
2. Email: admin@prosmat.tg
3. Mot de passe: ProSMAT2026!

---

## 🔐 Sécurité

### Bonnes Pratiques

1. **Changez le mot de passe** de admin@prosmat.tg immédiatement après le premier déploiement
2. **Activez 2FA** sur tatchida@gmail.com dans Firebase Console
3. **Limitez l'accès** à ces emails
4. **Surveillez les connexions** dans les logs

### Ajouter d'Autres Admins Automatiques

Pour ajouter d'autres emails à la liste des admins automatiques:

1. Éditez `accounts/firebase_auth.py`
2. Ajoutez l'email dans la liste:
   ```python
   admin_emails = [
       'tatchida@gmail.com',
       'admin@prosmat.tg',
       'nouvel-admin@example.com',  # Nouveau
   ]
   ```
3. Commitez et poussez:
   ```bash
   git add accounts/firebase_auth.py
   git commit -m "feat: Ajout nouvel admin automatique"
   git push origin main
   ```

---

## 📊 Vérification

### Vérifier le Rôle

Après connexion, vérifiez votre rôle:

1. Allez sur: https://prosmat-togo.onrender.com/accounts/profile/
2. Vérifiez: **Rôle: Administrateur**

Ou via Django Admin:
1. https://prosmat-togo.onrender.com/admin/accounts/user/
2. Cherchez votre email
3. Vérifiez les champs:
   - Role: ADMIN
   - Staff status: ✓
   - Superuser status: ✓

### Tester les Permissions

En tant qu'admin, vous devez avoir accès à:

- ✅ Dashboard Exécutif
- ✅ Gestion des utilisateurs (/accounts/manage-users/)
- ✅ Django Admin (/admin/)
- ✅ Toutes les régions
- ✅ Synthèse Nationale
- ✅ Contrôle Qualité
- ✅ Exports (Excel/PDF)

---

## 🔄 Workflow Complet

### Premier Déploiement

1. **Build Render** exécute `charger_donnees`
2. Crée les comptes:
   - admin@prosmat.tg (avec mot de passe)
   - tatchida@gmail.com (préparé pour Firebase)

### Première Connexion tatchida@gmail.com

1. Utilisateur se connecte via Firebase
2. Backend vérifie l'email
3. Email reconnu comme admin automatique
4. Compte mis à jour:
   - role = 'ADMIN'
   - is_staff = True
   - is_superuser = True
5. Utilisateur redirigé avec tous les droits

### Connexions Suivantes

1. Utilisateur se connecte
2. Compte déjà existant avec rôle ADMIN
3. Connexion normale avec tous les droits

---

## 🐛 Dépannage

### Problème: Je ne suis pas admin après connexion

**Solution 1**: Vérifiez l'email
- L'email doit être exactement: `tatchida@gmail.com`
- Pas de majuscules, pas d'espaces

**Solution 2**: Vérifiez dans Django Admin
```bash
# Via Shell Render (si disponible)
python manage.py shell

from accounts.models import User
user = User.objects.get(email='tatchida@gmail.com')
user.role = 'ADMIN'
user.is_staff = True
user.is_superuser = True
user.save()
```

**Solution 3**: Utilisez le script
```bash
python donner_admin.py
# Entrez: tatchida@gmail.com
```

### Problème: admin@prosmat.tg ne fonctionne pas

**Solution**: Réinitialisez le mot de passe
```bash
python manage.py changepassword admin@prosmat.tg
```

---

## 📝 Notes Importantes

1. **Emails sensibles à la casse**: Le système convertit en minuscules automatiquement
2. **Première connexion**: Le rôle est attribué à la création du compte
3. **Modifications manuelles**: Vous pouvez toujours changer le rôle via Django Admin
4. **Sécurité**: Ces emails ont un accès complet au système

---

## 🎉 Résumé

- ✅ **tatchida@gmail.com** est admin automatiquement
- ✅ **admin@prosmat.tg** est admin automatiquement
- ✅ Connexion Firebase ou Django Admin
- ✅ Tous les droits et permissions
- ✅ Pas de configuration manuelle nécessaire

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Mis à jour le: 11 février 2026*
