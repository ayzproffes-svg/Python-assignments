"""Single pass with dictionary (O(f*l)) vs re-reading all files per student (O(s*f*l)). Real timings."""
import os, tempfile, time, random, shutil
from pathlib import Path

def make(folder, s, f, ):
    random.seed(2)
    for d in range(f):
        with open(Path(folder) / f"day{d:02d}.csv", "w") as fh:
            for i in range(s):
                fh.write(f"19{i:07d},2026-10-{d+1:02d},{random.choice('PPPA')}\n")

def single_pass(folder):
    counts = {}
    for p in sorted(Path(folder).glob("*.csv")):
        with open(p) as fh:
            for line in fh:
                reg, _, st = line.strip().split(",")
                c = counts.setdefault(reg, [0, 0]); c[1] += 1; c[0] += st == "P"
    return counts

def per_student(folder, regs):
    out = {}
    for reg in regs:
        present = total = 0
        for p in sorted(Path(folder).glob("*.csv")):
            with open(p) as fh:
                for line in fh:
                    r, _, st = line.strip().split(",")
                    if r == reg:
                        total += 1; present += st == "P"
        out[reg] = [present, total]
    return out

print(f"{'s':>5} {'f':>3} {'l=s':>5} | {'single pass (ms)':>17} | {'per-student (ms)':>17} | ratio")
for s, f in [(25, 10), (50, 10), (100, 10), (200, 10)]:
    d = tempfile.mkdtemp(); make(d, s, f)
    t = time.perf_counter(); a = single_pass(d); t1 = time.perf_counter() - t
    t = time.perf_counter(); b = per_student(d, list(a)); t2 = time.perf_counter() - t
    assert a == b
    print(f"{s:>5} {f:>3} {s:>5} | {t1*1000:>17.2f} | {t2*1000:>17.2f} | {t2/t1:6.1f}x")
    shutil.rmtree(d)
