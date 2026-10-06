import shutil
import unittest
from unittest import mock

from journey import runners
from journey.runners import base, c

from .helpers import TempDirTestCase, make_task, write_files

HAS_CC = c.find_compiler() is not None


class ProcessRunnerTests(TempDirTestCase):
    def test_collects_output_and_status(self):
        out = base.run_process(
            ["python3", "-c", "import sys; print('hi'); sys.exit(3)"], cwd=self.tmp, timeout=5
        )
        self.assertEqual((out.stdout, out.returncode), ("hi\n", 3))

    def test_times_out(self):
        out = base.run_process(["python3", "-c", "while True: pass"], cwd=self.tmp, timeout=0.5)
        self.assertTrue(out.timed_out)

    def test_runaway_output_is_capped_and_killed(self):
        code = "import sys\nwhile True: sys.stdout.write('x' * 65536)"
        out = base.run_process(["python3", "-c", code], cwd=self.tmp, timeout=10)
        self.assertTrue(out.truncated)
        self.assertLessEqual(len(out.stdout), base.MAX_OUTPUT_BYTES)

    def test_stdin_is_delivered(self):
        out = base.run_process(
            ["python3", "-c", "print(input()[::-1])"], cwd=self.tmp, stdin="abc\n", timeout=5
        )
        self.assertEqual(out.stdout, "cba\n")

    def test_signal_names(self):
        self.assertEqual(base.signal_name(-11), "SIGSEGV")
        self.assertEqual(base.signal_name(0), "")


class SourceHelperTests(unittest.TestCase):
    def test_c_comments_are_stripped_but_strings_kept(self):
        text = 'write(1, "// not a comment", 2); // a comment\n/* block\n for */ x();'
        stripped = base.strip_c_comments(text)
        self.assertIn('"// not a comment"', stripped)
        self.assertNotIn("a comment\n", stripped.replace('"// not a comment"', ""))
        self.assertNotIn("for", stripped)

    def test_python_comments_are_stripped(self):
        stripped = base.strip_python_comments('x = 1  # while\nprint("#for")\n')
        self.assertNotIn("while", stripped)
        self.assertIn('"#for"', stripped)


class StyleTests(TempDirTestCase):
    def test_style_issues(self):
        path = self.tmp / "a.c"
        path.write_text("int x;  \n" + "y" * 90 + "\nlast line without newline")
        issues = base.style_issues([path], 80)
        self.assertEqual(len(issues), 3)
        self.assertTrue(any("trailing whitespace" in i for i in issues))
        self.assertTrue(any("longer than 80" in i for i in issues))
        self.assertTrue(any("no newline" in i for i in issues))

    def test_clean_file_has_no_issues(self):
        path = self.tmp / "a.c"
        path.write_text("int x;\n")
        self.assertEqual(base.style_issues([path], 80), [])


