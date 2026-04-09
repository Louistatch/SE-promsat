"""
Utilitaires pour améliorer les cartes SIG
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, Wedge
from matplotlib.lines import Line2D
import numpy as np

def add_scale_bar(ax, length=50, location=(0.1, 0.05)):
    """
    Ajouter une échelle à la carte
    
    Parameters:
    - ax: axes matplotlib
    - length: longueur de l'échelle en km
    - location: position (x, y) en coordonnées relatives
    """
    # Calculer la longueur en degrés (approximation: 1 degré ≈ 111 km)
    length_deg = length / 111.0
    
    x, y = location
    
    # Dessiner la barre d'échelle
    ax.plot([x, x + length_deg], [y, y], 'k-', linewidth=3, transform=ax.transData, 
            clip_on=False, zorder=1000)
    
    # Ajouter les marques
    for i in range(3):
        pos = x + (length_deg * i / 2)
        ax.plot([pos, pos], [y - 0.02, y + 0.02], 'k-', linewidth=2, 
               transform=ax.transData, clip_on=False, zorder=1000)
    
    # Ajouter le texte
    ax.text(x + length_deg/2, y - 0.08, f'{length} km', 
           ha='center', va='top', fontsize=9, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.8, edgecolor='black'),
           transform=ax.transData, zorder=1000)

def add_north_arrow(ax, location=(0.95, 0.95), size=0.05):
    """
    Ajouter une rose des vents (flèche Nord)
    
    Parameters:
    - ax: axes matplotlib
    - location: position (x, y) en coordonnées relatives (0-1)
    - size: taille de la flèche
    """
    x, y = location
    
    # Convertir en coordonnées de données
    xlim = ax.get_xlim()
    ylim = ax.get_ylim()
    x_data = xlim[0] + (xlim[1] - xlim[0]) * x
    y_data = ylim[0] + (ylim[1] - ylim[0]) * y
    
    arrow_length = (ylim[1] - ylim[0]) * size
    
    # Dessiner le cercle de fond
    circle = Circle((x_data, y_data), arrow_length * 0.4, 
                   facecolor='white', edgecolor='black', linewidth=2, 
                   alpha=0.9, zorder=1000)
    ax.add_patch(circle)
    
    # Dessiner la flèche Nord
    ax.arrow(x_data, y_data, 0, arrow_length, 
            head_width=arrow_length*0.3, head_length=arrow_length*0.3,
            fc='red', ec='black', linewidth=2, zorder=1001)
    
    # Ajouter le texte "N"
    ax.text(x_data, y_data + arrow_length * 1.3, 'N', 
           ha='center', va='center', fontsize=14, fontweight='bold',
           color='black', zorder=1002)

def add_legend_box(ax, legend_items, title="Legende", location='lower left'):
    """
    Ajouter une légende professionnelle avec boîte
    
    Parameters:
    - ax: axes matplotlib
    - legend_items: liste de tuples (label, color, marker)
    - title: titre de la légende
    - location: position de la légende
    """
    handles = []
    for item in legend_items:
        if len(item) == 2:
            label, color = item
            handles.append(mpatches.Patch(color=color, label=label))
        elif len(item) == 3:
            label, color, marker = item
            handles.append(Line2D([0], [0], marker=marker, color='w', 
                                 markerfacecolor=color, markersize=10, label=label,
                                 markeredgecolor='white', markeredgewidth=1.5))
    
    legend = ax.legend(handles=handles, title=title, loc=location,
                      frameon=True, fancybox=True, shadow=True,
                      fontsize=9, title_fontsize=10, framealpha=0.95,
                      edgecolor='black', facecolor='white')
    
    # Styliser le titre de la légende
    legend.get_title().set_fontweight('bold')
    
    return legend

def add_info_box(ax, info_text, location=(0.02, 0.98)):
    """
    Ajouter une boîte d'information
    
    Parameters:
    - ax: axes matplotlib
    - info_text: texte à afficher
    - location: position (x, y) en coordonnées relatives
    """
    ax.text(location[0], location[1], info_text,
           transform=ax.transAxes, fontsize=9,
           verticalalignment='top', horizontalalignment='left',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                    alpha=0.9, edgecolor='black', linewidth=1.5),
           zorder=1000)

def add_title_box(ax, title, subtitle=None):
    """
    Ajouter un titre professionnel avec boîte
    
    Parameters:
    - ax: axes matplotlib
    - title: titre principal
    - subtitle: sous-titre optionnel
    """
    title_text = title
    if subtitle:
        title_text += f"\n{subtitle}"
    
    ax.text(0.5, 1.02, title_text,
           transform=ax.transAxes, fontsize=14, fontweight='bold',
           verticalalignment='bottom', horizontalalignment='center',
           bbox=dict(boxstyle='round,pad=0.8', facecolor='white', 
                    alpha=0.95, edgecolor='#1e3c72', linewidth=2),
           zorder=1000)

def add_coordinates_grid(ax, interval=0.5):
    """
    Ajouter une grille de coordonnées
    
    Parameters:
    - ax: axes matplotlib
    - interval: intervalle entre les lignes de grille
    """
    ax.grid(True, linestyle='--', alpha=0.3, color='gray', linewidth=0.5)
    ax.tick_params(labelsize=8)

def add_data_source(ax, source_text="Source: ProSMAT 2025"):
    """
    Ajouter la source des données
    
    Parameters:
    - ax: axes matplotlib
    - source_text: texte de la source
    """
    ax.text(0.98, 0.02, source_text,
           transform=ax.transAxes, fontsize=8, style='italic',
           verticalalignment='bottom', horizontalalignment='right',
           color='gray', zorder=1000)

def add_statistics_box(ax, stats_dict, location=(0.02, 0.02)):
    """
    Ajouter une boîte de statistiques
    
    Parameters:
    - ax: axes matplotlib
    - stats_dict: dictionnaire de statistiques {label: value}
    - location: position (x, y) en coordonnées relatives
    """
    stats_text = "\n".join([f"{k}: {v}" for k, v in stats_dict.items()])
    
    ax.text(location[0], location[1], stats_text,
           transform=ax.transAxes, fontsize=8,
           verticalalignment='bottom', horizontalalignment='left',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='lightyellow', 
                    alpha=0.9, edgecolor='orange', linewidth=1.5),
           zorder=1000, family='monospace')
