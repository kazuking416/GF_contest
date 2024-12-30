import os
from pathlib import Path

# プロジェクトルートを自動取得
PROJECT_ROOT = Path(__file__).resolve().parent

# scripts/ ディレクトリへのパス
SCRIPTS_DIR = PROJECT_ROOT / "scripts"

# data ディレクトリへのパス
DATA_DIR = PROJECT_ROOT / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"

# 他にもよく使うパスや設定をここで定義しておく
