#include <SDL2/SDL.h>
#include <SDL2/SDL_opengl.h>

#include <algorithm>
#include <array>
#include <cctype>
#include <cmath>
#include <cstdio>
#include <cstring>
#include <limits>
#include <sstream>
#include <string>
#include <sys/wait.h>
#include <vector>

#include "imgui.h"
#include "backends/imgui_impl_opengl3.h"
#include "backends/imgui_impl_sdl2.h"

#ifndef ARMNEON_BENCHMARK_SOURCE_PATH
#define ARMNEON_BENCHMARK_SOURCE_PATH "ARMNEON.cpp"
#endif

#if defined(__aarch64__)
constexpr bool kNativeArmHost = true;
constexpr const char* kBenchmarkBinaryPath = "/tmp/armneon_runtime_native";
constexpr const char* kBuildCommandPrefix = "g++ -O2 -std=c++17 ";
#elif defined(__arm__)
constexpr bool kNativeArmHost = true;
constexpr const char* kBenchmarkBinaryPath = "/tmp/armneon_runtime_native";
constexpr const char* kBuildCommandPrefix = "g++ -O2 -std=c++17 -mfpu=neon -mfloat-abi=hard -march=armv7-a ";
#else
constexpr bool kNativeArmHost = false;
constexpr const char* kBenchmarkBinaryPath = "/tmp/armneon_runtime_arm";
constexpr const char* kBuildCommandPrefix = "arm-linux-gnueabihf-g++ -O2 -std=c++17 -mfpu=neon -mfloat-abi=hard -march=armv7-a ";
#endif

struct BenchmarkPoint {
    size_t size = 0;
    long long scalar_sum = 0;
    long long neon_sum = 0;
    bool ok = false;
    double scalar_time_ms = 0.0;
    double neon_time_ms = 0.0;
    double speedup = 0.0;
};

struct AppState {
    std::vector<BenchmarkPoint> points;
    std::string status = "Ready";
    std::string raw_output;
    std::string arm_binary_path = kBenchmarkBinaryPath;
    bool auto_run_done = false;
};

std::string shell_quote(const std::string& v) {
    return "\"" + v + "\"";
}

std::string make_build_command(const AppState& s) {
    return std::string(kBuildCommandPrefix) + shell_quote(ARMNEON_BENCHMARK_SOURCE_PATH) +
           " -o " + shell_quote(s.arm_binary_path);
}

std::string make_run_command(const AppState& s) {
    if (kNativeArmHost) return shell_quote(s.arm_binary_path) + " --csv";
    return "qemu-arm -L /usr/arm-linux-gnueabihf " + shell_quote(s.arm_binary_path) + " --csv";
}

std::string trim(const std::string& v) {
    size_t i = 0;
    while (i < v.size() && std::isspace((unsigned char)v[i])) i++;
    size_t j = v.size();
    while (j > i && std::isspace((unsigned char)v[j - 1])) j--;
    return v.substr(i, j - i);
}

std::vector<std::string> split_csv(const std::string& l) {
    std::vector<std::string> p;
    std::stringstream ss(l);
    std::string x;
    while (std::getline(ss, x, ',')) p.push_back(trim(x));
    return p;
}

std::string run_command_capture(const std::string& cmd, int& code) {
    std::string out;
    std::array<char, 4096> buf{};
    std::string full = cmd + " 2>&1";

    FILE* pipe = popen(full.c_str(), "r");
    if (!pipe) {
        code = -1;
        return "fail";
    }

    while (fgets(buf.data(), buf.size(), pipe)) out += buf.data();
    int status = pclose(pipe);
    code = WIFEXITED(status) ? WEXITSTATUS(status) : status;
    return out;
}

bool parse_benchmark_csv(const std::string& out, std::vector<BenchmarkPoint>& pts) {
    pts.clear();
    std::stringstream ss(out);
    std::string line;

    while (std::getline(ss, line)) {
        line = trim(line);
        if (line.empty() || line.rfind("size,", 0) == 0) continue;

        auto c = split_csv(line);
        if (c.size() != 7) continue;

        BenchmarkPoint p;
        p.size = std::stoull(c[0]);
        p.scalar_sum = std::stoll(c[1]);
        p.neon_sum = std::stoll(c[2]);
        p.ok = (c[3] == "OK");
        p.scalar_time_ms = std::stod(c[4]);
        p.neon_time_ms = std::stod(c[5]);
        p.speedup = std::stod(c[6]);
        pts.push_back(p);
    }

    std::sort(pts.begin(), pts.end(), [](auto& a, auto& b) { return a.size < b.size; });
    return !pts.empty();
}

double choose_rounded_axis_max(double v) {
    if (v <= 0) return 1;
    double m = std::pow(10, std::floor(std::log10(v)));
    double n = v / m;
    double r = n <= 1 ? 1 : n <= 2 ? 2 : n <= 5 ? 5 : 10;
    return r * m;
}

