#!/usr/bin/env python
"""
Script pour donner le rôle ADMIN à tatchida@gmail.com
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

def donner_admin():
    try:
        # Trouver l'utilisateur
        user = User.objects.get(email='tatchida@gmail.com')
        
        print(f"📧 Utilisateur trouvé: {user.email}")
        print(f"   Rôle actuel: {user.get_role_display()}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        
        # Mettre à jour les permissions
        user.role = 'ADMIN'
        user.is_staff = True
        user.is_superuser = True
        user.region = None  # Les admins n'ont pas de région
        user.save()
        
        print("\n" + "=" * 60)
        print("✅ RÔLE ADMIN ATTRIBUÉ AVEC SUCCÈS!")
        print("=" * 60)
        print(f"\n📧 Email: {user.email}")
        print(f"   Nouveau rôle: {user.get_role_display()}")
        print(f"   Staff: {user.is_staff}")
        print(f"   Superuser: {user.is_superuser}")
        print(f"   Région: {user.region or 'Aucune (accès national)'}")
        
        print("\n" + "=" * 60)
        print("🎯 VOUS POUVEZ MAINTENANT:")
        print("=" * 60)
        print("\n1. Gérer tous les utilisateurs:")
        print("   → http://127.0.0.1:8000/accounts/manage-users/")
        
        print("\n2. Accéder au Django Admin:")
        print("   → http://127.0.0.1:8000/admin/")
        
        print("\n3. Voir toutes les régions et données")
        
        print("\n4. Accéder au Dashboard Exécutif:")
        print("   → http://127.0.0.1:8000/executif/")
        
        print("\n" + "=" * 60)
        print("⚠️  IMPORTANT: Déconnectez-vous et reconnectez-vous")
        print("    pour que les changements prennent effet!")
        print("=" * 60)
        
    except User.DoesNotExist:
        print("❌ Erreur: Utilisateur tatchida@gmail.com non trouvé")
        print("   Connectez-vous d'abord via Firebase pour créer le compte")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    donner_admin()
