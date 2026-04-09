"""
Script pour importer TOUS les indicateurs depuis Excel vers Neon PostgreSQL
Adapté pour le fichier Indicateurs_ProSMAT_Complet.xlsx
"""
import os
import django
import pandas as pd
from pathlib import Path

# Configuration Django - Utiliser Neon
import sys
if '--neon' in sys.argv:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    # Forcer l'utilisation de DATABASE_URL depuis .env
    import dj_database_url
    from django.conf import settings
    django.setup()
    # Override database config
    settings.DATABASES['default'] = dj_database_url.config(conn_max_age=600)
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    django.setup()

from monitoring.models import Composante, SousComposante, Indicateur
from django.db import transaction

def nettoyer_texte(texte):
    """Nettoyer et normaliser le texte"""
    if pd.isna(texte) or texte == 'NaN':
        return ""
    return str(texte).strip()

def importer_feuille(fichier_excel, nom_feuille, composante_nom):
    """Importer les indicateurs d'une feuille spécifique"""
    print(f"\n{'='*70}")
    print(f"📋 FEUILLE: {nom_feuille}")
    print('='*70)
    
    try:
        # Lire la feuille en sautant les 3 premières lignes (en-têtes)
        df = pd.read_excel(fichier_excel, sheet_name=nom_feuille, skiprows=3)
        
        # Filtrer les lignes vides
        df = df.dropna(how='all')
        
        print(f"📊 {len(df)} lignes trouvées")
        print(f"📋 Colonnes: {list(df.columns)}")
        
        # Trouver ou créer la composante
        composante, created = Composante.objects.get_or_create(
            nom=composante_nom,
            defaults={'ordre': 1}
        )
        if created:
            print(f"✅ Composante créée: {composante_nom}")
        
        crees = 0
        mis_a_jour = 0
        ignores = 0
        
        # Parcourir les lignes
        for index, row in df.iterrows():
            try:
                # Extraire l'indicateur (première colonne)
                indicateur_col = df.columns[0]
                libelle = nettoyer_texte(row[indicateur_col])
                
                # Ignorer les lignes vides ou les titres de section
                if not libelle or len(libelle) < 5:
                    continue
                
                # Ignorer les lignes qui sont des titres de section (en majuscules ou avec des numéros)
                if libelle.isupper() or libelle.startswith(('1.', '2.', '3.', '4.')):
                    continue
                
                # Extraire les autres colonnes si elles existent
                code_gafsp = ""
                valeur_base = 0
                cible_finale = 0
                unite = "Unité"
                details = ""
                
                if 'Code GAFSP' in df.columns:
                    code_gafsp = nettoyer_texte(row.get('Code GAFSP', ''))
                
                if 'Valeur de Base' in df.columns:
                    try:
                        valeur_base = float(row.get('Valeur de Base', 0))
                    except:
                        valeur_base = 0
                
                if 'Cible Finale' in df.columns:
                    try:
                        cible_finale = float(row.get('Cible Finale', 0))
                    except:
                        cible_finale = 0
                
                if 'Unité' in df.columns:
                    unite = nettoyer_texte(row.get('Unité', 'Unité'))
                    if not unite:
                        unite = "Unité"
                
                if 'Détails' in df.columns:
                    details = nettoyer_texte(row.get('Détails', ''))
                
                # Générer un code unique si pas de code GAFSP
                if not code_gafsp:
                    # Utiliser les 3 premiers mots du libellé
                    mots = libelle.split()[:3]
                    code_gafsp = f"IND-{'-'.join(mots)}"[:50]
                
                # Créer ou mettre à jour l'indicateur
                indicateur, created = Indicateur.objects.update_or_create(
                    code=code_gafsp,
                    defaults={
                        'libelle': libelle,
                        'sous_composante': None,  # Pas de sous-composante pour l'instant
                        'type_indicateur': 'QUANTITATIF',
                        'niveau': 'EXTRANT',
                        'unite_mesure': unite,
                        'cible_finale': cible_finale,
                        'actif': True,
                    }
                )
                
                if created:
                    crees += 1
                    print(f"  ✅ Créé: {code_gafsp[:30]} - {libelle[:50]}")
                else:
                    mis_a_jour += 1
                    print(f"  🔄 Mis à jour: {code_gafsp[:30]} - {libelle[:50]}")
                
            except Exception as e:
                ignores += 1
                print(f"  ⚠️  Ligne {index}: {e}")
        
        print(f"\n📊 Résultats pour {nom_feuille}:")
        print(f"   ✅ Créés: {crees}")
        print(f"   🔄 Mis à jour: {mis_a_jour}")
        print(f"   ⚠️  Ignorés: {ignores}")
        
        return crees, mis_a_jour, ignores
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import de {nom_feuille}: {e}")
        return 0, 0, 0

