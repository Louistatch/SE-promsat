"""
Script de migration rapide vers Neon PostgreSQL
"""
import os
import sys
import django

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Charger les variables d'environnement
from decouple import config

print("\n" + "="*80)
print("MIGRATION RAPIDE VERS NEON POSTGRESQL")
print("="*80)

print("\n✅ Connexion Neon configurée:")
print(f"   Base: neondb")
print(f"   Région: eu-west-2 (Europe)")

# Vérifier que .env existe
if not os.path.exists('.env'):
    print("\n❌ Fichier .env non trouvé!")
    sys.exit(1)

print("\n✅ Fichier .env trouvé")

# Modifier settings.py pour utiliser Neon
print("\n" + "="*80)
print("ÉTAPE 1: Configuration de Django")
print("="*80)

settings_path = 'config/settings.py'

try:
    with open(settings_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Vérifier si déjà configuré
    if 'dj_database_url' in content and 'decouple' in content:
        print("✅ Django déjà configuré pour Neon")
    else:
        # Ajouter les imports nécessaires
        if 'from decouple import config' not in content:
            # Trouver la ligne des imports
            lines = content.split('\n')
            import_index = 0
            for i, line in enumerate(lines):
                if line.startswith('from pathlib import Path'):
                    import_index = i + 1
                    break
            
            lines.insert(import_index, 'import dj_database_url')
            lines.insert(import_index + 1, 'from decouple import config')
            content = '\n'.join(lines)
        
        # Remplacer la configuration de la base de données
        if 'DATABASES = {' in content:
            # Trouver et remplacer la section DATABASES
            start = content.find('DATABASES = {')
            end = content.find('}', start) + 1
            
            # Trouver la vraie fin (peut avoir plusieurs niveaux)
            bracket_count = 0
            for i in range(start, len(content)):
                if content[i] == '{':
                    bracket_count += 1
                elif content[i] == '}':
                    bracket_count -= 1
                    if bracket_count == 0:
                        end = i + 1
                        break
            
            new_db_config = """DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}"""
            
            content = content[:start] + new_db_config + content[end:]
        
        # Sauvegarder
        with open(settings_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("✅ Configuration Django mise à jour")

except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

# Maintenant on peut importer Django
django.setup()

from django.core.management import call_command
from monitoring.models import Indicateur, Periode, Composante

print("\n" + "="*80)
print("ÉTAPE 2: Sauvegarde des données SQLite")
print("="*80)

try:
    from datetime import datetime
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_sqlite_{timestamp}.json"
    
    print(f"Création de la sauvegarde: {backup_file}")
    call_command('dumpdata', output=backup_file, indent=2)
    print(f"✅ Sauvegarde créée: {backup_file}")
except Exception as e:
    print(f"⚠️  Erreur de sauvegarde: {e}")
    print("Continuons quand même...")

print("\n" + "="*80)
print("ÉTAPE 3: Création des tables dans Neon")
print("="*80)

try:
    print("Exécution des migrations...")
    call_command('migrate', verbosity=1)
    print("✅ Tables créées dans Neon")
except Exception as e:
    print(f"❌ Erreur: {e}")
    sys.exit(1)

print("\n" + "="*80)
print("ÉTAPE 4: Importation des indicateurs")
print("="*80)

try:
    # Vérifier si les données existent déjà
    nb_indicateurs = Indicateur.objects.count()
    
    if nb_indicateurs > 0:
        print(f"⚠️  {nb_indicateurs} indicateurs déjà présents dans Neon")
        reponse = input("Voulez-vous réimporter? (o/n): ").strip().lower()
        if reponse != 'o':
            print("Import annulé")
        else:
            print("Réimportation des indicateurs...")
            os.system('python import_prosmat_complet.py')
    else:
        print("Importation des indicateurs...")
        os.system('python import_prosmat_complet.py')
    
except Exception as e:
    print(f"⚠️  Erreur: {e}")

print("\n" + "="*80)
print("ÉTAPE 5: Vérification")
print("="*80)

try:
    nb_indicateurs = Indicateur.objects.count()
    nb_periodes = Periode.objects.count()
    nb_composantes = Composante.objects.count()
    
    print(f"\n✅ Données dans Neon:")
    print(f"   Indicateurs: {nb_indicateurs}")
    print(f"   Périodes: {nb_periodes}")
    print(f"   Composantes: {nb_composantes}")
    
    if nb_indicateurs == 75:
        print("\n🎉 MIGRATION RÉUSSIE!")
    else:
        print(f"\n⚠️  Attendu: 75 indicateurs, Trouvé: {nb_indicateurs}")
        print("Exécutez: python import_prosmat_complet.py")

except Exception as e:
    print(f"❌ Erreur: {e}")

print("\n" + "="*80)
print("PROCHAINES ÉTAPES")
print("="*80)

print("\n1. Tester la connexion:")
print("   python manage.py dbshell")

print("\n2. Démarrer l'application:")
print("   python manage.py runserver")

print("\n3. Accéder à l'application:")
print("   http://localhost:8000")

print("\n4. Pour Firebase Authentication:")
print("   - Créer un projet sur https://console.firebase.google.com")
print("   - Remplir les variables FIREBASE_* dans .env")
print("   - Consulter: GUIDE_MIGRATION_COMPLET.md")

print("\n" + "="*80)
