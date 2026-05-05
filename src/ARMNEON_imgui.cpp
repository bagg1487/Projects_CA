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
constexpr const char* kBuildCommandPrefix =
    "g++ -O2 -std=c++17 -mfpu=neon -mfloat-abi=hard -march=armv7-a ";
#else
constexpr bool kNativeArmHost = false;
constexpr const char* kBenchmarkBinaryPath = "/tmp/armneon_runtime_arm";
constexpr const char* kBuildCommandPrefix =
    "arm-linux-gnueabihf-g++ -O2 -std=c++17 -mfpu=neon -mfloat-abi=hard -march=armv7-a ";
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
    std::string status = "Ready to run";
    std::string raw_output;
    std::string arm_binary_path = kBenchmarkBinaryPath;
    bool auto_run_done = false;
};

std::string shell_quote(const std::string& value) {
    return "\"" + value + "\"";
}

std::string make_build_command(const AppState& state) {
    return std::string(kBuildCommandPrefix) + shell_quote(ARMNEON_BENCHMARK_SOURCE_PATH) +
           " -o " + shell_quote(state.arm_binary_path);
}

std::string make_run_command(const AppState& state) {
    if (kNativeArmHost) {
        return shell_quote(state.arm_binary_path) + " --csv";
    }

    return "qemu-arm -L /usr/arm-linux-gnueabihf " + shell_quote(state.arm_binary_path) +
           " --csv";
}

std::string trim(const std::string& value) {
    size_t first = 0;
    while (first < value.size() && std::isspace(static_cast<unsigned char>(value[first]))) {
        ++first;
    }

    size_t last = value.size();
    while (last > first && std::isspace(static_cast<unsigned char>(value[last - 1]))) {
        --last;
    }

    return value.substr(first, last - first);
}

std::vector<std::string> split_csv(const std::string& line) {
    std::vector<std::string> parts;
    std::stringstream stream(line);
    std::string item;

    while (std::getline(stream, item, ',')) {
        parts.push_back(trim(item));
    }

    return parts;
}

std::string run_command_capture(const std::string& command, int& exit_code) {
    std::string output;
    std::array<char, 4096> buffer{};
    std::string full_command = command + " 2>&1";

    FILE* pipe = popen(full_command.c_str(), "r");
    if (pipe == nullptr) {
        exit_code = -1;
        return "Failed to start command.";
    }

    while (std::fgets(buffer.data(), static_cast<int>(buffer.size()), pipe) != nullptr) {
        output += buffer.data();
    }

    int status = pclose(pipe);
    if (WIFEXITED(status)) {
        exit_code = WEXITSTATUS(status);
    } else {
        exit_code = status;
    }

    return output;
}

bool parse_benchmark_csv(const std::string& output, std::vector<BenchmarkPoint>& points) {
    points.clear();

    std::stringstream stream(output);
    std::string line;

    while (std::getline(stream, line)) {
        line = trim(line);
        if (line.empty() || line.rfind("size,", 0) == 0) {
            continue;
        }

        std::vector<std::string> cells = split_csv(line);
        if (cells.size() != 7) {
            continue;
        }

        BenchmarkPoint point;
        point.size = static_cast<size_t>(std::stoull(cells[0]));
        point.scalar_sum = std::stoll(cells[1]);
        point.neon_sum = std::stoll(cells[2]);
        point.ok = (cells[3] == "OK");
        point.scalar_time_ms = std::stod(cells[4]);
        point.neon_time_ms = std::stod(cells[5]);
        point.speedup = std::stod(cells[6]);

        points.push_back(point);
    }

    std::sort(points.begin(), points.end(),
              [](const BenchmarkPoint& left, const BenchmarkPoint& right) {
                  return left.size < right.size;
              });

    return !points.empty();
}

double choose_rounded_axis_max(double value) {
    if (value <= 0.0) {
        return 1.0;
    }

    const double magnitude = std::pow(10.0, std::floor(std::log10(value)));
    const double normalized = value / magnitude;

    double rounded = 1.0;
    if (normalized <= 1.0) {
        rounded = 1.0;
    } else if (normalized <= 2.0) {
        rounded = 2.0;
    } else if (normalized <= 5.0) {
        rounded = 5.0;
    } else {
        rounded = 10.0;
    }

    return rounded * magnitude;
}

