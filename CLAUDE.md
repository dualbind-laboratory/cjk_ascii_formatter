# CLAUDE.md - AI Assistant Guide for cjk_ascii_formatter

**Last Updated**: 2025-11-17
**Project Version**: Early Development (Initial Commit)
**License**: MIT

---

## Project Overview

### Purpose
`cjk_ascii_formatter` is a Python-based formatting and linting tool designed to enforce consistent spacing between CJK (Chinese, Japanese, Korean) characters and ASCII text according to Dualbind rules v3.1.

### Problem Statement
Mixed CJK and ASCII text often lacks proper spacing, making content harder to read. This tool automatically formats and validates spacing between:
- CJK characters and ASCII letters/numbers
- CJK characters and ASCII punctuation
- Mixed-script content in documentation, code comments, and text files

### Core Functionality (Planned)
- **Formatter**: Automatically add/remove spaces according to Dualbind rules v3.1
- **Linter**: Check files for spacing violations and report issues
- **CLI Tool**: Command-line interface for easy integration
- **Library**: Importable Python module for programmatic use
- **Pre-commit Hook**: Git integration for automatic formatting

---

## Current Repository State

### Existing Files
```
cjk_ascii_formatter/
├── .git/
├── .gitignore          # Python-focused gitignore
├── LICENSE             # MIT License (2025 dualbind-laboratory)
└── README.md           # Basic project description
```

### Status
- **Stage**: Initial setup, no source code yet
- **Branch Strategy**: Feature branches prefixed with `claude/`
- **Main Branch**: Not yet established
- **Last Commit**: 955a6b5 (Initial commit)

---

## Recommended Project Structure

When implementing this project, follow this structure:

```
cjk_ascii_formatter/
├── .github/
│   └── workflows/          # CI/CD (GitHub Actions)
│       ├── test.yml
│       └── lint.yml
├── src/
│   └── cjk_ascii_formatter/
│       ├── __init__.py     # Package initialization
│       ├── __main__.py     # CLI entry point
│       ├── formatter.py    # Core formatting logic
│       ├── linter.py       # Linting/checking logic
│       ├── rules.py        # Dualbind rules v3.1 implementation
│       ├── detector.py     # CJK/ASCII detection utilities
│       └── cli.py          # Command-line interface
├── tests/
│   ├── __init__.py
│   ├── test_formatter.py
│   ├── test_linter.py
│   ├── test_rules.py
│   ├── test_detector.py
│   └── fixtures/           # Test data files
│       ├── valid/
│       └── invalid/
├── docs/
│   ├── rules.md            # Dualbind rules v3.1 specification
│   ├── api.md              # API documentation
│   └── examples.md         # Usage examples
├── .gitignore
├── .pre-commit-config.yaml # Pre-commit hooks configuration
├── pyproject.toml          # Modern Python project config (PEP 621)
├── README.md
├── CLAUDE.md               # This file
├── CHANGELOG.md            # Version history
└── LICENSE
```

---

## Development Workflows

### Initial Setup
When setting up the development environment:

1. **Create project structure**:
   ```bash
   mkdir -p src/cjk_ascii_formatter tests docs
   ```

2. **Set up pyproject.toml** with:
   - Project metadata (name, version, description, authors)
   - Dependencies (click for CLI, regex for pattern matching)
   - Dev dependencies (pytest, black, ruff, mypy)
   - Build system (hatchling or setuptools)
   - Tool configurations (pytest, black, ruff, mypy)

3. **Install in development mode**:
   ```bash
   pip install -e ".[dev]"
   ```

### Development Cycle
1. **Create feature branch**: `claude/feature-name-<session-id>`
2. **Write tests first** (TDD approach)
3. **Implement functionality**
4. **Run tests**: `pytest -v`
5. **Format code**: `black src/ tests/`
6. **Lint code**: `ruff check src/ tests/`
7. **Type check**: `mypy src/`
8. **Commit with descriptive message**
9. **Push to feature branch**

### Testing Requirements
- **Minimum coverage**: 80%
- **Test categories**:
  - Unit tests for each module
  - Integration tests for CLI
  - Fixture-based tests with real-world examples
  - Edge cases (empty strings, pure CJK, pure ASCII, mixed scripts)

### Code Quality Standards
- **Formatter**: black (line length: 88)
- **Linter**: ruff (with strict settings)
- **Type Checker**: mypy (strict mode)
- **Docstrings**: Google style
- **Imports**: Organized with isort

---

