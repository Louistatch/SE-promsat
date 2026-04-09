from django.core.management.base import BaseCommand
import openpyxl
from monitoring.models import Composante, SousComposante, Indicateur

class Command(BaseCommand):
    help = 'Importe les indicateurs depuis le fichier Excel'

    def handle(self, *args, **options):
        self.stdout.write('📊 Importation des indicateurs depuis Excel...')
        
        # Charger le fichier Excel
        wb = openpyxl.load_workbook('Tableau de Bord de Suivi-Évaluation .xlsx')
        ws = wb['Ref-Indicateurs']
        
        # Créer les composantes
        comp_gafsp, _ = Composante.objects.get_or_create(
            nom="Indicateurs GAFSP",
            defaults={'ordre': 1, 'description': 'Indicateurs du Global Agriculture and Food Security Program'}
        )
        
        comp_dev, _ = Composante.objects.get_or_create(
            nom="Indicateurs DEV",
            defaults={'ordre': 2, 'description': 'Indicateurs de développement'}
        )
        
        comp_prod, _ = Composante.objects.get_or_create(
            nom="Indicateurs PROD",
            defaults={'ordre': 3, 'description': 'Indicateurs de production'}
        )
        
        comp_res, _ = Composante.objects.get_or_create(
            nom="Indicateurs RES",
            defaults={'ordre': 4, 'description': 'Indicateurs de résultats'}
        )
        
        # Créer les sous-composantes
        sous_comp_gafsp, _ = SousComposante.objects.get_or_create(
            composante=comp_gafsp,
            nom="Indicateurs principaux GAFSP",
            defaults={'ordre': 1}
        )
        
        sous_comp_dev, _ = SousComposante.objects.get_or_create(
            composante=comp_dev,
            nom="Indicateurs de développement",
            defaults={'ordre': 1}
        )
        
        sous_comp_prod, _ = SousComposante.objects.get_or_create(
            composante=comp_prod,
            nom="Indicateurs de production",
            defaults={'ordre': 1}
        )
        
        sous_comp_res, _ = SousComposante.objects.get_or_create(
            composante=comp_res,
            nom="Indicateurs de résultats",
            defaults={'ordre': 1}
        )
        
        # Lire les indicateurs
        count = 0
        for row in ws.iter_rows(min_row=5, values_only=True):
            if not row[1]:
                continue
                
            code = str(row[1]).strip() if row[1] else None
            niveau = str(row[2]).strip() if row[2] else "Extrant"
            libelle = str(row[3]).strip() if row[3] else ""
            unite = str(row[4]).strip() if row[4] else "Nombre"
            ref = float(row[5]) if row[5] and isinstance(row[5], (int, float)) else 0
            cible = float(row[6]) if row[6] and isinstance(row[6], (int, float)) else 0
            source = str(row[7]).strip() if row[7] else ""
            frequence = str(row[8]).strip() if row[8] else "Trimestriel"
            responsable = str(row[9]).strip() if row[9] else "S&E"
            
            if not code or not libelle:
                continue
            
            # Déterminer la sous-composante
            if code.startswith('GAFSP'):
                sous_comp = sous_comp_gafsp
            elif code.startswith('DEV'):
                sous_comp = sous_comp_dev
            elif code.startswith('PROD'):
                sous_comp = sous_comp_prod
            elif code.startswith('RES'):
                sous_comp = sous_comp_res
            else:
                sous_comp = sous_comp_gafsp
            
            # Mapper le niveau
            niveau_map = {
                'But': 'IMPACT',
                'Objectif': 'EFFET',
                'Résultat': 'EXTRANT',
                'Extrant': 'EXTRANT'
            }
            niveau_final = niveau_map.get(niveau, 'EXTRANT')
            
            # Créer l'indicateur
            indicateur, created = Indicateur.objects.update_or_create(
                code=code,
                defaults={
                    'sous_composante': sous_comp,
                    'libelle': libelle,
                    'type_indicateur': 'QUANTITATIF',
                    'niveau': niveau_final,
                    'unite_mesure': unite,
                    'valeur_reference': ref,
                    'cible_finale': cible,
                    'source_verification': source,
                    'frequence_collecte': frequence,
                    'responsable': responsable,
                    'actif': True
                }
            )
            
            if created:
                count += 1
                self.stdout.write(self.style.SUCCESS(f'✓ {code} - {libelle[:50]}...'))
        
        self.stdout.write(self.style.SUCCESS(f'\n✓ {count} indicateurs importés!'))
        self.stdout.write(self.style.SUCCESS(f'📊 Total: {Indicateur.objects.count()} indicateurs'))
