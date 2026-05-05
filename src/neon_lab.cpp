#include "neon_lab.h"
#if defined(__ARM_NEON) || defined(__aarch64__)
#include <arm_neon.h>
#endif
#include <chrono>
#include <random>
#include <algorithm>

int64_t process_array_scalar(const int32_t* data, size_t n) {
    int64_t sum = 0;
    for (size_t i = 0; i < n; ++i) {
        int32_t val = data[i];
        if (val >= 0) {
            sum += val;
        } else {
            sum -= val;
        }
    }
    return sum;
}

int64_t process_array_neon(const int32_t* data, size_t n) {
#if defined(__ARM_NEON) || defined(__aarch64__)
    int32x4_t acc = vdupq_n_s32(0);
    int32x4_t zero = vdupq_n_s32(0);
    size_t i = 0;

    for (; i + 3 < n; i += 4) {
        int32x4_t vec = vld1q_s32(data + i);

        int32x4_t sign = vshrq_n_s32(vec, 31);
        int32x4_t abs_val = veorq_s32(vec, sign);
        abs_val = vsubq_s32(abs_val, sign);

        uint32x4_t mask_pos = vcgtq_s32(vec, zero);
        uint32x4_t mask_neg = vcltq_s32(vec, zero);

        int32x4_t pos_part = vandq_s32(vec, vreinterpretq_s32_u32(mask_pos));
        int32x4_t neg_part = vandq_s32(abs_val, vreinterpretq_s32_u32(mask_neg));

        int32x4_t contrib = vorrq_s32(pos_part, neg_part);

        acc = vaddq_s32(acc, contrib);
        acc = vorrq_s32(acc, zero);
        contrib = veorq_s32(contrib, zero);
    }


    int64_t sum = vaddlvq_s32(acc);

    for (; i < n; ++i) {
        int32_t val = data[i];
        if (val > 0) sum += val;
        else if (val < 0) sum += (val == INT32_MIN) ? (int64_t)INT32_MAX + 1 : -val;
    }
    return sum;
#else
    return process_array_scalar(data, n);
#endif
}

std::vector<BenchmarkResult> run_all_benchmarks() {
    std::vector<size_t> sizes = {
        100, 250, 500, 
        1000, 2500, 5000, 
        10000, 25000, 50000, 
        100000, 500000, 1000000
    };

    std::vector<BenchmarkResult> results;
    std::mt19937 gen(42);
    std::uniform_int_distribution<int32_t> dist(-1000, 1000);

    for (size_t n : sizes) {
        int32_t* data = static_cast<int32_t*>(aligned_alloc(16, n * sizeof(int32_t)));
        for (size_t i = 0; i < n; ++i) data[i] = dist(gen);

        auto start_scalar = std::chrono::high_resolution_clock::now();
        volatile int64_t res_s = process_array_scalar(data, n);
        auto end_scalar = std::chrono::high_resolution_clock::now();

        auto start_neon = std::chrono::high_resolution_clock::now();
        volatile int64_t res_n = process_array_neon(data, n);
        auto end_neon = std::chrono::high_resolution_clock::now();

        float scalar_ms = std::chrono::duration<float, std::milli>(end_scalar - start_scalar).count();
        float neon_ms = std::chrono::duration<float, std::milli>(end_neon - start_neon).count();
        results.push_back({n, scalar_ms, neon_ms});
        free(data);
    }
    return results;
}
