"""Event Scheduler Implementation.

This module provides scheduling algorithms for meeting intervals:
- can_attend_all(events): Determines if a person can attend all meetings without overlap.
- min_rooms_required(events): Calculates the minimum number of meeting rooms required simultaneously.
- assign_rooms(events): Schedules events and assigns specific room labels ('Room A', 'Room B', etc.).
"""

import heapq
from typing import Any, Dict, List, Sequence, Tuple

Event = Tuple[int, int]


def can_attend_all(events: Sequence[Event]) -> bool:
    """Returns True if a person can attend all events without overlaps.

    Adjacent events where end_time == next_start_time are not considered overlaps.

    Args:
        events: A sequence of (start, end) time tuples.

    Returns:
        True if all events are non-overlapping, False otherwise.
    """
    if len(events) <= 1:
        return True

    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e[0])

    for i in range(1, len(sorted_events)):
        prev_start, prev_end = sorted_events[i - 1]
        curr_start, curr_end = sorted_events[i]

        # Overlap occurs strictly when curr_start < prev_end
        if curr_start < prev_end:
            return False

    return True


def min_rooms_required(events: Sequence[Event]) -> int:
    """Calculates the minimum number of meeting rooms required.

    Adjacent events where end_time == start_time do not require an extra room.

    Args:
        events: A sequence of (start, end) time tuples.

    Returns:
        The minimum number of rooms needed concurrently.
    """
    if not events:
        return 0

    # Sort events by start time
    sorted_events = sorted(events, key=lambda e: e[0])

    # Min-heap tracking the end times of active meeting rooms
    rooms_heap: List[int] = []

    for start, end in sorted_events:
        # If the earliest ending meeting finishes at or before the current start time,
        # that room is now free and can be reused.
        if rooms_heap and rooms_heap[0] <= start:
            heapq.heappop(rooms_heap)

        # Allocate room with the updated end time
        heapq.heappush(rooms_heap, end)

    return len(rooms_heap)


def _format_room_label(index: int) -> str:
    """Converts a zero-based index to spreadsheet-style room names:

    0 -> 'Room A', 25 -> 'Room Z', 26 -> 'Room AA', etc.
    """
    label = ""
    current = index
    while current >= 0:
        label = chr(ord("A") + (current % 26)) + label
        current = (current // 26) - 1
    return f"Room {label}"


def assign_rooms(events: Sequence[Event]) -> List[Dict[str, Any]]:
    """Assigns specific room names (e.g. 'Room A', 'Room B') to each event.

    Reuses existing freed rooms with the lowest alphanumeric identifier first.

    Args:
        events: A sequence of (start, end) time tuples.

    Returns:
        A list of dictionaries with event details and assigned room labels,
        in the original order of the input events.
    """
    if not events:
        return []

    # Pair each event with its original index to preserve order in the final output
    indexed_events = sorted(
        enumerate(events), key=lambda item: (item[1][0], item[1][1])
    )

    # active_rooms stores (end_time, room_id) in a min-heap
    active_rooms: List[Tuple[int, int]] = []

    # free_room_ids stores reusable room identifiers in a min-heap
    free_room_ids: List[int] = []

    max_room_allocated = 0
    results: List[Dict[str, Any]] = [{}] * len(events)

    for orig_idx, (start, end) in indexed_events:
        # Release all rooms whose meetings have finished at or before `start`
        while active_rooms and active_rooms[0][0] <= start:
            _, freed_room_id = heapq.heappop(active_rooms)
            heapq.heappush(free_room_ids, freed_room_id)

        # Reuse lowest available room ID, or allocate a new one
        if free_room_ids:
            room_id = heapq.heappop(free_room_ids)
        else:
            room_id = max_room_allocated
            max_room_allocated += 1

        heapq.heappush(active_rooms, (end, room_id))
        results[orig_idx] = {
            "event": (start, end),
            "room": _format_room_label(room_id),
            "room_id": room_id,
        }

    return results
