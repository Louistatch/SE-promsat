# 🚀 GUIDE D'INSTALLATION - PHASE 2

**Date**: 8 Février 2026  
**Version**: 2.0

---

## ✅ PRÉREQUIS

Avant d'installer la Phase 2, assurez-vous que:
- ✅ Phase 1 est installée et fonctionnelle
- ✅ Le serveur Django tourne sur http://localhost:8000
- ✅ L'environnement virtuel `venv_prosmat` est activé
- ✅ Python 3.11.9 est installé

---

## 📦 INSTALLATION DES DÉPENDANCES

### Étape 1: Activer l'environnement virtuel

```bash
# Windows
.\venv_prosmat\Scripts\activate

# Linux/Mac
source venv_prosmat/bin/activate
```

### Étape 2: Installer les nouvelles bibliothèques

```bash
pip install reportlab==4.4.9 xlsxwriter==3.1.9 django-crispy-forms==2.5 crispy-bootstrap5==2025.6
```

**OU** utiliser requirements.txt:

```bash
pip install -r requirements.txt
```

### Étape 3: Vérifier l'installation

```bash
pip list | grep -E "reportlab|xlsxwriter|crispy"
```

Vous devriez voir:
```
crispy-bootstrap5      2025.6
django-crispy-forms    2.5
reportlab              4.4.9
xlsxwriter             3.2.9
```

---

## 🔧 CONFIGURATION

### Aucune configuration supplémentaire requise!

La Phase 2 utilise les mêmes paramètres que la Phase 1:
- Base de données: `db.sqlite3` (existante)
- Utilisateurs: Ceux créés en Phase 1
- Permissions: Basées sur les rôles existants

---

## 🚀 DÉMARRAGE

### Le serveur est déjà en cours d'exécution

Si le serveur Django tourne déjà, il a automatiquement détecté les changements et redémarré.

### Si le serveur n'est pas démarré

```bash
python manage.py runserver
```

---

## ✅ VÉRIFICATION

### Test 1: Dashboard Exécutif

1. Ouvrir le navigateur: http://localhost:8000
2. Se connecter avec le compte **coordonnateur**:
   - Username: `coordonnateur`
   - Password: `prosmat2026`
3. Cliquer sur "Dashboard Exécutif" dans le menu
4. Vérifier que:
   - ✅ Les 3 KPI s'affichent
   - ✅ Les 3 graphiques sont visibles
   - ✅ Le tableau de performance est rempli
   - ✅ Les alertes récentes s'affichent

### Test 2: Export Excel

1. Depuis le Dashboard Exécutif, cliquer sur "Export Excel"
2. Le fichier `ProSMAT_Export_YYYYMMDD_HHMMSS.xlsx` se télécharge
3. Ouvrir le fichier avec Excel
4. Vérifier que:
   - ✅ Feuille "Synthese-Nationale" existe
   - ✅ 5 feuilles régionales existent
   - ✅ Feuille "Controle-Qualite" existe
   - ✅ Les données sont présentes

### Test 3: Export PDF

1. Depuis le Dashboard Exécutif, cliquer sur "Export PDF"
2. Le fichier `ProSMAT_Rapport_YYYYMMDD_HHMMSS.pdf` se télécharge
3. Ouvrir le fichier avec Adobe Reader
4. Vérifier que:
   - ✅ Le rapport a 2 pages
   - ✅ Les tableaux sont bien formatés
   - ✅ Les données sont lisibles
   - ✅ Le pied de page est présent

---

## 🐛 DÉPANNAGE

### Erreur: "No module named 'reportlab'"

**Solution**:
```bash
pip install reportlab==4.4.9
```

### Erreur: "No module named 'xlsxwriter'"

**Solution**:
```bash
pip install xlsxwriter==3.1.9
```

### Erreur 403: "Accès refusé" sur le Dashboard

**Cause**: Vous êtes connecté avec un compte Chargé de Projet

**Solution**: Se connecter avec:
- `coordonnateur` / `prosmat2026`
- `evaluateur` / `prosmat2026`
- `admin` / `admin123`

### Graphiques ne s'affichent pas

**Cause**: Chart.js ne se charge pas depuis le CDN

**Solution**:
1. Vérifier la connexion internet
2. Désactiver les bloqueurs de publicité
3. Vider le cache du navigateur (Ctrl + F5)

### Export Excel vide

**Cause**: Pas de données dans la base

**Solution**:
```bash
python manage.py creer_donnees_test
```

Cela créera 25 réalisations de test.

---

## 📊 DONNÉES DE TEST

### Créer des données de test supplémentaires

Si vous avez besoin de plus de données pour tester:

```bash
python manage.py creer_donnees_test
```

