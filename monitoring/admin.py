from django.contrib import admin
from .models import (
    Composante, SousComposante, Indicateur, Periode, 
    Realisation, Activite, Rapport, AlerteQualite
)

@admin.register(Composante)
class ComposanteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'ordre']
    list_editable = ['ordre']
    search_fields = ['nom', 'description']

class SousComposanteInline(admin.TabularInline):
    model = SousComposante
    extra = 1

@admin.register(SousComposante)
class SousComposanteAdmin(admin.ModelAdmin):
    list_display = ['nom', 'composante', 'ordre']
    list_filter = ['composante']
    list_editable = ['ordre']
    search_fields = ['nom', 'description']

@admin.register(Indicateur)
class IndicateurAdmin(admin.ModelAdmin):
    list_display = ['code', 'libelle_court', 'type_indicateur', 'niveau', 'valeur_reference', 'cible_finale', 'unite_mesure', 'actif']
    list_filter = ['type_indicateur', 'niveau', 'actif', 'sous_composante__composante']
    search_fields = ['code', 'libelle', 'unite_mesure']
    list_editable = ['actif', 'cible_finale']  # ✅ Permet de modifier la cible directement dans la liste
    
    fieldsets = (
        ('Identification', {
            'fields': ('code', 'libelle', 'sous_composante')
        }),
        ('Caractéristiques', {
            'fields': ('type_indicateur', 'niveau', 'unite_mesure')
        }),
        ('Valeurs', {
            'fields': ('valeur_reference', 'cible_finale')
        }),
        ('Suivi', {
            'fields': ('source_verification', 'frequence_collecte', 'responsable', 'actif')
        }),
    )
    
    def libelle_court(self, obj):
        return obj.libelle[:60] + '...' if len(obj.libelle) > 60 else obj.libelle
    libelle_court.short_description = 'Libellé'

@admin.register(Periode)
class PeriodeAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'date_debut', 'date_fin', 'cloture']
    list_filter = ['annee', 'trimestre', 'cloture']
    list_editable = ['cloture']
    ordering = ['-annee', '-trimestre']

@admin.register(Realisation)
class RealisationAdmin(admin.ModelAdmin):
    list_display = ['indicateur', 'periode', 'region', 'valeur_realisee', 'valide', 'date_saisie']
    list_filter = ['periode', 'region', 'valide', 'indicateur__sous_composante__composante']
    search_fields = ['indicateur__code', 'indicateur__libelle', 'commentaire']
    readonly_fields = ['date_saisie', 'date_modification']
    
    fieldsets = (
        ('Identification', {
            'fields': ('indicateur', 'periode', 'region')
        }),
        ('Données', {
            'fields': ('valeur_realisee', 'commentaire', 'fichier_justificatif')
        }),
        ('Validation', {
            'fields': ('valide', 'valide_par')
        }),
        ('Traçabilité', {
            'fields': ('saisi_par', 'date_saisie', 'date_modification'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.saisi_par = request.user
        super().save_model(request, obj, form, change)

@admin.register(Activite)
class ActiviteAdmin(admin.ModelAdmin):
    list_display = ['titre', 'sous_composante', 'region', 'statut', 'date_debut_prevue', 'date_fin_prevue', 'taux_execution']
    list_filter = ['statut', 'region', 'sous_composante__composante']
    search_fields = ['titre', 'description']
    date_hierarchy = 'date_debut_prevue'
    
    fieldsets = (
        ('Identification', {
            'fields': ('titre', 'description', 'sous_composante', 'region')
        }),
        ('Planification', {
            'fields': ('date_debut_prevue', 'date_fin_prevue', 'budget_prevu')
        }),
        ('Réalisation', {
            'fields': ('date_debut_reelle', 'date_fin_reelle', 'budget_execute', 'statut')
        }),
        ('Responsabilité', {
            'fields': ('responsable',)
        }),
    )
    
    def taux_execution(self, obj):
        return f"{obj.taux_execution_financier():.1f}%"
    taux_execution.short_description = 'Taux d\'exécution'

@admin.register(Rapport)
class RapportAdmin(admin.ModelAdmin):
    list_display = ['titre', 'type_rapport', 'periode', 'region', 'auteur', 'date_creation']
    list_filter = ['type_rapport', 'region', 'periode']
    search_fields = ['titre', 'contenu']
    date_hierarchy = 'date_creation'
    readonly_fields = ['date_creation', 'date_modification']
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.auteur = request.user
        super().save_model(request, obj, form, change)


@admin.register(AlerteQualite)
class AlerteQualiteAdmin(admin.ModelAdmin):
    list_display = ['type_alerte', 'severite', 'indicateur_code', 'region', 'resolue', 'date_detection']
    list_filter = ['type_alerte', 'severite', 'resolue', 'realisation__region']
    search_fields = ['message', 'realisation__indicateur__code']
    readonly_fields = ['date_detection', 'date_resolution']
    
    fieldsets = (
        ('Alerte', {
            'fields': ('realisation', 'type_alerte', 'severite', 'message')
        }),
        ('Résolution', {
            'fields': ('resolue', 'resolue_par', 'date_resolution', 'commentaire_resolution')
        }),
        ('Traçabilité', {
            'fields': ('date_detection',),
            'classes': ('collapse',)
        }),
    )
    
    def indicateur_code(self, obj):
        return obj.realisation.indicateur.code
    indicateur_code.short_description = 'Indicateur'
    
    def region(self, obj):
        return obj.realisation.get_region_display()
    region.short_description = 'Région'
