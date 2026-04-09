#!/usr/bin/env python3
"""Analyser les colonnes liées aux cultures et au marché"""

import pandas as pd

df = pd.read_excel('MISSION_DE_SUIVI_cleaned.xlsx')

print('=' * 60)
print('ANALYSE DES COLONNES - Cultures et Marché')
print('=' * 60)

# Rechercher les colonnes liées aux cultures
keywords = ['culture', 'produi', 'marche', 'vend', 'production', 'contre', 'saison', 'besoin', 'semence']

print('\nColonnes pertinentes trouvées:')
relevant_cols = []
for col in df.columns:
    if any(word in col.lower() for word in keywords):
        relevant_cols.append(col)
        print(f'  - {col}')

print(f'\nTotal: {len(relevant_cols)} colonnes')

# Afficher quelques exemples de données
if relevant_cols:
    print('\n' + '=' * 60)
    print('EXEMPLES DE DONNÉES')
    print('=' * 60)
    for col in relevant_cols[:5]:  # Afficher les 5 premières
        print(f'\n{col}:')
        values = df[col].dropna().unique()[:5]
        for val in values:
            print(f'  - {val}')
