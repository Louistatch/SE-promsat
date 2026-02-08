"""
Fonctions utilitaires pour le contrôle qualité
"""
from .models import AlerteQualite

def verifier_qualite_realisation(realisation):
    """
    Vérifie la qualité d'une réalisation et crée des alertes si nécessaire
    """
    # Supprimer les anciennes alertes non résolues
    AlerteQualite.objects.filter(realisation=realisation, resolue=False).delete()
    
    # 1. Vérifier les valeurs négatives
    if realisation.valeur_realisee < 0:
        AlerteQualite.objects.create(
            realisation=realisation,
            type_alerte='NEGATIF',
            severite='CRITIQUE',
            message=f'Valeur négative détectée: {realisation.valeur_realisee}'
        )
    
    # 2. Vérifier l'excès (Réalisé > Cible)
    if realisation.indicateur.cible_finale:
        cumul = realisation.calculer_cumul() + realisation.valeur_realisee
        if cumul > realisation.indicateur.cible_finale:
            ecart = cumul - realisation.indicateur.cible_finale
            AlerteQualite.objects.create(
                realisation=realisation,
                type_alerte='EXCES',
                severite='IMPORTANT',
                message=f'Réalisé ({cumul}) dépasse la cible ({realisation.indicateur.cible_finale}) de {ecart}'
            )
    
    # 3. Vérifier les données manquantes
    if realisation.valeur_realisee == 0 and realisation.indicateur.cible_finale > 0:
        AlerteQualite.objects.create(
            realisation=realisation,
            type_alerte='VIDE',
            severite='MINEUR',
            message='Aucune valeur saisie pour cette période'
        )
    
    # 4. Vérifier la cohérence genre (Total = Hommes + Femmes)
    if realisation.hommes > 0 or realisation.femmes > 0:
        if not realisation.verifier_coherence_genre():
            total_genre = realisation.hommes + realisation.femmes
            AlerteQualite.objects.create(
                realisation=realisation,
                type_alerte='INCOHERENT',
                severite='IMPORTANT',
                message=f'Incohérence: Total ({realisation.valeur_realisee}) ≠ Hommes ({realisation.hommes}) + Femmes ({realisation.femmes}) = {total_genre}'
            )

def calculer_synthese_nationale(indicateur, periode):
    """
    Calcule la synthèse nationale pour un indicateur et une période
    """
    from .models import Realisation
    from django.db.models import Sum
    
    # Agréger les 5 régions
    synthese = Realisation.objects.filter(
        indicateur=indicateur,
        periode=periode
    ).aggregate(
        total_realise=Sum('valeur_realisee'),
        total_hommes=Sum('hommes'),
        total_femmes=Sum('femmes')
    )
    
    # Récupérer les valeurs (gérer les None)
    total_realise = synthese['total_realise'] or 0
    total_hommes = synthese['total_hommes'] or 0
    total_femmes = synthese['total_femmes'] or 0
    cible = indicateur.cible_finale or 0
    
    # Calculer le % d'atteinte
    pourcentage = 0
    if cible > 0 and total_realise > 0:
        pourcentage = (total_realise / cible) * 100
    
    # Calculer l'écart
    ecart = 0
    if cible > 0:
        ecart = cible - total_realise
    
    return {
        'total_realise': total_realise,
        'total_hommes': total_hommes,
        'total_femmes': total_femmes,
        'pourcentage_atteinte': pourcentage,
        'ecart': ecart,
        'cible': cible
    }

def generer_rapport_qualite(periode=None, region=None):
    """
    Génère un rapport de contrôle qualité
    """
    from .models import AlerteQualite, Realisation
    
    # Filtrer les alertes
    alertes = AlerteQualite.objects.filter(resolue=False)
    
    if periode:
        alertes = alertes.filter(realisation__periode=periode)
    
    if region:
        alertes = alertes.filter(realisation__region=region)
    
    # Compter par type
    rapport = {
        'total_alertes': alertes.count(),
        'par_type': {},
        'par_severite': {},
        'par_region': {}
    }
    
    # Par type
    for type_alerte, _ in AlerteQualite.TYPE_CHOICES:
        count = alertes.filter(type_alerte=type_alerte).count()
        rapport['par_type'][type_alerte] = count
    
    # Par sévérité
    for severite, _ in AlerteQualite.SEVERITE_CHOICES:
        count = alertes.filter(severite=severite).count()
        rapport['par_severite'][severite] = count
    
    # Par région
    regions = ['MARITIME', 'PLATEAUX', 'CENTRALE', 'KARA', 'SAVANES']
    for reg in regions:
        count = alertes.filter(realisation__region=reg).count()
        rapport['par_region'][reg] = count
    
    return rapport
