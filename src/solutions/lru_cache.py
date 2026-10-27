"""LRU Cache Implementation.

This module implements a Least Recently Used (LRU) Cache supporting:
- get(key): O(1) lookup and marks key as recently used.
- put(key, value): O(1) insert/update and evicts the least recently used item
  when capacity is reached.

Additionally provides a thread-safe variant `ThreadSafeLRUCache` using `threading.RLock`.
"""

import threading
from typing import Any, Optional


class Node:
    """Doubly linked list node storing key, value, and neighbor pointers."""

    def __init__(self, key: Any = 0, val: Any = 0):
        self.key: Any = key
        self.val: Any = val
        self.prev: Optional["Node"] = None
        self.next: Optional["Node"] = None

    def __repr__(self) -> str:
        return f"Node(key={self.key!r}, val={self.val!r})"


class LRUCache:
    """Least Recently Used (LRU) Cache with O(1) get and put operations.

    Uses a Hash Map for O(1) key lookups and a Doubly Linked List with
    dummy head and tail sentinels to achieve O(1) recency updates and evictions.
    """

    def __init__(self, capacity: int):
        """Initializes the LRU Cache with a fixed capacity.

        Args:
            capacity: Maximum number of items the cache can hold (must be >= 1).

        Raises:
            ValueError: If capacity is less than 1.
        """
        if capacity <= 0:
            raise ValueError("Capacity must be greater than 0.")
        self.capacity: int = capacity
        self.cache: dict[Any, Node] = {}

        # Dummy sentinel nodes simplify insertion and deletion boundary logic
        self.head: Node = Node()  # MRU end
        self.tail: Node = Node()  # LRU end
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Detaches an existing node from the doubly linked list in O(1)."""
        prev_node = node.prev
        next_node = node.next
        if prev_node and next_node:
            prev_node.next = next_node
            next_node.prev = prev_node

    def _add_to_front(self, node: Node) -> None:
        """Inserts a node immediately after the dummy head (MRU position) in O(1)."""
        node.next = self.head.next
        node.prev = self.head
        if self.head.next:
            self.head.next.prev = node
        self.head.next = node

    def _move_to_front(self, node: Node) -> None:
        """Marks an existing node as most recently used."""
        self._remove(node)
        self._add_to_front(node)

    def _pop_tail(self) -> Node:
        """Removes and returns the least recently used node (preceding tail) in O(1)."""
        lru_node = self.tail.prev
        if lru_node is None or lru_node is self.head:
            raise RuntimeError("Cannot evict from an empty cache list.")
        self._remove(lru_node)
        return lru_node

    def get(self, key: Any) -> Any:
        """Returns the value associated with key if it exists, otherwise -1.

        Marks the key as most recently used on access.
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_front(node)
        return node.val

    def put(self, key: Any, value: Any) -> None:
        """Adds or updates the key-value pair.

        If key already exists, updates value and marks it as recently used.
        If cache is at capacity, evicts the least recently used item first.
        """
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
        """Returns current number of items stored in the cache."""
        return len(self.cache)

    def __contains__(self, key: Any) -> bool:
        """Checks if key is present without updating recency."""
        return key in self.cache


class ThreadSafeLRUCache(LRUCache):
    """Thread-safe wrapper around LRUCache using a Reentrant Lock (RLock)."""

    def __init__(self, capacity: int):
        super().__init__(capacity)
        self._lock = threading.RLock()

    def get(self, key: Any) -> Any:
        with self._lock:
            return super().get(key)

    def put(self, key: Any, value: Any) -> None:
        with self._lock:
            super().put(key, value)

    def __len__(self) -> int:
        with self._lock:
            return super().__len__()

    def __contains__(self, key: Any) -> bool:
        with self._lock:
            return super().__contains__(key)
