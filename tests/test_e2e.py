"""Drive the real CLI and real git, the way a learner does."""

import os
import shutil
import sqlite3
import subprocess
import sys
import unittest
from pathlib import Path

from journey.runners import c
from journey.tasks import load_catalog

from .helpers import IsolatedHome

SRC = str(Path(__file__).resolve().parents[1] / "src")


@unittest.skipUnless(shutil.which("git"), "git is required")
class EndToEndTests(IsolatedHome):
    def setUp(self):
        super().setUp()
        self.env = {**os.environ, "PYTHONPATH": SRC, "NO_COLOR": "1"}
        self.ws = self.tmp / "home" / "journey-workspace"
        self.catalog = load_catalog()

    def journey(self, *args):
        return subprocess.run(
            [sys.executable, "-m", "journey", *args],
            capture_output=True,
            text=True,
            env=self.env,
            cwd=self.tmp,
        )

    def git(self, *args):
        return subprocess.run(
            ["git", *args], capture_output=True, text=True, env=self.env, cwd=self.ws
        )

    def push(self, message="work"):
        self.git("add", ".")
        self.git("commit", "-m", message, "--allow-empty")
        proc = self.git("push", "-u", "origin", "main")
        return proc.stderr + proc.stdout  # the hook's output arrives as "remote: ..." lines

    def db(self, sql):
        con = sqlite3.connect(self.tmp / "home" / ".journey" / "journey.sqlite3")
        self.addCleanup(con.close)
        return con.execute(sql).fetchall()

    def use_solution(self, task_id):
        task = self.catalog.tasks[task_id]
        for name in task.files:
            shutil.copy(task.solution_dir / name, self.ws / task_id / name)

    def test_the_whole_loop(self):
        self.assertEqual(self.journey("init", "--lang", "python").returncode, 0)
        self.assertTrue(
            (self.tmp / "home" / ".journey" / "remote.git" / "hooks" / "post-receive").exists()
        )

        started = self.journey("start")
        self.assertEqual(started.returncode, 0, started.stderr)
        self.assertIn("py01_hello", started.stdout)
        self.assertTrue((self.ws / "py01_hello" / "hello.py").exists())  # the starter is there

        # The untouched starter does not pass the local check.
        self.assertEqual(self.journey("check").returncode, 1)

        # A wrong solution: graded, explained, counted as a failed attempt.
        (self.ws / "py01_hello" / "hello.py").write_text('print("Hello World")\n')
        wrong = self.push("first try")
        self.assertIn("Grading py01_hello", wrong)
        self.assertIn("Not yet", wrong)
        self.assertIn("expected 'Hello, World!\\n'", wrong)

        # The fix passes, and the earlier failure costs a little.
        self.use_solution("py01_hello")
        right = self.push("second try")
        self.assertIn("PASSED", right)
        self.assertIn("1 failed try", right)

        attempts = self.db("select passed from attempts order by id")
        self.assertEqual([row[0] for row in attempts], [0, 1])
        self.assertEqual(self.db("select task_id, gave_up from completions"), [("py01_hello", 0)])
        self.assertIn("py01_hello", self.journey("history").stdout)
        self.assertIn("Streak   1 day", self.journey("status").stdout)

        # Solutions are never shown, and finished tasks cannot be replayed by accident.
        self.assertNotEqual(self.journey("solution", "py01_hello").returncode, 0)
        again = self.journey("start", "py01_hello")
        self.assertEqual(again.returncode, 1)
        self.assertIn("--again", again.stderr)

    def test_pushing_without_a_task_explains_itself(self):
        self.journey("init")
        (self.ws / "note.txt").write_text("hi\n")
        out = self.push()
        self.assertIn("No task in progress", out)
        self.assertEqual(self.db("select count(*) from attempts"), [(0,)])

    def test_forgetting_to_add_the_folder_is_a_failed_attempt(self):
        self.journey("init", "--lang", "python")
        self.journey("start")
        (self.ws / "other.txt").write_text("not the exercise\n")
        self.git("add", "other.txt")
        self.git("commit", "-m", "only the wrong file")
        proc = self.git("push", "-u", "origin", "main")
        self.assertIn("is not in what you pushed", proc.stderr + proc.stdout)
        self.assertEqual(self.db("select passed from attempts"), [(0,)])

    def test_check_never_records_anything(self):
        self.journey("init", "--lang", "python")
        self.journey("start")
        self.use_solution("py01_hello")
        result = self.journey("check")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(self.db("select count(*) from attempts"), [(0,)])
        self.assertEqual(self.db("select count(*) from completions"), [(0,)])

    def test_branches_other_than_main_are_not_graded(self):
        self.journey("init", "--lang", "python")
        self.journey("start")
        self.use_solution("py01_hello")
        self.git("add", ".")
        self.git("commit", "-m", "x")
        proc = self.git("push", "origin", "HEAD:refs/heads/scratch")
        self.assertIn("main only", proc.stderr + proc.stdout)
        self.assertEqual(self.db("select count(*) from attempts"), [(0,)])

    def test_doctor_is_happy_after_init(self):
        self.journey("init")
        result = self.journey("doctor")
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("grading hook installed", result.stdout)

    @unittest.skipUnless(c.find_compiler(), "no C compiler")
    def test_c_task_forbidden_function_fails_then_the_fix_passes(self):
        self.journey("init", "--lang", "c")
        self.journey("start")
        hello = self.ws / "c01_hello" / "hello.c"
        hello.write_text(
            '#include <stdio.h>\nint main(void)\n{\n    printf("Hello, World!\\n");\n    return (0);\n}\n'
        )
        wrong = self.push("with printf")
        self.assertIn("Not yet", wrong)
        self.assertIn("you also call: printf", wrong)
        self.use_solution("c01_hello")
        self.assertIn("PASSED", self.push("with write"))


if __name__ == "__main__":
    unittest.main()
