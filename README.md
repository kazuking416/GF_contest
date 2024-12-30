# GF_contest

このプロジェクトは、データセットを用いた分析・モデル構築・結果の共有を目的としています。  
本リポジトリでは以下のディレクトリ構造を採用しており、それぞれの役割や使い方をまとめています。

```text
my_data_analysis_project/
├── config.py
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
├── scripts/
├── docs/
│   └── memo.md
├── results/
├── README.md
└── requirements.txt  (または environment.yml 等)
```

## ディレクトリ構造の詳細

### 1. `data/`
- **生データや中間生成物などのデータファイルを管理するディレクトリ** です。
- データの前処理を行う際は、`data/raw` 以下にある元データから必要な工程を踏み、`data/processed` に保存することを推奨します。

#### `data/raw/`
- 分析前のオリジナルのデータファイルを配置します。  
  例: `data/raw/train.csv`, `data/raw/test.csv`

#### `data/processed/`
- 前処理後のデータ（例: 欠損値補完、特徴量エンジニアリング後のデータなど）を配置します。  
  例: `data/processed/cleaned_train.csv`

### 2. `notebooks/`
- **Jupyter Notebook (`.ipynb`) を中心とした実験や可視化を行う場所** です。
- `01_data_exploration.ipynb`, `02_modeling.ipynb` といった形で**連番や目的別に名前を付ける**と管理しやすくなります。
- 大規模なノートブックが増える場合は、サブディレクトリを作成するなどして整理してください。

### 3. `scripts/`
- **Python スクリプト (`.py`) を配置する場所** です。
- Notebook から切り出した共通関数や、バッチで動かすトレーニングスクリプト、ユーティリティ関数などをまとめます。
- 規模が大きくなる場合は、さらにサブフォルダを作って機能別に整理してください。

### 4. `config.py`
- **パスや設定を集中的に管理するためのファイル** です。
- プロジェクトルート (`PROJECT_ROOT`) や `data/` へのパスなどを `pathlib.Path` で定義し、Notebook やスクリプトから `import` して使います。
- 例:  
  ```python
  import os
  from pathlib import Path
  
  # プロジェクトルートを自動取得
  PROJECT_ROOT = Path(__file__).resolve().parent
  
  # data ディレクトリへのパス
  DATA_DIR = PROJECT_ROOT / "data"
  RAW_DATA_DIR = DATA_DIR / "raw"
  PROCESSED_DATA_DIR = DATA_DIR / "processed"
  ```

### 5. `docs/`
- **プロジェクトのドキュメントやメモを書き留めるディレクトリ** です。
- チームメンバーが把握すべき内容を `memo.md` としてまとめるなど、自由に活用してください。

#### `docs/memo.md`
- 分析の過程や仮説、調査メモ、実験の概要などを Markdown で記載してください。  
  他の人が参照できるような形で残しておくと、情報共有がスムーズになります。

### 6. `results/`
- **分析結果（グラフ、モデルの出力、レポートなど）を保存するディレクトリ** です。
- 画像ファイル（例: `.png`, `.jpg`）や、評価結果の CSV、HTML レポートなどを一元管理します。

### 7. `requirements.txt` または `environment.yml`
- **Python 環境に必要なライブラリ** をまとめるファイルです。
- チームで分析環境を揃える場合や、本プロジェクトを再現する場合に役立ちます。
- Conda を使用している場合は `environment.yml` に、pip のみを使用している場合は `requirements.txt` にまとめるのがおすすめです。

### 8. `README.md` (本ファイル)
- **このリポジトリ全体の概要や構成についてまとめるファイル** です。
- 初めてこのリポジトリをクローンした人が一読して、何をどのように進めればよいのか理解できる内容を心がけてください。

---

## 開発環境の構築

1. リポジトリをクローン:
    ```bash
    git clone https://github.com/username/my_data_analysis_project.git
    cd my_data_analysis_project
    ```
2. 必要なライブラリをインストール:
    - `requirements.txt` がある場合:
      ```bash
      pip install -r requirements.txt
      ```
    - `environment.yml` がある場合:
      ```bash
      conda env create -f environment.yml
      conda activate <環境名>
      ```

3. Jupyter Notebook で作業する場合:
    ```bash
    jupyter notebook
    ```
    または
    ```bash
    jupyter lab
    ```
    を実行して、`notebooks/` ディレクトリの Notebook を開きます。

---

## パス管理の方針 (`config.py`)

このプロジェクトでは、複数の Notebook やスクリプト間で **一貫したパス管理** を行うため、`config.py` を利用します。

1. `config.py` 内で、プロジェクトのルートや `data/` フォルダなどのパスを `pathlib.Path` で定義します。
2. Notebook やスクリプト内で `import config` することで、任意の場所から同じパスを簡潔に参照できます。  
   ```python
   import config
   import pandas as pd

   # 生データのパス
   train_path = config.RAW_DATA_DIR / "train.csv"
   df = pd.read_csv(train_path)
   ```
3. チームで作業する際も、`config.py` を修正するだけで全ての Notebook / スクリプトが更新されたパスを参照するようになるため、**相対パスの書き換えミス**が格段に減ります。

---

## 使い方の流れ

1. **データ取得**  
   `data/raw/` に元データを配置します。

2. **前処理**  
   Notebook またはスクリプトを使ってデータクレンジングや特徴量エンジニアリングを行い、完成したデータを `data/processed/` に保存します。パスは `config.py` を使って参照します。

3. **分析・モデリング**  
   ノートブック (例: `notebooks/02_modeling.ipynb`) などで分析を進めます。共通して使う関数やクラスは `scripts/` に整理します。

4. **結果の保存**  
   Notebook で生成した可視化、モデルの予測結果、レポートなどを `results/` に保存します。

5. **ドキュメント作成**  
   考察やメモなどのドキュメントは、`docs/` ディレクトリ内に保管します。何を行ったか、どういう結果だったか、次のステップは何かを簡潔にまとめておくと便利です。

---

## ライセンス

- もし必要であれば、著作権や再配布ルールなどをこちらに追記してください。

---

## コントリビューション

- コントリビューションの方法がある場合は、Issue や Pull Request の手順・レビュー手順を追記してください。

---

不明点や質問があれば、適宜 `docs/memo.md` に追記したり、Issue を立てるなどしてプロジェクトメンバー同士で情報を共有しましょう。  
統一的に `config.py` を使ってパスを指定することで、複雑な相対パス指定やパスの書き換えを大幅に削減し、効率的に開発・分析を進めることができます。