"""Task 3.2 / 3.3 - processor with a custom exception and a complete try statement."""
import sys


class InvalidRecord(Exception):
    """A single damaged line.  Raised in parse_line(), handled in process_file()."""


class AttendanceFileError(Exception):
    """A whole file could not be processed.  Wraps the original cause (raise ... from ...)."""


def parse_line(line):
    parts = line.strip().split(",")
    try:
        reg, date, status = parts            # ValueError if not exactly 3 fields
    except ValueError as exc:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}") from exc
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status {status!r}")
    return reg, date, status


def process_file(path):
    """Return (present, absent, bad_lines).  Raises AttendanceFileError for file-level failures."""
    present = absent = 0
    bad = []
    f = None
    try:
        f = open(path, encoding="utf-8")
        lines = f.readlines()                # UnicodeDecodeError surfaces here, not in open()
    except FileNotFoundError as exc:
        raise AttendanceFileError(f"{path}: file or folder does not exist") from exc
    except PermissionError as exc:
        raise AttendanceFileError(f"{path}: permission denied") from exc
    except IsADirectoryError as exc:
        raise AttendanceFileError(f"{path}: is a folder, not a file") from exc
    except UnicodeDecodeError as exc:
        raise AttendanceFileError(f"{path}: not valid UTF-8 text") from exc
    else:
        if not lines:
            raise AttendanceFileError(f"{path}: file is empty")
        for n, line in enumerate(lines, 1):
            try:
                _, _, status = parse_line(line)
            except InvalidRecord as exc:
                bad.append((n, str(exc)))
            else:
                if status == "P":
                    present += 1
                else:
                    absent += 1
        return present, absent, bad
    finally:
        if f is not None:                    # runs on success AND on every failure
            f.close()


if __name__ == "__main__":
    import os, tempfile
    d = tempfile.mkdtemp()
    good = os.path.join(d, "good.csv"); open(good, "w").write("1,2026-10-08,P\n2,2026-10-08\n3,2026-10-08,A\n")
    empty = os.path.join(d, "empty.csv"); open(empty, "w").close()
    binary = os.path.join(d, "binary.csv"); open(binary, "wb").write(b"\xff\xfe\x00bad")
    for p in [good, empty, binary, os.path.join(d, "missing.csv"), d]:
        try:
            print(os.path.basename(p) or "<folder>", "->", process_file(p))
        except AttendanceFileError as e:
            print(os.path.basename(p) or "<folder>", "-> AttendanceFileError:", e, "| cause:", type(e.__cause__).__name__)
