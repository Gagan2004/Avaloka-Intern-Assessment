"""Problem 2: Event Scheduler

Logic and Approach:
-------------------
1. can_attend_all(events):
   - Sort intervals chronologically by start time.
   - For every adjacent pair, check if curr_start < prev_end.
   - If true, there is an overlap, so return False.
   - Adjacent events where prev_end == curr_start are valid (no overlap).
   - If no overlaps are found, return True.

2. min_rooms_required(events):
   - Finding the minimum meeting rooms is equivalent to finding the maximum number
     of overlapping intervals at any given moment.
   - Sort events by start time.
   - Use a min-heap to track the end times of active meetings across all rooms.
     The top of the heap is the earliest ending meeting.
   - For each event:
     - If the earliest meeting finishes at or before the current event's start time
       (heap[0] <= start), that room is freed and reused (heappop).
     - Push the current event's end time onto the heap (heappush).
   - The total elements in the heap at the end equals the peak rooms needed.

3. Future Proofing (assign_rooms):
   - Tracks free room identifiers (e.g., 'Room A', 'Room B') using a min-heap to
     reassign the lowest-indexed available room when an event finishes.
"""

import heapq
from typing import Any, Dict, List, Sequence, Tuple

Event = Tuple[int, int]


def can_attend_all(events: Sequence[Event]) -> bool:
    """Returns True if a person can attend all events without overlaps."""
    if len(events) <= 1:
        return True

    sorted_events = sorted(events, key=lambda e: e[0])

    for i in range(1, len(sorted_events)):
        prev_start, prev_end = sorted_events[i - 1]
        curr_start, curr_end = sorted_events[i]

        # Overlap occurs strictly when curr_start < prev_end
        if curr_start < prev_end:
            return False

    return True


def min_rooms_required(events: Sequence[Event]) -> int:
    """Calculates the minimum number of meeting rooms required simultaneously."""
    if not events:
        return 0

    sorted_events = sorted(events, key=lambda e: e[0])
    rooms_heap: List[int] = []

    for start, end in sorted_events:
        # If the earliest ending meeting is finished, reuse that room
        if rooms_heap and rooms_heap[0] <= start:
            heapq.heappop(rooms_heap)

        # Allocate room with new end time
        heapq.heappush(rooms_heap, end)

    return len(rooms_heap)


def _room_label(index: int) -> str:
    """Converts index 0 -> 'Room A', 1 -> 'Room B', 26 -> 'Room AA', etc."""
    label = ""
    curr = index
    while curr >= 0:
        label = chr(ord("A") + (curr % 26)) + label
        curr = (curr // 26) - 1
    return f"Room {label}"


def assign_rooms(events: Sequence[Event]) -> List[Dict[str, Any]]:
    """Assigns specific room names ('Room A', 'Room B') to each event."""
    if not events:
        return []

    # Keep track of original indices to maintain input order
    indexed = sorted(enumerate(events), key=lambda item: (item[1][0], item[1][1]))

    active_rooms: List[Tuple[int, int]] = []  # (end_time, room_id)
    free_room_ids: List[int] = []  # Min-heap of reusable room numbers
    max_allocated = 0
    assignments: List[Dict[str, Any]] = [{}] * len(events)

    for orig_idx, (start, end) in indexed:
        # Release finished rooms
        while active_rooms and active_rooms[0][0] <= start:
            _, freed_id = heapq.heappop(active_rooms)
            heapq.heappush(free_room_ids, freed_id)

        # Reuse or create room
        if free_room_ids:
            room_id = heapq.heappop(free_room_ids)
        else:
            room_id = max_allocated
            max_allocated += 1

        heapq.heappush(active_rooms, (end, room_id))
        assignments[orig_idx] = {
            "event": (start, end),
            "room": _room_label(room_id),
        }

    return assignments


if __name__ == "__main__":
    print("Testing Event Scheduler:")
    events_adjacent = [(9, 10), (10, 11), (11, 12)]
    print(f"Events: {events_adjacent}")
    print(f"  can_attend_all: {can_attend_all(events_adjacent)} (expected True)")
    print(f"  min_rooms_required: {min_rooms_required(events_adjacent)} (expected 1)")

    events_overlapping = [(0, 30), (5, 10), (15, 20), (25, 35)]
    print(f"\nEvents: {events_overlapping}")
    print(f"  can_attend_all: {can_attend_all(events_overlapping)} (expected False)")
    print(f"  min_rooms_required: {min_rooms_required(events_overlapping)} (expected 2)")

    print("\nRoom Assignments:")
    for a in assign_rooms(events_overlapping):
        print(f"  {a['event']} -> {a['room']}")
