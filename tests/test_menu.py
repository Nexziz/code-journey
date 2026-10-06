"""The way in: a bare `journey` shows a few choices and starts what you pick."""

import os
import subprocess
import sys
from pathlib import Path

from .helpers import IsolatedHome

SRC = str(Path(__file__).resolve().parents[1] / "src")


class MenuTests(IsolatedHome):
    def setUp(self):
        super().setUp()
        self.env = {**os.environ, "PYTHONPATH": SRC, "NO_COLOR": "1"}
        self.ws = self.tmp / "home" / "journey-workspace"

    def journey(self, *args, answer=None):
        return subprocess.run(
            [sys.executable, "-m", "journey", *args],
            capture_output=True,
            text=True,
            env=self.env,
            cwd=self.tmp,
            input=answer if answer is not None else "",
        )

    def test_first_run_asks_one_question_and_shows_the_menu(self):
        result = self.journey(answer="2\n")  # Python, then end of input at the menu prompt
        self.assertEqual(result.returncode, 0, result.stderr)
        out = result.stdout
        for label in ("Continue", "Daily", "Weekly", "Versus"):
            self.assertIn(label, out)
        self.assertIn("Python", out)
        self.assertTrue((self.ws / ".git").is_dir())  # set up without a separate init step

    def test_the_second_run_goes_straight_to_the_menu(self):
        self.journey(answer="1\n")
        result = self.journey()
        self.assertNotIn("Practise C or Python", result.stdout)
        self.assertIn("Continue", result.stdout)
        self.assertIn("C ·", result.stdout)

    def test_choosing_continue_starts_the_first_task(self):
        self.journey(answer="2\n")
        result = self.journey(answer="1\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Hello, terminal", result.stdout)  # the question
        self.assertIn("journey-workspace/py01_hello", result.stdout)  # where to work
        self.assertTrue((self.ws / "py01_hello" / "hello.py").exists())

    def test_enter_alone_continues(self):
        self.journey(answer="2\n")
        result = self.journey(answer="\n")
        self.assertIn("Hello, terminal", result.stdout)

    def test_choosing_the_daily_starts_it_or_says_when_it_opens(self):
        self.journey(answer="2\n")
        result = self.journey(answer="2\n")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue("## " not in result.stdout)
        self.assertIn("Assignment", result.stdout)

    def test_versus_is_announced_but_not_started(self):
        self.journey(answer="1\n")
        result = self.journey(answer="4\n")
        self.assertIn("coming soon", result.stdout.lower())

    def test_a_wrong_choice_is_politely_refused(self):
        self.journey(answer="1\n")
        result = self.journey(answer="9\n")
        self.assertEqual(result.returncode, 0)
        self.assertIn("Pick 1, 2 or 3", result.stdout)

    def test_help_shows_only_what_a_learner_needs(self):
        out = self.journey("--help").stdout
        for shown in ("continue", "daily", "weekly", "check", "track"):
            self.assertIn(shown, out)
        for hidden in ("solution", "giveup", "pause", "resume", "history", "validate", "doctor"):
            self.assertNotIn(hidden, out)

    def test_track_switches_the_language(self):
        self.journey(answer="1\n")
        self.assertIn("Python", self.journey("track", "python").stdout)
        self.assertIn("Python", self.journey(answer="").stdout)

    def test_no_command_ever_shows_a_solution(self):
        self.journey(answer="1\n")
        result = self.journey("solution")
        self.assertNotEqual(result.returncode, 0)
