# ネットワーク機器ログ解析ツール（Python CLI ツール）

## 概要

このツールは、ネットワーク機器のテストログを解析し、エラー検出、統計集計、可視化を行うPython製CLIツールです。  
指定されたログファイルを読み取り、エラー・警告などのイベントを抽出し、表やグラフ形式で結果を出力します。

## 特徴

- ログファイルからERROR / WARNING / INFOイベントを抽出
- イベントの件数統計
- エラー内容の一覧表示
- 頻出エラータイプの分析
- コンソール出力（整形済みテーブル）
- CSV / JSONへのエクスポート（オプション）
- イベント発生頻度のグラフ表示（オプション）

## 使用技術

- Python 3
- argparse
- re（正規表現）
- collections
- tabulate
- matplotlib（グラフ）

## 使用方法

### 1. 環境のセットアップ

```bash
git clone https://github.com/KNLighty/netdevice-log-analyzer.git
cd netdevice-log-analyzer
python -m venv venv
source venv/bin/activate  # Windowsの場合は venv\Scripts\activate
pip install -r requirements.txt
```

### 2. ツールの実行

```bash
python analyzer.py --file logs/sample.log
```

#### 主なオプション

- `--file`: ログファイルのパスを指定
- `--level`: INFO / WARNING / ERROR によるフィルタリング
- `--time`: 時間によるフィルタ

### 3. 出力例

#### ログファイル（例）

```
[2025-05-17 09:16:45] ERROR: Device connection failed. IP: 192.168.1.10, Reason: Timeout
```

#### 出力結果（テーブル）

| 時刻               | 種別   | メッセージ                   | 詳細                       |
|--------------------|--------|------------------------------|----------------------------|
| 2025-05-17 09:16:45 | ERROR  | Device connection failed     | IP: 192.168.1.10, Reason: Timeout |

#### 統計出力

```
INFO: 4件
WARNING: 2件
ERROR: 3件
```

## 想定ユースケース

- テスト結果のレポート作成補助
- エラーの自動検出と分類

## ディレクトリ構成

```
netdevice-log-analyzer/
├── analyzer.py           ← CLIの起点
├── parser.py             ← ログ解析ロジック
├── requirements.txt      ← 依存ライブラリ
├── logs/                 ← テスト用ログ格納ディレクトリ
├── output/               ← 結果出力（csv/jsonなど）
├── README.md             ← 本ファイル
```

## 作者

Kirill Zhirikhin
