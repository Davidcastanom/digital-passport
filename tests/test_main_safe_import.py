import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.main import _safe_import


class TestSafeImport:
    def test_returns_module_on_success(self):
        m = _safe_import("app.utils.config")
        assert m.get_api_key is not None

    def test_returns_deepest_module(self):
        m = _safe_import("app.database.connection")
        assert m.get_conn is not None
        assert m.get_tables is not None

    def test_retries_on_transient_keyerror(self, monkeypatch):
        calls = {"n": 0}

        def fake_import(module, *args, **kwargs):
            calls["n"] += 1
            if calls["n"] < 3:
                raise KeyError("import race")
            return "module-loaded"

        monkeypatch.setattr("importlib.import_module", fake_import)
        result = _safe_import("app.utils.config", attempts=5, delay=0.01)
        assert result == "module-loaded"
        assert calls["n"] == 3

    def test_raises_after_exhausting_attempts(self, monkeypatch):
        def fake_import(module, *args, **kwargs):
            raise KeyError("always fails")

        monkeypatch.setattr("importlib.import_module", fake_import)
        try:
            _safe_import("app.utils.config", attempts=3, delay=0.01)
            assert False, "debería lanzar RuntimeError"
        except RuntimeError:
            pass

    def test_other_errors_not_swallowed(self, monkeypatch):
        def fake_import(module, *args, **kwargs):
            raise ModuleNotFoundError("real problem")

        monkeypatch.setattr("importlib.import_module", fake_import)
        try:
            _safe_import("app.utils.config", attempts=3, delay=0.01)
            assert False, "debería propagar ModuleNotFoundError"
        except ModuleNotFoundError:
            pass
