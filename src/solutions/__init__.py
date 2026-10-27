"""Solutions package for LRU Cache and Event Scheduler."""

from solutions.lru_cache import LRUCache, ThreadSafeLRUCache
from solutions.event_scheduler import can_attend_all, min_rooms_required, assign_rooms

__all__ = [
    "LRUCache",
    "ThreadSafeLRUCache",
    "can_attend_all",
    "min_rooms_required",
    "assign_rooms",
]
