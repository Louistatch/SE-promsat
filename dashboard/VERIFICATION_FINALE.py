"""
Script de vérification finale du Dashboard SIG ProSMAT v3.0
Vérifie que tous les fichiers nécessaires sont présents et fonctionnels
"""

import os
import sys

print("=" * 70)
print("VÉRIFICATION FINALE - Dashboard SIG ProSMAT v3.0")
print("=" * 70)

# Compteurs
total_checks = 0
passed_checks = 0
failed_checks = 0

def check(description, condition, critical=False):
    """Vérifier une condition"""
    global total_checks, passed_checks, failed_checks
    total_checks += 1
    
    if condition:
        print(f"[OK] {description}")
        passed_checks += 1
        return True
    else:
        symbol = "[ERREUR]" if critical else "[ATTENTION]"
        print(f"{symbol} {description}")
        failed_checks += 1
        if critical:
            print(f"   CRITIQUE: Ce fichier est nécessaire pour le fonctionnement!")
        return False

print("\n1. FICHIERS DE DONNÉES")
print("-" * 70)
check("MISSION_DE_SUIVI_cleaned.xlsx", os.path.exists("MISSION_DE_SUIVI_cleaned.xlsx"), critical=True)
check("gadm41_TGO.gpkg", os.path.exists("gadm41_TGO.gpkg"), critical=True)
check("logo.jfif", os.path.exists("logo.jfif"), critical=False)

print("\n2. MODULES PYTHON")
print("-" * 70)
check("dashboard_sig_streamlit.py", os.path.exists("dashboard_sig_streamlit.py"), critical=True)
check("map_styles.py", os.path.exists("map_styles.py"), critical=True)
check("map_utils.py", os.path.exists("map_utils.py"), critical=True)
check("requirements.txt", os.path.exists("requirements.txt"), critical=True)

print("\n3. FICHIERS DE TEST")
print("-" * 70)
check("test_final.py", os.path.exists("test_final.py"))
check("test_marche_top10_regions.py", os.path.exists("test_marche_top10_regions.py"))
check("test_architecture.py", os.path.exists("test_architecture.py"))
check("test_zoom_region.py", os.path.exists("test_zoom_region.py"))

print("\n4. DOCUMENTATION PRINCIPALE")
print("-" * 70)
check("LISEZ_MOI_DABORD.md", os.path.exists("LISEZ_MOI_DABORD.md"))
check("GUIDE_DEMARRAGE_RAPIDE.md", os.path.exists("GUIDE_DEMARRAGE_RAPIDE.md"))
check("README_COMPLET.md", os.path.exists("README_COMPLET.md"))
check("SYNTHESE_FINALE_V3.md", os.path.exists("SYNTHESE_FINALE_V3.md"))

print("\n5. GUIDES UTILISATEUR")
print("-" * 70)
check("GUIDE_UTILISATION_ZOOM.md", os.path.exists("GUIDE_UTILISATION_ZOOM.md"))
check("GUIDE_MARCHE_AGROECOLOGIQUE.md", os.path.exists("GUIDE_MARCHE_AGROECOLOGIQUE.md"))

print("\n6. DOCUMENTATION TECHNIQUE")
print("-" * 70)
check("CHANGELOG_V3.md", os.path.exists("CHANGELOG_V3.md"))
check("CHANGEMENTS_ARCHITECTURE.md", os.path.exists("CHANGEMENTS_ARCHITECTURE.md"))
check("AMELIORATIONS_ZOOM_REGION.md", os.path.exists("AMELIORATIONS_ZOOM_REGION.md"))
check("CORRECTIONS_FINALES.md", os.path.exists("CORRECTIONS_FINALES.md"))

print("\n7. FICHIERS GÉNÉRÉS PAR LES TESTS")
print("-" * 70)
check("test_export_top10_regions.xlsx", os.path.exists("test_export_top10_regions.xlsx"))
check("test_export_top10_regions.csv", os.path.exists("test_export_top10_regions.csv"))

print("\n8. VÉRIFICATION DES PACKAGES PYTHON")
print("-" * 70)

packages_required = [
    'streamlit',
    'pandas',
    'geopandas',
    'folium',
    'plotly',
    'matplotlib',
    'seaborn',
    'openpyxl'
]

packages_ok = True
for package in packages_required:
    try:
        __import__(package)
        check(f"Package {package}", True)
    except ImportError:
        check(f"Package {package}", False, critical=True)
        packages_ok = False

print("\n9. VÉRIFICATION DE LA STRUCTURE DU CODE")
print("-" * 70)

# Vérifier que le fichier principal contient les fonctions clés
if os.path.exists("dashboard_sig_streamlit.py"):
    with open("dashboard_sig_streamlit.py", 'r', encoding='utf-8') as f:
        content = f.read()
        check("Fonction load_excel_data()", "def load_excel_data():" in content)
        check("Fonction load_geodata()", "def load_geodata():" in content)
        check("Fonction create_folium_map()", "def create_folium_map(" in content)
        check("Fonction main()", "def main():" in content)
        check("Onglet Marché Agroécologique", "Marche Agroecologique" in content)
        check("Top 10 par région", "Top 10 par region" in content or "Top 10 par Région" in content)

print("\n10. TAILLE DES FICHIERS")
print("-" * 70)

def check_file_size(filename, min_size_kb):
    """Vérifier la taille d'un fichier"""
    if os.path.exists(filename):
        size_kb = os.path.getsize(filename) / 1024
        check(f"{filename} (>= {min_size_kb} KB)", size_kb >= min_size_kb)
        print(f"   Taille: {size_kb:.1f} KB")
    else:
        check(f"{filename} existe", False)

check_file_size("dashboard_sig_streamlit.py", 100)  # Au moins 100 KB
check_file_size("MISSION_DE_SUIVI_cleaned.xlsx", 50)  # Au moins 50 KB
check_file_size("gadm41_TGO.gpkg", 1000)  # Au moins 1 MB

print("\n" + "=" * 70)
print("RÉSUMÉ DE LA VÉRIFICATION")
print("=" * 70)

print(f"\nTests réussis: {passed_checks}/{total_checks}")
print(f"Tests échoués: {failed_checks}/{total_checks}")

if failed_checks == 0:
    print("\nPARFAIT! Tous les fichiers sont en place.")
    print("\nPROCHAINES ÉTAPES:")
    print("   1. Lire LISEZ_MOI_DABORD.md")
    print("   2. Lire GUIDE_DEMARRAGE_RAPIDE.md")
    print("   3. Lancer: streamlit run dashboard_sig_streamlit.py")
    print("\nLe dashboard est prêt à être utilisé!")
    sys.exit(0)
else:
    print(f"\nATTENTION: {failed_checks} vérification(s) ont échoué.")
    print("\nACTIONS RECOMMANDÉES:")
    
    if not os.path.exists("MISSION_DE_SUIVI_cleaned.xlsx"):
        print("   • Ajouter le fichier MISSION_DE_SUIVI_cleaned.xlsx")
    
    if not os.path.exists("gadm41_TGO.gpkg"):
        print("   • Ajouter le fichier gadm41_TGO.gpkg")
    
    if not packages_ok:
        print("   • Installer les packages: pip install -r requirements.txt")
    
    print("\nConsulter la documentation:")
    print("   • LISEZ_MOI_DABORD.md")
    print("   • GUIDE_DEMARRAGE_RAPIDE.md")
    
    sys.exit(1)
