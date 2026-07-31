import streamlit as st
import pandas as pd
from app.database.connection import get_conn, validate_table_name

def show():
    st.title("Arquitectura de la Base de Datos")
    st.markdown("Diagrama entidad-relación y estructura completa.")

    conn = get_conn()
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    tables = [r[0] for r in c.fetchall()]
    c.execute("SELECT name, sql FROM sqlite_master WHERE type='view' ORDER BY name")
    views_ddl = c.fetchall()

    erd_parts = ["erDiagram"]
    table_columns = {}
    fk_relations = []

    for tname in tables:
        validate_table_name(tname, conn)
        cols = []
        for row in c.execute(f'PRAGMA table_info("{tname}")'):
            cname = row[1]
            ctype = row[2].split("(")[0].upper() if row[2] else "TEXT"
            nullable = "NOT NULL" if row[3] else "NULL"
            pk = "PK" if row[5] > 0 else ""
            cols.append({"name": cname, "type": ctype, "nullable": nullable, "pk": pk})
        for row in c.execute(f'PRAGMA foreign_key_list("{tname}")'):
            fk_relations.append((tname, row[2], row[3]))
        table_columns[tname] = cols
        props = "\n".join([f'        {c["type"]} "{c["name"]}" {c["nullable"]}' for c in cols])
        erd_parts.append(f'    {tname} {{\n{props}\n    }}')

    for child, parent, col in fk_relations:
        erd_parts.append(f'    {parent} ||--o{{ {child} : "tiene"')

    erd_code = "\n".join(erd_parts)

    with st.expander("Diagrama Entidad-Relación (ERD)", expanded=True):
        st.markdown(f'```mermaid\n{erd_code}\n```')
        st.caption("Cada tabla satélite se relaciona con user_identity como tabla padre.")

    fk_by_table = {}
    for src, dst, col in fk_relations:
        fk_by_table.setdefault(src, set()).add(col)

    for tname in tables:
        with st.expander(f"📋 {tname}"):
            cols = table_columns[tname]
            for col in cols:
                if col["name"] in fk_by_table.get(tname, set()):
                    col["fk"] = "🔗 FK"
                else:
                    col["fk"] = ""
                if col["pk"]:
                    col["pk"] = "🔑 PK"
            st.dataframe(pd.DataFrame(cols), use_container_width=True)

    st.subheader("Vistas del Sistema")
    for vname, ddl in views_ddl:
        with st.expander(f"👁️ {vname}"):
            try:
                validate_table_name(vname, conn)
                df_v = pd.read_sql(f'SELECT * FROM "{vname}" LIMIT 5', conn)
                st.dataframe(df_v, use_container_width=True)
            except Exception:
                st.info("Vista sin datos aún.")
            st.code(ddl, language="sql")

    st.subheader("Relaciones entre tablas")
    rel_data = []
    for src, dst, col in fk_relations:
        rel_data.append({"Tabla origen": src, "Columna FK": col, "Tabla destino": dst})
    if rel_data:
        st.dataframe(pd.DataFrame(rel_data), use_container_width=True)

    conn.close()