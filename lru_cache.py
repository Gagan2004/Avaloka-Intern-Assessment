"""Problem 1: LRU Cache Implementation

Logic and Approach:
-------------------
An LRU (Least Recently Used) cache requires O(1) performance for both `get` and `put`.

Why this combination of data structures was chosen:
1. Hash Map (dict): Provides O(1) average lookup for any key. However, a hash map
   alone does not maintain the temporal order of element access.
2. Doubly Linked List (DLL): Allows O(1) removal, insertion, and reordering of nodes,
   provided we hold a direct reference to the node.
3. Why not Singly Linked List: Removing a node from a singly linked list requires finding
   its predecessor, which takes O(N) traversal. A doubly linked list has `prev` and `next`,
   allowing instant O(1) detachment.
4. Dummy Sentinels (head & tail): Eliminate edge cases when inserting or evicting at boundaries.

Structure:
  [head (MRU)] <-> [Node] <-> ... <-> [Node] <-> [tail (LRU)]
"""

import threading
from typing import Any, Optional


class Node:
    """Doubly linked list node storing key, value, and pointers to neighbors."""

    def __init__(self, key: Any = 0, val: Any = 0):
        self.key: Any = key
        self.val: Any = val
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None


class LRUCache:
    """Least Recently Used Cache with O(1) get and put operations."""

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0.")
        self.capacity = capacity
        self.cache: dict[Any, Node] = {}

        # Dummy sentinels to simplify pointer boundary operations
        self.head = Node()  # Most recently used end
        self.tail = Node()  # Least recently used end
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Detaches a node from the doubly linked list in O(1)."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        """Inserts a node directly after the dummy head (MRU position) in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: Node) -> None:
        """Marks a node as most recently used."""
        self._remove(node)
        self._add_to_front(node)

    def _pop_tail(self) -> Node:
        """Evicts and returns the least recently used node in O(1)."""
        lru_node = self.tail.prev
        if lru_node is None or lru_node is self.head:
            raise RuntimeError("Cannot evict from an empty cache.")
        self._remove(lru_node)
        return lru_node

    def get(self, key: Any) -> Any:
        """Returns the value associated with key if found, otherwise -1.

        Marks key as most recently used.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_front(node)
        return node.val

    def put(self, key: Any, value: Any) -> None:
        """Adds or updates the key-value pair. Evicts LRU item if at capacity."""
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._move_to_front(node)
            return

        if len(self.cache) >= self.capacity:
            lru_node = self._pop_tail()
            del self.cache[lru_node.key]

        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_front(new_node)

    def __len__(self) -> int:
        return len(self.cache)


class ThreadSafeLRUCache(LRUCache):
    """Thread-safe variant using a Reentrant Lock (RLock)."""

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._lock = threading.RLock()

    def get(self, key: Any) -> Any:
        with self._lock:
            return super().get(key)

    def put(self, key: Any, value: Any) -> None:
        with self._lock:
            super().put(key, value)


if __name__ == "__main__":
    print("Testing LRUCache (capacity=2):")
    cache = LRUCache(2)
    cache.put(1, 10)
    cache.put(2, 20)
    print(f"get(1) -> {cache.get(1)} (expected 10)")

    cache.put(3, 30)  # Evicts key 2
    print(f"get(2) -> {cache.get(2)} (expected -1, evicted)")
    print(f"get(3) -> {cache.get(3)} (expected 30)")
    print(f"get(1) -> {cache.get(1)} (expected 10)")
