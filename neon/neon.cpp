#include "neon.h"
#include <arm_neon.h>
#include <chrono>
#include <numeric>

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
    int32x4_t acc = vdupq_n_s32(0);
    size_t i = 0;
    int32x4_t zero = vdupq_n_s32(0);

    for (; i + 3 < n; i += 4) {
        int32x4_t vec = vld1q_s32(data + i);
        int32x4_t sign = vshrq_n_s32(vec, 31);
        int32x4_t abs_val = vsubq_s32(veorq_s32(vec, sign), sign);
        uint32x4_t mask_pos = vcgtq_s32(vec, zero);
        uint32x4_t mask_neg = vcltq_s32(vec, zero);
        int32x4_t pos_part = vandq_s32(vec, vreinterpretq_s32_u32(mask_pos));
        int32x4_t neg_part = vandq_s32(abs_val, vreinterpretq_s32_u32(mask_neg));
        acc = vaddq_s32(acc, vorrq_s32(pos_part, neg_part));
    }

    int32_t temp[4];
    vst1q_s32(temp, acc);
    int64_t sum = temp[0] + temp[1] + temp[2] + temp[3];

    for (; i < n; ++i) {
        int32_t v = data[i];
        if (v > 0) sum += v;
        else if (v < 0) sum -= v;
    }
    return sum;
}

void run_benchmarks(BenchData& res) {
    res.sizes.clear();
    res.scalar_times.clear();
    res.neon_times.clear();
    for (int n = 1024; n <= 1024 * 1024; n *= 2) {
        std::vector<int32_t> data(n);
        std::iota(data.begin(), data.end(), -n/2);
        res.sizes.push_back((double)n);

        auto t0 = std::chrono::high_resolution_clock::now();
        for(int k=0; k<100; k++) process_array_scalar(data.data(), n);
        auto t1 = std::chrono::high_resolution_clock::now();
        res.scalar_times.push_back(std::chrono::duration<double, std::micro>(t1-t0).count()/100.0);

        t0 = std::chrono::high_resolution_clock::now();
        for(int k=0; k<100; k++) process_array_neon(data.data(), n);
        t1 = std::chrono::high_resolution_clock::now();
        res.neon_times.push_back(std::chrono::duration<double, std::micro>(t1-t0).count()/100.0);
    }
}