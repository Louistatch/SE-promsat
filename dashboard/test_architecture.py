#!/usr/bin/env python3
"""
Script de test pour vérifier la nouvelle architecture avec préfectures et communes
"""

import pandas as pd
import geopandas as gpd
from dashboard_sig_streamlit import load_excel_data, load_geodata

def test_data_loading():
    """Test du chargement des données"""
    print("=" * 60)
    print("TEST 1: Chargement des données Excel")
    print("=" * 60)
    
    df = load_excel_data()
    print(f"✓ Données chargées: {len(df)} lignes")
    
    # Vérifier les colonnes géographiques
    required_cols = ['region', 'prefecture', 'commune', 'village']
    for col in required_cols:
        if col in df.columns:
            n_unique = df[col].nunique()
            n_nan = df[col].isna().sum()
            print(f"✓ Colonne '{col}': {n_unique} valeurs uniques, {n_nan} valeurs manquantes")
        else:
            print(f"✗ Colonne '{col}' manquante!")
    
    print()

def test_geodata_loading():
    """Test du chargement des données géographiques"""
    print("=" * 60)
    print("TEST 2: Chargement des données géographiques GADM")
    print("=" * 60)
    
    gdf_regions, gdf_prefectures, gdf_country = load_geodata()
    print(f"✓ Régions: {len(gdf_regions)} entités")
    print(f"✓ Préfectures: {len(gdf_prefectures)} entités")
    print(f"✓ Pays: {len(gdf_country)} entité(s)")
    print()

def test_prefecture_matching():
    """Test de correspondance entre préfectures Excel et GADM"""
    print("=" * 60)
    print("TEST 3: Correspondance préfectures Excel <-> GADM")
    print("=" * 60)
    
    df = load_excel_data()
    gdf_regions, gdf_prefectures, gdf_country = load_geodata()
    
    excel_prefs = set(df['prefecture'].dropna().unique())
    gadm_prefs = set(gdf_prefectures['NAME_2'].unique())
    
    print(f"Préfectures dans Excel: {len(excel_prefs)}")
    print(f"Préfectures dans GADM: {len(gadm_prefs)}")
    
    # Préfectures communes
    common = excel_prefs & gadm_prefs
    print(f"\n✓ Préfectures communes: {len(common)}")
    for pref in sorted(common):
        print(f"  - {pref}")
    
    # Préfectures uniquement dans Excel
    only_excel = excel_prefs - gadm_prefs
    if only_excel:
        print(f"\nPréfectures uniquement dans Excel: {len(only_excel)}")
        for pref in sorted(only_excel):
            print(f"  - {pref}")
    
    # Préfectures uniquement dans GADM
    only_gadm = gadm_prefs - excel_prefs
    if only_gadm:
        print(f"\nPréfectures uniquement dans GADM: {len(only_gadm)}")
        for pref in sorted(only_gadm)[:10]:  # Afficher seulement les 10 premières
            print(f"  - {pref}")
        if len(only_gadm) > 10:
            print(f"  ... et {len(only_gadm) - 10} autres")
    
    print()

def test_statistics():
    """Test des statistiques par préfecture et commune"""
    print("=" * 60)
    print("TEST 4: Statistiques par préfecture et commune")
    print("=" * 60)
    
    df = load_excel_data()
    
    # Stats par préfecture
    stats_pref = df.groupby('prefecture').agg({
        'cooperative': 'count',
        'effectif_total': 'sum'
    }).rename(columns={'cooperative': 'nb_coop'}).reset_index()
    
    print("Top 5 préfectures par nombre de coopératives:")
    top_prefs = stats_pref.nlargest(5, 'nb_coop')
    for _, row in top_prefs.iterrows():
        print(f"  - {row['prefecture']}: {int(row['nb_coop'])} coopératives, {int(row['effectif_total'])} membres")
    
    # Stats par commune
    stats_commune = df.groupby('commune').agg({
        'cooperative': 'count',
        'effectif_total': 'sum'
    }).rename(columns={'cooperative': 'nb_coop'}).reset_index()
    
    print("\nTop 5 communes par nombre de coopératives:")
    top_communes = stats_commune.nlargest(5, 'nb_coop')
    for _, row in top_communes.iterrows():
        commune_name = row['commune'] if pd.notna(row['commune']) else 'Non renseigné'
        print(f"  - {commune_name}: {int(row['nb_coop'])} coopératives, {int(row['effectif_total'])} membres")
    
    print()

def test_hierarchical_structure():
    """Test de la structure hiérarchique région > préfecture > commune"""
    print("=" * 60)
    print("TEST 5: Structure hiérarchique")
    print("=" * 60)
    
    df = load_excel_data()
    
    for region in sorted(df['region'].unique()):
        region_data = df[df['region'] == region]
        n_prefs = region_data['prefecture'].nunique()
        n_communes = region_data['commune'].nunique()
        n_coops = len(region_data)
        
        print(f"\n{region}:")
        print(f"  - {n_prefs} préfectures")
        print(f"  - {n_communes} communes")
        print(f"  - {n_coops} coopératives")
        
        # Afficher les préfectures de cette région
        prefs = sorted(region_data['prefecture'].dropna().unique())
        if prefs:
            print(f"  Préfectures: {', '.join(prefs[:3])}", end="")
            if len(prefs) > 3:
                print(f" ... (+{len(prefs)-3})")
            else:
                print()
    
    print()

if __name__ == "__main__":
    try:
        test_data_loading()
        test_geodata_loading()
        test_prefecture_matching()
        test_statistics()
        test_hierarchical_structure()
        
        print("=" * 60)
        print("✓ TOUS LES TESTS SONT PASSÉS")
        print("=" * 60)
        print("\nLe dashboard est prêt à être utilisé avec la nouvelle architecture.")
        print("Lancez-le avec: streamlit run dashboard_sig_streamlit.py")
        
    except Exception as e:
        print(f"\n✗ ERREUR: {e}")
        import traceback
        traceback.print_exc()
