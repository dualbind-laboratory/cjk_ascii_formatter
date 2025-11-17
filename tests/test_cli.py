"""Smoke tests for CLI functionality."""

import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
from click.testing import CliRunner

from cjk_ascii_formatter.cli import main


@pytest.fixture
def runner() -> CliRunner:
    """Create a CLI test runner."""
    return CliRunner()


@pytest.fixture
def sample_file(tmp_path: Path) -> Path:
    """Create a temporary sample file."""
    test_file = tmp_path / "test.txt"
    test_file.write_text("中文English日本語123")
    return test_file


def test_version(runner: CliRunner) -> None:
    """Test version flag."""
    result = runner.invoke(main, ["--version"])
    assert result.exit_code == 0
    assert "cjkfmt" in result.output
    assert "0.1.0" in result.output


def test_check_mode(runner: CliRunner, sample_file: Path) -> None:
    """Test check mode with a sample file."""
    result = runner.invoke(main, ["--check", str(sample_file)])
    assert result.exit_code == 0
    assert "Checking" in result.output


def test_write_mode(runner: CliRunner, sample_file: Path) -> None:
    """Test write mode with a sample file."""
    result = runner.invoke(main, ["--write", str(sample_file)])
    assert result.exit_code == 0
    assert "Formatting" in result.output


def test_no_files_error(runner: CliRunner) -> None:
    """Test error when no files are specified."""
    result = runner.invoke(main, ["--check"])
    assert result.exit_code == 1
    assert "No files specified" in result.output


def test_conflicting_flags(runner: CliRunner, sample_file: Path) -> None:
    """Test error when both --check and --write are specified."""
    result = runner.invoke(main, ["--check", "--write", str(sample_file)])
    assert result.exit_code == 1
    assert "mutually exclusive" in result.output


def test_no_mode_error(runner: CliRunner, sample_file: Path) -> None:
    """Test error when neither --check nor --write is specified."""
    result = runner.invoke(main, [str(sample_file)])
    assert result.exit_code == 1
    assert "Specify either --check or --write" in result.output


def test_cli_entry_point() -> None:
    """Test that the cjkfmt entry point is installed."""
    result = subprocess.run(
        [sys.executable, "-m", "cjk_ascii_formatter", "--version"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "cjkfmt" in result.stdout
