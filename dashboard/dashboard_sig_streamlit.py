#!/usr/bin/env python3
"""
Dashboard SIG Avancé - Mission de Suivi des Coopératives ProSMAT
Niveau Data Science avec Streamlit
Deux cartes séparées: Folium (interactive) et SIG (matplotlib)

Développé par: TATCHIDA Louis
Qualifications: 
    - MSc Agronomie
    - MSc Ingénierie Financière adaptée à l'Agriculture
    - Data Analyst

Version: 3.0
Date: 2025
"""

import streamlit as st
import pandas as pd
import geopandas as gpd
import numpy as np
import folium
from folium import plugins
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium, folium_static
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
import io
warnings.filterwarnings('ignore')

# Importer les styles personnalisés
from map_styles import (
    REGION_COLORS, STATUS_COLORS, CHOROPLETH_CMAPS, MARKERS, LABELS, TITLES, SUBTITLES,
    configure_matplotlib, get_text_color, create_annotation_box, add_region_labels,
    add_prefecture_boundaries, format_number, get_map_title, get_base_map_style,
    get_choropleth_style, get_scatter_style
)

# Importer les utilitaires de carte
from map_utils import (
    add_scale_bar, add_north_arrow, add_legend_box, add_info_box,
    add_title_box, add_coordinates_grid, add_data_source, add_statistics_box
)

