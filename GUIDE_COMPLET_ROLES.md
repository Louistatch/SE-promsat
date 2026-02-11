# Guide Complet - Gestion des Rôles Firebase

## 📋 Vue d'ensemble

Le système de gestion des rôles permet d'attribuer et de gérer les rôles et régions des utilisateurs créés via Firebase Authentication.

### Rôles disponibles
- **CHARGE_PROJET** : Chargé de Projet (rôle par défaut)
- **COORDONNATEUR** : Coordonnateur
- **EVALUATEUR** : Évaluateur
- **ADMIN** : Administrateur

### Régions disponibles
- **MARITIME** : Région Maritime
- **PLATEAUX** : Région des Plateaux
- **CENTRALE** : Région Centrale
- **KARA** : Région de la Kara
- **SAVANES** : Région des Savanes

---

## 🎯 Méthodes de gestion des rôles

### 1️⃣ Interface Web de Gestion (Recommandée)

**URL**: `http://127.0.0.1:8000/accounts/manage-users/`

**Accès**: Réservé aux administrateurs (role=ADMIN)

**Fonctionnalités**:
- Vue d'ensemble avec statistiques
- Liste complète des utilisateurs
- Modification en temps réel des rôles et régions
- Interface moderne et intuitive
- Filtrage et recherche

**Comment utiliser**:
1. Connectez-vous avec un compte ADMIN
2. Accédez à `/accounts/manage-users/`
3. Cliquez sur "Modifier" pour un utilisateur
4. Sélectionnez le nouveau rôle et/ou région
5. Cliquez sur "Enregistrer"

---

### 2️⃣ Interface Django Admin

**URL**: `http://127.0.0.1:8000/admin/accounts/user/`

**Accès**: Utilisateurs avec `is_staff=True`

**Fonctionnalités**:
- Interface d'administration complète
- Actions en masse (bulk actions)
- Filtres avancés par rôle et région
- Recherche par email, nom, prénom
- Modification détaillée des utilisateurs

**Actions en masse disponibles**:
- Définir comme Chargé de Projet
- Définir comme Coordonnateur
- Définir comme Évaluateur
- Définir comme Administrateur
- Activer/Désactiver les comptes

**Comment utiliser**:
1. Connectez-vous à l'admin Django
2. Allez dans "Utilisateurs"
3. Sélectionnez un ou plusieurs utilisateurs
4. Choisissez une action dans le menu déroulant
5. Cliquez sur "Exécuter"

---

### 3️⃣ Script Python (Ligne de commande)

**Fichier**: `attribuer_roles.py`

**Accès**: Ligne de commande

**Fonctionnalités**:
- Attribution rapide de rôles
- Modification en masse
- Idéal pour l'automatisation
- Pas besoin d'interface web

**Comment utiliser**:

```bash
# Exécuter le script
python attribuer_roles.py
```

Le script vous guidera à travers les étapes:
1. Liste tous les utilisateurs
2. Demande l'email de l'utilisateur
3. Affiche les rôles disponibles
4. Demande le nouveau rôle
5. Demande la région (optionnel)
6. Confirme les modifications

**Exemple d'utilisation**:
```
Email de l'utilisateur: tatchida@gmail.com
Nouveau rôle (1-4): 4
Région (1-5 ou Enter pour ignorer): 1
✓ Rôle mis à jour avec succès!
```

---

## 🔐 Permissions et Accès

### Permissions par rôle

| Fonctionnalité | CHARGE_PROJET | COORDONNATEUR | EVALUATEUR | ADMIN |
|----------------|---------------|---------------|------------|-------|
| Voir sa région | ✅ | ✅ | ✅ | ✅ |
| Voir toutes les régions | ❌ | ✅ | ✅ | ✅ |
| Dashboard Exécutif | ❌ | ✅ | ✅ | ✅ |
| Synthèse Nationale | ❌ | ✅ | ✅ | ✅ |
| Contrôle Qualité | ❌ | ✅ | ✅ | ✅ |
| Exports (Excel/PDF) | ❌ | ✅ | ✅ | ✅ |
| Gérer les utilisateurs | ❌ | ❌ | ❌ | ✅ |
| Accès Django Admin | ❌ | ❌ | ❌ | ✅* |

