"""Checks over the bundled task packs: the curriculum is complete and every task is sound."""

import unittest

from journey import validate
from journey.tasks import LANGUAGES, load_catalog

CATALOG = load_catalog()


class CurriculumShapeTests(unittest.TestCase):
    def test_both_languages_have_levels_and_content(self):
        for language in LANGUAGES:
            self.assertTrue(CATALOG.levels[language], language)
            for kind in ("daily", "weekly"):
                self.assertTrue(CATALOG.of_kind(language, kind), f"no {kind} tasks in {language}")

    def test_levels_are_numbered_without_gaps(self):
        for language, levels in CATALOG.levels.items():
            self.assertEqual(
                [lvl.number for lvl in levels], list(range(1, len(levels) + 1)), language
            )

    def test_every_level_has_learning_tasks_and_exactly_one_boss_that_comes_last(self):
        for language, levels in CATALOG.levels.items():
            for level in levels:
                tasks = CATALOG.curriculum(language, level.number)
                bosses = [t for t in tasks if t.kind == "boss"]
                self.assertEqual(len(bosses), 1, f"{language} level {level.number}")
                self.assertGreaterEqual(len(tasks), 3, f"{language} level {level.number}")
                self.assertEqual(tasks[-1].kind, "boss")

    def test_rated_tasks_only_use_levels_that_exist(self):
        for task in CATALOG.tasks.values():
            self.assertLessEqual(task.level, CATALOG.max_level(task.language), task.id)

    def test_subjects_name_the_files_to_turn_in(self):
        for task in CATALOG.tasks.values():
            subject = task.subject_path.read_text(encoding="utf-8")
            for name in task.files:
                self.assertIn(f"`{name}`", subject, f"{task.id}: subject never mentions {name}")

    def test_c_subjects_list_the_allowed_functions(self):
        for task in CATALOG.tasks.values():
            if task.language != "c":
                continue
            subject = task.subject_path.read_text(encoding="utf-8")
            self.assertIn("Allowed functions", subject, task.id)
            for function in task.allowed:
                self.assertIn(f"`{function}`", subject, f"{task.id}: {function}")

    def test_the_difficulty_grows_with_the_level(self):
        for language, levels in CATALOG.levels.items():
            means = []
            for level in levels:
                tasks = CATALOG.curriculum(language, level.number)
                means.append(sum(t.rating for t in tasks) / len(tasks))
            self.assertEqual(means, sorted(means), language)


class EveryTaskIsSoundTests(unittest.TestCase):
    """Slow on purpose: grades every model solution, starter and known-bad mutant."""

    def test_validate_every_task(self):
        failures = {}
        for task in CATALOG.tasks.values():
            problems = validate.validate_task(task, CATALOG)
            if problems:
                failures[task.id] = problems
        self.assertEqual(failures, {})


if __name__ == "__main__":
    unittest.main()
