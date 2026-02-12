"""
Script pour importer les indicateurs depuis Excel vers Neon PostgreSQL
"""
import os
import django
import pandas as pd
from pathlib import Path

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Composante, SousComposante, Indicateur
from django.db import transaction

def nettoyer_texte(texte):
    """Nettoyer et normaliser le texte"""
    if pd.isna(texte):
        return ""
    return str(texte).strip()

def importer_indicateurs(fichier_excel):
    """Importer les indicateurs depuis le fichier Excel"""
    print("=" * 70)
    print("IMPORTATION DES INDICATEURS DEPUIS EXCEL")
    print("=" * 70)
    
    # Vérifier que le fichier existe
    if not Path(fichier_excel).exists():
        print(f"\n❌ Erreur: Fichier non trouvé: {fichier_excel}")
        print("\nAssurez-vous que le fichier existe et que le chemin est correct.")
        return
    
    try:
        # Lire le fichier Excel
        print(f"\n📂 Lecture du fichier: {fichier_excel}")
        
        # Essayer de lire avec différentes options pour gérer les en-têtes
        try:
            # Essayer de lire normalement
            df = pd.read_excel(fichier_excel)
            
            # Si la première ligne contient "VUE D'ENSEMBLE", sauter les en-têtes
            if df.columns[0].startswith("PROJET") or "VUE D'ENSEMBLE" in str(df.columns[0]):
                print("⚠️  Détection d'en-têtes multiples, ajustement...")
                # Relire en sautant les premières lignes
                df = pd.read_excel(fichier_excel, skiprows=2)
                
        except Exception as e:
            print(f"⚠️  Tentative de lecture avec skiprows...")
            df = pd.read_excel(fichier_excel, skiprows=2)
        
        print(f"✅ {len(df)} lignes trouvées dans le fichier")
        
        # Afficher les colonnes disponibles
        print(f"\n📋 Colonnes disponibles: {list(df.columns)}")
        
        # Statistiques avant import
        print("\n📊 État actuel de la base:")
        print(f"   - Composantes: {Composante.objects.count()}")
        print(f"   - Sous-composantes: {SousComposante.objects.count()}")
        print(f"   - Indicateurs: {Indicateur.objects.count()}")
        
        # Compteurs
        crees = 0
        mis_a_jour = 0
        erreurs = 0
        
        print("\n🔄 Importation en cours...")
        print("-" * 70)
        
        # Importer avec transaction
        with transaction.atomic():
            for index, row in df.iterrows():
                try:
                    # Extraire les données (adapter selon les colonnes de ton Excel)
                    code = nettoyer_texte(row.get('Code', row.get('code', '')))
                    libelle = nettoyer_texte(row.get('Libellé', row.get('libelle', row.get('Libelle', ''))))
                    
                    if not code or not libelle:
                        print(f"⚠️  Ligne {index + 2}: Code ou libellé manquant - ignoré")
                        continue
                    
                    # Extraire les autres champs
                    composante_nom = nettoyer_texte(row.get('Composante', ''))
                    sous_composante_nom = nettoyer_texte(row.get('Sous-composante', row.get('Sous_composante', '')))
                    type_indicateur = nettoyer_texte(row.get('Type', 'QUANTITATIF'))
                    niveau = nettoyer_texte(row.get('Niveau', 'EXTRANT'))
                    unite_mesure = nettoyer_texte(row.get('Unité', row.get('Unite', 'Unité')))
                    cible_finale = row.get('Cible', row.get('cible', 0))
                    
                    # Convertir la cible en nombre
                    try:
                        cible_finale = float(cible_finale) if not pd.isna(cible_finale) else 0
                    except:
                        cible_finale = 0
                    
                    # Trouver ou créer la composante
                    composante = None
                    if composante_nom:
                        composante, _ = Composante.objects.get_or_create(
                            nom__icontains=composante_nom[:20],  # Recherche partielle
                            defaults={'nom': composante_nom, 'ordre': 1}
                        )
                    
                    # Trouver ou créer la sous-composante
                    sous_composante = None
                    if sous_composante_nom and composante:
                        sous_composante, _ = SousComposante.objects.get_or_create(
                            nom__icontains=sous_composante_nom[:20],
                            composante=composante,
                            defaults={'nom': sous_composante_nom, 'ordre': 1}
                        )
                    
                    # Normaliser le type d'indicateur
                    type_map = {
                        'QUANTITATIF': 'QUANTITATIF',
                        'QUALITATIF': 'QUALITATIF',
                        'QUANTITATIVE': 'QUANTITATIF',
                        'QUALITATIVE': 'QUALITATIF',
                    }
                    type_indicateur = type_map.get(type_indicateur.upper(), 'QUANTITATIF')
                    
                    # Normaliser le niveau
                    niveau_map = {
                        'IMPACT': 'IMPACT',
                        'EFFET': 'EFFET',
                        'EXTRANT': 'EXTRANT',
                        'INTRANT': 'INTRANT',
                        'PROCESSUS': 'PROCESSUS',
                    }
                    niveau = niveau_map.get(niveau.upper(), 'EXTRANT')
                    
                    # Créer ou mettre à jour l'indicateur
                    indicateur, created = Indicateur.objects.update_or_create(
                        code=code,
                        defaults={
                            'libelle': libelle,
                            'sous_composante': sous_composante,
                            'type_indicateur': type_indicateur,
                            'niveau': niveau,
                            'unite_mesure': unite_mesure,
                            'cible_finale': cible_finale,
                            'actif': True,
                        }
                    )
                    
                    if created:
                        crees += 1
                        status = "✅ Créé"
                    else:
                        mis_a_jour += 1
                        status = "🔄 Mis à jour"
                    
                    print(f"{status}: {code} - {libelle[:50]}")
                    
                except Exception as e:
                    erreurs += 1
                    print(f"❌ Erreur ligne {index + 2}: {e}")
        
        # Résumé
        print("\n" + "=" * 70)
        print("✅ IMPORTATION TERMINÉE")
        print("=" * 70)
        print(f"\n📊 Résultats:")
        print(f"   ✅ Créés: {crees}")
        print(f"   🔄 Mis à jour: {mis_a_jour}")
        print(f"   ❌ Erreurs: {erreurs}")
        print(f"   📈 Total traité: {crees + mis_a_jour}")
        
        # Statistiques après import
        print(f"\n📊 État final de la base:")
        print(f"   - Composantes: {Composante.objects.count()}")
        print(f"   - Sous-composantes: {SousComposante.objects.count()}")
        print(f"   - Indicateurs: {Indicateur.objects.count()}")
        
        print("\n🎉 Les indicateurs sont maintenant sur Neon!")
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la lecture du fichier: {e}")
        print("\nVérifiez que:")
        print("1. Le fichier est bien un fichier Excel (.xlsx)")
        print("2. Le fichier n'est pas ouvert dans Excel")
        print("3. Les colonnes attendues existent dans le fichier")

