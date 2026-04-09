"""
Script pour analyser la structure du fichier Excel
"""
import pandas as pd
from pathlib import Path

fichier = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"

print("=" * 70)
print("ANALYSE DU FICHIER EXCEL")
print("=" * 70)

if not Path(fichier).exists():
    print(f"\n❌ Fichier non trouvé: {fichier}")
    exit(1)

print(f"\n📂 Fichier: {fichier}")

# Lire le fichier Excel
xl_file = pd.ExcelFile(fichier)

print(f"\n📋 Feuilles disponibles: {xl_file.sheet_names}")

# Analyser chaque feuille
for sheet_name in xl_file.sheet_names:
    print(f"\n{'=' * 70}")
    print(f"FEUILLE: {sheet_name}")
    print('=' * 70)
    
    # Lire la feuille
    df = pd.read_excel(fichier, sheet_name=sheet_name)
    
    print(f"\n📊 Dimensions: {df.shape[0]} lignes x {df.shape[1]} colonnes")
    print(f"\n📋 Colonnes: {list(df.columns)}")
    
    print(f"\n👀 Aperçu des 5 premières lignes:")
    print(df.head())
    
    # Essayer avec skiprows
    print(f"\n\n🔄 Essai avec skiprows=2:")
    df2 = pd.read_excel(fichier, sheet_name=sheet_name, skiprows=2)
    print(f"📊 Dimensions: {df2.shape[0]} lignes x {df2.shape[1]} colonnes")
    print(f"📋 Colonnes: {list(df2.columns)}")
    print(f"\n👀 Aperçu des 5 premières lignes:")
    print(df2.head())
    
    # Essayer avec skiprows=3
    print(f"\n\n🔄 Essai avec skiprows=3:")
    df3 = pd.read_excel(fichier, sheet_name=sheet_name, skiprows=3)
    print(f"📊 Dimensions: {df3.shape[0]} lignes x {df3.shape[1]} colonnes")
    print(f"📋 Colonnes: {list(df3.columns)}")
    print(f"\n👀 Aperçu des 5 premières lignes:")
    print(df3.head())

print("\n" + "=" * 70)
print("✅ ANALYSE TERMINÉE")
print("=" * 70)
