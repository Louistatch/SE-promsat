# 🔐 IDENTIFIANTS PAR DÉFAUT - PROSMAT

## ✅ Création Automatique au Déploiement

Tous ces utilisateurs sont créés automatiquement lors du déploiement sur Render!

---

## 👤 ADMINISTRATEUR SYSTÈME

**Accès complet à tout le système**

```
Username: admin
Password: ProSMAT2026!
Email: admin@prosmat.tg
Région: NATIONAL
Permissions: Superuser + Staff
```

**Accès**:
- ✅ Toutes les régions
- ✅ Dashboard exécutif
- ✅ Synthèse nationale
- ✅ Contrôle qualité
- ✅ Exports Excel/PDF
- ✅ Admin Django (/admin/)
- ✅ Gestion des utilisateurs

---

## 👥 COORDINATEUR NATIONAL

**Accès complet sauf gestion des utilisateurs**

```
Username: coord_national
Password: ProSMAT2026!
Email: national@prosmat.tg
Région: NATIONAL
Permissions: Staff
```

**Accès**:
- ✅ Toutes les régions
- ✅ Dashboard exécutif
- ✅ Synthèse nationale
- ✅ Contrôle qualité
- ✅ Exports Excel/PDF
- ❌ Admin Django

---

## 🌍 COORDINATEURS RÉGIONAUX

### Région MARITIME

```
Username: coord_maritime
Password: ProSMAT2026!
Email: maritime@prosmat.tg
Région: MARITIME
Permissions: Staff
```

**Accès**:
- ✅ Données région MARITIME uniquement
- ✅ Saisie des réalisations
- ✅ Validation des données
- ✅ Statistiques régionales
- ❌ Dashboard exécutif
- ❌ Synthèse nationale

---

### Région PLATEAUX

```
Username: coord_plateaux
Password: ProSMAT2026!
Email: plateaux@prosmat.tg
Région: PLATEAUX
Permissions: Staff
```

**Accès**:
- ✅ Données région PLATEAUX uniquement
- ✅ Saisie des réalisations
- ✅ Validation des données
- ✅ Statistiques régionales

---

### Région CENTRALE

```
Username: coord_centrale
Password: ProSMAT2026!
Email: centrale@prosmat.tg
Région: CENTRALE
Permissions: Staff
```

**Accès**:
- ✅ Données région CENTRALE uniquement
- ✅ Saisie des réalisations
- ✅ Validation des données
- ✅ Statistiques régionales

---

### Région KARA

```
Username: coord_kara
Password: ProSMAT2026!
Email: kara@prosmat.tg
Région: KARA
Permissions: Staff
```

**Accès**:
- ✅ Données région KARA uniquement
- ✅ Saisie des réalisations
- ✅ Validation des données
- ✅ Statistiques régionales

---

### Région SAVANES

```
Username: coord_savanes
Password: ProSMAT2026!
Email: savanes@prosmat.tg
Région: SAVANES
Permissions: Staff
```

**Accès**:
- ✅ Données région SAVANES uniquement
- ✅ Saisie des réalisations
- ✅ Validation des données
- ✅ Statistiques régionales

---

## 🔧 Configuration sur Render

### Variables d'Environnement (Optionnel)

Pour personnaliser les mots de passe, ajoutez sur Render:

```env
# Mot de passe admin personnalisé
ADMIN_PASSWORD=VotreMotDePasseSecurise123!

# Mot de passe par défaut pour tous les autres utilisateurs
DEFAULT_PASSWORD=AutreMotDePasse456!
```

**Si non configuré**: Le mot de passe par défaut sera `ProSMAT2026!`

---

## ⚠️ SÉCURITÉ - IMPORTANT!

### Après le Premier Déploiement

1. **Connectez-vous immédiatement** avec le compte admin
2. **Changez TOUS les mots de passe** via l'interface
3. **Distribuez les nouveaux identifiants** aux coordinateurs
4. **Ne partagez JAMAIS** ces identifiants par défaut publiquement

### Changer les Mots de Passe

**Via l'interface**:
1. Connectez-vous
2. Allez dans "Profil"
3. Cliquez sur "Changer le mot de passe"

**Via l'Admin Django** (pour admin seulement):
1. Allez sur `/admin/`
2. Cliquez sur "Users"
3. Sélectionnez l'utilisateur
4. Cliquez sur "Change password"

---

## 📋 Tableau Récapitulatif

| Username | Mot de Passe | Région | Accès Complet | Admin Django |
|----------|--------------|--------|---------------|--------------|
| admin | ProSMAT2026! | NATIONAL | ✅ | ✅ |
| coord_national | ProSMAT2026! | NATIONAL | ✅ | ❌ |
| coord_maritime | ProSMAT2026! | MARITIME | ❌ | ❌ |
| coord_plateaux | ProSMAT2026! | PLATEAUX | ❌ | ❌ |
| coord_centrale | ProSMAT2026! | CENTRALE | ❌ | ❌ |
| coord_kara | ProSMAT2026! | KARA | ❌ | ❌ |
| coord_savanes | ProSMAT2026! | SAVANES | ❌ | ❌ |

---

## 🚀 Déploiement

### Automatique

Les utilisateurs sont créés automatiquement lors du déploiement grâce à:
```
release: python manage.py migrate --noinput && python manage.py init_users
```

### Manuel (si nécessaire)

Dans le Shell Render:
```bash
python manage.py init_users
```

---

## ✅ Vérification

### Tester les Connexions

1. **Admin**: https://prosmat-se.onrender.com/accounts/login/
   - Username: `admin`
   - Password: `ProSMAT2026!`

2. **Coordinateur Maritime**: 
   - Username: `coord_maritime`
   - Password: `ProSMAT2026!`

3. **Etc.**

### Logs de Création

Dans les logs Render, vous verrez:
```
✅ admin créé - Région: NATIONAL
✅ coord_national créé - Région: NATIONAL
✅ coord_maritime créé - Région: MARITIME
...
```

---

## 👥 Créer d'Autres Utilisateurs

### Via l'Admin Django

1. Connectez-vous avec `admin`
2. Allez sur `/admin/`
3. Cliquez sur "Users" → "Add User"
4. Configurez selon les besoins

---

## 🆘 Problèmes Courants

### "User already exists"

Normal si vous redéployez. Les utilisateurs existants ne sont pas recréés.

### "Cannot connect"

Vérifiez que:
- L'application est bien "Live" sur Render
- Vous utilisez la bonne URL
- Les migrations ont été exécutées

### "Invalid credentials"

Vérifiez:
- Le username (pas l'email)
- Le mot de passe (sensible à la casse)
- Que l'utilisateur a bien été créé (vérifiez les logs)

---

**Date**: 8 février 2026
**Projet**: ProSMAT - Système de Suivi-Évaluation
**⚠️ CHANGEZ CES MOTS DE PASSE APRÈS LA PREMIÈRE CONNEXION!**
