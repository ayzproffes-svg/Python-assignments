"""Measure f.read() / readlines() vs line-by-line for 50,000 lines (real measurements)."""
import os, tempfile, time, tracemalloc, random
from mess_bill import total_mess_bills

N = 50_000
random.seed(1)
tmp = tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False, encoding="utf-8")
for i in range(N):
    tmp.write(f"19{i:07d},Student {i},{random.randint(500,2500)}.{random.choice(['00','25','50','75'])}\n")
tmp.close()
print(f"file size: {os.path.getsize(tmp.name)/1024:.0f} KB, lines: {N}")

def by_read(path):
    with open(path, encoding="utf-8") as f:
        data = f.read()
    total = 0
    for line in data.split("\n"):
        if line:
            total += float(line.split(",")[2])
    return total

def by_readlines(path):
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()
    return sum(float(l.split(",")[2]) for l in lines)

def by_iter(path):
    return total_mess_bills(path)[0]

for name, fn in [("f.read() + split", by_read), ("f.readlines()", by_readlines), ("line-by-line (mess_bill)", by_iter)]:
    t = time.perf_counter(); fn(tmp.name); elapsed = time.perf_counter() - t
    tracemalloc.start(); fn(tmp.name); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
    print(f"{name:26s} time {elapsed*1000:7.1f} ms   peak memory {peak/1024:9.0f} KB")

# pure memory cost of the reading style only (no Decimal / list of report lines)
def iter_only(path):
    n = 0
    with open(path, encoding="utf-8") as f:
        for line in f:
            n += len(line)
    return n
tracemalloc.start(); iter_only(tmp.name); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
print(f"{'iteration only (no report)':26s} peak memory {peak/1024:9.1f} KB")
os.remove(tmp.name)
