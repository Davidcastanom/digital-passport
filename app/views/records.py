import streamlit as st
import pandas as pd
from app.database.connection import get_conn, get_tables
from app.utils.helpers import get_key_info, style_keys

VIEWS_LIST = [
    "view_pasaporte_digital_usuario", "view_auditoria_seguridad",
    "view_compliance_fiscal_bancario", "view_logistica_comercio",
    "view_perfil_profesional_ciencia", "view_telemetria_rastreo_realtime"
]

def show():
    st.title("Explorar Base de Datos")
    conn = get_conn()
    tables = get_tables(conn)
    conn.close()
    sel_table = st.selectbox("Selecciona una tabla", tables + VIEWS_LIST)
    if sel_table:
        conn = get_conn()
        df = pd.read_sql(f'SELECT * FROM "{sel_table}"', conn)
        conn.close()
        pk_cols, fk_cols = get_key_info(sel_table, get_conn())
        st.markdown("**Leyenda:** <span style='background:#1a3a5c;color:#00d4ff;padding:2px 8px;border-radius:4px;font-weight:bold;'>🔑 PK</span> <span style='background:#2d1b4e;color:#a855f7;padding:2px 8px;border-radius:4px;font-weight:bold;'>🔗 FK</span>", unsafe_allow_html=True)
        styled = style_keys(df, pk_cols, fk_cols)
        st.dataframe(styled, use_container_width=True)
        if not df.empty:
            st.download_button("Descargar CSV", df.to_csv(index=False).encode("utf-8"), f"{sel_table}.csv", "text/csv")
