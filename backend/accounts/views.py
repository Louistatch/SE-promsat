from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from .models import User
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
import json

def login_view(request):
    """Vue de connexion Django classique (backup)"""
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Bienvenue {user.get_full_name() or user.username}!')
            return redirect('dashboard:home')
        else:
            messages.error(request, 'Identifiants invalides.')
    
    return render(request, 'accounts/login.html')

def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('accounts:login')

@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    return render(request, 'accounts/profile.html', {
        'user': request.user
    })

# Vérification des permissions
def is_admin(user):
    """Vérifie si l'utilisateur est administrateur"""
    return user.is_authenticated and user.role == 'ADMIN'

def is_coordonnateur_or_above(user):
    """Vérifie si l'utilisateur est coordonnateur ou plus"""
    return user.is_authenticated and user.role in ['COORDONNATEUR', 'EVALUATEUR', 'ADMIN']

@login_required
@user_passes_test(is_admin)
def manage_users_view(request):
    """Vue de gestion des utilisateurs (réservée aux admins)"""
    users = User.objects.all().order_by('-created_at')
    
    context = {
        'users': users,
        'role_choices': User.ROLE_CHOICES,
        'region_choices': User.REGION_CHOICES,
    }
    
    return render(request, 'accounts/manage_users.html', context)

@login_required
@user_passes_test(is_admin)
@require_http_methods(["POST"])
def update_user_role(request):
    """API pour mettre à jour le rôle d'un utilisateur"""
    try:
        data = json.loads(request.body)
        user_id = data.get('user_id')
        new_role = data.get('role')
        new_region = data.get('region')
        
        user = User.objects.get(id=user_id)
        
        if new_role:
            user.role = new_role
        
        if new_region:
            user.region = new_region
        
        user.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Rôle mis à jour pour {user.email}'
        })
    
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'error': 'Utilisateur non trouvé'
        }, status=404)
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
