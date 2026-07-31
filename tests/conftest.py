import sys
import os
import sqlite3
import shutil
import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture(scope="session")
def db_conn(tmp_path_factory):
    src = os.path.join(PROJECT_ROOT, "Esquema Relacional Global_David.db")
    dst = tmp_path_factory.mktemp("data") / "test.db"
    shutil.copy(src, dst)
    conn = sqlite3.connect(str(dst))
    conn.row_factory = sqlite3.Row
    yield conn
    conn.close()
