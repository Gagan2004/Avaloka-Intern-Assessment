"""Main entry point to run demonstrations for both Problem 1 and Problem 2."""

from lru_cache import LRUCache
from event_scheduler import can_attend_all, min_rooms_required, assign_rooms


def run_lru_demo() -> None:
    print("=" * 55)
    print("Problem 1: LRU Cache Demonstration")
    print("=" * 55)

    cache = LRUCache(capacity=2)
    print("Created LRUCache with capacity = 2\n")

    print("1. put(1, 10)")
    cache.put(1, 10)
    print("2. put(2, 20)")
    cache.put(2, 20)

    print(f"3. get(1) -> {cache.get(1)} (expected: 10, marks key 1 as MRU)")

    print("4. put(3, 30) -> Cache full; evicts key 2 (LRU)")
    cache.put(3, 30)

    print(f"5. get(2) -> {cache.get(2)} (expected: -1, evicted)")
    print(f"6. get(3) -> {cache.get(3)} (expected: 30)")
    print(f"7. get(1) -> {cache.get(1)} (expected: 10)")


def run_scheduler_demo() -> None:
    print("\n" + "=" * 55)
    print("Problem 2: Event Scheduler Demonstration")
    print("=" * 55)

    # Example 1: Adjacent events (no overlap)
    events_1 = [(9, 10), (10, 11), (11, 12)]
    print(f"\nEvents: {events_1}")
    print(f"  can_attend_all: {can_attend_all(events_1)} (Expected: True)")
    print(f"  min_rooms_required: {min_rooms_required(events_1)} (Expected: 1)")

    # Example 2: Overlapping events
    events_2 = [(9, 11), (10, 12), (11, 13)]
    print(f"\nEvents: {events_2}")
    print(f"  can_attend_all: {can_attend_all(events_2)} (Expected: False)")
    print(f"  min_rooms_required: {min_rooms_required(events_2)} (Expected: 2)")

    # Example 3: Multiple overlapping meetings & specific room assignment
    events_3 = [(0, 30), (5, 10), (15, 20), (25, 35)]
    print(f"\nEvents: {events_3}")
    print(f"  can_attend_all: {can_attend_all(events_3)} (Expected: False)")
    print(f"  min_rooms_required: {min_rooms_required(events_3)} (Expected: 2)")

    print("\nFuture-Proofing: Specific Room Allocation:")
    assignments = assign_rooms(events_3)
    for a in assignments:
        print(f"  Meeting {a['event']} -> Assigned to: {a['room']}")


if __name__ == "__main__":
    run_lru_demo()
    run_scheduler_demo()
