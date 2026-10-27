"""Unit tests for LRUCache and ThreadSafeLRUCache."""

import threading
import pytest
from solutions.lru_cache import LRUCache, ThreadSafeLRUCache


class TestLRUCache:
    def test_basic_put_and_get(self):
        cache = LRUCache(2)
        cache.put("a", 1)
        cache.put("b", 2)
        assert cache.get("a") == 1
        assert cache.get("b") == 2
        assert cache.get("non_existent") == -1

    def test_eviction_order(self):
        cache = LRUCache(2)
        cache.put(1, 100)
        cache.put(2, 200)
        # 1 accessed, so 2 becomes LRU
        assert cache.get(1) == 100
        # Inserting 3 should evict 2
        cache.put(3, 300)
        assert cache.get(2) == -1
        assert cache.get(1) == 100
        assert cache.get(3) == 300

    def test_update_existing_key(self):
        cache = LRUCache(2)
        cache.put(1, 10)
        cache.put(2, 20)
        # Update 1 with new value
        cache.put(1, 15)
        assert cache.get(1) == 15
        assert len(cache) == 2

        # Key 2 should be evicted next because key 1 was updated and marked MRU
        cache.put(3, 30)
        assert cache.get(2) == -1
        assert cache.get(1) == 15
        assert cache.get(3) == 30

    def test_capacity_one(self):
        cache = LRUCache(1)
        cache.put("x", 10)
        assert cache.get("x") == 10
        cache.put("y", 20)
        assert cache.get("x") == -1
        assert cache.get("y") == 20

    def test_invalid_capacity(self):
        with pytest.raises(ValueError):
            LRUCache(0)
        with pytest.raises(ValueError):
            LRUCache(-5)

    def test_contains_and_len(self):
        cache = LRUCache(3)
        assert len(cache) == 0
        cache.put(1, 10)
        cache.put(2, 20)
        assert len(cache) == 2
        assert 1 in cache
        assert 3 not in cache


class TestThreadSafeLRUCache:
    def test_concurrent_access(self):
        cache = ThreadSafeLRUCache(capacity=50)
        threads = []
        errors = []

        def worker(thread_id: int):
            try:
                for i in range(100):
                    key = (thread_id * 100) + i
                    cache.put(key, i)
                    val = cache.get(key)
                    assert val in (i, -1)
            except Exception as e:
                errors.append(e)

        for t_id in range(10):
            t = threading.Thread(target=worker, args=(t_id,))
            threads.append(t)
            t.start()

        for t in threads:
            t.join()

        assert len(errors) == 0
        assert len(cache) <= 50
