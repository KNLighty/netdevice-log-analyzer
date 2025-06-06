import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from analyzer import filter_by_level
from analyzer import filter_by_since

sample_logs = [
    {"datetime": "2025-05-17 09:15:00", "level": "INFO", "message": "OK"},
    {"datetime": "2025-05-17 09:16:00", "level": "ERROR", "message": "Failed"},
    {"datetime": "2025-05-17 09:17:00", "level": "WARNING", "message": "Hot"},
]

def test_filter_by_level_error():
    result = filter_by_level(sample_logs, "ERROR")
    assert len(result) == 1
    assert result[0]["level"] == "ERROR"

def test_filter_by_level_none():
    result = filter_by_level(sample_logs, None)
    assert len(result) == 3 

def test_filter_by_since():
    result = filter_by_since(sample_logs, "2025-05-17 09:16:00")
    assert len(result) == 2
    assert all(log["datetime"] >= "2025-05-17 09:16:00" for log in result)
