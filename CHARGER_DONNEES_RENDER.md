# 📊 Charger les Données Initiales sur Render

## 🎯 Objectif

Charger les composantes, indicateurs, périodes et créer un utilisateur admin dans la base de données Neon via Render.

---

## 🚀 Méthode 1: Via le Shell Render (Recommandé)

### Étape 1: Accéder au Shell

1. Allez sur: https://dashboard.render.com/
2. Sélectionnez votre service **prosmat-togo**
3. Cliquez sur l'onglet **"Shell"** en haut
4. Attendez que le shell se charge

### Étape 2: Exécuter le Script

Dans le shell, tapez:

```bash
python charger_donnees_initiales.py
```

Appuyez sur **Entrée** et attendez (~30 secondes).

### Étape 3: Vérifier

Vous devriez voir:

```
============================================================
CHARGEMENT DES DONNÉES INITIALES
============================================================

1. Création des composantes...
   ✓ Créé: Composante 1: Amélioration de la productivité agricole
   ✓ Créé: Composante 2: Développement des chaînes de valeur
   ...

✅ DONNÉES INITIALES CHARGÉES AVEC SUCCÈS!
```

---

## 🔐 Compte Admin Créé

Le script crée automatiquement un compte admin:

```
Email: admin@prosmat.tg
Mot de passe: ProSMAT2026!
Rôle: ADMIN
```

**Testez la connexion:**
1. Allez sur: https://prosmat-togo.onrender.com/admin/
2. Connectez-vous avec les identifiants ci-dessus
3. Changez le mot de passe immédiatement!

---

## 📊 Données Chargées

### Composantes (4)
- Composante 1: Amélioration de la productivité agricole
- Composante 2: Développement des chaînes de valeur
- Composante 3: Renforcement des capacités
- Composante 4: Coordination et gestion du projet

### Sous-composantes (6)
- 1.1 Infrastructures agricoles
- 1.2 Intrants et équipements
- 2.1 Transformation et commercialisation
- 2.2 Accès aux marchés
- 3.1 Formation des producteurs
- 3.2 Appui institutionnel

### Indicateurs (5 exemples)
- IND-1.1.1: Nombre de bénéficiaires directs (Cible: 50,000)
- IND-1.1.2: Nombre d'hectares aménagés (Cible: 5,000)
- IND-1.2.1: Producteurs ayant reçu des intrants (Cible: 10,000)
- IND-2.1.1: Unités de transformation créées (Cible: 50)
- IND-3.1.1: Producteurs formés (Cible: 15,000)

### Périodes (9)
- 2024: T1, T2, T3, T4
- 2025: T1, T2, T3, T4
- 2026: T1

---

## 🔄 Méthode 2: Importer depuis SQLite (Si vous avez des données)

Si vous avez déjà des données dans votre SQLite local:

### Étape 1: Exporter depuis SQLite

```bash
# Sur votre machine locale
python manage.py dumpdata monitoring.Composante monitoring.SousComposante monitoring.Indicateur monitoring.Periode --indent 2 > donnees_prosmat.json
```

### Étape 2: Créer un Gist GitHub

1. Allez sur: https://gist.github.com/
2. Créez un nouveau Gist
3. Collez le contenu de `donnees_prosmat.json`
4. Cliquez sur "Create public gist"
5. Cliquez sur "Raw" et copiez l'URL

### Étape 3: Charger dans Render

Dans le Shell Render:

```bash
# Télécharger le fichier
curl -o donnees.json https://gist.githubusercontent.com/VOTRE-URL-RAW

# Charger les données
python manage.py loaddata donnees.json
```

---

## 🔧 Méthode 3: Via Django Admin

### Étape 1: Créer un Superuser

Dans le Shell Render:

```bash
python manage.py createsuperuser
```

Suivez les instructions:
- Username: admin
- Email: admin@prosmat.tg
- Password: (choisissez un mot de passe fort)

### Étape 2: Ajouter les Données Manuellement

1. Connectez-vous à: https://prosmat-togo.onrender.com/admin/
2. Ajoutez les composantes, sous-composantes, indicateurs manuellement

---

## ✅ Vérification

### 1. Vérifier via Django Admin

1. Allez sur: https://prosmat-togo.onrender.com/admin/
2. Connectez-vous
3. Vérifiez:
   - Composantes
   - Sous-composantes
   - Indicateurs
   - Périodes
   - Utilisateurs

### 2. Vérifier via l'Application

1. Allez sur: https://prosmat-togo.onrender.com/
2. Connectez-vous avec Firebase
3. Vérifiez que les indicateurs apparaissent dans:
   - Dashboard
   - Saisie des réalisations
   - Statistiques

---

## 🐛 Dépannage

### Problème: "No module named 'monitoring'"

**Solution**: Assurez-vous d'être dans le bon répertoire:
```bash
cd /opt/render/project/src
python charger_donnees_initiales.py
```

### Problème: "Database connection failed"

**Solution**: Vérifiez que `DATABASE_URL` est correctement configuré dans les variables d'environnement.

### Problème: "Permission denied"

**Solution**: Le script nécessite les permissions d'écriture. Utilisez le Shell Render qui a les bonnes permissions.

### Problème: Les données existent déjà

**Solution**: Le script utilise `get_or_create`, donc il ne créera pas de doublons. Vous pouvez le réexécuter sans problème.

---

## 📝 Ajouter Plus d'Indicateurs

Pour ajouter plus d'indicateurs après le chargement initial:

### Via Django Admin

1. Connectez-vous à l'admin
2. Allez dans "Indicateurs"
3. Cliquez sur "Ajouter un indicateur"
4. Remplissez les champs
5. Enregistrez

### Via Script Python

Créez un fichier `ajouter_indicateurs.py`:

```python
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Indicateur, SousComposante

# Récupérer une sous-composante
sc = SousComposante.objects.first()

# Créer un indicateur
Indicateur.objects.create(
    code="IND-X.X.X",
    libelle="Description de l'indicateur",
    sous_composante=sc,
    type_indicateur="QUANTITATIF",
    niveau="EXTRANT",
    unite_mesure="Unité",
    cible_finale=1000,
    actif=True
)
```

Puis dans le Shell Render:
```bash
python ajouter_indicateurs.py
```

---

## 🔄 Réinitialiser les Données

⚠️ **ATTENTION**: Cela supprimera TOUTES les données!

Dans le Shell Render:

```bash
# Supprimer toutes les données
python manage.py flush --no-input

# Recharger les données initiales
python charger_donnees_initiales.py
```

---

## 📞 Support

Si vous rencontrez des problèmes:

1. Vérifiez les logs Render
2. Vérifiez que la base de données Neon est accessible
3. Vérifiez les variables d'environnement
4. Contactez le support Render si nécessaire

---

**Développé avec ❤️ pour ProSMAT - Togo**

*Guide créé le: 11 février 2026*
