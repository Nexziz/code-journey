import time
import unittest
from datetime import date, datetime, timedelta

from journey import curriculum, engine
from journey.runners import GradeResult
from journey.store import Store
from journey.tasks import Catalog, Level

from .helpers import TempDirTestCase, make_task


def passing(style=()):
    result = GradeResult()
    result.add("tests", True)
    result.style = list(style)
    return result


def failing():
    result = GradeResult()
    result.add("tests", False, "nope")
    return result


class ProgressCase(TempDirTestCase):
    def setUp(self):
        super().setUp()
        self.store = Store(self.tmp / "db.sqlite3")
        self.addCleanup(self.store.close)
        pack = self.tmp / "pack"
        specs = [
            dict(name="l1a", kind="learn", level=1, order=1),
            dict(name="l1boss", kind="boss", level=1, order=9),
            dict(name="l2a", kind="learn", level=2, order=1),
            dict(name="d_easy", kind="daily", level=1, rating=800),
            dict(name="d_mid", kind="daily", level=1, rating=1000),
            dict(name="d_hard", kind="daily", level=2, rating=1400),
            dict(name="w1", kind="weekly", level=1, rating=900),
        ]
        self.catalog = Catalog()
        for spec in specs:
            task = make_task(pack, **spec)
            self.catalog.tasks[task.id] = task
        self.catalog.levels["python"] = [
            Level("python", 1, "One", "output", ""),
            Level("python", 2, "Two", "variables", ""),
        ]

    def finish(self, task_id, *, now=None, result=None, style=()):
        """Start a task and pass it, returning the outcome."""
        now = now if now is not None else time.time()
        task = self.catalog.tasks[task_id]
        self.store.begin(task_id, now, repeat=task_id in self.store.passed_ids())
        self.store.set_meta("current", task_id)
        return engine.submit(
            self.store, self.catalog, task, result or passing(style), commit="abc1234", now=now + 60
        )


class StopwatchTests(ProgressCase):
    def test_active_time_only_counts_running_stretches(self):
        self.store.begin("l1a", 1000, repeat=False)
        self.store.settle("l1a", 1100)  # 100 s running
        self.assertEqual(self.store.elapsed("l1a", 5000), 100)  # paused: the clock stands still
        self.store.begin("l1a", 5000, repeat=False)  # resume
        self.assertEqual(self.store.elapsed("l1a", 5050), 150)

    def test_settle_all_stops_every_running_task(self):
        self.store.begin("l1a", 0, repeat=False)
        self.store.begin("l1boss", 10, repeat=False)
        self.store.settle_all(100)
        self.assertEqual(self.store.elapsed("l1a", 999), 100)
        self.assertEqual(self.store.elapsed("l1boss", 999), 90)


class CurriculumTests(ProgressCase):
    def test_levels_unlock_in_order(self):
        s, c = self.store, self.catalog
        self.assertEqual(curriculum.completed_levels(s, c, "python"), 0)
        self.assertEqual(curriculum.unlocked_level(s, c, "python"), 1)
        self.assertEqual(curriculum.next_curriculum_task(s, c, "python").id, "l1a")
        self.assertFalse(curriculum.is_unlocked(s, c, c.tasks["l2a"]))
        self.finish("l1a")
        self.assertEqual(curriculum.next_curriculum_task(s, c, "python").id, "l1boss")
        outcome = self.finish("l1boss")
        self.assertEqual(outcome.level_up.number, 1)
        self.assertEqual(curriculum.completed_levels(s, c, "python"), 1)
        self.assertTrue(curriculum.is_unlocked(s, c, c.tasks["l2a"]))

    def test_dailies_wait_for_their_levels(self):
        s, c = self.store, self.catalog
        self.assertFalse(curriculum.is_unlocked(s, c, c.tasks["d_easy"]))
        self.finish("l1a")
        self.finish("l1boss")
        self.assertTrue(curriculum.is_unlocked(s, c, c.tasks["d_easy"]))
        self.assertFalse(curriculum.is_unlocked(s, c, c.tasks["d_hard"]))  # needs level 2 done

    def test_finishing_everything_returns_no_next_task(self):
        for task_id in ("l1a", "l1boss", "l2a"):
            self.finish(task_id)
        self.assertIsNone(curriculum.next_curriculum_task(self.store, self.catalog, "python"))


