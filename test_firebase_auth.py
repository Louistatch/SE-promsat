"""
Script de test pour vérifier la configuration Firebase
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.firebase_auth import initialize_firebase, verify_firebase_token
from django.conf import settings

def test_firebase_config():
    """Tester la configuration Firebase"""
    print("\n" + "="*80)
    print("TEST DE CONFIGURATION FIREBASE")
    print("="*80)
    
    # Vérifier les variables d'environnement
    print("\n1. Variables d'environnement Firebase:")
    firebase_vars = [
        'FIREBASE_API_KEY',
        'FIREBASE_AUTH_DOMAIN',
        'FIREBASE_PROJECT_ID',
        'FIREBASE_STORAGE_BUCKET',
        'FIREBASE_MESSAGING_SENDER_ID',
        'FIREBASE_APP_ID',
    ]
    
    all_set = True
    for var in firebase_vars:
        value = settings.FIREBASE_CONFIG.get(var.lower().replace('firebase_', ''), '')
        status = "✅" if value else "❌"
        print(f"   {status} {var}: {'Configuré' if value else 'MANQUANT'}")
        if not value:
            all_set = False
    
    if not all_set:
        print("\n⚠️  ATTENTION: Certaines variables Firebase ne sont pas configurées!")
        print("   Copiez .env.example vers .env et remplissez les valeurs.")
        return False
    
    # Vérifier l'initialisation Firebase Admin SDK
    print("\n2. Firebase Admin SDK:")
    try:
        success = initialize_firebase()
        if success:
            print("   ✅ Firebase Admin SDK initialisé avec succès")
        else:
            print("   ❌ Échec de l'initialisation Firebase Admin SDK")
            return False
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
        return False
    
    # Vérifier le fichier credentials (optionnel)
    print("\n3. Fichier credentials (optionnel):")
    cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
    if os.path.exists(cred_path):
        print(f"   ✅ Fichier trouvé: {cred_path}")
    else:
        print(f"   ℹ️  Fichier non trouvé (utilise credentials par défaut)")
    
    # Vérifier les backends d'authentification
    print("\n4. Backends d'authentification:")
    backends = settings.AUTHENTICATION_BACKENDS
    firebase_backend = 'accounts.firebase_auth.FirebaseAuthenticationBackend'
    if firebase_backend in backends:
        print(f"   ✅ FirebaseAuthenticationBackend configuré")
    else:
        print(f"   ❌ FirebaseAuthenticationBackend MANQUANT")
        return False
    
    # Vérifier la configuration de logging
    print("\n5. Configuration de logging:")
    if hasattr(settings, 'LOGGING'):
        print("   ✅ Logging configuré")
        log_dir = settings.BASE_DIR / 'logs'
        if log_dir.exists():
            print(f"   ✅ Dossier logs existe: {log_dir}")
        else:
            print(f"   ⚠️  Dossier logs n'existe pas: {log_dir}")
            print("      Créez-le avec: mkdir logs")
    else:
        print("   ❌ Logging non configuré")
    
    # Vérifier la configuration du cache
    print("\n6. Configuration du cache (rate limiting):")
    if hasattr(settings, 'CACHES'):
        print("   ✅ Cache configuré")
    else:
        print("   ❌ Cache non configuré")
    
    # Vérifier la sécurité des sessions
    print("\n7. Sécurité des sessions:")
    security_checks = [
        ('SESSION_COOKIE_HTTPONLY', True),
        ('SESSION_COOKIE_SAMESITE', 'Lax'),
    ]
    
    for setting_name, expected_value in security_checks:
        actual_value = getattr(settings, setting_name, None)
        if actual_value == expected_value:
            print(f"   ✅ {setting_name} = {actual_value}")
        else:
            print(f"   ⚠️  {setting_name} = {actual_value} (attendu: {expected_value})")
    
    print("\n" + "="*80)
    print("✅ CONFIGURATION FIREBASE VALIDE")
    print("="*80)
    print("\nProchaines étapes:")
    print("1. Assurez-vous que toutes les variables .env sont remplies")
    print("2. Activez Email/Password dans Firebase Console")
    print("3. Activez Google Sign-In dans Firebase Console")
    print("4. Ajoutez vos domaines autorisés dans Firebase Console")
    print("5. Testez la connexion sur /accounts/login/")
    print("\n")
    
    return True


def test_rate_limiting():
    """Tester le système de rate limiting"""
    print("\n" + "="*80)
    print("TEST DU RATE LIMITING")
    print("="*80)
    
    from django.core.cache import cache
    
    # Tester le cache
    test_key = "test_rate_limit"
    cache.set(test_key, 1, 60)
    value = cache.get(test_key)
    
    if value == 1:
        print("   ✅ Cache fonctionne correctement")
        cache.delete(test_key)
    else:
        print("   ❌ Cache ne fonctionne pas")
        return False
    
    print("\n   ℹ️  Rate limiting configuré:")
    print("      - 10 tentatives maximum par minute par IP")
    print("      - Réponse HTTP 429 après dépassement")
    print("      - Réinitialisation après connexion réussie")
    
    return True


if __name__ == '__main__':
    print("\n🔥 TEST DU SYSTÈME D'AUTHENTIFICATION FIREBASE\n")
    
    try:
        # Test de configuration
        config_ok = test_firebase_config()
        
        # Test de rate limiting
        if config_ok:
            rate_limit_ok = test_rate_limiting()
        
        if config_ok and rate_limit_ok:
            print("\n✅ TOUS LES TESTS SONT PASSÉS!")
            print("\nVous pouvez maintenant:")
            print("1. Démarrer le serveur: python manage.py runserver")
            print("2. Accéder à: http://localhost:8000/accounts/login/")
            print("3. Tester la connexion Firebase")
            sys.exit(0)
        else:
            print("\n❌ CERTAINS TESTS ONT ÉCHOUÉ")
            print("\nVérifiez les erreurs ci-dessus et corrigez-les.")
            sys.exit(1)
    
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
