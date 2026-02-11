"""
Script de vérification des données importées
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Composante, SousComposante, Indicateur, Periode
from accounts.models import User

print("\n" + "="*80)
print("VERIFICATION DES DONNEES PROSMAT")
print("="*80)

# Vérifier les périodes
print(f"\nPERIODES: {Periode.objects.count()}")
for p in Periode.objects.all().order_by('annee', 'trimestre')[:5]:
    print(f"   - {p}")

# Vérifier les composantes
print(f"\nCOMPOSANTES: {Composante.objects.count()}")
for comp in Composante.objects.all().order_by('ordre'):
    nb_sc = comp.sous_composantes.count()
    nb_ind = Indicateur.objects.filter(sous_composante__composante=comp).count()
    print(f"\n   {comp.nom}")
    print(f"      Sous-composantes: {nb_sc}")
    print(f"      Indicateurs: {nb_ind}")
    
    # Afficher quelques indicateurs
    if nb_ind > 0:
        print(f"      Exemples d'indicateurs:")
        for ind in Indicateur.objects.filter(sous_composante__composante=comp)[:3]:
            print(f"         • {ind.code}: {ind.libelle[:60]}...")
            if ind.valeur_reference is not None:
                print(f"           Référence: {ind.valeur_reference} | Cible: {ind.cible_finale} {ind.unite_mesure}")

# Statistiques globales
print(f"\n" + "="*80)
print("STATISTIQUES GLOBALES")
print("="*80)
print(f"Total Indicateurs: {Indicateur.objects.count()}")
print(f"Indicateurs Actifs: {Indicateur.objects.filter(actif=True).count()}")
print(f"Indicateurs avec Cible: {Indicateur.objects.exclude(cible_finale__isnull=True).count()}")
print(f"Indicateurs GAFSP: {Indicateur.objects.filter(code__startswith='GAFSP').count()}")
print(f"Indicateurs Genre: {Indicateur.objects.filter(code__startswith='IND-GENRE').count()}")

# Vérifier les utilisateurs
print(f"\nUTILISATEURS: {User.objects.count()}")
print(f"   Administrateurs: {User.objects.filter(role='ADMIN').count()}")
print(f"   Coordonnateurs: {User.objects.filter(role='COORDONNATEUR').count()}")
print(f"   Saisie: {User.objects.filter(role='SAISIE').count()}")

# Indicateurs par type
print(f"\nINDICATEURS PAR TYPE:")
from django.db.models import Count
types = Indicateur.objects.values('type_indicateur').annotate(count=Count('id'))
for t in types:
    print(f"   {t['type_indicateur']}: {t['count']}")

# Indicateurs par niveau
print(f"\nINDICATEURS PAR NIVEAU:")
niveaux = Indicateur.objects.values('niveau').annotate(count=Count('id'))
for n in niveaux:
    print(f"   {n['niveau']}: {n['count']}")

print("\n" + "="*80)
print("VERIFICATION TERMINEE")
print("="*80)
print("\nPour acceder a l'application:")
print("   1. Démarrer le serveur: python manage.py runserver")
print("   2. Ouvrir: http://localhost:8000")
print("   3. Se connecter avec un compte admin")
print("\n")
