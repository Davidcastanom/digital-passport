import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.helpers import gen_id

def show():
    st.title("Red y Dispositivo")
    st.markdown("Registro de infraestructura de red del usuario.")
    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()
    if users_df.empty:
        st.warning("No hay usuarios registrados.")
    else:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        with st.form("form_red"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()))
            ip = st.text_input("Dirección IPv4")
            mac = st.text_input("Dirección MAC")
            submit_n = st.form_submit_button("Registrar")
        if submit_n:
            uid = user_options[email_sel]; net_id = gen_id("net-")
            conn = get_conn(); c = conn.cursor()
            try:
                c.execute("INSERT INTO network_infrastructure (net_log_id, user_id, ipv4_address, mac_address) VALUES (?, ?, ?, ?)",
                          (net_id, uid, ip if ip else None, mac if mac else None))
                conn.commit(); st.success("Registro de red guardado.")
            except Exception as e:
                conn.rollback(); st.error(f"Error: {e}")
            finally:
                conn.close()
