import reader, stats, report

if __name__ == "__main__":
    import sys
    folder = sys.argv[1] if len(sys.argv) > 1 else "data"
    out = sys.argv[2] if len(sys.argv) > 2 else "output_c"
    records, errors = reader.read_folder(folder)
    pcts = stats.percentages(records)
    report.write_all(out, pcts, stats.below(pcts), errors, stats.consecutive_absent(records))
    print("organisation (c): reports written to", out, "-", len(pcts), "students,", len(errors), "damaged lines")
