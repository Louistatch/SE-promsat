#!/usr/bin/env python
"""
Script pour charger les données initiales dans la base de données Neon
À exécuter depuis le Shell de Render
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from monitoring.models import Composante, SousComposante, Indicateur, Periode
from accounts.models import User
from datetime import date

def charger_donnees():
    print("=" * 60)
    print("CHARGEMENT DES DONNÉES INITIALES")
    print("=" * 60)
    print()
    
    # 1. Créer les composantes
    print("1. Création des composantes...")
    composantes_data = [
        {"nom": "Composante 1: Amélioration de la productivité agricole", "ordre": 1},
        {"nom": "Composante 2: Développement des chaînes de valeur", "ordre": 2},
        {"nom": "Composante 3: Renforcement des capacités", "ordre": 3},
        {"nom": "Composante 4: Coordination et gestion du projet", "ordre": 4},
    ]
    
    composantes = {}
    for data in composantes_data:
        comp, created = Composante.objects.get_or_create(
            nom=data["nom"],
            defaults={"ordre": data["ordre"]}
        )
        composantes[data["ordre"]] = comp
        print(f"   {'✓ Créé' if created else '✓ Existe'}: {comp.nom}")
    
    print()
    
    # 2. Créer les sous-composantes
    print("2. Création des sous-composantes...")
    sous_composantes_data = [
        {"composante": 1, "nom": "1.1 Infrastructures agricoles", "ordre": 1},
        {"composante": 1, "nom": "1.2 Intrants et équipements", "ordre": 2},
        {"composante": 2, "nom": "2.1 Transformation et commercialisation", "ordre": 1},
        {"composante": 2, "nom": "2.2 Accès aux marchés", "ordre": 2},
        {"composante": 3, "nom": "3.1 Formation des producteurs", "ordre": 1},
        {"composante": 3, "nom": "3.2 Appui institutionnel", "ordre": 2},
    ]
    
    sous_composantes = {}
    for data in sous_composantes_data:
        sc, created = SousComposante.objects.get_or_create(
            composante=composantes[data["composante"]],
            nom=data["nom"],
            defaults={"ordre": data["ordre"]}
        )
        sous_composantes[data["nom"]] = sc
        print(f"   {'✓ Créé' if created else '✓ Existe'}: {sc.nom}")
    
    print()
    
    # 3. Créer des indicateurs exemples
    print("3. Création des indicateurs...")
    indicateurs_data = [
        {
            "code": "IND-1.1.1",
            "libelle": "Nombre de bénéficiaires directs du projet",
            "sous_composante": "1.1 Infrastructures agricoles",
            "type": "QUANTITATIF",
            "niveau": "IMPACT",
            "unite": "Personnes",
            "cible": 50000,
        },
        {
            "code": "IND-1.1.2",
            "libelle": "Nombre d'hectares aménagés",
            "sous_composante": "1.1 Infrastructures agricoles",
            "type": "QUANTITATIF",
            "niveau": "EXTRANT",
            "unite": "Hectares",
            "cible": 5000,
        },
        {
            "code": "IND-1.2.1",
            "libelle": "Nombre de producteurs ayant reçu des intrants",
            "sous_composante": "1.2 Intrants et équipements",
            "type": "QUANTITATIF",
            "niveau": "EXTRANT",
            "unite": "Producteurs",
            "cible": 10000,
        },
        {
            "code": "IND-2.1.1",
            "libelle": "Nombre d'unités de transformation créées",
            "sous_composante": "2.1 Transformation et commercialisation",
            "type": "QUANTITATIF",
            "niveau": "EXTRANT",
            "unite": "Unités",
            "cible": 50,
        },
        {
            "code": "IND-3.1.1",
            "libelle": "Nombre de producteurs formés",
            "sous_composante": "3.1 Formation des producteurs",
            "type": "QUANTITATIF",
            "niveau": "EXTRANT",
            "unite": "Producteurs",
            "cible": 15000,
        },
    ]
    
    for data in indicateurs_data:
        ind, created = Indicateur.objects.get_or_create(
            code=data["code"],
            defaults={
                "libelle": data["libelle"],
                "sous_composante": sous_composantes[data["sous_composante"]],
                "type_indicateur": data["type"],
                "niveau": data["niveau"],
                "unite_mesure": data["unite"],
                "cible_finale": data["cible"],
                "actif": True,
            }
        )
        print(f"   {'✓ Créé' if created else '✓ Existe'}: {ind.code} - {ind.libelle[:50]}")
    
    print()
    
    # 4. Créer les périodes
    print("4. Création des périodes...")
    periodes_data = [
        {"annee": 2024, "trimestre": "T1", "debut": date(2024, 1, 1), "fin": date(2024, 3, 31)},
        {"annee": 2024, "trimestre": "T2", "debut": date(2024, 4, 1), "fin": date(2024, 6, 30)},
        {"annee": 2024, "trimestre": "T3", "debut": date(2024, 7, 1), "fin": date(2024, 9, 30)},
        {"annee": 2024, "trimestre": "T4", "debut": date(2024, 10, 1), "fin": date(2024, 12, 31)},
        {"annee": 2025, "trimestre": "T1", "debut": date(2025, 1, 1), "fin": date(2025, 3, 31)},
        {"annee": 2025, "trimestre": "T2", "debut": date(2025, 4, 1), "fin": date(2025, 6, 30)},
        {"annee": 2025, "trimestre": "T3", "debut": date(2025, 7, 1), "fin": date(2025, 9, 30)},
        {"annee": 2025, "trimestre": "T4", "debut": date(2025, 10, 1), "fin": date(2025, 12, 31)},
        {"annee": 2026, "trimestre": "T1", "debut": date(2026, 1, 1), "fin": date(2026, 3, 31)},
    ]
    
    for data in periodes_data:
        per, created = Periode.objects.get_or_create(
            annee=data["annee"],
            trimestre=data["trimestre"],
            defaults={
                "date_debut": data["debut"],
                "date_fin": data["fin"],
                "cloture": False,
            }
        )
        print(f"   {'✓ Créé' if created else '✓ Existe'}: {per}")
    
    print()
    
    # 5. Créer un utilisateur admin
    print("5. Création de l'utilisateur admin...")
    admin_email = "admin@prosmat.tg"
    
    if User.objects.filter(email=admin_email).exists():
        print(f"   ✓ Existe: {admin_email}")
    else:
        admin = User.objects.create_superuser(
            username="admin",
            email=admin_email,
            password="ProSMAT2026!",
            first_name="Administrateur",
            last_name="ProSMAT",
            role="ADMIN",
        )
        print(f"   ✓ Créé: {admin_email}")
        print(f"   📧 Email: {admin_email}")
        print(f"   🔑 Mot de passe: ProSMAT2026!")
    
    print()
    print("=" * 60)
    print("✅ DONNÉES INITIALES CHARGÉES AVEC SUCCÈS!")
    print("=" * 60)
    print()
    print("Résumé:")
    print(f"   - Composantes: {Composante.objects.count()}")
    print(f"   - Sous-composantes: {SousComposante.objects.count()}")
    print(f"   - Indicateurs: {Indicateur.objects.count()}")
    print(f"   - Périodes: {Periode.objects.count()}")
    print(f"   - Utilisateurs: {User.objects.count()}")
    print()
    print("Vous pouvez maintenant:")
    print("   1. Vous connecter avec: admin@prosmat.tg / ProSMAT2026!")
    print("   2. Créer d'autres utilisateurs")
    print("   3. Saisir des réalisations")
    print()

if __name__ == '__main__':
    try:
        charger_donnees()
    except Exception as e:
        print(f"\n❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
