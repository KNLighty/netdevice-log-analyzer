import re
import yaml

# YAMLから正規表現パターンを読み込む
def load_config(config_path="config.yaml"):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
            return data.get("patterns", {})
    except Exception as e:
        print(f"[エラー] config.yamlの読み込みに失敗しました: {e}")
        return {}

# 1行のログをパターンで解析
def parse_log_line(line, patterns):
    result = {}
    for key, pattern in patterns.items():
        match = re.search(pattern, line)
        if match:
            result[key] = match.group(key)

    # 互換性のため timestamp → datetime にリネーム
    if "timestamp" in result:
        result["datetime"] = result.pop("timestamp")

    if "datetime" in result and "level" in result:
        return result
    else:
        print(f"[スキップ] パターンに一致しません: {line}")
        return None

# ログファイルを開く関数
def open_log_file(file_path):
    try:
        file = open(file_path, "r", encoding="utf-8")
        print(f"[OK] ファイルを開きました: {file_path}")
        return file
    except FileNotFoundError:
        print(f"[エラー] ファイルが見つかりません: {file_path}")
        return None
    except Exception as e:
        print(f"[エラー] ファイルを開けませんでした: {e}")
        return None

# ログファイルを1行ずつ読み込む
def read_lines(file, patterns):
    logs = []
    for line in file:
        line = line.strip()
        if line:
            parsed = parse_log_line(line, patterns)
            if parsed:
                logs.append(parsed)
    return logs
