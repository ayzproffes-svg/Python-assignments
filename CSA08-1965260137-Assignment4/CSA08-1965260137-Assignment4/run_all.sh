#!/bin/bash
# Runs every program and saves its console output into Outputs/ (used as evidence in the report).
set -u
ROOT="$(cd "$(dirname "$0")" && pwd)"; O="$ROOT/Outputs"; mkdir -p "$O"
cd "$ROOT/Task01" && { echo "### original_script.py"; python3 original_script.py; echo; echo "### mess_bill.py"; python3 mess_bill.py; echo; echo "### mess_bill.py nofile.txt"; python3 mess_bill.py nofile.txt; } > "$O/task01_run.txt" 2>&1
cd "$ROOT/Task01" && python3 bench_task1.py > "$O/task01_bench.txt" 2>&1
cd "$ROOT/Task02" && { python3 process_month.py; echo "--- damaged_lines.log"; cat output/damaged_lines.log; echo "--- below_75.csv"; cat output/below_75.csv; } > "$O/task02_run.txt" 2>&1
cd "$ROOT/Task02" && python3 bench_task2.py > "$O/task02_bench.txt" 2>&1
cd "$ROOT/Task03" && python3 complete_code.py > "$O/task03_complete_code.txt" 2>&1
cd "$ROOT/Task03" && python3 attendance_processor.py 2>&1 | sed -E 's#/tmp/[^/ ]+/##g' > "$O/task03_processor.txt"
cd "$ROOT/Task03" && python3 misuse_experiment.py > "$O/task03_misuse.txt" 2>&1
cd "$ROOT/Task03" && python3 bench_eafp_lbyl.py > "$O/task03_bench.txt" 2>&1
cd "$ROOT/Task04" && python3 test_defects.py > "$O/task04_defects.txt" 2>&1
cd "$ROOT/Task04" && python3 test_fixed.py 2>&1 | sed -E 's#/tmp/[^/ ]+/##g' > "$O/task04_fixed.txt"
cd "$ROOT/Task05" && { python3 a_single_script/attendance_all.py data output_a; (cd b_one_module && python3 main_b.py ../data ../output_b); (cd c_three_modules && python3 main_c.py ../data ../output_c); (cd d_package && python3 main_d.py ../data ../output_d); for f in attendance_report.csv below_75.csv damaged_lines.log absent_3_days.csv; do for x in b c d; do cmp output_a/$f output_$x/$f && echo "$f: a == $x"; done; done; echo "--- absent_3_days.csv"; cat output_a/absent_3_days.csv; } > "$O/task05_run.txt" 2>&1
cd "$ROOT/Task05" && python3 import_cost.py > "$O/task05_import.txt" 2>&1
cd "$ROOT/Task06" && python3 demo.py > "$O/task06_demo.txt" 2>&1
cd "$ROOT/Task06" && python3 test_fest.py > "$O/task06_tests.txt" 2>&1
cd "$ROOT/Task06" && python3 bench_task6.py > "$O/task06_bench.txt" 2>&1
find "$ROOT" -name __pycache__ -type d -prune -exec rm -rf {} +
echo "Done. Outputs saved in $O"