# Configuration de la page
st.set_page_config(
    page_title="Dashboard SIG - Cooperatives ProSMAT",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé amélioré
st.markdown("""
<style>
    /* En-tête principal */
    .main-header {
        font-size: 2.2rem;
        font-weight: bold;
        color: #ffffff;
        text-align: center;
        padding: 1.5rem;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 50%, #7e8ba3 100%);
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    /* Logo et titre */
    .logo-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 20px;
        margin-bottom: 2rem;
    }
    
    /* Cartes métriques */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.2rem;
        border-radius: 12px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    
    /* Section de filtres */
    .filter-section {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1.5rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    }
    
    /* Onglets */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background-color: #f8f9fa;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 12px 24px;
        font-weight: 500;
        border: 2px solid transparent;
        transition: all 0.3s ease;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: #e9ecef;
        border-color: #667eea;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-color: #667eea;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #f8f9fa 0%, #e9ecef 100%);
    }
    
    /* Boutons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
    }
    
    /* Info boxes */
    .stAlert {
        border-radius: 10px;
        border-left: 4px solid #667eea;
    }
    
    /* Dataframes */
    .dataframe {
        border-radius: 10px;
        overflow: hidden;
    }
    
    /* Métriques Streamlit */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: bold;
    }
    
    /* Cartes */
    .element-container iframe {
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# =====================================================
# FONCTIONS DE CHARGEMENT DES DONNÉES
# =====================================================
@st.cache_data
def load_excel_data(uploaded_file=None):
    """Charger et nettoyer les données Excel"""
    if uploaded_file is not None:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel('MISSION_DE_SUIVI_cleaned.xlsx')

    # Mapping des colonnes - ATTENTION aux espaces dans les noms originaux
    column_mapping = {
        '2.1. Région': 'region',
        'prefectures': 'prefecture',  # NOUVELLE COLONNE
        'Commune': 'commune',  # NOUVELLE COLONNE
        '2.4. Canton': 'canton',  # Ancienne colonne (pour compatibilité)
        '2.5. Village': 'village',
        '3.1. Nom de la coopérative': 'cooperative',
        '3.2.1.Effectif total des membres ': 'effectif_total',  # ESPACE À LA FIN
        '3.2.2.Nombre de Jeune (moins de 35 ans)': 'nb_jeunes',
        '3.2.3.Nombre de femmes': 'nb_femmes',
        '3.2.4.Nombre de personnes vivant avec un handicap': 'nb_handicap',
        '3.4. Êtes-vous immatriculé ? ': 'immatricule',  # ESPACE À LA FIN
        '4.1. Avez-vous organisé la restitution de la formation ? ': 'restitution_formation',  # ESPACE À LA FIN
        "4.1.6. Y-a-t-il eu des engagements fermes d'adoption des pratiques agroécologiques par les membres ?": 'engagement_agroeco',
        "6.1. Avez-vous déjà choisi la parcelle d'apprentissage ?": 'parcelle_choisie',
        '6.4. Pouvez-vous produire collectivement ou individuellement en cette contre saison (Période de Décembre à Avril) ': 'production_contre_saison',  # ESPACE À LA FIN
        '_6.3. Coordonnées géographiques delaparcelle_latitude': 'latitude',
        '_6.3. Coordonnées géographiques delaparcelle_longitude': 'longitude',
        'Nom et prénoms du CRP': 'crp',
        '1.Date de la visite': 'date_visite',
        "5.1. La coopérative a-t-elle reçu du matériel de production d'intrants ?": 'materiel_recu',
        '3.3.1.Nom du président': 'president',
        '3.3.2.Contact du président': 'contact_president'
    }

    # Appliquer le mapping
    for old_name, new_name in column_mapping.items():
        if old_name in df.columns:
            df[new_name] = df[old_name]
    
    # Créer les colonnes manquantes avec valeur par défaut SEULEMENT si elles n'existent pas
    required_cols = ['region', 'prefecture', 'commune', 'canton', 'village', 'cooperative', 'effectif_total', 'nb_jeunes', 
                     'nb_femmes', 'nb_handicap', 'immatricule', 'restitution_formation', 
                     'engagement_agroeco', 'parcelle_choisie', 'production_contre_saison', 
                     'latitude', 'longitude', 'crp', 'materiel_recu']
    
    for col in required_cols:
        if col not in df.columns:
            if col in ['effectif_total', 'nb_jeunes', 'nb_femmes', 'nb_handicap']:
                df[col] = 0
            else:
                df[col] = 'Non renseigné'

    # Nettoyer les coordonnées
    df_clean = df.dropna(subset=['latitude', 'longitude']).copy()
    df_clean = df_clean[(df_clean['latitude'] != 0) & (df_clean['longitude'] != 0)]
    df_clean = df_clean[(df_clean['latitude'] > 5) & (df_clean['latitude'] < 12)]
    df_clean = df_clean[(df_clean['longitude'] > -1) & (df_clean['longitude'] < 2)]

    # Convertir les colonnes numériques
    for col in ['effectif_total', 'nb_jeunes', 'nb_femmes', 'nb_handicap']:
        if col in df_clean.columns:
            df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce').fillna(0).astype(int)

    # Nettoyer les valeurs catégorielles
    for col in ['immatricule', 'restitution_formation', 'engagement_agroeco', 'parcelle_choisie', 'production_contre_saison', 'materiel_recu']:
        if col in df_clean.columns:
            df_clean[col] = df_clean[col].fillna('Non renseigné')
            # Nettoyer les valeurs vides ou espaces
            df_clean[col] = df_clean[col].astype(str).str.strip()
            df_clean[col] = df_clean[col].replace('', 'Non renseigné')
            df_clean[col] = df_clean[col].replace('nan', 'Non renseigné')
    
    # Normaliser les noms de régions pour correspondre au GADM
    region_mapping = {
        'Centrale': 'Centre',
        'Centre': 'Centre',
        'Kara': 'Kara',
        'Maritime': 'Maritime',
        'Plateaux': 'Plateaux',
        'Savanes': 'Savanes'
    }
    
    if 'region' in df_clean.columns:
        df_clean['region_original'] = df_clean['region']
        df_clean['region'] = df_clean['region'].map(region_mapping).fillna(df_clean['region'])

    return df_clean

@st.cache_data
def load_geodata():
    """Charger les données géographiques GADM"""
    gdf_regions = gpd.read_file('gadm41_TGO.gpkg', layer='ADM_ADM_1')
    gdf_prefectures = gpd.read_file('gadm41_TGO.gpkg', layer='ADM_ADM_2')
    gdf_country = gpd.read_file('gadm41_TGO.gpkg', layer='ADM_ADM_0')
    return gdf_regions, gdf_prefectures, gdf_country

# =====================================================
# FONCTIONS DE CRÉATION DES CARTES
# =====================================================
def create_folium_map(df_filtered, gdf_regions, gdf_prefectures, show_heatmap=False, show_clusters=True):
    """Créer la carte Folium interactive"""

    # Centre de la carte
    if len(df_filtered) > 0:
        center_lat = df_filtered['latitude'].mean()
        center_lon = df_filtered['longitude'].mean()
    else:
        center_lat, center_lon = 8.6195, 0.8248

    # Créer la carte
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=7,
        tiles='CartoDB positron'
    )

    # Ajouter différentes tuiles
    folium.TileLayer('OpenStreetMap', name='OpenStreetMap').add_to(m)
    folium.TileLayer('CartoDB dark_matter', name='Mode Sombre').add_to(m)
    folium.TileLayer(
        tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        attr='Esri', name='Satellite'
    ).add_to(m)

    # Utiliser les couleurs de map_styles.py
    region_colors = REGION_COLORS

    # Calculer les stats par région pour choroplèthe
    stats_region = df_filtered.groupby('region').agg({
        'cooperative': 'count',
        'effectif_total': 'sum',
        'nb_femmes': 'sum',
        'nb_jeunes': 'sum'
    }).rename(columns={'cooperative': 'nb_cooperatives'}).reset_index()

    gdf_regions_stats = gdf_regions.merge(
        stats_region, left_on='NAME_1', right_on='region', how='left'
    ).fillna(0)

    # Style choroplèthe
    def style_function_regions(feature):
        nb_coop = feature['properties'].get('nb_cooperatives', 0)
        if nb_coop == 0:
            color = '#cccccc'
        elif nb_coop < 20:
            color = '#fee0d2'
        elif nb_coop < 40:
            color = '#fc9272'
        elif nb_coop < 60:
            color = '#de2d26'
        else:
            color = '#a50f15'
        return {
            'fillColor': color,
            'color': '#333333',
            'weight': 2,
            'fillOpacity': 0.5
        }

    # Ajouter les régions choroplèthes
    region_layer = folium.FeatureGroup(name='Régions (Choroplèthe)')
    folium.GeoJson(
        gdf_regions_stats.__geo_interface__,
        style_function=style_function_regions,
        tooltip=folium.GeoJsonTooltip(
            fields=['NAME_1', 'nb_cooperatives', 'effectif_total', 'nb_femmes', 'nb_jeunes'],
            aliases=['Région', 'Coopératives', 'Effectif Total', 'Femmes', 'Jeunes'],
            style="background-color: white; color: #333; font-size: 12px; padding: 10px;"
        )
    ).add_to(region_layer)
    region_layer.add_to(m)

    # Ajouter les préfectures
    pref_layer = folium.FeatureGroup(name='Préfectures')
    folium.GeoJson(
        gdf_prefectures.__geo_interface__,
        style_function=lambda x: {'fillColor': 'transparent', 'color': '#666', 'weight': 1},
        tooltip=folium.GeoJsonTooltip(fields=['NAME_1', 'NAME_2'], aliases=['Région', 'Préfecture'])
    ).add_to(pref_layer)
    pref_layer.add_to(m)

    # Ajouter les marqueurs par région
    if show_clusters:
        for region in df_filtered['region'].unique():
            region_df = df_filtered[df_filtered['region'] == region]
            color = region_colors.get(region, '#333333')
            group = folium.FeatureGroup(name=f'Coopératives - {region}')

            for _, row in region_df.iterrows():
                popup_html = f"""
                <div style="width:320px; font-family: Arial;">
                    <h4 style="color:{color}; border-bottom:2px solid {color}; padding-bottom:5px;">
                        {row.get('cooperative', 'N/A')}
                    </h4>
                    <table style="width:100%; font-size:11px;">
                        <tr><td><b>Région:</b></td><td>{row.get('region', 'N/A')}</td></tr>
                        <tr><td><b>Préfecture:</b></td><td>{row.get('prefecture', 'N/A')}</td></tr>
                        <tr><td><b>Commune:</b></td><td>{row.get('commune', 'N/A')}</td></tr>
                        <tr><td><b>Village:</b></td><td>{row.get('village', 'N/A')}</td></tr>
                        <tr><td colspan="2" style="background:#f0f0f0"><b>--- Effectifs ---</b></td></tr>
                        <tr><td><b>Effectif Total:</b></td><td>{int(row.get('effectif_total', 0))}</td></tr>
                        <tr><td><b>Femmes:</b></td><td>{int(row.get('nb_femmes', 0))}</td></tr>
                        <tr><td><b>Jeunes:</b></td><td>{int(row.get('nb_jeunes', 0))}</td></tr>
                        <tr><td><b>Handicapés:</b></td><td>{int(row.get('nb_handicap', 0))}</td></tr>
                        <tr><td colspan="2" style="background:#f0f0f0"><b>--- Statuts ---</b></td></tr>
                        <tr><td><b>Immatriculé:</b></td><td>{row.get('immatricule', 'N/A')}</td></tr>
                        <tr><td><b>Restitution:</b></td><td>{row.get('restitution_formation', 'N/A')}</td></tr>
                        <tr><td><b>Engagement Agroéco:</b></td><td>{row.get('engagement_agroeco', 'N/A')}</td></tr>
                        <tr><td><b>Parcelle Choisie:</b></td><td>{row.get('parcelle_choisie', 'N/A')}</td></tr>
                        <tr><td><b>Production CS:</b></td><td>{row.get('production_contre_saison', 'N/A')}</td></tr>
                        <tr><td colspan="2" style="background:#f0f0f0"><b>--- Mission ---</b></td></tr>
                        <tr><td><b>CRP:</b></td><td>{row.get('crp', 'N/A')}</td></tr>
                        <tr><td><b>Coordonnées:</b></td><td>{row['latitude']:.4f}, {row['longitude']:.4f}</td></tr>
                    </table>
                </div>
                """

                folium.Marker(
                    location=[row['latitude'], row['longitude']],
                    popup=folium.Popup(popup_html, max_width=350),
                    tooltip=f"{row.get('cooperative', 'N/A')}",
                    icon=folium.Icon(color='white', icon_color=color, icon='users', prefix='fa')
                ).add_to(group)

            group.add_to(m)

    # Carte de chaleur
    if show_heatmap and len(df_filtered) > 0:
        heat_layer = folium.FeatureGroup(name='Carte de Chaleur')
        heat_data = [[row['latitude'], row['longitude']] for _, row in df_filtered.iterrows()]
        HeatMap(heat_data, radius=15, blur=10, gradient={0.4: 'blue', 0.65: 'lime', 1: 'red'}).add_to(heat_layer)
        heat_layer.add_to(m)

    # Contrôles
    folium.LayerControl(collapsed=False).add_to(m)
    plugins.Fullscreen().add_to(m)
    plugins.MiniMap(toggle_display=True).add_to(m)

    # Légende
    legend_html = f'''
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 9999;
         background: white; padding: 15px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.2);">
        <h4 style="margin:0 0 10px 0;">Légende</h4>
        <p style="margin:3px 0;"><span style="background:#e74c3c;width:12px;height:12px;display:inline-block;border-radius:2px;"></span> Centrale</p>
        <p style="margin:3px 0;"><span style="background:#3498db;width:12px;height:12px;display:inline-block;border-radius:2px;"></span> Kara</p>
        <p style="margin:3px 0;"><span style="background:#2ecc71;width:12px;height:12px;display:inline-block;border-radius:2px;"></span> Savanes</p>
        <p style="margin:3px 0;"><span style="background:#9b59b6;width:12px;height:12px;display:inline-block;border-radius:2px;"></span> Plateaux</p>
        <p style="margin:3px 0;"><span style="background:#f39c12;width:12px;height:12px;display:inline-block;border-radius:2px;"></span> Maritime</p>
        <hr style="margin:8px 0;">
        <p style="margin:3px 0;font-size:10px;"><b>{len(df_filtered)} coopératives affichées</b></p>
    </div>
    '''
    m.get_root().html.add_child(folium.Element(legend_html))

    return m

def create_matplotlib_sig_map(df_filtered, gdf_regions, gdf_prefectures, map_type='localisation', 
                             selected_region=None, zoom_level=1, custom_bounds=None):
    """Créer la carte SIG avec matplotlib avec support du zoom"""

    # Configuration matplotlib
    configure_matplotlib()
    
    # Calculer les stats par région
    stats_region = df_filtered.groupby('region').agg({
        'cooperative': 'count',
        'effectif_total': 'sum',
        'nb_femmes': 'sum',
        'nb_jeunes': 'sum',
        'nb_handicap': 'sum'
    }).rename(columns={'cooperative': 'nb_cooperatives'}).reset_index()

    gdf_stats = gdf_regions.merge(stats_region, left_on='NAME_1', right_on='region', how='left').fillna(0)
    
    # Calculer les stats par préfecture
    stats_prefecture = df_filtered.groupby(['region', 'prefecture']).agg({
        'cooperative': 'count',
        'effectif_total': 'sum',
        'nb_femmes': 'sum',
        'nb_jeunes': 'sum'
    }).rename(columns={'cooperative': 'nb_cooperatives'}).reset_index()

    base_style = get_base_map_style()
    fig, ax = plt.subplots(1, 1, figsize=base_style['figsize'])

    if map_type == 'localisation':
        # Carte de localisation des coopératives
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures)

        for region, color in REGION_COLORS.items():
            region_data = df_filtered[df_filtered['region'] == region]
            if len(region_data) > 0:
                ax.scatter(
                    region_data['longitude'], region_data['latitude'],
                    c=color, s=50, alpha=0.7, label=f'{region} ({len(region_data)})',
                    edgecolor='white', linewidth=0.5
                )

        for idx, row in gdf_regions.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['NAME_1'], xy=(centroid.x, centroid.y),
                       ha='center', fontsize=10, fontweight='bold', color='#2c3e50')

        ax.legend(loc='lower left', fontsize=9, framealpha=0.9)
        ax.set_title(get_map_title(map_type, count=len(df_filtered)),
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'choropleth_coop':
        # Choroplèthe nombre de coopératives
        style = get_choropleth_style('cooperatives')
        gdf_stats.plot(ax=ax, column='nb_cooperatives', cmap=style['cmap'], 
                      edgecolor=style['edgecolor'], linewidth=style['linewidth'],
                      legend=style['legend'], legend_kwds={'label': 'Nombre de cooperatives', 'shrink': style['legend_shrink']})
        
        add_prefecture_boundaries(ax, gdf_prefectures)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            nb = int(row['nb_cooperatives'])
            text_color = get_text_color(nb, gdf_stats['nb_cooperatives'].mean())
            ax.annotate(f"{row['NAME_1']}\n{nb} coop.", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=create_annotation_box(text_color))

        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'choropleth_effectif':
        # Choroplèthe effectif total
        style = get_choropleth_style('effectif')
        gdf_stats.plot(ax=ax, column='effectif_total', cmap=style['cmap'],
                      edgecolor=style['edgecolor'], linewidth=style['linewidth'],
                      legend=style['legend'], legend_kwds={'label': 'Effectif total', 'shrink': style['legend_shrink']})
        
        add_prefecture_boundaries(ax, gdf_prefectures)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            eff = int(row['effectif_total'])
            text_color = get_text_color(eff, gdf_stats['effectif_total'].mean())
            ax.annotate(f"{row['NAME_1']}\n{format_number(eff)} membres", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=create_annotation_box(text_color))

        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'choropleth_femmes':
        # Choroplèthe nombre de femmes
        style = get_choropleth_style('femmes')
        gdf_stats.plot(ax=ax, column='nb_femmes', cmap=style['cmap'],
                      edgecolor=style['edgecolor'], linewidth=style['linewidth'],
                      legend=style['legend'], legend_kwds={'label': 'Nombre de femmes', 'shrink': style['legend_shrink']})
        
        add_prefecture_boundaries(ax, gdf_prefectures)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            fem = int(row['nb_femmes'])
            text_color = get_text_color(fem, gdf_stats['nb_femmes'].mean())
            ax.annotate(f"{row['NAME_1']}\n{format_number(fem)} F", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=create_annotation_box(text_color))

        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'choropleth_jeunes':
        # Choroplèthe nombre de jeunes
        style = get_choropleth_style('jeunes')
        gdf_stats.plot(ax=ax, column='nb_jeunes', cmap=style['cmap'],
                      edgecolor=style['edgecolor'], linewidth=style['linewidth'],
                      legend=style['legend'], legend_kwds={'label': 'Nombre de jeunes', 'shrink': style['legend_shrink']})
        
        add_prefecture_boundaries(ax, gdf_prefectures)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            jeunes = int(row['nb_jeunes'])
            text_color = get_text_color(jeunes, gdf_stats['nb_jeunes'].mean())
            ax.annotate(f"{row['NAME_1']}\n{format_number(jeunes)} J", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=create_annotation_box(text_color))

        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'choropleth_handicap':
        # Choroplèthe nombre de personnes handicapées
        style = get_choropleth_style('handicap')
        gdf_stats.plot(ax=ax, column='nb_handicap', cmap=style['cmap'],
                      edgecolor=style['edgecolor'], linewidth=style['linewidth'],
                      legend=style['legend'], legend_kwds={'label': 'Nombre de personnes handicapees', 'shrink': style['legend_shrink']})
        
        add_prefecture_boundaries(ax, gdf_prefectures)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            handicap = int(row['nb_handicap'])
            text_color = get_text_color(handicap, gdf_stats['nb_handicap'].mean())
            ax.annotate(f"{row['NAME_1']}\n{handicap} H", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=create_annotation_box(text_color))

        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'immatriculation':
        # Carte statut immatriculation
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures)

        immat_oui = df_filtered[df_filtered['immatricule'] == 'Oui']
        immat_non = df_filtered[df_filtered['immatricule'] == 'Non']
        immat_nr = df_filtered[df_filtered['immatricule'].isin(['Non renseigné', 'nan', ''])]

        style_oui = get_scatter_style('oui')
        style_non = get_scatter_style('non')
        style_nr = get_scatter_style('non_renseigne')

        if len(immat_oui) > 0:
            ax.scatter(immat_oui['longitude'], immat_oui['latitude'], 
                      c=STATUS_COLORS['oui'], label=f"{LABELS['immatriculation']['oui']} ({len(immat_oui)})",
                      **style_oui)
        if len(immat_non) > 0:
            ax.scatter(immat_non['longitude'], immat_non['latitude'],
                      c=STATUS_COLORS['non'], label=f"{LABELS['immatriculation']['non']} ({len(immat_non)})",
                      **style_non)
        if len(immat_nr) > 0:
            ax.scatter(immat_nr['longitude'], immat_nr['latitude'],
                      c=STATUS_COLORS['non_renseigne'], label=f"{LABELS['immatriculation']['non_renseigne']} ({len(immat_nr)})",
                      **style_nr)
        
        add_region_labels(ax, gdf_regions)
        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'engagement':
        # Carte engagement agroécologique
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures)

        engage_oui = df_filtered[df_filtered['engagement_agroeco'] == 'Oui']
        engage_non = df_filtered[df_filtered['engagement_agroeco'] == 'Non']
        engage_nr = df_filtered[df_filtered['engagement_agroeco'].isin(['Non renseigné', 'nan', ''])]

        style_oui = get_scatter_style('oui')
        style_non = get_scatter_style('non')
        style_nr = get_scatter_style('non_renseigne')

        if len(engage_oui) > 0:
            ax.scatter(engage_oui['longitude'], engage_oui['latitude'],
                      c=STATUS_COLORS['oui'], label=f"{LABELS['engagement']['oui']} ({len(engage_oui)})",
                      **style_oui)
        if len(engage_non) > 0:
            ax.scatter(engage_non['longitude'], engage_non['latitude'],
                      c=STATUS_COLORS['non'], label=f"{LABELS['engagement']['non']} ({len(engage_non)})",
                      **style_non)
        if len(engage_nr) > 0:
            ax.scatter(engage_nr['longitude'], engage_nr['latitude'],
                      c=STATUS_COLORS['non_renseigne'], label=f"{LABELS['engagement']['non_renseigne']} ({len(engage_nr)})",
                      **style_nr)
        
        add_region_labels(ax, gdf_regions)
        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'parcelle':
        # Carte parcelle choisie
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures)

        parcelle_oui = df_filtered[df_filtered['parcelle_choisie'] == 'Oui']
        parcelle_non = df_filtered[df_filtered['parcelle_choisie'] == 'Non']
        parcelle_nr = df_filtered[df_filtered['parcelle_choisie'].isin(['Non renseigné', 'nan', ''])]

        style_oui = get_scatter_style('oui')
        style_non = get_scatter_style('non')
        style_nr = get_scatter_style('non_renseigne')

        if len(parcelle_oui) > 0:
            ax.scatter(parcelle_oui['longitude'], parcelle_oui['latitude'],
                      c=STATUS_COLORS['oui'], label=f"{LABELS['parcelle']['oui']} ({len(parcelle_oui)})",
                      **style_oui)
        if len(parcelle_non) > 0:
            ax.scatter(parcelle_non['longitude'], parcelle_non['latitude'],
                      c=STATUS_COLORS['non'], label=f"{LABELS['parcelle']['non']} ({len(parcelle_non)})",
                      **style_non)
        if len(parcelle_nr) > 0:
            ax.scatter(parcelle_nr['longitude'], parcelle_nr['latitude'],
                      c=STATUS_COLORS['non_renseigne'], label=f"{LABELS['parcelle']['non_renseigne']} ({len(parcelle_nr)})",
                      **style_nr)
        
        add_region_labels(ax, gdf_regions)
        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'materiel':
        # Carte matériel reçu
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures)

        materiel_oui = df_filtered[df_filtered['materiel_recu'] == 'Oui']
        materiel_non = df_filtered[df_filtered['materiel_recu'] == 'Non']
        materiel_nr = df_filtered[df_filtered['materiel_recu'].isin(['Non renseigné', 'nan', ''])]

        style_oui = get_scatter_style('oui')
        style_non = get_scatter_style('non')
        style_nr = get_scatter_style('non_renseigne')

        if len(materiel_oui) > 0:
            ax.scatter(materiel_oui['longitude'], materiel_oui['latitude'],
                      c=STATUS_COLORS['oui'], label=f"{LABELS['materiel']['oui']} ({len(materiel_oui)})",
                      **style_oui)
        if len(materiel_non) > 0:
            ax.scatter(materiel_non['longitude'], materiel_non['latitude'],
                      c=STATUS_COLORS['non'], label=f"{LABELS['materiel']['non']} ({len(materiel_non)})",
                      **style_non)
        if len(materiel_nr) > 0:
            ax.scatter(materiel_nr['longitude'], materiel_nr['latitude'],
                      c=STATUS_COLORS['non_renseigne'], label=f"{LABELS['materiel']['non_renseigne']} ({len(materiel_nr)})",
                      **style_nr)
        
        add_region_labels(ax, gdf_regions)
        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'taille_effectif':
        # Points proportionnels à l'effectif
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures, alpha=0.3)

        sizes = df_filtered['effectif_total'].fillna(10)
        if sizes.max() > sizes.min():
            sizes = (sizes - sizes.min()) / (sizes.max() - sizes.min()) * 200 + 30
        else:
            sizes = 50

        for region, color in REGION_COLORS.items():
            region_data = df_filtered[df_filtered['region'] == region]
            if len(region_data) > 0:
                region_sizes = sizes[df_filtered['region'] == region]
                ax.scatter(region_data['longitude'], region_data['latitude'], c=color, s=region_sizes,
                          alpha=0.6, label=region, edgecolor='white', linewidth=0.5)

        ax.legend(loc='lower left', fontsize=9)
        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'zoom_region' and selected_region:
        # Zoom sur une région spécifique avec détails par préfecture
        region_gdf = gdf_regions[gdf_regions['NAME_1'] == selected_region]
        region_pref = gdf_prefectures[gdf_prefectures['NAME_1'] == selected_region]
        region_data = df_filtered[df_filtered['region'] == selected_region]
        
        if len(region_gdf) > 0:
            # Fond de la région
            region_gdf.plot(ax=ax, color='#f0f0f0', 
                           edgecolor='black', linewidth=2.5)
            
            # Calculer les stats par préfecture pour colorer
            stats_pref_zoom = region_data.groupby('prefecture').agg({
                'cooperative': 'count'
            }).rename(columns={'cooperative': 'nb_coop'}).reset_index()
            
            # Merger avec les géométries
            region_pref_stats = region_pref.merge(stats_pref_zoom, left_on='NAME_2', right_on='prefecture', how='left').fillna(0)
            
            # Afficher les préfectures avec un dégradé de couleur selon le nombre de coopératives
            if len(region_pref_stats) > 0 and region_pref_stats['nb_coop'].max() > 0:
                region_pref_stats.plot(ax=ax, column='nb_coop', cmap='YlOrRd', 
                                      edgecolor='#333', linewidth=1.5, alpha=0.7,
                                      legend=True, legend_kwds={'label': 'Nb Cooperatives', 'shrink': 0.6})
            else:
                region_pref.plot(ax=ax, color='white', edgecolor='#666', linewidth=1.5, alpha=0.5)
            
            # Afficher les noms des préfectures avec le nombre de coopératives
            for idx, row in region_pref_stats.iterrows():
                centroid = row.geometry.centroid
                nb_coop = int(row['nb_coop']) if pd.notna(row['nb_coop']) else 0
                label = f"{row['NAME_2']}\n({nb_coop} coop.)"
                
                # Boîte de texte pour meilleure lisibilité
                ax.annotate(label, xy=(centroid.x, centroid.y),
                           ha='center', va='center', fontsize=9, fontweight='bold',
                           color='#2c3e50',
                           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                                   alpha=0.8, edgecolor='#333', linewidth=1))
            
            # Afficher les coopératives par préfecture avec des couleurs différentes
            if len(region_data) > 0:
                # Générer des couleurs pour chaque préfecture
                import matplotlib.cm as cm
                prefectures_in_region = region_data['prefecture'].dropna().unique()
                colors_pref = cm.get_cmap('tab10', len(prefectures_in_region))
                
                for i, pref in enumerate(prefectures_in_region):
                    pref_data = region_data[region_data['prefecture'] == pref]
                    color = colors_pref(i)
                    ax.scatter(pref_data['longitude'], pref_data['latitude'], 
                              c=[color], s=100, alpha=0.8, edgecolor='white', 
                              linewidth=1.5, label=f'{pref} ({len(pref_data)})')
                
                # Légende pour les préfectures
                ax.legend(loc='upper left', fontsize=8, framealpha=0.95, 
                         title='Préfectures', title_fontsize=9)
            
            # Ajuster les limites
            bounds = region_gdf.total_bounds
            margin = 0.1
            ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
            ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
            
            ax.set_title(get_map_title(map_type, selected_region=selected_region, count=len(region_data)),
                        fontsize=14, fontweight='bold', pad=15)
            
            # Ajouter une grille pour faciliter la lecture
            ax.grid(True, linestyle='--', alpha=0.3, color='gray', linewidth=0.5)
        else:
            ax.text(0.5, 0.5, 'Region non trouvee', ha='center', va='center', transform=ax.transAxes)
            
    elif map_type == 'prefecture_detail':
        # Détail par préfecture avec statistiques
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'], alpha=0.3)
        
        # Calculer stats par préfecture
        stats_pref = df_filtered.groupby('prefecture').agg({
            'cooperative': 'count',
            'effectif_total': 'sum'
        }).rename(columns={'cooperative': 'nb_coop'}).reset_index()
        
        gdf_pref_stats = gdf_prefectures.merge(stats_pref, left_on='NAME_2', right_on='prefecture', how='left').fillna(0)
        
        style = get_choropleth_style('prefecture')
        gdf_pref_stats.plot(ax=ax, column='nb_coop', cmap=style['cmap'], 
                           edgecolor=style['edgecolor'], linewidth=0.5,
                           legend=style['legend'], 
                           legend_kwds={'label': 'Nombre de cooperatives', 'shrink': style['legend_shrink']})
        
        # Annoter les préfectures avec données
        for idx, row in gdf_pref_stats.iterrows():
            if row['nb_coop'] > 0:
                centroid = row.geometry.centroid
                ax.annotate(f"{row['NAME_2']}\n({int(row['nb_coop'])})", 
                           xy=(centroid.x, centroid.y),
                           ha='center', fontsize=7, fontweight='bold')
        
        ax.set_title(get_map_title(map_type), fontsize=14, fontweight='bold', pad=15)

    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_aspect('equal')

    plt.tight_layout()
    return fig
    """Créer la carte SIG avec matplotlib"""

    # Configuration matplotlib
    plt.switch_backend("Agg")
    plt.style.use("seaborn-v0_8")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.unicode_minus"] = False

    region_colors = {
        'Centrale': '#e74c3c',
        'Kara': '#3498db',
        'Savanes': '#2ecc71',
        'Plateaux': '#9b59b6',
        'Maritime': '#f39c12'
    }

    # Calculer les stats par région
    stats_region = df_filtered.groupby('region').agg({
        'cooperative': 'count',
        'effectif_total': 'sum',
        'nb_femmes': 'sum',
        'nb_jeunes': 'sum',
        'nb_handicap': 'sum'
    }).rename(columns={'cooperative': 'nb_cooperatives'}).reset_index()

    gdf_stats = gdf_regions.merge(stats_region, left_on='NAME_1', right_on='region', how='left').fillna(0)
    
    # Calculer les stats par préfecture
    stats_prefecture = df_filtered.groupby(['region', 'prefecture']).agg({
        'cooperative': 'count',
        'effectif_total': 'sum',
        'nb_femmes': 'sum',
        'nb_jeunes': 'sum'
    }).rename(columns={'cooperative': 'nb_cooperatives'}).reset_index()

    fig, ax = plt.subplots(1, 1, figsize=(12, 14))

    if map_type == 'localisation':
        # Carte de localisation des coopératives
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1)
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--')

        for region, color in region_colors.items():
            region_data = df_filtered[df_filtered['region'] == region]
            if len(region_data) > 0:
                ax.scatter(
                    region_data['longitude'], region_data['latitude'],
                    c=color, s=50, alpha=0.7, label=f'{region} ({len(region_data)})',
                    edgecolor='white', linewidth=0.5
                )

        for idx, row in gdf_regions.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['NAME_1'], xy=(centroid.x, centroid.y),
                       ha='center', fontsize=10, fontweight='bold', color='#2c3e50')

        ax.legend(loc='lower left', fontsize=9, framealpha=0.9)
        ax.set_title(f'Localisation des Coopératives par Région\n({len(df_filtered)} coopératives)',
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'choropleth_coop':
        # Choroplèthe nombre de coopératives
        gdf_stats.plot(ax=ax, column='nb_cooperatives', cmap='Reds', edgecolor='black', linewidth=1,
                      legend=True, legend_kwds={'label': 'Nombre de coopératives', 'shrink': 0.6})
        
        # Ajouter les limites des préfectures
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--', alpha=0.5)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            nb = int(row['nb_cooperatives'])
            # Choisir la couleur du texte selon l'intensité
            text_color = 'white' if nb > gdf_stats['nb_cooperatives'].mean() else 'black'
            ax.annotate(f"{row['NAME_1']}\n{nb} coop.", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_title('Nombre de Coopératives par Région\n(Répartition géographique)', 
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'choropleth_effectif':
        # Choroplèthe effectif total
        gdf_stats.plot(ax=ax, column='effectif_total', cmap='Blues', edgecolor='black', linewidth=1,
                      legend=True, legend_kwds={'label': 'Effectif total', 'shrink': 0.6})
        
        # Ajouter les limites des préfectures
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--', alpha=0.5)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            eff = int(row['effectif_total'])
            # Choisir la couleur du texte selon l'intensité
            text_color = 'white' if eff > gdf_stats['effectif_total'].mean() else 'black'
            ax.annotate(f"{row['NAME_1']}\n{eff:,} membres", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_title('Effectif Total des Membres par Région\n(Nombre de personnes dans les coopératives)', 
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'choropleth_femmes':
        # Choroplèthe nombre de femmes
        gdf_stats.plot(ax=ax, column='nb_femmes', cmap='Purples', edgecolor='black', linewidth=1,
                      legend=True, legend_kwds={'label': 'Nombre de femmes', 'shrink': 0.6})
        
        # Ajouter les limites des préfectures
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--', alpha=0.5)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            fem = int(row['nb_femmes'])
            # Choisir la couleur du texte selon l'intensité
            text_color = 'white' if fem > gdf_stats['nb_femmes'].mean() else 'black'
            ax.annotate(f"{row['NAME_1']}\n{format_number(fem)} F", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_title('Nombre de Femmes par Région\n(Membres féminins des coopératives)', 
                    fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'choropleth_jeunes':
        # Choroplèthe nombre de jeunes
        gdf_stats.plot(ax=ax, column='nb_jeunes', cmap='Greens', edgecolor='black', linewidth=1,
                      legend=True, legend_kwds={'label': 'Nombre de jeunes', 'shrink': 0.6})
        
        # Ajouter les limites des préfectures
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--', alpha=0.5)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            jeunes = int(row['nb_jeunes'])
            # Choisir la couleur du texte selon l'intensité
            text_color = 'white' if jeunes > gdf_stats['nb_jeunes'].mean() else 'black'
            ax.annotate(f"{row['NAME_1']}\n{format_number(jeunes)} J", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_title('Nombre de Jeunes (<35 ans) par Région\n(Membres jeunes des coopératives)', 
                    fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'choropleth_handicap':
        # Choroplèthe nombre de personnes handicapées
        gdf_stats.plot(ax=ax, column='nb_handicap', cmap='Oranges', edgecolor='black', linewidth=1,
                      legend=True, legend_kwds={'label': 'Nombre de personnes handicapées', 'shrink': 0.6})
        
        # Ajouter les limites des préfectures
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--', alpha=0.5)

        for idx, row in gdf_stats.iterrows():
            centroid = row.geometry.centroid
            handicap = int(row['nb_handicap'])
            # Choisir la couleur du texte selon l'intensité
            text_color = 'white' if handicap > gdf_stats['nb_handicap'].mean() else 'black'
            ax.annotate(f"{row['NAME_1']}\n{handicap} H", xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, fontweight='bold', color=text_color,
                       bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7, edgecolor='none'))

        ax.set_title('Nombre de Personnes Handicapées par Région\n(Membres vivant avec un handicap)', 
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'immatriculation':
        # Carte statut immatriculation
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1)
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--')

        immat_oui = df_filtered[df_filtered['immatricule'] == 'Oui']
        immat_non = df_filtered[df_filtered['immatricule'] == 'Non']
        immat_nr = df_filtered[df_filtered['immatricule'].isin(['Non renseigné', 'nan', ''])]

        if len(immat_oui) > 0:
            ax.scatter(immat_oui['longitude'], immat_oui['latitude'], c='#27ae60', s=80, alpha=0.8,
                      label=f'Immatricule ({len(immat_oui)})', marker='o', edgecolor='white', linewidth=1.5)
        if len(immat_non) > 0:
            ax.scatter(immat_non['longitude'], immat_non['latitude'], c='#e74c3c', s=80, alpha=0.8,
                      label=f'Non immatricule ({len(immat_non)})', marker='X', edgecolor='white', linewidth=1.5)
        if len(immat_nr) > 0:
            ax.scatter(immat_nr['longitude'], immat_nr['latitude'], c='#95a5a6', s=60, alpha=0.6,
                      label=f'? Non renseigné ({len(immat_nr)})', marker='s', edgecolor='white', linewidth=1)
        
        # Ajouter les noms des régions
        for idx, row in gdf_regions.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['NAME_1'], xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, style='italic', color='#555', alpha=0.7)

        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title("Statut d'Immatriculation des Cooperatives\n(O = Immatricule, X = Non immatricule)", 
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'engagement':
        # Carte engagement agroécologique
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1)
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--')

        engage_oui = df_filtered[df_filtered['engagement_agroeco'] == 'Oui']
        engage_non = df_filtered[df_filtered['engagement_agroeco'] == 'Non']
        engage_nr = df_filtered[df_filtered['engagement_agroeco'].isin(['Non renseigné', 'nan', ''])]

        if len(engage_oui) > 0:
            ax.scatter(engage_oui['longitude'], engage_oui['latitude'], c='#27ae60', s=80, alpha=0.8,
                      label=f'Engage ({len(engage_oui)})', marker='o', edgecolor='white', linewidth=1.5)
        if len(engage_non) > 0:
            ax.scatter(engage_non['longitude'], engage_non['latitude'], c='#e74c3c', s=80, alpha=0.8,
                      label=f'Non engage ({len(engage_non)})', marker='X', edgecolor='white', linewidth=1.5)
        if len(engage_nr) > 0:
            ax.scatter(engage_nr['longitude'], engage_nr['latitude'], c='#95a5a6', s=60, alpha=0.6,
                      label=f'? Non renseigné ({len(engage_nr)})', marker='s', edgecolor='white', linewidth=1)
        
        # Ajouter les noms des régions
        for idx, row in gdf_regions.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['NAME_1'], xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, style='italic', color='#555', alpha=0.7)

        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title('Engagement Agroecologique des Cooperatives\n(O = Engage, X = Non engage)', 
                    fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'parcelle':
        # Carte parcelle choisie
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1)
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--')

        parcelle_oui = df_filtered[df_filtered['parcelle_choisie'] == 'Oui']
        parcelle_non = df_filtered[df_filtered['parcelle_choisie'] == 'Non']
        parcelle_nr = df_filtered[df_filtered['parcelle_choisie'].isin(['Non renseigné', 'nan', ''])]

        if len(parcelle_oui) > 0:
            ax.scatter(parcelle_oui['longitude'], parcelle_oui['latitude'], c='#27ae60', s=80, alpha=0.8,
                      label=f'Parcelle choisie ({len(parcelle_oui)})', marker='o', edgecolor='white', linewidth=1.5)
        if len(parcelle_non) > 0:
            ax.scatter(parcelle_non['longitude'], parcelle_non['latitude'], c='#e74c3c', s=80, alpha=0.8,
                      label=f'Pas de parcelle ({len(parcelle_non)})', marker='X', edgecolor='white', linewidth=1.5)
        if len(parcelle_nr) > 0:
            ax.scatter(parcelle_nr['longitude'], parcelle_nr['latitude'], c='#95a5a6', s=60, alpha=0.6,
                      label=f'? Non renseigné ({len(parcelle_nr)})', marker='s', edgecolor='white', linewidth=1)
        
        # Ajouter les noms des régions
        for idx, row in gdf_regions.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['NAME_1'], xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, style='italic', color='#555', alpha=0.7)

        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title("Statut de Choix de Parcelle d'Apprentissage\n(O = Parcelle choisie, X = Pas de parcelle)", 
                    fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'materiel':
        # Carte matériel reçu
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1)
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3, linestyle='--')

        materiel_oui = df_filtered[df_filtered['materiel_recu'] == 'Oui']
        materiel_non = df_filtered[df_filtered['materiel_recu'] == 'Non']
        materiel_nr = df_filtered[df_filtered['materiel_recu'].isin(['Non renseigné', 'nan', ''])]

        if len(materiel_oui) > 0:
            ax.scatter(materiel_oui['longitude'], materiel_oui['latitude'], c='#27ae60', s=80, alpha=0.8,
                      label=f'Materiel recu ({len(materiel_oui)})', marker='o', edgecolor='white', linewidth=1.5)
        if len(materiel_non) > 0:
            ax.scatter(materiel_non['longitude'], materiel_non['latitude'], c='#e74c3c', s=80, alpha=0.8,
                      label=f'Pas de materiel ({len(materiel_non)})', marker='X', edgecolor='white', linewidth=1.5)
        if len(materiel_nr) > 0:
            ax.scatter(materiel_nr['longitude'], materiel_nr['latitude'], c='#95a5a6', s=60, alpha=0.6,
                      label=f'? Non renseigné ({len(materiel_nr)})', marker='s', edgecolor='white', linewidth=1)
        
        # Ajouter les noms des régions
        for idx, row in gdf_regions.iterrows():
            centroid = row.geometry.centroid
            ax.annotate(row['NAME_1'], xy=(centroid.x, centroid.y),
                       ha='center', fontsize=9, style='italic', color='#555', alpha=0.7)

        ax.legend(loc='lower left', fontsize=10, framealpha=0.95, edgecolor='black')
        ax.set_title("Reception de Materiel de Production d'Intrants\n(O = Materiel recu, X = Pas de materiel)", 
                    fontsize=14, fontweight='bold', pad=15)

    elif map_type == 'taille_effectif':
        # Points proportionnels à l'effectif
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1)
        gdf_prefectures.boundary.plot(ax=ax, color='gray', linewidth=0.3)

        sizes = df_filtered['effectif_total'].fillna(10)
        if sizes.max() > sizes.min():
            sizes = (sizes - sizes.min()) / (sizes.max() - sizes.min()) * 200 + 30
        else:
            sizes = 50

        for region, color in region_colors.items():
            region_data = df_filtered[df_filtered['region'] == region]
            if len(region_data) > 0:
                region_sizes = sizes[df_filtered['region'] == region]
                ax.scatter(region_data['longitude'], region_data['latitude'], c=color, s=region_sizes,
                          alpha=0.6, label=region, edgecolor='white', linewidth=0.5)

        ax.legend(loc='lower left', fontsize=9)
        ax.set_title('Coopératives (taille = effectif total)', fontsize=14, fontweight='bold', pad=15)
        
    elif map_type == 'zoom_region' and selected_region:
        # Zoom sur une région spécifique
        region_gdf = gdf_regions[gdf_regions['NAME_1'] == selected_region]
        region_pref = gdf_prefectures[gdf_prefectures['NAME_1'] == selected_region]
        region_data = df_filtered[df_filtered['region'] == selected_region]
        
        if len(region_gdf) > 0:
            region_gdf.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=2)
            region_pref.plot(ax=ax, color='white', edgecolor='#666', linewidth=1, alpha=0.3)
            
            # Afficher les noms des préfectures
            for idx, row in region_pref.iterrows():
                centroid = row.geometry.centroid
                ax.annotate(row['NAME_2'], xy=(centroid.x, centroid.y),
                           ha='center', fontsize=8, style='italic', color='#555')
            
            # Afficher les coopératives
            if len(region_data) > 0:
                color = region_colors.get(selected_region, '#333333')
                ax.scatter(region_data['longitude'], region_data['latitude'], 
                          c=color, s=80, alpha=0.7, edgecolor='white', linewidth=1)
                
                # Annoter chaque coopérative
                for idx, row in region_data.iterrows():
                    ax.annotate(row.get('cooperative', '')[:20], 
                               xy=(row['longitude'], row['latitude']),
                               xytext=(5, 5), textcoords='offset points',
                               fontsize=6, alpha=0.7)
            
            # Ajuster les limites
            bounds = region_gdf.total_bounds
            margin = 0.1
            ax.set_xlim(bounds[0] - margin, bounds[2] + margin)
            ax.set_ylim(bounds[1] - margin, bounds[3] + margin)
            
            ax.set_title(f'Zoom sur la Region {selected_region}\n({len(region_data)} cooperatives)',
                        fontsize=14, fontweight='bold', pad=15)
        else:
            ax.text(0.5, 0.5, 'Region non trouvee', ha='center', va='center', transform=ax.transAxes)
    
    elif map_type == 'zoom_custom':
        # Zoom personnalisé sur une zone définie par l'utilisateur
        gdf_regions.plot(ax=ax, color=base_style['region_color'], 
                        edgecolor=base_style['region_edge_color'], 
                        linewidth=base_style['region_edge_width'])
        add_prefecture_boundaries(ax, gdf_prefectures)
        
        # Afficher toutes les coopératives avec couleurs par région
        for region, color in REGION_COLORS.items():
            region_data = df_filtered[df_filtered['region'] == region]
            if len(region_data) > 0:
                ax.scatter(region_data['longitude'], region_data['latitude'], 
                          c=color, s=60, alpha=0.8, label=region, 
                          edgecolor='white', linewidth=1)
        
        if len(df_filtered) > 0:
            ax.legend(loc='best', fontsize=9, framealpha=0.9)
        
        ax.set_title(f'Zoom Personnalise\n({len(df_filtered)} cooperatives)',
                    fontsize=14, fontweight='bold', pad=15)
            
    elif map_type == 'prefecture_detail':
        # Détail par préfecture avec statistiques
        gdf_regions.plot(ax=ax, color='#f5f5f5', edgecolor='black', linewidth=1, alpha=0.3)
        
        # Calculer stats par préfecture
        stats_pref = df_filtered.groupby('prefecture').agg({
            'cooperative': 'count',
            'effectif_total': 'sum'
        }).rename(columns={'cooperative': 'nb_coop'}).reset_index()
        
        gdf_pref_stats = gdf_prefectures.merge(stats_pref, left_on='NAME_2', right_on='prefecture', how='left').fillna(0)
        
        gdf_pref_stats.plot(ax=ax, column='nb_coop', cmap='YlOrRd', edgecolor='black', 
                           linewidth=0.5, legend=True, 
                           legend_kwds={'label': 'Nombre de coopératives', 'shrink': 0.6})
        
        # Annoter les préfectures avec données
        for idx, row in gdf_pref_stats.iterrows():
            if row['nb_coop'] > 0:
                centroid = row.geometry.centroid
                ax.annotate(f"{row['NAME_2']}\n({int(row['nb_coop'])})", 
                           xy=(centroid.x, centroid.y),
                           ha='center', fontsize=7, fontweight='bold')
        
        ax.set_title('Nombre de Cooperatives par Prefecture', fontsize=14, fontweight='bold', pad=15)

    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.set_aspect('equal')
    
    # Ajouter une grille de coordonnées
    add_coordinates_grid(ax, interval=0.5)
    
    # Appliquer le zoom
    if map_type == 'zoom_custom' and custom_bounds:
        # Zoom personnalisé avec limites spécifiées
        lon_min, lat_min, lon_max, lat_max = custom_bounds
        ax.set_xlim(lon_min, lon_max)
        ax.set_ylim(lat_min, lat_max)
    elif zoom_level > 1:
        # Zoom automatique basé sur le niveau
        current_xlim = ax.get_xlim()
        current_ylim = ax.get_ylim()
        
        # Calculer le centre
        center_x = (current_xlim[0] + current_xlim[1]) / 2
        center_y = (current_ylim[0] + current_ylim[1]) / 2
        
        # Calculer la nouvelle étendue (plus petit = plus zoomé)
        zoom_factor = 1 / zoom_level
        width = (current_xlim[1] - current_xlim[0]) * zoom_factor
        height = (current_ylim[1] - current_ylim[0]) * zoom_factor
        
        # Si des données sont filtrées, centrer sur les données
        if len(df_filtered) > 0:
            center_x = df_filtered['longitude'].mean()
            center_y = df_filtered['latitude'].mean()
        
        ax.set_xlim(center_x - width/2, center_x + width/2)
        ax.set_ylim(center_y - height/2, center_y + height/2)
    
    # Ajouter les éléments professionnels
    # 1. Échelle
    add_scale_bar(ax, length=50, location=(ax.get_xlim()[0] + 0.2, ax.get_ylim()[0] + 0.2))
    
    # 2. Rose des vents (flèche Nord)
    add_north_arrow(ax, location=(0.95, 0.95), size=0.05)
    
    # 3. Boîte d'information
    info_text = f"Cooperatives: {len(df_filtered)}\nZoom: {zoom_level}x"
    if len(df_filtered) > 0:
        info_text += f"\nEffectif: {int(df_filtered['effectif_total'].sum()):,}"
    add_info_box(ax, info_text, location=(0.02, 0.98))
    
    # 4. Source des données
    add_data_source(ax, "Source: ProSMAT - Mission de Suivi 2025")
    
    # 5. Statistiques (pour certains types de cartes)
    if map_type in ['localisation', 'taille_effectif'] and len(df_filtered) > 0:
        stats = {
            'Total': len(df_filtered),
            'Femmes': int(df_filtered['nb_femmes'].sum()),
            'Jeunes': int(df_filtered['nb_jeunes'].sum())
        }
        add_statistics_box(ax, stats, location=(0.02, 0.12))

    plt.tight_layout()
    return fig

# =====================================================
# APPLICATION PRINCIPALE
# =====================================================
def main():
    # En-tête avec logo
    col_logo, col_title = st.columns([1, 4])
    
    with col_logo:
        try:
            st.image("logo.jfif", width=150)
        except:
            st.write("")  # Si le logo n'est pas trouvé, continuer sans erreur
    
    with col_title:
        st.markdown("""
        <div style="padding-top: 20px;">
            <h1 style="color: #1e3c72; margin-bottom: 0;">Dashboard SIG ProSMAT</h1>
            <h3 style="color: #7e8ba3; margin-top: 0;">Mission de Suivi des Cooperatives Agricoles ProsMAT</h3>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Option de chargement de fichier
    st.sidebar.markdown("### Chargement des Données")
    data_source = st.sidebar.radio(
        "Source des données",
        ["Fichier par défaut", "Charger un fichier Excel"],
        help="Choisissez d'utiliser le fichier par défaut ou de charger votre propre fichier Excel"
    )
    
    uploaded_file = None
    if data_source == "Charger un fichier Excel":
        # Bouton de téléchargement du template
        st.sidebar.markdown("#### Télécharger le Template")
        st.sidebar.caption("Utilisez ce fichier comme modèle pour vos données")
        
        # Charger le fichier template pour le téléchargement
        try:
            with open('MISSION_DE_SUIVI_cleaned.xlsx', 'rb') as template_file:
                template_data = template_file.read()
            
            st.sidebar.download_button(
                label="📥 Télécharger le Template Excel",
                data=template_data,
                file_name="TEMPLATE_ProSMAT_Cooperatives.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="Téléchargez ce fichier, remplissez-le avec vos données, puis rechargez-le"
            )
        except FileNotFoundError:
            st.sidebar.error("Template non disponible")
        
        st.sidebar.markdown("---")
        
        # File uploader
        uploaded_file = st.sidebar.file_uploader(
            "Choisir un fichier Excel",
            type=['xlsx', 'xls'],
            help="Le fichier doit avoir la même structure que le template téléchargé"
        )
        
        if uploaded_file is not None:
            st.sidebar.success(f"✓ Fichier chargé : {uploaded_file.name}")
        else:
            st.sidebar.warning("⚠ Veuillez charger un fichier Excel")
            
            # Message d'information avec instructions
            st.info("""
            ### 📋 Instructions de Chargement
            
            1. **Téléchargez le template** Excel depuis la barre latérale
            2. **Remplissez-le** avec vos données de coopératives
            3. **Sauvegardez** le fichier sur votre ordinateur
            4. **Chargez-le** en utilisant le bouton "Browse files" dans la barre latérale
            
            **Format requis :**
            - Colonnes : Région, Préfecture, Commune, Village, Coopérative, Effectifs, GPS
            - Coordonnées GPS valides (Latitude: 5-12, Longitude: -1 à 2)
            
            Consultez **TEMPLATE_EXCEL_FORMAT.md** pour plus de détails.
            """)
            st.stop()
    
    st.sidebar.markdown("---")

    # Charger les données
    with st.spinner('Chargement des donnees...'):
        df = load_excel_data(uploaded_file)
        gdf_regions, gdf_prefectures, gdf_country = load_geodata()

    # =====================================================
    # SIDEBAR - FILTRES
    # =====================================================
    # Logo dans la sidebar
    try:
        st.sidebar.image("logo.jfif", use_container_width=True)
    except:
        pass
    
    st.sidebar.markdown("---")
    st.sidebar.title("Filtres de Recherche")
    st.sidebar.markdown("Affinez votre analyse en selectionnant les criteres ci-dessous")
    st.sidebar.markdown("---")

    # Filtre par région
    st.sidebar.markdown("### Localisation Geographique")
    regions = ['Toutes'] + sorted(df['region'].dropna().unique().tolist())
    selected_region = st.sidebar.selectbox("Region", regions)
    
    # Filtre par préfecture (depuis GADM)
    if selected_region != 'Toutes':
        prefectures_list = ['Toutes'] + sorted(gdf_prefectures[gdf_prefectures['NAME_1'] == selected_region]['NAME_2'].unique().tolist())
    else:
        prefectures_list = ['Toutes'] + sorted(gdf_prefectures['NAME_2'].unique().tolist())
    selected_prefecture = st.sidebar.selectbox("Prefecture", prefectures_list)

    # Filtre par canton (dynamique selon région et préfecture)
    if selected_region != 'Toutes':
        communes_list = ['Toutes'] + sorted(df[df['region'] == selected_region]['commune'].dropna().unique().tolist())
    else:
        communes_list = ['Toutes'] + sorted(df['commune'].dropna().unique().tolist())
    selected_commune = st.sidebar.selectbox("Commune", communes_list)
    
    # Filtre par village (dynamique selon commune)
    if selected_commune != 'Toutes':
        if selected_region != 'Toutes':
            villages_list = ['Tous'] + sorted(df[(df['region'] == selected_region) & (df['commune'] == selected_commune)]['village'].dropna().unique().tolist())
        else:
            villages_list = ['Tous'] + sorted(df[df['commune'] == selected_commune]['village'].dropna().unique().tolist())
    else:
        if selected_region != 'Toutes':
            villages_list = ['Tous'] + sorted(df[df['region'] == selected_region]['village'].dropna().unique().tolist())
        else:
            villages_list = ['Tous'] + sorted(df['village'].dropna().unique().tolist())
    selected_village = st.sidebar.selectbox("🏡 Village", villages_list)

    st.sidebar.markdown("---")
    
    # Filtre par CRP
    st.sidebar.markdown("### 👤 Agent de Terrain")
    crps = ['Tous'] + sorted(df['crp'].dropna().unique().tolist())
    selected_crp = st.sidebar.selectbox("Agent CRP", crps)

    st.sidebar.markdown("---")
    
    # Filtres par statuts
    st.sidebar.markdown("### Statuts et Indicateurs")

    immat_options = ['Tous', 'Oui', 'Non', 'Non renseigné']
    selected_immat = st.sidebar.selectbox("Immatriculation", immat_options)

    restitution_options = ['Tous', 'Oui', 'Non', 'Non renseigné']
    selected_restitution = st.sidebar.selectbox("Restitution Formation", restitution_options)

    engagement_options = ['Tous', 'Oui', 'Non', 'Non renseigné']
    selected_engagement = st.sidebar.selectbox("Engagement Agroeco", engagement_options)

    parcelle_options = ['Tous', 'Oui', 'Non', 'Non renseigné']
    selected_parcelle = st.sidebar.selectbox("Parcelle Choisie", parcelle_options)

    production_options = ['Tous', 'Oui', 'Non', 'Non renseigné']
    selected_production = st.sidebar.selectbox("🌿 Production Contre-saison", production_options)

    st.sidebar.markdown("---")
    
    # Filtres numériques
    st.sidebar.markdown("### Effectifs")
    effectif_min, effectif_max = st.sidebar.slider(
        "Effectif total des membres",
        min_value=0,
        max_value=int(df['effectif_total'].max()) if df['effectif_total'].max() > 0 else 100,
        value=(0, int(df['effectif_total'].max()) if df['effectif_total'].max() > 0 else 100)
    )

    # Appliquer les filtres
    df_filtered = df.copy()

    if selected_region != 'Toutes':
        df_filtered = df_filtered[df_filtered['region'] == selected_region]
    
    # Filtre par préfecture (utiliser les coordonnées géographiques)
    if selected_prefecture != 'Toutes':
        # Créer un GeoDataFrame des coopératives
        from shapely.geometry import Point
        geometry = [Point(xy) for xy in zip(df_filtered['longitude'], df_filtered['latitude'])]
        gdf_coops = gpd.GeoDataFrame(df_filtered, geometry=geometry, crs=gdf_prefectures.crs)
        
        # Trouver la préfecture sélectionnée
        prefecture_geom = gdf_prefectures[gdf_prefectures['NAME_2'] == selected_prefecture]
        
        # Faire une jointure spatiale pour trouver les coopératives dans cette préfecture
        gdf_in_prefecture = gpd.sjoin(gdf_coops, prefecture_geom, how='inner', predicate='within')
        
        # Récupérer les indices des coopératives dans la préfecture
        df_filtered = df_filtered.loc[gdf_in_prefecture.index]
    
    if selected_commune != 'Toutes':
        df_filtered = df_filtered[df_filtered['commune'] == selected_commune]
    if selected_village != 'Tous':
        df_filtered = df_filtered[df_filtered['village'] == selected_village]
    if selected_crp != 'Tous':
        df_filtered = df_filtered[df_filtered['crp'] == selected_crp]
    if selected_immat != 'Tous':
        df_filtered = df_filtered[df_filtered['immatricule'] == selected_immat]
    if selected_restitution != 'Tous':
        df_filtered = df_filtered[df_filtered['restitution_formation'] == selected_restitution]
    if selected_engagement != 'Tous':
        df_filtered = df_filtered[df_filtered['engagement_agroeco'] == selected_engagement]
    if selected_parcelle != 'Tous':
        df_filtered = df_filtered[df_filtered['parcelle_choisie'] == selected_parcelle]
    if selected_production != 'Tous':
        df_filtered = df_filtered[df_filtered['production_contre_saison'] == selected_production]

    df_filtered = df_filtered[
        (df_filtered['effectif_total'] >= effectif_min) &
        (df_filtered['effectif_total'] <= effectif_max)
    ]

    # Bouton reset
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Reinitialiser tous les filtres", use_container_width=True):
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.success(f"**{len(df_filtered)}** cooperatives affichees sur **{len(df)}** au total")
    
    # Informations supplémentaires dans la sidebar
    with st.sidebar.expander("Informations"):
        st.markdown("""
        **Dashboard SIG ProSMAT**
        
        Ce tableau de bord permet de visualiser et analyser les donnees des cooperatives agricoles de ProSMAT.
        
        **Fonctionnalites:**
        - Cartes interactives et statiques
        - Filtres hierarchiques
        - Analyses statistiques
        - Export des donnees
        - Chargement de fichiers Excel personnalisés
        """)
        
        # Afficher les informations sur le fichier chargé
        if uploaded_file is not None:
            st.markdown("---")
            st.markdown("**Fichier chargé:**")
            st.info(f"📄 {uploaded_file.name}")
            st.caption(f"Nombre de coopératives: {len(df)}")
    
    with st.sidebar.expander("Guide d'utilisation"):
        st.markdown("""
        **Comment utiliser ce dashboard:**
        
        1. **Source de données**: Choisissez le fichier par défaut ou chargez votre propre fichier Excel
        2. **Filtres**: Selectionnez vos criteres dans la barre laterale
        3. **Cartes**: Explorez les onglets pour differentes visualisations
        4. **Zoom**: Utilisez le slider de zoom pour explorer en detail
        5. **Export**: Telechargez les cartes et donnees
        
        **Format du fichier Excel:**
        - Le fichier doit contenir les colonnes: Région, Préfecture, Commune, Village, Coopérative, Effectifs, Coordonnées GPS
        - Structure identique à MISSION_DE_SUIVI_cleaned.xlsx
        """)
    
    # Signature du développeur
    st.sidebar.markdown("---")
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                border-radius: 10px; color: white; margin-top: 20px;">
        <p style="margin: 0; font-size: 0.85em; font-weight: bold;">Développé par</p>
        <p style="margin: 5px 0; font-size: 1em; font-weight: bold;">TATCHIDA Louis</p>
        <p style="margin: 0; font-size: 0.75em;">MSc Agronomie</p>
        <p style="margin: 0; font-size: 0.75em;">MSc Ingénierie Financière adaptée à l'Agriculture</p>
        <p style="margin: 0; font-size: 0.75em;">Data Analyst</p>
    </div>
    """, unsafe_allow_html=True)


    # =====================================================
    # KPIs PRINCIPAUX
    # =====================================================
    st.markdown("### Indicateurs Cles de Performance")
    st.markdown("")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; color: white;">Cooperatives</h4>
            <h2 style="margin: 10px 0; color: white;">{}</h2>
            <p style="margin: 0; font-size: 0.9em;">{:.1f}% du total</p>
        </div>
        """.format(len(df_filtered), len(df_filtered)/len(df)*100 if len(df) > 0 else 0), unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; color: white;">Effectif Total</h4>
            <h2 style="margin: 10px 0; color: white;">{:,}</h2>
            <p style="margin: 0; font-size: 0.9em;">membres</p>
        </div>
        """.format(int(df_filtered['effectif_total'].sum())), unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; color: white;">Femmes</h4>
            <h2 style="margin: 10px 0; color: white;">{:,}</h2>
            <p style="margin: 0; font-size: 0.9em;">{:.1f}% de l'effectif</p>
        </div>
        """.format(int(df_filtered['nb_femmes'].sum()), 
                   df_filtered['nb_femmes'].sum()/df_filtered['effectif_total'].sum()*100 if df_filtered['effectif_total'].sum() > 0 else 0), 
        unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; color: white;">Jeunes</h4>
            <h2 style="margin: 10px 0; color: white;">{:,}</h2>
            <p style="margin: 0; font-size: 0.9em;">&lt;35 ans</p>
        </div>
        """.format(int(df_filtered['nb_jeunes'].sum())), unsafe_allow_html=True)
    
    with col5:
        pct_immat = len(df_filtered[df_filtered['immatricule'] == 'Oui']) / len(df_filtered) * 100 if len(df_filtered) > 0 else 0
        st.markdown("""
        <div style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); 
                    padding: 20px; border-radius: 10px; text-align: center; color: white;">
            <h4 style="margin: 0; color: white;">Immatriculation</h4>
            <h2 style="margin: 10px 0; color: white;">{:.1f}%</h2>
            <p style="margin: 0; font-size: 0.9em;">taux</p>
        </div>
        """.format(pct_immat), unsafe_allow_html=True)

    st.markdown("---")

    # =====================================================
    # ONGLETS PRINCIPAUX
    # =====================================================
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Carte Folium Interactive", 
        "Carte SIG Statique", 
        "Analyses Data Science", 
        "Marche Agroecologique", 
        "Donnees"
    ])

    # =====================================================
    # TAB 1: CARTE FOLIUM
    # =====================================================
    with tab1:
        st.subheader("Carte Folium Interactive")

        col1, col2 = st.columns([3, 1])
        with col1:
            st.info("Utilisez le panneau de couches (en haut à droite) pour activer/désactiver les différentes visualisations")
        with col2:
            show_heatmap = st.checkbox("Afficher carte de chaleur", value=True)

        folium_map = create_folium_map(df_filtered, gdf_regions, gdf_prefectures, show_heatmap=show_heatmap)
        st_folium(folium_map, width=None, height=650, returned_objects=[])

    # =====================================================
    # TAB 2: CARTE SIG MATPLOTLIB
    # =====================================================
    with tab2:
        st.subheader("Cartes SIG Statiques")
        
        # Contrôles de zoom et de carte
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            map_type = st.selectbox(
                "Selectionner le type de carte",
                options=[
                    ('localisation', 'Localisation des cooperatives'),
                    ('choropleth_coop', 'Choropleth - Nombre de cooperatives'),
                    ('choropleth_effectif', 'Choropleth - Effectif total'),
                    ('choropleth_femmes', 'Choropleth - Nombre de femmes'),
                    ('choropleth_jeunes', 'Choropleth - Nombre de jeunes'),
                    ('choropleth_handicap', 'Choropleth - Personnes handicapees'),
                    ('prefecture_detail', 'Detail par Prefecture'),
                    ('immatriculation', 'Statut Immatriculation'),
                    ('engagement', 'Engagement Agroecologique'),
                    ('parcelle', 'Parcelle d\'Apprentissage'),
                    ('materiel', 'Materiel de Production'),
                    ('taille_effectif', 'Taille proportionnelle a l\'effectif'),
                    ('zoom_region', 'Zoom sur une Region'),
                    ('zoom_custom', 'Zoom Personnalise')
                ],
                format_func=lambda x: x[1]
            )
        
        with col2:
            # Option de zoom sur région
            if map_type[0] == 'zoom_region':
                regions_list = sorted(df_filtered['region'].dropna().unique().tolist())
                if len(regions_list) > 0:
                    zoom_region = st.selectbox("Region a zoomer", regions_list)
                else:
                    zoom_region = None
                    st.warning("Aucune region disponible")
            else:
                zoom_region = None
        
        with col3:
            # Niveau de zoom pour toutes les cartes
            zoom_level = st.slider("Niveau de zoom", min_value=1, max_value=5, value=1, 
                                   help="1 = Vue complete, 5 = Zoom maximum")
        
        # Contrôles de zoom personnalisé
        if map_type[0] == 'zoom_custom':
            st.markdown("#### Parametres de Zoom Personnalise")
            col_z1, col_z2, col_z3, col_z4 = st.columns(4)
            
            with col_z1:
                lon_min = st.number_input("Longitude Min", value=-1.0, step=0.1, format="%.2f")
            with col_z2:
                lon_max = st.number_input("Longitude Max", value=2.0, step=0.1, format="%.2f")
            with col_z3:
                lat_min = st.number_input("Latitude Min", value=6.0, step=0.1, format="%.2f")
            with col_z4:
                lat_max = st.number_input("Latitude Max", value=11.0, step=0.1, format="%.2f")
            
            zoom_bounds = (lon_min, lat_min, lon_max, lat_max)
        else:
            zoom_bounds = None

        # Conteneur pour la carte avec style amélioré
        st.markdown("""
        <div style="background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                    padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        """, unsafe_allow_html=True)
        
        with st.spinner('Generation de la carte SIG en cours...'):
            fig = create_matplotlib_sig_map(df_filtered, gdf_regions, gdf_prefectures, 
                                           map_type=map_type[0], selected_region=zoom_region,
                                           zoom_level=zoom_level, custom_bounds=zoom_bounds)
            
            # Afficher la carte dans un conteneur avec zoom
            st.pyplot(fig, use_container_width=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Informations sur la carte
        col_info1, col_info2, col_info3 = st.columns(3)
        with col_info1:
            st.info(f"**{len(df_filtered)}** cooperatives affichees")
        with col_info2:
            st.info(f"**Niveau de zoom:** {zoom_level}/5")
        with col_info3:
            st.info(f"**Type:** {map_type[1]}")

        # Statistiques supplémentaires
        if map_type[0] == 'prefecture_detail':
            st.markdown("---")
            st.subheader("Statistiques par Prefecture")
            
            stats_pref = df_filtered.groupby('prefecture').agg({
                'cooperative': 'count',
                'effectif_total': 'sum',
                'nb_femmes': 'sum',
                'nb_jeunes': 'sum'
            }).rename(columns={'cooperative': 'Nombre de cooperatives'}).reset_index()
            stats_pref.columns = ['Prefecture', 'Cooperatives', 'Effectif Total', 'Femmes', 'Jeunes']
            stats_pref = stats_pref.sort_values('Cooperatives', ascending=False)
            
            st.dataframe(stats_pref, use_container_width=True, hide_index=True)
        
        elif map_type[0] == 'zoom_region' and zoom_region:
            st.markdown("---")
            st.subheader(f"Statistiques pour la Region {zoom_region}")
            
            region_data = df_filtered[df_filtered['region'] == zoom_region]
            
            # Métriques globales de la région
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Cooperatives", len(region_data))
            with col2:
                st.metric("Effectif Total", f"{int(region_data['effectif_total'].sum()):,}")
            with col3:
                st.metric("Femmes", f"{int(region_data['nb_femmes'].sum()):,}")
            with col4:
                st.metric("Jeunes", f"{int(region_data['nb_jeunes'].sum()):,}")
            
            st.markdown("---")
            
            # Statistiques par préfecture
            st.markdown("### Détails par Préfecture")
            
            stats_pref_region = region_data.groupby('prefecture').agg({
                'cooperative': 'count',
                'effectif_total': 'sum',
                'nb_femmes': 'sum',
                'nb_jeunes': 'sum',
                'nb_handicap': 'sum'
            }).rename(columns={'cooperative': 'Nb Cooperatives'}).reset_index()
            
            stats_pref_region.columns = ['Prefecture', 'Cooperatives', 'Effectif Total', 'Femmes', 'Jeunes', 'Handicapes']
            stats_pref_region = stats_pref_region.sort_values('Cooperatives', ascending=False)
            
            # Afficher les stats par préfecture avec des graphiques
            col_left, col_right = st.columns([1, 1])
            
            with col_left:
                st.markdown("#### Tableau des Préfectures")
                st.dataframe(stats_pref_region, use_container_width=True, hide_index=True)
            
            with col_right:
                st.markdown("#### Répartition par Préfecture")
                # Graphique en barres
                fig_pref = px.bar(
                    stats_pref_region, 
                    x='Prefecture', 
                    y='Cooperatives',
                    color='Effectif Total',
                    title=f'Nombre de Coopératives par Préfecture - {zoom_region}',
                    labels={'Cooperatives': 'Nombre de Coopératives', 'Effectif Total': 'Effectif'},
                    color_continuous_scale='Viridis'
                )
                fig_pref.update_layout(xaxis_tickangle=-45, height=400)
                st.plotly_chart(fig_pref, use_container_width=True)
            
            st.markdown("---")
            
            # Statistiques par commune dans la région
            st.markdown("### Détails par Commune")
            
            stats_commune_region = region_data.groupby(['prefecture', 'commune']).agg({
                'cooperative': 'count',
                'effectif_total': 'sum',
                'nb_femmes': 'sum',
                'nb_jeunes': 'sum'
            }).rename(columns={'cooperative': 'Nb Cooperatives'}).reset_index()
            
            stats_commune_region.columns = ['Prefecture', 'Commune', 'Cooperatives', 'Effectif Total', 'Femmes', 'Jeunes']
            stats_commune_region = stats_commune_region.sort_values(['Prefecture', 'Cooperatives'], ascending=[True, False])
            
            # Sélecteur de préfecture pour filtrer les communes
            prefs_in_region = sorted(region_data['prefecture'].dropna().unique())
            if len(prefs_in_region) > 0:
                selected_pref_filter = st.selectbox(
                    "Filtrer par préfecture (optionnel)", 
                    ['Toutes'] + prefs_in_region,
                    key='pref_filter_zoom'
                )
                
                if selected_pref_filter != 'Toutes':
                    stats_commune_display = stats_commune_region[stats_commune_region['Prefecture'] == selected_pref_filter]
                else:
                    stats_commune_display = stats_commune_region
                
                col_commune_left, col_commune_right = st.columns([1, 1])
                
                with col_commune_left:
                    st.markdown("#### Tableau des Communes")
                    st.dataframe(stats_commune_display, use_container_width=True, hide_index=True)
                
                with col_commune_right:
                    st.markdown("#### Top 10 Communes")
                    top_communes = stats_commune_display.nlargest(10, 'Cooperatives')
                    fig_commune = px.bar(
                        top_communes,
                        x='Commune',
                        y='Cooperatives',
                        color='Prefecture',
                        title='Top 10 Communes par Nombre de Coopératives',
                        labels={'Cooperatives': 'Nombre de Coopératives'}
                    )
                    fig_commune.update_layout(xaxis_tickangle=-45, height=400)
                    st.plotly_chart(fig_commune, use_container_width=True)
            
            st.markdown("---")
            
            # Indicateurs de performance par préfecture
            st.markdown("### Indicateurs de Performance par Préfecture")
            
            col_ind1, col_ind2, col_ind3 = st.columns(3)
            
            with col_ind1:
                st.markdown("#### Taux de Féminisation")
                stats_pref_region['Taux Femmes (%)'] = (stats_pref_region['Femmes'] / stats_pref_region['Effectif Total'] * 100).round(1)
                fig_femmes = px.bar(
                    stats_pref_region,
                    x='Prefecture',
                    y='Taux Femmes (%)',
                    title='% de Femmes par Préfecture',
                    color='Taux Femmes (%)',
                    color_continuous_scale='RdYlGn'
                )
                fig_femmes.update_layout(xaxis_tickangle=-45, height=300, showlegend=False)
                st.plotly_chart(fig_femmes, use_container_width=True)
            
            with col_ind2:
                st.markdown("#### Taux de Jeunes")
                stats_pref_region['Taux Jeunes (%)'] = (stats_pref_region['Jeunes'] / stats_pref_region['Effectif Total'] * 100).round(1)
                fig_jeunes = px.bar(
                    stats_pref_region,
                    x='Prefecture',
                    y='Taux Jeunes (%)',
                    title='% de Jeunes par Préfecture',
                    color='Taux Jeunes (%)',
                    color_continuous_scale='Blues'
                )
                fig_jeunes.update_layout(xaxis_tickangle=-45, height=300, showlegend=False)
                st.plotly_chart(fig_jeunes, use_container_width=True)
            
            with col_ind3:
                st.markdown("#### Effectif Moyen")
                stats_pref_region['Effectif Moyen'] = (stats_pref_region['Effectif Total'] / stats_pref_region['Cooperatives']).round(1)
                fig_moy = px.bar(
                    stats_pref_region,
                    x='Prefecture',
                    y='Effectif Moyen',
                    title='Effectif Moyen par Coopérative',
                    color='Effectif Moyen',
                    color_continuous_scale='Oranges'
                )
                fig_moy.update_layout(xaxis_tickangle=-45, height=300, showlegend=False)
                st.plotly_chart(fig_moy, use_container_width=True)
            
            st.markdown("---")
            
            # Tableau détaillé des coopératives de la région
            st.markdown("### 📋 Liste Détaillée des Coopératives")
            region_table = region_data[['cooperative', 'prefecture', 'commune', 'village', 'effectif_total', 'nb_femmes', 'nb_jeunes', 'immatricule', 'engagement_agroeco']].copy()
            region_table.columns = ['Cooperative', 'Prefecture', 'Commune', 'Village', 'Effectif', 'Femmes', 'Jeunes', 'Immatricule', 'Engagement AE']
            
            # Ajouter un filtre par préfecture pour la liste
            pref_filter_list = st.multiselect(
                "Filtrer par préfecture(s)",
                options=sorted(region_data['prefecture'].dropna().unique()),
                default=None,
                key='pref_filter_list'
            )
            
            if pref_filter_list:
                region_table_display = region_table[region_table['Prefecture'].isin(pref_filter_list)]
            else:
                region_table_display = region_table
            
            st.dataframe(region_table_display, use_container_width=True, hide_index=True)

        # Bouton de téléchargement
        buf = io.BytesIO()
        fig.savefig(buf, format='png', dpi=200, bbox_inches='tight', facecolor='white')
        buf.seek(0)
        st.download_button(
            label="Telecharger la carte (PNG)",
            data=buf,
            file_name=f"carte_sig_{map_type[0]}_zoom{zoom_level}.png",
            mime="image/png"
        )
        plt.close(fig)

    # =====================================================
    # TAB 3: ANALYSES DATA SCIENCE
    # =====================================================
    with tab3:
        st.subheader("Analyses des données")

        # Sous-onglets pour les analyses
        analysis_tab1, analysis_tab2, analysis_tab3, analysis_tab4 = st.tabs([
            "Distribution", "Correlations", "Indicateurs", "Tendances"
        ])

        with analysis_tab1:
            col1, col2 = st.columns(2)

            with col1:
                # Distribution par région
                fig_region = px.pie(
                    df_filtered.groupby('region').size().reset_index(name='count'),
                    values='count', names='region',
                    title='Répartition des coopératives par région',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig_region.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig_region, use_container_width=True)

            with col2:
                # Distribution effectif par région
                fig_effectif = px.bar(
                    df_filtered.groupby('region')['effectif_total'].sum().reset_index(),
                    x='region', y='effectif_total',
                    title='Effectif total par région',
                    color='region',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_effectif, use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                # Histogramme effectif
                fig_hist = px.histogram(
                    df_filtered, x='effectif_total', nbins=20,
                    title='Distribution de l\'effectif total',
                    color_discrete_sequence=['#667eea']
                )
                st.plotly_chart(fig_hist, use_container_width=True)

            with col4:
                # Box plot par région
                fig_box = px.box(
                    df_filtered, x='region', y='effectif_total',
                    title='Effectif par région (Box Plot)',
                    color='region',
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                st.plotly_chart(fig_box, use_container_width=True)

        with analysis_tab2:
            st.markdown("""
            ### Guide d'interprétation des corrélations
            
            **Matrice de corrélation :** Mesure la relation linéaire entre deux variables numériques.
            - **Valeur proche de +1** : Corrélation positive forte (quand l'une augmente, l'autre aussi)
            - **Valeur proche de 0** : Pas de corrélation linéaire
            - **Valeur proche de -1** : Corrélation négative forte (quand l'une augmente, l'autre diminue)
            
            **Couleurs :**
            - 🔴 Rouge : Corrélation positive
            - 🔵 Bleu : Corrélation négative
            - ⚪ Blanc : Pas de corrélation
            """)
            
            st.markdown("---")
            
            col1, col2 = st.columns(2)

            with col1:
                # Scatter plot femmes vs effectif
                st.markdown("#### Relation Effectif Total vs Femmes")
                st.caption("Ce graphique montre la relation entre l'effectif total et le nombre de femmes. La ligne de tendance (OLS) indique la corrélation générale.")
                
                fig_scatter = px.scatter(
                    df_filtered, x='effectif_total', y='nb_femmes',
                    color='region', size='nb_jeunes',
                    title='Relation Effectif Total vs Femmes',
                    hover_data=['cooperative', 'prefecture', 'commune'],
                    trendline='ols',
                    labels={
                        'effectif_total': 'Effectif Total',
                        'nb_femmes': 'Nombre de Femmes',
                        'nb_jeunes': 'Nombre de Jeunes',
                        'region': 'Région'
                    }
                )
                st.plotly_chart(fig_scatter, use_container_width=True)

            with col2:
                # Matrice de corrélation
                st.markdown("#### Matrice de Corrélation")
                st.caption("Valeurs entre -1 et +1. Plus la valeur est proche de ±1, plus la corrélation est forte.")
                
                numeric_cols = ['effectif_total', 'nb_femmes', 'nb_jeunes', 'nb_handicap']
                corr_matrix = df_filtered[numeric_cols].corr()

                fig_corr = px.imshow(
                    corr_matrix,
                    text_auto='.2f',
                    title='Matrice de Corrélation',
                    color_continuous_scale='RdBu_r',
                    labels=dict(
                        x="Variables",
                        y="Variables",
                        color="Corrélation"
                    ),
                    aspect="auto"
                )
                fig_corr.update_xaxes(side="bottom")
                st.plotly_chart(fig_corr, use_container_width=True)
                
                # Interprétation automatique
                st.info(f"""
                **Interprétation rapide :**
                - Corrélation Effectif/Femmes : {corr_matrix.loc['effectif_total', 'nb_femmes']:.2f}
                - Corrélation Effectif/Jeunes : {corr_matrix.loc['effectif_total', 'nb_jeunes']:.2f}
                - Corrélation Femmes/Jeunes : {corr_matrix.loc['nb_femmes', 'nb_jeunes']:.2f}
                """)

            # Scatter matrix
            st.markdown("---")
            st.markdown("#### Matrice de Dispersion")
            st.caption("Visualisation croisée de toutes les variables numériques. Chaque point représente une coopérative.")
            
            fig_matrix = px.scatter_matrix(
                df_filtered[numeric_cols + ['region']],
                dimensions=numeric_cols,
                color='region',
                title='Matrice de Dispersion',
                labels={
                    'effectif_total': 'Effectif',
                    'nb_femmes': 'Femmes',
                    'nb_jeunes': 'Jeunes',
                    'nb_handicap': 'Handicap'
                }
            )
            fig_matrix.update_layout(height=600)
            st.plotly_chart(fig_matrix, use_container_width=True)

        with analysis_tab3:
            st.markdown("""
            ### Guide d'interprétation des indicateurs
            
            **Jauges (Gauges) :** Affichent les taux en pourcentage avec des zones de performance :
            - 🔴 **0-30%** : Performance faible (zone rouge/orange clair)
            - 🟠 **30-60%** : Performance moyenne (zone orange)
            - 🟢 **60-100%** : Performance élevée (zone verte)
            
            **Delta :** La flèche indique si le taux est au-dessus (↑) ou en-dessous (↓) de la référence (50%)
            
            **Graphique Radar :** Compare les performances de chaque région sur 5 critères. Plus la zone colorée est grande, meilleure est la performance globale.
            """)
            
            st.markdown("---")
            
            col1, col2, col3 = st.columns(3)

            # Calcul des indicateurs
            total_coop = len(df_filtered)

            with col1:
                # Taux d'immatriculation
                immat_oui = len(df_filtered[df_filtered['immatricule'] == 'Oui'])
                taux_immat = immat_oui / total_coop * 100 if total_coop > 0 else 0

                fig_gauge1 = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=taux_immat,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Taux d'Immatriculation (%)"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#27ae60"},
                        'steps': [
                            {'range': [0, 30], 'color': "#fee0d2"},
                            {'range': [30, 60], 'color': "#fdae6b"},
                            {'range': [60, 100], 'color': "#a1d99b"}
                        ],
                        'threshold': {'line': {'color': "red", 'width': 4}, 'thickness': 0.75, 'value': 80}
                    }
                ))
                st.plotly_chart(fig_gauge1, use_container_width=True)
                
                # Explication
                if taux_immat >= 60:
                    st.success(f"✓ Bon taux : {immat_oui}/{total_coop} coopératives immatriculées")
                elif taux_immat >= 30:
                    st.warning(f"⚠ Taux moyen : {immat_oui}/{total_coop} coopératives immatriculées")
                else:
                    st.error(f"✗ Taux faible : {immat_oui}/{total_coop} coopératives immatriculées")

            with col2:
                # Taux d'engagement
                engage_oui = len(df_filtered[df_filtered['engagement_agroeco'] == 'Oui'])
                taux_engage = engage_oui / total_coop * 100 if total_coop > 0 else 0

                fig_gauge2 = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=taux_engage,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Engagement Agroécologique (%)"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#3498db"},
                        'steps': [
                            {'range': [0, 30], 'color': "#fee0d2"},
                            {'range': [30, 60], 'color': "#fdae6b"},
                            {'range': [60, 100], 'color': "#a1d99b"}
                        ]
                    }
                ))
                st.plotly_chart(fig_gauge2, use_container_width=True)
                
                # Explication
                if taux_engage >= 60:
                    st.success(f"✓ Bon engagement : {engage_oui}/{total_coop} coopératives")
                elif taux_engage >= 30:
                    st.warning(f"⚠ Engagement moyen : {engage_oui}/{total_coop} coopératives")
                else:
                    st.error(f"✗ Engagement faible : {engage_oui}/{total_coop} coopératives")

            with col3:
                # Taux restitution
                restit_oui = len(df_filtered[df_filtered['restitution_formation'] == 'Oui'])
                taux_restit = restit_oui / total_coop * 100 if total_coop > 0 else 0

                fig_gauge3 = go.Figure(go.Indicator(
                    mode="gauge+number+delta",
                    value=taux_restit,
                    domain={'x': [0, 1], 'y': [0, 1]},
                    title={'text': "Restitution Formation (%)"},
                    delta={'reference': 50},
                    gauge={
                        'axis': {'range': [0, 100]},
                        'bar': {'color': "#9b59b6"},
                        'steps': [
                            {'range': [0, 30], 'color': "#fee0d2"},
                            {'range': [30, 60], 'color': "#fdae6b"},
                            {'range': [60, 100], 'color': "#a1d99b"}
                        ]
                    }
                ))
                st.plotly_chart(fig_gauge3, use_container_width=True)
                
                # Explication
                if taux_restit >= 60:
                    st.success(f"✓ Bonne restitution : {restit_oui}/{total_coop} coopératives")
                elif taux_restit >= 30:
                    st.warning(f"⚠ Restitution moyenne : {restit_oui}/{total_coop} coopératives")
                else:
                    st.error(f"✗ Restitution faible : {restit_oui}/{total_coop} coopératives")

            # Graphique radar par région
            st.markdown("---")
            st.markdown("#### Performance Comparative par Région")
            st.caption("Le graphique radar permet de comparer visuellement les 5 indicateurs clés pour chaque région. Une forme plus large indique une meilleure performance globale.")
            
            regions_list = df_filtered['region'].unique().tolist()
            if len(regions_list) > 0:
                radar_data = []
                for region in regions_list:
                    region_df = df_filtered[df_filtered['region'] == region]
                    n = len(region_df) if len(region_df) > 0 else 1
                    radar_data.append({
                        'region': region,
                        'Immatriculation': len(region_df[region_df['immatricule'] == 'Oui']) / n * 100,
                        'Engagement': len(region_df[region_df['engagement_agroeco'] == 'Oui']) / n * 100,
                        'Restitution': len(region_df[region_df['restitution_formation'] == 'Oui']) / n * 100,
                        'Parcelle': len(region_df[region_df['parcelle_choisie'] == 'Oui']) / n * 100,
                        'Production CS': len(region_df[region_df['production_contre_saison'] == 'Oui']) / n * 100
                    })

                radar_df = pd.DataFrame(radar_data)

                fig_radar = go.Figure()
                categories = ['Immatriculation', 'Engagement', 'Restitution', 'Parcelle', 'Production CS']

                colors = ['#e74c3c', '#3498db', '#2ecc71', '#9b59b6', '#f39c12']
                for i, region in enumerate(radar_df['region']):
                    values = radar_df[radar_df['region'] == region][categories].values.flatten().tolist()
                    values.append(values[0])  # Close the loop
                    fig_radar.add_trace(go.Scatterpolar(
                        r=values,
                        theta=categories + [categories[0]],
                        fill='toself',
                        name=region,
                        line_color=colors[i % len(colors)]
                    ))

                fig_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                    showlegend=True,
                    title='Performance par Région (Graphique Radar)',
                    height=500
                )
                st.plotly_chart(fig_radar, use_container_width=True)
                
                # Tableau récapitulatif
                st.markdown("#### Tableau Récapitulatif des Performances")
                radar_df_display = radar_df.copy()
                for col in categories:
                    radar_df_display[col] = radar_df_display[col].apply(lambda x: f"{x:.1f}%")
                st.dataframe(radar_df_display, use_container_width=True, hide_index=True)

        with analysis_tab4:
            # Statistiques par CRP
            st.subheader("Performance par CRP")

            crp_stats = df_filtered.groupby('crp').agg({
                'cooperative': 'count',
                'effectif_total': 'sum',
                'nb_femmes': 'sum',
                'region': lambda x: list(x.unique())
            }).rename(columns={'cooperative': 'nb_visites'}).reset_index()

            fig_crp = px.bar(
                crp_stats.sort_values('nb_visites', ascending=True),
                y='crp', x='nb_visites',
                orientation='h',
                title='Nombre de visites par CRP',
                color='nb_visites',
                color_continuous_scale='Viridis'
            )
            fig_crp.update_layout(height=400)
            st.plotly_chart(fig_crp, use_container_width=True)

            # Sunburst chart - Filtrer les données avec valeurs complètes
            # Plotly Sunburst ne peut pas gérer les valeurs None dans la hiérarchie
            df_sunburst = df_filtered.dropna(subset=['region', 'prefecture', 'commune', 'cooperative']).copy()
            
            if len(df_sunburst) > 0:
                fig_sunburst = px.sunburst(
                    df_sunburst,
                    path=['region', 'prefecture', 'commune', 'cooperative'],
                    values='effectif_total',
                    title=f'Hiérarchie Région > Préfecture > Commune > Coopérative (par effectif)\n{len(df_sunburst)} coopératives avec données complètes'
                )
                fig_sunburst.update_layout(height=600)
                st.plotly_chart(fig_sunburst, use_container_width=True)
                
                # Afficher un message si des données ont été exclues
                excluded = len(df_filtered) - len(df_sunburst)
                if excluded > 0:
                    st.info(f"{excluded} coopérative(s) exclue(s) du graphique en raison de données géographiques incomplètes (préfecture ou commune manquante).")
            else:
                st.warning("Aucune coopérative avec données géographiques complètes pour afficher le graphique Sunburst.")

    # =====================================================
    # TAB 4: MARCHÉ AGROÉCOLOGIQUE
    # =====================================================
    with tab4:
        st.subheader("Marché Agroécologique - Analyse Prédictive")
        
        st.markdown("""
        Cette section utilise des techniques avancées de data science pour identifier les coopératives 
        à fort potentiel pour intégrer un marché agroécologique et analyser les cultures dominantes.
        """)
        
        # Charger toutes les colonnes nécessaires
        df_full = pd.read_excel('MISSION_DE_SUIVI_cleaned.xlsx')
        
        # =====================================================
        # SECTION 1: SCORING DES COOPÉRATIVES
        # =====================================================
        st.markdown("---")
        st.markdown("### Top 10 Coopératives à Fort Potentiel")
        
        # Créer un score de potentiel basé sur plusieurs critères
        df_score = df_filtered.copy()
        
        # Critère 1: Effectif (normalisé 0-100)
        if 'effectif_total' in df_score.columns:
            df_score['score_effectif'] = (df_score['effectif_total'] / df_score['effectif_total'].max() * 100).fillna(0)
        else:
            df_score['score_effectif'] = 0
        
        # Critère 2: Engagement agroécologique (Oui=100, Non=0)
        if 'engagement_agroeco' in df_score.columns:
            df_score['score_engagement'] = df_score['engagement_agroeco'].apply(lambda x: 100 if x == 'Oui' else 0)
        else:
            df_score['score_engagement'] = 0
        
        # Critère 3: Immatriculation (Oui=100, Non=0)
        if 'immatricule' in df_score.columns:
            df_score['score_immat'] = df_score['immatricule'].apply(lambda x: 100 if x == 'Oui' else 0)
        else:
            df_score['score_immat'] = 0
        
        # Critère 4: Restitution formation (Oui=100, Non=0)
        if 'restitution_formation' in df_score.columns:
            df_score['score_formation'] = df_score['restitution_formation'].apply(lambda x: 100 if x == 'Oui' else 0)
        else:
            df_score['score_formation'] = 0
        
        # Critère 5: Parcelle choisie (Oui=100, Non=0)
        if 'parcelle_choisie' in df_score.columns:
            df_score['score_parcelle'] = df_score['parcelle_choisie'].apply(lambda x: 100 if x == 'Oui' else 0)
        else:
            df_score['score_parcelle'] = 0
        
        # Critère 6: Production contre-saison (Oui=100, Non=0)
        if 'production_contre_saison' in df_score.columns:
            df_score['score_production'] = df_score['production_contre_saison'].apply(lambda x: 100 if x == 'Oui' else 0)
        else:
            df_score['score_production'] = 0
        
        # Critère 7: Taux de féminisation (bonus si >50%)
        if 'nb_femmes' in df_score.columns and 'effectif_total' in df_score.columns:
            df_score['taux_femmes'] = (df_score['nb_femmes'] / df_score['effectif_total'] * 100).fillna(0)
            df_score['score_femmes'] = df_score['taux_femmes'].apply(lambda x: 100 if x > 50 else x * 2)
        else:
            df_score['score_femmes'] = 0
        
        # Critère 8: Taux de jeunes (bonus si >30%)
        if 'nb_jeunes' in df_score.columns and 'effectif_total' in df_score.columns:
            df_score['taux_jeunes'] = (df_score['nb_jeunes'] / df_score['effectif_total'] * 100).fillna(0)
            df_score['score_jeunes'] = df_score['taux_jeunes'].apply(lambda x: 100 if x > 30 else x * 3.33)
        else:
            df_score['score_jeunes'] = 0
        
        # Score global (moyenne pondérée)
        weights = {
            'score_effectif': 0.15,
            'score_engagement': 0.20,
            'score_immat': 0.15,
            'score_formation': 0.15,
            'score_parcelle': 0.10,
            'score_production': 0.10,
            'score_femmes': 0.075,
            'score_jeunes': 0.075
        }
        
        df_score['score_total'] = sum(df_score[col] * weight for col, weight in weights.items())
        
        # Top 10 coopératives PAR RÉGION
        st.markdown("#### 🌍 Sélection par Région")
        
        # Créer un dictionnaire pour stocker les top 10 par région
        top10_by_region = {}
        all_top_coops = []
        
        for region in sorted(df_score['region'].unique()):
            region_data = df_score[df_score['region'] == region]
            top10_region = region_data.nlargest(10, 'score_total')
            top10_by_region[region] = top10_region
            
            # Ajouter au tableau global avec le rang par région
            for idx, (_, row) in enumerate(top10_region.iterrows(), 1):
                all_top_coops.append({
                    'Région': region,
                    'Rang': idx,
                    'Coopérative': row['cooperative'],
                    'Préfecture': row['prefecture'],
                    'Commune': row.get('commune', 'N/A'),
                    'Effectif': int(row['effectif_total']),
                    'Score': round(row['score_total'], 1)
                })
        
        # Créer le DataFrame global
        df_all_tops = pd.DataFrame(all_top_coops)
        
        # Affichage avec onglets par région
        st.markdown("---")
        
        # Créer des onglets pour chaque région
        region_tabs = st.tabs([f"{region}" for region in sorted(df_score['region'].unique())] + ["Toutes les Régions"])
        
        for idx, region in enumerate(sorted(df_score['region'].unique())):
            with region_tabs[idx]:
                top10_region = top10_by_region[region]
                
                col_left, col_right = st.columns([1, 1])
                
                with col_left:
                    st.markdown(f"#### Top 10 - {region}")
                    
                    top10_display = top10_region[[
                        'cooperative', 'prefecture', 'commune', 'effectif_total', 
                        'score_total'
                    ]].copy()
                    top10_display.columns = ['Coopérative', 'Préfecture', 'Commune', 'Effectif', 'Score']
                    top10_display['Score'] = top10_display['Score'].round(1)
                    top10_display['Rang'] = range(1, len(top10_display) + 1)
                    top10_display = top10_display[['Rang', 'Coopérative', 'Préfecture', 'Commune', 'Effectif', 'Score']]
                    
                    st.dataframe(top10_display, use_container_width=True, hide_index=True)
                    
                    # Statistiques de la région
                    st.markdown("**Statistiques de la région:**")
                    region_stats = df_score[df_score['region'] == region]
                    col_stat1, col_stat2, col_stat3 = st.columns(3)
                    with col_stat1:
                        st.metric("Coopératives", len(region_stats))
                    with col_stat2:
                        st.metric("Score Moyen", f"{region_stats['score_total'].mean():.1f}")
                    with col_stat3:
                        st.metric("Effectif Total", f"{int(region_stats['effectif_total'].sum()):,}")
                
                with col_right:
                    st.markdown(f"#### Scores - {region}")
                    
                    fig_region = px.bar(
                        top10_display,
                        x='Score',
                        y='Coopérative',
                        orientation='h',
                        color='Score',
                        color_continuous_scale='Viridis',
                        title=f'Score de Potentiel - {region}',
                        labels={'Score': 'Score de Potentiel'}
                    )
                    fig_region.update_layout(height=400, yaxis={'categoryorder': 'total ascending'})
                    st.plotly_chart(fig_region, use_container_width=True)
                
                # Profils détaillés pour cette région
                st.markdown(f"#### 📋 Profils Détaillés - Top 5 {region}")
                
                for idx_coop, (_, row) in enumerate(top10_region.head(5).iterrows(), 1):
                    with st.expander(f"#{idx_coop} - {row['cooperative']}"):
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.metric("Score Total", f"{row['score_total']:.1f}/100")
                            st.metric("Effectif", int(row['effectif_total']))
                            st.metric("Femmes", f"{int(row['nb_femmes'])} ({row.get('taux_femmes', 0):.1f}%)")
                        
                        with col2:
                            st.metric("Jeunes", f"{int(row['nb_jeunes'])} ({row.get('taux_jeunes', 0):.1f}%)")
                            st.write(f"**Préfecture:** {row['prefecture']}")
                            st.write(f"**Commune:** {row.get('commune', 'N/A')}")
                        
                        with col3:
                            st.write(f"**Engagement AE:** {row.get('engagement_agroeco', 'N/A')}")
                            st.write(f"**Immatriculé:** {row.get('immatricule', 'N/A')}")
                            st.write(f"**Formation:** {row.get('restitution_formation', 'N/A')}")
                        
                        # Graphique radar des scores
                        scores_detail = {
                            'Effectif': row['score_effectif'],
                            'Engagement': row['score_engagement'],
                            'Immatriculation': row['score_immat'],
                            'Formation': row['score_formation'],
                            'Parcelle': row['score_parcelle'],
                            'Production CS': row['score_production'],
                            'Féminisation': row['score_femmes'],
                            'Jeunes': row['score_jeunes']
                        }
                        
                        fig_radar = go.Figure(data=go.Scatterpolar(
                            r=list(scores_detail.values()),
                            theta=list(scores_detail.keys()),
                            fill='toself',
                            name=row['cooperative']
                        ))
                        fig_radar.update_layout(
                            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                            showlegend=False,
                            height=300,
                            title="Profil de Potentiel"
                        )
                        st.plotly_chart(fig_radar, use_container_width=True)
        
        # Onglet "Toutes les Régions"
        with region_tabs[-1]:
            st.markdown("#### 🌍 Top 10 de Toutes les Régions")
            st.markdown(f"**Total: {len(df_all_tops)} coopératives** (10 par région)")
            
            # Filtres
            col_filter1, col_filter2 = st.columns(2)
            with col_filter1:
                selected_regions_filter = st.multiselect(
                    "Filtrer par région(s)",
                    options=sorted(df_score['region'].unique()),
                    default=None
                )
            
            with col_filter2:
                min_score = st.slider("Score minimum", 0, 100, 0)
            
            # Appliquer les filtres
            df_display_all = df_all_tops.copy()
            if selected_regions_filter:
                df_display_all = df_display_all[df_display_all['Région'].isin(selected_regions_filter)]
            df_display_all = df_display_all[df_display_all['Score'] >= min_score]
            
            # Afficher le tableau
            st.dataframe(df_display_all, use_container_width=True, hide_index=True, height=600)
            
            # Graphique de comparaison
            st.markdown("#### Comparaison des Scores par Région")
            
            fig_comparison = px.box(
                df_all_tops,
                x='Région',
                y='Score',
                color='Région',
                title='Distribution des Scores par Région',
                labels={'Score': 'Score de Potentiel'}
            )
            fig_comparison.update_layout(height=400, showlegend=False)
            st.plotly_chart(fig_comparison, use_container_width=True)
            
            # Statistiques globales
            st.markdown("#### Statistiques Globales")
            col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
            
            with col_stat1:
                st.metric("Total Coopératives", len(df_all_tops))
            with col_stat2:
                st.metric("Score Moyen", f"{df_all_tops['Score'].mean():.1f}")
            with col_stat3:
                st.metric("Score Max", f"{df_all_tops['Score'].max():.1f}")
            with col_stat4:
                st.metric("Score Min", f"{df_all_tops['Score'].min():.1f}")

        
        # Détails des critères
        st.markdown("---")
        st.markdown("#### Méthodologie de Scoring")
        
        with st.expander("Voir les détails des critères et pondérations"):
            st.markdown("""
            **Critères et Pondérations:**
            
            1. **Engagement Agroécologique (20%)** - Coopératives ayant pris un engagement ferme
            2. **Effectif Total (15%)** - Taille de la coopérative (capacité de production)
            3. **Immatriculation (15%)** - Structure légale formalisée
            4. **Restitution Formation (15%)** - Transfert de connaissances effectué
            5. **Parcelle d'Apprentissage (10%)** - Infrastructure de formation disponible
            6. **Production Contre-Saison (10%)** - Capacité de production diversifiée
            7. **Taux de Féminisation (7.5%)** - Inclusion des femmes (>50% = bonus)
            8. **Taux de Jeunes (7.5%)** - Dynamisme et relève assurée (>30% = bonus)
            
            **Score Total:** Moyenne pondérée de 0 à 100
            
            **Interprétation:**
            - 90-100 : Excellent potentiel - Prêt pour le marché
            - 70-89 : Bon potentiel - Accompagnement léger
            - 50-69 : Potentiel moyen - Renforcement nécessaire
            - <50 : Potentiel faible - Formation intensive
            """)
        
        # =====================================================
        # SECTION 2: ANALYSE DES CULTURES
        # =====================================================
        st.markdown("---")
        st.markdown("### Cultures Dominantes et Tendances")
        
        # Analyser les cultures mentionnées
        culture_col = '6.6. Si oui, quelles sont les cultures que vous voudriez produire en contre-saison ? '
        
        if culture_col in df_full.columns:
            # Extraire toutes les cultures mentionnées
            all_cultures = []
            for val in df_full[culture_col].dropna():
                # Séparer par virgules et nettoyer
                cultures = str(val).split(',')
                for culture in cultures:
                    culture_clean = culture.strip().upper()
                    if culture_clean and len(culture_clean) > 2:
                        all_cultures.append(culture_clean)
            
            # Compter les occurrences
            from collections import Counter
            culture_counts = Counter(all_cultures)
            
            # Créer un DataFrame
            df_cultures = pd.DataFrame(culture_counts.most_common(20), columns=['Culture', 'Nombre'])
            
            col_cult_left, col_cult_right = st.columns([1, 1])
            
            with col_cult_left:
                st.markdown("#### Top 20 Cultures Mentionnées")
                st.dataframe(df_cultures, use_container_width=True, hide_index=True)
            
            with col_cult_right:
                st.markdown("#### Visualisation")
                
                fig_cultures = px.bar(
                    df_cultures.head(15),
                    x='Nombre',
                    y='Culture',
                    orientation='h',
                    color='Nombre',
                    color_continuous_scale='Greens',
                    title='Top 15 Cultures les Plus Populaires'
                )
                fig_cultures.update_layout(height=500, yaxis={'categoryorder': 'total ascending'})
                st.plotly_chart(fig_cultures, use_container_width=True)
            
            # Nuage de mots
            st.markdown("#### Nuage de Cultures")
            
            # Créer un graphique de bulles
            df_cultures_top = df_cultures.head(30)
            fig_bubble = px.scatter(
                df_cultures_top,
                x=range(len(df_cultures_top)),
                y=[1] * len(df_cultures_top),
                size='Nombre',
                text='Culture',
                color='Nombre',
                color_continuous_scale='Viridis',
                title='Importance Relative des Cultures (taille = fréquence)'
            )
            fig_bubble.update_traces(textposition='middle center', textfont_size=10)
            fig_bubble.update_layout(
                height=300,
                showlegend=False,
                xaxis={'visible': False},
                yaxis={'visible': False}
            )
            st.plotly_chart(fig_bubble, use_container_width=True)
            
            # Analyse par région
            st.markdown("#### Cultures par Région")
            
            # Créer un mapping des coopératives vers les régions depuis df_filtered
            coop_region_map = df_filtered[['cooperative', 'region']].drop_duplicates().set_index('cooperative')['region'].to_dict()
            
            # Ajouter la région à df_full en utilisant le nom original de la colonne
            coop_col_original = '3.1. Nom de la coopérative'
            if coop_col_original in df_full.columns:
                df_full_merged = df_full.copy()
                df_full_merged['region'] = df_full_merged[coop_col_original].map(coop_region_map)
            else:
                df_full_merged = df_full.copy()
                df_full_merged['region'] = None
            
            # Analyser par région
            region_cultures = {}
            for region in df_full_merged['region'].dropna().unique():
                region_data = df_full_merged[df_full_merged['region'] == region]
                region_cult = []
                for val in region_data[culture_col].dropna():
                    cultures = str(val).split(',')
                    for culture in cultures:
                        culture_clean = culture.strip().upper()
                        if culture_clean and len(culture_clean) > 2:
                            region_cult.append(culture_clean)
                
                if region_cult:
                    region_counts = Counter(region_cult)
                    region_cultures[region] = region_counts.most_common(5)
            
            # Afficher par région
            cols_regions = st.columns(len(region_cultures))
            for idx, (region, cultures) in enumerate(sorted(region_cultures.items())):
                with cols_regions[idx]:
                    st.markdown(f"**{region}**")
                    for culture, count in cultures:
                        st.write(f"• {culture}: {count}")
        
        else:
            st.warning("Colonne des cultures non trouvée dans les données")
        
        # =====================================================
        # SECTION 3: RECOMMANDATIONS
        # =====================================================
        st.markdown("---")
        st.markdown("### Recommandations Stratégiques")
        
        col_rec1, col_rec2 = st.columns(2)
        
        with col_rec1:
            st.markdown("#### Pour le Marché Agroécologique")
            st.markdown("""
            **Actions Prioritaires:**
            
            1. **Accompagner les Top 10** identifiées avec un score >70
            2. **Renforcer l'engagement** des coopératives avec score 50-70
            3. **Former** les coopératives avec faible score sur les pratiques AE
            4. **Créer des groupements** par région pour mutualiser les ressources
            5. **Développer des filières** pour les cultures dominantes
            """)
        
        with col_rec2:
            st.markdown("#### Pour les Cultures")
            st.markdown("""
            **Opportunités Identifiées:**
            
            1. **Tomates** - Culture la plus demandée, fort potentiel commercial
            2. **Piment** - Demande élevée, bonne valeur ajoutée
            3. **Gombo** - Culture traditionnelle, marché stable
            4. **Choux/Laitue** - Cultures maraîchères à développer
            5. **Diversification** - Encourager les associations de cultures
            """)
        
        # Export des résultats
        st.markdown("---")
        st.markdown("### 📥 Export des Résultats")
        
        st.markdown("Téléchargez les résultats de l'analyse pour vos rapports et présentations.")
        
        col_exp1, col_exp2, col_exp3 = st.columns(3)
        
        with col_exp1:
            # Export Top 10 par région en Excel
            st.markdown("#### Top 10 par Région")
            
            # Créer un fichier Excel avec plusieurs feuilles
            output = io.BytesIO()
            with pd.ExcelWriter(output, engine='openpyxl') as writer:
                # Feuille "Toutes les Régions"
                df_all_tops.to_excel(writer, sheet_name='Toutes les Régions', index=False)
                
                # Une feuille par région
                for region in sorted(df_score['region'].unique()):
                    region_tops = df_all_tops[df_all_tops['Région'] == region]
                    region_tops.to_excel(writer, sheet_name=region[:30], index=False)  # Limite de 31 caractères
            
            excel_data = output.getvalue()
            
            st.download_button(
                label="📥 Télécharger Excel (Top 10 par Région)",
                data=excel_data,
                file_name="top10_cooperatives_par_region.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            st.info(f"📄 {len(df_all_tops)} coopératives • {len(df_score['region'].unique())} régions")
        
        with col_exp2:
            # Export CSV simple
            st.markdown("#### 📄 Format CSV")
            
            csv_all_tops = df_all_tops.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Télécharger CSV (Toutes Régions)",
                data=csv_all_tops,
                file_name="top10_cooperatives_toutes_regions.csv",
                mime="text/csv"
            )
            
            st.info("Format simple pour analyse rapide")
        
        with col_exp3:
            # Export Cultures
            st.markdown("#### Analyse Cultures")
            
            if 'df_cultures' in locals():
                csv_cultures = df_cultures.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Télécharger CSV (Cultures)",
                    data=csv_cultures,
                    file_name="cultures_dominantes.csv",
                    mime="text/csv"
                )
                
                st.info(f"📄 {len(df_cultures)} cultures identifiées")
            else:
                st.warning("Données cultures non disponibles")

    # =====================================================
    # TAB 5: DONNÉES
    # =====================================================
    with tab5:
        st.subheader("Donnees Filtrees")

        # Colonnes à afficher
        display_cols = ['cooperative', 'region', 'prefecture', 'commune', 'village', 'effectif_total',
                       'nb_femmes', 'nb_jeunes', 'immatricule', 'engagement_agroeco',
                       'restitution_formation', 'parcelle_choisie', 'production_contre_saison', 'crp']

        available_cols = [col for col in display_cols if col in df_filtered.columns]

        # Recherche
        search_term = st.text_input("Rechercher une cooperative", "")

        if search_term:
            df_display = df_filtered[df_filtered['cooperative'].str.contains(search_term, case=False, na=False)]
        else:
            df_display = df_filtered

        st.dataframe(
            df_display[available_cols],
            use_container_width=True,
            height=500
        )

        # Export
        col1, col2 = st.columns(2)
        with col1:
            csv = df_display[available_cols].to_csv(index=False).encode('utf-8')
            st.download_button(
                "Telecharger CSV",
                csv,
                "cooperatives_filtrees.csv",
                "text/csv"
            )

        with col2:
            # Statistiques résumées
            st.markdown("**Statistiques Résumées:**")
            st.json({
                "Total coopératives": len(df_display),
                "Effectif total": int(df_display['effectif_total'].sum()),
                "Femmes": int(df_display['nb_femmes'].sum()),
                "Jeunes": int(df_display['nb_jeunes'].sum()),
                "Régions": df_display['region'].nunique(),
                "Préfectures": df_display['prefecture'].nunique(),
                "Communes": df_display['commune'].nunique()
            })

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 20px; background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                border-radius: 10px; margin-top: 30px;">
        <p style="margin: 0; color: #2c3e50; font-size: 14px; font-weight: bold;">
            Dashboard SIG - Mission de Suivi des Coopératives Agricoles ProSMAT
        </p>
        <p style="margin: 5px 0; color: #7f8c8d; font-size: 12px;">
            Données GADM41 | Développé avec Streamlit, Folium, GeoPandas & Plotly
        </p>
        <div style="margin-top: 15px; padding: 15px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                    border-radius: 8px; color: white;">
            <p style="margin: 0; font-size: 13px; font-weight: bold;">Développé par TATCHIDA Louis</p>
            <p style="margin: 5px 0; font-size: 11px;">
                MSc Agronomie | MSc Ingénierie Financière adaptée à l'Agriculture | Data Analyst
            </p>
            <p style="margin: 5px 0; font-size: 10px; opacity: 0.9;">
                © 2025 - Tous droits réservés
            </p>
        </div>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
