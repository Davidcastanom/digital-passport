from app.database.seed import generate_beacons, CITIES


class TestGenerateBeacons:
    def test_inserts_requested_count(self, db_conn):
        c = db_conn.cursor()
        before = c.execute("SELECT COUNT(*) FROM telemetry_log").fetchone()[0]
        generate_beacons(db_conn, "test-user-1", num_beacons=30)
        after = c.execute("SELECT COUNT(*) FROM telemetry_log").fetchone()[0]
        assert after - before == 30

    def test_beacon_shape(self, db_conn):
        beacons = generate_beacons(db_conn, "test-user-2", num_beacons=5, start=CITIES[0])
        assert len(beacons) == 5
        for b in beacons:
            assert set(b.keys()) == {"lat", "lng", "spd", "ts"}
            assert -90 <= b["lat"] <= 90
            assert -180 <= b["lng"] <= 180

    def test_stored_rows_match(self, db_conn):
        generate_beacons(db_conn, "test-user-3", num_beacons=10)
        rows = db_conn.execute(
            "SELECT * FROM telemetry_log WHERE user_id = ?", ("test-user-3",)
        ).fetchall()
        assert len(rows) == 10
        for row in rows:
            assert row["event_type"] == "gps_fix"
            assert row["latitude"] is not None
            assert row["longitude"] is not None

    def test_start_param_used(self, db_conn):
        beacons = generate_beacons(db_conn, "test-user-4", num_beacons=1, start=(4.7110, -74.0721))
        assert abs(beacons[0]["lat"] - 4.7110) < 0.01
