import streamlit as st
import pandas as pd
from app.database.connection import get_conn
from app.utils.id_gen import gen_id
from app.utils.validators import validate_hs_code, validate_incoterm

def show():
    st.title("Comercio y Logística")
    st.markdown("Órdenes de comercio, códigos HS, incoterms y medidas.")
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
        with st.form("form_comercio"):
            email_sel = st.selectbox("Selecciona usuario", options=list(user_options.keys()), index=default_idx)
            product = st.text_input("Nombre del producto")
            hs_code = st.text_input("Código HS (Sistema Armonizado)", help="HS Code: 4-10 dígitos de la nomenclatura aduanera armonizada (ej: 847130).")
            incoterm = st.text_input("Código Incoterm (ej: FOB, CIF, EXW)", help="Incoterms 2020: EXW, FCA, FAS, FOB, CFR, CIF, CPT, CIP, DPU, DAP, DDP.")
            qty = st.number_input("Cantidad", step=0.01, format="%.2f", help="Cantidad declarada de la orden.")
            unit = st.text_input("Unidad de medida (UN/CEFACT, ej: KGM, EA)", help="UN/CEFACT: código de unidad de medida internacional (KGM, EA, LTR, MTK...).")
            material = st.text_input("Especificación del material", help="Especificación técnica o composición del producto.")
            submit_c = st.form_submit_button("Registrar Orden")
        if submit_c:
            errors = []
            if hs_code and not validate_hs_code(hs_code):
                errors.append("Código HS inválido (4-10 dígitos numéricos)")
            if incoterm and not validate_incoterm(incoterm):
                errors.append("Código Incoterm inválido (usar: EXW, FCA, FAS, FOB, CFR, CIF, CPT, CIP, DPU, DAP, DDP)")
            if errors:
                for e in errors:
                    st.error(e)
            else:
                with st.spinner("Registrando orden de comercio..."):
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
