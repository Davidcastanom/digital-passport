import re

def validate_email(email):
    return bool(re.match(r'^[^@\s]+@[^@\s]+\.[^@\s]+$', email.strip())) if email else False

def validate_e164(phone):
    return bool(re.match(r'^\+[1-9]\d{6,14}$', phone.strip())) if phone else True

def validate_ipv4(ip):
    if not ip:
        return True
    parts = ip.strip().split(".")
    if len(parts) != 4:
        return False
    for p in parts:
        try:
            n = int(p)
            if n < 0 or n > 255:
                return False
        except ValueError:
            return False
    return True

def validate_mac(mac):
    if not mac:
        return True
    return bool(re.match(r'^([0-9A-Fa-f]{2}[-:]){5}[0-9A-Fa-f]{2}$', mac.strip()))

def validate_iban(iban):
    if not iban:
        return True
    cleaned = iban.strip().upper().replace(" ", "")
    if not re.match(r'^[A-Z]{2}\d{2}[A-Z0-9]{1,30}$', cleaned):
        return False
    return True

def validate_isco08(code):
    if not code:
        return False
    return bool(re.match(r'^\d{4}$', str(code).strip()))

def validate_doi(doi):
    if not doi:
        return True
    return bool(re.match(r'^10\.\d{4,}/.+$', doi.strip()))

def validate_hs_code(code):
    if not code:
        return True
    return bool(re.match(r'^\d{4,10}$', code.strip()))

def validate_incoterm(code):
    if not code:
        return True
    return code.strip().upper() in {"EXW", "FCA", "FAS", "FOB", "CFR", "CIF", "CPT", "CIP", "DPU", "DAP", "DDP"}
