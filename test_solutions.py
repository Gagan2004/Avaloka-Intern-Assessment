"""Unit tests for LRU Cache and Event Scheduler."""

import threading
import unittest
from lru_cache import LRUCache, ThreadSafeLRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms


class TestLRUCache(unittest.TestCase):
    def test_basic_put_get(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(2), 20)
        self.assertEqual(cache.get(999), -1)

    def test_lru_eviction(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.get(1)  # 1 is MRU, 2 is LRU
        cache.put(3, 30)  # Evicts 2
        self.assertEqual(cache.get(2), -1)
        self.assertEqual(cache.get(1), 10)
        self.assertEqual(cache.get(3), 30)

    def test_update_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        cache.put(1, 100)  # Update key 1
        self.assertEqual(cache.get(1), 100)
        cache.put(3, 30)  # Key 2 should be evicted
        self.assertEqual(cache.get(2), -1)
        self.assertEqual(cache.get(1), 100)

    def test_invalid_capacity(self):
        with self.assertRaises(ValueError):
            LRUCache(0)
        with self.assertRaises(ValueError):
            LRUCache(-1)

    def test_thread_safe_concurrent_access(self):
        cache = ThreadSafeLRUCache(capacity=20)
        errors = []

        def worker(t_id):
            try:
                for i in range(50):
                    cache.put(t_id * 100 + i, i)
                    cache.get(t_id * 100 + i)
            except Exception as e:
                errors.append(e)

        threads = [threading.Thread(target=worker, args=(t,)) for t in range(5)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()

        self.assertEqual(len(errors), 0)
        self.assertLessEqual(len(cache), 20)


class TestEventScheduler(unittest.TestCase):
    def test_can_attend_all_adjacent_events(self):
        # Adjacent events (end == start) are not considered overlaps
        events = [(9, 10), (10, 11), (11, 12)]
        self.assertTrue(can_attend_all(events))

    def test_can_attend_all_overlap(self):
        events = [(9, 11), (10, 12)]
        self.assertFalse(can_attend_all(events))

    def test_can_attend_all_empty_and_single(self):
        self.assertTrue(can_attend_all([]))
        self.assertTrue(can_attend_all([(1, 5)]))

    def test_min_rooms_required(self):
        self.assertEqual(min_rooms_required([]), 0)
        self.assertEqual(min_rooms_required([(9, 10), (10, 11)]), 1)
        self.assertEqual(min_rooms_required([(9, 11), (10, 12)]), 2)
        self.assertEqual(min_rooms_required([(0, 30), (5, 10), (15, 20)]), 2)

    def test_assign_rooms(self):
        events = [(0, 30), (5, 10), (15, 20)]
        assignments = assign_rooms(events)
        self.assertEqual(assignments[0]["room"], "Room A")
        self.assertEqual(assignments[1]["room"], "Room B")
        # Room B freed after (5, 10), should be reused for (15, 20)
        self.assertEqual(assignments[2]["room"], "Room B")


if __name__ == "__main__":
    unittest.main()
