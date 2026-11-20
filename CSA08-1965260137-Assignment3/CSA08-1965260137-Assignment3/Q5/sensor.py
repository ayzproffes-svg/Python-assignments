"""Q5 - List Comprehension: Cleaning Sensor Readings (M Ayaan, 1965260137)"""
import random, sys, time

def clean_loop(raw):
    c, f = [], []
    for x in raw:
        if -50 <= x <= 50:
            c.append(x); f.append(x * 9 / 5 + 32)
    return c, f

def clean_comp(raw):
    c = [x for x in raw if -50 <= x <= 50]
    return c, [x * 9 / 5 + 32 for x in c]

def clean_mapfilter(raw):
    c = list(filter(lambda x: -50 <= x <= 50, raw))
    return c, list(map(lambda x: x * 9 / 5 + 32, c))

def alarm_minutes(raw):
    return [i for i, x in enumerate(raw) if -50 <= x <= 50 and not 2 <= x <= 8]

def gen(n, seed=5, bad=0.05):
    random.seed(seed)
    return [round(random.uniform(60, 99), 1) if random.random() < bad else round(random.gauss(5, 2.5), 1) for _ in range(n)]

def best(f, *a, rep=3):
    b = 1e9
    for _ in range(rep):
        s = time.perf_counter(); f(*a); b = min(b, time.perf_counter() - s)
    return b

if __name__ == "__main__":
    raw = [4.5, 3.9, 99.9, 6.1, -120.0, 9.2, 1.0, 7.8, 2.0]
    print("raw:", raw)
    print("loop      :", clean_loop(raw)); print("comp      :", clean_comp(raw)); print("map/filter:", clean_mapfilter(raw))
    print("alarm minutes (enumerate):", alarm_minutes(raw))
    print("identical:", clean_loop(raw) == clean_comp(raw) == clean_mapfilter(raw))
    print("dict comp  :", {i: x for i, x in enumerate(raw) if -50 <= x <= 50})
    print("set comp   :", {x for x in raw if -50 <= x <= 50 and not 2 <= x <= 8})
    print("--- edge cases ---")
    ok = [5.0] * 6; badd = [100.0, -80.0, 75.5]
    print("all valid  :", clean_comp(ok)[0] == ok, "| alarm", alarm_minutes(ok))
    print("all invalid:", clean_comp(badd), clean_loop(badd) == clean_comp(badd) == clean_mapfilter(badd))
    print("--- timing (best of 3, seconds) ---")
    print("n | loop+append | comprehension | map+filter")
    for n in (10_000, 100_000, 1_000_000):
        r = gen(n)
        assert clean_loop(r) == clean_comp(r) == clean_mapfilter(r)
        print(f"{n} | {best(clean_loop, r):.5f} | {best(clean_comp, r):.5f} | {best(clean_mapfilter, r):.5f}")
    print("--- memory (sys.getsizeof) ---")
    for n in (10_000, 1_000_000):
        r = gen(n)
        lc = [x for x in r if -50 <= x <= 50]; ge = (x for x in r if -50 <= x <= 50)
        print(f"n={n}: list comp {sys.getsizeof(lc)} bytes | generator {sys.getsizeof(ge)} bytes")
    r = gen(1_000_000)
    t_sum_list = best(lambda: sum([c for c in r if -50 <= c <= 50]))
    t_sum_gen = best(lambda: sum(c for c in r if -50 <= c <= 50))
    print(f"sum over 1,000,000: list {t_sum_list:.5f} s | generator {t_sum_gen:.5f} s | equal={sum([c for c in r if -50<=c<=50])==sum(c for c in r if -50<=c<=50)}")
