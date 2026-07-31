import streamlit as st
import pandas as pd
from app.database.connection import get_conn, get_tables, validate_table_name

def show():
    st.title("Pasaporte Digital para Comercio Exterior")
    st.markdown("Sistema de registro unificado para importación y exportación con estándares internacionales.")
    conn = get_conn()
    c = conn.cursor()

    known_tables = get_tables(conn)
    counts = {}
    for t in known_tables:
        validate_table_name(t, conn)
        c.execute(f'SELECT COUNT(*) FROM "{t}"')
        counts[t] = c.fetchone()[0]

    c.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='view'")
    num_views = c.fetchone()[0]

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

    col9, col10, col11, col12 = st.columns(4)
    with col9: st.metric("Balizas GPS", counts.get("telemetry_log", 0))
    with col10: st.metric("Perfil Científico", counts.get("health_science_sectorial", 0))
    with col11: st.metric("Medidas Industriales", counts.get("industry_measurements", 0))
    with col12: st.metric("Vistas del Sistema", num_views)

    st.subheader("Progreso del Pasaporte")
    if st.session_state.active_user_id:
        uid = st.session_state.active_user_id
        satellite = {
            "Identidad": "user_identity",
            "Geolocalización": "user_geolocation",
            "Idioma/Cultura": "user_culture_language",
            "Financiero": "user_financials",
            "Actividad Legal": "legal_economic_activity",
            "Comercio": "trade_supply_chain",
            "Red": "network_infrastructure",
            "Ciencia": "health_science_sectorial",
        }
        done = 0
        for label, table in satellite.items():
            c.execute(f'SELECT COUNT(*) FROM "{table}" WHERE user_id = ?', (uid,))
            if c.fetchone()[0] > 0:
                done += 1
        pct = int(done / len(satellite) * 100)
        st.progress(pct / 100, text=f"Pasaporte completado al {pct}% ({done}/{len(satellite)} secciones)")
        missing = [label for label, table in satellite.items()
                   if c.execute(f'SELECT COUNT(*) FROM "{table}" WHERE user_id = ?', (uid,)).fetchone()[0] == 0]
        if missing:
            st.info("Faltan: " + ", ".join(missing))
        else:
            st.success("Pasaporte completo. ¡Listo para integración externa!")
    else:
        st.info("Selecciona un usuario en la barra lateral para ver su progreso.")

    st.subheader("Vista rápida")
    try:
        df = pd.read_sql("SELECT * FROM view_pasaporte_digital_usuario", conn)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.info("No hay registros en el pasaporte digital aún.")
    conn.close()
