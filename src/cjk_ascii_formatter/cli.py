"""Command-line interface for CJK-ASCII formatter."""

import sys
from pathlib import Path

import click

from cjk_ascii_formatter import __version__, format_text


@click.command()
@click.version_option(version=__version__, prog_name="cjkfmt")
@click.option(
    "--check",
    is_flag=True,
    help="Check formatting without making changes (exit 1 if violations found).",
)
@click.option(
    "--write",
    is_flag=True,
    help="Format files in-place (use '-' for stdin/stdout).",
)
@click.argument("files", nargs=-1)
def main(check: bool, write: bool, files: tuple[str, ...]) -> None:
    """CJK-ASCII spacing formatter and linter (Dualbind rules v3.1).

    Format or check spacing between CJK and ASCII characters.

    Use '-' as filename to read from stdin and write to stdout.
    """
    if check and write:
        click.echo("Error: --check and --write are mutually exclusive.", err=True)
        sys.exit(1)

    if not files:
        click.echo("Error: No files specified.", err=True)
        sys.exit(1)

    if not check and not write:
        click.echo("Error: Specify either --check or --write.", err=True)
        sys.exit(1)

    # Handle stdin/stdout
    if len(files) == 1 and files[0] == "-":
        if not write:
            click.echo("Error: stdin mode only works with --write.", err=True)
            sys.exit(1)

        content = sys.stdin.read()
        formatted = format_text(content)
        sys.stdout.write(formatted)
        sys.exit(0)

    # Handle file operations
    has_violations = False

    for file_path_str in files:
        file_path = Path(file_path_str)

        if not file_path.exists():
            click.echo(f"Error: File not found: {file_path}", err=True)
            sys.exit(1)

        try:
            content = file_path.read_text(encoding="utf-8")
            formatted = format_text(content)

            if check:
                if content != formatted:
                    click.echo(f"Would reformat: {file_path}")
                    has_violations = True
            elif write:
                if content != formatted:
                    file_path.write_text(formatted, encoding="utf-8")
                    click.echo(f"Formatted: {file_path}")
                else:
                    click.echo(f"Already formatted: {file_path}")

        except Exception as e:
            click.echo(f"Error processing {file_path}: {e}", err=True)
            sys.exit(1)

    if check and has_violations:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()
