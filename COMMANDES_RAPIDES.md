# ⚡ Commandes Rapides - ProSMAT

## 🚀 Démarrage

### Activer l'environnement virtuel
```bash
venv_prosmat\Scripts\activate
```

### Démarrer le serveur
```bash
python manage.py runserver
```
Accès: http://localhost:8000

### Utiliser le menu interactif
```bash
OPERATIONS_PROSMAT.bat
```

## 📊 Vérification des Données

### Vérifier l'importation
```bash
python verifier_donnees.py
```

### Compter les indicateurs
```bash
python manage.py shell
>>> from monitoring.models import Indicateur
>>> Indicateur.objects.count()
75
>>> exit()
```

### Voir les composantes
```bash
python manage.py shell
>>> from monitoring.models import Composante
>>> for c in Composante.objects.all():
...     print(f"{c.nom}: {c.sous_composantes.count()} sous-composantes")
>>> exit()
```

## 🔄 Importation

### Importer/Réimporter les données
```bash
python import_prosmat_complet.py
```

### Créer les périodes uniquement
```bash
python import_donnees_excel.py
```

### Analyser le fichier Excel
```bash
python analyser_excel.py
```

## 👤 Gestion des Utilisateurs

### Créer un superutilisateur
```bash
python manage.py createsuperuser
```

### Créer un utilisateur admin via script
```bash
python manage.py create_admin
```

### Initialiser les utilisateurs de test
```bash
python manage.py init_users
```

## 🗄️ Base de Données

### Appliquer les migrations
```bash
python manage.py migrate
```

### Créer une migration
```bash
python manage.py makemigrations
```

### Sauvegarder la base de données
```bash
python manage.py dumpdata > backup.json
```

### Restaurer la base de données
```bash
python manage.py loaddata backup.json
```

### Réinitialiser la base de données
```bash
# ATTENTION: Supprime toutes les données!
del db.sqlite3
python manage.py migrate
python import_prosmat_complet.py
```

## 🔍 Consultation des Données

### Shell Django
```bash
python manage.py shell
```

### Exemples de requêtes dans le shell

#### Voir tous les indicateurs
```python
from monitoring.models import Indicateur
for ind in Indicateur.objects.all()[:10]:
    print(f"{ind.code}: {ind.libelle}")
```

#### Voir les indicateurs d'une composante
```python
from monitoring.models import Indicateur, Composante
comp = Composante.objects.get(nom__contains='Production')
indicateurs = Indicateur.objects.filter(sous_composante__composante=comp)
print(f"{comp.nom}: {indicateurs.count()} indicateurs")
```

#### Voir les indicateurs GAFSP
```python
from monitoring.models import Indicateur
gafsp = Indicateur.objects.filter(code__startswith='GAFSP')
for ind in gafsp:
    print(f"{ind.code}: {ind.cible_finale} {ind.unite_mesure}")
```

#### Voir les périodes
```python
from monitoring.models import Periode
for p in Periode.objects.all().order_by('annee', 'trimestre'):
    print(p)
```

#### Statistiques rapides
```python
from monitoring.models import Indicateur, Composante
print(f"Total indicateurs: {Indicateur.objects.count()}")
print(f"Indicateurs actifs: {Indicateur.objects.filter(actif=True).count()}")
print(f"Composantes: {Composante.objects.count()}")
```

## 📈 Gestion des Réalisations

### Créer une réalisation (shell)
```python
from monitoring.models import Realisation, Indicateur, Periode
from accounts.models import User

indicateur = Indicateur.objects.get(code='IND-1-001')
periode = Periode.objects.get(annee=2024, trimestre='T1')
user = User.objects.first()

realisation = Realisation.objects.create(
    indicateur=indicateur,
    periode=periode,
    region='MARITIME',
    valeur_realisee=50,
    femmes=25,
    saisi_par=user,
    valide=False
)
print(f"Réalisation créée: {realisation}")
```

### Voir les réalisations
```python
from monitoring.models import Realisation
for r in Realisation.objects.all()[:10]:
    print(f"{r.indicateur.code} - {r.periode}: {r.valeur_realisee}")
```

## 🎨 Fichiers Statiques

