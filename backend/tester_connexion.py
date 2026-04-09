"""
Script pour tester la connexion Firebase avec des identifiants spécifiques
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.firebase_auth import initialize_firebase
from firebase_admin import auth
import requests
import json

print("\n" + "="*80)
print("🔍 TEST DE CONNEXION FIREBASE")
print("="*80)

# Initialiser Firebase
initialize_firebase()

# Informations de test
email = "tatchida@gmail.com"
print(f"\n📧 Email testé: {email}")

# 1. Vérifier que l'utilisateur existe dans Firebase
print("\n1️⃣ Vérification de l'utilisateur dans Firebase:")
try:
    user = auth.get_user_by_email(email)
    print(f"   ✅ Utilisateur trouvé!")
    print(f"   • UID: {user.uid}")
    print(f"   • Email: {user.email}")
    print(f"   • Email vérifié: {'✅' if user.email_verified else '❌'}")
    print(f"   • Désactivé: {'❌ OUI' if user.disabled else '✅ NON'}")
    print(f"   • Créé le: {user.user_metadata.creation_timestamp}")
    
    if user.disabled:
        print("\n   ⚠️  ATTENTION: Le compte est désactivé!")
        print("   Activez-le dans Firebase Console")
        
except auth.UserNotFoundError:
    print(f"   ❌ Utilisateur non trouvé avec l'email: {email}")
    print("\n   💡 Créez l'utilisateur dans Firebase Console:")
    print("      https://console.firebase.google.com/project/prosmat-auth/authentication/users")
    sys.exit(1)
except Exception as e:
    print(f"   ❌ Erreur: {e}")
    sys.exit(1)

# 2. Tester l'authentification Firebase (côté client)
print("\n2️⃣ Test d'authentification Firebase (simulation):")
print("   ℹ️  L'authentification se fait côté client (navigateur)")
print("   ℹ️  Le backend Django reçoit ensuite le token")

# 3. Vérifier la configuration Firebase dans settings
print("\n3️⃣ Configuration Firebase (frontend):")
from django.conf import settings
firebase_config = settings.FIREBASE_CONFIG

print(f"   • API Key: {firebase_config['apiKey'][:20]}...")
print(f"   • Auth Domain: {firebase_config['authDomain']}")
print(f"   • Project ID: {firebase_config['projectId']}")

# 4. Vérifier que Email/Password est activé
print("\n4️⃣ Méthodes d'authentification:")
print("   ℹ️  Vérifiez dans Firebase Console que Email/Password est activé:")
print("   https://console.firebase.google.com/project/prosmat-auth/authentication/providers")

# 5. Diagnostic du problème
print("\n" + "="*80)
print("🔍 DIAGNOSTIC")
print("="*80)

print("\n✅ Ce qui fonctionne:")
print("   • Firebase Admin SDK initialisé")
print("   • Utilisateur existe dans Firebase")
print("   • Configuration Firebase correcte")

print("\n❓ Causes possibles de l'échec:")
print("\n   1. Mot de passe incorrect")
print("      → Vérifiez que vous tapez exactement: L@uis1993")
print("      → Attention à la casse (majuscules/minuscules)")
print("      → Attention aux caractères spéciaux (@)")

print("\n   2. Email/Password non activé dans Firebase")
print("      → Allez sur Firebase Console > Authentication > Sign-in method")
print("      → Vérifiez que 'Email/Password' est activé")

print("\n   3. Compte désactivé")
if user.disabled:
    print("      ❌ Le compte EST désactivé!")
else:
    print("      ✅ Le compte n'est pas désactivé")

print("\n   4. Problème de token côté client")
print("      → Ouvrez la console du navigateur (F12)")
print("      → Regardez les erreurs dans l'onglet Console")
print("      → Regardez les requêtes dans l'onglet Network")

print("\n   5. Domaine non autorisé")
print("      → Vérifiez que localhost est autorisé dans Firebase Console")
print("      → Settings > Authorized domains")

# 6. Test de réinitialisation de mot de passe
print("\n" + "="*80)
print("💡 SOLUTIONS")
print("="*80)

print("\n1. Réinitialiser le mot de passe:")
print("   • Cliquez sur 'Mot de passe oublié?' sur la page de connexion")
print("   • Ou dans Firebase Console > Authentication > Users")
print("   • Cliquez sur les 3 points à côté de l'utilisateur")
print("   • Sélectionnez 'Reset password'")

print("\n2. Vérifier dans la console du navigateur:")
print("   • Ouvrez http://localhost:8000/accounts/login/")
print("   • Appuyez sur F12")
print("   • Onglet Console")
print("   • Tentez de vous connecter")
print("   • Notez les erreurs affichées")

print("\n3. Vérifier les logs Django:")
print("   • Ouvrez un nouveau terminal")
print("   • Exécutez: Get-Content logs\\django.log -Wait -Tail 50")
print("   • Tentez de vous connecter")
print("   • Regardez les logs en temps réel")

print("\n" + "="*80)
print("📋 CHECKLIST DE VÉRIFICATION")
print("="*80)

checklist = [
    ("Utilisateur existe dans Firebase", True),
    ("Firebase Admin SDK initialisé", True),
    ("Email/Password activé dans Firebase Console", "À vérifier"),
    ("Compte non désactivé", not user.disabled),
    ("Mot de passe correct", "À vérifier"),
    ("localhost dans domaines autorisés", "À vérifier"),
]

for item, status in checklist:
    if status == True:
        print(f"   ✅ {item}")
    elif status == False:
        print(f"   ❌ {item}")
    else:
        print(f"   ⚠️  {item}")

print("\n" + "="*80)
print("🎯 PROCHAINE ÉTAPE")
print("="*80)

print("\n1. Ouvrez la page de connexion:")
print("   http://localhost:8000/accounts/login/")

print("\n2. Ouvrez la console du navigateur (F12)")

print("\n3. Tentez de vous connecter avec:")
print(f"   Email: {email}")
print("   Mot de passe: L@uis1993")

print("\n4. Regardez les erreurs dans la console")

print("\n5. Si erreur 'auth/wrong-password':")
print("   → Le mot de passe est incorrect")
print("   → Réinitialisez-le dans Firebase Console")

print("\n6. Si erreur 'auth/user-not-found':")
print("   → L'email est incorrect")
print("   → Vérifiez l'orthographe")

print("\n7. Si erreur 'auth/invalid-email':")
print("   → Le format de l'email est invalide")

print("\n8. Si aucune erreur mais 'Authentification échouée':")
print("   → Le problème est côté backend Django")
print("   → Vérifiez les logs: Get-Content logs\\django.log -Tail 50")

print("\n")
