"""Task 4.2 - evidence for each defect in library_buggy.py."""
import builtins, os, tempfile
import library_buggy as lb

d = tempfile.mkdtemp()
lb.LOG = os.path.join(d, "returns.log")
days = {
    "day1.txt": "Python Crash Course\nDon Quixote\n",
    "day2.txt": "Wings of Fire\nGodan\n",
    "day3.txt": "Malgudi Days\nTwo States\n",
}
for name, text in days.items():
    with open(os.path.join(d, name), "w") as f:
        f.write(text)

print("== Defects 1 and 2: three days processed ==")
for name in days:
    lb.process(os.path.join(d, name))
print(repr(open(lb.LOG).read()))
print("-> day 1 and day 2 are gone ('w' truncates); titles are glued together (no newline written)\n")

print("== Defect 3: write() fails, what happens to the open file? ==")
opened = []
real_open = builtins.open
def spy_open(*a, **k):
    fh = real_open(*a, **k); opened.append(fh); return fh
builtins.open = spy_open
try:
    lb.save_returns(["Good Book", 12345])      # 12345 is not a str -> TypeError inside write()
except TypeError as e:
    print("TypeError escaped process():", e)
finally:
    builtins.open = real_open
print("log file closed?", opened[-1].closed, "-> the handle is left open (close() was skipped)")
opened[-1].close()

print("\n== Defect 4: an error is not recorded ==")
with real_open(os.path.join(d, "bad.txt"), "wb") as f:
    f.write(b"\xff\xfe broken")
try:
    lb.process(os.path.join(d, "bad.txt"))
except UnicodeDecodeError as e:
    print("UnicodeDecodeError crashed the program; nothing was saved to any log:", e.reason)
lb.process(os.path.join(d, "absent.txt"))
print("-> only 'missing' printed to the screen: no file name, no time, nothing saved")
