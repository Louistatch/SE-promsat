from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = [
        ('CHARGE_PROJET', 'Chargé de Projet'),
        ('COORDONNATEUR', 'Coordonnateur'),
        ('EVALUATEUR', 'Évaluateur'),
        ('ADMIN', 'Administrateur'),
    ]
    
    REGION_CHOICES = [
        ('MARITIME', 'Région Maritime'),
        ('PLATEAUX', 'Région des Plateaux'),
        ('CENTRALE', 'Région Centrale'),
        ('KARA', 'Région de la Kara'),
        ('SAVANES', 'Région des Savanes'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='CHARGE_PROJET')
    region = models.CharField(max_length=20, choices=REGION_CHOICES, null=True, blank=True)
    telephone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Utilisateur'
        verbose_name_plural = 'Utilisateurs'
    
    def __str__(self):
        return f"{self.get_full_name()} - {self.get_role_display()}"
    
    def has_region_access(self):
        return self.role == 'CHARGE_PROJET'
    
    def has_full_access(self):
        return self.role in ['COORDONNATEUR', 'EVALUATEUR', 'ADMIN']
