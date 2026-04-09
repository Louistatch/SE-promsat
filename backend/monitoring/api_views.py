"""
API Views pour ProSMAT
"""
from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Sum, Count, Avg, Q
from .models import (
    Composante, SousComposante, Indicateur, Periode,
    Realisation, Activite, Rapport, AlerteQualite
)
from accounts.models import User
from .serializers import (
    ComposanteSerializer, SousComposanteSerializer, IndicateurSerializer,
    PeriodeSerializer, RealisationSerializer, ActiviteSerializer,
    RapportSerializer, AlerteQualiteSerializer, UserSerializer,
    StatistiquesSerializer, SyntheseNationaleSerializer
)
from .utils import calculer_synthese_nationale


class ComposanteViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les composantes
    """
    queryset = Composante.objects.all().order_by('ordre')
    serializer_class = ComposanteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['code', 'nom']
    ordering_fields = ['ordre', 'code']


class SousComposanteViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les sous-composantes
    """
    queryset = SousComposante.objects.all().select_related('composante').order_by('ordre')
    serializer_class = SousComposanteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['composante']
    search_fields = ['code', 'nom']


class IndicateurViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les indicateurs
    """
    queryset = Indicateur.objects.all().select_related(
        'sous_composante__composante'
    ).filter(actif=True)
    serializer_class = IndicateurSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sous_composante', 'type_indicateur', 'niveau']
    search_fields = ['code', 'libelle']
    
    @action(detail=True, methods=['get'])
    def realisations(self, request, pk=None):
        """
        Récupère toutes les réalisations d'un indicateur
        """
        indicateur = self.get_object()
        realisations = Realisation.objects.filter(
            indicateur=indicateur
        ).select_related('periode', 'saisi_par', 'valide_par')
        
        # Filtrer par région si l'utilisateur est un chargé de projet
        if request.user.has_region_access():
            realisations = realisations.filter(region=request.user.region)
        
        serializer = RealisationSerializer(realisations, many=True)
        return Response(serializer.data)


class PeriodeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint pour les périodes (lecture seule)
    """
    queryset = Periode.objects.all().order_by('-annee', '-trimestre')
    serializer_class = PeriodeSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['annee', 'trimestre']


class RealisationViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les réalisations
    """
    queryset = Realisation.objects.all().select_related(
        'indicateur__sous_composante__composante',
        'periode', 'saisi_par', 'valide_par'
    )
    serializer_class = RealisationSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['indicateur', 'periode', 'region', 'valide']
    ordering_fields = ['date_saisie', 'valeur_realisee']
    
    def get_queryset(self):
        """
        Filtrer les réalisations selon le rôle de l'utilisateur
        """
        queryset = super().get_queryset()
        
        if self.request.user.has_region_access():
            queryset = queryset.filter(region=self.request.user.region)
        
        return queryset
    
    def perform_create(self, serializer):
        """
        Définir l'utilisateur qui a saisi la réalisation
        """
        region = self.request.user.region if self.request.user.has_region_access() else self.request.data.get('region')
        serializer.save(saisi_par=self.request.user, region=region)
    
    @action(detail=True, methods=['post'])
    def valider(self, request, pk=None):
        """
        Valider une réalisation
        """
        realisation = self.get_object()
        
        if not request.user.has_full_access():
            return Response(
                {'error': 'Vous n\'avez pas la permission de valider des réalisations'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        realisation.valider(request.user)
        
        serializer = self.get_serializer(realisation)
        return Response(serializer.data)


class AlerteQualiteViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les alertes qualité
    """
    queryset = AlerteQualite.objects.all().select_related(
        'realisation__indicateur',
        'realisation__periode'
    )
    serializer_class = AlerteQualiteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type_alerte', 'severite', 'resolue']
    ordering_fields = ['date_detection', 'severite']
    
    def get_queryset(self):
        """
        Filtrer les alertes selon le rôle de l'utilisateur
        """
        queryset = super().get_queryset()
        
        if self.request.user.has_region_access():
            queryset = queryset.filter(realisation__region=self.request.user.region)
        
        return queryset
    
    @action(detail=True, methods=['post'])
    def resoudre(self, request, pk=None):
        """
        Résoudre une alerte
        """
        alerte = self.get_object()
        alerte.resoudre()
        
        serializer = self.get_serializer(alerte)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistiques(self, request):
        """
        Statistiques des alertes
        """
        queryset = self.get_queryset()
        
        stats = {
            'total': queryset.count(),
            'non_resolues': queryset.filter(resolue=False).count(),
            'par_type': {},
            'par_severite': {},
            'par_region': {}
        }
        
        # Par type
        for type_alerte, _ in AlerteQualite.TYPE_CHOICES:
            stats['par_type'][type_alerte] = queryset.filter(
                type_alerte=type_alerte,
                resolue=False
            ).count()
        
        # Par sévérité
        for severite, _ in AlerteQualite.SEVERITE_CHOICES:
            stats['par_severite'][severite] = queryset.filter(
                severite=severite,
                resolue=False
            ).count()
        
        # Par région
        regions = ['MARITIME', 'PLATEAUX', 'CENTRALE', 'KARA', 'SAVANES']
        for region in regions:
            stats['par_region'][region] = queryset.filter(
                realisation__region=region,
                resolue=False
            ).count()
        
        return Response(stats)


class ActiviteViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les activités
    """
    queryset = Activite.objects.all().select_related(
        'sous_composante__composante', 'responsable'
    )
    serializer_class = ActiviteSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['sous_composante', 'region', 'statut']
    search_fields = ['code', 'libelle']
    
    def get_queryset(self):
        """
        Filtrer les activités selon le rôle de l'utilisateur
        """
        queryset = super().get_queryset()
        
        if self.request.user.has_region_access():
            queryset = queryset.filter(region=self.request.user.region)
        
        return queryset


class RapportViewSet(viewsets.ModelViewSet):
    """
    API endpoint pour les rapports
    """
    queryset = Rapport.objects.all().select_related('cree_par')
    serializer_class = RapportSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['type_rapport', 'region']
    ordering_fields = ['date_creation']
    
    def perform_create(self, serializer):
        """
        Définir l'utilisateur qui a créé le rapport
        """
        serializer.save(cree_par=self.request.user)


class StatistiquesViewSet(viewsets.ViewSet):
    """
    API endpoint pour les statistiques globales
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        Récupère les statistiques globales
        """
        # Indicateurs
        total_indicateurs = Indicateur.objects.filter(actif=True).count()
        
        # Réalisations
        realisations = Realisation.objects.all()
        if request.user.has_region_access():
            realisations = realisations.filter(region=request.user.region)
        
        total_realisations = realisations.count()
        realisations_validees = realisations.filter(valide=True).count()
        
        # Performance globale
        indicateurs = Indicateur.objects.filter(actif=True)
        total_pct = 0
        count_ind = 0
        
        for ind in indicateurs:
            if ind.cible_finale and ind.cible_finale > 0:
                total_realise = realisations.filter(
                    indicateur=ind,
                    valide=True
                ).aggregate(Sum('valeur_realisee'))['valeur_realisee__sum'] or 0
                pct = (total_realise / ind.cible_finale * 100)
                total_pct += pct
                count_ind += 1
        
        performance_globale = (total_pct / count_ind) if count_ind > 0 else 0
        
        # Alertes
        alertes = AlerteQualite.objects.all()
        if request.user.has_region_access():
            alertes = alertes.filter(realisation__region=request.user.region)
        
        alertes_non_resolues = alertes.filter(resolue=False).count()
        alertes_critiques = alertes.filter(
            resolue=False,
            severite='CRITIQUE'
        ).count()
        
        data = {
            'total_indicateurs': total_indicateurs,
            'total_realisations': total_realisations,
            'realisations_validees': realisations_validees,
            'performance_globale': round(performance_globale, 2),
            'alertes_non_resolues': alertes_non_resolues,
            'alertes_critiques': alertes_critiques
        }
        
        serializer = StatistiquesSerializer(data)
        return Response(serializer.data)


class SyntheseNationaleViewSet(viewsets.ViewSet):
    """
    API endpoint pour la synthèse nationale
    """
    permission_classes = [IsAuthenticated]
    
    def list(self, request):
        """
        Récupère la synthèse nationale pour tous les indicateurs et périodes
        """
        if not request.user.has_full_access():
            return Response(
                {'error': 'Accès refusé'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        indicateurs = Indicateur.objects.filter(actif=True)
        periodes = Periode.objects.all().order_by('-annee', '-trimestre')[:4]
        
        syntheses = []
        
        for indicateur in indicateurs:
            for periode in periodes:
                synthese = calculer_synthese_nationale(indicateur, periode)
                
                syntheses.append({
                    'indicateur_id': indicateur.id,
                    'indicateur_code': indicateur.code,
                    'indicateur_libelle': indicateur.libelle,
                    'periode_id': periode.id,
                    'periode_nom': periode.nom,
                    'total_realise': synthese['total_realise'],
                    'total_hommes': synthese['total_hommes'],
                    'total_femmes': synthese['total_femmes'],
                    'pourcentage_atteinte': synthese['pourcentage_atteinte'],
                    'ecart': synthese['ecart'],
                    'cible': synthese['cible']
                })
        
        serializer = SyntheseNationaleSerializer(syntheses, many=True)
        return Response(serializer.data)
