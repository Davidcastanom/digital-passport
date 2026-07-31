import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.utils.validators import (
    validate_email, validate_e164, validate_ipv4, validate_mac,
    validate_iban, validate_isco08, validate_doi, validate_hs_code,
    validate_incoterm,
)


class TestEmail:
    def test_valid(self):
        assert validate_email("usuario@ejemplo.com") is True

    def test_invalid(self):
        assert validate_email("sin-arroba") is False
        assert validate_email("") is False


class TestE164:
    def test_valid(self):
        assert validate_e164("+573001234567") is True
        assert validate_e164("") is True

    def test_invalid(self):
        assert validate_e164("573001234567") is False
        assert validate_e164("+1") is False


class TestIPv4:
    def test_valid(self):
        assert validate_ipv4("192.168.1.1") is True
        assert validate_ipv4("") is True

    def test_invalid(self):
        assert validate_ipv4("999.999.1.1") is False
        assert validate_ipv4("192.168.1") is False
        assert validate_ipv4("a.b.c.d") is False


class TestMAC:
    def test_valid(self):
        assert validate_mac("00:1A:2B:3C:4D:5E") is True
        assert validate_mac("00-1A-2B-3C-4D-5E") is True

    def test_invalid(self):
        assert validate_mac("00:1A:2B") is False
        assert validate_mac("GG:1A:2B:3C:4D:5E") is False


class TestIBAN:
    def test_valid(self):
        assert validate_iban("ES7921000813610123456789") is True

    def test_invalid(self):
        assert validate_iban("NOIBAN") is False


class TestISCO08:
    def test_valid(self):
        assert validate_isco08("1211") is True

    def test_invalid(self):
        assert validate_isco08("121") is False
        assert validate_isco08("") is False


class TestDOI:
    def test_valid(self):
        assert validate_doi("10.1234/articulo") is True

    def test_invalid(self):
        assert validate_doi("12.34/articulo") is False


class TestHSCode:
    def test_valid(self):
        assert validate_hs_code("847130") is True

    def test_invalid(self):
        assert validate_hs_code("84713x") is False


class TestIncoterm:
    def test_valid(self):
        for code in ["EXW", "FCA", "FAS", "FOB", "CFR", "CIF", "CPT", "CIP", "DPU", "DAP", "DDP"]:
            assert validate_incoterm(code) is True

    def test_invalid(self):
        assert validate_incoterm("XYZ") is False
