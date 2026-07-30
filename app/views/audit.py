import streamlit as st
import pandas as pd
from datetime import datetime, timezone
from app.database.connection import get_conn
from app.utils.helpers import gen_id

def show():
    st.title("Auditoría de Seguridad")
    st.markdown("Registro automático de eventos por usuario.")
    conn = get_conn()
    try:
        df = pd.read_sql("SELECT * FROM view_auditoria_seguridad ORDER BY fecha_hora_utc DESC", conn)
        st.dataframe(df, use_container_width=True)
    except Exception:
        st.info("No hay eventos registrados aún.")
    conn.close()
    if st.button("Generar evento de prueba"):
        conn = get_conn(); c = conn.cursor()
        c.execute("SELECT user_id, email FROM user_identity LIMIT 1")
        user = c.fetchone()
        if user:
            eid = gen_id("evt-")
            c.execute("INSERT INTO user_time_events (event_id, user_id, event_name, event_timestamp_utc) VALUES (?, ?, ?, ?)",
                      (eid, user[0], "Acceso_Manual_App", datetime.now(timezone.utc).isoformat()))
            conn.commit(); st.success(f"Evento registrado para {user[1]}")
        else:
            st.warning("No hay usuarios para generar eventos.")
        conn.close()
