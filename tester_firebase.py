"""
Script de test pour Firebase Authentication
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings

print("\n" + "="*80)
print("TEST DE LA CONFIGURATION FIREBASE")
print("="*80)

print("\n✅ Configuration Firebase:")
for key, value in settings.FIREBASE_CONFIG.items():
    if value:
        # Masquer partiellement les valeurs sensibles
        if key == 'apiKey':
            display_value = value[:10] + "..." + value[-5:]
        else:
            display_value = value
        print(f"   {key}: {display_value}")
    else:
        print(f"   ❌ {key}: NON CONFIGURÉ")

# Vérifier que toutes les valeurs sont remplies
all_configured = all(settings.FIREBASE_CONFIG.values())

if all_configured:
    print("\n✅ Toutes les variables Firebase sont configurées!")
    print("\nProchaines étapes:")
    print("  1. Activer l'authentification Email/Password dans Firebase Console")
    print("  2. Démarrer le serveur: python manage.py runserver")
    print("  3. Aller sur: http://localhost:8000/accounts/login-firebase/")
    print("  4. Créer un compte et se connecter")
else:
    print("\n❌ Certaines variables Firebase ne sont pas configurées")
    print("Vérifiez le fichier .env")

print("\n" + "="*80)
print("URLS DISPONIBLES")
print("="*80)

print("\nAuthentification Firebase:")
print("  - Connexion: http://localhost:8000/accounts/login-firebase/")
print("  - Déconnexion: http://localhost:8000/accounts/logout-firebase/")

print("\nAuthentification Django classique:")
print("  - Connexion: http://localhost:8000/accounts/login/")
print("  - Déconnexion: http://localhost:8000/accounts/logout/")

print("\nDashboard:")
print("  - Accueil: http://localhost:8000/")
print("  - Dashboard: http://localhost:8000/dashboard/")

print("\n" + "="*80)
