Approach. The cache has to do two things in constant time: find an entry by key, and know which entry was used least recently. No single structure does both... so I combine two.

An unordered_map<int, Node*> gives O(1)  time complexity lookup from a key to its node.
A doubly linked list keeps the entries in The order the nodes have been accesed. The most recently used node sits right after the HEAD sentinel, and the least recently used sits right before the TAIL sentinel.

The map and list work together. The map hands me the node directly (it stores the node reference as the value) , with no scanning. Because each node knows its own prev and next, I can unlink it and reinsert it at the front with a fixed number of pointer writes. That is how get marks a key as recently used. deletion is also O(1): the victim node is always tail_.prev, and since each node stores its own key, I can erase the matching map entry without searching.

 arrays can't be used instead of Doubly LL as moving an item to the front is O(n). In a singly linked list, unlinking a node needs its previous node, which takes an O(n) to find it. Sentinel head and tail nodes remove the special cases for an empty list or for operating on the first or last element.

#include <stdexcept>
#include <unordered_map>
using namespace std;

class LRUCache {
    struct Node {
        int key, val;
        Node *prev = nullptr, *next = nullptr;
        Node(int k = 0, int v = 0) : key(k), val(v) {}
    };

    int cap_;
    unordered_map<int, Node*> map_;
    Node head_, tail_;                       // sentinels

    void unlink(Node* n) {
        n->prev->next = n->next;
        n->next->prev = n->prev;
    }
    void pushFront(Node* n) {                // right after head_ = most recent
        n->prev = &head_;
        n->next = head_.next;
        head_.next->prev = n;
        head_.next = n;
    }

public:
    explicit LRUCache(int capacity) : cap_(capacity) {
        if (capacity <= 0) throw invalid_argument("capacity must be positive");
        head_.next = &tail_;
        tail_.prev = &head_;
    }
    ~LRUCache() {
        for (Node* c = head_.next; c != &tail_;) {
            Node* nx = c->next;
            delete c;
            c = nx;
        }
    }
    LRUCache(const LRUCache&) = delete;
    LRUCache& operator=(const LRUCache&) = delete;

    int get(int key) {
        auto it = map_.find(key);
        if (it == map_.end()) return -1;
        Node* n = it->second;
        unlink(n);                           // mark as recently used
        pushFront(n);
        return n->val;
    }

    void put(int key, int value) {
        auto it = map_.find(key);
        if (it != map_.end()) {              // update existing key
            Node* n = it->second;
            n->val = value;
            unlink(n);
            pushFront(n);
            return;
        }
        if (static_cast<int>(map_.size()) == cap_) {   // evict LRU
            Node* lru = tail_.prev;
            unlink(lru);
            map_.erase(lru->key);
            delete lru;
        }
        Node* n = new Node(key, value);
        map_[key] = n;
        pushFront(n);
    }
};