def importer_tous_indicateurs(fichier_excel):
    """Importer tous les indicateurs de toutes les feuilles"""
    print("=" * 70)
    print("IMPORTATION DE TOUS LES INDICATEURS PROSMAT")
    print("=" * 70)
    
    # Vérifier que le fichier existe
    if not Path(fichier_excel).exists():
        print(f"\n❌ Erreur: Fichier non trouvé: {fichier_excel}")
        return
    
    print(f"\n📂 Fichier: {fichier_excel}")
    
    # Statistiques avant import
    print(f"\n📊 État actuel de la base:")
    print(f"   - Composantes: {Composante.objects.count()}")
    print(f"   - Indicateurs: {Indicateur.objects.count()}")
    
    # Définir les feuilles à importer et leurs composantes
    feuilles = [
        ('Composante 1 - Production', 'Composante 1: Intensification de la production agroécologique'),
        ('Composante 2 - Valorisation', 'Composante 2: Valorisation des produits agroécologiques'),
        ('Composante 3 - Capacités', 'Composante 3: Renforcement des capacités et dialogue politique'),
        ('Indicateurs Genre & Inclusion', 'Transversal: Genre, Jeunesse et Inclusion'),
        ('Résilience Climatique', 'Transversal: Résilience Climatique et Durabilité'),
    ]
    
    total_crees = 0
    total_mis_a_jour = 0
    total_ignores = 0
    
    # Importer chaque feuille
    with transaction.atomic():
        for nom_feuille, composante_nom in feuilles:
            crees, mis_a_jour, ignores = importer_feuille(fichier_excel, nom_feuille, composante_nom)
            total_crees += crees
            total_mis_a_jour += mis_a_jour
            total_ignores += ignores
    
    # Résumé final
    print("\n" + "=" * 70)
    print("✅ IMPORTATION TERMINÉE")
    print("=" * 70)
    print(f"\n📊 Résultats globaux:")
    print(f"   ✅ Total créés: {total_crees}")
    print(f"   🔄 Total mis à jour: {total_mis_a_jour}")
    print(f"   ⚠️  Total ignorés: {total_ignores}")
    print(f"   📈 Total traité: {total_crees + total_mis_a_jour}")
    
    # Statistiques après import
    print(f"\n📊 État final de la base:")
    print(f"   - Composantes: {Composante.objects.count()}")
    print(f"   - Indicateurs: {Indicateur.objects.count()}")
    
    print("\n🎉 Les indicateurs sont maintenant sur Neon!")
    print("\nPour vérifier:")
    print("   python verifier_neon.py")

if __name__ == '__main__':
    fichier = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"
    
    print("\n🚀 IMPORTATION DES INDICATEURS PROSMAT\n")
    
    reponse = input(f"Importer depuis {fichier}? (O/n): ").strip().lower()
    
    if reponse in ['n', 'non', 'no']:
        fichier = input("\nEntrez le chemin complet du fichier Excel: ").strip()
    
    importer_tous_indicateurs(fichier)
