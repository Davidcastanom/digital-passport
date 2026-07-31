from app.database.connection import get_conn, get_tables, validate_table_name, VIEWS_LIST
from app.database.schema import get_key_info


class TestConnection:
    def test_tables_present(self, db_conn):
        tables = get_tables(db_conn)
        assert "user_identity" in tables
        assert "telemetry_log" in tables
        assert len(tables) >= 11

    def test_validate_every_table_allowed(self, db_conn):
        for table in get_tables(db_conn):
            assert validate_table_name(table, db_conn) == table

    def test_validate_every_view_allowed(self, db_conn):
        for view in VIEWS_LIST:
            assert validate_table_name(view, db_conn) == view

    def test_validate_returns_original_string(self, db_conn):
        assert validate_table_name("user_identity", db_conn) == "user_identity"

    def test_validate_invalid_raises(self, db_conn):
        try:
            validate_table_name("DROP TABLE users", db_conn)
            assert False, "debería lanzar ValueError"
        except ValueError:
            pass

    def test_validate_empty_raises(self, db_conn):
        try:
            validate_table_name("", db_conn)
            assert False, "debería lanzar ValueError"
        except ValueError:
            pass


class TestKeyInfo:
    def test_user_identity_pk(self, db_conn):
        pk, fk = get_key_info("user_identity", db_conn)
        assert "user_id" in pk

    def test_trade_fk(self, db_conn):
        pk, fk = get_key_info("trade_supply_chain", db_conn)
        assert fk.get("user_id") == "user_identity"

    def test_user_tables_fk_to_identity(self, db_conn):
        for table in get_tables(db_conn):
            pk, fk = get_key_info(table, db_conn)
            if table == "user_identity":
                continue
            if table == "industry_measurements":
                assert fk.get("order_item_id") == "trade_supply_chain"
                continue
            assert fk.get("user_id") == "user_identity", f"{table} debe FK a user_identity"

    def test_every_table_has_primary_key(self, db_conn):
        for table in get_tables(db_conn):
            pk, _ = get_key_info(table, db_conn)
            assert len(pk) > 0, f"{table} debe tener PK"

    def test_views_match_whitelist(self, db_conn):
        c = db_conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='view' ORDER BY name")
        real_views = {row[0] for row in c.fetchall()}
        assert set(VIEWS_LIST) == real_views
