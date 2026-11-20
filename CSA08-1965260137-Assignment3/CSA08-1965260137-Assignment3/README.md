# CSA08-1965260137-Assignment3

| | |
|---|---|
| **Name** | M Ayaan |
| **Register number** | 1965260137 |
| **Course** | CSA0809 - Python Programming |
| **Assignment** | Assignment 3 - CO3: Python data structures (lists, tuples, dictionaries, sets, comprehensions) |
| **Python version** | Python 3.12 |
| **Libraries** | Standard library only (`random`, `time`, `sys`, `copy`, `re`, `collections`) - see `requirements.txt` |

## How to run
From the repository root: `python3 Qn/<file>.py` (or `sh run_all.sh` to run everything).
Each program prints its results; the saved console output is in the `output*.txt` file beside it.

| Task | Command | Result (short note) |
|---|---|---|
| Q1 Lists and slicing | `python3 Q1/rainfall.py` | Weekly totals, max/min, 7-day moving average (naive = running sum), 208 dry days; running sum about 3x faster than naive. |
| Q2 Tuples, mutability, copying | `python3 Q2/complete_the_code.py` and `python3 Q2/tuples_copying.py` | Shared-row bug reproduced and fixed; expected output matched; list as dict key raises `TypeError: unhashable type`. |
| Q3 Dictionaries | `python3 Q3/complete_the_code.py` and `python3 Q3/helpline.py` | Output `[('seeds', 3), ('price', 2), ('received', 2)]` matched; dict and Counter fastest. |
| Q4 Sets | `python3 Q4/complete_the_code.py` and `python3 Q4/electives.py` | Expected output matched; set `&` and set lookup are orders of magnitude faster than loops / list lookup. |
| Q5 List comprehension | `python3 Q5/sensor.py` | Loop, comprehension and map/filter give identical results; generator uses 208 bytes. |
| Q6 Nested data | `python3 Q6/timetable.py` | 5-train timetable, station queries; the station index is faster at every size. |
| Q7 Contact merging | `python3 Q7/contacts.py` | Dictionary/union-find merge is O(n); pairwise comparison is O(n^2). |

## Folder structure
`Q1` ... `Q7` - one folder per task, each with the source file(s) and the saved console output (`output.txt`).
Output screenshots can be added to each folder as `screenshot.png`.

## Commit plan
One commit per task (`Add Q1 ...`, `Add Q2 ...` ... `Add Q7 ...`), then README/requirements.
