"""
Script d'importation complet des données ProSMAT depuis Excel
Importe toutes les composantes, indicateurs avec valeurs de référence et cibles
"""
import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Composante, SousComposante, Indicateur

def nettoyer_valeur(val):
    """Convertir une valeur en nombre ou None"""
    if pd.isna(val) or val == '' or val == '-' or val == 'N/A':
        return None
    try:
        val_str = str(val).replace(',', '.').replace(' ', '').strip()
        # Gérer les pourcentages
        if '%' in val_str:
            val_str = val_str.replace('%', '')
        return float(val_str)
    except:
        return None

def importer_composante_1():
    """Importer Composante 1 - Production"""
    print("\n" + "="*80)
    print("COMPOSANTE 1: INTENSIFICATION DE LA PRODUCTION AGROÉCOLOGIQUE")
    print("="*80)
    
    fichier = 'C:/Users/HP/Downloads/prosmat_se/Indicateurs_ProSMAT_Complet.xlsx'
    df = pd.read_excel(fichier, sheet_name='Composante 1 - Production', header=None)
    
    comp, _ = Composante.objects.get_or_create(
        nom='Composante 1: Production Agroécologique',
        defaults={'description': 'Intensification de la production agroécologique', 'ordre': 1}
    )
    
    # Sous-composante 1.1
    sc1, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='1.1 Production et Surfaces',
        defaults={'description': 'Indicateurs de production et surfaces cultivées'}
    )
    
    indicateurs_1_1 = [
        ('IND-1-001', 'Superficie sous pratiques agroécologiques', 0, 1250, 'Hectares', 'GAFSP #2'),
        ('IND-1-002', 'Superficie irriguée', 0, 50, 'Hectares', 'GAFSP #2'),
        ('IND-1-003', 'Pratiques résilientes mises en œuvre', 0, 1062.5, 'Hectares', 'GAFSP #14'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_1_1:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc1,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'EXTRANT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")
    
    # Sous-composante 1.2
    sc2, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='1.2 Formation et Renforcement des Capacités',
        defaults={'description': 'Formation des acteurs'}
    )
    
    indicateurs_1_2 = [
        ('IND-1-004', 'Fermes écoles agroécologiques', 6, 20, 'Fermes', ''),
        ('IND-1-005', 'Maîtres formateurs recyclés', 0, 40, 'Personnes', '2 par ferme école'),
        ('IND-1-006', 'Paysans relais formés', 0, 500, 'Personnes', '2 par coopérative'),
        ('IND-1-007', 'Maraîchers formés', 360, 5000, 'Personnes', 'GAFSP #3 - dont 2000 femmes'),
        ('IND-1-008', 'Taux d\'adoption des pratiques', 0, 70, 'Pourcentage', '3500 maraîchers'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_1_2:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc2,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'EXTRANT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")

def importer_composante_2():
    """Importer Composante 2 - Valorisation"""
    print("\n" + "="*80)
    print("COMPOSANTE 2: VALORISATION DES PRODUITS AGROÉCOLOGIQUES")
    print("="*80)
    
    comp, _ = Composante.objects.get_or_create(
        nom='Composante 2: Valorisation',
        defaults={'description': 'Valorisation des produits agroécologiques', 'ordre': 2}
    )
    
    # Sous-composante 2.1
    sc1, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='2.1 Infrastructures de Marché',
        defaults={'description': 'Développement des infrastructures'}
    )
    
    indicateurs_2_1 = [
        ('IND-2-001', 'Espaces de vente aménagés', 0, 5, 'Espaces', 'GAFSP #7 - Lomé, Atakpamé, Sokodé, Kara, Dapaong'),
        ('IND-2-002', 'Installations totales', 0, 40, 'Installations', 'GAFSP #7 - Transformation, stockage, marché'),
        ('IND-2-003', 'Chambres froides traditionnelles', 0, 5, 'Chambres', '3 tonnes par chambre'),
        ('IND-2-004', 'Agriculteurs avec accès marché', 0, 5000, 'Agriculteurs', 'GAFSP #8 - dont 2000 femmes'),
        ('IND-2-005', 'Commerçantes appuyées', 0, 150, 'Personnes', 'Mise en marché'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_2_1:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc1,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'EXTRANT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")
    
    # Sous-composante 2.2
    sc2, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='2.2 Transformation',
        defaults={'description': 'Unités de transformation'}
    )
    
    indicateurs_2_2 = [
        ('IND-2-006', 'Unités de transformation renforcées', 0, 25, 'Unités', 'Coopératives de femmes (90%+)'),
        ('IND-2-007', 'Subvention par unité', 0, 7500, 'USD', 'Plafond'),
        ('IND-2-008', 'Production par unité', 0, 3.3, 'Tonnes/mois', 'Tomates transformées'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_2_2:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc2,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'EXTRANT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")

def importer_composante_3():
    """Importer Composante 3 - Capacités"""
    print("\n" + "="*80)
    print("COMPOSANTE 3: RENFORCEMENT DES CAPACITÉS ET DIALOGUE POLITIQUE")
    print("="*80)
    
    comp, _ = Composante.objects.get_or_create(
        nom='Composante 3: Renforcement des Capacités',
        defaults={'description': 'Renforcement des capacités et dialogue politique', 'ordre': 3}
    )
    
    # Sous-composante 3.1
    sc1, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='3.1 Structuration des Organisations',
        defaults={'description': 'Organisations de producteurs'}
    )
    
    indicateurs_3_1 = [
        ('IND-3-001', 'Organisations de producteurs soutenues', 0, 286, 'Organisations', 'GAFSP #4'),
        ('IND-3-002', 'Coopératives structurées', 0, 275, 'Coopératives', '250 producteurs + 25 transformatrices'),
        ('IND-3-003', 'Unions régionales renforcées', 0, 5, 'Unions', 'Gouvernance'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_3_1:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc1,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'EXTRANT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")
    
    # Sous-composante 3.2
    sc2, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='3.2 Leadership et Gestion',
        defaults={'description': 'Formation en leadership'}
    )
    
    indicateurs_3_2 = [
        ('IND-3-004', 'Personnes formées en leadership', 0, 9885, 'Personnes', 'GAFSP #10 - dont 5720 femmes'),
        ('IND-3-005', 'Leaders et techniciens formés', 0, 185, 'Personnes', 'Leadership et gestion CTOP'),
        ('IND-3-006', 'Jeunes et femmes leaders', 0, 100, 'Personnes', 'Parcours spécifique leadership'),
        ('IND-3-007', 'Directeurs et comptables formés', 0, 20, 'Personnes', 'Faîtières membres'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_3_2:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc2,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'EXTRANT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")

def importer_indicateurs_genre():
    """Importer les indicateurs Genre et Inclusion"""
    print("\n" + "="*80)
    print("INDICATEURS GENRE ET INCLUSION SOCIALE")
    print("="*80)
    
    comp, _ = Composante.objects.get_or_create(
        nom='Genre et Inclusion Sociale',
        defaults={'description': 'Indicateurs transversaux de genre et inclusion', 'ordre': 4}
    )
    
    sc, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='Indicateurs Genre',
        defaults={'description': 'Suivi des aspects genre'}
    )
    
    indicateurs_genre = [
        ('IND-GENRE-001', 'Bénéficiaires directs - Total', 0, 9885, 'Personnes', 'GAFSP #1'),
        ('IND-GENRE-002', 'Bénéficiaires directs - Femmes', 0, 5720, 'Personnes', '57-59% du total'),
        ('IND-GENRE-003', 'Services financiers pour femmes', 0, 2250, 'Femmes', '100% femmes'),
        ('IND-GENRE-004', 'Emplois créés pour les femmes', 0, 2414, 'ETP', '44% des emplois totaux'),
        ('IND-GENRE-005', 'Coopératives de transformation dirigées par femmes', 0, 25, 'Coopératives', 'Composante 2'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_genre:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'IMPACT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")

def importer_indicateurs_gafsp():
    """Importer les indicateurs GAFSP récapitulatifs"""
    print("\n" + "="*80)
    print("INDICATEURS GAFSP RÉCAPITULATIFS")
    print("="*80)
    
    comp, _ = Composante.objects.get_or_create(
        nom='Indicateurs GAFSP',
        defaults={'description': 'Indicateurs du cadre GAFSP', 'ordre': 5}
    )
    
    sc, _ = SousComposante.objects.get_or_create(
        composante=comp,
        nom='Indicateurs GAFSP',
        defaults={'description': 'Cadre de résultats GAFSP'}
    )
    
    indicateurs_gafsp = [
        ('GAFSP-01', 'Nombre de bénéficiaires directs', 0, 9885, 'Personnes', '5720 femmes (58%)'),
        ('GAFSP-02', 'Superficie avec soutien production améliorée', 0, 1250, 'Hectares', ''),
        ('GAFSP-02-IRR', 'Superficie avec nouveaux services irrigation', 0, 50, 'Hectares', ''),
        ('GAFSP-03', 'Petits producteurs/transformateurs soutenus', 0, 5250, 'Personnes', '2250 femmes (43%)'),
        ('GAFSP-04', 'Organisations de producteurs soutenues', 0, 286, 'Organisations', ''),
        ('GAFSP-05', 'Personnes avec accès services financiers', 0, 2250, 'Personnes', '2250 femmes (100%)'),
        ('GAFSP-07', 'Installations transformation/stockage/marché', 0, 40, 'Installations', ''),
        ('GAFSP-08', 'Agriculteurs avec accès marchés', 0, 5000, 'Agriculteurs', '2000 femmes (40%)'),
        ('GAFSP-09', 'Emploi direct fourni (ETP)', 0, 5467, 'ETP', '2414 femmes (44%)'),
        ('GAFSP-10', 'Personnes avec renforcement capacités', 0, 9885, 'Personnes', '5720 femmes (58%)'),
        ('GAFSP-11', 'Produits politiques/notes connaissances', 1, 4, 'Documents', 'Perspective genre intégrée'),
        ('GAFSP-12', 'Personnes avec produits nutritionnels améliorés', 0, 4000, 'Personnes', '3000 femmes (75%)'),
        ('GAFSP-13', 'Agriculteurs recevant intrants/services durables', 0, 5000, 'Agriculteurs', 'dont 2000 femmes'),
        ('GAFSP-14', 'Pratiques agricoles résilientes', 0, 1062.5, 'Hectares', 'Surfaces avec pratiques durables'),
    ]
    
    for code, libelle, ref, cible, unite, details in indicateurs_gafsp:
        ind, created = Indicateur.objects.update_or_create(
            code=code,
            defaults={
                'libelle': libelle,
                'sous_composante': sc,
                'valeur_reference': ref,
                'cible_finale': cible,
                'unite_mesure': unite,
                'type_indicateur': 'QUANTITATIF',
                'niveau': 'IMPACT',
                'source_verification': details,
                'actif': True
            }
        )
        print(f"  {'✓' if created else '↻'} {code}: {libelle}")

def afficher_resume():
    """Afficher le résumé de l'importation"""
    print("\n" + "="*80)
    print("RÉSUMÉ DE L'IMPORTATION")
    print("="*80)
    
    for comp in Composante.objects.all().order_by('ordre'):
        nb_sc = comp.sous_composantes.count()
        nb_ind = Indicateur.objects.filter(sous_composante__composante=comp).count()
        print(f"\n{comp.nom}")
        print(f"  Sous-composantes: {nb_sc}")
        print(f"  Indicateurs: {nb_ind}")
    
    print(f"\n{'='*80}")
    print(f"TOTAL INDICATEURS: {Indicateur.objects.count()}")
    print(f"INDICATEURS ACTIFS: {Indicateur.objects.filter(actif=True).count()}")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("IMPORTATION COMPLÈTE DES DONNÉES PROSMAT")
    print("="*80)
    
    try:
        importer_composante_1()
        importer_composante_2()
        importer_composante_3()
        importer_indicateurs_genre()
        importer_indicateurs_gafsp()
        afficher_resume()
        
        print("✅ IMPORTATION TERMINÉE AVEC SUCCÈS!\n")
        
    except Exception as e:
        print(f"\n❌ ERREUR: {e}")
        import traceback
        traceback.print_exc()
