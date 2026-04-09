"""
Configuration des styles et symboles pour les cartes SIG
"""

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.patches as mpatches

# =====================================================
# CONFIGURATION DES COULEURS
# =====================================================

REGION_COLORS = {
    'Centre': '#e74c3c',
    'Kara': '#3498db',
    'Savanes': '#2ecc71',
    'Plateaux': '#9b59b6',
    'Maritime': '#f39c12'
}

STATUS_COLORS = {
    'oui': '#27ae60',      # Vert pour positif
    'non': '#e74c3c',      # Rouge pour négatif
    'non_renseigne': '#95a5a6'  # Gris pour non renseigné
}

CHOROPLETH_CMAPS = {
    'cooperatives': 'Reds',
    'effectif': 'Blues',
    'femmes': 'Purples',
    'jeunes': 'Greens',
    'handicap': 'Oranges',
    'prefecture': 'YlOrRd'
}

# =====================================================
# CONFIGURATION DES MARQUEURS
# =====================================================

MARKERS = {
    'oui': {
        'marker': 'o',           # Cercle
        's': 80,                 # Taille (s au lieu de size)
        'alpha': 0.8,
        'edgecolor': 'white',
        'linewidth': 1.5
    },
    'non': {
        'marker': 'X',           # Croix
        's': 80,                 # Taille (s au lieu de size)
        'alpha': 0.8,
        'edgecolor': 'white',
        'linewidth': 1.5
    },
    'non_renseigne': {
        'marker': 's',           # Carré
        's': 60,                 # Taille (s au lieu de size)
        'alpha': 0.6,
        'edgecolor': 'white',
        'linewidth': 1
    }
}

# =====================================================
# CONFIGURATION DES LABELS
# =====================================================

LABELS = {
    'immatriculation': {
        'oui': 'Immatricule',
        'non': 'Non immatricule',
        'non_renseigne': 'Non renseigne'
    },
    'engagement': {
        'oui': 'Engage',
        'non': 'Non engage',
        'non_renseigne': 'Non renseigne'
    },
    'parcelle': {
        'oui': 'Parcelle choisie',
        'non': 'Pas de parcelle',
        'non_renseigne': 'Non renseigne'
    },
    'materiel': {
        'oui': 'Materiel recu',
        'non': 'Pas de materiel',
        'non_renseigne': 'Non renseigne'
    }
}

# =====================================================
# CONFIGURATION DES TITRES
# =====================================================

TITLES = {
    'localisation': 'Localisation des Cooperatives par Region',
    'choropleth_coop': 'Nombre de Cooperatives par Region',
    'choropleth_effectif': 'Effectif Total des Membres par Region',
    'choropleth_femmes': 'Nombre de Femmes par Region',
    'choropleth_jeunes': 'Nombre de Jeunes (<35 ans) par Region',
    'choropleth_handicap': 'Nombre de Personnes Handicapees par Region',
    'prefecture_detail': 'Nombre de Cooperatives par Prefecture',
    'immatriculation': "Statut d'Immatriculation des Cooperatives",
    'engagement': 'Engagement Agroecologique des Cooperatives',
    'parcelle': "Statut de Choix de Parcelle d'Apprentissage",
    'materiel': "Reception de Materiel de Production d'Intrants",
    'taille_effectif': 'Cooperatives (taille = effectif total)',
    'zoom_region': 'Zoom sur la Region'
}

SUBTITLES = {
    'localisation': 'Repartition geographique',
    'choropleth_coop': 'Repartition geographique',
    'choropleth_effectif': 'Nombre de personnes dans les cooperatives',
    'choropleth_femmes': 'Membres feminins des cooperatives',
    'choropleth_jeunes': 'Membres jeunes des cooperatives',
    'choropleth_handicap': 'Membres vivant avec un handicap',
    'immatriculation': 'O = Immatricule, X = Non immatricule',
    'engagement': 'O = Engage, X = Non engage',
    'parcelle': 'O = Parcelle choisie, X = Pas de parcelle',
    'materiel': 'O = Materiel recu, X = Pas de materiel'
}