void run_benchmark(AppState& s) {
    int code = 0;
    s.raw_output = run_command_capture(make_run_command(s), code);
    if (code != 0) {
        s.status = "Run failed";
        return;
    }
    if (parse_benchmark_csv(s.raw_output, s.points)) s.status = "OK";
    else s.status = "Parse failed";
}

void build_arm_binary(AppState& s) {
    int code = 0;
    s.raw_output = run_command_capture(make_build_command(s), code);
    s.status = (code == 0) ? "Built" : "Build failed";
}

void build_and_run(AppState& s) {
    build_arm_binary(s);
    if (s.status == "Built") run_benchmark(s);
}

void draw_timing_chart(const std::vector<BenchmarkPoint>& points) {
    ImVec2 size(ImGui::GetContentRegionAvail().x, 320);
    ImVec2 pos = ImGui::GetCursorScreenPos();
    ImGui::InvisibleButton("chart", size);

    auto* dl = ImGui::GetWindowDrawList();

    if (points.empty()) {
        dl->AddText(pos, IM_COL32_WHITE, "No data");
        return;
    }

    float pad_l = 55, pad_r = 16, pad_t = 16, pad_b = 40;
    ImVec2 o(pos.x + pad_l, pos.y + size.y - pad_b);
    ImVec2 tr(pos.x + size.x - pad_r, pos.y + pad_t);

    float w = tr.x - o.x;
    float h = o.y - tr.y;

    double minx = std::log10(points.front().size);
    double maxx = std::log10(points.back().size);
    double xr = std::max(0.001, maxx - minx);

    double maxy = 0;
    for (auto& p : points)
        maxy = std::max(maxy, std::max(p.scalar_time_ms, p.neon_time_ms) / 1000.0);
    maxy = choose_rounded_axis_max(maxy);

    std::vector<ImVec2> a, b;

    for (auto& p : points) {
        double lx = std::log10(p.size);
        float x = o.x + (lx - minx) / xr * w;
        float y1 = o.y - (p.scalar_time_ms / 1000.0) / maxy * h;
        float y2 = o.y - (p.neon_time_ms / 1000.0) / maxy * h;
        a.push_back({x, y1});
        b.push_back({x, y2});
    }

    dl->AddPolyline(a.data(), a.size(), IM_COL32(200, 200, 200, 255), 0, 2);
    dl->AddPolyline(b.data(), b.size(), IM_COL32(100, 200, 255, 255), 0, 2);
}

void draw_results_table(const std::vector<BenchmarkPoint>& p) {
    if (ImGui::BeginTable("t", 6, ImGuiTableFlags_ScrollY | ImGuiTableFlags_SizingFixedFit)) {
        ImGui::TableSetupColumn("Size");
        ImGui::TableSetupColumn("S");
        ImGui::TableSetupColumn("N");
        ImGui::TableSetupColumn("ms S");
        ImGui::TableSetupColumn("ms N");
        ImGui::TableSetupColumn("x");
        ImGui::TableHeadersRow();

        for (auto& r : p) {
            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::Text("%zu", r.size);
            ImGui::TableSetColumnIndex(1);
            ImGui::Text("%lld", r.scalar_sum);
            ImGui::TableSetColumnIndex(2);
            ImGui::Text("%lld", r.neon_sum);
            ImGui::TableSetColumnIndex(3);
            ImGui::Text("%.3f", r.scalar_time_ms);
            ImGui::TableSetColumnIndex(4);
            ImGui::Text("%.3f", r.neon_time_ms);
            ImGui::TableSetColumnIndex(5);
            ImGui::Text("%.2fx", r.speedup);
        }

        ImGui::EndTable();
    }
}

void apply_style() {
    ImGuiStyle& s = ImGui::GetStyle();
    s.WindowRounding = 6;
    s.FrameRounding = 4;
    s.FramePadding = ImVec2(6, 4);
}

int main() {
    SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER);

    SDL_Window* w = SDL_CreateWindow("NEON", 0, 0, 1280, 900, SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE);
    SDL_GLContext gl = SDL_GL_CreateContext(w);

    ImGui::CreateContext();
    ImGui_ImplSDL2_InitForOpenGL(w, gl);
    ImGui_ImplOpenGL3_Init("#version 150");

    apply_style();

    AppState s;

    while (true) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            ImGui_ImplSDL2_ProcessEvent(&e);
            if (e.type == SDL_QUIT) return 0;
        }

        if (!s.auto_run_done) {
            build_and_run(s);
            s.auto_run_done = true;
        }

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplSDL2_NewFrame();
        ImGui::NewFrame();

        ImGui::Begin("dashboard");

        ImGui::Columns(2, nullptr, false);

        ImGui::SetColumnWidth(0, ImGui::GetWindowWidth() * 0.7f);
        draw_timing_chart(s.points);

        ImGui::NextColumn();
        draw_results_table(s.points);

        ImGui::Columns(1);

        if (ImGui::Button("Run")) run_benchmark(s);
        ImGui::SameLine();
        ImGui::Text("%s", s.status.c_str());

        ImGui::End();

        ImGui::Render();
        glViewport(0, 0, 1280, 900);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        SDL_GL_SwapWindow(w);
    }
}