from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, Avg, Q
from monitoring.models import Realisation, Indicateur, Activite, Periode

@login_required
def home_view(request):
    user = request.user
    
    # Filtrer selon le rôle
    if user.has_region_access():
        realisations = Realisation.objects.filter(region=user.region)
        activites = Activite.objects.filter(region=user.region)
    else:
        realisations = Realisation.objects.all()
        activites = Activite.objects.all()
    
    # Statistiques générales
    stats = {
        'total_indicateurs': Indicateur.objects.filter(actif=True).count(),
        'total_realisations': realisations.count(),
        'realisations_validees': realisations.filter(valide=True).count(),
        'activites_en_cours': activites.filter(statut='EN_COURS').count(),
        'activites_terminees': activites.filter(statut='TERMINE').count(),
    }
    
    # Dernières réalisations
    dernieres_realisations = realisations.select_related(
        'indicateur', 'periode', 'saisi_par'
    ).order_by('-date_saisie')[:10]
    
    # Activités récentes
    activites_recentes = activites.select_related(
        'sous_composante', 'responsable'
    ).order_by('-date_debut_prevue')[:10]
    
    context = {
        'stats': stats,
        'dernieres_realisations': dernieres_realisations,
        'activites_recentes': activites_recentes,
    }
    
    return render(request, 'dashboard/home.html', context)

@login_required
def statistiques_view(request):
    user = request.user
    
    # Filtrer selon le rôle
    if user.has_region_access():
        realisations = Realisation.objects.filter(region=user.region)
        activites = Activite.objects.filter(region=user.region)
    else:
        realisations = Realisation.objects.all()
        activites = Activite.objects.all()
    
    # Statistiques par région
    stats_regions = []
    regions = ['MARITIME', 'PLATEAUX', 'CENTRALE', 'KARA', 'SAVANES']
    
    if user.has_full_access():
        for region in regions:
            stats_regions.append({
                'region': region,
                'realisations': Realisation.objects.filter(region=region).count(),
                'activites': Activite.objects.filter(region=region).count(),
                'budget_execute': Activite.objects.filter(region=region).aggregate(
                    total=Sum('budget_execute')
                )['total'] or 0,
            })
    
    # Statistiques par période
    periodes = Periode.objects.all()[:4]
    stats_periodes = []
    for periode in periodes:
        stats_periodes.append({
            'periode': periode,
            'realisations': realisations.filter(periode=periode).count(),
            'validees': realisations.filter(periode=periode, valide=True).count(),
        })
    
    context = {
        'stats_regions': stats_regions,
        'stats_periodes': stats_periodes,
    }
    
    return render(request, 'dashboard/statistiques.html', context)

@login_required
def indicateurs_view(request):
    user = request.user
    indicateurs = Indicateur.objects.filter(actif=True).select_related('sous_composante__composante')
    
    # Filtrer par région si nécessaire
    if user.has_region_access():
        # Ajouter les réalisations de la région de l'utilisateur
        for indicateur in indicateurs:
            indicateur.realisations_region = indicateur.realisations.filter(region=user.region)
    
    context = {
        'indicateurs': indicateurs,
    }
    
    return render(request, 'dashboard/indicateurs.html', context)

@login_required
def activites_view(request):
    user = request.user
    
    if user.has_region_access():
        activites = Activite.objects.filter(region=user.region)
    else:
        activites = Activite.objects.all()
    
    activites = activites.select_related('sous_composante__composante', 'responsable')
    
    # Filtres
    statut = request.GET.get('statut')
    if statut:
        activites = activites.filter(statut=statut)
    
    context = {
        'activites': activites,
    }
    
    return render(request, 'dashboard/activites.html', context)

