import random
from datetime import datetime, timedelta, timezone
from app.utils.id_gen import gen_id

CITIES: list[tuple[float, float]] = [
    (4.7110, -74.0721), (6.2476, -75.5658), (3.4516, -76.5320),
    (10.9685, -74.7813), (7.1193, -73.1227), (4.4378, -75.2005),
    (11.2404, -74.1990), (8.7474, -75.8814), (10.3997, -75.5144),
]

def generate_beacons(conn, user_id: str, num_beacons: int = 30, start: tuple | None = None) -> list:
    if start is None:
        start = random.choice(CITIES)
    lat, lon = start
    c = conn.cursor()
    now = datetime.now(timezone.utc)
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
