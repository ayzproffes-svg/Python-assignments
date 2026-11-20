"""Orchestrates reading -> validating -> de-duplicating -> writing. Never stops on a bad line or file."""
import sys
from pathlib import Path

from .exceptions import InvalidRegistration, DuplicateRegistration
from .reader import read_department_file
from .validator import parse_registration, check_duplicate
from . import writer

DEPARTMENTS = ["CSE", "ECE", "MECH", "IT", "EEE"]


def run(data_dir, out_dir, departments=DEPARTMENTS):
    data_dir, out_dir = Path(data_dir), Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    seen, accepted, errors, missing = set(), [], [], []
    total = duplicates = invalid = 0
    for dept in departments:
        path = data_dir / f"{dept}.txt"
        try:
            for line_no, line in read_department_file(path):
                total += 1
                try:
                    record = parse_registration(line)
                    check_duplicate(record, seen)
                except DuplicateRegistration as exc:
                    duplicates += 1
                    errors.append((path.name, line_no, f"DUPLICATE: {exc}"))
                except InvalidRegistration as exc:
                    invalid += 1
                    errors.append((path.name, line_no, f"INVALID: {exc}"))
                else:
                    accepted.append(record)
        except FileNotFoundError:
            missing.append(path.name)
            errors.append((path.name, 0, "MISSING FILE: department file not found"))
        except (PermissionError, UnicodeDecodeError) as exc:
            missing.append(path.name)
            errors.append((path.name, 0, f"UNREADABLE FILE: {type(exc).__name__}"))
    writer.write_master(out_dir / "master_list.csv", accepted)
    per_event = writer.write_event_files(out_dir / "events", accepted)
    writer.write_summary(out_dir / "summary.txt", total, len(accepted), duplicates, invalid, missing, per_event)
    writer.write_errors(out_dir / "errors.log", errors)
    return {"total": total, "accepted": len(accepted), "duplicates": duplicates,
            "invalid": invalid, "missing": missing}


if __name__ == "__main__":
    print(run(sys.argv[1] if len(sys.argv) > 1 else "data", sys.argv[2] if len(sys.argv) > 2 else "output"))
