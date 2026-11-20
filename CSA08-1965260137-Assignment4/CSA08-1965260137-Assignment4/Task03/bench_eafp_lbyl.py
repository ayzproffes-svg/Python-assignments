"""EAFP (try/except) vs LBYL (if checks) per-line cost, bad lines rare vs common. Real timings."""
import timeit
from attendance_processor import parse_line, InvalidRecord

def eafp(lines):
    ok = bad = 0
    for l in lines:
        try:
            parse_line(l); ok += 1
        except InvalidRecord:
            bad += 1
    return ok, bad

def lbyl(lines):
    ok = bad = 0
    for l in lines:
        parts = l.strip().split(",")
        if len(parts) == 3 and parts[2] in ("P", "A"):
            ok += 1
        else:
            bad += 1
    return ok, bad

N = 100_000
for pct in (0, 1, 10, 50):
    nbad = N * pct // 100
    lines = ["1,2026-10-08,P"] * (N - nbad) + ["1,2026-10-08"] * nbad
    assert eafp(lines) == lbyl(lines)
    t1 = min(timeit.repeat(lambda: eafp(lines), number=1, repeat=3))
    t2 = min(timeit.repeat(lambda: lbyl(lines), number=1, repeat=3))
    print(f"bad lines {pct:>3}%:  EAFP {t1/N*1e9:7.0f} ns/line   LBYL {t2/N*1e9:7.0f} ns/line")
