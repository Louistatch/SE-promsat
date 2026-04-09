from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """
    Administration personnalisée pour le modèle User
    Permet de gérer les rôles et régions des utilisateurs Firebase
    """
    
    # Champs affichés dans la liste
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'region', 'is_staff', 'is_active', 'created_at')
    
    # Filtres dans la sidebar
    list_filter = ('role', 'region', 'is_staff', 'is_superuser', 'is_active', 'created_at')
    
    # Champs de recherche
    search_fields = ('username', 'email', 'first_name', 'last_name')
    
    # Ordre d'affichage
    ordering = ('-created_at',)
    
    # Champs en lecture seule
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')
    
    # Organisation des champs dans le formulaire
    fieldsets = (
        ('Informations de connexion', {
            'fields': ('username', 'password')
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'email', 'telephone')
        }),
        ('Rôle et Région ProSMAT', {
            'fields': ('role', 'region'),
            'description': 'Définissez le rôle et la région de l\'utilisateur pour ProSMAT'
        }),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        ('Dates importantes', {
            'fields': ('last_login', 'date_joined', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    # Champs pour l'ajout d'un nouvel utilisateur
    add_fieldsets = (
        ('Informations de connexion', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
        ('Informations personnelles', {
            'fields': ('first_name', 'last_name', 'telephone'),
        }),
        ('Rôle et Région ProSMAT', {
            'fields': ('role', 'region'),
            'description': 'Définissez le rôle et la région de l\'utilisateur'
        }),
        ('Permissions', {
            'fields': ('is_staff', 'is_superuser'),
        }),
    )
    
    # Actions personnalisées
    actions = ['make_charge_projet', 'make_coordonnateur', 'make_evaluateur', 'make_admin']
    
    def make_charge_projet(self, request, queryset):
        """Définir les utilisateurs sélectionnés comme Chargé de Projet"""
        updated = queryset.update(role='CHARGE_PROJET')
        self.message_user(request, f'{updated} utilisateur(s) défini(s) comme Chargé de Projet.')
    make_charge_projet.short_description = "Définir comme Chargé de Projet"
    
    def make_coordonnateur(self, request, queryset):
        """Définir les utilisateurs sélectionnés comme Coordonnateur"""
        updated = queryset.update(role='COORDONNATEUR')
        self.message_user(request, f'{updated} utilisateur(s) défini(s) comme Coordonnateur.')
    make_coordonnateur.short_description = "Définir comme Coordonnateur"
    
    def make_evaluateur(self, request, queryset):
        """Définir les utilisateurs sélectionnés comme Évaluateur"""
        updated = queryset.update(role='EVALUATEUR')
        self.message_user(request, f'{updated} utilisateur(s) défini(s) comme Évaluateur.')
    make_evaluateur.short_description = "Définir comme Évaluateur"
    
    def make_admin(self, request, queryset):
        """Définir les utilisateurs sélectionnés comme Administrateur"""
        updated = queryset.update(role='ADMIN', is_staff=True)
        self.message_user(request, f'{updated} utilisateur(s) défini(s) comme Administrateur.')
    make_admin.short_description = "Définir comme Administrateur"
