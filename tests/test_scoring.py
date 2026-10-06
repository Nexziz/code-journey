import unittest

from journey import scoring


class ExpectedScoreTests(unittest.TestCase):
    def test_equal_rating_is_expected_to_do_well(self):
        self.assertAlmostEqual(scoring.expected_score(1000, 1000), 0.76, places=2)

    def test_harder_tasks_lower_the_expectation(self):
        self.assertLess(scoring.expected_score(1000, 1300), scoring.expected_score(1000, 1000))
        self.assertGreater(scoring.expected_score(1000, 700), scoring.expected_score(1000, 1000))


class SpeedTests(unittest.TestCase):
    def test_fast_is_full_marks(self):
        self.assertEqual(scoring.speed_factor(5 * 60, 20), 1.0)
        self.assertEqual(scoring.speed_factor(10 * 60, 20), 1.0)  # exactly half the par time

    def test_slow_is_zero(self):
        self.assertEqual(scoring.speed_factor(40 * 60, 20), 0.0)
        self.assertEqual(scoring.speed_factor(10 * 3600, 20), 0.0)

    def test_linear_in_between(self):
        self.assertAlmostEqual(scoring.speed_factor(25 * 60, 20), 0.5)  # 1.25 x par


class PerformanceTests(unittest.TestCase):
    def perf(self, **kw):
        base = dict(
            rated=True, failed_attempts=0, active_seconds=60, par_minutes=30, style_issues=0
        )
        return scoring.performance(**{**base, **kw})

    def test_perfect_rated_solve_scores_one(self):
        perf = self.perf()
        self.assertAlmostEqual(perf.score, 1.0)
        self.assertEqual(perf.stars, 3)

    def test_perfect_learning_solve_scores_one_and_ignores_time(self):
        slow = self.perf(rated=False, active_seconds=10 * 3600)
        self.assertAlmostEqual(slow.score, 1.0)
        self.assertIsNone(slow.speed)

    def test_correctness_is_worth_the_most(self):
        worst = self.perf(failed_attempts=9, active_seconds=10 * 3600, style_issues=9)
        self.assertAlmostEqual(worst.score, 0.60)
        worst_learning = self.perf(rated=False, failed_attempts=9, style_issues=9)
        self.assertAlmostEqual(worst_learning.score, 0.70)

    def test_failed_attempts_and_style_cost_score(self):
        self.assertLess(self.perf(failed_attempts=1).score, self.perf().score)
        self.assertLess(self.perf(style_issues=2).score, self.perf().score)

    def test_stars(self):
        self.assertEqual(self.perf(rated=False).stars, 3)
        self.assertEqual(self.perf(rated=False, failed_attempts=1).stars, 2)
        self.assertEqual(self.perf(rated=False, failed_attempts=5, style_issues=5).stars, 1)


class RatingUpdateTests(unittest.TestCase):
    def test_provisional_ratings_move_more(self):
        new_player, _, _ = scoring.rating_update(800, 0, 800, 1.0, "daily")
        settled, _, _ = scoring.rating_update(800, 50, 800, 1.0, "daily")
        self.assertGreater(new_player - 800, settled - 800)

    def test_weekly_counts_one_and_a_half_times(self):
        _, _, daily = scoring.rating_update(800, 50, 800, 1.0, "daily")
        _, _, weekly = scoring.rating_update(800, 50, 800, 1.0, "weekly")
        self.assertAlmostEqual(weekly, daily * 1.5)

    def test_giving_up_loses_rating_and_beating_expectations_gains_it(self):
        lost, _, delta = scoring.rating_update(900, 50, 900, 0.0, "daily")
        self.assertLess(lost, 900)
        self.assertLess(delta, 0)
        gained, _, _ = scoring.rating_update(900, 50, 900, 1.0, "daily")
        self.assertGreater(gained, 900)

    def test_rank_titles(self):
        self.assertEqual(scoring.rank_title(800), "Apprentice")
        self.assertEqual(scoring.rank_title(1650), "Master")
        self.assertEqual(scoring.rank_title(100), "Rookie")


if __name__ == "__main__":
    unittest.main()
