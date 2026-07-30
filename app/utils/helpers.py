import uuid
import math
import pandas as pd

def gen_id(prefix=""):
    return f"{prefix}{uuid.uuid4()}" if prefix else str(uuid.uuid4())

def haversine(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def style_keys(df, pk_cols, fk_cols):
    if df.empty:
        return df
    rename = {}
    for col in df.columns:
        if col in pk_cols:
            rename[col] = f"🔑 {col}"
        elif col in fk_cols:
            rename[col] = f"🔗 {col}"
    return df.rename(columns=rename)

def get_key_info(table, conn):
    c = conn.cursor()
    pk_cols = set()
    for row in c.execute(f'PRAGMA table_info("{table}")'):
        if row[5] > 0:
            pk_cols.add(row[1])
    fk_cols = {}
    for row in c.execute(f'PRAGMA foreign_key_list("{table}")'):
        fk_cols[row[3]] = row[2]
    return pk_cols, fk_cols