@login_required
def dashboard_executif_view(request):
    """
    Dashboard exécutif avec KPI et graphiques avancés
    """
    from monitoring.models import Composante
    from django.db.models import F
    import json
    
    user = request.user
    
    # Vérifier les permissions (Coordonnateur, Évaluateur, Admin)
    if not user.has_full_access():
        return render(request, 'dashboard/acces_refuse.html')
    
    # === KPI PRINCIPAUX ===
    
    # 1. Bénéficiaires directs (tous indicateurs avec "bénéficiaires")
    beneficiaires_indicateurs = Indicateur.objects.filter(
        Q(libelle__icontains='bénéficiaires') | Q(libelle__icontains='beneficiaires'),
        actif=True
    )
    
    total_beneficiaires = 0
    cible_beneficiaires = 0
    beneficiaires_femmes = 0
    
    for ind in beneficiaires_indicateurs:
        realisations = Realisation.objects.filter(indicateur=ind, valide=True)
        total_beneficiaires += realisations.aggregate(Sum('valeur_realisee'))['valeur_realisee__sum'] or 0
        beneficiaires_femmes += realisations.aggregate(Sum('femmes'))['femmes__sum'] or 0
        cible_beneficiaires += ind.cible_finale or 0
    
    pct_beneficiaires = (total_beneficiaires / cible_beneficiaires * 100) if cible_beneficiaires > 0 else 0
    pct_femmes = (beneficiaires_femmes / total_beneficiaires * 100) if total_beneficiaires > 0 else 0
    
    # 2. Emplois créés (ETP)
    emplois_indicateurs = Indicateur.objects.filter(
        Q(libelle__icontains='emploi') | Q(libelle__icontains='ETP'),
        actif=True
    )
    
    total_emplois = 0
    cible_emplois = 0
    
    for ind in emplois_indicateurs:
        realisations = Realisation.objects.filter(indicateur=ind, valide=True)
        total_emplois += realisations.aggregate(Sum('valeur_realisee'))['valeur_realisee__sum'] or 0
        cible_emplois += ind.cible_finale or 0
    
    pct_emplois = (total_emplois / cible_emplois * 100) if cible_emplois > 0 else 0
    
    # 3. Performance globale (moyenne de tous les indicateurs)
    tous_indicateurs = Indicateur.objects.filter(actif=True)
    total_pct = 0
    count_ind = 0
    
    for ind in tous_indicateurs:
        if ind.cible_finale and ind.cible_finale > 0:
            realisations = Realisation.objects.filter(indicateur=ind, valide=True)
            total_realise = realisations.aggregate(Sum('valeur_realisee'))['valeur_realisee__sum'] or 0
            pct = (total_realise / ind.cible_finale * 100)
            total_pct += pct
            count_ind += 1
    
    performance_globale = (total_pct / count_ind) if count_ind > 0 else 0
    
    kpis = {
        'beneficiaires': {
            'valeur': int(total_beneficiaires),
            'cible': int(cible_beneficiaires),
            'pourcentage': round(pct_beneficiaires, 1),
            'femmes': int(beneficiaires_femmes),
            'pct_femmes': round(pct_femmes, 1),
        },
        'emplois': {
            'valeur': int(total_emplois),
            'cible': int(cible_emplois),
            'pourcentage': round(pct_emplois, 1),
        },
        'performance': {
            'pourcentage': round(performance_globale, 1),
        }
    }
    
    # === PERFORMANCE PAR RÉGION ===
    regions = ['MARITIME', 'PLATEAUX', 'CENTRALE', 'KARA', 'SAVANES']
    performance_regions = []
    
    for region in regions:
        realisations_region = Realisation.objects.filter(region=region, valide=True)
        total_pct_region = 0
        count_ind_region = 0
        
        for ind in tous_indicateurs:
            if ind.cible_finale and ind.cible_finale > 0:
                total_realise = realisations_region.filter(indicateur=ind).aggregate(
                    Sum('valeur_realisee')
                )['valeur_realisee__sum'] or 0
                pct = (total_realise / ind.cible_finale * 100)
                total_pct_region += pct
                count_ind_region += 1
        
        pct_region = (total_pct_region / count_ind_region) if count_ind_region > 0 else 0
        
        performance_regions.append({
            'region': region,
            'pourcentage': round(pct_region, 1),
            'nb_realisations': realisations_region.count(),
        })
    
    # === ATTEINTE PAR TYPE D'INDICATEUR ===
    composantes = Composante.objects.all()
    performance_composantes = []
    
    for comp in composantes:
        indicateurs_comp = Indicateur.objects.filter(
            sous_composante__composante=comp,
            actif=True
        )
        
        total_pct_comp = 0
        count_ind_comp = 0
        
        for ind in indicateurs_comp:
            if ind.cible_finale and ind.cible_finale > 0:
                realisations = Realisation.objects.filter(indicateur=ind, valide=True)
                total_realise = realisations.aggregate(Sum('valeur_realisee'))['valeur_realisee__sum'] or 0
                pct = (total_realise / ind.cible_finale * 100)
                total_pct_comp += pct
                count_ind_comp += 1
        
        pct_comp = (total_pct_comp / count_ind_comp) if count_ind_comp > 0 else 0
        
        performance_composantes.append({
            'composante': comp.nom,
            'code': comp.nom[:10],  # Utiliser les 10 premiers caractères du nom
            'pourcentage': round(pct_comp, 1),
            'nb_indicateurs': indicateurs_comp.count(),
        })
    
    # === ÉVOLUTION TEMPORELLE ===
    periodes = Periode.objects.all().order_by('-annee', '-trimestre')[:4]
    evolution_temporelle = []
    
    for periode in periodes:
        realisations_periode = Realisation.objects.filter(periode=periode, valide=True)
        total_realise = realisations_periode.aggregate(Sum('valeur_realisee'))['valeur_realisee__sum'] or 0
        
        evolution_temporelle.append({
            'periode': str(periode),  # Utiliser __str__ du modèle
            'total': float(total_realise),
        })
    
    # === ALERTES RÉCENTES ===
    from monitoring.models import AlerteQualite
    from decimal import Decimal
    
    alertes_recentes = AlerteQualite.objects.filter(
        resolue=False
    ).select_related('realisation__indicateur', 'realisation__periode').order_by('-date_detection')[:10]
    
    # Fonction helper pour convertir Decimal en float
    def convert_decimal(obj):
        if isinstance(obj, Decimal):
            return float(obj)
        return obj
    
    # Convertir en JSON pour Chart.js
    chart_data = {
        'regions': {
            'labels': [r['region'] for r in performance_regions],
            'data': [float(r['pourcentage']) for r in performance_regions],
        },
        'composantes': {
            'labels': [c['code'] for c in performance_composantes],
            'data': [float(c['pourcentage']) for c in performance_composantes],
        },
        'evolution': {
            'labels': [e['periode'] for e in evolution_temporelle],
            'data': [float(e['total']) for e in evolution_temporelle],
        }
    }
    
    context = {
        'kpis': kpis,
        'performance_regions': performance_regions,
        'performance_composantes': performance_composantes,
        'evolution_temporelle': evolution_temporelle,
        'alertes_recentes': alertes_recentes,
        'chart_data_json': json.dumps(chart_data),
    }
    
    return render(request, 'dashboard/dashboard_executif.html', context)
