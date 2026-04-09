"""
Import complet du fichier Excel ProSMAT vers Neon PostgreSQL
Toutes les valeurs null sont traitées comme 0
"""
import os
import sys

# Forcer l'utilisation de Neon
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require'

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
import dj_database_url
settings.DATABASES['default'] = dj_database_url.config(
    default=os.environ['DATABASE_URL'],
    conn_max_age=600
)

import pandas as pd
from monitoring.models import Composante, SousComposante, Indicateur
from django.db import transaction
from decimal import Decimal

fichier = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"

def nettoyer_valeur(valeur):
    """Convertir les valeurs null en 0, sinon retourner la valeur"""
    if pd.isna(valeur) or valeur == 'NaN' or valeur == '':
        return 0
    try:
        # Nettoyer les espaces et virgules
        if isinstance(valeur, str):
            valeur = valeur.replace(' ', '').replace(',', '')
        return Decimal(str(valeur))
    except:
        return 0

def nettoyer_texte(texte):
    """Nettoyer le texte"""
    if pd.isna(texte) or texte == 'NaN':
        return ""
    return str(texte).strip()

print("=" * 80)
print("IMPORT COMPLET EXCEL → NEON POSTGRESQL")
print("=" * 80)

print(f"\n📂 Fichier: {fichier}")
print(f"🗄️  Base: Neon PostgreSQL")
print(f"⚠️  Règle: Valeurs null = 0")

reponse = input("\nContinuer? (O/n): ")
if reponse.lower() in ['n', 'non']:
    print("❌ Annulé")
    sys.exit(0)

# Mapping des feuilles vers composantes
feuilles_composantes = {
    'Composante 1 - Production': {
        'nom': 'Composante 1: Intensification de la production agroécologique',
        'description': 'Amélioration de la productivité agricole par des pratiques agroécologiques',
        'ordre': 1
    },
    'Composante 2 - Valorisation': {
        'nom': 'Composante 2: Valorisation des produits agroécologiques',
        'description': 'Développement des chaînes de valeur et accès aux marchés',
        'ordre': 2
    },
    'Composante 3 - Capacités': {
        'nom': 'Composante 3: Renforcement des capacités et dialogue politique',
        'description': 'Structuration des organisations et plaidoyer',
        'ordre': 3
    },
    'Indicateurs Genre & Inclusion': {
        'nom': 'Transversal: Genre, Jeunesse et Inclusion',
        'description': 'Indicateurs transversaux de genre et inclusion sociale',
        'ordre': 4
    },
    'Résilience Climatique': {
        'nom': 'Transversal: Résilience Climatique et Durabilité',
        'description': 'Pratiques agricoles résilientes et adaptation climatique',
        'ordre': 5
    }
}

total_crees = 0
total_mis_a_jour = 0

with transaction.atomic():
    for nom_feuille, comp_data in feuilles_composantes.items():
        print(f"\n{'=' * 80}")
        print(f"📋 FEUILLE: {nom_feuille}")
        print('=' * 80)
        
        try:
            # Lire la feuille
            df = pd.read_excel(fichier, sheet_name=nom_feuille, skiprows=3)
            df = df.dropna(how='all')
            
            print(f"📊 {len(df)} lignes trouvées")
            
            # Créer ou mettre à jour la composante
            composante, created = Composante.objects.update_or_create(
                nom=comp_data['nom'],
                defaults={
                    'description': comp_data['description'],
                    'ordre': comp_data['ordre']
                }
            )
            status = "✅ Créée" if created else "🔄 Mise à jour"
            print(f"{status}: {composante.nom}")
            
            # Importer les indicateurs
            crees = 0
            mis_a_jour = 0
            
            for index, row in df.iterrows():
                try:
                    # Colonne indicateur (première colonne)
                    indicateur_col = df.columns[0]
                    libelle = nettoyer_texte(row[indicateur_col])
                    
                    # Ignorer les lignes vides ou titres
                    if not libelle or len(libelle) < 5:
                        continue
                    if libelle.isupper() or libelle.startswith(('1.', '2.', '3.', '4.')):
                        continue
                    
                    # Extraire les données
                    code = ""
                    valeur_base = 0
                    cible_finale = 0
                    unite = "Unité"
                    details = ""
                    
                    # Code GAFSP ou générer un code
                    if 'Code GAFSP' in df.columns:
                        code = nettoyer_texte(row.get('Code GAFSP', ''))
                    
                    if not code:
                        # Générer un code unique
                        mots = libelle.split()[:3]
                        code = f"IND-{'-'.join(mots)}"[:50]
                    
                    # Valeur de base (null = 0)
                    if 'Valeur de Base' in df.columns:
                        valeur_base = nettoyer_valeur(row.get('Valeur de Base'))
                    
                    # Cible finale (null = 0)
                    if 'Cible Finale' in df.columns:
                        cible_finale = nettoyer_valeur(row.get('Cible Finale'))
                    
                    # Unité
                    if 'Unité' in df.columns:
                        unite = nettoyer_texte(row.get('Unité', 'Unité'))
                        if not unite:
                            unite = "Unité"
                    
                    # Détails
                    if 'Détails' in df.columns:
                        details = nettoyer_texte(row.get('Détails', ''))
                    
                    # Créer ou mettre à jour l'indicateur
                    indicateur, created = Indicateur.objects.update_or_create(
                        code=code,
                        defaults={
                            'libelle': libelle,
                            'sous_composante': None,
                            'type_indicateur': 'QUANTITATIF',
                            'niveau': 'EXTRANT',
                            'unite_mesure': unite,
                            'valeur_reference': valeur_base,
                            'cible_finale': cible_finale,
                            'source_verification': details,
                            'actif': True,
                        }
                    )
                    
                    if created:
                        crees += 1
                        print(f"  ✅ {code[:30]:30} | Base: {valeur_base:>8} | Cible: {cible_finale:>8}")
                    else:
                        mis_a_jour += 1
                        print(f"  🔄 {code[:30]:30} | Base: {valeur_base:>8} | Cible: {cible_finale:>8}")
                
                except Exception as e:
                    print(f"  ⚠️  Ligne {index}: {e}")
            
            print(f"\n📊 Résultats {nom_feuille}:")
            print(f"   ✅ Créés: {crees}")
            print(f"   🔄 Mis à jour: {mis_a_jour}")
            
            total_crees += crees
            total_mis_a_jour += mis_a_jour
            
        except Exception as e:
            print(f"❌ Erreur: {e}")

print("\n" + "=" * 80)
print("✅ IMPORT TERMINÉ")
print("=" * 80)
print(f"\n📊 Résultats globaux:")
print(f"   ✅ Total créés: {total_crees}")
print(f"   🔄 Total mis à jour: {total_mis_a_jour}")
print(f"   📈 Total traité: {total_crees + total_mis_a_jour}")

# Statistiques finales
from monitoring.models import Composante, Indicateur
print(f"\n📊 État final de Neon:")
print(f"   - Composantes: {Composante.objects.count()}")
print(f"   - Indicateurs: {Indicateur.objects.count()}")

print("\n✅ Toutes les données sont maintenant sur Neon!")
print("\nVérifiez dans Neon Console:")
print("   SELECT code, libelle, valeur_reference, cible_finale")
print("   FROM monitoring_indicateur")
print("   WHERE valeur_reference = 0 OR cible_finale = 0;")
