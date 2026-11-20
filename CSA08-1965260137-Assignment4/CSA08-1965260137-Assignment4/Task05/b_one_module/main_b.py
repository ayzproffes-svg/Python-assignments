from attendance_lib import read_folder, percentages, below, consecutive_absent, write_all

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "data"
    out = sys.argv[2] if len(sys.argv) > 2 else "output_b"
    records, errors = read_folder(folder)
    pcts = percentages(records)
    write_all(out, pcts, below(pcts), errors, consecutive_absent(records))
    print("organisation (b): reports written to", out, "-", len(pcts), "students,", len(errors), "damaged lines")
