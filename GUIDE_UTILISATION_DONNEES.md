# Guide d'Utilisation - Données ProSMAT Importées

## 🎯 Vue d'Ensemble

L'application ProSMAT a été mise à jour avec **75 indicateurs réels** provenant du fichier Excel officiel. Toutes les valeurs de référence et cibles sont maintenant dans le système.

## 🚀 Démarrage Rapide

### 1. Vérifier l'Importation

```bash
# Activer l'environnement virtuel
venv_prosmat\Scripts\activate

# Vérifier les données
python verifier_donnees.py
```

Vous devriez voir:
- ✅ 75 indicateurs importés
- ✅ 16 périodes créées (2024-2027)
- ✅ 5 composantes principales
- ✅ Toutes les valeurs de référence et cibles

### 2. Démarrer l'Application

```bash
# Démarrer le serveur
python manage.py runserver

# Ou utiliser le fichier batch
LANCER_MAINTENANT.bat
```

Accéder à: http://localhost:8000

### 3. Se Connecter

Utiliser un compte administrateur existant ou créer un nouveau:

```bash
python manage.py createsuperuser
```

## 📊 Données Disponibles

### Composante 1: Production Agroécologique (8 indicateurs)

**Indicateurs clés:**
- `IND-1-001`: Superficie sous pratiques agroécologiques (0 → 1250 ha)
- `IND-1-007`: Maraîchers formés (360 → 5000 personnes)
- `IND-1-008`: Taux d'adoption des pratiques (0% → 70%)

### Composante 2: Valorisation (8 indicateurs)

**Indicateurs clés:**
- `IND-2-001`: Espaces de vente aménagés (0 → 5)
- `IND-2-004`: Agriculteurs avec accès marché (0 → 5000)
- `IND-2-006`: Unités de transformation renforcées (0 → 25)

### Composante 3: Renforcement des Capacités (7 indicateurs)

**Indicateurs clés:**
- `IND-3-001`: Organisations de producteurs soutenues (0 → 286)
- `IND-3-004`: Personnes formées en leadership (0 → 9885)

### Genre et Inclusion (6 indicateurs)

**Indicateurs clés:**
- `IND-GENRE-001`: Bénéficiaires directs total (0 → 9885)
- `IND-GENRE-002`: Bénéficiaires femmes (0 → 5720, soit 58%)
- `IND-GENRE-004`: Emplois créés pour femmes (0 → 2414 ETP)

### Indicateurs GAFSP (14 indicateurs)

Tous les indicateurs du cadre GAFSP avec leurs codes officiels:
- `GAFSP-01`: Bénéficiaires directs
- `GAFSP-02`: Superficie avec soutien production
- `GAFSP-09`: Emplois créés (ETP)
- etc.

## 📝 Prochaines Étapes

### 1. Saisir les Réalisations

1. Aller dans **Monitoring** → **Réalisations**
2. Cliquer sur **Nouvelle Réalisation**
3. Sélectionner:
   - Indicateur
   - Période (trimestre)
   - Région
   - Valeur réalisée
4. Enregistrer

**Exemple:**
```
Indicateur: IND-1-007 (Maraîchers formés)
Période: T1 2024
Région: MARITIME
Valeur réalisée: 150
Dont femmes: 85
```

### 2. Créer des Activités

1. Aller dans **Monitoring** → **Activités**
2. Cliquer sur **Nouvelle Activité**
3. Remplir:
   - Nom de l'activité
   - Sous-composante
   - Dates prévues
   - Budget
   - Responsable
4. Enregistrer

### 3. Consulter le Dashboard

1. Aller sur la page d'accueil
2. Voir les statistiques en temps réel:
   - Total des réalisations
   - Taux d'atteinte des cibles
   - Performance par région
   - Alertes qualité

### 4. Générer des Rapports

1. Aller dans **Monitoring** → **Rapports**
2. Sélectionner:
   - Type de rapport
   - Période
   - Région (optionnel)
