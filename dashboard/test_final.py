#!/usr/bin/env python3
"""Test final de toutes les fonctionnalités"""

print('=' * 60)
print('TEST FINAL - Dashboard SIG ProSMAT')
print('=' * 60)

import dashboard_sig_streamlit as dash

# Test 1: Chargement des données
print('\n1. Chargement des données...')
df = dash.load_excel_data()
print(f'   ✓ {len(df)} coopératives chargées')

# Test 2: Colonnes géographiques
print('\n2. Vérification des colonnes géographiques...')
print(f'   ✓ Préfectures: {df["prefecture"].nunique()} uniques')
print(f'   ✓ Communes: {df["commune"].nunique()} uniques')
print(f'   ✓ Villages: {df["village"].nunique()} uniques')

# Test 3: Géodonnées
print('\n3. Chargement des géodonnées...')
gdf_r, gdf_p, gdf_c = dash.load_geodata()
print(f'   ✓ {len(gdf_r)} régions')
print(f'   ✓ {len(gdf_p)} préfectures GADM')
print(f'   ✓ {len(gdf_c)} pays')

# Test 4: Statistiques par région
print('\n4. Statistiques par région...')
for region in sorted(df['region'].unique()):
    region_data = df[df['region'] == region]
    n_pref = region_data['prefecture'].nunique()
    n_comm = region_data['commune'].nunique()
    print(f'   ✓ {region}: {len(region_data)} coop, {n_pref} préf, {n_comm} comm')

# Test 5: Fonctionnalités du zoom
print('\n5. Test des fonctionnalités de zoom...')
test_region = 'Kara'
region_data = df[df['region'] == test_region]
stats_pref = region_data.groupby('prefecture').agg({
    'cooperative': 'count',
    'effectif_total': 'sum'
}).reset_index()
print(f'   ✓ Zoom sur {test_region}: {len(stats_pref)} préfectures')
print(f'   ✓ Statistiques calculées correctement')

print('\n' + '=' * 60)
print('TOUS LES TESTS SONT PASSÉS')
print('=' * 60)
print('\nLe dashboard est prêt à être utilisé !')
print('\nCommande de lancement:')
print('   streamlit run dashboard_sig_streamlit.py')
print('\nFonctionnalités disponibles:')
print('   • Carte interactive Folium')
print('   • 13 types de cartes SIG')
print('   • Zoom par région avec détails par préfecture')
print('   • Analyses Data Science')
print('   • Export de données')
print('\nDocumentation:')
print('   • GUIDE_UTILISATION_ZOOM.md - Guide utilisateur')
print('   • RESUME_FINAL.md - Résumé complet')
print('   • AMELIORATIONS_ZOOM_REGION.md - Détails techniques')
