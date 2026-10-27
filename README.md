# High-Performance C++ Algorithms: LRU Cache & Event Scheduler

Clean, modern, and production-ready **C++17** implementations of:
1. **LRU Cache**: Strict $O(1)$ `get` and `put` operations using `std::unordered_map` and a custom Doubly Linked List with dummy sentinels, plus a thread-safe wrapper.
2. **Event Scheduler**: Interval overlap checking (`can_attend_all`), room requirement calculation via min-heap (`min_rooms_required`), and future-proofing room assignments (`assign_rooms`).

All files reside cleanly on the **root level**.

---

## Files

- **[`lru_cache.h`](lru_cache.h)**: Generic `LRUCache<Key, Value>` and `ThreadSafeLRUCache` implementation.
- **[`event_scheduler.h`](event_scheduler.h)**: `can_attend_all`, `min_rooms_required`, and `assign_rooms`.
- **[`main.cpp`](main.cpp)**: Demonstrations and self-verifying test assertions for both problems.
- **[`README.md`](README.md)**: Logic explanations, complexities, trade-offs, and compilation instructions.
- **[`.gitignore`](.gitignore)**: Standard C++ build artifact ignore list.

---

## Build & Run Instructions

Any modern C++ compiler (C++17 or later) can compile the code in one command:

### GCC / Clang
```bash
g++ -std=c++17 main.cpp -o main
./main
```

### MSVC (Windows Visual Studio Command Prompt)
```cmd
cl /std:c++17 /EHsc main.cpp
main.exe
```

---

## Problem 1: LRU Cache

### Logic & Choice of Data Structures
- **`std::unordered_map<Key, Node*>`**: Provides $O(1)$ average-time lookup for any key. Storing raw pointers to nodes allows direct access without list traversal.
- **Custom Doubly Linked List (DLL)**: Maintains temporal access order ($MRU \leftrightarrow LRU$). Enables $O(1)$ node detachment, front-insertion, and eviction.
- **Why not a Singly Linked List?** Deleting an arbitrary node from a singly linked list requires finding its predecessor node, requiring an $O(N)$ traversal. A doubly linked list has `prev` and `next`, enabling instant $O(1)$ deletion.
- **Dummy Sentinels (`head` and `tail`)**: Eliminates edge-case checks for empty lists or boundary operations.

```
[head (sentinel)] <-> [Node(MRU)] <-> ... <-> [Node(LRU)] <-> [tail (sentinel)]
```

---

## Problem 2: Event Scheduler

### Logic & Room Requirement Calculation
1. **`can_attend_all(events)`**:
   - Sort intervals by start time.
   - Linearly verify that for all adjacent meetings, `curr_start >= prev_end`.
   - Adjacent events where `prev_end == curr_start` are allowed (no overlap).
2. **`min_rooms_required(events)`**:
   - The minimum rooms required equals the peak number of concurrent overlapping meetings.
   - Sort intervals by start time.
   - Maintain a **min-heap** (`std::priority_queue<int, std::vector<int>, std::greater<int>>`) storing end times of active meetings.
   - The root of the heap (`heap.top()`) is always the meeting ending earliest.
   - If `heap.top() <= start`, that meeting has finished; pop it from the heap and reuse the room.
   - Push the current meeting's end time.
   - Heap size after processing all events equals the minimum rooms required.

---

## Discussion & Analysis

### 1. Time & Space Complexity

| Function | Time Complexity | Auxiliary Space | Explanation |
| :--- | :---: | :---: | :--- |
| `LRUCache::get` | $O(1)$ | $O(1)$ | Hash map lookup is $O(1)$; pointer rewiring in DLL is $O(1)$. |
| `LRUCache::put` | $O(1)$ | $O(1)$ | Hash map insert/delete and DLL front/tail manipulation are $O(1)$. Overall memory is $O(C)$ where $C$ is capacity. |
| `can_attend_all` | $O(N \log N)$ | $O(1)$ aux / $O(N)$ | Sorting $N$ events takes $O(N \log N)$; linear scan takes $O(N)$. |
| `min_rooms_required` | $O(N \log N)$ | $O(N)$ | Sorting takes $O(N \log N)$; each heap push/pop takes $O(\log K)$ where $K \le N$ is the number of concurrent rooms. |
| `assign_rooms` | $O(N \log N)$ | $O(N)$ | Sorting plus min-heap room ID pooling. |

### 2. Trade-offs (Hash Map + Doubly Linked List)
- **Advantages:** Strictly satisfies the $O(1)$ time complexity requirement for both reads and writes.
- **Trade-offs:** Higher pointer memory footprint: each node stores `key`, `val`, `prev`, and `next` pointers, along with the hash bucket table overhead in `std::unordered_map`.

### 3. Future Proofing (Specific Room Allocation)
Implemented in `assign_rooms`:
- Maintains a min-heap of free room IDs (`0 -> "Room A"`, `1 -> "Room B"`).
- When any active meeting finishes, its room ID is returned to the available pool so that lower-indexed rooms are consistently prioritized and reused.

### 4. Concurrency (Thread Safety)
Implemented in `ThreadSafeLRUCache`:
- Uses `std::mutex` and `std::lock_guard` across `get()` and `put()`.
- Note: In an LRU cache, `get()` **mutates** list state (moves node to MRU), meaning standard Read-Write locks (`std::shared_mutex`) would still require an exclusive write lock on reads unless decoupled via concurrent read buffers.
