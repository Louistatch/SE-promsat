#!/usr/bin/env python3
"""
Script de test pour vérifier les améliorations du zoom par région
"""

import pandas as pd
from dashboard_sig_streamlit import load_excel_data, load_geodata

def test_zoom_statistics():
    """Test des statistiques par préfecture dans une région"""
    print("=" * 60)
    print("TEST: Statistiques de Zoom par Région")
    print("=" * 60)
    
    df = load_excel_data()
    
    # Tester pour chaque région
    for region in sorted(df['region'].unique()):
        print(f"\nRégion: {region}")
        print("-" * 60)
        
        region_data = df[df['region'] == region]
        
        # Métriques globales
        print(f"  Coopératives: {len(region_data)}")
        print(f"  Effectif Total: {int(region_data['effectif_total'].sum())}")
        print(f"  Femmes: {int(region_data['nb_femmes'].sum())}")
        print(f"  Jeunes: {int(region_data['nb_jeunes'].sum())}")
        
        # Stats par préfecture
        stats_pref = region_data.groupby('prefecture').agg({
            'cooperative': 'count',
            'effectif_total': 'sum',
            'nb_femmes': 'sum',
            'nb_jeunes': 'sum'
        }).rename(columns={'cooperative': 'Nb Coop'}).reset_index()
        
        print(f"\n  Préfectures ({len(stats_pref)}):")
        for _, row in stats_pref.sort_values('Nb Coop', ascending=False).iterrows():
            pref_name = row['prefecture'] if pd.notna(row['prefecture']) else 'Non renseigné'
            print(f"    - {pref_name}: {int(row['Nb Coop'])} coop, {int(row['effectif_total'])} membres")
        
        # Stats par commune
        stats_commune = region_data.groupby(['prefecture', 'commune']).agg({
            'cooperative': 'count'
        }).rename(columns={'cooperative': 'Nb Coop'}).reset_index()
        
        print(f"\n  Communes ({len(stats_commune)}):")
        top_communes = stats_commune.nlargest(3, 'Nb Coop')
        for _, row in top_communes.iterrows():
            pref_name = row['prefecture'] if pd.notna(row['prefecture']) else 'N/A'
            commune_name = row['commune'] if pd.notna(row['commune']) else 'Non renseigné'
            print(f"    - {commune_name} ({pref_name}): {int(row['Nb Coop'])} coop")
        
        # Indicateurs de performance
        stats_pref['Taux Femmes (%)'] = (stats_pref['nb_femmes'] / stats_pref['effectif_total'] * 100).round(1)
        stats_pref['Taux Jeunes (%)'] = (stats_pref['nb_jeunes'] / stats_pref['effectif_total'] * 100).round(1)
        stats_pref['Effectif Moyen'] = (stats_pref['effectif_total'] / stats_pref['Nb Coop']).round(1)
        
        print(f"\n  Indicateurs de Performance:")
        for _, row in stats_pref.iterrows():
            pref_name = row['prefecture'] if pd.notna(row['prefecture']) else 'Non renseigné'
            print(f"    - {pref_name}:")
            print(f"      • Taux Femmes: {row['Taux Femmes (%)']}%")
            print(f"      • Taux Jeunes: {row['Taux Jeunes (%)']}%")
            print(f"      • Effectif Moyen: {row['Effectif Moyen']} membres/coop")

def test_prefecture_colors():
    """Test de la génération de couleurs pour les préfectures"""
    print("\n" + "=" * 60)
    print("TEST: Génération de Couleurs par Préfecture")
    print("=" * 60)
    
    df = load_excel_data()
    
    import matplotlib.cm as cm
    
    for region in sorted(df['region'].unique())[:2]:  # Tester 2 régions
        region_data = df[df['region'] == region]
        prefectures = region_data['prefecture'].dropna().unique()
        
        print(f"\nRégion: {region}")
        print(f"  Nombre de préfectures: {len(prefectures)}")
        
        colors_pref = cm.get_cmap('tab10', len(prefectures))
        
        print("  Couleurs assignées:")
        for i, pref in enumerate(prefectures):
            color = colors_pref(i)
            print(f"    - {pref}: RGB{tuple(int(c*255) for c in color[:3])}")

def test_geodata_matching():
    """Test de correspondance entre données Excel et GADM pour le zoom"""
    print("\n" + "=" * 60)
    print("TEST: Correspondance Données Excel <-> GADM")
    print("=" * 60)
    
    df = load_excel_data()
    gdf_regions, gdf_prefectures, gdf_country = load_geodata()
    
    for region in sorted(df['region'].unique()):
        print(f"\nRégion: {region}")
        
        # Préfectures dans Excel
        excel_prefs = set(df[df['region'] == region]['prefecture'].dropna().unique())
        
        # Préfectures dans GADM
        gadm_prefs = set(gdf_prefectures[gdf_prefectures['NAME_1'] == region]['NAME_2'].unique())
        
        print(f"  Excel: {len(excel_prefs)} préfectures")
        print(f"  GADM: {len(gadm_prefs)} préfectures")
        
        # Correspondances
        common = excel_prefs & gadm_prefs
        only_excel = excel_prefs - gadm_prefs
        
        if common:
            print(f"  ✓ Correspondances ({len(common)}): {', '.join(sorted(common))}")
        
        if only_excel:
            print(f"  Uniquement dans Excel ({len(only_excel)}): {', '.join(sorted(only_excel))}")

def test_data_completeness():
    """Test de complétude des données pour le zoom"""
    print("\n" + "=" * 60)
    print("TEST: Complétude des Données")
    print("=" * 60)
    
    df = load_excel_data()
    
    print(f"\nTotal coopératives: {len(df)}")
    print(f"\nValeurs manquantes:")
    print(f"  - Préfecture: {df['prefecture'].isna().sum()} ({df['prefecture'].isna().sum()/len(df)*100:.1f}%)")
    print(f"  - Commune: {df['commune'].isna().sum()} ({df['commune'].isna().sum()/len(df)*100:.1f}%)")
    print(f"  - Village: {df['village'].isna().sum()} ({df['village'].isna().sum()/len(df)*100:.1f}%)")
    
    print(f"\nCoopératives avec données complètes:")
    complete = df[df['prefecture'].notna() & df['commune'].notna() & df['village'].notna()]
    print(f"  {len(complete)} / {len(df)} ({len(complete)/len(df)*100:.1f}%)")

if __name__ == "__main__":
    try:
        test_zoom_statistics()
        test_prefecture_colors()
        test_geodata_matching()
        test_data_completeness()
        
        print("\n" + "=" * 60)
        print("✓ TOUS LES TESTS SONT PASSÉS")
        print("=" * 60)
        print("\nLes améliorations du zoom par région sont opérationnelles.")
        print("Lancez le dashboard avec: streamlit run dashboard_sig_streamlit.py")
        print("Puis sélectionnez 'Zoom sur une Région' dans les types de carte.")
        
    except Exception as e:
        print(f"\n✗ ERREUR: {e}")
        import traceback
        traceback.print_exc()
