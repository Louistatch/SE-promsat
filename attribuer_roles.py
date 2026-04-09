"""
Script pour attribuer les rôles aux utilisateurs Firebase
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

print("\n" + "="*80)
print("🎭 ATTRIBUTION DES RÔLES AUX UTILISATEURS FIREBASE")
print("="*80)

# Configuration des rôles par email
# Modifiez cette section selon vos besoins
roles_mapping = {
    # Format: 'email@example.com': ('ROLE', 'REGION ou None'),
    
    # Administrateurs (accès complet, pas de région)
    'tatchida@gmail.com': ('ADMIN', None),
    
    # Coordonnateurs (toutes régions, pas de région spécifique)
    # 'coordo@prosmat.tg': ('COORDONNATEUR', None),
    
    # Évaluateurs (toutes régions, pas de région spécifique)
    # 'eval@prosmat.tg': ('EVALUATEUR', None),
    
    # Chargés de Projet (région spécifique obligatoire)
    # 'charge.maritime@prosmat.tg': ('CHARGE_PROJET', 'MARITIME'),
    # 'charge.plateaux@prosmat.tg': ('CHARGE_PROJET', 'PLATEAUX'),
    # 'charge.centrale@prosmat.tg': ('CHARGE_PROJET', 'CENTRALE'),
    # 'charge.kara@prosmat.tg': ('CHARGE_PROJET', 'KARA'),
    # 'charge.savanes@prosmat.tg': ('CHARGE_PROJET', 'SAVANES'),
}

print("\n📋 Configuration à appliquer:")
print("-" * 80)
for email, (role, region) in roles_mapping.items():
    region_str = region if region else "Aucune région"
    print(f"  • {email}")
    print(f"    → Rôle: {role}")
    print(f"    → Région: {region_str}")
print("-" * 80)

# Demander confirmation
response = input("\n⚠️  Voulez-vous appliquer ces changements? (oui/non): ").strip().lower()

if response not in ['oui', 'o', 'yes', 'y']:
    print("\n❌ Opération annulée.")
    sys.exit(0)

print("\n🔄 Application des changements...")
print("-" * 80)

success_count = 0
not_found_count = 0
error_count = 0

for email, (role, region) in roles_mapping.items():
    try:
        user = User.objects.get(email=email)
        
        # Sauvegarder l'ancien rôle pour affichage
        old_role = user.get_role_display()
        old_region = user.get_region_display() if user.region else "Aucune"
        
        # Appliquer les changements
        user.role = role
        if region:
            user.region = region
        else:
            user.region = None
        
        # Si ADMIN, donner aussi les permissions staff
        if role == 'ADMIN':
            user.is_staff = True
        
        user.save()
        
        new_role = user.get_role_display()
        new_region = user.get_region_display() if user.region else "Aucune"
        
        print(f"\n✅ {email}")
        print(f"   Ancien: {old_role} - {old_region}")
        print(f"   Nouveau: {new_role} - {new_region}")
        
        success_count += 1
        
    except User.DoesNotExist:
        print(f"\n❌ {email}")
        print(f"   Utilisateur non trouvé dans la base de données")
        print(f"   💡 L'utilisateur doit se connecter au moins une fois via Firebase")
        not_found_count += 1
        
    except Exception as e:
        print(f"\n❌ {email}")
        print(f"   Erreur: {e}")
        error_count += 1

print("\n" + "="*80)
print("📊 RÉSUMÉ")
print("="*80)
print(f"✅ Succès: {success_count}")
print(f"❌ Non trouvés: {not_found_count}")
print(f"⚠️  Erreurs: {error_count}")
print(f"📝 Total: {len(roles_mapping)}")

if not_found_count > 0:
    print("\n💡 CONSEIL:")
    print("   Les utilisateurs non trouvés doivent se connecter au moins une fois")
    print("   via Firebase pour que leur compte soit créé dans Django.")

print("\n" + "="*80)
print("✅ OPÉRATION TERMINÉE")
print("="*80)

# Afficher tous les utilisateurs actuels
print("\n📋 LISTE ACTUELLE DES UTILISATEURS:")
print("-" * 80)

all_users = User.objects.all().order_by('role', 'email')

if all_users:
    for user in all_users:
        role_display = user.get_role_display()
        region_display = user.get_region_display() if user.region else "Aucune région"
        staff_badge = " [STAFF]" if user.is_staff else ""
        print(f"  • {user.email}")
        print(f"    → {role_display} - {region_display}{staff_badge}")
else:
    print("  Aucun utilisateur trouvé")

print("-" * 80)
print(f"\nTotal: {all_users.count()} utilisateur(s)")
print("\n")
