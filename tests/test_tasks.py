"""Loading task packs: what the catalog sees, and what it must ignore."""

import os
import subprocess
import sys
from pathlib import Path

from journey import config
from journey.tasks import TaskError, load_catalog, load_task

from .helpers import IsolatedHome, make_task, write_files

SRC = str(Path(__file__).resolve().parents[1] / "src")


class CatalogScanTests(IsolatedHome):
    def test_user_tasks_join_the_built_in_ones(self):
        make_task(config.user_tasks_dir(), name="u_mine")
        self.assertIn("u_mine", load_catalog().tasks)
        self.assertIn("c01_hello", load_catalog().tasks)

    def test_hidden_and_underscore_folders_are_work_in_progress(self):
        user = config.user_tasks_dir()
        make_task(user / ".wip-x", name="t_hidden")
        make_task(user / "_scratch", name="t_scratch")
        make_task(user, name="t_visible")
        tasks = load_catalog().tasks
        self.assertIn("t_visible", tasks)
        self.assertNotIn("t_hidden", tasks)
        self.assertNotIn("t_scratch", tasks)

    def test_a_half_written_task_is_an_error_not_silently_skipped(self):
        broken = config.user_tasks_dir() / "broken"
        broken.mkdir(parents=True)
        (broken / "task.toml").write_text('title = "no language or kind"\n')
        with self.assertRaises(TaskError):
            load_catalog()

    def test_fixture_tables_are_loaded_and_checked(self):
        task = make_task(
            self.tmp,
            cases=[
                {
                    "name": "files",
                    "stdout": "",
                    "files": {"in.txt": "a\n"},
                    "expect_files": {"out.txt": "b\n"},
                }
            ],
        )
        case = task.cases[0]
        self.assertEqual(case.files, (("in.txt", "a\n"),))
        self.assertEqual(case.expect_files, (("out.txt", "b\n"),))
        with self.assertRaises(TaskError):
            make_task(
                self.tmp,
                name="t_bad",
                cases=[{"name": "x", "stdout": "", "files": {"../escape.txt": "x"}}],
            )


class ValidatePathTests(IsolatedHome):
    def run_validate(self, folder):
        env = {**os.environ, "PYTHONPATH": SRC, "NO_COLOR": "1"}
        return subprocess.run(
            [sys.executable, "-m", "journey", "validate", "--path", str(folder)],
            capture_output=True,
            text=True,
            env=env,
            cwd=self.tmp,
        )

    def test_a_work_in_progress_folder_can_be_validated_in_place(self):
        task = make_task(
            self.tmp / ".wip-pack",
            name="t_wip",
            cases=[{"name": "prints ok", "stdout": "ok\n"}],
        )
        write_files(task.root / "solution", {"sol.py": "print('ok')\n"})
        result = self.run_validate(task.root)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("t_wip", result.stdout)

    def test_a_wrong_reference_solution_is_reported(self):
        task = make_task(self.tmp / ".wip-pack", name="t_wip")
        write_files(task.root / "solution", {"sol.py": "print('nope')\n"})
        result = self.run_validate(task.root)
        self.assertEqual(result.returncode, 1)
        self.assertIn("reference solution fails", result.stdout)

    def test_load_task_requires_a_subject(self):
        task = make_task(self.tmp, name="t_nosubject")
        (task.root / "subject.md").unlink()
        with self.assertRaises(TaskError):
            load_task(task.root / "task.toml")
