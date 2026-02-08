# 🎯 ProSMAT - Système de Suivi & Évaluation

## 📌 Présentation du Projet

**ProSMAT** est une application web Django complète pour le suivi et l'évaluation des projets au Togo. Elle permet aux équipes régionales de saisir leurs réalisations, aux coordonnateurs de valider les données, et aux évaluateurs d'analyser les performances.

---

## 🌟 Caractéristiques Principales

### ✨ Multi-utilisateurs avec Rôles
- **5 Chargés de Projet** (un par région du Togo)
- **Coordonnateur National** (vue d'ensemble)
- **Évaluateur** (validation et analyse)
- **Administrateur** (gestion complète)

### 🗺️ Couverture Nationale
- Région Maritime
- Région des Plateaux
- Région Centrale
- Région de la Kara
- Région des Savanes

### 📊 Gestion Complète des Indicateurs
- Indicateurs quantitatifs et qualitatifs
- Niveaux : Impact, Effet, Extrant
- Valeurs de référence et cibles
- Suivi par période (trimestriel)

### 📈 Tableau de Bord Interactif
- Statistiques en temps réel
- Vue par région
- Vue par période
- Indicateurs clés de performance

---

## 🎨 Interface Utilisateur

### Page de Connexion
```
┌─────────────────────────────────────┐
│         🔐 ProSMAT S&E              │
│   Système de Suivi & Évaluation    │
│                                     │
│   Username: [____________]          │
│   Password: [____________]          │
│                                     │
│   [    Se Connecter    ]           │
└─────────────────────────────────────┘
```

### Tableau de Bord
```
┌─────────────────────────────────────────────────────────┐
│  🏠 ProSMAT S&E  │  Accueil  Statistiques  Indicateurs  │
└─────────────────────────────────────────────────────────┘

┌──────────────┐ ┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ 📋 Indicateurs│ │ ✅ Réalisations│ │ ✓ Validées   │ │ 🔄 En cours  │
│      45       │ │      128      │ │      95      │ │      12      │
└──────────────┘ └──────────────┘ └──────────────┘ └──────────────┘

┌─────────────────────────────────┐ ┌─────────────────────────────────┐
│  📊 Dernières Réalisations      │ │  📅 Activités Récentes          │
│  ─────────────────────────────  │ │  ─────────────────────────────  │
│  IND-001 | T1 2026 | 150 | ✓   │ │  Formation | Maritime | En cours│
│  IND-002 | T1 2026 | 85  | ⏳  │ │  Atelier   | Plateaux | Terminé │
│  IND-003 | T1 2026 | 200 | ✓   │ │  Mission   | Centrale | Planifié│
└─────────────────────────────────┘ └─────────────────────────────────┘
```

### Saisie de Réalisation
```
┌─────────────────────────────────────────────────────────┐
│  ✏️ Saisie de Réalisation                               │
└─────────────────────────────────────────────────────────┘

  Indicateur *     [Sélectionner un indicateur ▼]
  
  Période *        [T1 2026 ▼]
  
  Région *         [Région Maritime ▼]
  
  Valeur Réalisée *[____________]
  
  Commentaire      [________________________]
                   [________________________]
  
  Fichier          [Choisir un fichier...]
  
  [    Enregistrer    ]  [    Annuler    ]
```

---

## 🔄 Flux de Travail

### 1️⃣ Saisie (Chargé de Projet)
```
Chargé de Projet
       ↓
Sélectionne Indicateur
       ↓
Saisit la Valeur
       ↓
Ajoute Commentaire
       ↓
Upload Justificatif
       ↓
💾 Enregistrement
```

### 2️⃣ Validation (Coordonnateur)
```
Coordonnateur
       ↓
Consulte Réalisations
       ↓
Vérifie les Données
       ↓
✅ Valide
       ↓
📧 Notification
```

### 3️⃣ Analyse (Évaluateur)
```
Évaluateur
       ↓
Vue d'Ensemble
       ↓
Statistiques
       ↓
Comparaisons
       ↓
📊 Rapports
```

---

## 📊 Architecture Technique

### Stack Technologique
```
┌─────────────────────────────────────┐
│         Frontend                    │
│  Bootstrap 5 + HTML5 + CSS3        │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│         Backend                     │
│         Django 6.0.2                │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│        Base de Données              │
│    SQLite (dev) / PostgreSQL (prod) │
└─────────────────────────────────────┘
```

### Applications Django
```
ProSMAT
├── accounts      → Gestion utilisateurs
├── dashboard     → Tableau de bord
└── monitoring    → Suivi-évaluation
```

---

## 📈 Modèles de Données

### Relations Principales
```
Composante
    ↓ (1:N)
SousComposante
    ↓ (1:N)
Indicateur
    ↓ (1:N)
Realisation ← Periode
    ↑
   User
```

### Modèles Clés
- **User** : Utilisateurs avec rôles et régions
- **Indicateur** : Indicateurs de performance
- **Realisation** : Valeurs saisies par période/région
- **Activite** : Activités du projet
- **Rapport** : Rapports générés

---

## 🚀 Installation en 3 Étapes

### Étape 1 : Installer
```bash
> install.bat
```
✅ Crée l'environnement virtuel  
✅ Installe les dépendances  
✅ Crée la base de données  
✅ Initialise les données  

### Étape 2 : Démarrer
```bash
> start_new.bat
```
✅ Active l'environnement  
✅ Lance le serveur Django  
✅ Ouvre sur http://localhost:8000  

### Étape 3 : Se Connecter
```
Admin:        admin / admin123
Coordonnateur: coordonnateur / prosmat2026
Région:       charge_maritime / prosmat2026
```

---

## 📊 Statistiques du Projet

### Code Source
- **3 Applications Django** complètes
- **7 Modèles de données** métier
- **13 Templates HTML** responsive
- **15+ Vues** fonctionnelles
- **Interface Admin** complète

### Documentation
- **10 Fichiers** de documentation
- **Guide d'installation** détaillé
- **Guide de déploiement** production
- **Roadmap** des fonctionnalités

### Fonctionnalités
- ✅ Authentification multi-rôles
- ✅ Gestion des indicateurs
- ✅ Saisie de réalisations
- ✅ Validation des données
- ✅ Tableau de bord statistiques
- ✅ Gestion des activités
- ✅ Génération de rapports
- ✅ Upload de fichiers
- ✅ Traçabilité complète

---

## 🎯 Cas d'Usage Réels

### Scénario 1 : Saisie Mensuelle
**Acteur :** Chargé de Projet - Région Maritime

1. Se connecte le dernier jour du mois
2. Consulte la liste des indicateurs
3. Saisit les valeurs réalisées
4. Ajoute des commentaires explicatifs
5. Upload les justificatifs (photos, rapports)
6. Soumet pour validation

**Résultat :** Données régionales à jour

### Scénario 2 : Validation Trimestrielle
**Acteur :** Coordonnateur National

1. Reçoit notification de nouvelles saisies
2. Consulte les réalisations par région
3. Vérifie la cohérence des données
4. Demande des clarifications si nécessaire
5. Valide les réalisations conformes
6. Génère le rapport trimestriel

**Résultat :** Données validées et rapport disponible

### Scénario 3 : Analyse Annuelle
**Acteur :** Évaluateur

1. Accède au tableau de bord
2. Compare les performances régionales
3. Analyse les tendances trimestrielles
4. Identifie les indicateurs en retard
5. Génère des recommandations
6. Prépare la présentation pour la direction

**Résultat :** Analyse complète et recommandations

---

## 🔒 Sécurité et Permissions

### Matrice de Permissions
```
┌──────────────────┬─────────┬──────────────┬───────────┬───────┐
│ Fonctionnalité   │ Chargé  │ Coordonnateur│ Évaluateur│ Admin │
├──────────────────┼─────────┼──────────────┼───────────┼───────┤
│ Voir sa région   │    ✅   │      ✅      │     ✅    │   ✅  │
│ Voir tout        │    ❌   │      ✅      │     ✅    │   ✅  │
│ Saisir           │    ✅   │      ✅      │     ✅    │   ✅  │
│ Valider          │    ❌   │      ✅      │     ✅    │   ✅  │
│ Gérer indicateurs│    ❌   │      ❌      │     ❌    │   ✅  │
│ Gérer users      │    ❌   │      ❌      │     ❌    │   ✅  │
└──────────────────┴─────────┴──────────────┴───────────┴───────┘
```

### Traçabilité
- 👤 Qui a saisi quoi
- 📅 Quand
- ✏️ Modifications
- ✅ Validations
- 📊 Consultations

---

## 📱 Responsive Design

### Desktop
```
┌────────────────────────────────────────────────────────┐
│  Navigation │ Statistiques │ Tableaux │ Graphiques    │
└────────────────────────────────────────────────────────┘
```

### Tablet
```
┌──────────────────────────────┐
│  Navigation                  │
│  Statistiques                │
│  Tableaux                    │
└──────────────────────────────┘
```

### Mobile
```
┌──────────────┐
│ ☰ Menu       │
│ Stats        │
│ Données      │
└──────────────┘
```

---

## 🎓 Formation et Support

### Documentation Disponible
- 📘 Guide d'installation
- 📗 Guide utilisateur
- 📙 Guide administrateur
- 📕 Guide de déploiement
- 📔 Architecture technique

### Support
- 💬 Documentation en ligne
- 📧 Support par email
- 🎥 Tutoriels vidéo (à venir)
- 📞 Assistance technique

---

## 🌟 Points Forts

### 1. Simplicité d'Utilisation
- Interface intuitive
- Navigation claire
- Formulaires guidés
- Messages d'aide contextuels

### 2. Robustesse
- Framework Django éprouvé
- Validation des données
- Gestion des erreurs
- Sauvegardes automatiques

### 3. Évolutivité
- Architecture modulaire
- Code bien structuré
- Documentation complète
- Facile à étendre

### 4. Sécurité
- Authentification forte
- Permissions granulaires
- Traçabilité complète
- HTTPS en production

---

## 📈 Roadmap

### ✅ Version 1.0 (Actuelle)
- Gestion des utilisateurs
- Saisie de réalisations
- Validation
- Tableau de bord
- Interface admin

### 🔄 Version 1.1 (Prochaine)
- Graphiques interactifs
- Export Excel
- Notifications email
- Rapports PDF

### 🚀 Version 2.0 (Future)
- API REST
- Application mobile
- BI avancé
- Intégrations externes

---

## 💡 Pourquoi ProSMAT ?

### Avant ProSMAT
- ❌ Fichiers Excel dispersés
- ❌ Consolidation manuelle
- ❌ Risque d'erreurs
- ❌ Pas de traçabilité
- ❌ Difficile à analyser

### Avec ProSMAT
- ✅ Données centralisées
- ✅ Consolidation automatique
- ✅ Validation intégrée
- ✅ Traçabilité complète
- ✅ Analyse en temps réel

---

## 🎉 Conclusion

**ProSMAT** transforme la gestion du suivi-évaluation en un processus :
- 🚀 **Rapide** - Saisie en quelques clics
- 🎯 **Précis** - Validation et contrôles
- 📊 **Analytique** - Statistiques en temps réel
- 🔒 **Sécurisé** - Permissions et traçabilité
- 📱 **Accessible** - Partout, tout le temps

---

## 📞 Contact

**Équipe ProSMAT**  
Email: support@prosmat.tg  
Web: https://prosmat.tg

---

**Prêt à démarrer ?**  
👉 Lancez `install.bat` et commencez en 5 minutes !

---

*ProSMAT - Suivi & Évaluation Simplifié* 🎯
