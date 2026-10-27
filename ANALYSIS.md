# Final Discussion & Analysis

## 1. Time & Space Complexity

### Problem 1: LRU Cache

| Function | Time Complexity | Space Complexity |
| :--- | :---: | :---: |
| `LRUCache(cap)` | $O(1)$ | $O(1)$ |
| `get(key)` | $O(1)$ average / $O(n)$ worst-case | $O(1)$ extra |
| `put(key, val)` | $O(1)$ amortized / $O(n)$ worst-case | $O(1)$ extra |
| `unlink` / `pushFront` | $O(1)$ | $O(1)$ |
| `~LRUCache()` | $O(n)$ | $O(1)$ |
| **Overall Cache** | — | **$O(C)$** capacity |

- **Hash Map ($O(1)$ avg):** Lookup and insertion are constant time on average; pathological collisions or rehashing can degrade to $O(n)$.
- **Doubly Linked List (Strict $O(1)$):** Pointer rewiring (`unlink`, `pushFront`, tail eviction) is always a fixed number of operations.

### Problem 2: Event Scheduler

| Function | Time Complexity | Space Complexity |
| :--- | :---: | :---: |
| `can_attend_all` | $O(n \log n)$ | $O(n)$ for copy ($O(1)$ extra if sorted in place) |
| `min_rooms_required` | $O(n \log n)$ | $O(n)$ for starts and ends arrays |
| `assign_rooms` | $O(n \log n)$ | $O(n)$ for index and heap tracking |

- Sorting intervals dominates at $O(n \log n)$. Sweeps and heap operations run in linear or amortized logarithmic time ($O(\log k)$ per event).

---

## 2. Trade-offs: Why Hash Map + Doubly Linked List?

Each data structure addresses the other's limitations:

- **Hash map alone:** $O(1)$ key lookup, but lacks temporal ordering. Identifying the oldest entry requires an $O(n)$ scan.
- **Linked list alone:** Preserves access order and allows $O(1)$ eviction at the tail, but finding an arbitrary key requires an $O(n)$ search.
- **Singly linked list:** Unlinking an arbitrary node requires its predecessor, which takes an $O(n)$ search from the head.
- **Combined:** The hash map jumps directly to the node in $O(1)$. Because the list is doubly linked, each node carries `prev` and `next`, enabling instant $O(1)$ detachment and front-insertion. Eviction is simply `tail.prev`.

**Costs & Trade-offs:**
- Extra memory overhead (two pointers per node plus hash bucket overhead).
- Pointer chasing causes lower CPU cache locality than contiguous arrays.

---

## 3. Future Proofing: Specific Room Allocation

The two-pointer counting sweep only finds the peak room count; it discards meeting identity and cannot name rooms. To assign specific rooms (e.g., `"Room A"`, `"Room B"`), we simulate the schedule using two min-heaps:

- **Busy heap** of `(end_time, room_id)`: Rooms in use, ordered by earliest finish time.
- **Free heap** of `room_id`: Available rooms, lowest ID on top (ensuring deterministic and contiguous reuse).

**Algorithm:**
1. Sort events chronologically by start time while tracking original indices.
2. For each event, pop all finished meetings (`end <= start`) from the busy heap and return their room IDs to the free heap (`<=` allows adjacent events to share rooms).
3. Assign the lowest available room from the free heap (or increment a room counter if empty).
4. Record the assignment and push `(end, room_id)` onto the busy heap.

*Extension:* For room constraints (capacity, equipment), maintain categorized free pools or query a capacity-sorted set using `lower_bound`.

---

## 4. Concurrency: Making the LRU Cache Thread-Safe

### Key Insight
`get()` is **not a read-only operation** in an LRU cache—it mutates the doubly linked list by promoting the accessed node to MRU. Therefore, reader-writer locks (`std::shared_mutex`) offer no concurrency benefit because reads still require exclusive write access to reorder pointers.

### Synchronization Strategies
1. **Coarse-Grained Mutex (Baseline):**
   Wrap `get` and `put` with a single `std::mutex` and `std::lock_guard`. Operations remain $O(1)$, but all threads serialize.
2. **Lock Striping / Sharding (High Contention):**
   Split into $N$ independent cache shards via `hash(key) % N`, each with its own mutex. Reduces contention significantly at the cost of localized per-shard eviction.
3. **Deferred Recency Updates:**
   Record read accesses in a lock-free buffer and batch-apply list reordering under the lock periodically (pattern used by high-performance caches like Caffeine).
4. **Approximate CLOCK Policy:**
   Replace linked-list pointer moves with an atomic flag (`std::atomic<bool> accessed`) per node, cleared during circular eviction sweeps.

### Correctness Rules
- Never invoke user callbacks or I/O while holding cache mutexes.
- Coalesce concurrent cache misses (single-flight) to prevent thundering herds on backend storage.
- Delete copy constructor and assignment operator (`= delete`) to prevent accidental pointer sharing.
