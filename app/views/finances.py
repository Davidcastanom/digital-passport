import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.id_gen import gen_id
from app.utils.validators import validate_iban

def show():
    st.title("Datos Financieros y Legales")
    st.markdown("Registra información bancaria, fiscal y de actividad económica.")
    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()
    if users_df.empty:
        st.warning("No hay usuarios registrados. Primero registra un usuario.")
        if st.button("→ Registrar primer usuario"):
            st.session_state.nav_to_register = True
            st.rerun()
    else:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        default_idx = list(user_options.keys()).index(st.session_state.active_user_email) if st.session_state.active_user_email in user_options else 0
        with st.form("form_financiero"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()), index=default_idx)
            iban = st.text_input("Código IBAN", help="IBAN: código bancario internacional de hasta 34 caracteres (ej: ES79 2100 0813 6101 2345 6789).")
            swift = st.text_input("SWIFT/BIC", help="SWIFT/BIC: código de 8-11 caracteres del banco (ej: BBVAESMM).")
            tax_id = st.text_input("NIT / Identificación fiscal", help="NIT en Colombia o identificación fiscal del país de residencia.")
            ciiu = st.number_input("Código CIIU", step=1, format="%d", help="CIIU: clasificación industrial internacional uniforme de la ONU.")
            submit_f = st.form_submit_button("Guardar")
        if submit_f:
            errors = []
            if iban and not validate_iban(iban):
                errors.append("Formato IBAN inválido")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                with st.spinner("Guardando datos financieros..."):
                    uid = user_options[email_sel]
                    fin_id = gen_id("fin-"); legal_id = gen_id("leg-")
                    conn = get_conn(); c = conn.cursor()
                    try:
                        c.execute("INSERT INTO user_financials (financial_id, user_id, iban_code, swift_bic_code) VALUES (?, ?, ?, ?)",
                                  (fin_id, uid, iban if iban else None, swift))
                        c.execute("INSERT INTO legal_economic_activity (legal_id, user_id, tax_id_number, ciiu_code) VALUES (?, ?, ?, ?)",
                                  (legal_id, uid, tax_id if tax_id else None, ciiu if ciiu else None))
                        conn.commit(); st.success("Datos financieros y legales registrados.")
                    except Exception as e:
                        conn.rollback(); st.error(f"Error: {e}")
                    finally:
                        conn.close()
