import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from app.utils.config import get_api_key
from app.database.connection import get_conn, get_tables

st.set_page_config(page_title="Telemetriamaps - Comercio Exterior", layout="wide")

if "db_path" not in st.session_state:
    st.session_state.db_path = ""
if "landing" not in st.session_state:
    st.session_state.landing = True

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

if st.session_state.get("landing", True):
    from app.views.landing import show as show_landing
    show_landing()
    st.stop()

st.sidebar.image(IMG_LOGO, width=180)
st.sidebar.markdown("---")

page = st.sidebar.radio("Navegación", list(VIEWS.keys()))

module_path = VIEWS[page]
__import__(module_path)
module = sys.modules[module_path]
module.show()

st.sidebar.markdown("---")
st.sidebar.markdown("**BD:** SQLite · Telemetriamaps v1.0")
