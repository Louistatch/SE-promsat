from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .api_views import (
    ComposanteViewSet, SousComposanteViewSet, IndicateurViewSet,
    PeriodeViewSet, RealisationViewSet, AlerteQualiteViewSet,
    ActiviteViewSet, RapportViewSet, StatistiquesViewSet,
    SyntheseNationaleViewSet
)

router = DefaultRouter()
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


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me_view(request):
    """Retourne les infos de l'utilisateur connecté."""
    u = request.user
    return Response({
        'id':         u.id,
        'username':   u.username,
        'email':      u.email,
        'first_name': u.first_name,
        'last_name':  u.last_name,
        'role':       u.role,
        'region':     u.region,
        'is_staff':   u.is_staff,
    })


urlpatterns = [
    path('', include(router.urls)),
    path('users/me/', me_view, name='users-me'),
]
