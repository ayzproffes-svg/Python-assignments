# The ORIGINAL poor script (kept only to demonstrate its defects). Do not reuse.
import sys
filename = sys.argv[1] if len(sys.argv) > 1 else "mess_oct.txt"   # path made a parameter only so it can be run here
f = open(filename)
data = f.read()
total = 0
report = ""
for line in data.split("\n"):
    try:
        parts = line.split(",")
        total = total + int(parts[2])
        report = report + parts[1] + " " + parts[2] + "\n"
    except:
        pass
print(report)
print("Total", total)
