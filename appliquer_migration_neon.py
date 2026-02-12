"""
Appliquer les migrations Django sur Neon
"""
import os
import sys

# Forcer l'utilisation de Neon
os.environ['DATABASE_URL'] = 'postgresql://neondb_owner:npg_KAWbvj8u0HlY@ep-little-morning-ab9ty32l-pooler.eu-west-2.aws.neon.tech/neondb?sslmode=require'

import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Override database config
from django.conf import settings
import dj_database_url
settings.DATABASES['default'] = dj_database_url.config(
    default=os.environ['DATABASE_URL'],
    conn_max_age=600
)

from django.core.management import call_command
from django.db import connection

print("=" * 70)
print("APPLICATION DES MIGRATIONS SUR NEON")
print("=" * 70)

# Vérifier la connexion
with connection.cursor() as cursor:
    cursor.execute("SELECT current_database();")
    db_name = cursor.fetchone()[0]
    print(f"\n✅ Connecté à: {db_name}")

print("\n📋 Migrations à appliquer:")
print("   - monitoring.0003_alter_indicateur_sous_composante")
print("     (Rendre sous_composante optionnel)")

reponse = input("\nAppliquer les migrations? (O/n): ")
if reponse.lower() in ['n', 'non']:
    print("❌ Annulé")
    sys.exit(0)

print("\n🔄 Application des migrations...")
try:
    call_command('migrate', verbosity=2)
    print("\n✅ Migrations appliquées avec succès!")
except Exception as e:
    print(f"\n❌ Erreur: {e}")
    sys.exit(1)

print("\n" + "=" * 70)
print("✅ NEON EST PRÊT POUR L'IMPORT")
print("=" * 70)
print("\nMaintenant vous pouvez exécuter:")
print("   python migrer_vers_neon_complet.py")