3. Générer et télécharger

## 🔍 Recherche et Filtrage

### Rechercher un Indicateur

**Par code:**
```
Dans l'admin: Monitoring → Indicateurs
Rechercher: IND-1-001
```

**Par composante:**
```
Filtrer par: Composante 1: Production Agroécologique
```

**Par type GAFSP:**
```
Rechercher: GAFSP
```

### Filtrer les Réalisations

**Par période:**
```
Monitoring → Réalisations
Filtrer: Trimestre 1 2024
```

**Par région:**
```
Filtrer: MARITIME
```

**Par statut:**
```
Filtrer: Validées / En attente
```

## 📈 Visualisations Disponibles

### Dashboard Principal
- Statistiques globales
- Dernières réalisations
- Activités en cours
- Alertes récentes

### Dashboard Exécutif
- KPI principaux (bénéficiaires, emplois, performance)
- Performance par région
- Atteinte par composante
- Évolution temporelle
- Graphiques interactifs

### Statistiques
- Réalisations par région
- Budget exécuté
- Taux de validation
- Progression vers les cibles

## 🎨 Personnalisation

### Ajouter de Nouveaux Indicateurs

1. Modifier `import_prosmat_complet.py`
2. Ajouter l'indicateur dans la liste appropriée
3. Réexécuter: `python import_prosmat_complet.py`

### Modifier les Périodes

```python
# Dans import_donnees_excel.py
annees = [2024, 2025, 2026, 2027, 2028]  # Ajouter 2028
```

### Configurer les Alertes

Les alertes se déclenchent automatiquement pour:
- Valeurs aberrantes (> 150% de la cible)
- Incohérences genre (femmes > total)
- Données manquantes

## 🔧 Maintenance

### Sauvegarder la Base de Données

```bash
# Créer une sauvegarde
python manage.py dumpdata > backup_prosmat.json

# Restaurer depuis une sauvegarde
python manage.py loaddata backup_prosmat.json
```

### Nettoyer les Données de Test

```bash
python manage.py shell
```

```python
from monitoring.models import Realisation
# Supprimer les réalisations de test
Realisation.objects.filter(commentaire__contains='test').delete()
```

### Mettre à Jour depuis Excel

Si le fichier Excel est mis à jour:

1. Remplacer le fichier Excel
2. Réexécuter: `python import_prosmat_complet.py`
3. Les indicateurs existants seront mis à jour (pas de doublons)

## 📞 Aide et Support

### Problèmes Courants

**Erreur: "Indicateur not found"**
- Vérifier que l'importation s'est bien déroulée
- Exécuter: `python verifier_donnees.py`

**Erreur: "Permission denied"**
- Vérifier les droits utilisateur
- Se connecter avec un compte admin

**Données manquantes**
- Réexécuter l'importation
- Vérifier le chemin du fichier Excel

### Commandes Utiles

```bash
# Vérifier les données
python verifier_donnees.py

# Créer un admin
python manage.py createsuperuser

# Réinitialiser les migrations
python manage.py migrate

# Collecter les fichiers statiques
python manage.py collectstatic

# Lancer les tests
python manage.py test
```

## 📚 Documentation Complémentaire

- `IMPORTATION_DONNEES_REELLES.md` - Détails techniques de l'importation
- `DEMARRAGE_RAPIDE.md` - Guide de démarrage général
- `DEPLOIEMENT.md` - Guide de déploiement en production

## ✅ Checklist de Validation

Avant de commencer la saisie:

- [ ] Vérifier que 75 indicateurs sont importés
- [ ] Vérifier que les périodes 2024-2027 existent
- [ ] Se connecter à l'interface admin
- [ ] Consulter la liste des indicateurs
- [ ] Tester la création d'une réalisation
- [ ] Vérifier le dashboard
- [ ] Configurer les utilisateurs et leurs rôles

---

**Bon travail avec ProSMAT! 🚀**

Pour toute question, consulter la documentation ou contacter l'équipe technique.