# =====================================================
# CONFIGURATION MATPLOTLIB
# =====================================================

def configure_matplotlib():
    """Configurer les paramètres matplotlib pour les cartes"""
    plt.switch_backend("Agg")
    plt.style.use("seaborn-v0_8")
    plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]
    plt.rcParams["axes.unicode_minus"] = False
    plt.rcParams["figure.facecolor"] = "white"
    plt.rcParams["axes.facecolor"] = "white"

# =====================================================
# FONCTIONS UTILITAIRES
# =====================================================

def get_text_color(value, mean_value):
    """Retourner la couleur du texte selon l'intensité"""
    return 'white' if value > mean_value else 'black'

def create_annotation_box(text_color='black'):
    """Créer un style de boîte pour les annotations"""
    return dict(
        boxstyle='round,pad=0.3',
        facecolor='white',
        alpha=0.7,
        edgecolor='none'
    )

def add_region_labels(ax, gdf_regions, alpha=0.7):
    """Ajouter les noms des régions sur la carte"""
    for idx, row in gdf_regions.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row['NAME_1'],
            xy=(centroid.x, centroid.y),
            ha='center',
            fontsize=9,
            style='italic',
            color='#555',
            alpha=alpha
        )

def add_prefecture_boundaries(ax, gdf_prefectures, alpha=0.5):
    """Ajouter les limites des préfectures"""
    gdf_prefectures.boundary.plot(
        ax=ax,
        color='gray',
        linewidth=0.3,
        linestyle='--',
        alpha=alpha
    )

def format_number(value):
    """Formater un nombre avec séparateur de milliers"""
    return f"{int(value):,}".replace(',', ' ')

def create_legend_elements(map_type, counts):
    """Créer les éléments de légende personnalisés"""
    labels = LABELS.get(map_type, {})
    elements = []
    
    if 'oui' in counts and counts['oui'] > 0:
        elements.append(mpatches.Patch(
            color=STATUS_COLORS['oui'],
            label=f"{labels.get('oui', 'Oui')} ({counts['oui']})"
        ))
    
    if 'non' in counts and counts['non'] > 0:
        elements.append(mpatches.Patch(
            color=STATUS_COLORS['non'],
            label=f"{labels.get('non', 'Non')} ({counts['non']})"
        ))
    
    if 'non_renseigne' in counts and counts['non_renseigne'] > 0:
        elements.append(mpatches.Patch(
            color=STATUS_COLORS['non_renseigne'],
            label=f"{labels.get('non_renseigne', 'Non renseigne')} ({counts['non_renseigne']})"
        ))
    
    return elements

def get_map_title(map_type, selected_region=None, count=None):
    """Obtenir le titre complet de la carte"""
    title = TITLES.get(map_type, 'Carte')
    
    if selected_region:
        title = f"{title} {selected_region}"
    
    if count is not None:
        title = f"{title}\n({count} cooperatives)"
    
    subtitle = SUBTITLES.get(map_type)
    if subtitle:
        title = f"{title}\n({subtitle})"
    
    return title

# =====================================================
# STYLES DE CARTES PRÉDÉFINIS
# =====================================================

def get_base_map_style():
    """Style de base pour toutes les cartes"""
    return {
        'figsize': (12, 14),
        'region_color': '#f5f5f5',
        'region_edge_color': 'black',
        'region_edge_width': 1
    }

def get_choropleth_style(cmap_name):
    """Style pour les cartes choroplèthes"""
    return {
        'cmap': CHOROPLETH_CMAPS.get(cmap_name, 'YlOrRd'),
        'edgecolor': 'black',
        'linewidth': 1,
        'legend': True,
        'legend_shrink': 0.6
    }

def get_scatter_style(status):
    """Style pour les marqueurs de points"""
    return MARKERS.get(status, MARKERS['non_renseigne'])
