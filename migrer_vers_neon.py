"""
Script de migration de SQLite vers Neon PostgreSQL
"""
import os
import sys
import subprocess
from datetime import datetime

def run_command(command, description):
    """Exécuter une commande et afficher le résultat"""
    print(f"\n{'='*80}")
    print(f"{description}")
    print(f"{'='*80}")
    print(f"Commande: {command}\n")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.returncode != 0:
        print(f"❌ Erreur: {result.stderr}")
        return False
    
    print(f"✅ {description} - Terminé")
    return True

def main():
    print("\n" + "="*80)
    print("MIGRATION VERS NEON POSTGRESQL")
    print("="*80)
    
    print("\n⚠️  IMPORTANT:")
    print("  1. Assurez-vous d'avoir créé votre base Neon")
    print("  2. Assurez-vous d'avoir configuré le fichier .env")
    print("  3. Cette migration va:")
    print("     - Sauvegarder les données SQLite")
    print("     - Créer les tables dans Neon")
    print("     - Importer les données")
    print("     - Réimporter les indicateurs")
    
    continuer = input("\nContinuer? (o/n): ").strip().lower()
    
    if continuer != 'o':
        print("\nMigration annulée.")
        return
    
    # Étape 1: Sauvegarder les données SQLite
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_file = f"backup_sqlite_{timestamp}.json"
    
    if not run_command(
        f"python manage.py dumpdata > {backup_file}",
        "Étape 1: Sauvegarde des données SQLite"
    ):
        return
    
    print(f"\n✅ Sauvegarde créée: {backup_file}")
    
    # Étape 2: Vérifier la configuration .env
    if not os.path.exists('.env'):
        print("\n❌ Fichier .env non trouvé!")
        print("Exécutez: python setup_neon_firebase.py")
        return
    
    print("\n✅ Fichier .env trouvé")
    
    # Étape 3: Modifier settings.py pour utiliser Neon
    print("\n" + "="*80)
    print("Étape 2: Configuration de Django pour Neon")
    print("="*80)
    
    print("\nModification de config/settings.py...")
    print("Ajoutez cette ligne au début du fichier:")
    print("from config.settings_neon import *")
    
    modifier = input("\nVoulez-vous que je modifie automatiquement? (o/n): ").strip().lower()
    
    if modifier == 'o':
        try:
            with open('config/settings.py', 'r', encoding='utf-8') as f:
                content = f.read()
            
            if 'from config.settings_neon import *' not in content:
                with open('config/settings.py', 'w', encoding='utf-8') as f:
                    f.write('from config.settings_neon import *\n\n' + content)
                print("✅ Fichier modifié")
            else:
                print("✅ Déjà configuré")
        except Exception as e:
            print(f"❌ Erreur: {e}")
            return
    
    # Étape 4: Créer les tables dans Neon
    if not run_command(
        "python manage.py migrate",
        "Étape 3: Création des tables dans Neon"
    ):
        return
    
    # Étape 5: Importer les données
    if not run_command(
        f"python manage.py loaddata {backup_file}",
        "Étape 4: Importation des données"
    ):
        print("\n⚠️  L'importation a échoué. Essayons de réimporter les indicateurs...")
    
    # Étape 6: Réimporter les indicateurs
    if not run_command(
        "python import_prosmat_complet.py",
        "Étape 5: Réimportation des indicateurs"
    ):
        print("\n⚠️  Réimportation des indicateurs échouée")
    
    # Étape 7: Vérifier les données
    if not run_command(
        "python verifier_donnees.py",
        "Étape 6: Vérification des données"
    ):
        print("\n⚠️  Vérification échouée")
    
    print("\n" + "="*80)
    print("✅ MIGRATION TERMINÉE!")
    print("="*80)
    
    print("\nProchaines étapes:")
    print("  1. Vérifier que les données sont correctes")
    print("  2. Tester l'application: python manage.py runserver")
    print("  3. Si tout fonctionne, vous pouvez supprimer db.sqlite3")
    print(f"  4. Conserver la sauvegarde: {backup_file}")

if __name__ == '__main__':
    main()
