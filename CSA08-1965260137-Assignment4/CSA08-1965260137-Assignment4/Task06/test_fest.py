import tempfile, unittest, os
from pathlib import Path
from fest.validator import is_valid_email, parse_registration, check_duplicate
from fest.exceptions import InvalidRegistration, DuplicateRegistration
from fest.main import run


class EmailTests(unittest.TestCase):
    def test_valid(self):
        self.assertTrue(is_valid_email("a.b@college.edu"))
    def test_invalid(self):
        for bad in ["", "no-at.college.edu", "a@@b.com", "a@b", "@b.com", "a b@c.com", "a@.com", "a@b.", "a@b.c"]:
            self.assertFalse(is_valid_email(bad), bad)


class ParseTests(unittest.TestCase):
    def test_good_line(self):
        r = parse_registration("1,Ann,cse,Ann@X.com,dance; quiz")
        self.assertEqual(r["events"], ["Dance", "Quiz"]); self.assertEqual(r["dept"], "CSE")
    def test_damaged(self):
        with self.assertRaises(InvalidRegistration): parse_registration("1,Ann,cse")
    def test_no_events(self):
        with self.assertRaises(InvalidRegistration): parse_registration("1,Ann,cse,a@x.com,")
    def test_duplicate(self):
        seen = set(); r = parse_registration("1,Ann,cse,a@x.com,Quiz")
        check_duplicate(r, seen)
        with self.assertRaises(DuplicateRegistration): check_duplicate(r, seen)


class RunTests(unittest.TestCase):
    def test_missing_and_bad_files_do_not_stop_run(self):
        d = tempfile.mkdtemp(); out = tempfile.mkdtemp()
        Path(d, "CSE.txt").write_text("1,Ann,CSE,a@x.com,Quiz\n1,Ann,CSE,a@x.com,Quiz\nxx\n")
        Path(d, "ECE.txt").write_bytes(b"\xff\xfe")
        res = run(d, out, ["CSE", "ECE", "IT"])
        self.assertEqual((res["accepted"], res["duplicates"], res["invalid"]), (1, 1, 1))
        self.assertEqual(res["missing"], ["ECE.txt", "IT.txt"])
    def test_events_files_written(self):
        d = tempfile.mkdtemp(); out = tempfile.mkdtemp()
        Path(d, "CSE.txt").write_text("1,Ann,CSE,a@x.com,Quiz;Dance\n")
        run(d, out, ["CSE"])
        self.assertTrue(Path(out, "events", "Quiz.txt").exists())

if __name__ == "__main__":
    unittest.main(verbosity=2)
