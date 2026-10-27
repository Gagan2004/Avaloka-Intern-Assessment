# High-Performance Algorithms: LRU Cache & Event Scheduler

Production-grade, modular, and fully tested Python implementations for:
1. **Least Recently Used (LRU) Cache** with strict $O(1)$ operations and thread-safe extensions.
2. **Event Scheduler** with overlap detection, min-room allocation using min-heaps, and room assignment future-proofing.

---

## Repository Structure

```text
.
├── .github/
│   └── workflows/
│       └── ci.yml             # GitHub Actions CI for multi-version testing
├── src/
│   ├── main.py                # Demonstration entry point
│   └── solutions/
│       ├── __init__.py        # Package exports
│       ├── lru_cache.py       # LRUCache & ThreadSafeLRUCache implementations
│       └── event_scheduler.py # can_attend_all, min_rooms_required, assign_rooms
├── tests/
│   ├── __init__.py
│   ├── test_lru_cache.py      # Full unit tests & concurrency stress tests
│   └── test_event_scheduler.py# Interval tests, edge cases, and assignment tests
├── .gitignore                 # Standard Python gitignore
├── pyproject.toml             # Project metadata and pytest configuration
└── README.md                  # Comprehensive technical documentation
```

---

## Problem 1: LRU Cache Implementation

### Problem Statement
Design and implement an LRU cache with:
- `get(key)`: Returns the value if present, else `-1`. Marks key as recently used.
- `put(key, value)`: Inserts or updates the key-value pair. If capacity is exceeded, evicts the least recently used item.
- **Constraint:** Both `get` and `put` must run in $O(1)$ average time.

### Why Hash Map + Doubly Linked List?
- **Hash Map:** Gives $O(1)$ lookup time for keys, but does not preserve access order.
- **Doubly Linked List (DLL):** Enables $O(1)$ removal and insertion anywhere in the chain once a pointer to the node is known.
- **Why not a Singly Linked List?** Deleting an arbitrary node from a singly linked list requires finding its predecessor, taking $O(N)$ time.
- **Sentinels:** Uses dummy `head` and `tail` nodes to eliminate edge cases when inserting or removing elements at boundaries.

```
[head (sentinel)] <-> [Node(MRU)] <-> ... <-> [Node(LRU)] <-> [tail (sentinel)]
```

### Thread-Safe LRU Cache
The repository also includes `ThreadSafeLRUCache`, which uses `threading.RLock()` to guarantee thread safety across concurrent reader and writer threads.

---

## Problem 2: Event Scheduler

### Problem Statement
Given a list of meeting intervals `(start_time, end_time)`:
- `can_attend_all(events)`: Returns `True` if all events can be attended without overlaps, `False` otherwise.
- `min_rooms_required(events)`: Returns the minimum number of meeting rooms required simultaneously.
- **Constraint:** Adjacent events (where `prev_end == curr_start`) are not considered overlaps.

### Algorithmic Approach
1. **`can_attend_all`:**
   - Sort events chronologically by start time.
   - Linearly check if `curr_start < prev_end`. If true, collision detected -> `False`.
2. **`min_rooms_required`:**
   - Sort events by start time.
   - Maintain a min-heap containing the end times of ongoing meetings across all active rooms.
   - The root of the heap (`heap[0]`) is the meeting ending earliest.
   - If `heap[0] <= start`, the room is freed and reused (`heapq.heappop`).
   - Push the new meeting's end time (`heapq.heappush`).
   - Peak concurrent rooms equals the final size of the heap.

### Future Proofing: Named Room Assignment
`assign_rooms(events)` labels specific rooms (`"Room A"`, `"Room B"`, etc.) and reuses the lowest-index available room whenever a meeting finishes, ensuring optimal room utilization.

---

## Complexity Analysis

| Function | Time Complexity | Auxiliary Space | Explanation |
| :--- | :---: | :---: | :--- |
| `LRUCache.get` | $O(1)$ | $O(1)$ | Hash map lookup is $O(1)$; pointer reassignment in DLL is $O(1)$. |
| `LRUCache.put` | $O(1)$ | $O(1)$ | Map insertions/evictions and DLL head/tail adjustments are all $O(1)$. Overall memory is $O(C)$ where $C$ is capacity. |
| `can_attend_all` | $O(N \log N)$ | $O(N)$ | Sorting $N$ intervals takes $O(N \log N)$; linear scan takes $O(N)$. |
| `min_rooms_required` | $O(N \log N)$ | $O(N)$ | Sorting $N$ events takes $O(N \log N)$. $N$ heap operations take $O(\log K)$ where $K \le N$ is the maximum number of concurrent rooms. |
| `assign_rooms` | $O(N \log N)$ | $O(N)$ | Sorting plus min-heap room pooling and assignments. |

---

## Quick Start & Testing

### 1. Run the Demo
```bash
python src/main.py
```

### 2. Run the Test Suite
```bash
pytest
```
All 20 unit and concurrency tests will run automatically with verbose output.

### 3. CI/CD
GitHub Actions workflow is included at `.github/workflows/ci.yml` to automatically validate pushes and pull requests across Python versions 3.10 through 3.13.
