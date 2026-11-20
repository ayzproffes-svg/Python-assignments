#!/bin/sh
# Run once after `git init` and adding your remote; makes one commit per task.
git add README.md requirements.txt run_all.sh && git commit -m "Add README, requirements and run script"
for q in Q1 Q2 Q3 Q4 Q5 Q6 Q7; do git add $q && git commit -m "Add $q solution, output and notes"; done
echo "Now: git branch -M main && git remote add origin <your-repo-url> && git push -u origin main"
