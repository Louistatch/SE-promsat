"""
Système de notifications email pour ProSMAT
"""
from django.core.mail import send_mail, send_mass_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import AlerteQualite, Realisation, User
from datetime import datetime, timedelta


def envoyer_notification_alerte(alerte):
    """
    Envoie une notification email pour une alerte critique
    """
    if alerte.severite != 'CRITIQUE':
        return False
    
    # Destinataires: Coordonnateur et Évaluateur
    destinataires = User.objects.filter(
        role__in=['COORDONNATEUR', 'EVALUATEUR']
    ).values_list('email', flat=True)
    
    if not destinataires:
        return False
    
    sujet = f"[ProSMAT] Alerte Critique - {alerte.realisation.region}"
    
    message = f"""
    Alerte Critique Détectée
    
    Région: {alerte.realisation.region}
    Indicateur: {alerte.realisation.indicateur.libelle}
    Période: {alerte.realisation.periode.nom}
    Type: {alerte.get_type_alerte_display()}
    
    Message: {alerte.message}
    
    Date de détection: {alerte.date_detection.strftime('%d/%m/%Y %H:%M')}
    
    Veuillez consulter le système pour plus de détails:
    http://localhost:8000/monitoring/controle-qualite/
    
    ---
    ProSMAT - Système de Suivi & Évaluation
    """
    
    try:
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            list(destinataires),
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False


def envoyer_rappel_saisie():
    """
    Envoie un rappel aux chargés de projet qui n'ont pas saisi de données
    """
    # Période actuelle (dernier trimestre)
    from .models import Periode
    periode_actuelle = Periode.objects.filter(
        annee=datetime.now().year
    ).order_by('-ordre').first()
    
    if not periode_actuelle:
        return False
    
    # Chargés de projet
    charges_projet = User.objects.filter(role='CHARGE_PROJET')
    
    messages = []
    
    for charge in charges_projet:
        # Vérifier s'il a saisi des données pour la période actuelle
        nb_realisations = Realisation.objects.filter(
            region=charge.region,
            periode=periode_actuelle,
            saisi_par=charge
        ).count()
        
        if nb_realisations == 0:
            sujet = f"[ProSMAT] Rappel de Saisie - {periode_actuelle.nom}"
            message = f"""
            Bonjour {charge.get_full_name()},
            
            Nous vous rappelons qu'aucune donnée n'a été saisie pour votre région ({charge.region}) 
            pour la période {periode_actuelle.nom}.
            
            Veuillez vous connecter au système pour saisir vos réalisations:
            http://localhost:8000/monitoring/saisie/
            
            Date limite: {(datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')}
            
            Merci de votre collaboration.
            
            ---
            ProSMAT - Système de Suivi & Évaluation
            """
            
            if charge.email:
                messages.append((
                    sujet,
                    message,
                    settings.DEFAULT_FROM_EMAIL,
                    [charge.email]
                ))
    
    if messages:
        try:
            send_mass_mail(messages, fail_silently=False)
            return True
        except Exception as e:
            print(f"Erreur envoi emails: {e}")
            return False
    
    return False


def envoyer_rapport_hebdomadaire():
    """
    Envoie un rapport hebdomadaire au coordonnateur
    """
    coordonnateurs = User.objects.filter(role='COORDONNATEUR')
    
    if not coordonnateurs:
        return False
    
    # Statistiques de la semaine
    date_debut = datetime.now() - timedelta(days=7)
    
    nouvelles_realisations = Realisation.objects.filter(
        date_saisie__gte=date_debut
    ).count()
    
    nouvelles_alertes = AlerteQualite.objects.filter(
        date_detection__gte=date_debut,
        resolue=False
    ).count()
    
    alertes_critiques = AlerteQualite.objects.filter(
        date_detection__gte=date_debut,
        severite='CRITIQUE',
        resolue=False
    ).count()
    
    sujet = f"[ProSMAT] Rapport Hebdomadaire - {datetime.now().strftime('%d/%m/%Y')}"
    
    message = f"""
    Rapport Hebdomadaire ProSMAT
    Semaine du {date_debut.strftime('%d/%m/%Y')} au {datetime.now().strftime('%d/%m/%Y')}
    
    📊 STATISTIQUES
    
    • Nouvelles réalisations saisies: {nouvelles_realisations}
    • Nouvelles alertes détectées: {nouvelles_alertes}
    • Alertes critiques non résolues: {alertes_critiques}
    
    🎯 ACTIONS RECOMMANDÉES
    
    {'⚠️ Attention: ' + str(alertes_critiques) + ' alertes critiques nécessitent votre attention!' if alertes_critiques > 0 else '✅ Aucune alerte critique cette semaine.'}
    
    📈 ACCÈS RAPIDE
    
    • Dashboard Exécutif: http://localhost:8000/executif/
    • Contrôle Qualité: http://localhost:8000/monitoring/controle-qualite/
    • Synthèse Nationale: http://localhost:8000/monitoring/synthese-nationale/
    
    ---
    ProSMAT - Système de Suivi & Évaluation
    """
    
    destinataires = [c.email for c in coordonnateurs if c.email]
    
    if destinataires:
        try:
            send_mail(
                sujet,
                message,
                settings.DEFAULT_FROM_EMAIL,
                destinataires,
                fail_silently=False,
            )
            return True
        except Exception as e:
            print(f"Erreur envoi email: {e}")
            return False
    
    return False


def envoyer_notification_validation(realisation):
    """
    Envoie une notification quand une réalisation est validée
    """
    if not realisation.saisi_par or not realisation.saisi_par.email:
        return False
    
    sujet = f"[ProSMAT] Réalisation Validée - {realisation.indicateur.code}"
    
    message = f"""
    Bonjour {realisation.saisi_par.get_full_name()},
    
    Votre réalisation a été validée:
    
    Indicateur: {realisation.indicateur.libelle}
    Période: {realisation.periode.nom}
    Région: {realisation.region}
    Valeur: {realisation.valeur_realisee} {realisation.indicateur.unite}
    
    Validée par: {realisation.valide_par.get_full_name() if realisation.valide_par else 'Système'}
    Date de validation: {realisation.date_validation.strftime('%d/%m/%Y %H:%M') if realisation.date_validation else 'N/A'}
    
    Merci pour votre contribution!
    
    ---
    ProSMAT - Système de Suivi & Évaluation
    """
    
    try:
        send_mail(
            sujet,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [realisation.saisi_par.email],
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Erreur envoi email: {e}")
        return False
