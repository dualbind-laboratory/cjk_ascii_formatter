**English README：** see [`README.md`](README.md)
[![CI](https://github.com/dualbind-laboratory/cjk_ascii_formatter/actions/workflows/ci.yml/badge.svg)](https://github.com/dualbind-laboratory/cjk_ascii_formatter/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/dualbind-laboratory/cjk_ascii_formatter?display_name=tag&sort=semver)](https://github.com/dualbind-laboratory/cjk_ascii_formatter/releases/latest)

# cjk_ascii_formatter

CJK–ASCII スペーシング フォーマッタ & リンター（ Dualbind rules v3.1 ）

CJK（中国語・日本語・韓国語）と ASCII の境界に **半角スペース** を自動挿入し、ASCII の連続部分はそのまま保持する Python ツールです。

最新リリース：<https://github.com/dualbind-laboratory/cjk_ascii_formatter/releases/latest>

---

## クイックスタート

### インストール（ PyPI 公開までは GitHub から ）

**方法 A — タグ付きリリースからインストール（推奨）**
```bash
pip install "git+https://github.com/dualbind-laboratory/cjk_ascii_formatter@v0.1.0"
```

**方法 B — ソースからインストール**
```bash
git clone https://github.com/dualbind-laboratory/cjk_ascii_formatter.git
cd cjk_ascii_formatter
pip install -e .
```

### 使い方
```bash
# 標準入力 → 整形（ASCII 連続は維持）
echo "日本語123ABC" | cjkfmt --write -
# 出力: 日本語 123ABC

echo "CJK混在AIテキストv3" | cjkfmt --write -
# 出力: CJK 混在 AI テキスト v3

echo "Version2日本語" | cjkfmt --write -
# 出力: Version2 日本語

# ファイルを上書き整形
cjkfmt --write path/to/file.txt

# バージョン表示
cjkfmt --version
```

---

## 開発者向け

### 前提
- Python 3.10 以上
- pip または uv

### セットアップ
```bash
pip install -e ".[dev]"    # もしくは: uv pip install -e ".[dev]"
```

### Lint / 型 / テスト
```bash
ruff check src/ tests/
mypy src/
pytest
ruff check --fix src/ tests/
```

---

## 既知の制限
- 現状は基本ルール（ CJK × ASCII の境界スペース ）のみ。句読点・括弧・引用符などの詳細規則は順次追加予定。

## 今後の予定
- 句読点・括弧・引用符まわりの詳細ルール
- dry-run / diff 出力オプション
- ディレクトリ再帰処理と除外パターン

連絡先：laboratory@dualbind.com

## ライセンス
MIT
