"""Task 4.3 - repaired library return logger (append mode, newlines, with, error log)."""
import logging

LOG = "returns.log"
ERROR_LOG = "errors.log"


def _setup_error_log():
    logger = logging.getLogger("library")
    if not logger.handlers:
        handler = logging.FileHandler(ERROR_LOG, mode="a", encoding="utf-8")
        handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
        logger.addHandler(handler)
        logger.setLevel(logging.ERROR)
    return logger


def save_returns(books, log_name=None):
    with open(log_name or LOG, "a", encoding="utf-8") as log:    # "a": earlier days are kept
        for b in books:
            log.write(b + "\n")                                    # one title per line


def process(day_file):
    logger = _setup_error_log()
    try:
        with open(day_file, encoding="utf-8") as f:
            books = [line.strip() for line in f if line.strip()]  # no empty trailing title
        save_returns(books)
    except FileNotFoundError:
        logger.error("day file missing: %s", day_file)
        return False
    except (PermissionError, UnicodeDecodeError, TypeError, OSError) as exc:
        logger.exception("could not process %s: %s", day_file, exc)
        return False
    return True


def save_returns_try_finally(books, log_name=None):
    """Alternative concept: manual try/finally instead of with."""
    log = open(log_name or LOG, "a", encoding="utf-8")
    try:
        for b in books:
            log.write(b + "\n")
    finally:
        log.close()
