#ifndef EVENT_SCHEDULER_H
#define EVENT_SCHEDULER_H

/**
 * Problem 2: Event Scheduler Implementation (C++)
 *
 * Logic and Approach:
 * -------------------
 * 1. can_attend_all(events):
 *    - Sort intervals chronologically by start time.
 *    - Compare each interval with the preceding one: if curr_start < prev_end, return false.
 *    - Note: Adjacent events where prev_end == curr_start are not considered overlaps.
 *    - If no overlap exists across the sequence, return true.
 *
 * 2. min_rooms_required(events):
 *    - Minimum rooms needed equals the peak number of concurrent overlapping events.
 *    - Sort intervals by start time.
 *    - Use a min-heap (std::priority_queue with std::greater) to track active meeting end times.
 *      The top of the heap is the earliest ending meeting.
 *    - For each event:
 *        - If min_heap.top() <= start, that meeting is over; pop it (reuse room).
 *        - Push the new meeting's end time onto the heap.
 *    - The heap size after processing all events is the minimum rooms required.
 *
 * 3. Future Proofing: assign_rooms(events):
 *    - Assigns specific room names ("Room A", "Room B", etc.).
 *    - Reuses the lowest-indexed freed room number using an available-rooms min-heap.
 */

#include <algorithm>
#include <iostream>
#include <queue>
#include <string>
#include <utility>
#include <vector>

using Event = std::pair<int, int>;

struct EventAssignment {
    Event event;
    std::string room;
    int room_id;
};

/**
 * Returns true if all events can be attended without overlapping.
 */
inline bool can_attend_all(std::vector<Event> events) {
    if (events.size() <= 1) {
        return true;
    }

    std::sort(events.begin(), events.end(), [](const Event& a, const Event& b) {
        return a.first < b.first;
    });

    for (size_t i = 1; i < events.size(); ++i) {
        // Overlap occurs strictly when current start < previous end
        if (events[i].first < events[i - 1].second) {
            return false;
        }
    }

    return true;
}

/**
 * Calculates the minimum meeting rooms required simultaneously.
 */
inline int min_rooms_required(std::vector<Event> events) {
    if (events.empty()) {
        return 0;
    }

    std::sort(events.begin(), events.end(), [](const Event& a, const Event& b) {
        return a.first < b.first;
    });

    // Min-heap tracking the end times of active meetings
    std::priority_queue<int, std::vector<int>, std::greater<int>> rooms_heap;

    for (const auto& ev : events) {
        int start = ev.first;
        int end = ev.second;

        // If earliest meeting ended at or before current start, reuse room
        if (!rooms_heap.empty() && rooms_heap.top() <= start) {
            rooms_heap.pop();
        }

        rooms_heap.push(end);
    }

    return static_cast<int>(rooms_heap.size());
}

/**
 * Converts index 0 -> "Room A", 1 -> "Room B", 26 -> "Room AA", etc.
 */
inline std::string format_room_label(int index) {
    std::string label = "";
    int curr = index;
    while (curr >= 0) {
        label = static_cast<char>('A' + (curr % 26)) + label;
        curr = (curr / 26) - 1;
    }
    return "Room " + label;
}

/**
 * Assigns specific room labels ("Room A", "Room B") to each event,
 * preserving original input order.
 */
inline std::vector<EventAssignment> assign_rooms(const std::vector<Event>& events) {
    if (events.empty()) {
        return {};
    }

    // Keep track of original indices
    struct IndexedEvent {
        size_t orig_idx;
        Event event;
    };

    std::vector<IndexedEvent> indexed;
    indexed.reserve(events.size());
    for (size_t i = 0; i < events.size(); ++i) {
        indexed.push_back({i, events[i]});
    }

    std::sort(indexed.begin(), indexed.end(), [](const IndexedEvent& a, const IndexedEvent& b) {
        if (a.event.first != b.event.first) {
            return a.event.first < b.event.first;
        }
        return a.event.second < b.event.second;
    });

    // Min-heap of active rooms: stores pair<end_time, room_id>
    using ActiveRoom = std::pair<int, int>;
    std::priority_queue<ActiveRoom, std::vector<ActiveRoom>, std::greater<ActiveRoom>> active_rooms;

    // Min-heap of available reusable room IDs
    std::priority_queue<int, std::vector<int>, std::greater<int>> free_room_ids;

    int max_allocated = 0;
    std::vector<EventAssignment> results(events.size());

    for (const auto& item : indexed) {
        int start = item.event.first;
        int end = item.event.second;

        // Release rooms whose meetings have finished
        while (!active_rooms.empty() && active_rooms.top().first <= start) {
            free_room_ids.push(active_rooms.top().second);
            active_rooms.pop();
        }

        // Reuse lowest available room ID or create a new one
        int room_id;
        if (!free_room_ids.empty()) {
            room_id = free_room_ids.top();
            free_room_ids.pop();
        } else {
            room_id = max_allocated++;
        }

        active_rooms.push({end, room_id});
        results[item.orig_idx] = {item.event, format_room_label(room_id), room_id};
    }

    return results;
}

#endif // EVENT_SCHEDULER_H
