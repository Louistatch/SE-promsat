"""
Backend d'authentification Firebase pour Django
"""
import firebase_admin
from firebase_admin import credentials, auth
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
from django.conf import settings
import os
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

# Initialiser Firebase Admin SDK
def initialize_firebase():
    """Initialise Firebase Admin SDK avec gestion d'erreurs"""
    if firebase_admin._apps:
        return True
    
    try:
        # Utiliser les credentials par défaut ou un fichier de service account
        cred_path = os.path.join(settings.BASE_DIR, 'firebase-credentials.json')
        
        if os.path.exists(cred_path):
            logger.info("Initialisation Firebase avec fichier credentials")
            cred = credentials.Certificate(cred_path)
            firebase_admin.initialize_app(cred)
        else:
            # Utiliser les credentials par défaut (pour Cloud Run, etc.)
            logger.info("Initialisation Firebase avec credentials par défaut")
            firebase_admin.initialize_app()
        
        logger.info("Firebase Admin SDK initialisé avec succès")
        return True
    except Exception as e:
        logger.error(f"Erreur lors de l'initialisation de Firebase: {e}")
        return False

# Initialiser au chargement du module
initialize_firebase()


class FirebaseAuthenticationBackend(BaseBackend):
    """
    Backend d'authentification Firebase
    """
    
    def authenticate(self, request, firebase_token=None, **kwargs):
        """
        Authentifier un utilisateur avec un token Firebase
        """
        if not firebase_token:
            return None
        
        # Vérifier que Firebase est initialisé
        if not firebase_admin._apps:
            logger.error("Firebase Admin SDK n'est pas initialisé")
            return None
        
        try:
            # Vérifier le token Firebase
            decoded_token = auth.verify_id_token(firebase_token)
            uid = decoded_token['uid']
            email = decoded_token.get('email', '')
            name = decoded_token.get('name', '')
            email_verified = decoded_token.get('email_verified', False)
            
            if not email:
                logger.warning("Email manquant dans le token Firebase")
                return None
            
            # Vérifier que l'email est vérifié (optionnel mais recommandé)
            if not email_verified:
                logger.warning(f"Email non vérifié pour {email}")
                # Vous pouvez choisir de bloquer ou autoriser les emails non vérifiés
                # return None  # Décommentez pour bloquer les emails non vérifiés
            
            # Chercher l'utilisateur par email
            try:
                user = User.objects.get(email=email)
                logger.info(f"Utilisateur trouvé: {user.email}")
            except User.DoesNotExist:
                # Créer un nouvel utilisateur
                # Générer un username unique basé sur l'email
                base_username = email.split('@')[0]
                username = base_username
                counter = 1
                
                # S'assurer que le username est unique
                while User.objects.filter(username=username).exists():
                    username = f"{base_username}{counter}"
                    counter += 1
                
                # Extraire le prénom et nom du name
                first_name = ''
                last_name = ''
                if name:
                    name_parts = name.split()
                    first_name = name_parts[0] if name_parts else ''
                    last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                # Créer l'utilisateur
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    first_name=first_name,
                    last_name=last_name,
                )
                logger.info(f"Nouvel utilisateur créé: {user.email} (username: {user.username})")
            
            return user
            
        except auth.InvalidIdTokenError as e:
            logger.error(f"Token Firebase invalide: {e}")
            return None
        except auth.ExpiredIdTokenError as e:
            logger.error(f"Token Firebase expiré: {e}")
            return None
        except Exception as e:
            logger.error(f"Erreur d'authentification Firebase: {e}", exc_info=True)
            return None
    
    def get_user(self, user_id):
        """
        Récupérer un utilisateur par son ID
        """
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def verify_firebase_token(token):
    """
    Vérifier un token Firebase et retourner les informations de l'utilisateur
    """
    if not firebase_admin._apps:
        logger.error("Firebase Admin SDK n'est pas initialisé")
        return None
    
    try:
        decoded_token = auth.verify_id_token(token)
        return {
            'uid': decoded_token['uid'],
            'email': decoded_token.get('email', ''),
            'name': decoded_token.get('name', ''),
            'email_verified': decoded_token.get('email_verified', False),
        }
    except Exception as e:
        logger.error(f"Erreur de vérification du token: {e}")
        return None


def create_firebase_user(email, password, display_name=None):
    """
    Créer un utilisateur Firebase
    """
    if not firebase_admin._apps:
        logger.error("Firebase Admin SDK n'est pas initialisé")
        return None
    
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name,
        )
        logger.info(f"Utilisateur Firebase créé: {email}")
        return user
    except Exception as e:
        logger.error(f"Erreur de création d'utilisateur Firebase: {e}")
        return None


def update_firebase_user(uid, **kwargs):
    """
    Mettre à jour un utilisateur Firebase
    """
    if not firebase_admin._apps:
        logger.error("Firebase Admin SDK n'est pas initialisé")
        return None
    
    try:
        user = auth.update_user(uid, **kwargs)
        logger.info(f"Utilisateur Firebase mis à jour: {uid}")
        return user
    except Exception as e:
        logger.error(f"Erreur de mise à jour d'utilisateur Firebase: {e}")
        return None


def delete_firebase_user(uid):
    """
    Supprimer un utilisateur Firebase
    """
    if not firebase_admin._apps:
        logger.error("Firebase Admin SDK n'est pas initialisé")
        return False
    
    try:
        auth.delete_user(uid)
        logger.info(f"Utilisateur Firebase supprimé: {uid}")
        return True
    except Exception as e:
        logger.error(f"Erreur de suppression d'utilisateur Firebase: {e}")
        return False
