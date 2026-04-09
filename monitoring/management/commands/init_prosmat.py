from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from monitoring.models import Composante, SousComposante, Periode
from datetime import date

User = get_user_model()

class Command(BaseCommand):
    help = 'Initialise les données de base pour ProSMAT'

    def handle(self, *args, **options):
        self.stdout.write('Initialisation de ProSMAT...')
        
        # Créer un superutilisateur si aucun n'existe
        if not User.objects.filter(is_superuser=True).exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@prosmat.tg',
                password='admin123',
                first_name='Administrateur',
                last_name='ProSMAT',
                role='ADMIN'
            )
            self.stdout.write(self.style.SUCCESS(f'✓ Superutilisateur créé: admin / admin123'))
        
        # Créer des utilisateurs de test pour chaque région
        regions = ['MARITIME', 'PLATEAUX', 'CENTRALE', 'KARA', 'SAVANES']
        for region in regions:
            username = f'charge_{region.lower()}'
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    password='prosmat2026',
                    first_name=f'Chargé',
                    last_name=region.title(),
                    role='CHARGE_PROJET',
                    region=region,
                    email=f'{username}@prosmat.tg'
                )
                self.stdout.write(self.style.SUCCESS(f'✓ Utilisateur créé: {username} / prosmat2026'))
        
        # Créer un coordonnateur
        if not User.objects.filter(username='coordonnateur').exists():
            User.objects.create_user(
                username='coordonnateur',
                password='prosmat2026',
                first_name='Coordonnateur',
                last_name='National',
                role='COORDONNATEUR',
                email='coordonnateur@prosmat.tg'
            )
            self.stdout.write(self.style.SUCCESS('✓ Coordonnateur créé: coordonnateur / prosmat2026'))
        
        # Créer un évaluateur
        if not User.objects.filter(username='evaluateur').exists():
            User.objects.create_user(
                username='evaluateur',
                password='prosmat2026',
                first_name='Évaluateur',
                last_name='S&E',
                role='EVALUATEUR',
                email='evaluateur@prosmat.tg'
            )
            self.stdout.write(self.style.SUCCESS('✓ Évaluateur créé: evaluateur / prosmat2026'))
        
        # Créer les composantes de base
        composantes_data = [
            {'nom': 'Composante 1: Renforcement des capacités', 'ordre': 1},
            {'nom': 'Composante 2: Amélioration des infrastructures', 'ordre': 2},
            {'nom': 'Composante 3: Développement économique', 'ordre': 3},
        ]
        
        for comp_data in composantes_data:
            comp, created = Composante.objects.get_or_create(
                nom=comp_data['nom'],
                defaults={'ordre': comp_data['ordre']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Composante créée: {comp.nom}'))
        
        # Créer les périodes pour 2026
        periodes_data = [
            {'annee': 2026, 'trimestre': 'T1', 'date_debut': date(2026, 1, 1), 'date_fin': date(2026, 3, 31)},
            {'annee': 2026, 'trimestre': 'T2', 'date_debut': date(2026, 4, 1), 'date_fin': date(2026, 6, 30)},
            {'annee': 2026, 'trimestre': 'T3', 'date_debut': date(2026, 7, 1), 'date_fin': date(2026, 9, 30)},
            {'annee': 2026, 'trimestre': 'T4', 'date_debut': date(2026, 10, 1), 'date_fin': date(2026, 12, 31)},
        ]
        
        for periode_data in periodes_data:
            periode, created = Periode.objects.get_or_create(
                annee=periode_data['annee'],
                trimestre=periode_data['trimestre'],
                defaults={
                    'date_debut': periode_data['date_debut'],
                    'date_fin': periode_data['date_fin']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ Période créée: {periode}'))
        
        self.stdout.write(self.style.SUCCESS('\n✓ Initialisation terminée avec succès!'))
        self.stdout.write('\n=== COMPTES CRÉÉS ===')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Coordonnateur: coordonnateur / prosmat2026')
        self.stdout.write('Évaluateur: evaluateur / prosmat2026')
        self.stdout.write('Chargés de projet:')
        for region in regions:
            self.stdout.write(f'  - charge_{region.lower()} / prosmat2026 ({region})')