## Dualbind Rules v3.1 (Expected)

Based on the project description, implement these spacing rules:

### Rule Categories
1. **CJK ↔ ASCII Letters/Numbers**
   - Add space between CJK and ASCII alphanumeric
   - Example: `中文English` → `中文 English`
   - Example: `日本語123` → `日本語 123`

2. **CJK ↔ ASCII Punctuation**
   - Handle special punctuation rules
   - Preserve existing formatting for quotes, parentheses
   - Example: `中文(English)` → `中文 (English)`

3. **Exceptions**
   - No space before/after certain punctuation: `,`, `.`, `!`, `?`
   - Preserve code blocks and inline code
   - Respect existing double spaces and line breaks

4. **Line Breaks and Whitespace**
   - Preserve paragraph structure
   - Maintain indentation
   - Handle trailing whitespace

### Configuration
Support configuration via:
- `pyproject.toml` under `[tool.cjk-ascii-formatter]`
- `.cjk-ascii-formatter.toml` in project root
- Command-line flags

---

## Coding Conventions

### Python Style
- **Version**: Python 3.9+ (use modern features)
- **Type Hints**: Required for all functions
- **Error Handling**: Use custom exceptions, never bare `except`
- **Logging**: Use `logging` module, not print statements
- **Constants**: UPPER_SNAKE_CASE at module level

### Naming Conventions
- **Modules**: lowercase_with_underscores
- **Classes**: PascalCase
- **Functions**: lowercase_with_underscores
- **Variables**: lowercase_with_underscores
- **Private**: Leading underscore _private_function

### Documentation
- **Docstrings**: Required for all public functions/classes
- **Format**: Google style
- **Include**: Description, Args, Returns, Raises, Examples

Example:
```python
def format_text(text: str, strict: bool = False) -> str:
    """Format CJK-ASCII spacing according to Dualbind rules.

    Args:
        text: Input text with mixed CJK and ASCII characters.
        strict: If True, enforce strict spacing rules.

    Returns:
        Formatted text with proper spacing.

    Raises:
        ValueError: If text is None.

    Examples:
        >>> format_text("中文English")
        '中文 English'
    """
```

### Imports Organization
```python
# Standard library
import re
import sys
from pathlib import Path

# Third-party
import click

# Local
from cjk_ascii_formatter.rules import DualbindRules
```

---

## Key Technical Decisions

### Unicode Handling
- Use Python's built-in Unicode support
- Identify CJK characters using Unicode ranges:
  - CJK Unified Ideographs: U+4E00 to U+9FFF
  - Hiragana: U+3040 to U+309F
  - Katakana: U+30A0 to U+30FF
  - Hangul: U+AC00 to U+D7AF

### Pattern Matching
- Use `regex` module (not `re`) for Unicode property support
- Build comprehensive regex patterns for rule detection
- Cache compiled patterns for performance

### CLI Design
- Use `click` for CLI framework
- Support stdin/stdout piping
- Provide `--check` mode (exit 1 on violations)
- Provide `--fix` mode (auto-format)
- Support glob patterns for multiple files

### Performance Considerations
- Process files in streaming mode for large files
- Use generators where possible
- Implement caching for repeated pattern matches
- Benchmark with files >10MB

---

## Git Workflow

### Branch Strategy
- **Feature branches**: `claude/<description>-<session-id>`
- **Branch from**: Current development branch or main
- **Merge via**: Pull requests (when main branch established)

### Commit Messages
Follow Conventional Commits:
- `feat: Add CJK character detection`
- `fix: Correct spacing around parentheses`
- `docs: Update API documentation`
- `test: Add edge cases for mixed scripts`
- `refactor: Simplify rule matching logic`
- `chore: Update dependencies`

### Pushing Changes
```bash
# Always push to feature branch with -u flag
git push -u origin claude/feature-name-<session-id>
```

### Retry Logic
If network errors occur:
- Retry up to 4 times with exponential backoff (2s, 4s, 8s, 16s)
- Applies to: git push, git fetch, git pull

---

## Testing Guidelines

### Test Structure
```python
import pytest
from cjk_ascii_formatter import format_text

class TestFormatter:
    def test_cjk_ascii_spacing(self):
        """Test basic CJK-ASCII spacing."""
        input_text = "中文English"
        expected = "中文 English"
        assert format_text(input_text) == expected

    @pytest.mark.parametrize("input,expected", [
        ("中文English", "中文 English"),
        ("日本語123", "日本語 123"),
        ("한글ABC", "한글 ABC"),
    ])
    def test_multiple_cases(self, input, expected):
        """Test multiple formatting cases."""
        assert format_text(input) == expected
```