void run_benchmark(AppState& state) {
    int exit_code = 0;
    state.raw_output = run_command_capture(make_run_command(state), exit_code);

    if (exit_code != 0) {
        state.status = "Run failed with exit code " + std::to_string(exit_code);
        return;
    }

    if (parse_benchmark_csv(state.raw_output, state.points)) {
        state.status = "Benchmark finished successfully";
    } else {
        state.status = "CSV parse failed. Check command output below.";
    }
}

void build_arm_binary(AppState& state) {
    int exit_code = 0;
    state.raw_output = run_command_capture(make_build_command(state), exit_code);

    if (exit_code == 0) {
        state.status = "ARM binary rebuilt successfully";
    } else {
        state.status = "Build failed with exit code " + std::to_string(exit_code);
    }
}

void build_and_run(AppState& state) {
    build_arm_binary(state);
    if (state.status == "ARM binary rebuilt successfully") {
        run_benchmark(state);
    }
}

void draw_timing_chart(const std::vector<BenchmarkPoint>& points) {
    ImVec2 canvas_size(ImGui::GetContentRegionAvail().x, 320.0f);
    if (canvas_size.x < 200.0f) {
        canvas_size.x = 200.0f;
    }

    ImVec2 canvas_pos = ImGui::GetCursorScreenPos();
    ImGui::InvisibleButton("timing_chart", canvas_size);

    ImDrawList* draw_list = ImGui::GetWindowDrawList();
    const ImU32 background = IM_COL32(17, 24, 39, 255);
    const ImU32 frame = IM_COL32(82, 103, 129, 255);
    const ImU32 grid = IM_COL32(56, 72, 92, 255);
    const ImU32 text = IM_COL32(216, 225, 236, 255);
    const ImU32 scalar_color = IM_COL32(243, 122, 55, 255);
    const ImU32 neon_color = IM_COL32(48, 194, 102, 255);

    draw_list->AddRectFilled(
        canvas_pos, ImVec2(canvas_pos.x + canvas_size.x, canvas_pos.y + canvas_size.y),
        background, 6.0f);
    draw_list->AddRect(
        canvas_pos, ImVec2(canvas_pos.x + canvas_size.x, canvas_pos.y + canvas_size.y), frame,
        6.0f, 0, 1.5f);

    if (points.empty()) {
        draw_list->AddText(ImVec2(canvas_pos.x + 20.0f, canvas_pos.y + 20.0f), text,
                           "No benchmark data yet.");
        draw_list->AddText(ImVec2(canvas_pos.x + 20.0f, canvas_pos.y + 44.0f), text,
                           "X: array size");
        draw_list->AddText(ImVec2(canvas_pos.x + 20.0f, canvas_pos.y + 64.0f), text,
                           "Y: time (ms)");
        return;
    }

    const float padding_left = 70.0f;
    const float padding_right = 24.0f;
    const float padding_top = 24.0f;
    const float padding_bottom = 52.0f;
    const ImVec2 origin(canvas_pos.x + padding_left,
                        canvas_pos.y + canvas_size.y - padding_bottom);
    const ImVec2 top_right(canvas_pos.x + canvas_size.x - padding_right,
                           canvas_pos.y + padding_top);
    const float plot_width = top_right.x - origin.x;
    const float plot_height = origin.y - top_right.y;

    const double min_log_x = std::log10(static_cast<double>(points.front().size));
    const double max_log_x = std::log10(static_cast<double>(points.back().size));
    const double log_range = std::max(0.001, max_log_x - min_log_x);

    double max_y_seconds = 0.0;
    for (const BenchmarkPoint& point : points) {
        max_y_seconds = std::max(
            max_y_seconds,
            std::max(point.scalar_time_ms, point.neon_time_ms) / 1000.0);
    }
    max_y_seconds = choose_rounded_axis_max(std::max(0.001, max_y_seconds * 1.15));

    for (int tick = 0; tick <= 5; ++tick) {
        const float t = static_cast<float>(tick) / 5.0f;
        const float y = origin.y - t * plot_height;
        draw_list->AddLine(ImVec2(origin.x, y), ImVec2(top_right.x, y), grid, 1.0f);

        char label[32];
        std::snprintf(label, sizeof(label), "%.4f", max_y_seconds * t);
        draw_list->AddText(ImVec2(canvas_pos.x + 14.0f, y - 8.0f), text, label);
    }

    draw_list->AddLine(origin, ImVec2(top_right.x, origin.y), frame, 2.0f);
    draw_list->AddLine(origin, ImVec2(origin.x, top_right.y), frame, 2.0f);

    const struct {
        int exponent;
        const char* label;
    } x_ticks[] = {
        {2, "100"},
        {3, "1K"},
        {4, "10K"},
        {5, "100K"},
        {6, "1M"},
    };

    for (const auto& tick : x_ticks) {
        const float x =
            origin.x + static_cast<float>((tick.exponent - min_log_x) / log_range) * plot_width;

        if (x >= origin.x && x <= top_right.x) {
            draw_list->AddLine(ImVec2(x, origin.y), ImVec2(x, top_right.y), grid, 1.0f);
            draw_list->AddLine(ImVec2(x, origin.y), ImVec2(x, origin.y + 6.0f), frame, 1.0f);
            draw_list->AddText(ImVec2(x - 14.0f, origin.y + 12.0f), text, tick.label);
        }
    }

    std::vector<ImVec2> scalar_line;
    std::vector<ImVec2> neon_line;
    scalar_line.reserve(points.size());
    neon_line.reserve(points.size());

    for (const BenchmarkPoint& point : points) {
        const double log_x = std::log10(static_cast<double>(point.size));
        const float x =
            origin.x + static_cast<float>((log_x - min_log_x) / log_range) * plot_width;
        const float scalar_y =
            origin.y -
            static_cast<float>((point.scalar_time_ms / 1000.0) / max_y_seconds) * plot_height;
        const float neon_y =
            origin.y -
            static_cast<float>((point.neon_time_ms / 1000.0) / max_y_seconds) * plot_height;

        scalar_line.push_back(ImVec2(x, scalar_y));
        neon_line.push_back(ImVec2(x, neon_y));
    }

    if (scalar_line.size() >= 2) {
        draw_list->AddPolyline(scalar_line.data(), static_cast<int>(scalar_line.size()),
                               scalar_color, 0, 2.5f);
        draw_list->AddPolyline(neon_line.data(), static_cast<int>(neon_line.size()), neon_color,
                               0, 2.5f);
    }

    float best_distance = std::numeric_limits<float>::max();
    int hovered_index = -1;
    bool hovered_scalar = true;
    const ImVec2 mouse = ImGui::GetIO().MousePos;

    for (size_t i = 0; i < scalar_line.size(); ++i) {
        draw_list->AddCircleFilled(scalar_line[i], 4.0f, scalar_color);
        draw_list->AddCircleFilled(neon_line[i], 4.0f, neon_color);

        const float scalar_distance =
            std::sqrt((mouse.x - scalar_line[i].x) * (mouse.x - scalar_line[i].x) +
                      (mouse.y - scalar_line[i].y) * (mouse.y - scalar_line[i].y));
        const float neon_distance =
            std::sqrt((mouse.x - neon_line[i].x) * (mouse.x - neon_line[i].x) +
                      (mouse.y - neon_line[i].y) * (mouse.y - neon_line[i].y));

        if (scalar_distance < best_distance) {
            best_distance = scalar_distance;
            hovered_index = static_cast<int>(i);
            hovered_scalar = true;
        }
        if (neon_distance < best_distance) {
            best_distance = neon_distance;
            hovered_index = static_cast<int>(i);
            hovered_scalar = false;
        }
    }

    draw_list->AddText(ImVec2(origin.x - 70.0f, top_right.y - 18.0f), text, "Y: time (s)");
    draw_list->AddText(ImVec2(origin.x, canvas_pos.y + 8.0f), scalar_color, "Scalar");
    draw_list->AddText(ImVec2(origin.x + 80.0f, canvas_pos.y + 8.0f), neon_color, "NEON");
    draw_list->AddText(ImVec2(origin.x + plot_width * 0.5f - 44.0f, origin.y + 28.0f), text,
                       "X: log10(array size)");

    if (hovered_index >= 0 && best_distance <= 12.0f) {
        const BenchmarkPoint& point = points[hovered_index];
        ImGui::BeginTooltip();
        ImGui::Text("Size: %zu", point.size);
        ImGui::Text("Scalar: %.6f s", point.scalar_time_ms / 1000.0);
        ImGui::Text("NEON: %.6f s", point.neon_time_ms / 1000.0);
        ImGui::Text("Focus: %s", hovered_scalar ? "Scalar" : "NEON");
        ImGui::Text("Speedup: %.3fx", point.speedup);
        ImGui::EndTooltip();
    }
}

