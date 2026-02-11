"""
Vues pour l'authentification Firebase
"""
import json
import logging
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django.conf import settings
from .firebase_auth import FirebaseAuthenticationBackend
from django.core.cache import cache
from django.utils import timezone
from datetime import timedelta

logger = logging.getLogger(__name__)

def login_firebase_view(request):
    """
    Page de connexion avec Firebase
    """
    if request.user.is_authenticated:
        return redirect('dashboard:home')
    
    context = {
        'firebase_config': settings.FIREBASE_CONFIG
    }
    return render(request, 'accounts/login_firebase.html', context)

@csrf_exempt
@require_http_methods(["POST"])
@never_cache
def firebase_login_api(request):
    """
    API pour authentifier un utilisateur avec un token Firebase
    Avec rate limiting pour prévenir les attaques par force brute
    """
    # Rate limiting: 10 tentatives par IP par minute
    client_ip = get_client_ip(request)
    rate_limit_key = f"login_attempts_{client_ip}"
    attempts = cache.get(rate_limit_key, 0)
    
    if attempts >= 10:
        logger.warning(f"Trop de tentatives de connexion depuis {client_ip}")
        return JsonResponse({
            'error': 'Trop de tentatives. Veuillez réessayer dans quelques minutes.'
        }, status=429)
    
    try:
        data = json.loads(request.body)
        id_token = data.get('idToken')
        
        logger.info(f"Tentative de connexion Firebase depuis {client_ip}")
        
        if not id_token:
            logger.warning("Token manquant dans la requête")
            increment_rate_limit(rate_limit_key, attempts)
            return JsonResponse({'error': 'Token manquant'}, status=400)
        
        # Authentifier avec Firebase
        backend = FirebaseAuthenticationBackend()
        user = backend.authenticate(request, firebase_token=id_token)
        
        if user:
            logger.info(f"Authentification réussie pour: {user.email}")
            
            # Réinitialiser le compteur de tentatives
            cache.delete(rate_limit_key)
            
            # Connecter l'utilisateur Django
            login(request, user, backend='accounts.firebase_auth.FirebaseAuthenticationBackend')
            
            logger.info(f"Utilisateur connecté: {user.username} (ID: {user.id})")
            
            return JsonResponse({
                'success': True,
                'user': {
                    'id': user.id,
                    'email': user.email,
                    'username': user.username,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role,
                }
            })
        else:
            logger.warning(f"Authentification échouée depuis {client_ip}")
            increment_rate_limit(rate_limit_key, attempts)
            return JsonResponse({
                'error': 'Authentification échouée. Vérifiez vos identifiants.'
            }, status=401)
    
    except json.JSONDecodeError as e:
        logger.error(f"Erreur JSON: {e}")
        increment_rate_limit(rate_limit_key, attempts)
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        logger.error(f"Erreur inattendue: {e}", exc_info=True)
        increment_rate_limit(rate_limit_key, attempts)
        return JsonResponse({
            'error': 'Erreur serveur. Veuillez réessayer.'
        }, status=500)


def get_client_ip(request):
    """Récupérer l'adresse IP du client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def increment_rate_limit(key, current_attempts):
    """Incrémenter le compteur de tentatives avec expiration"""
    cache.set(key, current_attempts + 1, 60)  # Expire après 60 secondes

@login_required
def logout_view(request):
    """
    Déconnexion
    """
    logout(request)
    return redirect('accounts:login-firebase')
