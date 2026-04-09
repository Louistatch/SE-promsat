"""
Script pour migrer les données de SQLite vers Neon PostgreSQL
"""
import os
import django
import json
from datetime import datetime

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from django.core import serializers
from monitoring.models import Composante, SousComposante, Indicateur, Periode, Realisation
from accounts.models import User

def exporter_donnees_sqlite():
    """Exporter toutes les données de SQLite vers un fichier JSON"""
    print("=" * 60)
    print("EXPORT DES DONNÉES SQLITE")
    print("=" * 60)
    
    # Créer un backup
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"backup_sqlite_{timestamp}.json"
    
    # Exporter toutes les données
    data = []
    
    models_to_export = [
        ('accounts.User', User),
        ('monitoring.Composante', Composante),
        ('monitoring.SousComposante', SousComposante),
        ('monitoring.Indicateur', Indicateur),
        ('monitoring.Periode', Periode),
        ('monitoring.Realisation', Realisation),
    ]
    
    for model_name, model_class in models_to_export:
        count = model_class.objects.count()
        print(f"\n📦 Export {model_name}: {count} objets")
        
        for obj in model_class.objects.all():
            data.append({
                'model': model_name.lower(),
                'pk': obj.pk,
                'fields': serializers.serialize('python', [obj])[0]['fields']
            })
    
    # Sauvegarder dans un fichier
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"\n✅ Données exportées vers: {filename}")
    print(f"📊 Total: {len(data)} objets")
    
    return filename

def importer_vers_neon(filename):
    """
    Importer les données vers Neon
    
    ATTENTION: Exécutez ce script APRÈS avoir configuré DATABASE_URL pour Neon
    """
    print("\n" + "=" * 60)
    print("IMPORT VERS NEON")
    print("=" * 60)
    print("\n⚠️  IMPORTANT:")
    print("1. Configurez DATABASE_URL vers Neon dans .env")
    print("2. Exécutez: python manage.py migrate")
    print("3. Puis exécutez ce script avec l'option --import")
    print("\nCommande:")
    print(f"   python migrer_sqlite_vers_neon.py --import {filename}")

if __name__ == '__main__':
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == '--import':
        if len(sys.argv) > 2:
            filename = sys.argv[2]
            importer_vers_neon(filename)
        else:
            print("❌ Erreur: Spécifiez le fichier à importer")
            print("Usage: python migrer_sqlite_vers_neon.py --import backup_sqlite_XXXXXX.json")
    else:
        # Export par défaut
        filename = exporter_donnees_sqlite()
        print("\n" + "=" * 60)
        print("PROCHAINES ÉTAPES")
        print("=" * 60)
        print("\n1. Gardez ce fichier en sécurité:")
        print(f"   {filename}")
        print("\n2. Si vous voulez migrer vers Neon:")
        print("   a. Configurez DATABASE_URL vers Neon")
        print("   b. python manage.py migrate")
        print(f"   c. python migrer_sqlite_vers_neon.py --import {filename}")
        print("\n3. Ou laissez charger_donnees créer de nouvelles données")