class PickTests(ProgressCase):
    today = date(2026, 3, 4)

    def unlock(self):
        self.finish("l1a")
        self.finish("l1boss")

    def test_nothing_to_pick_before_level_one_is_done(self):
        self.assertIsNone(
            curriculum.pick_task(self.store, self.catalog, "daily", "python", self.today)
        )

    def test_pick_is_stable_for_the_day_even_if_rating_changes(self):
        self.unlock()
        first = curriculum.pick_task(self.store, self.catalog, "daily", "python", self.today)
        self.store.set_rating("python", 2000, 30)
        again = curriculum.pick_task(self.store, self.catalog, "daily", "python", self.today)
        self.assertEqual(first.id, again.id)

    def test_pick_fits_the_rating(self):
        self.unlock()
        self.store.set_rating("python", 790, 30)
        task = curriculum.pick_task(self.store, self.catalog, "daily", "python", self.today)
        self.assertEqual(task.id, "d_easy")  # the others are 200+ points away
        tomorrow = self.today + timedelta(days=1)
        self.store.set_rating("python", 1010, 30)
        task = curriculum.pick_task(self.store, self.catalog, "daily", "python", tomorrow)
        self.assertEqual(task.id, "d_mid")

    def test_resolved_tasks_are_not_picked_again(self):
        self.unlock()
        self.store.set_rating("python", 800, 30)
        self.finish("d_easy")
        task = curriculum.pick_task(self.store, self.catalog, "daily", "python", self.today)
        self.assertEqual(task.id, "d_mid")

    def test_reruns_when_the_pool_is_dry(self):
        self.unlock()
        self.finish("d_easy")
        self.finish("d_mid")
        task = curriculum.pick_task(self.store, self.catalog, "daily", "python", self.today)
        self.assertIn(task.id, ("d_easy", "d_mid"))

    def test_weekly_pick_is_per_week(self):
        self.unlock()
        monday = date(2026, 3, 2)
        sunday = date(2026, 3, 8)
        self.assertEqual(
            curriculum.period_key("weekly", monday), curriculum.period_key("weekly", sunday)
        )
        self.assertNotEqual(
            curriculum.period_key("weekly", sunday),
            curriculum.period_key("weekly", sunday + timedelta(days=1)),
        )
        task = curriculum.pick_task(self.store, self.catalog, "weekly", "python", monday)
        self.assertEqual(task.id, "w1")


class NothingUnlockedTests(ProgressCase):
    def test_the_message_names_the_level_that_opens_dailies(self):
        message = curriculum.nothing_unlocked(self.catalog, "daily", "python")
        self.assertIn("level 1", message)  # the lowest daily needs level 1
        self.assertIn(
            "no weekly", curriculum.nothing_unlocked(Catalog(), "weekly", "python").lower()
        )


class StreakTests(ProgressCase):
    def complete_on(self, day: date, task_id="l1a"):
        ts = datetime.combine(day, datetime.min.time()).timestamp() + 12 * 3600
        self.store.add_completion(
            task_id=task_id,
            language="python",
            kind="learn",
            ts=ts,
            gave_up=0,
            repeat=0,
            score=1.0,
            stars=3,
            active_seconds=1,
            failed_attempts=0,
        )

    def test_streak_counts_consecutive_days_ending_today_or_yesterday(self):
        today = date(2026, 3, 10)
        self.assertEqual(curriculum.practice_streak(self.store, today), 0)
        for back in (1, 2, 3):
            self.complete_on(today - timedelta(days=back))
        self.assertEqual(curriculum.practice_streak(self.store, today), 3)  # yesterday still counts
        self.complete_on(today)
        self.assertEqual(curriculum.practice_streak(self.store, today), 4)

    def test_a_gap_breaks_the_streak(self):
        today = date(2026, 3, 10)
        self.complete_on(today)
        self.complete_on(today - timedelta(days=2))
        self.assertEqual(curriculum.practice_streak(self.store, today), 1)

    def test_giving_up_does_not_count(self):
        today = date(2026, 3, 10)
        self.store.add_completion(
            task_id="d_easy",
            language="python",
            kind="daily",
            ts=datetime.combine(today, datetime.min.time()).timestamp() + 100,
            gave_up=1,
            repeat=0,
            score=0.0,
            stars=0,
            active_seconds=1,
            failed_attempts=0,
        )
        self.assertEqual(curriculum.practice_streak(self.store, today), 0)


