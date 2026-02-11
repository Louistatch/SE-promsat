"""
Script de vérification complète de Firebase
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.conf import settings
import firebase_admin
from firebase_admin import auth

print("\n" + "="*80)
print("🔍 DIAGNOSTIC COMPLET FIREBASE")
print("="*80)

# 1. Vérifier les variables d'environnement
print("\n1️⃣ Variables d'environnement:")
firebase_vars = {
    'FIREBASE_API_KEY': settings.FIREBASE_CONFIG.get('apiKey', ''),
    'FIREBASE_AUTH_DOMAIN': settings.FIREBASE_CONFIG.get('authDomain', ''),
    'FIREBASE_PROJECT_ID': settings.FIREBASE_CONFIG.get('projectId', ''),
    'FIREBASE_STORAGE_BUCKET': settings.FIREBASE_CONFIG.get('storageBucket', ''),
    'FIREBASE_MESSAGING_SENDER_ID': settings.FIREBASE_CONFIG.get('messagingSenderId', ''),
    'FIREBASE_APP_ID': settings.FIREBASE_CONFIG.get('appId', ''),
}

all_ok = True
for key, value in firebase_vars.items():
    status = "✅" if value else "❌"
    print(f"   {status} {key}: {'OK' if value else 'MANQUANT'}")
    if not value:
        all_ok = False

if not all_ok:
    print("\n❌ Certaines variables sont manquantes!")
    sys.exit(1)

# 2. Vérifier Firebase Admin SDK
print("\n2️⃣ Firebase Admin SDK:")
if firebase_admin._apps:
    print("   ✅ Firebase Admin SDK initialisé")
    
    # Essayer de lister les utilisateurs
    try:
        print("\n3️⃣ Utilisateurs Firebase:")
        page = auth.list_users()
        users = list(page.users)
        
        if users:
            print(f"   ✅ {len(users)} utilisateur(s) trouvé(s):")
            for user in users[:5]:  # Afficher max 5 utilisateurs
                print(f"      • {user.email} (UID: {user.uid[:20]}...)")
                print(f"        Email vérifié: {'✅' if user.email_verified else '❌'}")
                print(f"        Désactivé: {'❌' if user.disabled else '✅'}")
        else:
            print("   ⚠️  Aucun utilisateur trouvé dans Firebase!")
            print("\n   📝 Pour créer un utilisateur:")
            print("      1. Allez sur https://console.firebase.google.com")
            print(f"      2. Projet: {firebase_vars['FIREBASE_PROJECT_ID']}")
            print("      3. Authentication > Users > Add user")
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la récupération des utilisateurs: {e}")
        print("\n   💡 Vérifiez que vous avez les permissions nécessaires")
else:
    print("   ❌ Firebase Admin SDK non initialisé")
    sys.exit(1)

# 4. Vérifier la configuration Django
print("\n4️⃣ Configuration Django:")
backends = settings.AUTHENTICATION_BACKENDS
firebase_backend = 'accounts.firebase_auth.FirebaseAuthenticationBackend'
if firebase_backend in backends:
    print(f"   ✅ FirebaseAuthenticationBackend configuré")
else:
    print(f"   ❌ FirebaseAuthenticationBackend manquant")

# 5. Tester la création d'un token (simulation)
print("\n5️⃣ Test de connexion:")
print("   Pour tester la connexion:")
print("   1. Créez un utilisateur dans Firebase Console")
print("   2. Allez sur http://localhost:8000/accounts/login/")
print("   3. Utilisez les identifiants créés")

# 6. Informations utiles
print("\n" + "="*80)
print("📋 INFORMATIONS UTILES")
print("="*80)
print(f"\n🔗 Firebase Console:")
print(f"   https://console.firebase.google.com/project/{firebase_vars['FIREBASE_PROJECT_ID']}/authentication/users")

print(f"\n🔗 Page de connexion:")
print(f"   http://localhost:8000/accounts/login/")

print(f"\n📊 Logs Django:")
print(f"   Get-Content logs\\django.log -Wait -Tail 50")

print("\n" + "="*80)
print("✅ DIAGNOSTIC TERMINÉ")
print("="*80)

# Recommandations
print("\n💡 RECOMMANDATIONS:")

if not users:
    print("\n⚠️  AUCUN UTILISATEUR FIREBASE TROUVÉ!")
    print("\n   Créez un utilisateur de test:")
    print("   1. Console Firebase > Authentication > Users")
    print("   2. Cliquez 'Add user'")
    print("   3. Email: test@prosmat.tg")
    print("   4. Mot de passe: Test123456")
    print("   5. Testez la connexion")
else:
    print("\n✅ Des utilisateurs existent dans Firebase")
    print("   Si la connexion échoue:")
    print("   1. Vérifiez que vous utilisez le bon email")
    print("   2. Vérifiez que vous utilisez le bon mot de passe")
    print("   3. Vérifiez la console du navigateur (F12)")
    print("   4. Vérifiez les logs Django")

print("\n")
