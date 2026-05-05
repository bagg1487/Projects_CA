# ARM NEON Visualizer

ImGui application for comparing scalar and ARM NEON processing times on test arrays of sizes:

- `100`
- `1000`
- `10000`
- `100000`
- `1000000`

The app:

- rebuilds the benchmark source automatically
- runs the benchmark
- shows a timing chart
- shows a table with array size, sums, timings, speedup, and result status

## Build

```bash
chmod +x build.sh
./build.sh
```

## Build and Run

```bash
./build.sh --run
```

## Direct CMake

```bash
cmake -S . -B build
cmake --build build -j
./build/armneon_app
```
