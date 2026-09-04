#include <iostream>
#include <vector>
#include <algorithm>
using namespace std;
struct Meeting {
    int start;
    int end;
};
bool compareMeetings(const Meeting& a, const Meeting& b) {
    if (a.end == b.end) {
        return a.start < b.start;
    }
    return a.end < b.end;
}
int getMaxMeetings(vector<Meeting>& meetings) {
    if (meetings.empty()) {
        return 0;
    }
    sort(meetings.begin(), meetings.end(), compareMeetings);
    int max_count = 1;
    int last_end_time = meetings[0].end;
    for (size_t i = 1; i < meetings.size(); i++) {
        if (meetings[i].start >= last_end_time) {
            max_count++;
            last_end_time = meetings[i].end;
        }
    }
    return max_count;
}
int main() {
    ios_base::sync_with_stdio(false);
    cin.tie(NULL);
    int n;
    if (cin >> n) {
        vector<Meeting> meetings(n);
        for (int i = 0; i < n; i++) {
            cin >> meetings[i].start >> meetings[i].end;
        }
        cout << getMaxMeetings(meetings) << "\n";
    }
    return 0;
}