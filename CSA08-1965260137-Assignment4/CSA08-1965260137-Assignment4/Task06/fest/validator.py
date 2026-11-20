"""Validation using string methods only (no regular expressions)."""
from .exceptions import InvalidRegistration, DuplicateRegistration


def is_valid_email(email):
    if not email or " " in email or email.count("@") != 1:
        return False
    local, domain = email.split("@")
    if not local or not domain or "." not in domain:
        return False
    if domain.startswith(".") or domain.endswith(".") or ".." in domain:
        return False
    return len(domain.rsplit(".", 1)[1]) >= 2          # top-level part has >= 2 characters


def parse_registration(line):
    """'reg,name,dept,email,ev1;ev2' -> dict. Raises InvalidRegistration."""
    parts = [p.strip() for p in line.strip().split(",")]
    if len(parts) != 5:
        raise InvalidRegistration(f"expected 5 fields, found {len(parts)}")
    reg, name, dept, email, events = parts
    if not reg.isdigit():
        raise InvalidRegistration(f"register number {reg!r} is not numeric")
    if not name:
        raise InvalidRegistration("name is empty")
    if not is_valid_email(email):
        raise InvalidRegistration(f"invalid e-mail {email!r}")
    event_list = [e.strip().title() for e in events.split(";") if e.strip()]
    if not event_list:
        raise InvalidRegistration("no events chosen")
    return {"reg": reg, "name": name, "dept": dept.upper(), "email": email.lower(), "events": event_list}


def check_duplicate(record, seen):
    """`seen` is a set of register numbers: membership test is O(1) on average."""
    if record["reg"] in seen:
        raise DuplicateRegistration(f"register number {record['reg']} already registered")
    seen.add(record["reg"])