Cette commande:
- Crée 25 réalisations aléatoires
- Répartit sur les 5 régions
- Utilise les 4 périodes (T1-T4 2026)
- Ajoute des désagrégations Hommes/Femmes
- Génère quelques incohérences pour tester les alertes

### Réinitialiser les données

Pour repartir de zéro:

```bash
# Supprimer la base de données
del db.sqlite3

# Recréer les tables
python manage.py migrate

# Réinitialiser les données de base
python manage.py init_prosmat

# Importer les indicateurs
python manage.py import_excel "Tableau de Bord de Suivi-Évaluation .xlsx"

# Créer des données de test
python manage.py creer_donnees_test
```

---

## 🔐 COMPTES UTILISATEURS

### Comptes Existants (Phase 1)

| Username | Password | Rôle | Accès Phase 2 |
|----------|----------|------|---------------|
| admin | admin123 | Administrateur | ✅ Complet |
| coordonnateur | prosmat2026 | Coordonnateur | ✅ Dashboard + Exports |
| evaluateur | prosmat2026 | Évaluateur | ✅ Dashboard + Exports |
| maritime | prosmat2026 | Chargé Projet | ❌ Limité |
| plateaux | prosmat2026 | Chargé Projet | ❌ Limité |
| centrale | prosmat2026 | Chargé Projet | ❌ Limité |
| kara | prosmat2026 | Chargé Projet | ❌ Limité |
| savanes | prosmat2026 | Chargé Projet | ❌ Limité |

---

## 📁 STRUCTURE DES FICHIERS PHASE 2

### Nouveaux Fichiers

```
prosmat_se/
├── templates/
│   └── dashboard/
│       └── dashboard_executif.html    # Template du dashboard
├── PHASE2_TERMINEE.md                 # Documentation complète
├── GUIDE_PHASE2.md                    # Guide utilisateur
└── PHASE2_GUIDE_INSTALLATION.md       # Ce fichier
```

### Fichiers Modifiés

```
prosmat_se/
├── dashboard/
│   ├── views.py                       # + dashboard_executif_view()
│   └── urls.py                        # + route /executif/
├── monitoring/
│   ├── views.py                       # + export_excel_view() + export_pdf_view()
│   └── urls.py                        # + routes /export/excel/ et /export/pdf/
├── templates/
│   └── base.html                      # Navigation mise à jour
└── requirements.txt                   # Nouvelles dépendances
```

---

## 🎯 PROCHAINES ÉTAPES

### Après l'installation

1. **Tester toutes les fonctionnalités**
   - Dashboard exécutif
   - Export Excel
   - Export PDF
   - Navigation

2. **Former les utilisateurs**
   - Organiser une session de démonstration
   - Partager le GUIDE_PHASE2.md
   - Répondre aux questions

3. **Collecter les retours**
   - Demander l'avis des utilisateurs
   - Noter les bugs éventuels
   - Identifier les améliorations

4. **Planifier la Phase 3**
   - Graphiques avancés
   - Tableaux de bord personnalisés
   - API REST
   - Notifications email

---

## 📞 SUPPORT

### En cas de problème

1. **Consulter la documentation**:
   - PHASE2_TERMINEE.md (documentation technique)
   - GUIDE_PHASE2.md (guide utilisateur)
   - README.md (vue d'ensemble)

2. **Vérifier les logs**:
   ```bash
   # Logs Django dans le terminal
   # Chercher les erreurs en rouge
   ```

3. **Tester avec un autre navigateur**:
   - Chrome
   - Firefox
   - Edge

4. **Réinstaller les dépendances**:
   ```bash
   pip uninstall reportlab xlsxwriter django-crispy-forms crispy-bootstrap5
   pip install -r requirements.txt
   ```

---

## ✅ CHECKLIST D'INSTALLATION

- [ ] Environnement virtuel activé
- [ ] Dépendances installées (reportlab, xlsxwriter, etc.)
- [ ] Serveur Django démarré
- [ ] Dashboard exécutif accessible
- [ ] Export Excel fonctionne
- [ ] Export PDF fonctionne
- [ ] Graphiques s'affichent correctement
- [ ] Navigation mise à jour
- [ ] Données de test créées
- [ ] Documentation lue

---

## 🎉 FÉLICITATIONS!

Si tous les tests passent, la Phase 2 est installée avec succès!

Vous disposez maintenant de:
- ✅ Dashboard exécutif avec KPI et graphiques
- ✅ Export Excel professionnel
- ✅ Rapports PDF de qualité
- ✅ Système d'alertes intégré

**Le système ProSMAT est prêt pour une utilisation avancée!** 🚀

---

**Développé avec Django 5.1.4 | Python 3.11.9 | Chart.js 4.4.0**
