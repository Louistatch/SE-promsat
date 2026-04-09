# 🎭 Gestion des Rôles pour les Utilisateurs Firebase

## 📋 Vue d'Ensemble

Maintenant que vous utilisez Firebase pour l'authentification, voici comment gérer les rôles des utilisateurs créés via Firebase.

## 🔄 Mécanisme de Fonctionnement

### 1. Création Automatique dans Django

Quand un utilisateur se connecte via Firebase pour la première fois:
1. Firebase authentifie l'utilisateur
2. Django reçoit le token Firebase
3. Django crée automatiquement l'utilisateur dans la base de données
4. **Rôle par défaut**: `CHARGE_PROJET`
5. **Région**: `null` (à définir plus tard)

### 2. Attribution des Rôles

Vous avez **3 méthodes** pour attribuer les rôles:

## 🎯 Méthode 1: Via l'Interface d'Administration Django (Recommandé)

### Accès
```
http://localhost:8000/admin/accounts/user/
```

### Étapes
1. Connectez-vous en tant qu'administrateur
2. Allez dans **Accounts** > **Utilisateurs**
3. Cliquez sur l'utilisateur à modifier
4. Section **"Rôle et Région ProSMAT"**:
   - Sélectionnez le **Rôle**
   - Sélectionnez la **Région** (si applicable)
5. Cliquez **"Enregistrer"**

### Actions en Masse
Vous pouvez sélectionner plusieurs utilisateurs et:
- Définir comme Chargé de Projet
- Définir comme Coordonnateur
- Définir comme Évaluateur
- Définir comme Administrateur

## 🎯 Méthode 2: Via l'Interface de Gestion des Utilisateurs

### Accès
```
http://localhost:8000/accounts/manage-users/
```

### Fonctionnalités
- **Vue d'ensemble**: Statistiques par rôle
- **Liste complète**: Tous les utilisateurs avec leurs rôles
- **Modification rapide**: Bouton d'édition pour chaque utilisateur
- **Filtrage**: Par rôle, région, statut

### Étapes
1. Accédez à la page de gestion
2. Cliquez sur le bouton **"Modifier"** (icône crayon)
3. Sélectionnez le nouveau rôle et la région
4. Cliquez **"Enregistrer"**

## 🎯 Méthode 3: Via Script Python (Pour Migration en Masse)

### Script de Migration

Créez un fichier `attribuer_roles.py`:

```python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

# Attribuer des rôles par email
roles_mapping = {
    'tatchida@gmail.com': ('ADMIN', None),
    'coordo@prosmat.tg': ('COORDONNATEUR', None),
    'charge1@prosmat.tg': ('CHARGE_PROJET', 'MARITIME'),
    'charge2@prosmat.tg': ('CHARGE_PROJET', 'PLATEAUX'),
}

for email, (role, region) in roles_mapping.items():
    try:
        user = User.objects.get(email=email)
        user.role = role
        if region:
            user.region = region
        user.save()
        print(f'✅ {email}: {role} - {region or "Aucune région"}')
    except User.DoesNotExist:
        print(f'❌ {email}: Utilisateur non trouvé')
```

Exécutez:
```bash
python attribuer_roles.py
```

## 📊 Rôles Disponibles

### 1. CHARGE_PROJET (Chargé de Projet)
- **Accès**: Limité à sa région
- **Permissions**: Gestion des activités de sa région
- **Région**: Obligatoire

### 2. COORDONNATEUR (Coordonnateur)
- **Accès**: Toutes les régions
- **Permissions**: Supervision et coordination
- **Région**: Optionnelle

### 3. EVALUATEUR (Évaluateur)
- **Accès**: Toutes les régions
- **Permissions**: Évaluation et reporting
- **Région**: Optionnelle

### 4. ADMIN (Administrateur)
- **Accès**: Complet
- **Permissions**: Gestion complète du système
- **Région**: Non applicable

## 🔄 Workflow Recommandé

### Pour un Nouvel Utilisateur Firebase

1. **L'utilisateur se connecte via Firebase**
   - Première connexion
   - Compte créé automatiquement dans Django
   - Rôle par défaut: CHARGE_PROJET

