from django.core.management.base import BaseCommand
from monitoring.models import Indicateur, Periode, Realisation
from accounts.models import User
from decimal import Decimal

class Command(BaseCommand):
    help = 'Crée des données de test pour la Phase 1'

    def handle(self, *args, **options):
        self.stdout.write('📊 Création de données de test...')
        
        # Récupérer les objets nécessaires
        try:
            periode = Periode.objects.filter(annee=2026, trimestre='T1').first()
            if not periode:
                self.stdout.write(self.style.ERROR('Aucune période T1 2026 trouvée'))
                return
            
            # Récupérer quelques indicateurs
            indicateurs = Indicateur.objects.filter(actif=True)[:5]
            if not indicateurs:
                self.stdout.write(self.style.ERROR('Aucun indicateur trouvé'))
                return
            
            # Régions
            regions = ['MARITIME', 'PLATEAUX', 'CENTRALE', 'KARA', 'SAVANES']
            
            # Utilisateurs par région
            users = {}
            for region in regions:
                user = User.objects.filter(region=region, role='CHARGE_PROJET').first()
                if user:
                    users[region] = user
            
            count = 0
            for indicateur in indicateurs:
                for region in regions:
                    # Générer des valeurs aléatoires mais cohérentes
                    if indicateur.cible_finale:
                        # 20% de la cible par région (5 régions = 100%)
                        valeur_base = float(indicateur.cible_finale) * 0.20
                    else:
                        valeur_base = 100
                    
                    # Variation par région
                    variations = {
                        'MARITIME': 1.1,
                        'PLATEAUX': 0.9,
                        'CENTRALE': 0.8,
                        'KARA': 1.0,
                        'SAVANES': 0.7
                    }
                    
                    valeur = Decimal(str(valeur_base * variations[region]))
                    
                    # Désagrégation par genre (55% femmes, 45% hommes)
                    femmes = valeur * Decimal('0.55')
                    hommes = valeur * Decimal('0.45')
                    
                    # Créer la réalisation
                    realisation, created = Realisation.objects.update_or_create(
                        indicateur=indicateur,
                        periode=periode,
                        region=region,
                        defaults={
                            'valeur_realisee': valeur,
                            'hommes': hommes,
                            'femmes': femmes,
                            'commentaire': f'Données de test pour {region}',
                            'saisi_par': users.get(region),
                            'valide': True
                        }
                    )
                    
                    if created:
                        count += 1
                        self.stdout.write(self.style.SUCCESS(
                            f'✓ {indicateur.code} - {region}: {valeur}'
                        ))
            
            self.stdout.write(self.style.SUCCESS(f'\n✓ {count} réalisations créées!'))
            
            # Vérifier les alertes
            from monitoring.utils import verifier_qualite_realisation
            for realisation in Realisation.objects.filter(periode=periode):
                verifier_qualite_realisation(realisation)
            
            self.stdout.write(self.style.SUCCESS('✓ Contrôle qualité effectué!'))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Erreur: {str(e)}'))
