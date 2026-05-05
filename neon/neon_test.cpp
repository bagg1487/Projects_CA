#include "neon_test.hpp"
#include <chrono>
#include <numeric>
#include <vector>

#if defined(__ARM_NEON)
#include <arm_neon.h>
#define USE_NEON 1
#else
#define USE_NEON 0
#endif

int64_t process_array_scalar(const int32_t* data, size_t n) {
    int64_t sum = 0;
    for (size_t i = 0; i < n; ++i) {
        int32_t v = data[i];
        if (v > 0) sum += v;
        else if (v < 0) sum -= v;
    }
    return sum;
}

int64_t process_array_neon(const int32_t* data, size_t n) {
#if USE_NEON
    int32x4_t acc = vdupq_n_s32(0);
    int32x4_t zero = vdupq_n_s32(0);
    size_t i = 0;

    for (; i + 3 < n; i += 4) {
        int32x4_t vec = vld1q_s32(data + i);
        uint32x4_t mask_pos = vcgtq_s32(vec, zero);
        uint32x4_t mask_neg = vcltq_s32(vec, zero);

        int32x4_t pos = vandq_s32(vec, vreinterpretq_s32_u32(mask_pos));
        int32x4_t neg = vandq_s32(vabsq_s32(vec), vreinterpretq_s32_u32(mask_neg));

        acc = vaddq_s32(acc, vaddq_s32(pos, neg));
    }

    int32_t tmp[4];
    vst1q_s32(tmp, acc);

    int64_t sum = tmp[0] + tmp[1] + tmp[2] + tmp[3];

    for (; i < n; ++i) {
        int32_t v = data[i];
        if (v > 0) sum += v;
        else if (v < 0) sum -= v;
    }

    return sum;
#else
    return process_array_scalar(data, n);
#endif
}

void run_benchmarks(BenchData& res) {
    res.sizes.clear();
    res.scalar_times.clear();
    res.neon_times.clear();
    res.speedups.clear();
    res.diff.clear();

    for (int n = 1024; n <= 1024 * 1024; n *= 2) {
        std::vector<int32_t> data(n);
        std::iota(data.begin(), data.end(), -n/2);

        res.sizes.push_back((double)n);

        auto bench = [&](auto fn) {
            auto t0 = std::chrono::high_resolution_clock::now();
            for (int k = 0; k < 50; k++) fn(data.data(), n);
            auto t1 = std::chrono::high_resolution_clock::now();
            return std::chrono::duration<double, std::micro>(t1 - t0).count() / 50.0;
        };

        double scalar = bench(process_array_scalar);
        double neon = bench(process_array_neon);

        if (scalar <= 0) scalar = 1e-6;
        if (neon <= 0) neon = 1e-6;

        res.scalar_times.push_back(scalar);
        res.neon_times.push_back(neon);
        res.speedups.push_back(scalar / neon);
        res.diff.push_back(scalar - neon);
    }
}