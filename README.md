[![CI](https://github.com/dualbind-laboratory/cjk_ascii_formatter/actions/workflows/ci.yml/badge.svg)](https://github.com/dualbind-laboratory/cjk_ascii_formatter/actions/workflows/ci.yml)
[![Release](https://img.shields.io/github/v/release/dualbind-laboratory/cjk_ascii_formatter?display_name=tag&sort=semver)](https://github.com/dualbind-laboratory/cjk_ascii_formatter/releases/latest)

# cjk_ascii_formatter

CJK–ASCII spacing formatter & linter (Dualbind rules v3.1)

A Python tool that inserts a half-width space at CJK↔ASCII boundaries while keeping ASCII runs intact.

Latest release: <https://github.com/dualbind-laboratory/cjk_ascii_formatter/releases/latest>

---

## Quick Start

### Install (until PyPI is available)

**Option A — from a tagged release (recommended)**

```bash
pip install "git+https://github.com/dualbind-laboratory/cjk_ascii_formatter@v0.1.0"
```

**Option B — from source**

```bash
git clone https://github.com/dualbind-laboratory/cjk_ascii_formatter.git
cd cjk_ascii_formatter
pip install -e .
```

### Usage

```bash
# stdin → formatted to stdout, ASCII runs preserved
echo "日本語123ABC" | cjkfmt --write -
# Output: 日本語 123ABC

echo "CJK混在AIテキストv3" | cjkfmt --write -
# Output: CJK 混在 AI テキスト v3

echo "Version2日本語" | cjkfmt --write -
# Output: Version2 日本語

# format a file in place
cjkfmt --write path/to/file.txt

# show version
cjkfmt --version
```

---

## Development

### Prerequisites

- Python 3.10+
- pip or uv

### Setup

```bash
pip install -e ".[dev]"    # or: uv pip install -e ".[dev]"
```

### Lint / Type / Test

```bash
ruff check src/ tests/
mypy src/
pytest
ruff check --fix src/ tests/
```

---

## Known limitations

- Currently only the basic “CJK × ASCII spacing” rule is implemented.
  More rules (punctuation, brackets, quotes, etc.) will be added.

## Roadmap

- Punctuation / bracket / quote rules
- Dry-run / diff outputs
- Recursive directory processing and ignore patterns

For correspondence: laboratory@dualbind.com

## License

MIT
