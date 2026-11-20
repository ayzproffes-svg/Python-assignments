"""Q7 - Contact Merging from First Principles (M Ayaan, 1965260137)"""
import random, re, sys, time

TITLES = {"dr", "mr", "mrs", "ms", "prof", "sri", "smt"}

def norm_number(raw):
    """keep digits; use the last 10 digits (drops +91 / 0 / spaces / dashes). None if < 10 digits."""
    d = re.sub(r"\D", "", raw or "")
    return d[-10:] if len(d) >= 10 else None

def norm_name(raw):
    parts = re.findall(r"[a-z]+", (raw or "").lower())
    return " ".join(p for p in parts if p not in TITLES)

def norm_email(raw):
    return (raw or "").strip().lower() or None

# ---------- dictionary (hash) based merge with union-find over numbers/e-mails ----------
def merge_contacts(contacts):
    """contacts: list of dicts {name, numbers:[...], emails:[...]}.  Two contacts are the SAME person when
    they share a normalised number or e-mail.  Returns list of merged people."""
    parent = {}
    def find(k):
        while parent[k] != k:
            parent[k] = parent[parent[k]]; k = parent[k]
        return k
    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb: parent[rb] = ra
    key_of = {}                                    # contact index -> one key of that contact
    for i, c in enumerate(contacts):
        keys = [("n", n) for n in map(norm_number, c.get("numbers", [])) if n] + \
               [("e", e) for e in map(norm_email, c.get("emails", [])) if e]
        if not keys:                               # missing number and e-mail: fall back to name
            keys = [("m", norm_name(c.get("name")) or f"#{i}")]
        for k in keys:
            parent.setdefault(k, k)
        for k in keys[1:]:
            union(keys[0], k)
        key_of[i] = keys[0]
    people = {}
    for i, c in enumerate(contacts):
        p = people.setdefault(find(key_of[i]), {"names": set(), "numbers": set(), "emails": set()})
        nm = norm_name(c.get("name"))
        if nm: p["names"].add(nm)
        p["numbers"].update(n for n in map(norm_number, c.get("numbers", [])) if n)
        p["emails"].update(e for e in map(norm_email, c.get("emails", [])) if e)
    return list(people.values())

# ---------- brute force: compare every pair ----------
def merge_pairwise(contacts):
    data = []
    for c in contacts:
        data.append(({n for n in map(norm_number, c.get("numbers", [])) if n} | {e for e in map(norm_email, c.get("emails", [])) if e},
                     norm_name(c.get("name"))))
    n = len(data); group = list(range(n))
    def find(x):
        while group[x] != x: group[x] = group[group[x]]; x = group[x]
        return x
    for i in range(n):
        for j in range(i + 1, n):
            if data[i][0] & data[j][0]:
                group[find(j)] = find(i)
    return len({find(i) for i in range(n)})

def gen(n, seed=21, dup=0.4):
    random.seed(seed)
    base = max(1, int(n * (1 - dup)))
    people = [(f"person{i}", "98" + f"{random.randint(0, 10**8-1):08d}") for i in range(base)]
    fmts = [lambda x: x, lambda x: "+91 " + x[:5] + " " + x[5:], lambda x: "0" + x, lambda x: x[:3] + "-" + x[3:]]
    out = []
    for i in range(n):
        name, num = people[i] if i < base else random.choice(people)
        c = {"name": random.choice(["Dr. ", "", "mr "]) + name, "numbers": [random.choice(fmts)(num)]}
        if random.random() < 0.3: c["emails"] = [f"{name}@mail.com".upper()]
        out.append(c)
    return out, base

def best(f, rep=1):
    b = 1e9
    for _ in range(rep):
        s = time.perf_counter(); f(); b = min(b, time.perf_counter() - s)
    return b

if __name__ == "__main__":
    print("norm_number:", [norm_number(x) for x in ("+91 98400 12345", "9840012345", "098400-12345", "12345", "")])
    print("norm_name  :", [norm_name(x) for x in ("Dr. Ravi", "ravi kumar", "  RAVI   Kumar ", None)])
    sample = [
        {"name": "Dr. Ravi", "numbers": ["+91 98400 12345"]},
        {"name": "ravi kumar", "numbers": ["9840012345"], "emails": ["Ravi@Mail.com"]},
        {"name": "Ravi K", "numbers": ["98400-12345", "044 2345 6789"]},
        {"name": "Meena", "numbers": ["+91 90030 55555"]},
        {"name": "Meena S", "emails": ["meena.s@x.in"]},
        {"name": "Ravi Kumar", "numbers": ["+91 99999 11111"]},    # same name, different person
        {"name": "Anu", "numbers": []},                            # missing fields
        {"name": "Anu", "numbers": []},
        {"name": "Meena", "numbers": ["90030 55555"], "emails": ["meena.s@x.in"]},   # links two Meena entries
    ]
    merged = merge_contacts(sample)
    print("input contacts:", len(sample), "-> merged people:", len(merged))
    for p in sorted(merged, key=lambda p: sorted(p["names"])):
        print("  ", sorted(p["names"]), sorted(p["numbers"]), sorted(p["emails"]))
    with_keys = [c for c in sample if c.get("numbers") or c.get("emails")]
    print("pairwise people (contacts with a number/e-mail only):", merge_pairwise(with_keys), "| dict merge for same contacts:", len(merge_contacts(with_keys)))
    print("--- empty / bad input ---")
    print("empty list:", merge_contacts([]), "| all missing:", len(merge_contacts([{"name": ""}, {}])))
    print("--- timing ---")
    print("n | people (expected) | dict merge s | pairwise s")
    for n in (1000, 5000, 100000):
        data, base = gen(n)
        t1 = best(lambda: merge_contacts(data)); got = len(merge_contacts(data))
        if n <= 5000:
            t2 = best(lambda: merge_pairwise(data)); same = merge_pairwise(data) == got
            print(f"{n} | {got} ({base}) | {t1:.4f} | {t2:.4f} | equal={same}")
        else:
            est = best(lambda: merge_pairwise(data[:1000])) * (n / 1000) ** 2
            print(f"{n} | {got} ({base}) | {t1:.4f} | ~{est:.0f} (extrapolated, n^2)")
