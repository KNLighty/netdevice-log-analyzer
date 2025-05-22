import re

log_pattern = re.compile(
    r"\[(?P<datetime>.*?)\]\s+(?P<level>INFO|WARNING|ERROR):\s+(?P<message>.*)"
)

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
def read_lines(file):
    logs = []  # ← ここに辞書を追加していく
    for line in file:
        line = line.strip()
        if line:
            parsed = parse_log_line(line)
            if parsed:
                logs.append(parsed)
    return logs  # 最終的に list[dict] を返す


# 1行のログを正規表現で解析し、辞書形式で返す関数（マッチしない場合はNone）
def parse_log_line(line):
    match = log_pattern.match(line)
    if match:
        return match.groupdict()
    else:
        print(f"[スキップ] 正規表現に一致しません: {line}")
        return None
