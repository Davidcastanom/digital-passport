import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.helpers import gen_id

def show():
    st.title("Datos Financieros y Legales")
    st.markdown("Registra información bancaria, fiscal y de actividad económica.")
    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()
    if users_df.empty:
        st.warning("No hay usuarios registrados. Primero registra un usuario.")
    else:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        with st.form("form_financiero"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()))
            iban = st.text_input("Código IBAN")
            swift = st.text_input("Código SWIFT/BIC")
            tax_id = st.text_input("NIT / Identificación fiscal")
            ciiu = st.number_input("Código CIIU", step=1, format="%d")
            submit_f = st.form_submit_button("Guardar")
        if submit_f:
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