### Collecter les fichiers statiques
```bash
python manage.py collectstatic --noinput
```

### Nettoyer les fichiers statiques
```bash
rmdir /s /q staticfiles
python manage.py collectstatic --noinput
```

## 🧪 Tests

### Lancer tous les tests
```bash
python manage.py test
```

### Tester une application spécifique
```bash
python manage.py test monitoring
```

### Tester avec verbosité
```bash
python manage.py test --verbosity=2
```

## 📝 Logs et Débogage

### Voir les logs du serveur
Le serveur affiche les logs dans la console

### Mode debug
Dans `config/settings.py`:
```python
DEBUG = True
```

### Vérifier les erreurs
```bash
python manage.py check
```

### Vérifier les migrations
```bash
python manage.py showmigrations
```

## 🔧 Maintenance

### Nettoyer les sessions expirées
```bash
python manage.py clearsessions
```

### Optimiser la base de données SQLite
```bash
python manage.py shell
>>> from django.db import connection
>>> cursor = connection.cursor()
>>> cursor.execute("VACUUM")
>>> exit()
```

### Vérifier l'espace disque
```bash
dir db.sqlite3
```

## 📦 Dépendances

### Installer les dépendances
```bash
pip install -r requirements.txt
```

### Mettre à jour les dépendances
```bash
pip install --upgrade -r requirements.txt
```

### Voir les dépendances installées
```bash
pip list
```

### Créer requirements.txt
```bash
pip freeze > requirements.txt
```

## 🌐 Déploiement

### Préparer pour la production
```bash
# Collecter les fichiers statiques
python manage.py collectstatic --noinput

# Vérifier la configuration
python manage.py check --deploy

# Créer une sauvegarde
python manage.py dumpdata > backup_production.json
```

### Variables d'environnement
```bash
set DEBUG=False
set SECRET_KEY=votre-clé-secrète
set DATABASE_URL=postgresql://...
```

## 🆘 Dépannage

### Erreur de migration
```bash
python manage.py migrate --fake
python manage.py migrate
```

### Réinitialiser les migrations
```bash
# ATTENTION: Perte de données!
del db.sqlite3
rmdir /s /q monitoring\migrations
python manage.py makemigrations monitoring
python manage.py migrate
```

### Problème de port occupé
```bash
# Utiliser un autre port
python manage.py runserver 8001
```

### Erreur d'importation
```bash
# Vérifier le chemin du fichier Excel
python -c "import os; print(os.path.exists('C:/Users/HP/Downloads/prosmat_se/Indicateurs_ProSMAT_Complet.xlsx'))"
```

## 📚 Documentation

### Générer la documentation
```bash
python manage.py help
```

### Voir l'aide d'une commande
```bash
python manage.py help migrate
```

## 🔐 Sécurité

### Changer le SECRET_KEY
Dans `config/settings.py`:
```python
SECRET_KEY = 'nouvelle-clé-très-secrète'
```

### Désactiver DEBUG en production
```python
DEBUG = False
ALLOWED_HOSTS = ['votre-domaine.com']
```

## 📊 Raccourcis Utiles

### Tout en un: Vérifier et démarrer
```bash
python verifier_donnees.py && python manage.py runserver
```

### Sauvegarder et importer
```bash
python manage.py dumpdata > backup.json && python import_prosmat_complet.py
```

### Nettoyer et redémarrer
```bash
del db.sqlite3 && python manage.py migrate && python import_prosmat_complet.py && python manage.py runserver
```

---

## 💡 Astuces

### Utiliser le menu interactif
Le plus simple: `OPERATIONS_PROSMAT.bat`

### Créer un alias (PowerShell)
```powershell
function prosmat { python manage.py runserver }
function verif { python verifier_donnees.py }
```

### Historique des commandes
Utilisez les flèches ↑↓ dans le terminal

### Copier-coller dans CMD
Clic droit pour coller

---

**Pour plus d'informations:**
- `GUIDE_UTILISATION_DONNEES.md` - Guide complet
- `DEMARRAGE_RAPIDE.md` - Démarrage de l'application
- Documentation Django: https://docs.djangoproject.com/
