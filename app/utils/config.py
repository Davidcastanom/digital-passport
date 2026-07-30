import os

_env_loaded = False
def _ensure_env():
    global _env_loaded
    if _env_loaded:
        return
    _env_loaded = True
    try:
        dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), ".env")
        if os.path.exists(dotenv_path):
            with open(dotenv_path, encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if not line or line.startswith("#") or "=" not in line:
                        continue
                    k, _, v = line.partition("=")
                    k, v = k.strip(), v.strip().strip("\"'")
                    if k and not os.getenv(k):
                        os.environ[k] = v
    except Exception:
        pass

def get_api_key():
    _ensure_env()
    key = os.getenv("MAPS_API_KEY", "")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("MAPS_API_KEY", "")
        except Exception:
            pass
    return key

def get_db_path():
    _ensure_env()
    env_path = os.getenv("DB_PATH", "")
    if env_path:
        return env_path
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    candidates = [
        os.path.join(base, "Esquema Relacional Global_David.db"),
        os.path.join(base, "data", "pasaporte_digital.db"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]