def afficher_aide():
    """Afficher l'aide"""
    print("\n" + "=" * 70)
    print("AIDE - IMPORTATION INDICATEURS")
    print("=" * 70)
    print("\nColonnes attendues dans le fichier Excel:")
    print("   - Code (obligatoire): Code de l'indicateur (ex: IND-1.1.1)")
    print("   - Libellé (obligatoire): Description de l'indicateur")
    print("   - Composante (optionnel): Nom de la composante")
    print("   - Sous-composante (optionnel): Nom de la sous-composante")
    print("   - Type (optionnel): QUANTITATIF ou QUALITATIF")
    print("   - Niveau (optionnel): IMPACT, EFFET, EXTRANT, etc.")
    print("   - Unité (optionnel): Unité de mesure")
    print("   - Cible (optionnel): Valeur cible")
    print("\nUtilisation:")
    print("   python importer_indicateurs_excel.py")
    print("\nLe script vous demandera le chemin du fichier Excel.")

if __name__ == '__main__':
    import sys
    
    print("\n🚀 IMPORTATION DES INDICATEURS PROSMAT")
    
    # Chemin par défaut
    fichier_par_defaut = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            afficher_aide()
            sys.exit(0)
        fichier_excel = sys.argv[1]
    else:
        print(f"\nFichier par défaut: {fichier_par_defaut}")
        reponse = input("\nUtiliser ce fichier? (O/n): ").strip().lower()
        
        if reponse in ['n', 'non', 'no']:
            fichier_excel = input("\nEntrez le chemin complet du fichier Excel: ").strip()
        else:
            fichier_excel = fichier_par_defaut
    
    # Importer
    importer_indicateurs(fichier_excel)
    
    print("\n" + "=" * 70)
    print("Pour vérifier les données sur Neon:")
    print("   python verifier_neon.py")
    print("=" * 70)
