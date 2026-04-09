"""
Styles CSS globaux pour le SaaS ProSMAT Streamlit
"""

GLOBAL_CSS = """
<style>
/* ── Reset & Base ── */
[data-testid="stAppViewContainer"] { background: #0f1117; }
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d1b2a 0%, #1b2838 100%);
    border-right: 1px solid #2d3748;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }

/* ── Header ── */
.saas-header {
    background: linear-gradient(135deg, #1a365d 0%, #2b6cb0 60%, #3182ce 100%);
    padding: 1.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 1.5rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    box-shadow: 0 4px 24px rgba(49,130,206,0.3);
}
.saas-header h1 { color: #fff; font-size: 1.8rem; font-weight: 700; margin: 0; }
.saas-header p  { color: #bee3f8; font-size: 0.9rem; margin: 0; }

/* ── KPI Cards ── */
.kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 1rem; margin-bottom: 1.5rem; }
.kpi-card {
    background: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 1.2rem;
    text-align: center;
    transition: transform .2s, box-shadow .2s;
    position: relative;
    overflow: hidden;
}
.kpi-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: var(--accent, #3182ce);
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.4); }
.kpi-value { font-size: 2rem; font-weight: 800; color: var(--accent, #3182ce); }
.kpi-label { font-size: 0.75rem; color: #a0aec0; text-transform: uppercase; letter-spacing: .05em; margin-top: .3rem; }
.kpi-delta { font-size: 0.8rem; margin-top: .4rem; }
.kpi-delta.up   { color: #48bb78; }
.kpi-delta.down { color: #fc8181; }

/* ── Section titles ── */
.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #e2e8f0;
    border-left: 3px solid #3182ce;
    padding-left: .75rem;
    margin: 1.5rem 0 1rem;
}

/* ── Alert badges ── */
.badge {
    display: inline-block;
    padding: .2rem .6rem;
    border-radius: 999px;
    font-size: .72rem;
    font-weight: 600;
}
.badge-red    { background: #742a2a; color: #fc8181; }
.badge-yellow { background: #744210; color: #f6e05e; }
.badge-green  { background: #1c4532; color: #68d391; }
.badge-blue   { background: #1a365d; color: #90cdf4; }

/* ── Progress bar ── */
.progress-wrap { background: #2d3748; border-radius: 999px; height: 8px; overflow: hidden; }
.progress-bar  { height: 100%; border-radius: 999px; transition: width .4s; }

/* ── Table ── */
.styled-table { width: 100%; border-collapse: collapse; font-size: .85rem; }
.styled-table th {
    background: #2d3748;
    color: #a0aec0;
    padding: .6rem 1rem;
    text-align: left;
    font-weight: 600;
    text-transform: uppercase;
    font-size: .72rem;
    letter-spacing: .05em;
}
.styled-table td { padding: .6rem 1rem; border-bottom: 1px solid #2d3748; color: #e2e8f0; }
.styled-table tr:hover td { background: #1a202c; }

/* ── Form ── */
.form-card {
    background: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}

/* ── Sidebar nav ── */
.nav-item {
    display: flex;
    align-items: center;
    gap: .6rem;
    padding: .6rem .8rem;
    border-radius: 8px;
    cursor: pointer;
    transition: background .15s;
    color: #a0aec0;
    font-size: .9rem;
}
.nav-item:hover, .nav-item.active { background: #2d3748; color: #fff; }

/* ── Streamlit overrides ── */
div[data-testid="metric-container"] {
    background: #1a202c;
    border: 1px solid #2d3748;
    border-radius: 12px;
    padding: 1rem;
}
.stSelectbox label, .stTextInput label, .stNumberInput label { color: #a0aec0 !important; }
.stButton > button {
    background: linear-gradient(135deg, #2b6cb0, #3182ce);
    color: white;
    border: none;
    border-radius: 8px;
    font-weight: 600;
    transition: opacity .2s;
}
.stButton > button:hover { opacity: .85; }
</style>
"""

REGION_COLORS = {
    'MARITIME': '#f6ad55',
    'PLATEAUX': '#9f7aea',
    'CENTRALE': '#fc8181',
    'KARA':     '#63b3ed',
    'SAVANES':  '#68d391',
}

REGION_LABELS = {
    'MARITIME': 'Maritime',
    'PLATEAUX': 'Plateaux',
    'CENTRALE': 'Centrale',
    'KARA':     'Kara',
    'SAVANES':  'Savanes',
}

STATUS_COLORS = {
    'PLANIFIE':  '#63b3ed',
    'EN_COURS':  '#f6ad55',
    'TERMINE':   '#68d391',
    'SUSPENDU':  '#fc8181',
    'ANNULE':    '#a0aec0',
}