class EngineTests(ProgressCase):
    def test_failed_attempts_are_counted_and_remembered(self):
        task = self.catalog.tasks["l1a"]
        self.store.begin("l1a", 0, repeat=False)
        first = engine.submit(self.store, self.catalog, task, failing(), commit="a", now=10)
        self.assertFalse(first.passed)
        self.assertEqual((first.attempt_no, first.failed_attempts), (1, 1))
        second = engine.submit(self.store, self.catalog, task, passing(), commit="b", now=20)
        self.assertTrue(second.passed)
        self.assertEqual((second.attempt_no, second.failed_attempts), (2, 1))
        self.assertLess(second.performance.score, 1.0)
        self.assertEqual(len(self.store.attempts_for("l1a")), 2)
        self.assertIsNone(self.store.state("l1a"))  # finished tasks leave the "in progress" list

    def test_learning_tasks_never_touch_the_rating(self):
        outcome = self.finish("l1a")
        self.assertIsNone(outcome.rating_after)
        self.assertEqual(self.store.rating("python"), (800.0, 0))
        self.assertEqual(self.store.best_stars()["l1a"], 3)

    def test_rated_tasks_move_the_rating(self):
        before, games = self.store.rating("python")
        outcome = self.finish("d_easy")
        after, games_after = self.store.rating("python")
        self.assertGreater(after, before)
        self.assertEqual(games_after, games + 1)
        self.assertEqual(outcome.rating_after, after)

    def test_slow_solutions_score_less_on_rated_tasks(self):
        task = self.catalog.tasks["d_easy"]
        self.store.begin("d_easy", 0, repeat=False)
        outcome = engine.submit(
            self.store, self.catalog, task, passing(), commit="a", now=task.par_minutes * 60 * 3
        )
        self.assertAlmostEqual(outcome.performance.speed, 0.0)

    def test_style_costs_stars(self):
        outcome = self.finish("l1a", style=["x:1: trailing whitespace"] * 4)
        self.assertLess(outcome.performance.stars, 3)

    def test_repeat_runs_keep_the_rating(self):
        self.finish("d_easy")
        rating = self.store.rating("python")
        outcome = self.finish("d_easy")  # now a repeat
        self.assertTrue(outcome.repeat)
        self.assertEqual(self.store.rating("python"), rating)
        self.assertEqual(self.store.passed_ids(), {"d_easy"})

    def test_giving_up_a_rated_task_costs_rating_but_a_learning_task_costs_nothing(self):
        self.store.begin("d_easy", 0, repeat=False)
        before, _ = self.store.rating("python")
        change = engine.give_up(self.store, self.catalog.tasks["d_easy"], now=60)
        self.assertLess(change[1], before)
        self.assertNotIn("d_easy", self.store.passed_ids())
        self.assertIn("d_easy", self.store.resolved_ids())
        self.store.begin("l1a", 0, repeat=False)
        self.assertIsNone(engine.give_up(self.store, self.catalog.tasks["l1a"], now=60))
        self.assertNotIn("l1a", self.store.resolved_ids())

    def test_unknown_task_is_an_error(self):
        with self.assertRaises(LookupError):
            engine.submit(
                self.store, self.catalog, self.catalog.tasks["l1a"], passing(), commit=None, now=1
            )


if __name__ == "__main__":
    unittest.main()
