"""Organisation (b): reader + stats + report in one module."""
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

def percentage(present, total):
    return round(100 * present / total, 2) if total else 0.0


def percentages(records):
    counts = {}
    for reg, _, status in records:
        c = counts.setdefault(reg, [0, 0])
        c[1] += 1
        c[0] += status == "P"
    return {reg: percentage(p, t) for reg, (p, t) in counts.items()}


def below(pcts, limit=75.0):
    return {r: p for r, p in pcts.items() if p < limit}


def consecutive_absent(records, run=3):
    """Students with `run` or more consecutive recorded days marked A (NEW report, Task 5.2)."""
    by_student = {}
    for reg, date, status in sorted(records, key=lambda r: (r[0], r[1])):
        by_student.setdefault(reg, []).append(status)
    result = []
    for reg, statuses in by_student.items():
        streak = best = 0
        for s in statuses:
            streak = streak + 1 if s == "A" else 0
            best = max(best, streak)
        if best >= run:
            result.append((reg, best))
    return sorted(result)

def write_all(out_dir, pcts, low, errors, absent_run):
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with open(out / "attendance_report.csv", "w", encoding="utf-8") as f:
        f.write("register_no,percentage\n")
        for reg in sorted(pcts):
            f.write(f"{reg},{pcts[reg]}\n")
    with open(out / "below_75.csv", "w", encoding="utf-8") as f:
        f.write("register_no,percentage\n")
        for reg in sorted(low):
            f.write(f"{reg},{low[reg]}\n")
    with open(out / "damaged_lines.log", "w", encoding="utf-8") as f:
        for name, n, msg in errors:
            f.write(f"{name}:{n}: {msg}\n")
    with open(out / "absent_3_days.csv", "w", encoding="utf-8") as f:     # NEW report
        f.write("register_no,longest_absent_run\n")
        for reg, run in absent_run:
            f.write(f"{reg},{run}\n")
