"""
Serializers pour l'API REST ProSMAT
"""
from rest_framework import serializers
from .models import (
    Composante, SousComposante, Indicateur, Periode,
    Realisation, Activite, Rapport, AlerteQualite
)
from accounts.models import User


class ComposanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Composante
        fields = ['id', 'code', 'nom', 'description', 'ordre']


class SousComposanteSerializer(serializers.ModelSerializer):
    composante = ComposanteSerializer(read_only=True)
    composante_id = serializers.PrimaryKeyRelatedField(
        queryset=Composante.objects.all(),
        source='composante',
        write_only=True
    )
    
    class Meta:
        model = SousComposante
        fields = ['id', 'code', 'nom', 'description', 'composante', 'composante_id', 'ordre']


class IndicateurSerializer(serializers.ModelSerializer):
    sous_composante = SousComposanteSerializer(read_only=True)
    sous_composante_id = serializers.PrimaryKeyRelatedField(
        queryset=SousComposante.objects.all(),
        source='sous_composante',
        write_only=True
    )
    
    class Meta:
        model = Indicateur
        fields = [
            'id', 'code', 'libelle', 'type_indicateur', 'niveau',
            'unite', 'valeur_reference', 'cible_finale', 'source_verification',
            'frequence_collecte', 'responsable_collecte', 'sous_composante',
            'sous_composante_id', 'actif'
        ]


class PeriodeSerializer(serializers.ModelSerializer):
    nom = serializers.SerializerMethodField()
    
    class Meta:
        model = Periode
        fields = ['id', 'nom', 'annee', 'trimestre', 'date_debut', 'date_fin', 'cloture']
    
    def get_nom(self, obj):
        return str(obj)


class RealisationSerializer(serializers.ModelSerializer):
    indicateur = IndicateurSerializer(read_only=True)
    indicateur_id = serializers.PrimaryKeyRelatedField(
        queryset=Indicateur.objects.all(),
        source='indicateur',
        write_only=True
    )
    periode = PeriodeSerializer(read_only=True)
    periode_id = serializers.PrimaryKeyRelatedField(
        queryset=Periode.objects.all(),
        source='periode',
        write_only=True
    )
    saisi_par_nom = serializers.CharField(source='saisi_par.get_full_name', read_only=True)
    valide_par_nom = serializers.CharField(source='valide_par.get_full_name', read_only=True)
    
    # Champs calculés
    cumul = serializers.SerializerMethodField()
    pourcentage_atteinte = serializers.SerializerMethodField()
    ecart = serializers.SerializerMethodField()
    pourcentage_femmes = serializers.SerializerMethodField()
    
    class Meta:
        model = Realisation
        fields = [
            'id', 'indicateur', 'indicateur_id', 'periode', 'periode_id',
            'region', 'valeur_realisee', 'hommes', 'femmes', 'commentaire',
            'fichier_justificatif', 'valide', 'date_validation', 'valide_par',
            'valide_par_nom', 'saisi_par', 'saisi_par_nom', 'date_saisie',
            'cumul', 'pourcentage_atteinte', 'ecart', 'pourcentage_femmes'
        ]
        read_only_fields = ['date_saisie', 'saisi_par']
    
    def get_cumul(self, obj):
        return float(obj.calculer_cumul())
    
    def get_pourcentage_atteinte(self, obj):
        return float(obj.calculer_pourcentage_atteinte())
    
    def get_ecart(self, obj):
        return float(obj.calculer_ecart())
    
    def get_pourcentage_femmes(self, obj):
        return float(obj.pourcentage_femmes())


class AlerteQualiteSerializer(serializers.ModelSerializer):
    realisation = RealisationSerializer(read_only=True)
    realisation_id = serializers.PrimaryKeyRelatedField(
        queryset=Realisation.objects.all(),
        source='realisation',
        write_only=True
    )
    type_alerte_display = serializers.CharField(source='get_type_alerte_display', read_only=True)
    severite_display = serializers.CharField(source='get_severite_display', read_only=True)
    
    class Meta:
        model = AlerteQualite
        fields = [
            'id', 'realisation', 'realisation_id', 'type_alerte',
            'type_alerte_display', 'severite', 'severite_display',
            'message', 'resolue', 'date_detection', 'date_resolution'
        ]
        read_only_fields = ['date_detection']


class ActiviteSerializer(serializers.ModelSerializer):
    sous_composante = SousComposanteSerializer(read_only=True)
    sous_composante_id = serializers.PrimaryKeyRelatedField(
        queryset=SousComposante.objects.all(),
        source='sous_composante',
        write_only=True
    )
    responsable_nom = serializers.CharField(source='responsable.get_full_name', read_only=True)
    
    class Meta:
        model = Activite
        fields = [
            'id', 'code', 'libelle', 'description', 'sous_composante',
            'sous_composante_id', 'region', 'date_debut_prevue',
            'date_fin_prevue', 'date_debut_reelle', 'date_fin_reelle',
            'statut', 'budget_prevu', 'budget_execute', 'responsable',
            'responsable_nom'
        ]


class RapportSerializer(serializers.ModelSerializer):
    cree_par_nom = serializers.CharField(source='cree_par.get_full_name', read_only=True)
    
    class Meta:
        model = Rapport
        fields = [
            'id', 'titre', 'type_rapport', 'periode_debut', 'periode_fin',
            'region', 'contenu', 'fichier', 'cree_par', 'cree_par_nom',
            'date_creation'
        ]
        read_only_fields = ['date_creation', 'cree_par']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'region', 'is_active', 'date_joined'
        ]
        read_only_fields = ['date_joined']
        extra_kwargs = {
            'password': {'write_only': True}
        }


class StatistiquesSerializer(serializers.Serializer):
    """
    Serializer pour les statistiques globales
    """
    total_indicateurs = serializers.IntegerField()
    total_realisations = serializers.IntegerField()
    realisations_validees = serializers.IntegerField()
    performance_globale = serializers.FloatField()
    alertes_non_resolues = serializers.IntegerField()
    alertes_critiques = serializers.IntegerField()


class SyntheseNationaleSerializer(serializers.Serializer):
    """
    Serializer pour la synthèse nationale
    """
    indicateur_id = serializers.IntegerField()
    indicateur_code = serializers.CharField()
    indicateur_libelle = serializers.CharField()
    periode_id = serializers.IntegerField()
    periode_nom = serializers.CharField()
    total_realise = serializers.FloatField()
    total_hommes = serializers.FloatField()
    total_femmes = serializers.FloatField()
    pourcentage_atteinte = serializers.FloatField()
    ecart = serializers.FloatField()
    cible = serializers.FloatField()
