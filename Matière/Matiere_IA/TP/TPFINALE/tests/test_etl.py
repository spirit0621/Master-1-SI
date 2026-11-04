"""
Tests unitaires pour le pipeline ETL TECHCORP
"""
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))
from etl.clean_and_load import is_valid_ipv4, clean_hostname, normalize_priority, normalize_date

def test_ipv4_validation():
    assert is_valid_ipv4("192.168.56.10") is True
    assert is_valid_ipv4("192.168.56.20") is True
    assert is_valid_ipv4("192.168.56.999") is False # Rejet anomalie
    assert is_valid_ipv4("") is False
    assert is_valid_ipv4("invalid_ip") is False

def test_hostname_cleaning():
    assert clean_hostname("srv-db-01") == "SRV-DB-01"
    assert clean_hostname("SRV-DB-01 ") == "SRV-DB-01"
    assert clean_hostname(" srv-dns-01 ") == "SRV-DNS-01"

def test_priority_normalization():
    assert normalize_priority("CRITIQUE") == "CRITICAL"
    assert normalize_priority("critical") == "CRITICAL"
    assert normalize_priority("high") == "HIGH"
    assert normalize_priority("moyen") == "MEDIUM"
    assert normalize_priority("bas") == "LOW"

def test_date_normalization():
    iso_date = "2026-09-15T11:18:00"
    assert normalize_date(iso_date) == "2026-09-15 11:18:00"
    fr_date = "15/09/2026 12:00:00"
    assert normalize_date(fr_date) == "2026-09-15 12:00:00"
