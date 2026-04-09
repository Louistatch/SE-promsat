from django.urls import path
from . import views

app_name = 'monitoring'

urlpatterns = [
    path('saisie/', views.saisie_realisation_view, name='saisie_realisation'),
    path('realisations/', views.liste_realisations_view, name='liste_realisations'),
    path('realisation/<int:pk>/modifier/', views.modifier_realisation_view, name='modifier_realisation'),
    path('realisation/<int:pk>/valider/', views.valider_realisation_view, name='valider_realisation'),
    path('rapports/', views.liste_rapports_view, name='liste_rapports'),
    path('rapport/<int:pk>/', views.detail_rapport_view, name='detail_rapport'),
    path('generer-rapport/', views.generer_rapport_view, name='generer_rapport'),
    
    # Phase 1 - Nouvelles fonctionnalités
    path('synthese-nationale/', views.synthese_nationale_view, name='synthese_nationale'),
    path('controle-qualite/', views.controle_qualite_view, name='controle_qualite'),
    path('alerte/<int:pk>/resoudre/', views.resoudre_alerte_view, name='resoudre_alerte'),
    
    # Phase 2 - Export et Rapports
    path('export/excel/', views.export_excel_view, name='export_excel'),
    path('export/pdf/', views.export_pdf_view, name='export_pdf'),
]
