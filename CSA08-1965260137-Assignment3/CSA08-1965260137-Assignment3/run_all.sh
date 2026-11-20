#!/bin/sh
# Runs every program of the assignment from the repository root
for q in Q1/rainfall.py Q2/complete_the_code.py Q2/tuples_copying.py Q3/complete_the_code.py Q3/helpline.py \
         Q4/complete_the_code.py Q4/electives.py Q5/sensor.py Q6/timetable.py Q7/contacts.py; do
  echo "=== python3 $q ==="; python3 "$q"
done
