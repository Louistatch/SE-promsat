
"""
ProSMAT SaaS — Application Streamlit Unifiée
Frontend unique : Suivi & Évaluation + SIG + Data Science
Connecté à l'API Django REST

Développeur: TATCHIDA Louis
Version: 4.0 — 2026
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import st_folium
import geopandas as gpd
import warnings
warnings.filterwarnings("ignore")

from styles import GLOBAL_CSS, REGION_COLORS, REGION_LABELS, STATUS_COLORS
import api_client as api

# ── Config page ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ProSMAT SaaS",
    page_icon="🌾",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

REGIONS = list(REGION_LABELS.keys())

# ── Session state ────────────────────────────────────────────────────────────
if "token" not in st.session_state:
    st.session_state.token = None
if "user_info" not in st.session_state:
    st.session_state.user_info = {}
if "page" not in st.session_state:
    st.session_state.page = "dashboard"


# ════════════════════════════════════════════════════════════════════════════
# AUTH
# ════════════════════════════════════════════════════════════════════════════

def page_login():
    col1, col2, col3 = st.columns([1, 1.4, 1])
    with col2:
        st.markdown("""
        <div style='text-align:center; padding: 2rem 0 1rem;'>
            <div style='font-size:3rem;'>🌾</div>
            <h1 style='color:#e2e8f0; font-size:1.8rem; margin:.5rem 0;'>ProSMAT</h1>
            <p style='color:#718096; font-size:.9rem;'>Plateforme de Suivi & Évaluation — Togo</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            username = st.text_input("Identifiant", placeholder="nom.utilisateur")
            password = st.text_input("Mot de passe", type="password")
            submitted = st.form_submit_button("Se connecter", use_container_width=True)

        if submitted:
            with st.spinner("Connexion..."):
                token = api.login(username, password)
            if token:
                st.session_state.token = token
                st.session_state.user_info = {"username": username}
                st.rerun()
            else:
                st.error("Identifiants incorrects ou serveur inaccessible.")

        st.markdown("""
        <p style='text-align:center; color:#4a5568; font-size:.8rem; margin-top:2rem;'>
        ProSMAT · GAFSP/FIDA · Togo · © 2026
        </p>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════
# SIDEBAR NAVIGATION
# ════════════════════════════════════════════════════════════════════════════

def sidebar_nav():
    with st.sidebar:
        st.markdown("""
        <div style='padding:.8rem; text-align:center; border-bottom:1px solid #2d3748; margin-bottom:1rem;'>
            <span style='font-size:1.5rem;'>🌾</span>
            <span style='font-size:1rem; font-weight:700; color:#e2e8f0; margin-left:.5rem;'>ProSMAT</span>
        </div>""", unsafe_allow_html=True)

        pages = [
            ("📊", "dashboard",    "Tableau de bord"),
            ("📝", "saisie",       "Saisie S&E"),
            ("📋", "realisations", "Réalisations"),
            ("🗺️", "carte",        "Carte SIG"),
            ("📈", "analytics",    "Analytics"),
            ("🚨", "alertes",      "Alertes Qualité"),
            ("📄", "rapports",     "Rapports"),
        ]

        for icon, key, label in pages:
            active = "active" if st.session_state.page == key else ""
            if st.button(f"{icon}  {label}", key=f"nav_{key}", use_container_width=True):
                st.session_state.page = key
                st.rerun()

        st.markdown("<div style='border-top:1px solid #2d3748; margin-top:1rem; padding-top:1rem;'>", unsafe_allow_html=True)
        user = st.session_state.user_info.get("username", "—")
        st.markdown(f"<p style='color:#718096; font-size:.8rem; text-align:center;'>👤 {user}</p>", unsafe_allow_html=True)
        if st.button("🚪 Déconnexion", use_container_width=True):
            st.session_state.token = None
            st.session_state.user_info = {}
            st.rerun()


# ════════════════════════════════════════════════════════════════════════════
# HELPERS UI
# ════════════════════════════════════════════════════════════════════════════

def kpi_card(label: str, value, accent: str = "#3182ce", delta: str = None, delta_up: bool = True):
    delta_html = ""
    if delta:
        cls = "up" if delta_up else "down"
        arrow = "↑" if delta_up else "↓"
        delta_html = f'<div class="kpi-delta {cls}">{arrow} {delta}</div>'
    st.markdown(f"""
    <div class="kpi-card" style="--accent:{accent};">
        <div class="kpi-value" style="color:{accent};">{value}</div>
        <div class="kpi-label">{label}</div>
        {delta_html}
    </div>""", unsafe_allow_html=True)


def section_title(title: str):
    st.markdown(f'<div class="section-title">{title}</div>', unsafe_allow_html=True)


def progress_bar(pct: float, color: str = "#3182ce"):
    pct = min(max(pct, 0), 100)
    st.markdown(f"""
    <div class="progress-wrap">
        <div class="progress-bar" style="width:{pct:.1f}%; background:{color};"></div>
    </div>
    <small style="color:#718096;">{pct:.1f}%</small>""", unsafe_allow_html=True)


def badge(text: str, cls: str = "blue"):
    st.markdown(f'<span class="badge badge-{cls}">{text}</span>', unsafe_allow_html=True)


def header(title: str, subtitle: str = ""):
    st.markdown(f"""
    <div class="saas-header">
        <div>
            <h1>{title}</h1>
            {'<p>' + subtitle + '</p>' if subtitle else ''}
        </div>
    </div>""", unsafe_allow_html=True)



# ════════════════════════════════════════════════════════════════════════════
# PAGE : TABLEAU DE BORD
# ════════════════════════════════════════════════════════════════════════════

def page_dashboard():
    token = st.session_state.token
    header("📊 Tableau de bord", "Vue d'ensemble ProSMAT — Togo")

    with st.spinner("Chargement des données..."):
        stats       = api.fetch_stats(token)
        realisations = api.fetch_realisations(token)
        alertes     = api.fetch_alertes(token)
        activites   = api.fetch_activites(token)

    # ── KPI row ──
    cols = st.columns(5)
    kpis = [
        ("Indicateurs",       stats.get("total_indicateurs", 0),       "#3182ce"),
        ("Réalisations",      stats.get("total_realisations", 0),       "#9f7aea"),
        ("Validées",          stats.get("realisations_validees", 0),    "#48bb78"),
        ("Performance",       f"{stats.get('performance_globale', 0):.1f}%", "#f6ad55"),
        ("Alertes actives",   stats.get("alertes_non_resolues", 0),     "#fc8181"),
    ]
    for col, (label, val, color) in zip(cols, kpis):
        with col:
            kpi_card(label, val, color)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ──
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        section_title("Performance par région")
        if realisations:
            df = pd.DataFrame(realisations)
            if "region" in df.columns and "valeur_realisee" in df.columns:
                df["valeur_realisee"] = pd.to_numeric(df["valeur_realisee"], errors="coerce")
                by_region = df.groupby("region")["valeur_realisee"].sum().reset_index()
                by_region["color"] = by_region["region"].map(REGION_COLORS)
                fig = px.bar(
                    by_region, x="region", y="valeur_realisee",
                    color="region",
                    color_discrete_map=REGION_COLORS,
                    labels={"region": "Région", "valeur_realisee": "Total réalisé"},
                    template="plotly_dark",
                )
                fig.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    showlegend=False,
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=280,
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("Aucune réalisation disponible.")

    with col_right:
        section_title("Statut des activités")
        if activites:
            df_act = pd.DataFrame(activites)
            if "statut" in df_act.columns:
                counts = df_act["statut"].value_counts().reset_index()
                counts.columns = ["statut", "count"]
                fig2 = px.pie(
                    counts, names="statut", values="count",
                    color="statut",
                    color_discrete_map=STATUS_COLORS,
                    hole=0.55,
                    template="plotly_dark",
                )
                fig2.update_layout(
                    paper_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=0, r=0, t=10, b=0),
                    height=280,
                    legend=dict(font=dict(color="#a0aec0")),
                )
                st.plotly_chart(fig2, use_container_width=True)
        else:
            st.info("Aucune activité disponible.")

    # ── Évolution temporelle ──
    section_title("Évolution des réalisations")
    if realisations:
        df = pd.DataFrame(realisations)
        if "periode" in df.columns:
            df["periode_nom"] = df["periode"].apply(
                lambda p: p.get("nom", "?") if isinstance(p, dict) else str(p)
            )
            df["valeur_realisee"] = pd.to_numeric(df["valeur_realisee"], errors="coerce")
            evo = df.groupby(["periode_nom", "region"])["valeur_realisee"].sum().reset_index()
            fig3 = px.line(
                evo, x="periode_nom", y="valeur_realisee",
                color="region",
                color_discrete_map=REGION_COLORS,
                markers=True,
                labels={"periode_nom": "Période", "valeur_realisee": "Réalisé", "region": "Région"},
                template="plotly_dark",
            )
            fig3.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=0, r=0, t=10, b=0),
                height=260,
                legend=dict(font=dict(color="#a0aec0")),
            )
            st.plotly_chart(fig3, use_container_width=True)

    # ── Alertes récentes ──
    section_title("Alertes qualité récentes")
    if alertes:
        df_al = pd.DataFrame(alertes[:8])
        cols_show = [c for c in ["type_alerte_display", "severite_display", "message", "date_detection"] if c in df_al.columns]
        if cols_show:
            st.dataframe(
                df_al[cols_show].rename(columns={
                    "type_alerte_display": "Type",
                    "severite_display": "Sévérité",
                    "message": "Message",
                    "date_detection": "Date",
                }),
                use_container_width=True,
                hide_index=True,
            )
    else:
        st.success("Aucune alerte active.")



# ════════════════════════════════════════════════════════════════════════════
# PAGE : SAISIE S&E
# ════════════════════════════════════════════════════════════════════════════

def page_saisie():
    token = st.session_state.token
    header("📝 Saisie des réalisations", "Enregistrer les données de terrain")

    with st.spinner("Chargement..."):
        indicateurs = api.fetch_indicateurs(token)
        periodes    = api.fetch_periodes(token)

    if not indicateurs:
        st.warning("Aucun indicateur disponible. Vérifiez la connexion au backend.")
        return
    if not periodes:
        st.warning("Aucune période disponible.")
        return

    col_form, col_info = st.columns([1.4, 1])

    with col_form:
        st.markdown('<div class="form-card">', unsafe_allow_html=True)
        section_title("Nouvelle réalisation")

        ind_options = {f"{i['code']} — {i['libelle'][:60]}": i["id"] for i in indicateurs}
        per_options = {p.get("nom", str(p["id"])): p["id"] for p in periodes}

        ind_label = st.selectbox("Indicateur *", list(ind_options.keys()))
        per_label = st.selectbox("Période *", list(per_options.keys()))
        region    = st.selectbox("Région *", REGIONS, format_func=lambda r: REGION_LABELS.get(r, r))

        col_v, col_h, col_f = st.columns(3)
        with col_v:
            valeur = st.number_input("Valeur réalisée *", min_value=0.0, step=0.01)
        with col_h:
            hommes = st.number_input("Hommes", min_value=0.0, step=1.0)
        with col_f:
            femmes = st.number_input("Femmes", min_value=0.0, step=1.0)

        commentaire = st.text_area("Commentaire", height=80)

        # Validation genre en temps réel
        if hommes + femmes > 0 and abs(valeur - (hommes + femmes)) > 0.01:
            st.warning(f"⚠️ Incohérence genre : {hommes:.0f} H + {femmes:.0f} F = {hommes+femmes:.0f} ≠ {valeur:.0f}")

        submitted = st.button("💾 Enregistrer", use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

        if submitted:
            if valeur <= 0:
                st.error("La valeur réalisée doit être > 0.")
            else:
                payload = {
                    "indicateur_id": ind_options[ind_label],
                    "periode_id":    per_options[per_label],
                    "region":        region,
                    "valeur_realisee": valeur,
                    "hommes":        hommes,
                    "femmes":        femmes,
                    "commentaire":   commentaire,
                }
                with st.spinner("Enregistrement..."):
                    result = api.create_realisation(token, payload)
                if "error" in result:
                    st.error(f"Erreur : {result['error']}")
                else:
                    st.success("✅ Réalisation enregistrée avec succès !")
                    st.balloons()

    with col_info:
        section_title("Indicateur sélectionné")
        if indicateurs:
            ind_id = ind_options.get(ind_label)
            ind_data = next((i for i in indicateurs if i["id"] == ind_id), None)
            if ind_data:
                st.markdown(f"""
                <div class="form-card">
                    <p style="color:#a0aec0; font-size:.8rem; margin:0;">Code</p>
                    <p style="color:#e2e8f0; font-weight:600;">{ind_data.get('code','—')}</p>
                    <p style="color:#a0aec0; font-size:.8rem; margin:0;">Libellé</p>
                    <p style="color:#e2e8f0;">{ind_data.get('libelle','—')}</p>
                    <p style="color:#a0aec0; font-size:.8rem; margin:0;">Unité</p>
                    <p style="color:#e2e8f0;">{ind_data.get('unite_mesure','—')}</p>
                    <p style="color:#a0aec0; font-size:.8rem; margin:0;">Cible finale</p>
                    <p style="color:#f6ad55; font-weight:700; font-size:1.2rem;">{ind_data.get('cible_finale','—')}</p>
                    <p style="color:#a0aec0; font-size:.8rem; margin:0;">Niveau</p>
                    <p style="color:#e2e8f0;">{ind_data.get('niveau','—')}</p>
                </div>
                """, unsafe_allow_html=True)



# ════════════════════════════════════════════════════════════════════════════
# PAGE : RÉALISATIONS
# ════════════════════════════════════════════════════════════════════════════

def page_realisations():
    token = st.session_state.token
    header("📋 Réalisations", "Suivi des données saisies")

    with st.spinner("Chargement..."):
        realisations = api.fetch_realisations(token)
        periodes     = api.fetch_periodes(token)

    if not realisations:
        st.info("Aucune réalisation disponible.")
        return

    df = pd.DataFrame(realisations)

    # Extraire les champs imbriqués
    if "indicateur" in df.columns:
        df["ind_code"]   = df["indicateur"].apply(lambda x: x.get("code", "?") if isinstance(x, dict) else "?")
        df["ind_libelle"] = df["indicateur"].apply(lambda x: x.get("libelle", "?")[:50] if isinstance(x, dict) else "?")
        df["cible"]      = df["indicateur"].apply(lambda x: x.get("cible_finale") if isinstance(x, dict) else None)
    if "periode" in df.columns:
        df["periode_nom"] = df["periode"].apply(lambda x: x.get("nom", "?") if isinstance(x, dict) else "?")

    df["valeur_realisee"] = pd.to_numeric(df["valeur_realisee"], errors="coerce")
    df["pourcentage_atteinte"] = pd.to_numeric(df.get("pourcentage_atteinte", 0), errors="coerce")

    # ── Filtres ──
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        regions_sel = st.multiselect("Région", REGIONS, default=REGIONS,
                                     format_func=lambda r: REGION_LABELS.get(r, r))
    with col_f2:
        per_opts = ["Toutes"] + sorted(df["periode_nom"].unique().tolist()) if "periode_nom" in df.columns else ["Toutes"]
        per_sel = st.selectbox("Période", per_opts)
    with col_f3:
        val_sel = st.selectbox("Statut validation", ["Tous", "Validées", "En attente"])

    mask = df["region"].isin(regions_sel) if regions_sel else pd.Series([True] * len(df))
    if per_sel != "Toutes" and "periode_nom" in df.columns:
        mask &= df["periode_nom"] == per_sel
    if val_sel == "Validées":
        mask &= df["valide"] == True
    elif val_sel == "En attente":
        mask &= df["valide"] == False

    df_f = df[mask].copy()

    # ── Synthèse ──
    col_s1, col_s2, col_s3, col_s4 = st.columns(4)
    with col_s1:
        kpi_card("Total", len(df_f), "#3182ce")
    with col_s2:
        kpi_card("Validées", int(df_f["valide"].sum()), "#48bb78")
    with col_s3:
        kpi_card("En attente", int((~df_f["valide"]).sum()), "#f6ad55")
    with col_s4:
        avg_pct = df_f["pourcentage_atteinte"].mean() if len(df_f) else 0
        kpi_card("% Atteinte moy.", f"{avg_pct:.1f}%", "#9f7aea")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Heatmap région × période ──
    if "periode_nom" in df_f.columns and len(df_f) > 0:
        section_title("Heatmap réalisations — Région × Période")
        pivot = df_f.pivot_table(
            index="region", columns="periode_nom",
            values="valeur_realisee", aggfunc="sum", fill_value=0
        )
        fig = px.imshow(
            pivot,
            color_continuous_scale="Blues",
            template="plotly_dark",
            labels=dict(x="Période", y="Région", color="Réalisé"),
        )
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=10, b=0),
            height=260,
        )
        st.plotly_chart(fig, use_container_width=True)

    # ── Tableau ──
    section_title(f"Détail ({len(df_f)} entrées)")
    cols_show = [c for c in ["ind_code", "ind_libelle", "periode_nom", "region",
                              "valeur_realisee", "hommes", "femmes",
                              "pourcentage_atteinte", "valide"] if c in df_f.columns]
    rename_map = {
        "ind_code": "Code", "ind_libelle": "Indicateur", "periode_nom": "Période",
        "region": "Région", "valeur_realisee": "Réalisé", "hommes": "H",
        "femmes": "F", "pourcentage_atteinte": "% Cible", "valide": "Validé",
    }
    st.dataframe(
        df_f[cols_show].rename(columns=rename_map),
        use_container_width=True,
        hide_index=True,
    )

    # ── Export ──
    csv = df_f[cols_show].rename(columns=rename_map).to_csv(index=False).encode("utf-8")
    st.download_button("⬇️ Exporter CSV", csv, "realisations.csv", "text/csv")



# ════════════════════════════════════════════════════════════════════════════
# PAGE : CARTE SIG
# ════════════════════════════════════════════════════════════════════════════

def page_carte():
    token = st.session_state.token
    header("🗺️ Carte SIG", "Visualisation géospatiale — Coopératives & Indicateurs")

    # Charger les données géographiques
    try:
        gdf_regions = gpd.read_file("gadm41_TGO.gpkg", layer=1)
        gdf_prefectures = gpd.read_file("gadm41_TGO.gpkg", layer=2)
        geo_ok = True
    except Exception:
        geo_ok = False

    # Charger les réalisations depuis l'API
    with st.spinner("Chargement des données..."):
        realisations = api.fetch_realisations(token)

    col_ctrl, col_map = st.columns([1, 3])

    with col_ctrl:
        section_title("Contrôles")
        map_type = st.radio("Type de carte", ["Réalisations S&E", "Coopératives (Excel)"])
        zoom_level = st.selectbox("Zoom", ["Pays", "Région"])
        if zoom_level == "Région":
            region_zoom = st.selectbox("Région", REGIONS, format_func=lambda r: REGION_LABELS.get(r, r))

        if map_type == "Réalisations S&E" and realisations:
            df_r = pd.DataFrame(realisations)
            if "indicateur" in df_r.columns:
                ind_opts = {
                    f"{i.get('code','?')} — {i.get('libelle','?')[:40]}": i.get("id")
                    for r in realisations
                    if isinstance(r.get("indicateur"), dict)
                    for i in [r["indicateur"]]
                }
                ind_sel = st.selectbox("Indicateur", list(ind_opts.keys()) or ["—"])

        if map_type == "Coopératives (Excel)":
            uploaded = st.file_uploader("Charger Excel coopératives", type=["xlsx"])

    with col_map:
        # ── Carte Folium ──
        center = [8.6, 0.8]
        zoom_start = 7

        if zoom_level == "Région" and geo_ok:
            region_map = {
                "MARITIME": "Maritime", "PLATEAUX": "Plateaux",
                "CENTRALE": "Centrale", "KARA": "Kara", "SAVANES": "Savanes"
            }
            r_name = region_map.get(region_zoom, "")
            sub = gdf_regions[gdf_regions["NAME_1"].str.upper().str.contains(r_name.upper(), na=False)]
            if not sub.empty:
                bounds = sub.total_bounds
                center = [(bounds[1] + bounds[3]) / 2, (bounds[0] + bounds[2]) / 2]
                zoom_start = 9

        m = folium.Map(location=center, zoom_start=zoom_start, tiles="CartoDB dark_matter")

        # Couche régions
        if geo_ok:
            folium.GeoJson(
                gdf_regions.__geo_interface__,
                style_function=lambda f: {
                    "fillColor": "#2b6cb0", "color": "#63b3ed",
                    "weight": 1.5, "fillOpacity": 0.15,
                },
                tooltip=folium.GeoJsonTooltip(fields=["NAME_1"], aliases=["Région:"]),
            ).add_to(m)

        # Couche réalisations S&E (cercles proportionnels par région)
        if map_type == "Réalisations S&E" and realisations:
            df_r = pd.DataFrame(realisations)
            df_r["valeur_realisee"] = pd.to_numeric(df_r["valeur_realisee"], errors="coerce")
            by_region = df_r.groupby("region")["valeur_realisee"].sum().reset_index()

            region_coords = {
                "MARITIME": [6.2, 1.2], "PLATEAUX": [7.0, 1.1],
                "CENTRALE": [8.5, 1.1], "KARA": [9.5, 1.2], "SAVANES": [10.5, 0.5],
            }
            max_val = by_region["valeur_realisee"].max() or 1
            for _, row in by_region.iterrows():
                coords = region_coords.get(row["region"])
                if coords:
                    radius = 10 + 40 * (row["valeur_realisee"] / max_val)
                    folium.CircleMarker(
                        location=coords,
                        radius=radius,
                        color=REGION_COLORS.get(row["region"], "#3182ce"),
                        fill=True,
                        fill_opacity=0.7,
                        popup=folium.Popup(
                            f"<b>{REGION_LABELS.get(row['region'], row['region'])}</b><br>"
                            f"Total réalisé: {row['valeur_realisee']:,.0f}",
                            max_width=200,
                        ),
                    ).add_to(m)

        # Couche coopératives (Excel uploadé)
        if map_type == "Coopératives (Excel)" and "uploaded" in dir() and uploaded:
            try:
                df_coop = pd.read_excel(uploaded)
                lat_col = next((c for c in df_coop.columns if "lat" in c.lower()), None)
                lon_col = next((c for c in df_coop.columns if "lon" in c.lower() or "lng" in c.lower()), None)
                if lat_col and lon_col:
                    df_coop = df_coop.dropna(subset=[lat_col, lon_col])
                    cluster = MarkerCluster().add_to(m)
                    for _, row in df_coop.iterrows():
                        region_val = str(row.get("region", "")).upper()
                        color = REGION_COLORS.get(region_val, "#3182ce")
                        popup_html = "<br>".join(
                            f"<b>{k}:</b> {v}" for k, v in row.items()
                            if pd.notna(v) and k not in [lat_col, lon_col]
                        )
                        folium.CircleMarker(
                            location=[row[lat_col], row[lon_col]],
                            radius=6, color=color, fill=True, fill_opacity=0.8,
                            popup=folium.Popup(popup_html, max_width=300),
                        ).add_to(cluster)
                    st.success(f"{len(df_coop)} coopératives chargées.")
                else:
                    st.warning("Colonnes latitude/longitude non trouvées dans le fichier.")
            except Exception as e:
                st.error(f"Erreur lecture fichier : {e}")

        folium.LayerControl().add_to(m)
        st_folium(m, width=None, height=520, returned_objects=[])



# ════════════════════════════════════════════════════════════════════════════
# PAGE : ANALYTICS AVANCÉS
# ════════════════════════════════════════════════════════════════════════════

def page_analytics():
    token = st.session_state.token
    header("📈 Analytics", "Analyses avancées & Data Science")

    with st.spinner("Chargement..."):
        realisations = api.fetch_realisations(token)
        indicateurs  = api.fetch_indicateurs(token)
        synthese     = api.fetch_synthese(token)

    if not realisations:
        st.info("Pas de données disponibles.")
        return

    df = pd.DataFrame(realisations)
    df["valeur_realisee"]      = pd.to_numeric(df["valeur_realisee"], errors="coerce")
    df["hommes"]               = pd.to_numeric(df.get("hommes", 0), errors="coerce").fillna(0)
    df["femmes"]               = pd.to_numeric(df.get("femmes", 0), errors="coerce").fillna(0)
    df["pourcentage_atteinte"] = pd.to_numeric(df.get("pourcentage_atteinte", 0), errors="coerce").fillna(0)

    if "indicateur" in df.columns:
        df["niveau"] = df["indicateur"].apply(lambda x: x.get("niveau", "?") if isinstance(x, dict) else "?")
        df["ind_code"] = df["indicateur"].apply(lambda x: x.get("code", "?") if isinstance(x, dict) else "?")
    if "periode" in df.columns:
        df["periode_nom"] = df["periode"].apply(lambda x: x.get("nom", "?") if isinstance(x, dict) else "?")

    tab1, tab2, tab3, tab4 = st.tabs(["🎯 Performance", "👥 Genre", "📊 Synthèse nationale", "🔍 Corrélations"])

    # ── Tab 1 : Performance ──
    with tab1:
        col1, col2 = st.columns(2)

        with col1:
            section_title("% Atteinte par région")
            by_reg = df.groupby("region")["pourcentage_atteinte"].mean().reset_index()
            fig = px.bar(
                by_reg, x="pourcentage_atteinte", y="region",
                orientation="h",
                color="region", color_discrete_map=REGION_COLORS,
                labels={"pourcentage_atteinte": "% Atteinte", "region": ""},
                template="plotly_dark",
            )
            fig.add_vline(x=100, line_dash="dash", line_color="#fc8181", annotation_text="Cible 100%")
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, height=300, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            section_title("Performance par niveau d'indicateur")
            if "niveau" in df.columns:
                by_niv = df.groupby("niveau")["pourcentage_atteinte"].mean().reset_index()
                fig2 = px.bar(
                    by_niv, x="niveau", y="pourcentage_atteinte",
                    color="niveau",
                    color_discrete_sequence=["#3182ce", "#9f7aea", "#48bb78"],
                    labels={"niveau": "Niveau", "pourcentage_atteinte": "% Atteinte moy."},
                    template="plotly_dark",
                )
                fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                                   showlegend=False, height=300, margin=dict(l=0, r=0, t=10, b=0))
                st.plotly_chart(fig2, use_container_width=True)

        # Top 10 indicateurs
        section_title("Top 10 indicateurs — % Atteinte")
        top10 = df.groupby("ind_code")["pourcentage_atteinte"].mean().nlargest(10).reset_index()
        fig3 = px.bar(
            top10, x="pourcentage_atteinte", y="ind_code",
            orientation="h",
            color="pourcentage_atteinte",
            color_continuous_scale="Greens",
            labels={"pourcentage_atteinte": "% Atteinte", "ind_code": "Indicateur"},
            template="plotly_dark",
        )
        fig3.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                           height=320, margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig3, use_container_width=True)

    # ── Tab 2 : Genre ──
    with tab2:
        section_title("Désagrégation par genre")
        col1, col2 = st.columns(2)

        with col1:
            by_reg_genre = df.groupby("region")[["hommes", "femmes"]].sum().reset_index()
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Hommes", x=by_reg_genre["region"],
                                 y=by_reg_genre["hommes"], marker_color="#63b3ed"))
            fig.add_trace(go.Bar(name="Femmes", x=by_reg_genre["region"],
                                 y=by_reg_genre["femmes"], marker_color="#f687b3"))
            fig.update_layout(
                barmode="group", template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                height=300, margin=dict(l=0, r=0, t=10, b=0),
                legend=dict(font=dict(color="#a0aec0")),
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            total_h = df["hommes"].sum()
            total_f = df["femmes"].sum()
            fig2 = go.Figure(go.Pie(
                labels=["Hommes", "Femmes"],
                values=[total_h, total_f],
                hole=0.6,
                marker_colors=["#63b3ed", "#f687b3"],
            ))
            fig2.update_layout(
                template="plotly_dark",
                paper_bgcolor="rgba(0,0,0,0)",
                height=300, margin=dict(l=0, r=0, t=10, b=0),
                annotations=[dict(text=f"{total_f/(total_h+total_f)*100:.1f}%<br>Femmes" if (total_h+total_f) > 0 else "—",
                                  x=0.5, y=0.5, font_size=16, showarrow=False, font_color="#f687b3")],
            )
            st.plotly_chart(fig2, use_container_width=True)

    # ── Tab 3 : Synthèse nationale ──
    with tab3:
        section_title("Synthèse nationale par indicateur")
        if synthese:
            df_syn = pd.DataFrame(synthese)
            cols_show = [c for c in ["indicateur_code", "indicateur_libelle", "periode_nom",
                                      "total_realise", "cible", "pourcentage_atteinte",
                                      "total_hommes", "total_femmes"] if c in df_syn.columns]
            if cols_show:
                st.dataframe(
                    df_syn[cols_show].rename(columns={
                        "indicateur_code": "Code", "indicateur_libelle": "Indicateur",
                        "periode_nom": "Période", "total_realise": "Réalisé",
                        "cible": "Cible", "pourcentage_atteinte": "% Atteinte",
                        "total_hommes": "Hommes", "total_femmes": "Femmes",
                    }),
                    use_container_width=True, hide_index=True,
                )
        else:
            st.info("Synthèse nationale non disponible (accès restreint ou données manquantes).")

    # ── Tab 4 : Corrélations ──
    with tab4:
        section_title("Matrice de corrélation")
        num_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        num_cols = [c for c in num_cols if c not in ["id"]]
        if len(num_cols) >= 2:
            corr = df[num_cols].corr()
            fig = px.imshow(
                corr, text_auto=".2f",
                color_continuous_scale="RdBu_r",
                template="plotly_dark",
                zmin=-1, zmax=1,
            )
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=400,
                              margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)



# ════════════════════════════════════════════════════════════════════════════
# PAGE : ALERTES QUALITÉ
# ════════════════════════════════════════════════════════════════════════════

def page_alertes():
    token = st.session_state.token
    header("🚨 Alertes Qualité", "Contrôle et résolution des anomalies")

    with st.spinner("Chargement..."):
        alertes = api.fetch_alertes(token)

    if not alertes:
        st.success("✅ Aucune alerte active. Données de bonne qualité.")
        return

    df = pd.DataFrame(alertes)

    # KPIs
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        kpi_card("Total alertes", len(df), "#fc8181")
    with col2:
        non_res = int((~df["resolue"]).sum()) if "resolue" in df.columns else 0
        kpi_card("Non résolues", non_res, "#f6ad55")
    with col3:
        critiques = int((df.get("severite", pd.Series()) == "CRITIQUE").sum())
        kpi_card("Critiques", critiques, "#fc8181")
    with col4:
        resolues = int(df["resolue"].sum()) if "resolue" in df.columns else 0
        kpi_card("Résolues", resolues, "#48bb78")

    st.markdown("<br>", unsafe_allow_html=True)

    # Graphique par type
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        section_title("Alertes par type")
        if "type_alerte" in df.columns:
            by_type = df["type_alerte"].value_counts().reset_index()
            fig = px.bar(by_type, x="type_alerte", y="count",
                         color="type_alerte",
                         color_discrete_sequence=["#fc8181", "#f6ad55", "#63b3ed", "#9f7aea"],
                         template="plotly_dark",
                         labels={"type_alerte": "Type", "count": "Nombre"})
            fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                              showlegend=False, height=250, margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        section_title("Alertes par sévérité")
        if "severite" in df.columns:
            by_sev = df["severite"].value_counts().reset_index()
            fig2 = px.pie(by_sev, names="severite", values="count",
                          color="severite",
                          color_discrete_map={"CRITIQUE": "#fc8181", "IMPORTANT": "#f6ad55", "MINEUR": "#68d391"},
                          hole=0.5, template="plotly_dark")
            fig2.update_layout(paper_bgcolor="rgba(0,0,0,0)", height=250,
                               margin=dict(l=0, r=0, t=10, b=0))
            st.plotly_chart(fig2, use_container_width=True)

    # Tableau alertes
    section_title("Liste des alertes")
    cols_show = [c for c in ["type_alerte_display", "severite_display", "message",
                              "resolue", "date_detection"] if c in df.columns]
    if cols_show:
        df_show = df[~df["resolue"]] if "resolue" in df.columns else df
        st.dataframe(
            df_show[cols_show].rename(columns={
                "type_alerte_display": "Type", "severite_display": "Sévérité",
                "message": "Message", "resolue": "Résolue", "date_detection": "Date",
            }),
            use_container_width=True, hide_index=True,
        )

    # Résoudre une alerte
    section_title("Résoudre une alerte")
    alerte_ids = df[~df["resolue"]]["id"].tolist() if "resolue" in df.columns else []
    if alerte_ids:
        alerte_sel = st.selectbox("ID Alerte à résoudre", alerte_ids)
        if st.button("✅ Marquer comme résolue"):
            result = api.resoudre_alerte(token, alerte_sel)
            if result:
                st.success("Alerte résolue.")
                st.rerun()
    else:
        st.info("Toutes les alertes sont résolues.")


# ════════════════════════════════════════════════════════════════════════════
# PAGE : RAPPORTS
# ════════════════════════════════════════════════════════════════════════════

def page_rapports():
    token = st.session_state.token
    header("📄 Rapports", "Génération et consultation des rapports")

    with st.spinner("Chargement..."):
        realisations = api.fetch_realisations(token)
        indicateurs  = api.fetch_indicateurs(token)
        alertes      = api.fetch_alertes(token)

    tab1, tab2 = st.tabs(["📊 Rapport automatique", "📋 Historique"])

    with tab1:
        section_title("Générer un rapport")
        col1, col2 = st.columns(2)
        with col1:
            type_rapport = st.selectbox("Type", ["Synthèse nationale", "Rapport régional", "Contrôle qualité"])
        with col2:
            format_export = st.selectbox("Format", ["Excel", "CSV"])

        if st.button("🔄 Générer", use_container_width=True):
            if not realisations:
                st.warning("Aucune donnée disponible.")
            else:
                df = pd.DataFrame(realisations)
                df["valeur_realisee"] = pd.to_numeric(df["valeur_realisee"], errors="coerce")
                if "indicateur" in df.columns:
                    df["ind_code"]    = df["indicateur"].apply(lambda x: x.get("code", "?") if isinstance(x, dict) else "?")
                    df["ind_libelle"] = df["indicateur"].apply(lambda x: x.get("libelle", "?") if isinstance(x, dict) else "?")
                if "periode" in df.columns:
                    df["periode_nom"] = df["periode"].apply(lambda x: x.get("nom", "?") if isinstance(x, dict) else "?")

                if format_export == "CSV":
                    csv = df.to_csv(index=False).encode("utf-8")
                    st.download_button("⬇️ Télécharger CSV", csv, "rapport.csv", "text/csv")
                else:
                    import io
                    output = io.BytesIO()
                    with pd.ExcelWriter(output, engine="openpyxl") as writer:
                        df.to_excel(writer, sheet_name="Réalisations", index=False)
                        if alertes:
                            pd.DataFrame(alertes).to_excel(writer, sheet_name="Alertes", index=False)
                    st.download_button(
                        "⬇️ Télécharger Excel",
                        output.getvalue(),
                        "rapport_prosmat.xlsx",
                        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                    )
                st.success("Rapport généré.")

    with tab2:
        section_title("Rapports disponibles")
        rapports = api.get("rapports/", token)
        if rapports:
            items = rapports.get("results", rapports) if isinstance(rapports, dict) else rapports
            if items:
                st.dataframe(pd.DataFrame(items), use_container_width=True, hide_index=True)
            else:
                st.info("Aucun rapport enregistré.")
        else:
            st.info("Aucun rapport disponible.")


# ════════════════════════════════════════════════════════════════════════════
# ROUTER PRINCIPAL
# ════════════════════════════════════════════════════════════════════════════

def main():
    if not st.session_state.token:
        page_login()
        return

    sidebar_nav()

    page = st.session_state.page
    if page == "dashboard":
        page_dashboard()
    elif page == "saisie":
        page_saisie()
    elif page == "realisations":
        page_realisations()
    elif page == "carte":
        page_carte()
    elif page == "analytics":
        page_analytics()
    elif page == "alertes":
        page_alertes()
    elif page == "rapports":
        page_rapports()


if __name__ == "__main__":
    main()
