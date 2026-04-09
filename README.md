# ProSMAT — Plateforme Intégrée

Plateforme complète pour le projet de Sécurité Alimentaire et Nutritionnelle (ProSMAT) au Togo, financé par GAFSP/FIDA.

## Structure

```
ProSMAT/
├── backend/      # Application Django — Suivi & Évaluation (KPI, rapports, utilisateurs)
├── dashboard/    # Dashboard Streamlit — SIG & Data Science (coopératives, cartes)
├── docker-compose.yml
└── README.md
```

## Démarrage rapide

### Avec Docker (recommandé)

```bash
docker-compose up --build
```

- Backend Django  → http://localhost:8000
- Dashboard Streamlit → http://localhost:8501

### Sans Docker

**Backend Django**
```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
cp .env.example .env         # configurer les variables
python manage.py migrate
python manage.py runserver
```

**Dashboard Streamlit**
```bash
cd dashboard
pip install -r requirements.txt
streamlit run dashboard_sig_streamlit.py
```

## Composants

### Backend (`/backend`)
Application Django pour le suivi & évaluation :
- Authentification Firebase + Django
- Gestion des rôles (Chargé de Projet, Coordonnateur, Évaluateur, Admin)
- Saisie et validation des indicateurs KPI
- Génération de rapports (Excel, PDF)
- Couverture des 5 régions du Togo

### Dashboard (`/dashboard`)
Dashboard Streamlit pour l'analyse géospatiale :
- Carte Folium interactive avec clusters
- 13 types de cartes SIG statiques
- Analyses data science (corrélations, scoring)
- Marché agroécologique (Top 10 coopératives)
- 232 coopératives, 5 régions, 16 préfectures

## Développeur
TATCHIDA Louis — MSc Agronomie / MSc Ingénierie Financière adaptée à l'Agriculture / Data Analyst

## Licence
© 2025 ProSMAT — Tous droits réservés
