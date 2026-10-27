#include <algorithm>
#include <utility>
#include <vector>
using namespace std;

using Event = pair<int, int>;   // (start, end)

// Takes the vector by value so sorting works on a copy.
bool can_attend_all(vector<Event> events) {
    sort(events.begin(), events.end());
    for (size_t i = 1; i < events.size(); ++i)
        if (events[i].first < events[i - 1].second)   // strict: adjacent is OK
            return false;
    return true;
}

int min_rooms_required(const vector<Event>& events) {
    if (events.empty()) return 0;

    vector<int> starts, ends;
    starts.reserve(events.size());
    ends.reserve(events.size());
    for (const auto& [s, e] : events) {
        starts.push_back(s);
        ends.push_back(e);
    }
    sort(starts.begin(), starts.end());
    sort(ends.begin(), ends.end());

    int rooms = 0;
    size_t j = 0;                      // earliest end not yet matched
    for (int s : starts) {
        if (s >= ends[j]) ++j;         // a room freed up (adjacent counts as free)
        else ++rooms;                  // all rooms busy, open another
    }
    return rooms;
}