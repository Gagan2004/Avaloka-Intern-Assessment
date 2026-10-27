#ifndef LRU_CACHE_H
#define LRU_CACHE_H

/**
 * Problem 1: LRU Cache Implementation (C++)
 *
 * Logic and Approach:
 * -------------------
 * An LRU (Least Recently Used) cache requires O(1) performance for both `get` and `put`.
 *
 * Data Structures Chosen:
 * 1. std::unordered_map<Key, Node*>:
 *    - Provides O(1) average-time lookup for any key.
 *    - Storing pointers directly to doubly linked list nodes allows immediate access.
 *
 * 2. Custom Doubly Linked List (DLL):
 *    - Maintains access order: most recently used (MRU) at the front, least recently used (LRU) at the back.
 *    - Allows O(1) detachment, insertion, and eviction without shifting elements.
 *
 * Why not a Singly Linked List:
 *    - In a singly linked list, deleting a node requires finding its predecessor, which is an O(N) traversal.
 *    - A doubly linked list has `prev` and `next`, enabling instant O(1) deletion given the node pointer.
 *
 * Dummy Sentinels (head & tail):
 *    - Head and tail sentinel nodes eliminate boundary edge-case checks (e.g., empty list, single element).
 *
 * Memory Management:
 *    - Destructor safely cleans up all allocated nodes to prevent memory leaks.
 */

#include <iostream>
#include <mutex>
#include <stdexcept>
#include <unordered_map>

template <typename Key = int, typename Value = int>
class LRUCache {
public:
    struct Node {
        Key key;
        Value val;
        Node* prev;
        Node* next;

        Node(Key k = Key(), Value v = Value())
            : key(k), val(v), prev(nullptr), next(nullptr) {}
    };

    explicit LRUCache(int cap) : capacity(cap) {
        if (capacity <= 0) {
            throw std::invalid_argument("Capacity must be greater than 0.");
        }
        // Initialize sentinels
        head = new Node();
        tail = new Node();
        head->next = tail;
        tail->prev = head;
    }

    virtual ~LRUCache() {
        Node* curr = head;
        while (curr != nullptr) {
            Node* next_node = curr->next;
            delete curr;
            curr = next_node;
        }
    }

    // Disable copy semantics to prevent double frees
    LRUCache(const LRUCache&) = delete;
    LRUCache& operator=(const LRUCache&) = delete;

    /**
     * Returns the value for key if present (marking it MRU), otherwise -1.
     */
    virtual Value get(const Key& key) {
        auto it = cache.find(key);
        if (it == cache.end()) {
            return -1;
        }

        Node* node = it->second;
        moveToFront(node);
        return node->val;
    }

    /**
     * Inserts or updates the key-value pair.
     * Evicts the least recently used item if capacity is exceeded.
     */
    virtual void put(const Key& key, const Value& value) {
        auto it = cache.find(key);
        if (it != cache.end()) {
            Node* node = it->second;
            node->val = value;
            moveToFront(node);
            return;
        }

        if (static_cast<int>(cache.size()) >= capacity) {
            Node* lru = popTail();
            cache.erase(lru->key);
            delete lru;
        }

        Node* new_node = new Node(key, value);
        cache[key] = new_node;
        addToFront(new_node);
    }

    int size() const {
        return static_cast<int>(cache.size());
    }

protected:
    int capacity;
    std::unordered_map<Key, Node*> cache;
    Node* head; // Sentinel: head->next is MRU
    Node* tail; // Sentinel: tail->prev is LRU

    void removeNode(Node* node) {
        node->prev->next = node->next;
        node->next->prev = node->prev;
    }

    void addToFront(Node* node) {
        node->next = head->next;
        node->prev = head;
        head->next->prev = node;
        head->next = node;
    }

    void moveToFront(Node* node) {
        removeNode(node);
        addToFront(node);
    }

    Node* popTail() {
        Node* lru = tail->prev;
        if (lru == head) {
            throw std::runtime_error("Attempted eviction from empty cache.");
        }
        removeNode(lru);
        return lru;
    }
};

/**
 * Thread-safe wrapper around LRUCache using std::mutex.
 */
template <typename Key = int, typename Value = int>
class ThreadSafeLRUCache : public LRUCache<Key, Value> {
public:
    explicit ThreadSafeLRUCache(int cap) : LRUCache<Key, Value>(cap) {}

    Value get(const Key& key) override {
        std::lock_guard<std::mutex> lock(mtx);
        return LRUCache<Key, Value>::get(key);
    }

    void put(const Key& key, const Value& value) override {
        std::lock_guard<std::mutex> lock(mtx);
        LRUCache<Key, Value>::put(key, value);
    }

private:
    std::mutex mtx;
};

#endif // LRU_CACHE_H
