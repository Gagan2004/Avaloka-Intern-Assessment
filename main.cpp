/**
 * Main entry point demonstrating Problem 1 (LRU Cache) and Problem 2 (Event Scheduler) in C++.
 *
 * Compilation:
 *   g++ -std=c++17 main.cpp -o main
 *   ./main
 *
 * Or using MSVC:
 *   cl /std:c++17 /EHsc main.cpp
 *   main.exe
 */

#include <cassert>
#include <iostream>
#include <thread>
#include <vector>

#include "lru_cache.h"
#include "event_scheduler.h"

void test_and_demo_lru_cache() {
    std::cout << "=======================================================\n";
    std::cout << "Problem 1: LRU Cache Demonstration & Verification\n";
    std::cout << "=======================================================\n";

    LRUCache<int, int> cache(2);
    std::cout << "Initialized LRUCache with capacity = 2\n\n";

    std::cout << "1. put(1, 10)\n";
    cache.put(1, 10);
    std::cout << "2. put(2, 20)\n";
    cache.put(2, 20);

    int val1 = cache.get(1);
    std::cout << "3. get(1) -> " << val1 << " (expected: 10, marks key 1 as MRU)\n";
    assert(val1 == 10);

    std::cout << "4. put(3, 30) -> Cache full; evicts key 2 (LRU)\n";
    cache.put(3, 30);

    int val2 = cache.get(2);
    std::cout << "5. get(2) -> " << val2 << " (expected: -1, evicted)\n";
    assert(val2 == -1);

    int val3 = cache.get(3);
    std::cout << "6. get(3) -> " << val3 << " (expected: 30)\n";
    assert(val3 == 30);

    val1 = cache.get(1);
    std::cout << "7. get(1) -> " << val1 << " (expected: 10)\n";
    assert(val1 == 10);

    // Multithreaded concurrency verification
    std::cout << "\nTesting ThreadSafeLRUCache across concurrent threads...\n";
    ThreadSafeLRUCache<int, int> safe_cache(20);
    std::vector<std::thread> workers;
    for (int t = 0; t < 5; ++t) {
        workers.emplace_back([&safe_cache, t]() {
            for (int i = 0; i < 50; ++i) {
                safe_cache.put(t * 100 + i, i);
                safe_cache.get(t * 100 + i);
            }
        });
    }
    for (auto& w : workers) {
        w.join();
    }
    std::cout << "ThreadSafeLRUCache test passed successfully! Final cache size: "
              << safe_cache.size() << " (<= 20)\n";
    assert(safe_cache.size() <= 20);
}

void test_and_demo_event_scheduler() {
    std::cout << "\n=======================================================\n";
    std::cout << "Problem 2: Event Scheduler Demonstration & Verification\n";
    std::cout << "=======================================================\n";

    // Example 1: Adjacent events (end == start, no overlap)
    std::vector<Event> events_1 = {{9, 10}, {10, 11}, {11, 12}};
    bool can_attend_1 = can_attend_all(events_1);
    int rooms_1 = min_rooms_required(events_1);
    std::cout << "\nEvents 1 (adjacent): [(9, 10), (10, 11), (11, 12)]\n";
    std::cout << "  can_attend_all: " << (can_attend_1 ? "True" : "False") << " (Expected: True)\n";
    std::cout << "  min_rooms_required: " << rooms_1 << " (Expected: 1)\n";
    assert(can_attend_1 == true);
    assert(rooms_1 == 1);

    // Example 2: Overlapping events
    std::vector<Event> events_2 = {{9, 11}, {10, 12}, {11, 13}};
    bool can_attend_2 = can_attend_all(events_2);
    int rooms_2 = min_rooms_required(events_2);
    std::cout << "\nEvents 2 (overlapping): [(9, 11), (10, 12), (11, 13)]\n";
    std::cout << "  can_attend_all: " << (can_attend_2 ? "True" : "False") << " (Expected: False)\n";
    std::cout << "  min_rooms_required: " << rooms_2 << " (Expected: 2)\n";
    assert(can_attend_2 == false);
    assert(rooms_2 == 2);

    // Example 3: Multiple overlaps and room assignment
    std::vector<Event> events_3 = {{0, 30}, {5, 10}, {15, 20}, {25, 35}};
    bool can_attend_3 = can_attend_all(events_3);
    int rooms_3 = min_rooms_required(events_3);
    std::cout << "\nEvents 3 (multiple overlaps): [(0, 30), (5, 10), (15, 20), (25, 35)]\n";
    std::cout << "  can_attend_all: " << (can_attend_3 ? "True" : "False") << " (Expected: False)\n";
    std::cout << "  min_rooms_required: " << rooms_3 << " (Expected: 2)\n";
    assert(can_attend_3 == false);
    assert(rooms_3 == 2);

    std::cout << "\nFuture-Proofing: Specific Room Allocation:\n";
    std::vector<EventAssignment> assignments = assign_rooms(events_3);
    for (const auto& a : assignments) {
        std::cout << "  Meeting (" << a.event.first << ", " << a.event.second
                  << ") -> Assigned to: " << a.room << "\n";
    }

    assert(assignments[0].room == "Room A");
    assert(assignments[1].room == "Room B");
    assert(assignments[2].room == "Room B"); // Room B reused after (5, 10) finishes
}

int main() {
    test_and_demo_lru_cache();
    test_and_demo_event_scheduler();

    std::cout << "\n=======================================================\n";
    std::cout << "ALL DEMOS AND ASSERTIONS PASSED SUCCESSFULLY!\n";
    std::cout << "=======================================================\n";
    return 0;
}
