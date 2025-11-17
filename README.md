# cjk_ascii_formatter

CJK–ASCII spacing formatter & linter (Dualbind rules v3.1)

A Python tool for enforcing consistent spacing between CJK (Chinese, Japanese, Korean) characters and ASCII text.

最新のリリース: https://github.com/dualbind-laboratory/cjk_ascii_formatter/releases/latest

## Quick Start

Install and check version:
```bash
pip install -e .
cjkfmt --version
```

Format text with proper CJK ↔ ASCII spacing (ASCII runs stay intact):
```bash
echo "日本語123ABC" | cjkfmt --write -
# Output: 日本語 123ABC

echo "CJK混在AIテキストv3" | cjkfmt --write -
# Output: CJK 混在 AI テキスト v3

echo "Version2日本語" | cjkfmt --write -
# Output: Version2 日本語
```

## How to Install & Run (Dev)

### Prerequisites
- Python 3.10 or higher
- pip or uv

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/dualbind-laboratory/cjk_ascii_formatter.git
   cd cjk_ascii_formatter
   ```

2. Install in development mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

   Or using uv:
   ```bash
   uv pip install -e ".[dev]"
   ```

### Usage

Run the formatter with:

```bash
# Check files for formatting issues
cjkfmt --check file1.txt file2.txt

# Format files in-place
cjkfmt --write file1.txt file2.txt

# Show version
cjkfmt --version
```

### Development

Run tests:
```bash
pytest
```

Run linting and type checking:
```bash
ruff check src/ tests/
mypy src/
```

Format code:
```bash
ruff check --fix src/ tests/
```

## License

MIT
