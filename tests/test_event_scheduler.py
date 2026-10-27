"""Unit tests for Event Scheduler functions."""

import pytest
from solutions.event_scheduler import can_attend_all, min_rooms_required, assign_rooms


class TestCanAttendAll:
    def test_empty_and_single(self):
        assert can_attend_all([]) is True
        assert can_attend_all([(10, 12)]) is True

    def test_adjacent_events_no_overlap(self):
        # Per prompt: adjacent events where end equals start are not considered overlaps
        events = [(9, 10), (10, 11), (11, 12)]
        assert can_attend_all(events) is True

    def test_overlapping_events(self):
        events = [(9, 11), (10, 12), (11, 13)]
        assert can_attend_all(events) is False

    def test_unsorted_events(self):
        events = [(12, 13), (9, 10), (10, 11)]
        assert can_attend_all(events) is True

    def test_nested_events(self):
        events = [(1, 10), (2, 5)]
        assert can_attend_all(events) is False


class TestMinRoomsRequired:
    def test_empty_and_single(self):
        assert min_rooms_required([]) == 0
        assert min_rooms_required([(9, 10)]) == 1

    def test_adjacent_events_reusing_room(self):
        events = [(9, 10), (10, 11), (11, 12)]
        assert min_rooms_required(events) == 1

    def test_overlapping_events(self):
        events = [(9, 11), (10, 12), (11, 13)]
        assert min_rooms_required(events) == 2

    def test_multiple_overlaps(self):
        # (0, 30) spans across (5, 10) and (15, 20)
        events = [(0, 30), (5, 10), (15, 20)]
        assert min_rooms_required(events) == 2

    def test_simultaneous_starts(self):
        events = [(1, 5), (1, 5), (1, 5)]
        assert min_rooms_required(events) == 3


class TestAssignRooms:
    def test_empty_events(self):
        assert assign_rooms([]) == []

    def test_room_assignment_labels_and_reuse(self):
        events = [(0, 30), (5, 10), (15, 20)]
        assignments = assign_rooms(events)
        assert len(assignments) == 3

        # (0, 30) gets Room A
        assert assignments[0]["event"] == (0, 30)
        assert assignments[0]["room"] == "Room A"

        # (5, 10) gets Room B because Room A is busy
        assert assignments[1]["event"] == (5, 10)
        assert assignments[1]["room"] == "Room B"

        # (15, 20) should reuse Room B because meeting (5, 10) finished
        assert assignments[2]["event"] == (15, 20)
        assert assignments[2]["room"] == "Room B"

    def test_no_room_conflict(self):
        events = [(1, 4), (2, 5), (4, 6), (5, 7), (6, 8)]
        assignments = assign_rooms(events)

        # Ensure no two events assigned to the same room overlap
        room_events = {}
        for a in assignments:
            r = a["room"]
            start, end = a["event"]
            if r not in room_events:
                room_events[r] = []
            for prev_start, prev_end in room_events[r]:
                assert not (start < prev_end and prev_start < end)
            room_events[r].append((start, end))
