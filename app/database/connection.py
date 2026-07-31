import sqlite3
from contextlib import contextmanager
from app.utils.config import get_db_path

VIEWS_LIST = [
    "view_pasaporte_digital_usuario", "view_auditoria_seguridad",
    "view_compliance_fiscal_bancario", "view_logistica_comercio",
    "view_perfil_profesional_ciencia", "view_telemetria_rastreo_realtime"
]

def get_conn():
    db_path = get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

@contextmanager
def get_conn_cm():
    conn = get_conn()
    try:
        yield conn
    finally:
        conn.close()

def get_tables(conn):
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
    return [row[0] for row in c.fetchall()]

def validate_table_name(name, conn):
    known = set(get_tables(conn))
    known.update(VIEWS_LIST)
    if name not in known:
        raise ValueError(f"Nombre de tabla/vista no permitido: {name}")
    return name