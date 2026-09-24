import unittest

from causality import Tracker
from vectorclock import VClock


class TestVClock(unittest.TestCase):
    def test_tick_counts(self):
        clock = VClock("n1")
        self.assertEqual(clock.tick(), {"n1": 1})

    def test_tick_other_node(self):
        clock = VClock("n1")
        self.assertEqual(clock.tick("n2"), {"n2": 1})

    def test_merge_takes_max(self):
        left, right = VClock("n1"), VClock("n2")
        left.tick()
        right.tick()
        self.assertEqual(left.merge(right), {"n1": 1, "n2": 1})

    def test_stats_shape(self):
        self.assertIn("merges", VClock().stats())

    def test_tracker_wraps_clock(self):
        tracker = Tracker()
        tracker.tick()
        self.assertEqual(tracker.vclock.stats()["clock"], {"n1": 1})


if __name__ == "__main__":
    unittest.main()
