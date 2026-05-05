#include <arm_neon.h>
#include <chrono>
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

    for (size_t i = 0; i < n; i++) {
        if (data[i] > 0)
            sum += data[i];
        else if (data[i] < 0)
            sum -= data[i];
    }

    return sum;
}

int64_t process_neon(const int32_t* data, size_t n) {
    int32x4_t acc = vdupq_n_s32(0);
    int32x4_t zero = vdupq_n_s32(0);

    size_t i = 0;

    for (; i + 4 <= n; i += 4) {
        int32x4_t vec = vld1q_s32(data + i);

        uint32x4_t mask_pos = vcgtq_s32(vec, zero);
        uint32x4_t mask_neg = vcltq_s32(vec, zero);

        int32x4_t sign = vshrq_n_s32(vec, 31);
        int32x4_t abs_val = veorq_s32(vec, sign);
        abs_val = vsubq_s32(abs_val, sign);

        int32x4_t pos = vbslq_s32(mask_pos, vec, zero);
        int32x4_t neg = vbslq_s32(mask_neg, abs_val, zero);

        int32x4_t result = vaddq_s32(pos, neg);
        acc = vaddq_s32(acc, result);
    }

    int32_t temp[4];
    vst1q_s32(temp, acc);

    int64_t sum = temp[0] + temp[1] + temp[2] + temp[3];

    for (; i < n; i++) {
        if (data[i] > 0)
            sum += data[i];
        else if (data[i] < 0)
            sum -= data[i];
    }

    return sum;
}

BenchmarkResult run_test(size_t n) {
    BenchmarkResult result;
    result.size = n;

    std::vector<int32_t> data(n);

    for (size_t i = 0; i < n; i++) {
        data[i] = std::rand() % 2001 - 1000;
    }

    auto start1 = std::chrono::high_resolution_clock::now();
    result.scalar_sum = process_scalar(data.data(), n);
    auto end1 = std::chrono::high_resolution_clock::now();

    auto start2 = std::chrono::high_resolution_clock::now();
    result.neon_sum = process_neon(data.data(), n);
    auto end2 = std::chrono::high_resolution_clock::now();

    result.scalar_time =
        std::chrono::duration<double, std::milli>(end1 - start1).count();

    result.neon_time =
        std::chrono::duration<double, std::milli>(end2 - start2).count();

    return result;
}

void print_text_result(const BenchmarkResult& result, int test_number) {
    std::cout << "Test #" << test_number << std::endl;
    std::cout << "Data size:   " << result.size << std::endl;
    std::cout << "Scalar sum:  " << result.scalar_sum << std::endl;
    std::cout << "NEON sum:    " << result.neon_sum << std::endl;

    if (result.scalar_sum == result.neon_sum)
        std::cout << "Result:      OK" << std::endl;
    else
        std::cout << "Result:      ERROR" << std::endl;

    std::cout << "Scalar time: " << result.scalar_time << " ms" << std::endl;
    std::cout << "NEON time:   " << result.neon_time << " ms" << std::endl;

    if (result.neon_time > 0.0)
        std::cout << "Speedup:     " << result.scalar_time / result.neon_time << "x" << std::endl;
    else
        std::cout << "Speedup:     inf" << std::endl;

    std::cout << "-----------------------------" << std::endl;
}

void print_csv_header() {
    std::cout << "size,scalar_sum,neon_sum,result,scalar_time_ms,neon_time_ms,speedup" << std::endl;
}

void print_csv_result(const BenchmarkResult& result) {
    std::cout << result.size << ","
              << result.scalar_sum << ","
              << result.neon_sum << ","
              << (result.scalar_sum == result.neon_sum ? "OK" : "ERROR") << ","
              << std::fixed << std::setprecision(6)
              << result.scalar_time << ","
              << result.neon_time << ",";

    if (result.neon_time > 0.0)
        std::cout << result.scalar_time / result.neon_time;
    else
        std::cout << 0.0;

    std::cout << std::endl;
}

int main(int argc, char* argv[]) {
    std::srand(static_cast<unsigned>(std::time(nullptr)));

    bool csv_mode = false;

    for (int i = 1; i < argc; i++) {
        if (std::string(argv[i]) == "--csv") {
            csv_mode = true;
        }
    }

    const size_t sizes[] = {
        100,
        200,
        500,
        1000,
        2000,
        5000,
        10000,
        20000,
        50000,
        100000,
        200000,
        350000,
        500000,
        750000,
        1000000
    };

    const int tests = sizeof(sizes) / sizeof(sizes[0]);

    if (csv_mode) {
        print_csv_header();
    }

    for (int test = 0; test < tests; test++) {
        BenchmarkResult result = run_test(sizes[test]);

        if (csv_mode)
            print_csv_result(result);
        else
            print_text_result(result, test + 1);
    }

    return 0;
}
