#include <arm_neon.h>
#include <chrono>
#include <cmath>
#include <cstddef>
#include <cstdint>
#include <cstdlib>
#include <ctime>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct BenchmarkResult {
    size_t size = 0;
    int64_t scalar_sum = 0;
    int64_t neon_sum = 0;
    double scalar_time = 0.0;
    double neon_time = 0.0;
};

int64_t process_scalar(const int32_t* data, size_t n) {
    int64_t sum = 0;
    for (size_t i = 0; i < n; i++) sum += std::abs(data[i]);
    return sum;
}

int64_t process_neon(const int32_t* data, size_t n) {
    int32x4_t acc = vdupq_n_s32(0);
    size_t i = 0;
    for (; i + 4 <= n; i += 4) {
        int32x4_t vec = vld1q_s32(data + i);
        acc = vaddq_s32(acc, vabsq_s32(vec));
    }
    int32_t temp[4];
    vst1q_s32(temp, acc);
    int64_t sum = (int64_t)temp[0] + temp[1] + temp[2] + temp[3];
    for (; i < n; i++) sum += std::abs(data[i]);
    return sum;
}

BenchmarkResult run_test(size_t n) {
    BenchmarkResult result;
    result.size = n;
    std::vector<int32_t> data(n);
    for (size_t i = 0; i < n; i++) data[i] = std::rand() % 2001 - 1000;
    auto s1 = std::chrono::high_resolution_clock::now();
    result.scalar_sum = process_scalar(data.data(), n);
    auto e1 = std::chrono::high_resolution_clock::now();
    auto s2 = std::chrono::high_resolution_clock::now();
    result.neon_sum = process_neon(data.data(), n);
    auto e2 = std::chrono::high_resolution_clock::now();
    result.scalar_time = std::chrono::duration<double, std::milli>(e1 - s1).count();
    result.neon_time = std::chrono::duration<double, std::milli>(e2 - s2).count();
    return result;
}

int main(int argc, char* argv[]) {
    std::srand(0);
    bool csv = false;
    for (int i = 1; i < argc; i++) if (std::string(argv[i]) == "--csv") csv = true;
    std::vector<size_t> sizes;
    for (int step = 0; step <= 60; step++) {
        size_t val = (size_t)std::pow(10.0, 2.0 + (double)step / 12.0);
        if (sizes.empty() || val > sizes.back()) sizes.push_back(val);
    }
    if (csv) {
        for (const auto& s : sizes) {
            BenchmarkResult r = run_test(s);
            std::cout << r.size << "," << r.scalar_sum << "," << r.neon_sum << ","
                      << (r.scalar_sum == r.neon_sum ? "OK" : "ERR") << ","
                      << std::fixed << std::setprecision(6) << r.scalar_time << ","
                      << r.neon_time << "," << (r.neon_time > 0 ? r.scalar_time / r.neon_time : 1.0) << "\n";
        }
    }
    return 0;
}