"""
Script de configuration pour Neon PostgreSQL et Firebase Authentication
"""
import os
import sys

def create_env_file():
    """Créer le fichier .env avec les variables nécessaires"""
    
    print("\n" + "="*80)
    print("CONFIGURATION NEON POSTGRESQL + FIREBASE")
    print("="*80)
    
    print("\n📋 Ce script va créer votre fichier .env")
    print("Vous aurez besoin de:")
    print("  1. Votre chaîne de connexion Neon PostgreSQL")
    print("  2. Vos identifiants Firebase")
    
    input("\nAppuyez sur Entrée pour continuer...")
    
    # Neon PostgreSQL
    print("\n" + "="*80)
    print("1. NEON POSTGRESQL")
    print("="*80)
    print("\nAllez sur: https://neon.tech")
    print("Créez un projet et copiez la chaîne de connexion")
    print("\nExemple:")
    print("postgresql://user:password@ep-name-123.region.aws.neon.tech/dbname?sslmode=require")
    
    database_url = input("\nCollez votre DATABASE_URL: ").strip()
    
    # Firebase
    print("\n" + "="*80)
    print("2. FIREBASE AUTHENTICATION")
    print("="*80)
    print("\nAllez sur: https://console.firebase.google.com")
    print("Créez un projet et récupérez la configuration Web")
    
    firebase_api_key = input("\nFirebase API Key: ").strip()
    firebase_auth_domain = input("Firebase Auth Domain: ").strip()
    firebase_project_id = input("Firebase Project ID: ").strip()
    firebase_storage_bucket = input("Firebase Storage Bucket: ").strip()
    firebase_messaging_sender_id = input("Firebase Messaging Sender ID: ").strip()
    firebase_app_id = input("Firebase App ID: ").strip()
    
    # Django
    print("\n" + "="*80)
    print("3. DJANGO CONFIGURATION")
    print("="*80)
    
    import secrets
    secret_key = secrets.token_urlsafe(50)
    print(f"\nSecret Key générée automatiquement: {secret_key[:20]}...")
    
    debug = input("\nMode DEBUG (True/False) [True]: ").strip() or "True"
    allowed_hosts = input("ALLOWED_HOSTS (séparés par des virgules) [localhost,127.0.0.1]: ").strip() or "localhost,127.0.0.1"
    
    # Créer le fichier .env
    env_content = f"""# Neon PostgreSQL
DATABASE_URL={database_url}

# Django
SECRET_KEY={secret_key}
DEBUG={debug}
ALLOWED_HOSTS={allowed_hosts}

# Firebase Authentication
FIREBASE_API_KEY={firebase_api_key}
FIREBASE_AUTH_DOMAIN={firebase_auth_domain}
FIREBASE_PROJECT_ID={firebase_project_id}
FIREBASE_STORAGE_BUCKET={firebase_storage_bucket}
FIREBASE_MESSAGING_SENDER_ID={firebase_messaging_sender_id}
FIREBASE_APP_ID={firebase_app_id}
"""
    
    with open('.env', 'w', encoding='utf-8') as f:
        f.write(env_content)
    
    print("\n" + "="*80)
    print("✅ Fichier .env créé avec succès!")
    print("="*80)
    print("\nProchaines étapes:")
    print("  1. Installer les dépendances: pip install -r requirements.txt")
    print("  2. Exporter les données: python manage.py dumpdata > backup.json")
    print("  3. Migrer vers Neon: python manage.py migrate")
    print("  4. Importer les données: python manage.py loaddata backup.json")
    print("  5. Tester: python manage.py runserver")

def install_dependencies():
    """Installer les dépendances nécessaires"""
    
    print("\n" + "="*80)
    print("INSTALLATION DES DÉPENDANCES")
    print("="*80)
    
    dependencies = [
        'psycopg2-binary',
        'dj-database-url',
        'python-decouple',
        'firebase-admin',
    ]
    
    print("\nDépendances à installer:")
    for dep in dependencies:
        print(f"  - {dep}")
    
    install = input("\nInstaller maintenant? (o/n): ").strip().lower()
    
    if install == 'o':
        import subprocess
        for dep in dependencies:
            print(f"\nInstallation de {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep])
        
        print("\n✅ Toutes les dépendances sont installées!")
    else:
        print("\nVous pouvez les installer plus tard avec:")
        print("pip install psycopg2-binary dj-database-url python-decouple firebase-admin")

def main():
    """Fonction principale"""
    
    print("\n" + "="*80)
    print("ASSISTANT DE CONFIGURATION")
    print("Neon PostgreSQL + Firebase Authentication")
    print("="*80)
    
    print("\nQue voulez-vous faire?")
    print("  1. Créer le fichier .env")
    print("  2. Installer les dépendances")
    print("  3. Les deux")
    print("  4. Quitter")
    
    choix = input("\nVotre choix (1-4): ").strip()
    
    if choix == '1':
        create_env_file()
    elif choix == '2':
        install_dependencies()
    elif choix == '3':
        install_dependencies()
        create_env_file()
    else:
        print("\nAu revoir!")
        return
    
    print("\n" + "="*80)
    print("Configuration terminée!")
    print("="*80)
    print("\nConsultez GUIDE_NEON_FIREBASE.md pour plus de détails.")

if __name__ == '__main__':
    main()
