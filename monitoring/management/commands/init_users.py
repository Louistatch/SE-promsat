"""
Commande pour créer tous les utilisateurs par défaut au déploiement
Usage: python manage.py init_users
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée tous les utilisateurs par défaut (admin + coordinateurs régionaux)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Création des utilisateurs par défaut...'))
        
        # Mot de passe par défaut (peut être changé via variable d'environnement)
        default_password = os.environ.get('DEFAULT_PASSWORD', 'ProSMAT2026!')
        
        # Liste des utilisateurs à créer
        users_to_create = [
            {
                'username': 'admin',
                'email': 'admin@prosmat.tg',
                'password': os.environ.get('ADMIN_PASSWORD', default_password),
                'first_name': 'Administrateur',
                'last_name': 'Système',
                'region': 'NATIONAL',
                'is_staff': True,
                'is_superuser': True,
            },
            {
                'username': 'coord_national',
                'email': 'national@prosmat.tg',
                'password': default_password,
                'first_name': 'Coordinateur',
                'last_name': 'National',
                'region': 'NATIONAL',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'coord_maritime',
                'email': 'maritime@prosmat.tg',
                'password': default_password,
                'first_name': 'Coordinateur',
                'last_name': 'Maritime',
                'region': 'MARITIME',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'coord_plateaux',
                'email': 'plateaux@prosmat.tg',
                'password': default_password,
                'first_name': 'Coordinateur',
                'last_name': 'Plateaux',
                'region': 'PLATEAUX',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'coord_centrale',
                'email': 'centrale@prosmat.tg',
                'password': default_password,
                'first_name': 'Coordinateur',
                'last_name': 'Centrale',
                'region': 'CENTRALE',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'coord_kara',
                'email': 'kara@prosmat.tg',
                'password': default_password,
                'first_name': 'Coordinateur',
                'last_name': 'Kara',
                'region': 'KARA',
                'is_staff': True,
                'is_superuser': False,
            },
            {
                'username': 'coord_savanes',
                'email': 'savanes@prosmat.tg',
                'password': default_password,
                'first_name': 'Coordinateur',
                'last_name': 'Savanes',
                'region': 'SAVANES',
                'is_staff': True,
                'is_superuser': False,
            },
        ]
        
        created_count = 0
        existing_count = 0
        
        for user_data in users_to_create:
            username = user_data['username']
            
            # Vérifier si l'utilisateur existe déjà
            if User.objects.filter(username=username).exists():
                self.stdout.write(
                    self.style.WARNING(f'⚠️  {username} existe déjà - ignoré')
                )
                existing_count += 1
                continue
            
            # Créer l'utilisateur
            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            
            created_count += 1
            self.stdout.write(
                self.style.SUCCESS(f'✅ {username} créé - Région: {user_data["region"]}')
            )
        
        # Résumé
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS(f'✅ {created_count} utilisateur(s) créé(s)'))
        self.stdout.write(self.style.WARNING(f'⚠️  {existing_count} utilisateur(s) existant(s)'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write('')
        
        # Afficher les identifiants
        self.stdout.write(self.style.SUCCESS('📋 IDENTIFIANTS PAR DÉFAUT:'))
        self.stdout.write('')
        self.stdout.write('👤 ADMINISTRATEUR SYSTÈME:')
        self.stdout.write(f'   Username: admin')
        self.stdout.write(f'   Password: {os.environ.get("ADMIN_PASSWORD", default_password)}')
        self.stdout.write('')
        self.stdout.write('👥 COORDINATEURS RÉGIONAUX:')
        self.stdout.write(f'   Username: coord_maritime, coord_plateaux, coord_centrale, coord_kara, coord_savanes')
        self.stdout.write(f'   Password: {default_password}')
        self.stdout.write('')
        self.stdout.write(self.style.WARNING('⚠️  IMPORTANT: Changez ces mots de passe après la première connexion!'))
        self.stdout.write('')
