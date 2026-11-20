"""Task 3.4 - what happens when specific excepts are replaced with 'except Exception: pass'."""
import os, tempfile

def count_present_misused(path):
    present = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip().endswith("P"):
                    presnt += 1            # <-- typing error in the variable name
    except Exception:
        pass
    return present

def count_present_correct(path):
    present = 0
    try:
        with open(path, encoding="utf-8") as f:
            for line in f:
                if line.strip().endswith("P"):
                    presnt += 1            # same typo, specific handler only
    except FileNotFoundError:
        print("missing file")
    return present

tmp = tempfile.NamedTemporaryFile("w", suffix=".csv", delete=False)
tmp.write("1,2026-10-08,P\n2,2026-10-08,P\n3,2026-10-08,A\n"); tmp.close()
print("Misused version returns:", count_present_misused(tmp.name), "(true answer is 2, no error shown!)")
print("Version with specific except:")
try:
    print(count_present_correct(tmp.name))
except UnboundLocalError as e:
    print("  UnboundLocalError (a NameError subclass):", e)
os.remove(tmp.name)
