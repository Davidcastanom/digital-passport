import streamlit as st
import pandas as pd
from app.database.connection import get_conn, get_tables

def show():
    st.title("Telemetriamaps para Comercio Exterior")
    st.markdown("Sistema de registro unificado para importación y exportación con estándares internacionales.")
    conn = get_conn()
    c = conn.cursor()
    counts = {}
    for t in get_tables(conn):
        c.execute(f'SELECT COUNT(*) FROM "{t}"')
        counts[t] = c.fetchone()[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Usuarios", counts.get("user_identity", 0))
    with col2: st.metric("Geolocalización", counts.get("user_geolocation", 0))
    with col3: st.metric("Cultura/Idioma", counts.get("user_culture_language", 0))
    with col4: st.metric("Eventos", counts.get("user_time_events", 0))
    col5, col6, col7, col8 = st.columns(4)
    with col5: st.metric("Financiero", counts.get("user_financials", 0))
    with col6: st.metric("Actividad Legal", counts.get("legal_economic_activity", 0))
    with col7: st.metric("Comercio", counts.get("trade_supply_chain", 0))
    with col8: st.metric("Red", counts.get("network_infrastructure", 0))

    st.subheader("Vista rápida")
    try:
        df = pd.read_sql("SELECT * FROM view_pasaporte_digital_usuario", conn)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.info("No hay registros en el pasaporte digital aún.")
    conn.close()
