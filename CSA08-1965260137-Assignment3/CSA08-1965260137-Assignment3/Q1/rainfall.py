"""Q1 - Lists and Slicing: Daily Rainfall Records (M Ayaan, 1965260137)"""
import random, time

def weekly_totals(r):
    # slicing: a short last week is kept as its own total
    return [sum(r[i:i + 7]) for i in range(0, len(r), 7)]

def max_min(r):
    if not r:
        return None
    hi, lo = max(r), min(r)
    return (hi, r.index(hi)), (lo, r.index(lo))

def moving_avg_naive(r, w=7):
    """re-adds w values for every window: (w-1)(n-w+1) additions"""
    if len(r) < w:
        return []
    return [sum(r[i:i + w]) / w for i in range(len(r) - w + 1)]

def moving_avg_running(r, w=7):
    """running sum: w-1 additions first, then 1 add + 1 subtract per slide"""
    if len(r) < w:
        return []
    s = sum(r[:w]); out = [s / w]
    for i in range(w, len(r)):
        s += r[i] - r[i - w]
        out.append(s / w)
    return out

def dry_days(r):
    return [i for i, v in enumerate(r) if v == 0]

def make(n, seed=1):
    random.seed(seed)
    return [0.0 if random.random() < 0.55 else round(random.uniform(0.5, 60), 1) for _ in range(n)]

def best(f, *a, rep=5):
    t = float("inf")
    for _ in range(rep):
        s = time.perf_counter(); f(*a); t = min(t, time.perf_counter() - s)
    return t

if __name__ == "__main__":
    readings = make(365)
    wk = weekly_totals(readings)
    print("Weeks:", len(wk), "| first 5 totals:", [round(x, 1) for x in wk[:5]])
    full = wk[:52]
    print("Wettest week: #%d (%.1f mm)" % (full.index(max(full)) + 1, max(full)))
    print("Driest week : #%d (%.1f mm)" % (full.index(min(full)) + 1, min(full)))
    (hi, hp), (lo, lp) = max_min(readings)
    print("Max reading %.1f mm at index %d; min %.1f mm at index %d" % (hi, hp, lo, lp))
    ma = moving_avg_running(readings)
    print("Moving-average values:", len(ma), "first 3:", [round(x, 2) for x in ma[:3]])
    print("Naive == running:", all(abs(a - b) < 1e-9 for a, b in zip(ma, moving_avg_naive(readings))))
    d = dry_days(readings)
    print("Dry days:", len(d), "first 10 indices:", d[:10])
    print("readings[7:14] ->", readings[7:14])
    print("readings[-7:]  ->", readings[-7:])
    print("readings[::7]  -> %d values, first 5: %s" % (len(readings[::7]), readings[::7][:5]))
    print("--- edge cases ---")
    print("empty: weekly", weekly_totals([]), "| max_min", max_min([]), "| MA", moving_avg_running([]), "| dry", dry_days([]))
    short = [1.0, 2.0, 0.0, 4.0]
    print("short(4): weekly", weekly_totals(short), "| MA naive", moving_avg_naive(short), "| MA running", moving_avg_running(short))
    print("--- timing (best of 5, seconds) ---")
    print("n | naive_s | running_s | additions naive 6(n-6) | operations running 6+2(n-7)")
    for n in (365, 36500, 365000):
        r = make(n)
        print(f"{n} | {best(moving_avg_naive, r):.6f} | {best(moving_avg_running, r):.6f} | {6*(n-6)} | {6+2*(n-7)}")
