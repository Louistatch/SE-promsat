from django.core.management.base import BaseCommand
from monitoring.models import Composante, SousComposante, Indicateur, Periode
from accounts.models import User
from datetime import date


class Command(BaseCommand):
    help = 'Charge les données initiales dans la base de données'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=' * 60))
        self.stdout.write(self.style.SUCCESS('CHARGEMENT DES DONNÉES INITIALES'))
        self.stdout.write(self.style.SUCCESS('=' * 60))
        
        # Vérifier si des données existent déjà
        if Composante.objects.exists():
            self.stdout.write(self.style.WARNING('⚠️  Des données existent déjà. Chargement ignoré.'))
            self.stdout.write(self.style.WARNING('   Pour forcer le rechargement, utilisez: python manage.py flush'))
            return
        
        # 1. Créer les composantes
        self.stdout.write('\n1. Création des composantes...')
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
            status = '✓ Créé' if created else '✓ Existe'
            self.stdout.write(f'   {status}: {comp.nom}')
        
        # 2. Créer les sous-composantes
        self.stdout.write('\n2. Création des sous-composantes...')
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
            status = '✓ Créé' if created else '✓ Existe'
            self.stdout.write(f'   {status}: {sc.nom}')
        
        # 3. Créer des indicateurs exemples
        self.stdout.write('\n3. Création des indicateurs...')
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
            status = '✓ Créé' if created else '✓ Existe'
            self.stdout.write(f'   {status}: {ind.code} - {ind.libelle[:50]}')
        
        # 4. Créer les périodes
        self.stdout.write('\n4. Création des périodes...')
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
            status = '✓ Créé' if created else '✓ Existe'
            self.stdout.write(f'   {status}: {per}')
        
        # 5. Créer les utilisateurs admin
        self.stdout.write('\n5. Création des utilisateurs admin...')
        
        # Admin principal
        admin_email = "admin@prosmat.tg"
        if User.objects.filter(email=admin_email).exists():
            self.stdout.write(f'   ✓ Existe: {admin_email}')
        else:
            admin = User.objects.create_superuser(
                username="admin",
                email=admin_email,
                password="ProSMAT2026!",
                first_name="Administrateur",
                last_name="ProSMAT",
                role="ADMIN",
            )
            self.stdout.write(self.style.SUCCESS(f'   ✓ Créé: {admin_email}'))
            self.stdout.write(self.style.WARNING(f'   📧 Email: {admin_email}'))
            self.stdout.write(self.style.WARNING(f'   🔑 Mot de passe: ProSMAT2026!'))
        
        # Admin tatchida (pour Firebase)
        tatchida_email = "tatchida@gmail.com"
        if User.objects.filter(email=tatchida_email).exists():
            # Mettre à jour pour s'assurer qu'il est admin
            user = User.objects.get(email=tatchida_email)
            if user.role != 'ADMIN':
                user.role = 'ADMIN'
                user.is_staff = True
                user.is_superuser = True
                user.save()
                self.stdout.write(self.style.SUCCESS(f'   ✓ Mis à jour: {tatchida_email} → ADMIN'))
            else:
                self.stdout.write(f'   ✓ Existe: {tatchida_email} (déjà ADMIN)')
        else:
            # Créer le compte (sera complété lors de la première connexion Firebase)
            tatchida = User.objects.create_user(
                username="tatchida",
                email=tatchida_email,
                first_name="Louis",
                last_name="Tatchida",
            )
            tatchida.role = 'ADMIN'
            tatchida.is_staff = True
            tatchida.is_superuser = True
            tatchida.save()
            self.stdout.write(self.style.SUCCESS(f'   ✓ Créé: {tatchida_email}'))
            self.stdout.write(self.style.WARNING(f'   📧 Se connectera via Firebase'))
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ DONNÉES INITIALES CHARGÉES AVEC SUCCÈS!'))
        self.stdout.write('=' * 60)
        self.stdout.write('\nRésumé:')
        self.stdout.write(f'   - Composantes: {Composante.objects.count()}')
        self.stdout.write(f'   - Sous-composantes: {SousComposante.objects.count()}')
        self.stdout.write(f'   - Indicateurs: {Indicateur.objects.count()}')
        self.stdout.write(f'   - Périodes: {Periode.objects.count()}')
        self.stdout.write(f'   - Utilisateurs: {User.objects.count()}')
        self.stdout.write('\nVous pouvez maintenant:')
        self.stdout.write('   1. Vous connecter avec: admin@prosmat.tg / ProSMAT2026!')
        self.stdout.write("   2. Créer d'autres utilisateurs")
        self.stdout.write('   3. Saisir des réalisations\n')
