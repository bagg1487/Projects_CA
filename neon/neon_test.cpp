void run_benchmarks(BenchData& res) {
    res.sizes.clear();
    res.scalar_times.clear();
    res.neon_times.clear();
    res.speedups.clear();
    res.diff.clear();

    for (int n = 1024; n <= 1024 * 1024; n *= 2) {
        std::vector<int32_t> data(n);
        std::iota(data.begin(), data.end(), -n/2);

        res.sizes.push_back(n);

        auto t0 = std::chrono::high_resolution_clock::now();
        for(int k=0; k<100; k++) process_array_scalar(data.data(), n);
        auto t1 = std::chrono::high_resolution_clock::now();
        double scalar = std::chrono::duration<double, std::micro>(t1-t0).count()/100.0;
        res.scalar_times.push_back(scalar);

        t0 = std::chrono::high_resolution_clock::now();
        for(int k=0; k<100; k++) process_array_neon(data.data(), n);
        t1 = std::chrono::high_resolution_clock::now();
        double neon = std::chrono::duration<double, std::micro>(t1-t0).count()/100.0;
        res.neon_times.push_back(neon);

        res.speedups.push_back(neon > 0 ? scalar / neon : 0.0);
        res.diff.push_back(scalar - neon);
    }
}