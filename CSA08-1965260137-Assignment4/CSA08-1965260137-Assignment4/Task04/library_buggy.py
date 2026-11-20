# The ORIGINAL defective program (as given). Paths are module variables only so tests can redirect them.
LOG = "returns.log"

def save_returns(books):
    log = open(LOG, "w")
    for b in books:
        log.write(b)
    log.close()

def process(day_file):
    try:
        books = open(day_file).read().split("\n")
        save_returns(books)
    except FileNotFoundError:
        print("missing")
