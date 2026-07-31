import math

from app.utils.id_gen import gen_id
from app.utils.geo import haversine
from app.utils.ui import style_keys
from app.utils import helpers
import pandas as pd


class TestGenId:
    def test_plain_uuid(self):
        value = gen_id()
        assert isinstance(value, str)
        assert len(value) == 36

    def test_with_prefix(self):
        assert gen_id("bea-").startswith("bea-")

    def test_unique(self):
        assert gen_id() != gen_id()


class TestHaversine:
    def test_zero_distance(self):
        assert haversine(4.711, -74.0721, 4.711, -74.0721) == 0

    def test_known_distance_bogota_medellin(self):
        d = haversine(4.711, -74.0721, 6.2476, -75.5658)
        assert 230 < d < 270

    def test_symmetry(self):
        d1 = haversine(0, 0, 10, 10)
        d2 = haversine(10, 10, 0, 0)
        assert math.isclose(d1, d2, rel_tol=1e-9)


class TestStyleKeys:
    def test_renames_pk_and_fk(self):
        df = pd.DataFrame([{"user_id": "u1", "trade_id": "t1"}])
        out = style_keys(df, {"user_id"}, {"trade_id"})
        assert "🔑 user_id" in out.columns
        assert "🔗 trade_id" in out.columns

    def test_empty_df_unchanged(self):
        df = pd.DataFrame()
        out = style_keys(df, {"user_id"}, {})
        assert out.empty

    def test_plain_columns_unchanged(self):
        df = pd.DataFrame([{"nombre": "x"}])
        out = style_keys(df, set(), set())
        assert list(out.columns) == ["nombre"]


class TestHelpersShim:
    def test_reexports(self):
        assert helpers.gen_id is gen_id
        assert helpers.haversine is haversine
        assert helpers.style_keys is style_keys
        assert helpers.CITIES
        assert callable(helpers.generate_beacons)
        assert callable(helpers.get_key_info)
