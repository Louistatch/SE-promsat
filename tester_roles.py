#!/usr/bin/env python
"""
Script de test pour le système de gestion des rôles Firebase
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

def tester_roles():
    print("=" * 60)
    print("TEST DU SYSTÈME DE GESTION DES RÔLES")
    print("=" * 60)
    
    # 1. Lister tous les utilisateurs
    users = User.objects.all()
    print(f"\n✓ Nombre total d'utilisateurs: {users.count()}")
    
    if users.count() == 0:
        print("\n⚠ Aucun utilisateur trouvé dans la base de données.")
        print("Connectez-vous d'abord via Firebase pour créer un utilisateur.")
        return
    
    # 2. Afficher les utilisateurs avec leurs rôles
    print("\n" + "=" * 60)
    print("LISTE DES UTILISATEURS ET LEURS RÔLES")
    print("=" * 60)
    
    for user in users:
        print(f"\n📧 Email: {user.email}")
        print(f"   Nom: {user.get_full_name() or 'Non défini'}")
        print(f"   Rôle: {user.get_role_display()}")
        print(f"   Région: {user.get_region_display() if user.region else 'Non définie'}")
        print(f"   Staff: {'Oui' if user.is_staff else 'Non'}")
        print(f"   Superuser: {'Oui' if user.is_superuser else 'Non'}")
        print(f"   Créé le: {user.created_at.strftime('%d/%m/%Y %H:%M')}")
    
    # 3. Statistiques par rôle
    print("\n" + "=" * 60)
    print("STATISTIQUES PAR RÔLE")
    print("=" * 60)
    
    for role_code, role_name in User.ROLE_CHOICES:
        count = User.objects.filter(role=role_code).count()
        print(f"   {role_name}: {count}")
    
    # 4. Statistiques par région
    print("\n" + "=" * 60)
    print("STATISTIQUES PAR RÉGION")
    print("=" * 60)
    
    for region_code, region_name in User.REGION_CHOICES:
        count = User.objects.filter(region=region_code).count()
        print(f"   {region_name}: {count}")
    
    print("\n" + "=" * 60)
    print("ACCÈS AUX INTERFACES DE GESTION")
    print("=" * 60)
    print("\n1. Interface Web de gestion:")
    print("   URL: http://127.0.0.1:8000/accounts/manage-users/")
    print("   Accès: Réservé aux administrateurs (role=ADMIN)")
    
    print("\n2. Interface Django Admin:")
    print("   URL: http://127.0.0.1:8000/admin/accounts/user/")
    print("   Accès: Utilisateurs avec is_staff=True")
    
    print("\n3. Script Python:")
    print("   Commande: python attribuer_roles.py")
    print("   Accès: Ligne de commande")
    
    print("\n" + "=" * 60)
    print("✓ Test terminé avec succès!")
    print("=" * 60)

if __name__ == '__main__':
    try:
        tester_roles()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