class PythonRunnerTests(TempDirTestCase):
    def grade(self, task, files, hidden=True):
        return runners.grade(task, write_files(self.tmp / "work", files), include_hidden=hidden)

    def test_passing_and_failing_cases(self):
        task = make_task(
            self.tmp / "pack",
            cases=[{"name": "greets", "stdin": "Ada\n", "stdout": "Hello, Ada!\n"}],
        )
        good = self.grade(task, {"sol.py": 'print(f"Hello, {input()}!")\n'})
        self.assertTrue(good.passed, good.checks)
        bad = runners.grade(
            task, write_files(self.tmp / "bad", {"sol.py": "print('Hello')\n"}), include_hidden=True
        )
        self.assertFalse(bad.passed)
        self.assertIn("expected 'Hello, Ada!\\n'", bad.checks[-1].detail)

    def test_missing_file_is_reported(self):
        task = make_task(self.tmp / "pack")
        result = self.grade(task, {"other.py": ""})
        self.assertFalse(result.passed)
        self.assertIn("missing: sol.py", result.checks[0].detail)

    def test_syntax_error_points_at_the_line(self):
        task = make_task(self.tmp / "pack")
        result = self.grade(task, {"sol.py": "print('a'\nx = = 1\n"})
        self.assertFalse(result.passed)
        self.assertEqual(result.checks[-1].name, "Syntax")

    def test_forbidden_calls_methods_and_imports(self):
        task = make_task(
            self.tmp / "pack",
            forbidden_calls=("len", ".sort"),
            forbidden_imports=("itertools",),
            cases=[{"name": "any", "stdout": ""}],
        )
        result = self.grade(task, {"sol.py": "import itertools\nx = [2, 1]\nx.sort()\nlen(x)\n"})
        banned = next(c for c in result.checks if c.name.startswith("Not using"))
        self.assertFalse(banned.ok)
        for name in ("len", ".sort", "itertools"):
            self.assertIn(name, banned.detail)
        clean = runners.grade(
            task, write_files(self.tmp / "ok", {"sol.py": "x = 1\n"}), include_hidden=True
        )
        self.assertTrue(clean.passed)

    def test_require_and_forbid_patterns_ignore_comments(self):
        task = make_task(
            self.tmp / "pack",
            require=[(r"\bfor\b", "Uses a loop")],
            forbid=[("abc", "No hard-coding")],
            cases=[{"name": "any", "stdout": ""}],
        )
        no_loop = self.grade(task, {"sol.py": "# for\nx = 1\n"})
        self.assertFalse(no_loop.passed)
        hard_coded = self.grade(task, {"sol.py": "for i in []:\n    pass\ns = 'abc'\n"})
        self.assertFalse(hard_coded.passed)
        fine = self.grade(task, {"sol.py": "for i in []:\n    pass\n"})
        self.assertTrue(fine.passed)

    def test_hidden_cases_are_skipped_locally_and_masked_when_failing(self):
        task = make_task(
            self.tmp / "pack",
            cases=[
                {"name": "visible", "stdout": "a\n"},
                {"name": "secret", "stdout": "b\n", "hidden": True, "hint": "think harder"},
            ],
        )
        files = {"sol.py": "print('a')\n"}
        local = self.grade(task, files, hidden=False)
        self.assertTrue(local.passed)
        self.assertEqual(
            [c.name for c in local.checks], ["Files turned in", "Syntax", "Test: visible"]
        )
        full = self.grade(task, files, hidden=True)
        self.assertFalse(full.passed)
        secret = full.checks[-1]
        self.assertTrue(secret.hidden)
        self.assertEqual(secret.name, "Hidden test")
        self.assertEqual(secret.detail, "think harder")

    def test_infinite_loop_is_a_failure_not_a_hang(self):
        task = make_task(self.tmp / "pack", timeout=1)
        result = self.grade(task, {"sol.py": "while True:\n    pass\n"})
        self.assertFalse(result.passed)
        self.assertIn("timed out", result.checks[-1].detail)

    def test_exception_shows_the_last_traceback_line(self):
        task = make_task(self.tmp / "pack")
        result = self.grade(task, {"sol.py": "raise ValueError('boom')\n"})
        self.assertIn("ValueError: boom", result.checks[-1].detail)

    def test_harness_calls_the_function(self):
        harness = (
            "harness.py",
            "import sys\nfrom sol import double\nprint(double(int(sys.argv[1])))\n",
        )
        task = make_task(
            self.tmp / "pack",
            harness=harness,
            cases=[{"name": "four", "args": ["2"], "stdout": "4\n"}],
        )
        self.assertTrue(self.grade(task, {"sol.py": "def double(n):\n    return n * 2\n"}).passed)

    def test_style_notes_are_collected(self):
        task = make_task(self.tmp / "pack", cases=[{"name": "any", "stdout": ""}])
        result = self.grade(task, {"sol.py": "x = 1  \n" + "y = " + "1" * 120 + "\n"})
        self.assertTrue(result.passed)  # style never fails a solution...
        self.assertEqual(len(result.style), 2)  # ...it only costs score


