import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from parser import parse_log_line, load_config

patterns = load_config("config.yaml")

def test_parse_log_line_success():
    line = "[2025-05-17 09:16:45] ERROR: Connection failed. IP: 192.168.1.10"
    result = parse_log_line(line, patterns)
    assert result is not None
    assert result["level"] == "ERROR"
    assert "Connection failed" in result["message"]

def test_parse_log_line_invalid_format():
    line = "invalid log format without brackets"
    result = parse_log_line(line, patterns)
    assert result is None
