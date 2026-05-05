#pragma once
#include <cstdint>
#include <vector>
#include <string>

struct BenchmarkResult {
    size_t array_size;
    float scalar_time_ms;
    float neon_time_ms;
};

int64_t process_array_scalar(const int32_t* data, size_t n);
int64_t process_array_neon(const int32_t* data, size_t n);
std::vector<BenchmarkResult> run_all_benchmarks();
