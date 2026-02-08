"""
URLs pour l'API REST ProSMAT
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    ComposanteViewSet, SousComposanteViewSet, IndicateurViewSet,
    PeriodeViewSet, RealisationViewSet, AlerteQualiteViewSet,
    ActiviteViewSet, RapportViewSet, StatistiquesViewSet,
    SyntheseNationaleViewSet
)

# Créer le router
router = DefaultRouter()

# Enregistrer les viewsets
router.register(r'composantes', ComposanteViewSet, basename='composante')
router.register(r'sous-composantes', SousComposanteViewSet, basename='sous-composante')
router.register(r'indicateurs', IndicateurViewSet, basename='indicateur')
router.register(r'periodes', PeriodeViewSet, basename='periode')
router.register(r'realisations', RealisationViewSet, basename='realisation')
router.register(r'alertes', AlerteQualiteViewSet, basename='alerte')
router.register(r'activites', ActiviteViewSet, basename='activite')
router.register(r'rapports', RapportViewSet, basename='rapport')
router.register(r'statistiques', StatistiquesViewSet, basename='statistiques')
router.register(r'synthese-nationale', SyntheseNationaleViewSet, basename='synthese-nationale')

# URLs
urlpatterns = [
    path('', include(router.urls)),
]
