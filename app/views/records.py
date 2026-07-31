import streamlit as st
import pandas as pd
from app.database.connection import get_conn, get_tables, validate_table_name, VIEWS_LIST
from app.database.schema import get_key_info
from app.utils.ui import style_keys

def show():
    st.title("Explorar Base de Datos")
    conn = get_conn()
    tables = get_tables(conn)
    conn.close()
    sel_table = st.selectbox("Selecciona una tabla", tables + VIEWS_LIST)
    if sel_table:
        conn = get_conn()
        validate_table_name(sel_table, conn)
        df = pd.read_sql(f'SELECT * FROM "{sel_table}"', conn)
        conn.close()
        pk_cols, fk_cols = get_key_info(sel_table, get_conn())
        st.markdown("**Leyenda:** <span style='background:#1a3a5c;color:#00d4ff;padding:2px 8px;border-radius:4px;font-weight:bold;'>🔑 PK</span> <span style='background:#2d1b4e;color:#a855f7;padding:2px 8px;border-radius:4px;font-weight:bold;'>🔗 FK</span>", unsafe_allow_html=True)
        styled = style_keys(df, pk_cols, fk_cols)
        st.dataframe(styled, use_container_width=True)
        if not df.empty:
            c1, c2 = st.columns(2)
            with c1:
                st.download_button("📄 Descargar CSV", df.to_csv(index=False).encode("utf-8"), f"{sel_table}.csv", "text/csv", use_container_width=True)
            with c2:
                st.download_button("📦 Descargar JSON", df.to_json(orient="records").encode("utf-8"), f"{sel_table}.json", "application/json", use_container_width=True)
