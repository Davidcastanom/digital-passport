import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.helpers import gen_id

def show():
    st.title("Perfil Profesional y Ciencia")
    st.markdown("Registro de ocupación ISCO-08 y publicaciones DOI.")
    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()
    if users_df.empty:
        st.warning("No hay usuarios registrados.")
    else:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        with st.form("form_ciencia"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()))
            isco_code = st.number_input("Código ISCO-08 (ocupación OIT)", step=1, format="%d")
            isco_desc = st.text_input("Descripción de la ocupación")
            doi = st.text_input("DOI de publicación (opcional)")
            submit_s = st.form_submit_button("Registrar")
        if submit_s:
            uid = user_options[email_sel]; sec_id = gen_id("sec-")
            conn = get_conn(); c = conn.cursor()
            try:
                c.execute('INSERT INTO health_science_sectorial ("sec-001", user_id, doi_identifier, isco_08_occupation, isco_08_Description) VALUES (?, ?, ?, ?, ?)',
                          (sec_id, uid, doi if doi else None, isco_code if isco_code else None, isco_desc))
                conn.commit(); st.success("Perfil profesional registrado.")
            except Exception as e:
                conn.rollback(); st.error(f"Error: {e}")
            finally:
                conn.close()