2. **L'administrateur attribue le rôle**
   - Via /admin/ ou /accounts/manage-users/
   - Sélectionne le rôle approprié
   - Définit la région si nécessaire

3. **L'utilisateur se reconnecte**
   - Les permissions sont appliquées
   - Accès selon son rôle

## 🎨 Interface de Gestion

### Statistiques Affichées
- Total des utilisateurs
- Nombre de Chargés de Projet
- Nombre de Coordonnateurs
- Nombre d'Administrateurs

### Tableau des Utilisateurs
Colonnes:
- Nom complet
- Email
- Rôle (avec badge coloré)
- Région
- Statut (Actif/Inactif)
- Date de création
- Actions (Modifier/Configurer)

### Badges de Rôle
- 🔵 Chargé de Projet: Bleu
- 🟢 Coordonnateur: Vert
- 🟡 Évaluateur: Jaune
- 🔴 Administrateur: Rouge

## 🔐 Permissions et Sécurité

### Qui Peut Gérer les Rôles?

**Via /admin/**:
- Utilisateurs avec `is_staff=True`
- Superusers

**Via /accounts/manage-users/**:
- Utilisateurs avec `role=ADMIN`

### Protection
- Décorateur `@user_passes_test(is_admin)`
- Vérification du rôle ADMIN
- Logs de toutes les modifications

## 📝 Exemples Pratiques

### Exemple 1: Nouvel Utilisateur Firebase

```
1. Jean se connecte via Firebase (jean@prosmat.tg)
2. Django crée automatiquement:
   - Username: jean
   - Email: jean@prosmat.tg
   - Rôle: CHARGE_PROJET
   - Région: null

3. Admin va sur /admin/accounts/user/
4. Trouve Jean et modifie:
   - Rôle: COORDONNATEUR
   - Région: (laisse vide)

5. Jean se reconnecte
6. Il a maintenant accès à toutes les régions
```

### Exemple 2: Migration en Masse

```python
# Script pour attribuer les rôles à tous les chargés de projet
from accounts.models import User

# Tous les utilisateurs sans région deviennent coordonnateurs
User.objects.filter(region__isnull=True).update(role='COORDONNATEUR')

# Attribuer les régions aux chargés de projet
regions = {
    'MARITIME': ['user1@email.com', 'user2@email.com'],
    'PLATEAUX': ['user3@email.com'],
    # ...
}

for region, emails in regions.items():
    User.objects.filter(email__in=emails).update(
        role='CHARGE_PROJET',
        region=region
    )
```

## 🚀 Commandes Utiles

### Lister tous les utilisateurs avec leurs rôles
```bash
python manage.py shell
```

```python
from accounts.models import User

for user in User.objects.all():
    print(f"{user.email}: {user.get_role_display()} - {user.get_region_display() or 'Aucune'}")
```

### Compter par rôle
```python
from accounts.models import User
from django.db.models import Count

User.objects.values('role').annotate(count=Count('id'))
```

### Trouver les utilisateurs sans région
```python
User.objects.filter(role='CHARGE_PROJET', region__isnull=True)
```

## ✅ Checklist de Configuration

- [ ] Interface d'admin configurée
- [ ] Page de gestion des utilisateurs accessible
- [ ] Rôles par défaut définis
- [ ] Administrateurs identifiés
- [ ] Régions attribuées aux chargés de projet
- [ ] Permissions testées
- [ ] Documentation partagée avec l'équipe

## 📞 Support

### Problèmes Courants

**Q: Un utilisateur Firebase n'apparaît pas dans Django**
R: Il doit se connecter au moins une fois via Firebase

**Q: Comment changer le rôle par défaut?**
R: Modifiez `default='CHARGE_PROJET'` dans `accounts/models.py`

**Q: Un utilisateur ne voit pas les bonnes données**
R: Vérifiez son rôle et sa région dans /admin/

**Q: Comment donner l'accès admin à un utilisateur Firebase?**
R: Dans /admin/, cochez "Staff status" et définissez role=ADMIN

---

**Date**: 11 février 2026  
**Projet**: ProSMAT  
**Statut**: ✅ Système de gestion des rôles opérationnel
