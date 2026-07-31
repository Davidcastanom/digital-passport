import json
import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.database.schema import get_key_info
from app.utils.ui import style_keys

def show():
    st.title("Perfil de Conexión")
    st.markdown("Todos los datos de un usuario en un solo lugar, listo para integrarse con sistemas externos.")
    st.markdown("**Leyenda:** <span style='background:#1a3a5c;color:#00d4ff;padding:2px 8px;border-radius:4px;font-weight:bold;'>🔑 PK</span> <span style='background:#2d1b4e;color:#a855f7;padding:2px 8px;border-radius:4px;font-weight:bold;'>🔗 FK</span>", unsafe_allow_html=True)

    if not st.session_state.active_user_id:
        st.warning("Selecciona un usuario en la barra lateral primero.")
        if st.button("→ Registrar primer usuario"):
            st.session_state.nav_to_register = True
            st.rerun()
        return

    uid = st.session_state.active_user_id
    selected = st.session_state.active_user_email
    conn = get_conn()

    def show_section(title, table, uid):
        st.subheader(title)
        df = pd.read_sql(f'SELECT * FROM {table} WHERE user_id = ?', conn, params=[uid])
        pk, fk = get_key_info(table, conn)
        st.dataframe(style_keys(df, pk, fk), use_container_width=True)
        return df

    df_id = show_section("Identidad", "user_identity", uid)
    col_a, col_b = st.columns(2)
    with col_a:
        show_section("Geolocalización", "user_geolocation", uid)
        show_section("Idioma y Cultura", "user_culture_language", uid)
        show_section("Red y Dispositivo", "network_infrastructure", uid)
    with col_b:
        show_section("Financiero", "user_financials", uid)
        show_section("Actividad Legal", "legal_economic_activity", uid)
        show_section("Perfil Profesional", "health_science_sectorial", uid)

    st.subheader("Órdenes de Comercio")
    df_ord = pd.read_sql("""
        SELECT tsc.*, im.quantity, im.un_cefact_unit, im.material_spec
        FROM trade_supply_chain tsc
        LEFT JOIN industry_measurements im ON tsc.order_item_id = im.order_item_id
        WHERE tsc.user_id = ?
    """, conn, params=[uid])
    st.dataframe(df_ord, use_container_width=True)

    st.subheader("Auditoría de Eventos")
    df_evt = pd.read_sql("SELECT * FROM user_time_events WHERE user_id = ? ORDER BY event_timestamp_utc DESC", conn, params=[uid])
    st.dataframe(df_evt, use_container_width=True)

    st.subheader("Resumen JSON para integración externa")
    profile = {
        "user_id": uid, "email": selected,
        "identidad": df_id.to_dict(orient="records")[0] if not df_id.empty else {},
        "ordenes_comercio": df_ord.to_dict(orient="records"),
        "eventos_auditoria": df_evt.to_dict(orient="records"),
    }
    st.json(profile)
    st.download_button(
        "📦 Descargar JSON del perfil",
        json.dumps(profile, ensure_ascii=False, indent=2).encode("utf-8"),
        f"perfil_{uid[:8]}.json", "application/json"
    )
    conn.close()