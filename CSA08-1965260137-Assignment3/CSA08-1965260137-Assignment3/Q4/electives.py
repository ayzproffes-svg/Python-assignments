"""Q4 - Sets: Elective Registration Clash Detection (M Ayaan, 1965260137)"""
import random, time

def clashes_nested(a, b):
    out = []
    for x in a:
        for y in b:
            if x == y:
                out.append(x); break
    return out

def clashes_sorted(a, b):
    a, b = sorted(a), sorted(b); i = j = 0; out = []
    while i < len(a) and j < len(b):
        if a[i] == b[j]: out.append(a[i]); i += 1; j += 1
        elif a[i] < b[j]: i += 1
        else: j += 1
    return out

def best(f, *args, rep=3):
    b = 1e9
    for _ in range(rep):
        s = time.perf_counter(); f(*args); b = min(b, time.perf_counter() - s)
    return b

if __name__ == "__main__":
    raw = ["192311001", "192311004", "192311004", "192311007", "192311009", "192311001"]
    print("raw list:", len(raw), "-> set:", len(set(raw)), sorted(set(raw)))
    print("--- small case (verified by hand in report) ---")
    A = {"192311001", "192311004", "192311007", "192311009"}
    B = {"192311002", "192311004", "192311009", "192311010"}
    U = {f"1923110{i:02d}" for i in range(1, 11)}
    print("A|B :", sorted(A | B)); print("A&B :", sorted(A & B))
    print("A-B :", sorted(A - B)); print("B-A :", sorted(B - A)); print("A^B :", sorted(A ^ B))
    print("none:", sorted(U - (A | B)))
    print("--- edge cases ---")
    E = set()
    print("empty A, B   : &", A & E, "| ^", sorted(A ^ E) == sorted(A), "| |", A | E == A)
    print("identical    : &", A & A == A, "| ^", A ^ A, "| -", A - A)
    print("tuples in set:", {(1, 2), (3, 4)}, "| list in set ->", end=" ")
    try:
        {[1, 2]}
    except TypeError as e:
        print("TypeError:", e)
    print("--- x in list vs x in set (worst-case element, 100 lookups, seconds) ---")
    print("n | list | set")
    for n in (10_000, 100_000, 1_000_000):
        L = [str(192300000 + i) for i in range(n)]; S = set(L)
        target = L[-1]
        reps = 100 if n <= 100_000 else 20
        tl = best(lambda: [target in L for _ in range(reps)]) / reps
        ts = best(lambda: [target in S for _ in range(reps)]) / reps
        print(f"{n} | {tl:.8f} | {ts:.10f}")
    print("--- common students: nested loops vs & (seconds) ---")
    print("n each | nested | sorted-walk | set &")
    random.seed(3)
    for n in (500, 2000, 5000):
        a = random.sample(range(10**7), n); b = random.sample(range(10**7), n)
        a += b[:n // 5]; b = b  # ensure some overlap
        sa, sb = set(a), set(b)
        tn = best(clashes_nested, a, b, rep=1); tw = best(clashes_sorted, a, b); ts = best(lambda: sa & sb)
        ok = sorted(clashes_nested(a, b)) == clashes_sorted(a, b) == sorted(sa & sb)
        print(f"{len(a)} | {tn:.5f} | {tw:.5f} | {ts:.6f} | same={ok}")
