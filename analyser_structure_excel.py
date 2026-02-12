"""
Analyser la structure complète du fichier Excel pour créer les modèles Django
"""
import pandas as pd
from pathlib import Path

fichier = r"C:\Users\HP\Downloads\prosmat_se\Indicateurs_ProSMAT_Complet.xlsx"

print("=" * 80)
print("ANALYSE COMPLÈTE DU FICHIER EXCEL PROSMAT")
print("=" * 80)

if not Path(fichier).exists():
    print(f"\n❌ Fichier non trouvé: {fichier}")
    exit(1)

# Lire le fichier Excel
xl_file = pd.ExcelFile(fichier)

print(f"\n📂 Fichier: {fichier}")
print(f"\n📋 {len(xl_file.sheet_names)} feuilles trouvées:")

for i, sheet_name in enumerate(xl_file.sheet_names, 1):
    print(f"   {i}. {sheet_name}")

# Analyser chaque feuille en détail
for sheet_name in xl_file.sheet_names:
    print(f"\n{'=' * 80}")
    print(f"FEUILLE: {sheet_name}")
    print('=' * 80)
    
    # Lire avec skiprows=3 pour avoir les vraies colonnes
    df = pd.read_excel(fichier, sheet_name=sheet_name, skiprows=3)
    
    print(f"\n📊 Dimensions: {df.shape[0]} lignes x {df.shape[1]} colonnes")
    print(f"\n📋 Colonnes:")
    for col in df.columns:
        non_null = df[col].notna().sum()
        print(f"   - {col:40} ({non_null} valeurs non-nulles)")
    
    print(f"\n👀 Aperçu des 3 premières lignes:")
    print(df.head(3).to_string())
    
    # Analyser les types de données
    print(f"\n📈 Types de données uniques:")
    for col in df.columns:
        unique_count = df[col].nunique()
        dtype = df[col].dtype
        print(f"   - {col:40} | Type: {dtype} | {unique_count} valeurs uniques")

print("\n" + "=" * 80)
print("RECOMMANDATIONS POUR LES MODÈLES DJANGO")
print("=" * 80)

print("""
Basé sur l'analyse, voici la structure recommandée:

1. COMPOSANTE
   - nom (CharField)
   - description (TextField)
   - ordre (IntegerField)

2. SOUS_COMPOSANTE
   - composante (ForeignKey → Composante)
   - nom (CharField)
   - description (TextField)
   - ordre (IntegerField)

3. INDICATEUR
   - code (CharField, unique) - Ex: GAFSP #1, IND-1.1.1
   - libelle (TextField)
   - sous_composante (ForeignKey → SousComposante, nullable)
   - type_indicateur (CharField) - QUANTITATIF/QUALITATIF
   - niveau (CharField) - IMPACT/EFFET/EXTRANT
   - unite_mesure (CharField)
   - valeur_base (DecimalField)
   - cible_finale (DecimalField)
   - details (TextField)
   - actif (BooleanField)

4. PERIODE
   - annee (IntegerField)
   - trimestre (CharField) - T1, T2, T3, T4
   - date_debut (DateField)
   - date_fin (DateField)
   - cloture (BooleanField)

5. REALISATION
   - indicateur (ForeignKey → Indicateur)
   - periode (ForeignKey → Periode)
   - region (CharField)
   - valeur_realisee (DecimalField)
   - commentaire (TextField)
   - date_saisie (DateTimeField)
   - saisi_par (ForeignKey → User)

6. CIBLE_INTERMEDIAIRE
   - indicateur (ForeignKey → Indicateur)
   - periode (ForeignKey → Periode)
   - valeur_cible (DecimalField)

7. RAPPORT
   - titre (CharField)
   - periode (ForeignKey → Periode)
   - type_rapport (CharField) - TRIMESTRIEL/ANNUEL/SPECIAL
   - contenu (TextField)
   - fichier (FileField)
   - date_creation (DateTimeField)
   - cree_par (ForeignKey → User)
""")

print("\n✅ Analyse terminée!")
