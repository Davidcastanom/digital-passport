import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.id_gen import gen_id
from app.utils.validators import validate_isco08, validate_doi

def show():
    st.title("Perfil Profesional y Ciencia")
    st.markdown("Registro de ocupación ISCO-08 y publicaciones DOI.")
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
        with st.form("form_ciencia"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()), index=default_idx)
            isco_code = st.number_input("Código ISCO-08 (ocupación OIT)", step=1, format="%d", help="ISCO-08: clasificación de ocupaciones de la OIT (ej: 1211 = Gerente de finanzas).")
            isco_desc = st.text_input("Descripción de la ocupación", help="Título/descripción de la ocupación registrada.")
            doi = st.text_input("DOI de publicación (opcional)", help="DOI: identificador de objeto digital (ej: 10.1234/articulo).")
            submit_s = st.form_submit_button("Registrar")
        if submit_s:
            errors = []
            if not validate_isco08(isco_code):
                errors.append("Código ISCO-08 inválido (debe ser 4 dígitos)")
            if doi and not validate_doi(doi):
                errors.append("Formato DOI inválido (ej: 10.1234/abcde)")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                with st.spinner("Registrando perfil profesional..."):
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