@unittest.skipUnless(HAS_CC, "no C compiler")
class CRunnerTests(TempDirTestCase):
    HELLO = (
        '#include <unistd.h>\nint main(void)\n{\n    write(1, "ok\\n", 3);\n    return (0);\n}\n'
    )

    def grade(self, task, source, name="sol.c"):
        return runners.grade(
            task, write_files(self.tmp / "work", {name: source}), include_hidden=True
        )

    def task(self, **kw):
        return make_task(
            self.tmp / "pack", language="c", files=("sol.c",), allowed=("write",), **kw
        )

    def test_good_solution_passes(self):
        result = self.grade(self.task(), self.HELLO)
        self.assertTrue(result.passed, result.checks)

    def test_warnings_are_errors(self):
        result = self.grade(self.task(), "int main(void)\n{\n    int unused;\n    return (0);\n}\n")
        self.assertFalse(result.passed)
        self.assertIn("unused", result.checks[-1].detail)

    def test_only_allowed_functions(self):
        source = '#include <stdio.h>\nint main(void)\n{\n    printf("ok\\n");\n    return (0);\n}\n'
        result = self.grade(self.task(), source)
        banned = next(c for c in result.checks if c.name.startswith("Allowed functions"))
        self.assertFalse(banned.ok)
        self.assertIn("printf", banned.detail)

    def test_crash_and_exit_status(self):
        crash = self.grade(self.task(), "int main(void)\n{\n    int *p = 0;\n    return (*p);\n}\n")
        self.assertFalse(crash.passed)
        status = self.grade(
            self.task(),
            '#include <unistd.h>\nint main(void)\n{\n    write(1, "ok\\n", 3);\n    return (4);\n}\n',
        )
        self.assertIn("exit status 4", status.checks[-1].detail)

    @unittest.skipUnless(c.sanitizer_support(c.find_compiler() or "cc")[1], "no leak detection")
    def test_leaks_and_overflows_are_reported(self):
        leak = (
            "#include <stdlib.h>\n#include <unistd.h>\nint main(void)\n{\n"
            '    char *p = malloc(8);\n    p[0] = 1;\n    write(1, "ok\\n", 3);\n    p = 0;\n    return (0);\n}\n'
        )
        task = make_task(
            self.tmp / "pack", language="c", files=("sol.c",), allowed=("write", "malloc")
        )
        result = self.grade(task, leak)
        self.assertFalse(result.passed)
        self.assertIn("LeakSanitizer", result.checks[-1].detail)

    def test_infinite_loop_is_stopped(self):
        task = make_task(self.tmp / "pack", language="c", files=("sol.c",), allowed=(), timeout=1)
        result = self.grade(
            task, "int main(void)\n{\n    while (1)\n        ;\n    return (0);\n}\n"
        )
        self.assertIn("timed out", result.checks[-1].detail)

    def test_main_is_rejected_when_the_task_brings_its_own(self):
        harness = ("harness.c", "int f(void);\nint main(void)\n{\n    return (f());\n}\n")
        task = make_task(
            self.tmp / "pack", language="c", files=("sol.c",), allowed=(), harness=harness
        )
        result = self.grade(
            task, "int f(void)\n{\n    return (0);\n}\nint main(void)\n{\n    return (0);\n}\n"
        )
        self.assertFalse(result.passed)
        self.assertEqual(result.checks[-1].name, "No main()")

    def test_missing_nm_only_adds_a_note(self):
        real_which = shutil.which

        def without_nm(name):
            return None if name == "nm" else real_which(name)

        with mock.patch("journey.runners.c.shutil.which", side_effect=without_nm):
            result = self.grade(self.task(), self.HELLO)
        self.assertTrue(result.passed, result.checks)
        self.assertTrue(any("nm" in note for note in result.notes))


if __name__ == "__main__":
    unittest.main()
