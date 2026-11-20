"""Q2 - Tuples, Mutability and Copying (M Ayaan, 1965260137)"""
import copy, sys, time

stops = {(13.0827, 80.2707): "Chennai Central", (13.0418, 80.2341): "T. Nagar",
         (13.0732, 80.2609): "Egmore", (12.9941, 80.1709): "Chromepet"}
print("1. Tuple keys:", stops[(13.0732, 80.2609)])
for (lat, lon), name in stops.items():          # tuple unpacking in a for loop
    print(f"   {name:16s} lat={lat:.4f} lon={lon:.4f}")

rows, cols = 3, 3
bad = [[0] * cols] * rows
good = [[0 for _ in range(cols)] for _ in range(rows)]
bad[0][0] = 5; good[0][0] = 5
print("2. bad :", bad, "| ids of rows:", [id(r) % 10**5 for r in bad], "| bad[0] is bad[1]:", bad[0] is bad[1])
print("   good:", good, "| ids of rows:", [id(r) % 10**5 for r in good], "| good[0] is good[1]:", good[0] is good[1])

print("3. Aliasing / shallow / deep copy")
orig = [[1, 2], [3, 4]]
alias = orig; sh1 = copy.copy(orig); sh2 = orig[:]; deep = copy.deepcopy(orig)
orig[0][0] = 99; orig.append([5, 6])
print("   orig  :", orig)
print("   alias :", alias, "(same object:", alias is orig, ")")
print("   copy.copy  :", sh1, "(inner shared:", sh1[0] is orig[0], ")")
print("   slice [:]  :", sh2, "(inner shared:", sh2[0] is orig[0], ")")
print("   deepcopy   :", deep, "(inner shared:", deep[0] is orig[0], ")")

def add_stop(lst):       # function mutating its argument
    lst.append("New Stop")
def rebind(lst):         # rebinding does not affect the caller
    lst = ["x"]
caller = ["A", "B"]; add_stop(caller); rebind(caller)
print("4. After add_stop + rebind, caller's list:", caller)

print("5. Tuple containing a list")
t = (1, [10, 20])
try:
    t[0] = 2
except TypeError as e:
    print("   t[0]=2 ->", "TypeError:", e)
t[1].append(30)
print("   t[1].append(30) works ->", t)
try:
    t[1] += [40]
except TypeError as e:
    print("   t[1] += [40] -> TypeError:", e, "| but t is now", t)

print("6. Memory with sys.getsizeof (1,000,000 values)")
L = list(range(1_000_000)); T = tuple(L)
print("   list :", sys.getsizeof(L), "bytes | tuple:", sys.getsizeof(T), "bytes")
print("   empty list", sys.getsizeof([]), "| empty tuple", sys.getsizeof(()))

def best(f, rep=5):
    b = 1e9
    for _ in range(rep):
        s = time.perf_counter(); f(); b = min(b, time.perf_counter() - s)
    return b
print("7. Timing (best of 5, seconds)")
print("   create list(range(1e6)) :", f"{best(lambda: list(range(1_000_000))):.6f}")
print("   create tuple(range(1e6)):", f"{best(lambda: tuple(range(1_000_000))):.6f}")
def idx(c):
    def f():
        for i in range(0, 1_000_000, 10):
            c[i]
    return f
print("   index 100,000 times list :", f"{best(idx(L)):.6f}")
print("   index 100,000 times tuple:", f"{best(idx(T)):.6f}")

print("8. Alternative: sparse dict grid")
sparse = {}
for r, c in [(0, 1), (0, 1), (2, 2)]:
    sparse[(r, c)] = sparse.get((r, c), 0) + 1
print("  ", sparse, "| size grid 1000x1000 list-of-lists:",
      sys.getsizeof([[0]*1000 for _ in range(1000)]) + 1000*sys.getsizeof([0]*1000), "bytes (outer+rows) vs dict of 3 entries:", sys.getsizeof(sparse), "bytes")