void draw_results_table(const std::vector<BenchmarkPoint>& points) {
    if (ImGui::BeginTable("results_table", 7,
                          ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg |
                              ImGuiTableFlags_SizingStretchProp |
                              ImGuiTableFlags_ScrollY)) {
        ImGui::TableSetupColumn("Size");
        ImGui::TableSetupColumn("Scalar sum");
        ImGui::TableSetupColumn("NEON sum");
        ImGui::TableSetupColumn("Scalar ms");
        ImGui::TableSetupColumn("NEON ms");
        ImGui::TableSetupColumn("Speedup");
        ImGui::TableSetupColumn("Result");
        ImGui::TableHeadersRow();

        for (const BenchmarkPoint& point : points) {
            ImGui::TableNextRow();
            ImGui::TableSetColumnIndex(0);
            ImGui::Text("%zu", point.size);
            ImGui::TableSetColumnIndex(1);
            ImGui::Text("%lld", point.scalar_sum);
            ImGui::TableSetColumnIndex(2);
            ImGui::Text("%lld", point.neon_sum);
            ImGui::TableSetColumnIndex(3);
            ImGui::Text("%.6f", point.scalar_time_ms);
            ImGui::TableSetColumnIndex(4);
            ImGui::Text("%.6f", point.neon_time_ms);
            ImGui::TableSetColumnIndex(5);
            ImGui::Text("%.3fx", point.speedup);
            ImGui::TableSetColumnIndex(6);
            ImGui::TextColored(point.ok ? ImVec4(0.34f, 0.85f, 0.46f, 1.0f)
                                        : ImVec4(0.92f, 0.33f, 0.28f, 1.0f),
                               "%s", point.ok ? "OK" : "ERROR");
        }

        ImGui::EndTable();
    }
}

