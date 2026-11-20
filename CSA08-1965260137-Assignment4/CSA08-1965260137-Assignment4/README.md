# CSA08 – Assignment 4 (File Handling, Modules and Packages)

| | |
|---|---|
| **Name** | M Ayaan |
| **Register Number** | 1965260137 |
| **Course** | CSA0809 – Python Programming |
| **Course Outcome** | CO4 |
| **Python version** | Python 3.12 |
| **Libraries** | Python standard library only (see `requirements.txt`) – no third-party packages |

## Folder layout and how to run (run each command from inside the task folder)

| Task | Folder | Command(s) | Result in one line |
|---|---|---|---|
| 1 | `Task01/` | `python mess_bill.py` · `python original_script.py` · `python bench_task1.py` | Repaired script totals 5151.50 and rejects 3 bad lines; the original silently gave 1250. |
| 2 | `Task02/` | `python process_month.py data_oct output` · `python bench_task2.py` | Attendance % per student, one student below 75%, 2 damaged lines logged. |
| 3 | `Task03/` | `python complete_code.py` · `python attendance_processor.py` · `python misuse_experiment.py` · `python bench_eafp_lbyl.py` | Output matches the expected tuple; misuse experiment hides a typo. |
| 4 | `Task04/` | `python test_defects.py` · `python test_fixed.py` | Defects demonstrated; fixed version appends, adds newlines, closes files, logs errors. |
| 5 | `Task05/` | `python a_single_script/attendance_all.py data output_a` · `cd b_one_module && python main_b.py ../data ../output_b` · `cd c_three_modules && python main_c.py ../data ../output_c` · `cd d_package && python main_d.py ../data ../output_d` · `python import_cost.py` | Four organisations give identical reports, incl. the new 3-day-absence report. |
| 6 | `Task06/` | `python demo.py` · `python test_fest.py` · `python bench_task6.py` | 10 lines read: 6 accepted, 1 duplicate, 3 invalid, 1 missing department file – no crash. |

`bash run_all.sh` runs everything and stores the console output in `Outputs/`.

Screenshots of each run can be added to each task folder (`screenshot_*.png`).
