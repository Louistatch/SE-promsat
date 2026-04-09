from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('statistiques/', views.statistiques_view, name='statistiques'),
    path('indicateurs/', views.indicateurs_view, name='indicateurs'),
    path('activites/', views.activites_view, name='activites'),
    path('executif/', views.dashboard_executif_view, name='executif'),
]
