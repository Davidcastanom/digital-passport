import os
from dotenv import load_dotenv

load_dotenv()

def get_api_key():
    key = os.getenv("MAPS_API_KEY", "")
    if not key:
        try:
            import streamlit as st
            key = st.secrets.get("MAPS_API_KEY", "")
        except Exception:
            pass
    return key

def get_db_path():
    env_path = os.getenv("DB_PATH", "")
    if env_path:
        return env_path
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    candidates = [
        os.path.join(base, "Esquema Relacional Global_David.db"),
        os.path.join(base, "data", "telemetriamaps.db"),
    ]
    for p in candidates:
        if os.path.exists(p):
            return p
    return candidates[0]