void apply_style() {
    ImGuiStyle& style = ImGui::GetStyle();
    style.WindowRounding = 10.0f;
    style.FrameRounding = 6.0f;
    style.GrabRounding = 6.0f;
    style.TabRounding = 6.0f;
    style.FramePadding = ImVec2(10.0f, 7.0f);
    style.ItemSpacing = ImVec2(10.0f, 10.0f);
    style.WindowPadding = ImVec2(16.0f, 16.0f);

    ImVec4* colors = style.Colors;
    colors[ImGuiCol_WindowBg] = ImVec4(0.09f, 0.10f, 0.12f, 1.0f);
    colors[ImGuiCol_ChildBg] = ImVec4(0.11f, 0.13f, 0.16f, 1.0f);
    colors[ImGuiCol_Header] = ImVec4(0.19f, 0.23f, 0.28f, 1.0f);
    colors[ImGuiCol_HeaderHovered] = ImVec4(0.24f, 0.29f, 0.35f, 1.0f);
    colors[ImGuiCol_Button] = ImVec4(0.11f, 0.45f, 0.72f, 1.0f);
    colors[ImGuiCol_ButtonHovered] = ImVec4(0.18f, 0.55f, 0.84f, 1.0f);
    colors[ImGuiCol_ButtonActive] = ImVec4(0.09f, 0.39f, 0.64f, 1.0f);
    colors[ImGuiCol_FrameBg] = ImVec4(0.15f, 0.17f, 0.21f, 1.0f);
    colors[ImGuiCol_Border] = ImVec4(0.28f, 0.32f, 0.37f, 0.8f);
    colors[ImGuiCol_TitleBg] = ImVec4(0.09f, 0.10f, 0.12f, 1.0f);
    colors[ImGuiCol_TitleBgActive] = ImVec4(0.09f, 0.10f, 0.12f, 1.0f);
    colors[ImGuiCol_TableRowBgAlt] = ImVec4(0.12f, 0.14f, 0.17f, 0.8f);
}

