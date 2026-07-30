import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.helpers import gen_id

def show():
    st.title("Comercio y Logística")
    st.markdown("Órdenes de comercio, códigos HS, incoterms y medidas.")
    conn = get_conn()
    users_df = pd.read_sql("SELECT user_id, email FROM user_identity", conn)
    conn.close()
    if users_df.empty:
        st.warning("No hay usuarios registrados.")
    else:
        user_options = {row["email"]: row["user_id"] for _, row in users_df.iterrows()}
        with st.form("form_comercio"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()))
            product = st.text_input("Nombre del producto")
            hs_code = st.text_input("Código HS (Sistema Armonizado)")
            incoterm = st.text_input("Código Incoterm (ej: FOB, CIF, EXW)")
            qty = st.number_input("Cantidad", step=0.01, format="%.2f")
            unit = st.text_input("Unidad de medida (UN/CEFACT, ej: KGM, EA)")
            material = st.text_input("Especificación del material")
            submit_c = st.form_submit_button("Registrar Orden")
        if submit_c:
            uid = user_options[email_sel]
            order_id = gen_id("ord-"); measure_id = gen_id("mes-")
            conn = get_conn(); c = conn.cursor()
            try:
                c.execute("INSERT INTO trade_supply_chain (order_item_id, user_id, product_name, hs_code, incoterm_code) VALUES (?, ?, ?, ?, ?)",
                          (order_id, uid, product, hs_code, incoterm if incoterm else None))
                c.execute("INSERT INTO industry_measurements (measure_id, order_item_id, quantity, un_cefact_unit, material_spec) VALUES (?, ?, ?, ?, ?)",
                          (measure_id, order_id, qty, unit, material if material else None))
                conn.commit(); st.success("Orden de comercio registrada.")
            except Exception as e:
                conn.rollback(); st.error(f"Error: {e}")
            finally:
                conn.close()
