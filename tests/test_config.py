import os

from app.utils import config


class TestProjectRoot:
    def test_returns_project_root_when_not_frozen(self, monkeypatch):
        monkeypatch.setattr(config.sys, "frozen", False, raising=False)
        root = config._get_project_root()
        assert os.path.basename(root) == "sql_archivos"
        assert os.path.isdir(os.path.join(root, "app"))

    def test_returns_exe_dir_when_frozen(self, monkeypatch):
        monkeypatch.setattr(config.sys, "frozen", True, raising=False)
        monkeypatch.setattr(config.sys, "executable", r"C:\app\pasaporte.exe")
        assert config._get_project_root() == r"C:\app"


class TestDbPath:
    def test_env_var_wins(self, monkeypatch):
        monkeypatch.setenv("DB_PATH", r"C:\custom\db.sqlite")
        assert config.get_db_path() == r"C:\custom\db.sqlite"

    def test_resolves_existing_project_db(self, monkeypatch):
        monkeypatch.delenv("DB_PATH", raising=False)
        monkeypatch.setattr(config, "_env_loaded", True)
        path = config.get_db_path()
        assert os.path.exists(path)
        assert path.endswith(".db")

    def test_env_parser_skips_comments_and_blank(self, monkeypatch, tmp_path):
        env = tmp_path / ".env"
        env.write_text(
            "# comentario\n\nDB_PATH=/tmp/x.db\nMAPS_API_KEY=\"secret1\"\n"
            "BADLINE\nMAPS_API_KEY2='secret2'\n",
            encoding="utf-8",
        )
        config._env_loaded = False
        monkeypatch.setattr(config, "_get_project_root", lambda: str(tmp_path))
        monkeypatch.setenv("MAPS_API_KEY", "existing")
        config._ensure_env()
        assert os.environ["MAPS_API_KEY"] == "existing"
        assert os.environ.get("MAPS_API_KEY2") == "secret2"
        assert os.environ.get("DB_PATH") == "/tmp/x.db"
        monkeypatch.delenv("MAPS_API_KEY2", raising=False)


class TestApiKey:
    def test_from_env(self, monkeypatch):
        monkeypatch.setenv("MAPS_API_KEY", "env-key-123")
        assert config.get_api_key() == "env-key-123"

    def test_empty_when_missing(self, monkeypatch):
        monkeypatch.delenv("MAPS_API_KEY", raising=False)
        monkeypatch.setattr(config, "_env_loaded", True)
        assert config.get_api_key() == ""
