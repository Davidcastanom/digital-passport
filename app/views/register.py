import streamlit as st
from datetime import datetime, timezone
from app.database.connection import get_conn
from app.utils.helpers import gen_id

def show():
    st.title("Registro de Usuario")
    st.markdown("Datos básicos del pasaporte digital (identidad, ubicación, idioma).")
    with st.form("form_usuario"):
        email = st.text_input("Correo electrónico")
        phone = st.text_input("Teléfono (formato E.164, ej: +573001234567)")
        city = st.text_input("Ciudad")
        lat = st.number_input("Latitud", format="%.6f")
        lon = st.number_input("Longitud", format="%.6f")
        lang = st.text_input("Idioma (ISO 639-1, ej: es)", value="es")
        locale = st.text_input("Locale BCP47 (ej: es-CO)", value="es-CO")
        submitted = st.form_submit_button("Registrar Pasaporte")
    if submitted:
        if not email:
            st.error("El correo es obligatorio")
        else:
            uid = gen_id(); geo_id = gen_id("geo-"); culture_id = gen_id("cul-")
            conn = get_conn(); c = conn.cursor()
            try:
                c.execute("INSERT INTO user_identity (user_id, email, phone_e164, created_at) VALUES (?, ?, ?, ?)",
                          (uid, email, phone if phone else None, datetime.now(timezone.utc).isoformat()))
                c.execute("INSERT INTO user_geolocation (geo_id, user_id, city_name, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
                          (geo_id, uid, city if city else None, lat if lat else None, lon if lon else None))
                c.execute("INSERT INTO user_culture_language (culture_id, user_id, language_iso_639_1, bcp47_locale) VALUES (?, ?, ?, ?)",
                          (culture_id, uid, lang, locale))
                conn.commit()
                st.success(f"Pasaporte registrado. ID: {uid}")
                st.balloons()
            except Exception as e:
                conn.rollback(); st.error(f"Error: {e}")
            finally:
                conn.close()
