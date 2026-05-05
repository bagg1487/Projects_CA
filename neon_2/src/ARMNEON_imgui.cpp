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

static const char* kBuildScript = "./build.sh";
static const char* kRunBinary = "./build/armneon_app";

struct BenchmarkPoint {
    size_t size = 0;
    long long scalar_sum = 0;
    long long neon_sum = 0;
    double scalar_time_ms = 0;
    double neon_time_ms = 0;
    double speedup = 0;
};

struct AppState {
    std::vector<BenchmarkPoint> points;
    std::string raw_output;
    std::string status = "Ready";
    bool auto_run = false;
};

std::string run_cmd(const std::string& cmd) {
    std::array<char, 4096> buf{};
    std::string out;
    FILE* p = popen((cmd + " 2>&1").c_str(), "r");
    if (!p) return "popen failed";
    while (fgets(buf.data(), buf.size(), p)) out += buf.data();
    pclose(p);
    return out;
}

bool parse_csv(const std::string& s, std::vector<BenchmarkPoint>& out) {
    out.clear();
    std::stringstream ss(s);
    std::string line;

    while (std::getline(ss, line)) {
        if (line.empty()) continue;
        if (line.find("size") == 0) continue;

        std::stringstream ls(line);
        std::string c;
        std::vector<std::string> v;

        while (std::getline(ls, c, ',')) v.push_back(c);

        if (v.size() < 6) continue;

        BenchmarkPoint p;
        p.size = std::stoull(v[0]);
        p.scalar_sum = std::stoll(v[1]);
        p.neon_sum = std::stoll(v[2]);
        p.scalar_time_ms = std::stod(v[3]);
        p.neon_time_ms = std::stod(v[4]);
        p.speedup = std::stod(v[5]);

        out.push_back(p);
    }

    return !out.empty();
}

void run(AppState& s) {
    s.raw_output = run_cmd(kRunBinary);

    if (!parse_csv(s.raw_output, s.points)) {
        s.status = "NO DATA (CSV parse failed)";
    } else {
        s.status = "OK";
    }
}

void build(AppState& s) {
    s.raw_output = run_cmd(kBuildScript);
    s.status = "Built";
}

void build_and_run(AppState& s) {
    build(s);
    run(s);
}

void draw_chart(const std::vector<BenchmarkPoint>&) {
    ImGui::Text("Chart placeholder (kept simple)");
}

void draw_table(const std::vector<BenchmarkPoint>& pts) {
    if (ImGui::BeginTable("t", 6)) {
        for (auto& p : pts) {
            ImGui::TableNextRow();
            ImGui::TableNextColumn(); ImGui::Text("%zu", p.size);
            ImGui::TableNextColumn(); ImGui::Text("%lld", p.scalar_sum);
            ImGui::TableNextColumn(); ImGui::Text("%lld", p.neon_sum);
            ImGui::TableNextColumn(); ImGui::Text("%.3f", p.scalar_time_ms);
            ImGui::TableNextColumn(); ImGui::Text("%.3f", p.neon_time_ms);
            ImGui::TableNextColumn(); ImGui::Text("%.2fx", p.speedup);
        }
        ImGui::EndTable();
    }
}

int main() {
    SDL_Init(SDL_INIT_VIDEO);
    SDL_Window* w = SDL_CreateWindow("NEON", 0,0,1280,800, SDL_WINDOW_OPENGL);
    SDL_GLContext gl = SDL_GL_CreateContext(w);

    ImGui::CreateContext();
    ImGui_ImplSDL2_InitForOpenGL(w, gl);
    ImGui_ImplOpenGL3_Init("#version 150");

    AppState s;

    while (true) {
        SDL_Event e;
        while (SDL_PollEvent(&e)) {
            ImGui_ImplSDL2_ProcessEvent(&e);
            if (e.type == SDL_QUIT) return 0;
        }

        if (!s.auto_run) {
            build_and_run(s);
            s.auto_run = true;
        }

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplSDL2_NewFrame();
        ImGui::NewFrame();

        ImGui::Begin("dashboard");

        ImGui::Columns(2);
        ImGui::SetColumnWidth(0, 800);

        draw_chart(s.points);

        ImGui::NextColumn();

        draw_table(s.points);

        ImGui::Columns(1);

        if (ImGui::Button("Run")) run(s);

        ImGui::Text("%s", s.status.c_str());
        ImGui::TextWrapped("%s", s.raw_output.c_str());

        ImGui::End();

        ImGui::Render();
        glViewport(0,0,1280,800);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        SDL_GL_SwapWindow(w);
    }
}