"""
Script pour vérifier les données dans Neon PostgreSQL
"""
import os
import django

# Configuration Django pour utiliser Neon
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings_production')
django.setup()

from monitoring.models import Composante, SousComposante, Indicateur, Periode, Realisation
from accounts.models import User
from django.db import connection

def verifier_connexion():
    """Vérifier la connexion à la base de données"""
    print("=" * 60)
    print("VÉRIFICATION CONNEXION BASE DE DONNÉES")
    print("=" * 60)
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print(f"\n✅ Connexion réussie!")
            print(f"📊 Version PostgreSQL: {version[:50]}...")
            
            # Afficher le nom de la base
            cursor.execute("SELECT current_database();")
            db_name = cursor.fetchone()[0]
            print(f"🗄️  Base de données: {db_name}")
            
            # Afficher l'hôte
            cursor.execute("SELECT inet_server_addr();")
            try:
                host = cursor.fetchone()[0]
                print(f"🌐 Serveur: {host}")
            except:
                print(f"🌐 Serveur: Neon (pooler)")
            
            return True
    except Exception as e:
        print(f"\n❌ Erreur de connexion: {e}")
        return False

def compter_donnees():
    """Compter les données dans chaque table"""
    print("\n" + "=" * 60)
    print("COMPTAGE DES DONNÉES")
    print("=" * 60)
    
    tables = [
        ("Utilisateurs", User),
        ("Composantes", Composante),
        ("Sous-composantes", SousComposante),
        ("Indicateurs", Indicateur),
        ("Périodes", Periode),
        ("Réalisations", Realisation),
    ]
    
    total = 0
    for nom, model in tables:
        count = model.objects.count()
        total += count
        status = "✅" if count > 0 else "⚠️ "
        print(f"{status} {nom:20} : {count:5} enregistrements")
    
    print(f"\n📊 TOTAL: {total} enregistrements")
    return total

def afficher_exemples():
    """Afficher quelques exemples de données"""
    print("\n" + "=" * 60)
    print("EXEMPLES DE DONNÉES")
    print("=" * 60)
    
    # Composantes
    print("\n📦 Composantes:")
    for comp in Composante.objects.all()[:3]:
        print(f"   - {comp.nom}")
    
    # Indicateurs
    print("\n📊 Indicateurs:")
    for ind in Indicateur.objects.all()[:3]:
        print(f"   - {ind.code}: {ind.libelle[:50]}")
    
    # Utilisateurs
    print("\n👥 Utilisateurs:")
    for user in User.objects.all()[:5]:
        role = user.get_role_display() if hasattr(user, 'get_role_display') else user.role
        print(f"   - {user.email:30} | {role:15} | Staff: {user.is_staff}")
    
    # Périodes
    print("\n📅 Périodes:")
    for per in Periode.objects.all()[:5]:
        print(f"   - {per}")

def verifier_admins():
    """Vérifier les comptes admin"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION COMPTES ADMIN")
    print("=" * 60)
    
    admin_emails = ['tatchida@gmail.com', 'admin@prosmat.tg']
    
    for email in admin_emails:
        try:
            user = User.objects.get(email=email)
            print(f"\n✅ {email}")
            print(f"   Username: {user.username}")
            print(f"   Rôle: {user.role}")
            print(f"   Staff: {user.is_staff}")
            print(f"   Superuser: {user.is_superuser}")
        except User.DoesNotExist:
            print(f"\n⚠️  {email} - Compte non trouvé")

def verifier_tables():
    """Vérifier les tables dans la base"""
    print("\n" + "=" * 60)
    print("VÉRIFICATION TABLES")
    print("=" * 60)
    
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name;
        """)
        tables = cursor.fetchall()
        
        print(f"\n📋 {len(tables)} tables trouvées:")
        for table in tables:
            print(f"   - {table[0]}")

if __name__ == '__main__':
    print("\n🔍 VÉRIFICATION BASE DE DONNÉES NEON\n")
    
    # 1. Vérifier la connexion
    if not verifier_connexion():
        print("\n❌ Impossible de se connecter à la base de données")
        print("\nVérifiez:")
        print("1. DATABASE_URL est correctement configuré dans .env")
        print("2. Vous avez exécuté: python manage.py migrate")
        exit(1)
    
    # 2. Vérifier les tables
    verifier_tables()
    
    # 3. Compter les données
    total = compter_donnees()
    
    # 4. Afficher des exemples
    if total > 0:
        afficher_exemples()
        verifier_admins()
    else:
        print("\n⚠️  AUCUNE DONNÉE TROUVÉE")
        print("\nPour charger les données initiales:")
        print("   python manage.py charger_donnees")
    
    print("\n" + "=" * 60)
    print("✅ VÉRIFICATION TERMINÉE")
    print("=" * 60)
