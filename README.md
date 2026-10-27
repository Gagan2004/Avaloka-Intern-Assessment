# LRU Cache & Event Scheduler

Concise, high-performance Python implementations for **LRU Cache** and **Event Scheduler** with explanations, complexities, trade-offs, and tests.

---

## Files

- **[`lru_cache.py`](lru_cache.py)**: LRU Cache implementation ($O(1)$ `get` & `put`) + `ThreadSafeLRUCache`.
- **[`event_scheduler.py`](event_scheduler.py)**: `can_attend_all`, `min_rooms_required` (min-heap), and `assign_rooms`.
- **[`main.py`](main.py)**: Runs a demo of both problems.
- **[`test_solutions.py`](test_solutions.py)**: Unit and concurrency tests (using Python's built-in `unittest`).

---

## Running the Code

```bash
# Run the demo
python main.py

# Run the tests
python test_solutions.py
```

---

## Problem 1: LRU Cache

### Logic & Choice of Data Structures
- **Hash Map (`dict`):** Provides $O(1)$ average-time lookup for any key, but cannot track access order.
- **Doubly Linked List (DLL):** Maintains recency order ($MRU \leftrightarrow LRU$). Provides $O(1)$ insertion, deletion, and relocation once a node reference is held.
- **Why not Singly Linked List?** Deleting a node requires finding its predecessor, which takes $O(N)$ traversal.
- **Sentinels (dummy head/tail):** Eliminate edge-case checks for boundary insertions and deletions.

```
[head (MRU)] <-> [Node] <-> ... <-> [Node] <-> [tail (LRU)]
```

---

## Problem 2: Event Scheduler

### Logic & Room Requirement Calculation
1. **`can_attend_all(events)`**:
   - Sort intervals by start time.
   - For adjacent intervals, check if `curr_start < prev_end`. If true, an overlap exists (`False`).
   - Adjacent events where `prev_end == curr_start` are allowed.
2. **`min_rooms_required(events)`**:
   - Minimum rooms = peak overlapping meetings at any point in time.
   - Sort intervals by start time.
   - Maintain a **min-heap** containing end times of currently active meetings. The top of the heap is the earliest ending meeting.
   - If `heap[0] <= start`, that meeting is over; pop it and reuse the room.
   - Push the new meeting's end time.
   - The size of the heap after processing equals the minimum rooms required.

---

## Discussion & Analysis

### 1. Time & Space Complexity

| Function | Time | Space | Explanation |
| :--- | :---: | :---: | :--- |
| `LRUCache.get` | $O(1)$ | $O(1)$ | $O(1)$ hash map lookup + pointer updates. |
| `LRUCache.put` | $O(1)$ | $O(1)$ | $O(1)$ map insert/delete + pointer updates ($O(C)$ total cache capacity). |
| `can_attend_all` | $O(N \log N)$ | $O(N)$ | Sorting $N$ events takes $O(N \log N)$; linear scan takes $O(N)$. |
| `min_rooms_required` | $O(N \log N)$ | $O(N)$ | Sorting takes $O(N \log N)$; heap pushes/pops take $O(N \log K)$. |
| `assign_rooms` | $O(N \log N)$ | $O(N)$ | Sorting plus min-heap room pooling. |

### 2. Trade-offs (Hash Map + Doubly Linked List)
- **Strengths:** Meets the strict $O(1)$ time requirement for all operations.
- **Trade-off:** Higher memory overhead compared to an array, as each node must store pointers to `prev`, `next`, `key`, and `val`, plus hash table references.

### 3. Future Proofing (Specific Room Allocation)
Implemented in `assign_rooms()`:
- Maintains a min-heap of free room IDs (`"Room A"`, `"Room B"`, etc.) alongside the active meetings heap.
- When a meeting finishes, its room ID is returned to the pool and immediately prioritized for reuse.

### 4. Concurrency (Thread Safety)
Implemented in `ThreadSafeLRUCache`:
- Uses `threading.RLock()` across `get()` and `put()`.
- Note: In an LRU cache, `get()` mutates internal state (recency order), so standard Read-Write locks still require write locks on reads unless decoupled via read buffers (e.g., Caffeine-style ring buffers).
