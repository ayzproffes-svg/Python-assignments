from pathlib import Path


def read_department_file(path):
    """Yield (line_number, text) for non-blank lines. Raises OSError / UnicodeDecodeError to the caller."""
    with open(path, encoding="utf-8") as f:
        for n, line in enumerate(f, 1):
            if line.strip():
                yield n, line
