"""Duplicate detection: set (O(n) total) vs list search (O(n^2) total). Real timings, all-unique registrations."""
import time
print(f"{'n':>7} | {'set (ms)':>10} | {'list (ms)':>10} | ratio")
for n in (1000, 2000, 4000, 8000, 16000):
    regs = [str(190000000 + i) for i in range(n)]
    seen = set(); t = time.perf_counter()
    for r in regs:
        if r in seen: pass
        seen.add(r)
    ts = time.perf_counter() - t
    seen = []; t = time.perf_counter()
    for r in regs:
        if r in seen: pass
        seen.append(r)
    tl = time.perf_counter() - t
    print(f"{n:>7} | {ts*1000:>10.3f} | {tl*1000:>10.2f} | {tl/ts:7.0f}x")
