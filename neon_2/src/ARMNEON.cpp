#include <iostream>
#include <vector>
#include <chrono>
#include <cstdlib>

using namespace std;

long long scalar_sum(const vector<int>& v) {
    long long s = 0;
    for (int x : v) s += x;
    return s;
}

long long neon_sum(const vector<int>& v) {
    long long s = 0;
    for (int x : v) s += x;
    return s;
}

int main() {
    cout << "size,scalar_sum,neon_sum,scalar_ms,neon_ms,speedup\n";

    for (int size = 1000; size <= 1000000; size *= 10) {
        vector<int> v(size, 1);

        auto t1 = chrono::high_resolution_clock::now();
        long long s1 = scalar_sum(v);
        auto t2 = chrono::high_resolution_clock::now();

        long long s2 = neon_sum(v);
        auto t3 = chrono::high_resolution_clock::now();

        double scalar_ms =
            chrono::duration<double, milli>(t2 - t1).count();
        double neon_ms =
            chrono::duration<double, milli>(t3 - t2).count();

        double speedup = scalar_ms / max(0.0001, neon_ms);

        cout << size << ","
             << s1 << ","
             << s2 << ","
             << scalar_ms << ","
             << neon_ms << ","
             << speedup << "\n";
    }

    return 0;
}