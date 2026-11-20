"""Q6 - Nested Data: A Railway Timetable (M Ayaan, 1965260137)"""
import random, sys, time

DAYS = {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}

timetable = {
 "12615": {"name": "Grand Trunk Express", "stops": [("Chennai Central", "-", "18:35"), ("Katpadi", "20:48", "20:50"), ("Vijayawada", "01:05", "01:15"), ("Nagpur", "10:20", "10:30"), ("New Delhi", "06:35", "-")], "days": {"Mon", "Wed", "Fri"}},
 "12007": {"name": "Shatabdi Express", "stops": [("Chennai Central", "-", "06:00"), ("Katpadi", "07:43", "07:45"), ("Bengaluru", "11:00", "-")], "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"}},
 "12627": {"name": "Karnataka Express", "stops": [("Bengaluru", "-", "19:20"), ("Katpadi", "22:03", "22:05"), ("Chennai Central", "23:30", "-")], "days": {"Tue", "Thu", "Sat"}},
 "12639": {"name": "Brindavan Express", "stops": [("Chennai Central", "-", "07:50"), ("Arakkonam", "08:50", "08:52"), ("Katpadi", "09:50", "09:55"), ("Bengaluru", "13:25", "-")], "days": {"Mon", "Tue", "Wed", "Thu", "Fri", "Sat"}},
 "12163": {"name": "Dadar Express", "stops": [("Chennai Central", "-", "20:10"), ("Katpadi", "22:15", "22:20"), ("Mumbai Dadar", "16:00", "-")], "days": {"Sun", "Wed"}},
}

def trains_at(tt, station, day):
    out = []
    for no, t in tt.items():
        if day in t["days"]:
            for s, arr, dep in t["stops"]:
                if s == station:
                    out.append((no, t["name"], arr, dep)); break
    return out

def by_departure(rows):
    return sorted(rows, key=lambda r: (r[3] == "-", r[3]))   # "-" (terminating) last

def build_index(tt):
    idx = {}
    for no, t in tt.items():
        for s, arr, dep in t["stops"]:
            idx.setdefault(s, []).append(no)
    return idx

def trains_at_indexed(tt, idx, station, day):
    out = []
    for no in idx.get(station, []):
        t = tt[no]
        if day in t["days"]:
            for s, arr, dep in t["stops"]:
                if s == station:
                    out.append((no, t["name"], arr, dep)); break
    return out

def gen(n, nst=300, seed=11):
    random.seed(seed)
    stations = [f"Station{i:03d}" for i in range(nst)]
    d = {}
    for i in range(n):
        route = random.sample(stations, 8)
        h = random.randint(0, 20) * 60
        stops = [(s, f"{(h+k*60)//60%24:02d}:{(h+k*60)%60:02d}", f"{(h+k*60+5)//60%24:02d}:{(h+k*60+5)%60:02d}") for k, s in enumerate(route)]
        d[str(10000 + i)] = {"name": f"Train {i}", "stops": stops, "days": set(random.sample(sorted(DAYS), random.randint(2, 7)))}
    return d

def best(f, rep=3):
    b = 1e9
    for _ in range(rep):
        s = time.perf_counter(); f(); b = min(b, time.perf_counter() - s)
    return b

if __name__ == "__main__":
    print("%-8s %-22s %-6s  %s" % ("No.", "Name", "Days", "Route (station arr/dep)"))
    for no, t in timetable.items():
        print("%-8s %-22s %-6d  %s" % (no, t["name"], len(t["days"]), " > ".join(f"{s} {a}/{d}" for s, a, d in t["stops"])))
    print("third station departure of 12615:", timetable["12615"]["stops"][2][2])
    print("--- Katpadi on Wed, sorted by departure ---")
    for r in by_departure(trains_at(timetable, "Katpadi", "Wed")): print(" ", r)
    idx = build_index(timetable)
    print("indexed result equal:", by_departure(trains_at_indexed(timetable, idx, "Katpadi", "Wed")) == by_departure(trains_at(timetable, "Katpadi", "Wed")))
    print("--- edge cases ---")
    print("unknown station:", trains_at(timetable, "Atlantis", "Mon"), trains_at_indexed(timetable, idx, "Atlantis", "Mon"))
    print("train not running (Dadar Express, Mon at Katpadi):", [r for r in trains_at(timetable, "Katpadi", "Mon") if r[0] == "12163"])
    print("--- timing: 200 queries, seconds per query ---")
    print("trains | total stops | no index | with index | index memory (bytes)")
    for n in (100, 1000, 10000):
        tt = gen(n); ix = build_index(tt)
        stns = [f"Station{i:03d}" for i in range(0, 300, 3)][:100] * 2
        t1 = best(lambda: [trains_at(tt, s, "Wed") for s in stns], rep=1) / len(stns)
        t2 = best(lambda: [trains_at_indexed(tt, ix, s, "Wed") for s in stns]) / len(stns)
        mem = sys.getsizeof(ix) + sum(sys.getsizeof(v) for v in ix.values())
        assert all(trains_at(tt, s, "Wed") == trains_at_indexed(tt, ix, s, "Wed") or
                   sorted(trains_at(tt, s, "Wed")) == sorted(trains_at_indexed(tt, ix, s, "Wed")) for s in stns[:20])
        print(f"{n} | {n*8} | {t1:.7f} | {t2:.7f} | {mem}")
    print("--- alternative: flat list of tuples, scanned per query ---")
    tt = gen(10000)
    flat = [(no, s, a, d, t["days"]) for no, t in tt.items() for s, a, d in t["stops"]]
    t3 = best(lambda: [r for r in flat if r[1] == "Station003" and "Wed" in r[4]], rep=3)
    print(f"flat list of {len(flat)} stops, one query: {t3:.6f} s | list memory {sys.getsizeof(flat)} bytes (outer only)")
