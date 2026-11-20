"""Task 1.2 - repaired mess-bill totaller."""
import sys
from decimal import Decimal, InvalidOperation


def total_mess_bills(filename):
    """Return (total, report_lines, rejected) for a mess-bill file.

    Each line: register number, name, amount.  Bad lines are never lost:
    they are returned in `rejected` as (line_number, text, reason).
    """
    total = Decimal("0.00")
    report_lines = []          # list + join is O(n); repeated '+' on str is not
    rejected = []
    with open(filename, encoding="utf-8") as f:      # always closed
        for line_no, line in enumerate(f, start=1):   # one line in memory at a time
            line = line.strip()
            if not line:                              # trailing / blank line is not an error
                continue
            parts = [p.strip() for p in line.split(",")]
            try:
                if len(parts) != 3:
                    raise ValueError(f"expected 3 fields, found {len(parts)}")
                amount = Decimal(parts[2])            # keeps paise exactly (1250.50)
                if amount < 0:
                    raise ValueError("negative amount")
            except (ValueError, InvalidOperation) as exc:
                reason = "amount is not a number" if isinstance(exc, InvalidOperation) else str(exc)
                rejected.append((line_no, line, reason))
                continue
            total += amount
            report_lines.append(f"{parts[1]} {amount:.2f}")
    return total, report_lines, rejected


def main(filename):
    try:
        total, report_lines, rejected = total_mess_bills(filename)
    except FileNotFoundError:
        print(f"File not found: {filename}")
        return 1
    except PermissionError:
        print(f"No permission to read: {filename}")
        return 1
    except UnicodeDecodeError as exc:
        print(f"File is not valid UTF-8: {exc}")
        return 1
    print("\n".join(report_lines))
    print("Total", total)
    if rejected:
        print(f"\n{len(rejected)} line(s) rejected:")
        for line_no, text, reason in rejected:
            print(f"  line {line_no}: {text!r} -> {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else "mess_oct.txt"))
