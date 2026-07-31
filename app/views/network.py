import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.id_gen import gen_id
from app.utils.validators import validate_ipv4, validate_mac

def show():
    st.title("Red y Dispositivo")
    st.markdown("Registro de infraestructura de red del usuario.")
    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()
    if users_df.empty:
        st.warning("No hay usuarios registrados.")
        if st.button("→ Registrar primer usuario"):
            st.session_state.nav_to_register = True
            st.rerun()
    else:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        default_idx = list(user_options.keys()).index(st.session_state.active_user_email) if st.session_state.active_user_email in user_options else 0
        with st.form("form_red"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()), index=default_idx)
            ip = st.text_input("Dirección IPv4", help="IPv4: 4 octetos de 0-255 separados por puntos (ej: 192.168.1.10).")
            mac = st.text_input("Dirección MAC", help="MAC: 6 pares hexadecimales con separador : o - (ej: 00:1A:2B:3C:4D:5E).")
            submit_n = st.form_submit_button("Registrar")
        if submit_n:
            errors = []
            if ip and not validate_ipv4(ip):
                errors.append("Dirección IPv4 inválida")
            if mac and not validate_mac(mac):
                errors.append("Dirección MAC inválida (formato: XX:XX:XX:XX:XX:XX)")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                with st.spinner("Guardando registro de red..."):
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
