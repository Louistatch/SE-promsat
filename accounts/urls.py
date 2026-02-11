from django.urls import path
from . import views
from .views_firebase import login_firebase_view, firebase_login_api, logout_view as firebase_logout_view

app_name = 'accounts'

urlpatterns = [
    # Authentification Firebase (principale)
    path('login/', login_firebase_view, name='login'),
    path('login-firebase/', login_firebase_view, name='login-firebase'),
    path('firebase-login/', firebase_login_api, name='firebase-login-api'),
    path('logout/', firebase_logout_view, name='logout'),
    path('logout-firebase/', firebase_logout_view, name='logout-firebase'),
    
    # Authentification Django classique (backup)
    path('login-django/', views.login_view, name='login-django'),
    path('logout-django/', views.logout_view, name='logout-django'),
    path('profile/', views.profile_view, name='profile'),
    
    # Gestion des utilisateurs et rôles
    path('manage-users/', views.manage_users_view, name='manage-users'),
    path('update-user-role/', views.update_user_role, name='update-user-role'),
]
