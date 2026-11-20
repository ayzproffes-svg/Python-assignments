"""Task 2 - reference implementation of the monthly attendance design.

Usage: python process_month.py [folder] [output_folder]
Reads every *.csv in `folder` once, accumulates counts in a dict, writes
attendance_report.csv, below_75.csv and damaged_lines.log.
"""
import csv
import sys
from pathlib import Path


def process_folder(folder):
    counts = {}      # reg_no -> [present_days, total_days]
    damaged = []     # (file name, line number, reason, text)
    folder = Path(folder)
    if not folder.is_dir():                       # Path.glob() on a missing folder silently yields nothing
        raise FileNotFoundError(folder)
    for path in sorted(folder.glob("*.csv")):                 # one pass over each file
        with open(path, "r", encoding="utf-8") as f:
            for line_no, line in enumerate(f, start=1):
                line = line.strip()
                if not line:
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    damaged.append((path.name, line_no, f"expected 3 fields, found {len(parts)}", line))
                    continue
                reg, date, status = (p.strip() for p in parts)
                if status not in ("P", "A") or not reg or not date:
                    damaged.append((path.name, line_no, f"invalid status '{status}'", line))
                    continue
                entry = counts.setdefault(reg, [0, 0])
                entry[1] += 1
                if status == "P":
                    entry[0] += 1
    return counts, damaged


def write_reports(counts, damaged, out_dir, limit=75.0):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = []
    for reg in sorted(counts):
        present, total = counts[reg]
        rows.append((reg, present, total, round(100 * present / total, 2)))
    with open(out_dir / "attendance_report.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["register_no", "present", "total", "percentage"])
        w.writerows(rows)
    with open(out_dir / "below_75.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["register_no", "percentage"])
        w.writerows((r[0], r[3]) for r in rows if r[3] < limit)
    with open(out_dir / "damaged_lines.log", "w", encoding="utf-8") as f:
        for name, line_no, reason, text in damaged:
            f.write(f"{name}:{line_no}: {reason}: {text!r}\n")
    return rows


if __name__ == "__main__":
    folder = sys.argv[1] if len(sys.argv) > 1 else "data_oct"
    out = sys.argv[2] if len(sys.argv) > 2 else "output"
    try:
        counts, damaged = process_folder(folder)
    except FileNotFoundError:
        sys.exit(f"Folder not found: {folder}")
    rows = write_reports(counts, damaged, out)
    for r in rows:
        print(r)
    print(f"{len(damaged)} damaged line(s) logged to {out}/damaged_lines.log")