int main() {
    if (SDL_Init(SDL_INIT_VIDEO | SDL_INIT_TIMER | SDL_INIT_GAMECONTROLLER) != 0) {
        std::fprintf(stderr, "SDL init failed: %s\n", SDL_GetError());
        return 1;
    }

    SDL_GL_SetAttribute(SDL_GL_CONTEXT_FLAGS, 0);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_PROFILE_MASK, SDL_GL_CONTEXT_PROFILE_CORE);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MAJOR_VERSION, 3);
    SDL_GL_SetAttribute(SDL_GL_CONTEXT_MINOR_VERSION, 2);
    SDL_GL_SetAttribute(SDL_GL_DOUBLEBUFFER, 1);
    SDL_GL_SetAttribute(SDL_GL_DEPTH_SIZE, 24);
    SDL_GL_SetAttribute(SDL_GL_STENCIL_SIZE, 8);

    SDL_Window* window = SDL_CreateWindow(
        "ARM NEON Benchmark Viewer",
        SDL_WINDOWPOS_CENTERED,
        SDL_WINDOWPOS_CENTERED,
        1280,
        900,
        SDL_WINDOW_OPENGL | SDL_WINDOW_RESIZABLE | SDL_WINDOW_ALLOW_HIGHDPI);
    if (window == nullptr) {
        std::fprintf(stderr, "Window creation failed: %s\n", SDL_GetError());
        SDL_Quit();
        return 1;
    }

    SDL_GLContext gl_context = SDL_GL_CreateContext(window);
    if (gl_context == nullptr) {
        std::fprintf(stderr, "OpenGL context failed: %s\n", SDL_GetError());
        SDL_DestroyWindow(window);
        SDL_Quit();
        return 1;
    }

    SDL_GL_MakeCurrent(window, gl_context);
    SDL_GL_SetSwapInterval(1);

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO();
    io.ConfigFlags |= ImGuiConfigFlags_NavEnableKeyboard;

    apply_style();

    ImGui_ImplSDL2_InitForOpenGL(window, gl_context);
    ImGui_ImplOpenGL3_Init("#version 150");

    AppState state;
    bool running = true;

    while (running) {
        SDL_Event event;
        while (SDL_PollEvent(&event)) {
            ImGui_ImplSDL2_ProcessEvent(&event);
            if (event.type == SDL_QUIT) {
                running = false;
            }
            if (event.type == SDL_WINDOWEVENT &&
                event.window.event == SDL_WINDOWEVENT_CLOSE &&
                event.window.windowID == SDL_GetWindowID(window)) {
                running = false;
            }
        }

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplSDL2_NewFrame();
        ImGui::NewFrame();

        if (!state.auto_run_done) {
            build_and_run(state);
            state.auto_run_done = true;
        }

        ImGui::SetNextWindowPos(ImVec2(0.0f, 0.0f), ImGuiCond_Always);
        ImGui::SetNextWindowSize(io.DisplaySize, ImGuiCond_Always);
        ImGui::Begin("ARM NEON Benchmark Dashboard", nullptr,
                     ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoMove |
                         ImGuiWindowFlags_NoCollapse | ImGuiWindowFlags_NoTitleBar);

        ImGui::TextUnformatted("ARM NEON benchmark");
        ImGui::Separator();

        if (ImGui::Button("Repeat", ImVec2(120.0f, 0.0f))) {
            run_benchmark(state);
        }

        ImGui::Text("Status: %s", state.status.c_str());
        ImGui::Spacing();
        ImGui::TextUnformatted("Timing chart");
        draw_timing_chart(state.points);
        ImGui::Spacing();
        ImGui::TextUnformatted("Results");
        ImGui::BeginChild("table_container", ImVec2(0.0f, 0.0f), true);
        draw_results_table(state.points);
        ImGui::EndChild();

        ImGui::End();

        ImGui::Render();
        glViewport(0, 0, static_cast<int>(io.DisplaySize.x), static_cast<int>(io.DisplaySize.y));
        glClearColor(0.05f, 0.07f, 0.10f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        SDL_GL_SwapWindow(window);
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplSDL2_Shutdown();
    ImGui::DestroyContext();

    SDL_GL_DeleteContext(gl_context);
    SDL_DestroyWindow(window);
    SDL_Quit();
    return 0;
}
