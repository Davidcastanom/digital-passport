import streamlit as st
from datetime import datetime, timezone
from app.database.connection import get_conn
from app.utils.id_gen import gen_id
from app.utils.validators import validate_email, validate_e164

def show():
    st.title("Registro de Usuario")
    st.markdown("Datos básicos del pasaporte digital (identidad, ubicación, idioma).")
    with st.form("form_usuario"):
        email = st.text_input("Correo electrónico", help="Identificador único del pasaporte digital.")
        phone = st.text_input("Teléfono (formato E.164, ej: +573001234567)", help="E.164: código de país + número nacional, sin espacios ni guiones.")
        city = st.text_input("Ciudad", help="Ciudad base del usuario (punto de origen para telemetría).")
        lat = st.number_input("Latitud (ciudad)", format="%.6f", help="Coordenada geográfica: de -90 a 90.")
        lon = st.number_input("Longitud (ciudad)", format="%.6f", help="Coordenada geográfica: de -180 a 180.")
        lang = st.text_input("Idioma (ISO 639-1, ej: es)", value="es", help="ISO 639-1: código de 2 letras del idioma principal.")
        locale = st.text_input("Locale BCP47 (ej: es-CO)", value="es-CO", help="BCP47: idioma y región, separados por guión.")
        submitted = st.form_submit_button("Registrar Pasaporte")
    if submitted:
        errors = []
        if not email:
            errors.append("El correo es obligatorio")
        elif not validate_email(email):
            errors.append("Formato de correo inválido")
        if phone and not validate_e164(phone):
            errors.append("Teléfono: formato E.164 inválido (ej: +573001234567)")
        if errors:
            for e in errors:
                st.error(e)
        else:
            with st.spinner("Registrando pasaporte..."):
                uid = gen_id(); geo_id = gen_id("geo-"); culture_id = gen_id("cul-")
                conn = get_conn(); c = conn.cursor()
                try:
                    c.execute("INSERT INTO user_identity (user_id, email, phone_e164, created_at) VALUES (?, ?, ?, ?)",
                              (uid, email, phone if phone else None, datetime.now(timezone.utc).isoformat()))
                    c.execute("INSERT INTO user_geolocation (geo_id, user_id, city_name, city_latitude, city_longitude) VALUES (?, ?, ?, ?, ?)",
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
