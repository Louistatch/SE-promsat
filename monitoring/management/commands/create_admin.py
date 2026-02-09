"""
Commande pour créer un superuser automatiquement
Usage: python manage.py create_admin
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import os

User = get_user_model()

class Command(BaseCommand):
    help = 'Crée un superuser automatiquement'

    def handle(self, *args, **options):
        # Récupérer les informations depuis les variables d'environnement
        username = os.environ.get('ADMIN_USERNAME', 'admin')
        email = os.environ.get('ADMIN_EMAIL', 'admin@prosmat.tg')
        password = os.environ.get('ADMIN_PASSWORD', 'admin123')
        
        # Vérifier si l'utilisateur existe déjà
        if User.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f'Le superuser "{username}" existe déjà.')
            )
            return
        
        # Créer le superuser
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            first_name='Admin',
            last_name='ProSMAT'
        )
        
        # Donner tous les accès
        user.is_staff = True
        user.is_superuser = True
        user.region = 'NATIONAL'
        user.save()
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Superuser "{username}" créé avec succès!')
        )
        self.stdout.write(
            self.style.SUCCESS(f'   Email: {email}')
        )
        self.stdout.write(
            self.style.WARNING(f'   ⚠️ Changez le mot de passe après la première connexion!')
        )
