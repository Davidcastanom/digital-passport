import uuid
import math
import random
import sqlite3
from datetime import datetime, timedelta

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

CITIES = [
    (4.7110, -74.0721), (6.2476, -75.5658), (3.4516, -76.5320),
    (10.9685, -74.7813), (7.1193, -73.1227), (4.4378, -75.2005),
    (11.2404, -74.1990), (8.7474, -75.8814), (10.3997, -75.5144),
]

def generate_beacons(conn, user_id, num_beacons=30, start=None):
    if start is None:
        start = random.choice(CITIES)
    lat, lon = start
    c = conn.cursor()
    now = datetime.utcnow()
    beacons = []
    for i in range(num_beacons):
        lat += random.uniform(-0.003, 0.003)
        lon += random.uniform(-0.003, 0.003)
        speed = random.uniform(10, 80)
        heading = random.uniform(0, 360)
        ts = (now + timedelta(seconds=i * 45)).isoformat()
        bid = gen_id("bea-")
        c.execute(
            "INSERT INTO telemetry_log (beacon_id, user_id, latitude, longitude, speed_kmh, heading_deg, event_type, recorded_at) VALUES (?, ?, ?, ?, ?, ?, 'gps_fix', ?)",
            (bid, user_id, lat, lon, speed, heading, ts),
        )
        beacons.append({"lat": lat, "lng": lon, "spd": speed, "ts": ts})
    conn.commit()
    return beacons
