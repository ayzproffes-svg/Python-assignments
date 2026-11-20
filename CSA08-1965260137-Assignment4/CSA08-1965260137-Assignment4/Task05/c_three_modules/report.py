from pathlib import Path


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
