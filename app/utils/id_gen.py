import uuid

def gen_id(prefix: str = "") -> str:
    return f"{prefix}{uuid.uuid4()}" if prefix else str(uuid.uuid4())
