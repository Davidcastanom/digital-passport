import sys
import os
import time
import importlib
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _safe_import(module, attempts=8, delay=0.25):
    last = None
    for attempt in range(attempts):
        try:
            return importlib.import_module(module)
        except KeyError as exc:
            last = exc
            time.sleep(delay * (attempt + 1))
    raise RuntimeError(f"Import race persistente en {module}") from last


def _nav_change(idx):
    selected = st.session_state.get(f"nav_{idx}")
    if selected and selected != st.session_state.get("page"):
        st.session_state.page = selected


if __name__ == "__main__":
    st = _safe_import("streamlit")
    pd = _safe_import("pandas")
    get_api_key = _safe_import("app.utils.config").get_api_key
    _conn = _safe_import("app.database.connection")
    get_conn, get_tables = _conn.get_conn, _conn.get_tables

    st.set_page_config(page_title="Pasaporte Digital - Comercio Exterior", layout="wide")

    st.markdown("""
    <style>
        .main .block-container { padding-top: 1.5rem; }
        section[data-testid="stSidebar"] { background: #0c1029 !important; }
        section[data-testid="stSidebar"] .stSelectbox label,
        section[data-testid="stSidebar"] .stRadio label { color: #94a3b8 !important; font-size: 13px; }
        section[data-testid="stSidebar"] .st-bb { color: white !important; }
        .st-bb { background: #0f172a !important; }
        div[data-testid="stMetric"] { background: #0f172a; border: 1px solid rgba(255,255,255,0.06); border-radius: 12px; padding: 12px; }
        div[data-testid="stMetric"] label { color: #00d4ff !important; }
        div.stTextInput input, div.stSelectbox div[data-baseweb="select"] { background: #0f172a !important; color: white !important; border-color: rgba(255,255,255,0.12) !important; }
        div.stTextInput label, div.stSelectbox label { color: #94a3b8 !important; }
        .stButton button { border-radius: 60px !important; font-weight: 600 !important; letter-spacing: 1px; }
        h1, h2, h3 { color: white !important; }
        .stMarkdown, .stText, p, li { color: #cbd5e1 !important; }
        .st-emotion-cache-1kyxreq { color: #cbd5e1 !important; }
        .stAlert { background: #0f172a !important; border: 1px solid rgba(255,255,255,0.08) !important; color: #cbd5e1 !important; }
        .st-b7 { border-color: rgba(255,255,255,0.08) !important; }
        footer { display: none !important; }
        #MainMenu { display: none !important; }
        .stDeployButton { display: none !important; }
    </style>
    """, unsafe_allow_html=True)

    if "db_path" not in st.session_state:
        st.session_state.db_path = ""
    if "landing" not in st.session_state:
        st.session_state.landing = True
    if "active_user_id" not in st.session_state:
        st.session_state.active_user_id = None
    if "active_user_email" not in st.session_state:
        st.session_state.active_user_email = None
    if "page" not in st.session_state:
        st.session_state.page = "Dashboard"

    IMG_LOGO = "https://res.cloudinary.com/dfn5g9ve3/image/upload/v1785366976/logo_2_ne0zk5.png"

    VIEWS = {
        "Dashboard": "app.views.dashboard",
        "Registrar Usuario": "app.views.register",
        "Datos Financieros y Legales": "app.views.finances",
        "Comercio y Logística": "app.views.trade",
        "Red y Dispositivo": "app.views.network",
        "Perfil Profesional y Ciencia": "app.views.science",
        "Arquitectura de Datos": "app.views.architecture",
        "Ver Registros": "app.views.records",
        "Perfil de Conexión": "app.views.connection_profile",
        "Telemetría y Mapas": "app.views.telemetry",
        "Auditoría de Eventos": "app.views.audit",
    }

    NAV_GROUPS = {
        "📋 Gestión": ["Dashboard", "Registrar Usuario"],
        "💼 Datos del Perfil": [
            "Datos Financieros y Legales", "Comercio y Logística",
            "Red y Dispositivo", "Perfil Profesional y Ciencia",
        ],
        "🔍 Exploración": [
            "Arquitectura de Datos", "Ver Registros", "Perfil de Conexión",
            "Telemetría y Mapas", "Auditoría de Eventos",
        ],
    }

    if st.session_state.get("landing", True):
        show_landing = _safe_import("app.views.landing").show
        show_landing()
        st.stop()

    st.sidebar.image(IMG_LOGO, width=180)
    st.sidebar.markdown("---")

    if st.session_state.pop("nav_to_register", False):
        st.session_state.page = "Registrar Usuario"

    for idx, (group, pages) in enumerate(NAV_GROUPS.items()):
        default_index = pages.index(st.session_state.page) if st.session_state.page in pages else 0
        st.sidebar.selectbox(
            group, pages, index=default_index, key=f"nav_{idx}", on_change=_nav_change, args=(idx,)
        )

    page = st.session_state.page

    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity ORDER BY email", conn)
    conn.close()

    st.sidebar.markdown("---")
    if not users_df.empty:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        current_email = st.session_state.active_user_email
        if current_email not in user_options:
            current_email = list(user_options.keys())[0]
        sel_email = st.sidebar.selectbox(
            "👤 Usuario activo", options=list(user_options.keys()),
            index=list(user_options.keys()).index(current_email),
            key="global_user_selector"
        )
        st.session_state.active_user_id = user_options[sel_email]
        st.session_state.active_user_email = sel_email
    else:
        st.sidebar.warning("Sin usuarios")
        st.session_state.active_user_id = None
        st.session_state.active_user_email = None

    module_path = VIEWS[page]
    module = _safe_import(module_path)
    module.show()

    st.sidebar.markdown("---")
    st.sidebar.markdown("**BD:** SQLite · Pasaporte Digital v1.0")
