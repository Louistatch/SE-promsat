"""
Script pour migrer les données locales vers Neon PostgreSQL
"""
import os
import sys

# Forcer l'utilisation de Neon
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require'

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Override database config pour utiliser Neon
from django.conf import settings
import dj_database_url
settings.DATABASES['default'] = dj_database_url.config(
    default=os.environ['DATABASE_URL'],
    conn_max_age=600
)

from monitoring.models import Composante, SousComposante, Indicateur, Periode
from accounts.models import User
from django.db import connection

def verifier_connexion():
    """Vérifier qu'on est bien connecté à Neon"""
    print("=" * 70)
    print("VÉRIFICATION CONNEXION NEON")
    print("=" * 70)
    
    with connection.cursor() as cursor:
        cursor.execute("SELECT current_database(), version();")
        db_name, version = cursor.fetchone()
        print(f"\n✅ Connecté à: {db_name}")
        print(f"📊 PostgreSQL: {version[:50]}...")
        
        if 'neon' not in version.lower() and 'postgres' not in version.lower():
            print("\n⚠️  ATTENTION: Vous n'êtes peut-être pas sur Neon!")
            reponse = input("Continuer quand même? (o/N): ")
            if reponse.lower() != 'o':
                sys.exit(1)
    
    return True

def compter_donnees():
    """Compter les données actuelles"""
    print("\n" + "=" * 70)
    print("ÉTAT ACTUEL DE NEON")
    print("=" * 70)
    
    print(f"\n📊 Données actuelles:")
    print(f"   - Composantes: {Composante.objects.count()}")
    print(f"   - Sous-composantes: {SousComposante.objects.count()}")
    print(f"   - Indicateurs: {Indicateur.objects.count()}")
    print(f"   - Périodes: {Periode.objects.count()}")
    print(f"   - Utilisateurs: {User.objects.count()}")

def importer_depuis_excel():
    """Importer les indicateurs depuis Excel vers Neon"""
    print("\n" + "=" * 70)
    print("IMPORTATION DEPUIS EXCEL VERS NEON")
    print("=" * 70)
    
    fichier = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"
    
    print(f"\n📂 Fichier: {fichier}")
    print("\n⚠️  Cette opération va importer les indicateurs directement dans Neon")
    reponse = input("Continuer? (O/n): ")
    
    if reponse.lower() in ['n', 'non']:
        print("❌ Importation annulée")
        return
    
    # Importer
    import pandas as pd
    from django.db import transaction
    
    def nettoyer_texte(texte):
        if pd.isna(texte) or texte == 'NaN':
            return ""
        return str(texte).strip()
    
    def importer_feuille(nom_feuille, composante_nom):
        print(f"\n📋 Feuille: {nom_feuille}")
        
        df = pd.read_excel(fichier, sheet_name=nom_feuille, skiprows=3)
        df = df.dropna(how='all')
        
        # Trouver ou créer la composante
        composante, _ = Composante.objects.get_or_create(
            nom=composante_nom,
            defaults={'ordre': 1}
        )
        
        crees = 0
        mis_a_jour = 0
        
        for index, row in df.iterrows():
            try:
                indicateur_col = df.columns[0]
                libelle = nettoyer_texte(row[indicateur_col])
                
                if not libelle or len(libelle) < 5:
                    continue
                
                if libelle.isupper() or libelle.startswith(('1.', '2.', '3.', '4.')):
                    continue
                
                code_gafsp = ""
                cible_finale = 0
                unite = "Unité"
                
                if 'Code GAFSP' in df.columns:
                    code_gafsp = nettoyer_texte(row.get('Code GAFSP', ''))
                
                if 'Cible Finale' in df.columns:
                    try:
                        cible_finale = float(row.get('Cible Finale', 0))
                    except:
                        cible_finale = 0
                
                if 'Unité' in df.columns:
                    unite = nettoyer_texte(row.get('Unité', 'Unité'))
                    if not unite:
                        unite = "Unité"
                
                if not code_gafsp:
                    mots = libelle.split()[:3]
                    code_gafsp = f"IND-{'-'.join(mots)}"[:50]
                
                indicateur, created = Indicateur.objects.update_or_create(
                    code=code_gafsp,
                    defaults={
                        'libelle': libelle,
                        'sous_composante': None,
                        'type_indicateur': 'QUANTITATIF',
                        'niveau': 'EXTRANT',
                        'unite_mesure': unite,
                        'cible_finale': cible_finale,
                        'actif': True,
                    }
                )
                
                if created:
                    crees += 1
                else:
                    mis_a_jour += 1
                
            except Exception as e:
                pass
        
        print(f"   ✅ Créés: {crees} | 🔄 Mis à jour: {mis_a_jour}")
        return crees, mis_a_jour
    
    # Feuilles à importer
    feuilles = [
        ('Composante 1 - Production', 'Composante 1: Intensification de la production agroécologique'),
        ('Composante 2 - Valorisation', 'Composante 2: Valorisation des produits agroécologiques'),
        ('Composante 3 - Capacités', 'Composante 3: Renforcement des capacités et dialogue politique'),
        ('Indicateurs Genre & Inclusion', 'Transversal: Genre, Jeunesse et Inclusion'),
        ('Résilience Climatique', 'Transversal: Résilience Climatique et Durabilité'),
    ]
    
    total_crees = 0
    total_mis_a_jour = 0
    
    with transaction.atomic():
        for nom_feuille, composante_nom in feuilles:
            crees, mis_a_jour = importer_feuille(nom_feuille, composante_nom)
            total_crees += crees
            total_mis_a_jour += mis_a_jour
    
    print("\n" + "=" * 70)
    print("✅ IMPORTATION TERMINÉE")
    print("=" * 70)
    print(f"\n📊 Résultats:")
    print(f"   ✅ Total créés: {total_crees}")
    print(f"   🔄 Total mis à jour: {total_mis_a_jour}")

if __name__ == '__main__':
    print("\n🚀 MIGRATION VERS NEON\n")
    
    # 1. Vérifier la connexion
    verifier_connexion()
    
    # 2. Afficher l'état actuel
    compter_donnees()
    
    # 3. Importer depuis Excel
    importer_depuis_excel()
    
    # 4. Afficher l'état final
    print("\n" + "=" * 70)
    print("ÉTAT FINAL DE NEON")
    print("=" * 70)
    compter_donnees()
    
    print("\n✅ Migration terminée!")
    print("\nVérifiez dans Neon Console:")
    print("   SELECT COUNT(*) FROM monitoring_indicateur;")