*Nécessite aussi `is_staff=True`

### Accès aux données

**CHARGE_PROJET**:
- Accès limité à sa région uniquement
- Peut saisir et voir les réalisations de sa région
- Peut voir les activités de sa région

**COORDONNATEUR, EVALUATEUR, ADMIN**:
- Accès à toutes les régions
- Vue d'ensemble nationale
- Rapports consolidés

---

## 🚀 Workflow de création d'utilisateur

### Étape 1: Création via Firebase
1. L'utilisateur s'inscrit via l'interface Firebase
2. Firebase crée le compte d'authentification
3. L'utilisateur se connecte pour la première fois

### Étape 2: Création automatique dans Django
1. Lors de la première connexion, Django crée automatiquement:
   - Un utilisateur dans la base de données
   - Avec le rôle par défaut: **CHARGE_PROJET**
   - Sans région assignée

### Étape 3: Attribution du rôle (par un admin)
1. Un administrateur accède à l'interface de gestion
2. Sélectionne l'utilisateur
3. Attribue le rôle approprié
4. Attribue la région (si CHARGE_PROJET)

### Étape 4: Accès aux fonctionnalités
1. L'utilisateur se reconnecte
2. Accède aux fonctionnalités selon son rôle
3. Voit les données selon sa région (si applicable)

---

## 📊 Statistiques actuelles

**Utilisateurs**: 15 comptes créés

**Par rôle**:
- Chargé de Projet: 12
- Coordonnateur: 1
- Évaluateur: 1
- Administrateur: 1

**Par région**:
- Région Maritime: 2
- Région des Plateaux: 2
- Région Centrale: 2
- Région de la Kara: 2
- Région des Savanes: 2

---

## 🧪 Tests et Vérification

### Tester le système

```bash
# Vérifier les utilisateurs et leurs rôles
python tester_roles.py
```

Ce script affiche:
- Liste complète des utilisateurs
- Rôles et régions assignés
- Statistiques par rôle et région
- URLs d'accès aux interfaces

### Vérifier les permissions

1. Connectez-vous avec différents rôles
2. Vérifiez l'accès aux menus:
   - CHARGE_PROJET: Pas de "Dashboard Exécutif"
   - COORDONNATEUR+: Tous les menus visibles

---

## 🔧 Dépannage

### Problème: Utilisateur ne voit pas les bonnes données

**Solution**:
1. Vérifiez le rôle: `python tester_roles.py`
2. Si CHARGE_PROJET, vérifiez que la région est assignée
3. Déconnectez et reconnectez l'utilisateur

### Problème: Impossible d'accéder à /accounts/manage-users/

**Solution**:
1. Vérifiez que vous êtes connecté avec un compte ADMIN
2. Vérifiez le rôle: `python tester_roles.py`
3. Si nécessaire, utilisez le script pour vous donner le rôle ADMIN

### Problème: Nouveau compte Firebase n'apparaît pas

**Solution**:
1. L'utilisateur doit se connecter au moins une fois
2. La création Django est automatique à la première connexion
3. Vérifiez les logs: `logs/django.log`

---

## 📝 Bonnes pratiques

### Attribution des rôles

1. **CHARGE_PROJET**: 
   - Toujours assigner une région
   - Pour les agents de terrain
   - Accès limité à leur zone

2. **COORDONNATEUR**:
   - Pas de région (accès national)
   - Pour la coordination du projet
   - Accès aux rapports consolidés

3. **EVALUATEUR**:
   - Pas de région (accès national)
   - Pour le suivi-évaluation
   - Accès au contrôle qualité

4. **ADMIN**:
   - Pas de région (accès national)
   - Pour l'administration système
   - Gestion des utilisateurs

### Sécurité

- Ne donnez le rôle ADMIN qu'aux personnes de confiance
- Vérifiez régulièrement les comptes actifs
- Désactivez les comptes inutilisés
- Utilisez des emails professionnels

---

## 📞 Support

Pour toute question ou problème:
1. Consultez ce guide
2. Exécutez `python tester_roles.py` pour diagnostiquer
3. Vérifiez les logs dans `logs/django.log`
4. Contactez l'administrateur système

---

**Dernière mise à jour**: 11 février 2026
**Version**: 1.0
