from django.db import models
from django.conf import settings

class Composante(models.Model):
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Composante'
        verbose_name_plural = 'Composantes'
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return self.nom

class SousComposante(models.Model):
    composante = models.ForeignKey(Composante, on_delete=models.CASCADE, related_name='sous_composantes')
    nom = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    ordre = models.IntegerField(default=0)
    
    class Meta:
        verbose_name = 'Sous-composante'
        verbose_name_plural = 'Sous-composantes'
        ordering = ['ordre', 'nom']
    
    def __str__(self):
        return f"{self.composante.nom} - {self.nom}"

class Indicateur(models.Model):
    TYPE_CHOICES = [
        ('QUANTITATIF', 'Quantitatif'),
        ('QUALITATIF', 'Qualitatif'),
    ]
    
    NIVEAU_CHOICES = [
        ('IMPACT', 'Impact'),
        ('EFFET', 'Effet'),
        ('EXTRANT', 'Extrant'),
    ]
    
    sous_composante = models.ForeignKey(SousComposante, on_delete=models.CASCADE, related_name='indicateurs')
    code = models.CharField(max_length=50, unique=True)
    libelle = models.TextField()
    type_indicateur = models.CharField(max_length=20, choices=TYPE_CHOICES)
    niveau = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    unite_mesure = models.CharField(max_length=100)
    valeur_reference = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    cible_finale = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    source_verification = models.TextField(blank=True)
    frequence_collecte = models.CharField(max_length=100, blank=True)
    responsable = models.CharField(max_length=200, blank=True)
    actif = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = 'Indicateur'
        verbose_name_plural = 'Indicateurs'
        ordering = ['code']
    
    def __str__(self):
        return f"{self.code} - {self.libelle[:50]}"

class Periode(models.Model):
    TRIMESTRE_CHOICES = [
        ('T1', 'Trimestre 1'),
        ('T2', 'Trimestre 2'),
        ('T3', 'Trimestre 3'),
        ('T4', 'Trimestre 4'),
    ]
    
    annee = models.IntegerField()
    trimestre = models.CharField(max_length=2, choices=TRIMESTRE_CHOICES)
    date_debut = models.DateField()
    date_fin = models.DateField()
    cloture = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'Période'
        verbose_name_plural = 'Périodes'
        unique_together = ['annee', 'trimestre']
        ordering = ['-annee', '-trimestre']
    
    def __str__(self):
        return f"{self.get_trimestre_display()} {self.annee}"

class Realisation(models.Model):
    indicateur = models.ForeignKey(Indicateur, on_delete=models.CASCADE, related_name='realisations')
    periode = models.ForeignKey(Periode, on_delete=models.CASCADE, related_name='realisations')
    region = models.CharField(max_length=20, choices=settings.AUTH_USER_MODEL and [
        ('MARITIME', 'Région Maritime'),
        ('PLATEAUX', 'Région des Plateaux'),
        ('CENTRALE', 'Région Centrale'),
        ('KARA', 'Région de la Kara'),
        ('SAVANES', 'Région des Savanes'),
    ])
    valeur_realisee = models.DecimalField(max_digits=15, decimal_places=2)
    
    # Désagrégation par genre
    hommes = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Hommes')
    femmes = models.DecimalField(max_digits=15, decimal_places=2, default=0, verbose_name='Femmes')
    
    commentaire = models.TextField(blank=True)
    fichier_justificatif = models.FileField(upload_to='justificatifs/', blank=True, null=True)
    saisi_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='realisations_saisies')
    valide = models.BooleanField(default=False)
    valide_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='realisations_validees')
    date_saisie = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Réalisation'
        verbose_name_plural = 'Réalisations'
        unique_together = ['indicateur', 'periode', 'region']
        ordering = ['-periode__annee', '-periode__trimestre', 'region']
    
    def __str__(self):
        return f"{self.indicateur.code} - {self.periode} - {self.region}"
    
    def pourcentage_femmes(self):
        """Calcule le pourcentage de femmes"""
        if self.valeur_realisee > 0:
            return (self.femmes / self.valeur_realisee) * 100
        return 0
    
    def calculer_cumul(self):
        """Calcule le cumul des périodes précédentes"""
        periodes_precedentes = Realisation.objects.filter(
            indicateur=self.indicateur,
            region=self.region,
            periode__annee__lte=self.periode.annee,
            periode__trimestre__lt=self.periode.trimestre
        ).aggregate(total=models.Sum('valeur_realisee'))
        return periodes_precedentes['total'] or 0
    
    def calculer_pourcentage_atteinte(self):
        """Calcule le % d'atteinte de la cible"""
        if self.indicateur.cible_finale and self.indicateur.cible_finale > 0:
            cumul = self.calculer_cumul() + self.valeur_realisee
            return (cumul / self.indicateur.cible_finale) * 100
        return 0
    
    def calculer_ecart(self):
        """Calcule l'écart par rapport à la cible"""
        if self.indicateur.cible_finale:
            cumul = self.calculer_cumul() + self.valeur_realisee
            return self.indicateur.cible_finale - cumul
        return 0
    
    def verifier_coherence_genre(self):
        """Vérifie que Total = Hommes + Femmes"""
        total_genre = self.hommes + self.femmes
        if total_genre > 0:
            return abs(self.valeur_realisee - total_genre) < 0.01
        return True

