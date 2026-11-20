"""Task 5 analysis: one-time import cost, caching in sys.modules, namespace forms. Real measurements."""
import sys, time, importlib, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "d_package"))

t = time.perf_counter(); import attendance.stats; first = time.perf_counter() - t
t = time.perf_counter(); import attendance.stats; second = time.perf_counter() - t
print(f"first import of attendance.stats (loads package + sub-module): {first*1e6:8.1f} us")
print(f"second import (found in sys.modules cache):                    {second*1e6:8.1f} us")
print("in sys.modules:", [m for m in sys.modules if m.startswith("attendance")])

import attendance.stats                      # name bound: attendance
from attendance import stats                 # name bound: stats
from attendance.stats import percentage      # name bound: percentage
print("form 1 call: attendance.stats.percentage(3, 4) =", attendance.stats.percentage(3, 4))
print("form 2 call: stats.percentage(3, 4)            =", stats.percentage(3, 4))
print("form 3 call: percentage(3, 4)                  =", percentage(3, 4))
print("all three refer to the same function object:", attendance.stats.percentage is stats.percentage is percentage)
