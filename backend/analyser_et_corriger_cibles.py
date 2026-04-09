"""
Analyser le fichier Excel pour trouver TOUTES les cibles et les mettre à jour sur Neon
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
from monitoring.models import Indicateur
from decimal import Decimal

fichier = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"

def extraire_nombre(valeur):
    """Extraire un nombre d'une chaîne, même avec du texte"""
    if pd.isna(valeur) or valeur == '' or valeur == 'NaN':
        return None
    
    # Si c'est déjà un nombre
    if isinstance(valeur, (int, float)):
        return Decimal(str(valeur))
    
    # Si c'est une chaîne
    valeur_str = str(valeur).strip()
    
    # Cas spéciaux
    if valeur_str.lower() in ['nan', 'n/a', '-', '']:
        return None
    
    # Essayer d'extraire le premier nombre
    import re
    # Chercher un nombre (avec ou sans décimales, avec ou sans espaces/virgules)
    match = re.search(r'(\d[\d\s,\.]*\d|\d)', valeur_str)
    if match:
        nombre_str = match.group(1).replace(' ', '').replace(',', '')
        try:
            return Decimal(nombre_str)
        except:
            return None
    
    return None

print("=" * 80)
print("ANALYSE DES CIBLES DANS LE FICHIER EXCEL")
print("=" * 80)

# Feuilles à analyser
feuilles = [
    'Composante 1 - Production',
    'Composante 2 - Valorisation',
    'Composante 3 - Capacités',
    'Indicateurs Genre & Inclusion',
    'Résilience Climatique'
]

cibles_trouvees = []

for nom_feuille in feuilles:
    print(f"\n{'=' * 80}")
    print(f"📋 FEUILLE: {nom_feuille}")
    print('=' * 80)
    
    try:
        # Lire la feuille
        df = pd.read_excel(fichier, sheet_name=nom_feuille, skiprows=3)
        df = df.dropna(how='all')
        
        print(f"\n📊 Colonnes: {list(df.columns)}")
        
        # Chercher la colonne "Cible Finale" ou équivalent
        col_cible = None
        for col in df.columns:
            if 'cible' in str(col).lower() or 'finale' in str(col).lower():
                col_cible = col
                break
        
        if not col_cible:
            print("⚠️  Pas de colonne 'Cible' trouvée")
            continue
        
        print(f"✅ Colonne cible trouvée: {col_cible}")
        
        # Analyser chaque ligne
        for index, row in df.iterrows():
            # Indicateur
            indicateur_col = df.columns[0]
            libelle = str(row[indicateur_col]).strip() if pd.notna(row[indicateur_col]) else ""
            
            if not libelle or len(libelle) < 5:
                continue
            if libelle.isupper() or libelle.startswith(('1.', '2.', '3.', '4.')):
                continue
            
            # Code
            code = ""
            if 'Code GAFSP' in df.columns:
                code = str(row.get('Code GAFSP', '')).strip() if pd.notna(row.get('Code GAFSP')) else ""
            
            if not code:
                mots = libelle.split()[:3]
                code = f"IND-{'-'.join(mots)}"[:50]
            
            # Cible
            cible_raw = row[col_cible]
            cible = extraire_nombre(cible_raw)
            
            if cible is not None and cible > 0:
                cibles_trouvees.append({
                    'feuille': nom_feuille,
                    'code': code,
                    'libelle': libelle[:60],
                    'cible_raw': str(cible_raw),
                    'cible': cible
                })
                print(f"  ✅ {code:30} | Cible: {cible:>10} | Raw: {str(cible_raw)[:30]}")
            else:
                print(f"  ⚠️  {code:30} | Cible: NULL/0    | Raw: {str(cible_raw)[:30]}")
    
    except Exception as e:
        print(f"❌ Erreur: {e}")

print("\n" + "=" * 80)
print("RÉSUMÉ DES CIBLES TROUVÉES")
print("=" * 80)
print(f"\n📊 Total cibles > 0 trouvées: {len(cibles_trouvees)}")

if cibles_trouvees:
    print("\n📋 Liste des cibles:")
    for item in cibles_trouvees[:20]:  # Afficher les 20 premières
        print(f"  {item['code']:30} | {item['cible']:>10}")
    
    if len(cibles_trouvees) > 20:
        print(f"  ... et {len(cibles_trouvees) - 20} autres")

# Comparer avec Neon
print("\n" + "=" * 80)
print("COMPARAISON AVEC NEON")
print("=" * 80)

indicateurs_neon = Indicateur.objects.all()
print(f"\n📊 Indicateurs dans Neon: {indicateurs_neon.count()}")
print(f"📊 Indicateurs avec cible > 0 dans Neon: {Indicateur.objects.filter(cible_finale__gt=0).count()}")
print(f"📊 Cibles trouvées dans Excel: {len(cibles_trouvees)}")

# Trouver les différences
codes_excel = {item['code'] for item in cibles_trouvees}
codes_neon_avec_cible = set(Indicateur.objects.filter(cible_finale__gt=0).values_list('code', flat=True))

manquants_neon = codes_excel - codes_neon_avec_cible
if manquants_neon:
    print(f"\n⚠️  {len(manquants_neon)} indicateurs ont une cible dans Excel mais pas dans Neon:")
    for code in list(manquants_neon)[:10]:
        cible_excel = next((item['cible'] for item in cibles_trouvees if item['code'] == code), None)
        print(f"  - {code:30} | Cible Excel: {cible_excel}")

# Proposer la mise à jour
print("\n" + "=" * 80)
print("MISE À JOUR")
print("=" * 80)

if manquants_neon:
    reponse = input(f"\nMettre à jour les {len(manquants_neon)} cibles manquantes sur Neon? (O/n): ")
    if reponse.lower() not in ['n', 'non']:
        from django.db import transaction
        
        mis_a_jour = 0
        with transaction.atomic():
            for item in cibles_trouvees:
                try:
                    indicateur = Indicateur.objects.get(code=item['code'])
                    if indicateur.cible_finale == 0 or indicateur.cible_finale is None:
                        indicateur.cible_finale = item['cible']
                        indicateur.save()
                        mis_a_jour += 1
                        print(f"  ✅ {item['code']:30} | Cible: {item['cible']}")
                except Indicateur.DoesNotExist:
                    print(f"  ⚠️  {item['code']:30} | Indicateur non trouvé dans Neon")
        
        print(f"\n✅ {mis_a_jour} cibles mises à jour sur Neon!")
        print(f"\n📊 État final:")
        print(f"   - Total indicateurs: {Indicateur.objects.count()}")
        print(f"   - Avec cible > 0: {Indicateur.objects.filter(cible_finale__gt=0).count()}")
    else:
        print("❌ Mise à jour annulée")
else:
    print("\n✅ Toutes les cibles de l'Excel sont déjà dans Neon!")

print("\n" + "=" * 80)
print("✅ ANALYSE TERMINÉE")
print("=" * 80)
