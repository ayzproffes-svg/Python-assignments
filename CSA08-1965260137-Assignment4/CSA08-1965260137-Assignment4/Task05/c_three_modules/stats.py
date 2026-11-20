def percentage(present, total):
    return round(100 * present / total, 2) if total else 0.0


def percentages(records):
    counts = {}
    for reg, _, status in records:
        c = counts.setdefault(reg, [0, 0])
        c[1] += 1
        c[0] += status == "P"
    return {reg: percentage(p, t) for reg, (p, t) in counts.items()}


def below(pcts, limit=75.0):
    return {r: p for r, p in pcts.items() if p < limit}


def consecutive_absent(records, run=3):
    """Students with `run` or more consecutive recorded days marked A (NEW report, Task 5.2)."""
    by_student = {}
    for reg, date, status in sorted(records, key=lambda r: (r[0], r[1])):
        by_student.setdefault(reg, []).append(status)
    result = []
    for reg, statuses in by_student.items():
        streak = best = 0
        for s in statuses:
            streak = streak + 1 if s == "A" else 0
            best = max(best, streak)
        if best >= run:
            result.append((reg, best))
    return sorted(result)
