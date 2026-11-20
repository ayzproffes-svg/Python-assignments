from pathlib import Path


def write_master(path, records):
    with open(path, "w", encoding="utf-8") as f:
        f.write("reg_no,name,dept,email,events\n")
        for r in records:
            f.write(f"{r['reg']},{r['name']},{r['dept']},{r['email']},{';'.join(r['events'])}\n")


def write_event_files(folder, records):
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    by_event = {}
    for r in records:
        for e in r["events"]:
            by_event.setdefault(e, []).append(r)
    for event, people in by_event.items():
        with open(folder / f"{event.replace(' ', '_')}.txt", "w", encoding="utf-8") as f:
            for p in people:
                f.write(f"{p['reg']},{p['name']},{p['dept']}\n")
    return {e: len(p) for e, p in by_event.items()}


def write_summary(path, total_lines, accepted, duplicates, invalid, missing, per_event):
    with open(path, "w", encoding="utf-8") as f:
        f.write("FEST REGISTRATION SUMMARY\n")
        f.write(f"lines read      : {total_lines}\n")
        f.write(f"accepted        : {accepted}\n")
        f.write(f"duplicates      : {duplicates}\n")
        f.write(f"invalid/damaged : {invalid}\n")
        f.write(f"missing files   : {', '.join(missing) if missing else 'none'}\n")
        f.write("participants per event:\n")
        for e in sorted(per_event):
            f.write(f"  {e}: {per_event[e]}\n")


def write_errors(path, errors):
    with open(path, "w", encoding="utf-8") as f:
        for source, line_no, msg in errors:
            f.write(f"{source}:{line_no}: {msg}\n")