class Activite(models.Model):
    sous_composante = models.ForeignKey(SousComposante, on_delete=models.CASCADE, related_name='activites')
    titre = models.CharField(max_length=300)
    description = models.TextField()
    date_debut_prevue = models.DateField()
    date_fin_prevue = models.DateField()
    date_debut_reelle = models.DateField(null=True, blank=True)
    date_fin_reelle = models.DateField(null=True, blank=True)
    budget_prevu = models.DecimalField(max_digits=15, decimal_places=2)
    budget_execute = models.DecimalField(max_digits=15, decimal_places=2, default=0)
    region = models.CharField(max_length=20, choices=[
        ('MARITIME', 'Région Maritime'),
        ('PLATEAUX', 'Région des Plateaux'),
        ('CENTRALE', 'Région Centrale'),
        ('KARA', 'Région de la Kara'),
        ('SAVANES', 'Région des Savanes'),
        ('NATIONAL', 'National'),
    ])
    statut = models.CharField(max_length=20, choices=[
        ('PLANIFIE', 'Planifié'),
        ('EN_COURS', 'En cours'),
        ('TERMINE', 'Terminé'),
        ('SUSPENDU', 'Suspendu'),
        ('ANNULE', 'Annulé'),
    ], default='PLANIFIE')
    responsable = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='activites_responsable')
    
    class Meta:
        verbose_name = 'Activité'
        verbose_name_plural = 'Activités'
        ordering = ['-date_debut_prevue']
    
    def __str__(self):
        return self.titre
    
    def taux_execution_financier(self):
        if self.budget_prevu > 0:
            return (self.budget_execute / self.budget_prevu) * 100
        return 0

class Rapport(models.Model):
    TYPE_CHOICES = [
        ('TRIMESTRIEL', 'Rapport Trimestriel'),
        ('ANNUEL', 'Rapport Annuel'),
        ('MISSION', 'Rapport de Mission'),
        ('AUTRE', 'Autre'),
    ]
    
    titre = models.CharField(max_length=300)
    type_rapport = models.CharField(max_length=20, choices=TYPE_CHOICES)
    periode = models.ForeignKey(Periode, on_delete=models.SET_NULL, null=True, blank=True)
    region = models.CharField(max_length=20, choices=[
        ('MARITIME', 'Région Maritime'),
        ('PLATEAUX', 'Région des Plateaux'),
        ('CENTRALE', 'Région Centrale'),
        ('KARA', 'Région de la Kara'),
        ('SAVANES', 'Région des Savanes'),
        ('NATIONAL', 'National'),
    ], blank=True)
    contenu = models.TextField()
    fichier = models.FileField(upload_to='rapports/')
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    date_creation = models.DateTimeField(auto_now_add=True)
    date_modification = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Rapport'
        verbose_name_plural = 'Rapports'
        ordering = ['-date_creation']
    
    def __str__(self):
        return self.titre

class AlerteQualite(models.Model):
    TYPE_CHOICES = [
        ('EXCES', '⚠️ Excès (Réalisé > Cible)'),
        ('NEGATIF', '🔴 Valeur Négative'),
        ('VIDE', '❓ Donnée Manquante'),
        ('INCOHERENT', '⚠️ Incohérence Genre'),
    ]
    
    SEVERITE_CHOICES = [
        ('CRITIQUE', 'Critique'),
        ('IMPORTANT', 'Important'),
        ('MINEUR', 'Mineur'),
    ]
    
    realisation = models.ForeignKey(Realisation, on_delete=models.CASCADE, related_name='alertes')
    type_alerte = models.CharField(max_length=20, choices=TYPE_CHOICES)
    severite = models.CharField(max_length=20, choices=SEVERITE_CHOICES, default='IMPORTANT')
    message = models.TextField()
    resolue = models.BooleanField(default=False)
    resolue_par = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='alertes_resolues')
    date_detection = models.DateTimeField(auto_now_add=True)
    date_resolution = models.DateTimeField(null=True, blank=True)
    commentaire_resolution = models.TextField(blank=True)
    
    class Meta:
        verbose_name = 'Alerte Qualité'
        verbose_name_plural = 'Alertes Qualité'
        ordering = ['-date_detection']
    
    def __str__(self):
        return f"{self.get_type_alerte_display()} - {self.realisation.indicateur.code}"
    
    def resoudre(self, user, commentaire=''):
        """Marque l'alerte comme résolue"""
        self.resolue = True
        self.resolue_par = user
        self.date_resolution = models.timezone.now()
        self.commentaire_resolution = commentaire
        self.save()