### Test Fixtures
Create fixtures in `tests/fixtures/`:
- `valid/` - Correctly formatted examples
- `invalid/` - Examples needing formatting
- Use real-world text samples (documentation, README files, blog posts)

### Running Tests
```bash
# All tests
pytest

# With coverage
pytest --cov=cjk_ascii_formatter --cov-report=html

# Specific file
pytest tests/test_formatter.py

# Watch mode (with pytest-watch)
ptw
```

---

## Dependencies

### Core Dependencies
- **click** (>= 8.0): CLI framework
- **regex** (>= 2023.0.0): Advanced Unicode regex

### Development Dependencies
- **pytest** (>= 7.0): Testing framework
- **pytest-cov**: Coverage reporting
- **black**: Code formatting
- **ruff**: Fast linting
- **mypy**: Static type checking
- **pre-commit**: Git hooks

### Optional Dependencies
- **rich**: Enhanced CLI output
- **pydantic**: Configuration validation

---

## Common Tasks for AI Assistants

### When Asked to Add Features
1. Check if feature aligns with Dualbind rules v3.1
2. Write tests first (TDD)
3. Implement in appropriate module
4. Update documentation
5. Add usage examples
6. Run full test suite

### When Asked to Fix Bugs
1. Reproduce the issue with a test
2. Identify root cause
3. Implement fix
4. Verify test passes
5. Check for similar issues elsewhere
6. Update CHANGELOG.md

### When Asked to Refactor
1. Ensure tests exist and pass
2. Make incremental changes
3. Run tests after each change
4. Preserve public API
5. Update docstrings if needed

### When Asked About Rules
1. Refer to `docs/rules.md` (when it exists)
2. For Dualbind rules v3.1, research if specification is unclear
3. Provide examples of correct formatting
4. Cite specific rule numbers/sections

---

## Important Reminders

### Do Not
- Skip writing tests
- Commit directly to main branch (when established)
- Use `print()` for debugging (use `logging`)
- Ignore type errors
- Add dependencies without updating `pyproject.toml`

### Always
- Run tests before committing
- Update documentation when changing behavior
- Use type hints
- Handle edge cases (empty input, None, invalid Unicode)
- Consider performance impact
- Follow existing code style

### Before Pushing
1. All tests pass: `pytest`
2. Code is formatted: `black src/ tests/`
3. No linting errors: `ruff check src/ tests/`
4. Type checking passes: `mypy src/`
5. Documentation is updated
6. Commit message follows conventions

---

## Resources

### Unicode References
- [Unicode CJK Blocks](https://en.wikipedia.org/wiki/CJK_Unified_Ideographs)
- [Unicode Property Escapes](https://www.regular-expressions.info/unicode.html)

### Python Best Practices
- [PEP 8 - Style Guide](https://pep8.org/)
- [PEP 257 - Docstring Conventions](https://www.python.org/dev/peps/pep-0257/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)

### Tools Documentation
- [pytest Documentation](https://docs.pytest.org/)
- [black Documentation](https://black.readthedocs.io/)
- [ruff Documentation](https://beta.ruff.rs/docs/)
- [mypy Documentation](https://mypy.readthedocs.io/)
- [click Documentation](https://click.palletsprojects.com/)

---

## Questions & Decisions Needed

### To Be Determined
1. **Exact Dualbind Rules v3.1 Specification**
   - Need detailed rules document
   - Edge case handling
   - Exception rules

2. **Configuration Format**
   - Which options should be configurable?
   - Default behavior vs. strict mode?

3. **CLI Interface**
   - Exact command structure
   - Flag names and defaults
   - Output format (human-readable vs. machine-readable)

4. **Platform Support**
   - Windows line endings?
   - Path handling across OS?

5. **Performance Targets**
   - Acceptable processing speed?
   - Maximum file size to handle?

---

## Change Log

### 2025-11-17 - Initial CLAUDE.md Creation
- Created comprehensive guide for AI assistants
- Documented project structure and conventions
- Outlined development workflows
- Established testing and code quality standards
- Repository contains only README, LICENSE, and .gitignore

---

## Contact & Contribution

**Repository**: dualbind-laboratory/cjk_ascii_formatter
**License**: MIT
**Python Version**: 3.9+

When contributing or making changes, always refer to this guide to maintain consistency and quality across the codebase.
