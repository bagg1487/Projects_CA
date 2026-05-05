#include <arm_neon.h>
#include <cstdint>
#include <cstddef>
#include <iostream>
#include <vector>

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

    for (; i + 3 < n; i += 4) {
        int32x4_t vec = vld1q_s32(data + i);

        uint32x4_t mask_pos = vcgtq_s32(vec, vdupq_n_s32(0));
        uint32x4_t mask_neg = vcltq_s32(vec, vdupq_n_s32(0));

        int32x4_t sign = vshrq_n_s32(vec, 31);
        int32x4_t abs_val = veorq_s32(vec, sign);
        abs_val = vsubq_s32(abs_val, sign);

        int32x4_t pos_part = vandq_s32(vec, vreinterpretq_s32_u32(mask_pos));
        int32x4_t neg_part = vandq_s32(abs_val, vreinterpretq_s32_u32(mask_neg));

        int32x4_t contrib = vorrq_s32(pos_part, neg_part);

        acc = vaddq_s32(acc, contrib);
    }

    int32x2_t low = vget_low_s32(acc);
    int32x2_t high = vget_high_s32(acc);

    int32x2_t pair = vadd_s32(low, high);
    pair = vpadd_s32(pair, pair);

    int64_t sum = vget_lane_s32(pair, 0);

    for (; i < n; ++i) {
        int32_t v = data[i];
        if (v > 0) sum += v;
        else if (v < 0) sum -= v;
    }

    return sum;
}

int main() {
    std::vector<int32_t> data = {1, -2, 3, 0, -5, 6, -7, 8};

    int64_t s1 = process_array_scalar(data.data(), data.size());
    int64_t s2 = process_array_neon(data.data(), data.size());

    std::cout << "scalar: " << s1 << std::endl;
    std::cout << "neon:   " << s2 << std::endl;

}