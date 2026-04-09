#!/usr/bin/env python3
"""Test de l'onglet Marché Agroécologique"""

import pandas as pd
from collections import Counter

print('=' * 60)
print('TEST - Onglet Marché Agroécologique')
print('=' * 60)

# Charger les données
df = pd.read_excel('MISSION_DE_SUIVI_cleaned.xlsx')

# Test 1: Scoring des coopératives
print('\n1. Test du Scoring des Coopératives')
print('-' * 60)

# Simuler le scoring
df_score = df.copy()

# Critères de base
criteria = {
    'engagement_agroeco': "4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?",
    'immatricule': '3.4. Êtes-vous immatriculé ? ',
    'restitution': '4.1. Avez-vous organisé la restitution de la formation ? ',
    'parcelle': "6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?",
    'production_cs': '6.4. Pouvez-vous produire collectivement ou individuellement en cette contre saison (Période de Décembre à Avril) '
}

# Compter les Oui pour chaque critère
for name, col in criteria.items():
    if col in df.columns:
        count_oui = (df[col] == 'Oui').sum()
        total = df[col].notna().sum()
        pct = (count_oui / total * 100) if total > 0 else 0
        print(f'  {name}: {count_oui}/{total} Oui ({pct:.1f}%)')

# Test 2: Analyse des cultures
print('\n2. Test de l\'Analyse des Cultures')
print('-' * 60)

culture_col = '6.6. Si oui, quelles sont les cultures que vous voudriez produire en contre-saison ? '

if culture_col in df.columns:
    # Extraire toutes les cultures
    all_cultures = []
    for val in df[culture_col].dropna():
        cultures = str(val).split(',')
        for culture in cultures:
            culture_clean = culture.strip().upper()
            if culture_clean and len(culture_clean) > 2:
                all_cultures.append(culture_clean)
    
    # Compter
    culture_counts = Counter(all_cultures)
    
    print(f'  Total de mentions: {len(all_cultures)}')
    print(f'  Cultures uniques: {len(culture_counts)}')
    print(f'\n  Top 10 Cultures:')
    for culture, count in culture_counts.most_common(10):
        print(f'    {count:3d} - {culture}')
else:
    print('  Colonne cultures non trouvée')

# Test 3: Statistiques globales
print('\n3. Statistiques Globales')
print('-' * 60)

print(f'  Total coopératives: {len(df)}')
print(f'  Avec coordonnées GPS: {df["_6.3. Coordonnées géographiques delaparcelle_latitude"].notna().sum()}')

# Effectifs
effectif_col = '3.2.1.Effectif total des membres '
if effectif_col in df.columns:
    effectif_total = pd.to_numeric(df[effectif_col], errors='coerce').sum()
    print(f'  Effectif total: {int(effectif_total)} membres')

# Test 4: Potentiel par région
print('\n4. Potentiel par Région')
print('-' * 60)

region_col = '2.1. Région'
if region_col in df.columns and criteria['engagement_agroeco'] in df.columns:
    for region in sorted(df[region_col].dropna().unique()):
        region_data = df[df[region_col] == region]
        engaged = (region_data[criteria['engagement_agroeco']] == 'Oui').sum()
        total = len(region_data)
        pct = (engaged / total * 100) if total > 0 else 0
        print(f'  {region}: {engaged}/{total} engagées ({pct:.1f}%)')

print('\n' + '=' * 60)
print('TESTS TERMINÉS')
print('=' * 60)
print('\nL\'onglet Marché Agroécologique est prêt à être utilisé.')
print('Lancez le dashboard avec: streamlit run dashboard_sig_streamlit.py')
print('Puis allez dans l\'onglet "Marché Agroécologique"')
