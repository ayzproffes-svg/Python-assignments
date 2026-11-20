import os, tempfile
import library_fixed as lf

d = tempfile.mkdtemp()
lf.LOG = os.path.join(d, "returns.log"); lf.ERROR_LOG = os.path.join(d, "errors.log")
for i, titles in enumerate(["Python Crash Course\nDon Quixote\n", "Wings of Fire\nGodan\n", "Malgudi Days\nTwo States\n"], 1):
    open(os.path.join(d, f"day{i}.txt"), "w").write(titles)
for i in (1, 2, 3):
    lf.process(os.path.join(d, f"day{i}.txt"))
open(os.path.join(d, "bad.txt"), "wb").write(b"\xff\xfe broken")
print("bad file ok?   ", lf.process(os.path.join(d, "bad.txt")))
print("missing file ok?", lf.process(os.path.join(d, "absent.txt")))
print("--- returns.log ---"); print(open(lf.LOG).read(), end="")
print("--- errors.log (first line of each entry) ---")
for line in open(lf.ERROR_LOG):
    if line[:2] == "20": print(line.rstrip())
import builtins
opened = []
real_open = builtins.open
def spy(*a, **k):
    fh = real_open(*a, **k); opened.append(fh); return fh
builtins.open = spy
for fn in (lf.save_returns, lf.save_returns_try_finally):
    try:
        fn(["Good", 5], lf.LOG)
    except TypeError:
        pass
    print(f"{fn.__name__}: write failed, file closed afterwards? {opened[-1].closed}")
builtins.open = real_open
