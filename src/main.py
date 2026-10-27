"""Demo script showcasing the LRU Cache and Event Scheduler implementations."""

import sys
from pathlib import Path

# Add src directory to sys.path so it runs standalone directly
sys.path.insert(0, str(Path(__file__).parent))

from solutions.lru_cache import LRUCache
from solutions.event_scheduler import can_attend_all, min_rooms_required, assign_rooms


def demo_lru_cache() -> None:
    print("=" * 60)
    print("DEMO 1: LRU Cache")
    print("=" * 60)

    cache = LRUCache(capacity=2)
    print("Initialized LRUCache with capacity = 2")

    print("\nput(1, 10)")
    cache.put(1, 10)
    print("put(2, 20)")
    cache.put(2, 20)

    print(f"get(1) -> {cache.get(1)} (expected 10, marks 1 as MRU)")

    print("put(3, 30) -> Evicts key 2 (least recently used)")
    cache.put(3, 30)

    print(f"get(2) -> {cache.get(2)} (expected -1, since 2 was evicted)")
    print(f"get(3) -> {cache.get(3)} (expected 30)")
    print(f"get(1) -> {cache.get(1)} (expected 10)")


def demo_event_scheduler() -> None:
    print("\n" + "=" * 60)
    print("DEMO 2: Event Scheduler")
    print("=" * 60)

    events_1 = [(9, 10), (10, 11), (11, 12)]
    print(f"Events 1 (adjacent): {events_1}")
    print(f"  can_attend_all: {can_attend_all(events_1)} (Expected: True)")
    print(f"  min_rooms_required: {min_rooms_required(events_1)} (Expected: 1)")

    events_2 = [(9, 11), (10, 12), (11, 13)]
    print(f"\nEvents 2 (overlapping): {events_2}")
    print(f"  can_attend_all: {can_attend_all(events_2)} (Expected: False)")
    print(f"  min_rooms_required: {min_rooms_required(events_2)} (Expected: 2)")

    events_3 = [(0, 30), (5, 10), (15, 20), (25, 35)]
    print(f"\nEvents 3 (multiple overlaps): {events_3}")
    print(f"  can_attend_all: {can_attend_all(events_3)} (Expected: False)")
    print(f"  min_rooms_required: {min_rooms_required(events_3)} (Expected: 2)")

    print("\nRoom Allocation Future-Proofing:")
    assignments = assign_rooms(events_3)
    for a in assignments:
        print(f"  Event {a['event']} -> Assigned to: {a['room']}")


if __name__ == "__main__":
    demo_lru_cache()
    demo_event_scheduler()
