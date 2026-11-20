"""Task 6 Stage 5 - demonstration on the sample data (clean lines, duplicate, bad e-mail, damaged line, missing file)."""
from fest.main import run

print("result:", run("data", "output"))
for name in ("summary.txt", "errors.log", "master_list.csv"):
    print(f"\n--- output/{name} ---")
    print(open(f"output/{name}", encoding="utf-8").read(), end="")
