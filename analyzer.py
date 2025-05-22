import argparse
from datetime import datetime
from tabulate import tabulate
import csv
import json
import os
import matplotlib.pyplot as plt
from collections import Counter, defaultdict
from parser import open_log_file, read_lines

# ログレベルでフィルタリングする関数
def filter_by_level(logs, level):
    if not level:
        return logs  # フィルターが指定されていない場合、そのまま返す
    return [log for log in logs if log["level"] == level]

# 指定した時刻以降のログのみを返す関数
def filter_by_since(logs, since_str):
    if not since_str:
        return logs
    try:
        since_time = datetime.strptime(since_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        print("[エラー] 時刻のフォーマットは 'YYYY-MM-DD HH:MM:SS' で指定してください。")
        return logs

    filtered = []
    for log in logs:
        try:
            log_time = datetime.strptime(log["datetime"], "%Y-%m-%d %H:%M:%S")
            if log_time >= since_time:
                filtered.append(log)
        except ValueError:
            print(f"[スキップ] 日時形式エラー: {log['datetime']}")
    return filtered

# ログをCSVまたはJSONとして保存する関数
def export_logs(log_data, export_format, output_dir="output"):
    if not export_format:
        return

    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, f"filtered_log.{export_format}")

    if export_format == "csv":
        try:
            with open(output_path, "w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["datetime", "level", "message"])
                writer.writeheader()
                writer.writerows(log_data)
            print(f"[OK] CSVファイルに保存しました: {output_path}")
        except Exception as e:
            print(f"[エラー] CSVエクスポート失敗: {e}")

    elif export_format == "json":
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            print(f"[OK] JSONファイルに保存しました: {output_path}")
        except Exception as e:
            print(f"[エラー] JSONエクスポート失敗: {e}")


def plot_event_frequency(log_data):
    if not log_data:
        print("[INFO] ログが空のため、グラフは表示されません。")
        return

    # イベントを時間単位で集計（分単位）
    freq = defaultdict(lambda: {"INFO": 0, "WARNING": 0, "ERROR": 0})

    for log in log_data:
        try:
            timestamp = datetime.strptime(log["datetime"], "%Y-%m-%d %H:%M:%S")
            time_key = timestamp.strftime("%H:%M")  # 分単位で集約
            freq[time_key][log["level"]] += 1
        except Exception as e:
            print(f"[スキップ] 日付形式エラー: {log['datetime']}")

    times = sorted(freq.keys())
    info_vals = [freq[t]["INFO"] for t in times]
    warn_vals = [freq[t]["WARNING"] for t in times]
    error_vals = [freq[t]["ERROR"] for t in times]

    # グラフの描画
    plt.figure(figsize=(10, 5))
    plt.plot(times, info_vals, label="INFO")
    plt.plot(times, warn_vals, label="WARNING")
    plt.plot(times, error_vals, label="ERROR")
    plt.xlabel("Time (minute)")
    plt.ylabel("Frequency")
    plt.title("Log event frequency (by minutes)")
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.grid(True)
    plt.show()

def print_event_statistics(log_data):
    levels = [log["level"] for log in log_data]
    counter = Counter(levels)

    print("\n[統計] ログタイプ別の件数:")
    for level in ["INFO", "WARNING", "ERROR"]:
        print(f"{level}: {counter.get(level, 0)} 件")


def main():
    parser = argparse.ArgumentParser(description="ネットワーク機器ログ解析ツール")

    # ログファイルパス
    parser.add_argument("--file", "-f", required=True, help="ログファイルのパスを指定してください（.log / .txt）")

    # ログレベルフィルター（INFO, WARNING, ERROR）
    parser.add_argument("--level", "-l", choices=["INFO", "WARNING", "ERROR"], help="レベルでフィルターする（INFO, WARNING, ERROR）")

    # 時刻フィルター（YYYY-MM-DD HH:MM:SS）
    parser.add_argument("--since", "-s", help="指定した時刻以降のログのみ表示（例: '2025-05-17 09:00:00')")

    # ログをファイルにエクスポート
    parser.add_argument("--export", "-e", choices=["csv", "json"], help="ログをファイルにエクスポート（csv/json）")

    # グラフ
    parser.add_argument("--plot", action="store_true", help="イベント頻度をグラフで表示する")


    args = parser.parse_args()

    log_file = open_log_file(args.file)
    if not log_file:
        return
    
    log_data = read_lines(log_file)
    log_file.close()

    if not log_data:
        print("[警告] ログデータが存在しません。処理を終了します。")
        return

    # ここでフィルターを適用
    log_data = filter_by_level(log_data, args.level)
    log_data = filter_by_since(log_data, args.since)


    print(f"[INFO] {len(log_data)} 行を解析しました。")
    # statistics
    print_event_statistics(log_data)

    # ログを datetime でソート（昇順）
    try:
        log_data.sort(key=lambda log: datetime.strptime(log["datetime"], "%Y-%m-%d %H:%M:%S"))
    except Exception as e:
        print(f"[エラー] ソート中に問題が発生しました: {e}")

    # 表に出力するためのデータを整形
    table_data = []
    for log in log_data:
        table_data.append([
            log["datetime"],
            log["level"],
            log["message"]
    ])
    headers = ["日時", "レベル", "メッセージ"]

    print(tabulate(table_data, headers=headers, tablefmt="grid"))
    export_logs(log_data, args.export)
    if args.plot:
        plot_event_frequency(log_data)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[致命的エラー] 予期しない例外が発生しました: {e}")
