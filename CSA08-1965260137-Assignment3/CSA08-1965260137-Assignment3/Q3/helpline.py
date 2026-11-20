"""Q3 - Dictionaries: Farmer Helpline Complaint Analysis (M Ayaan, 1965260137)"""
import random, re, time
from collections import Counter

STOP = {"not", "high", "the", "is", "a", "of", "and", "to", "in", "for", "my", "has", "have", "since", "was"}

def words(text):
    return re.findall(r"[a-z']+", text.lower())      # lower-case, strip punctuation

def freq_get(texts, stop=STOP):
    c = {}
    for t in texts:
        for w in words(t):
            if w not in stop:
                c[w] = c.get(w, 0) + 1
    return c

def freq_setdefault(texts, stop=STOP):
    c = {}
    for t in texts:
        for w in words(t):
            if w not in stop:
                c.setdefault(w, [0])[0] += 1
    return {k: v[0] for k, v in c.items()}

def freq_listcount(texts, stop=STOP):
    allw = [w for t in texts for w in words(t) if w not in stop]
    return {w: allw.count(w) for w in set(allw)}      # list.count for each distinct word

def freq_counter(texts, stop=STOP):
    return Counter(w for t in texts for w in words(t) if w not in stop)

def top(counts, k):
    return sorted(counts.items(), key=lambda p: (-p[1], p[0]))[:k]

def by_district(records):
    g = {}
    for district, text, crop in records:
        g.setdefault(district, []).append(text)
    return g

def by_crop(records):
    g = {}
    for district, text, crop in records:
        g.setdefault(crop, []).append(text)
    return g

VOCAB = ["seeds", "fertiliser", "price", "subsidy", "received", "delayed", "pest", "water", "loan", "insurance",
         "harvest", "market", "tractor", "drought", "credit", "rain", "storage", "transport", "quality", "shortage"] + \
        [f"term{i}" for i in range(180)]      # 200 distinct words overall
DISTRICTS = ["Chennai", "Madurai", "Salem", "Erode", "Thanjavur", "Coimbatore"]
CROPS = ["paddy", "cotton", "sugarcane", "groundnut", "maize"]

def gen(n, seed=7):
    random.seed(seed)
    fillers = ["not", "high", "the", "is"]
    return [" ".join(random.choice(VOCAB + fillers) for _ in range(8)) for _ in range(n)]

def best(f, *a, rep=3):
    b = 1e9
    for _ in range(rep):
        s = time.perf_counter(); f(*a); b = min(b, time.perf_counter() - s)
    return b

if __name__ == "__main__":
    calls = ["seeds not received seeds delayed", "fertiliser price high", "seeds price high subsidy not received"]
    print("top 3:", top(freq_get(calls, {"not", "high"}), 3))
    print("get == setdefault == Counter == list.count:",
          freq_get(calls) == freq_setdefault(calls) == dict(freq_counter(calls)) == freq_listcount(calls))
    print("--- edge cases ---")
    print("empty text:", freq_get([""]), "| no texts:", freq_get([]))
    print("case:", freq_get(["Seeds SEEDS seeds"]))
    print("punctuation:", freq_get(["Seeds, seeds! (seeds)."]))
    print("--- grouping ---")
    recs = [("Salem", "seeds late", "paddy"), ("Erode", "pest attack", "cotton"),
            ("Salem", "price low", "cotton"), ("Madurai", "loan delay", "paddy")]
    print("per district:", {k: len(v) for k, v in by_district(recs).items()})
    print("per crop    :", by_crop(recs))
    print("--- views ---")
    d = {"a": 1, "b": 2}
    kv, vv, iv = d.keys(), d.values(), d.items()
    d["c"] = 3
    print("keys():", kv, "| values():", vv, "| items():", iv, "(views are live)")
    print("--- timing (best of 3, seconds) ---")
    print("n | dict.get | setdefault | list.count | Counter")
    for n in (1000, 10000, 100000):
        t = gen(n)
        res = [best(f, t) if not (f is freq_listcount and n > 10000) else best(f, t, rep=1)
               for f in (freq_get, freq_setdefault, freq_listcount, freq_counter)]
        print(f"{n} | " + " | ".join(f"{x:.4f}" for x in res))
