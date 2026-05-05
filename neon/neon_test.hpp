#pragma once
#include <cstdint>
#include <cstddef>
#include <vector>

int64_t process_array_scalar(const int32_t* data, size_t n);
int64_t process_array_neon(const int32_t* data, size_t n);

struct BenchData {
    std::vector<double> sizes;
    std::vector<double> scalar_times;
    std::vector<double> neon_times;
    std::vector<double> speedups;
    std::vector<double> diff;
};

void run_benchmarks(BenchData& data);