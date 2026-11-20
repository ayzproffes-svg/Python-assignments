from pathlib import Path


class InvalidRecord(Exception):
    pass


def parse_line(line):
    parts = line.strip().split(",")
    if len(parts) != 3:
        raise InvalidRecord(f"expected 3 fields, found {len(parts)}")
    reg, date, status = (p.strip() for p in parts)
    if status not in ("P", "A"):
        raise InvalidRecord(f"invalid status '{status}'")
    return reg, date, status


def read_folder(folder):
    records, errors = [], []
    for path in sorted(Path(folder).glob("*.csv")):
        try:
            with open(path, encoding="utf-8") as f:
                for n, line in enumerate(f, 1):
                    if not line.strip():
                        continue
                    try:
                        records.append(parse_line(line))
                    except InvalidRecord as exc:
                        errors.append((path.name, n, str(exc)))
        except (OSError, UnicodeDecodeError) as exc:
            errors.append((path.name, 0, f"cannot read file: {exc}"))
    return records, errors
