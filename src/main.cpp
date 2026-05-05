#include "imgui.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include "neon_lab.h"
#include <stdio.h>
#include <vector>
#include <cmath>
#include <GLFW/glfw3.h>

static void glfw_error_callback(int error, const char* description) {
    fprintf(stderr, "Glfw Error %d: %s\n", error, description);
}

void DrawPerformanceGraph(const std::vector<BenchmarkResult>& results, float max_time) {
    if (results.empty()) return;

    ImDrawList* draw_list = ImGui::GetWindowDrawList();
    ImVec2 canvas_p0 = ImGui::GetCursorScreenPos();
    ImVec2 canvas_sz = ImGui::GetContentRegionAvail();
    if (canvas_sz.x < 50.0f) canvas_sz.x = 50.0f;
    if (canvas_sz.y < 50.0f) canvas_sz.y = 50.0f;
    ImVec2 canvas_p1 = ImVec2(canvas_p0.x + canvas_sz.x, canvas_p0.y + canvas_sz.y);

    draw_list->AddRectFilled(canvas_p0, canvas_p1, IM_COL32(30, 30, 30, 255));
    draw_list->AddRect(canvas_p0, canvas_p1, IM_COL32(100, 100, 100, 255));

    float margin_left = 60.0f;
    float margin_right = 80.0f;
    float margin_bottom = 50.0f;
    ImVec2 plot_p0 = ImVec2(canvas_p0.x + margin_left, canvas_p0.y + 20.0f);
    ImVec2 plot_p1 = ImVec2(canvas_p1.x - margin_right, canvas_p1.y - margin_bottom);
    float plot_w = plot_p1.x - plot_p0.x;
    float plot_h = plot_p1.y - plot_p0.y;

    draw_list->AddLine(ImVec2(plot_p0.x, plot_p1.y), ImVec2(plot_p1.x, plot_p1.y), IM_COL32(200, 200, 200, 255), 2.0f);
    draw_list->AddLine(ImVec2(plot_p0.x, plot_p0.y), ImVec2(plot_p0.x, plot_p1.y), IM_COL32(200, 200, 200, 255), 2.0f);

    draw_list->AddText(ImVec2(plot_p1.x + 10, plot_p1.y - 10), IM_COL32(200, 200, 200, 255), "Size (N)");
    draw_list->AddText(ImVec2(plot_p0.x - 50, plot_p0.y - 25), IM_COL32(200, 200, 200, 255), "Time (ms)");

    float min_t = 0.0001f;
    float max_t = max_time > min_t ? max_time : 1.0f;
    float log_min_t = log10(min_t);
    float log_max_t = log10(max_t);

    float min_s = (float)results.front().array_size;
    float max_s = (float)results.back().array_size;
    float log_min_s = log10(min_s);
    float log_max_s = log10(max_s);

    auto get_pos = [&](float size, float time) {
        float s_val = size > 0 ? size : 1.0f;
        float t_val = time > min_t ? time : min_t;
        float x_ratio = (log10(s_val) - log_min_s) / (log_max_s - log_min_s);
        float y_ratio = (log10(t_val) - log_min_t) / (log_max_t - log_min_t);
        return ImVec2(plot_p0.x + x_ratio * plot_w, plot_p1.y - y_ratio * plot_h);
    };

    for (int i = 0; i < (int)results.size(); i++) {
        ImVec2 p = get_pos((float)results[i].array_size, 0);
        char buf[32];
        size_t n = results[i].array_size;
        if (n >= 1000000) sprintf(buf, "%zuM", n / 1000000);
        else if (n >= 1000) sprintf(buf, "%zuK", n / 1000);
        else sprintf(buf, "%zu", n);
        
        draw_list->AddText(ImVec2(p.x - 15, plot_p1.y + 10), IM_COL32(150, 150, 150, 255), buf);
    }

    for (int i = 0; i < (int)results.size() - 1; i++) {
        ImVec2 p1_s = get_pos((float)results[i].array_size, results[i].scalar_time_ms);
        ImVec2 p2_s = get_pos((float)results[i+1].array_size, results[i+1].scalar_time_ms);
        draw_list->AddLine(p1_s, p2_s, IM_COL32(255, 100, 100, 255), 2.0f);

        ImVec2 p1_n = get_pos((float)results[i].array_size, results[i].neon_time_ms);
        ImVec2 p2_n = get_pos((float)results[i+1].array_size, results[i+1].neon_time_ms);
        draw_list->AddLine(p1_n, p2_n, IM_COL32(100, 255, 100, 255), 2.0f);
    }

    for (int i = 0; i < (int)results.size(); i++) {
        ImVec2 p_s = get_pos((float)results[i].array_size, results[i].scalar_time_ms);
        draw_list->AddCircleFilled(p_s, 4.0f, IM_COL32(255, 100, 100, 255));
        
        ImVec2 p_n = get_pos((float)results[i].array_size, results[i].neon_time_ms);
        draw_list->AddCircleFilled(p_n, 4.0f, IM_COL32(100, 255, 100, 255));
    }

    ImGui::Dummy(canvas_sz);
}

int main(int, char**) {
    glfwSetErrorCallback(glfw_error_callback);
    if (!glfwInit()) return 1;

    const char* glsl_version = "#version 130";
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 0);

    GLFWwindow* window = glfwCreateWindow(1280, 720, "ARM NEON Performance Lab", NULL, NULL);
    if (window == NULL) return 1;
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    IMGUI_CHECKVERSION();
    ImGui::CreateContext();
    ImGuiIO& io = ImGui::GetIO(); (void)io;
    ImGui::StyleColorsDark();
    io.FontGlobalScale = 1.5f;

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init(glsl_version);

    std::vector<BenchmarkResult> results;
    float max_time = 0.0f;

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        ImGuiViewport* viewport = ImGui::GetMainViewport();
        ImGui::SetNextWindowPos(viewport->Pos);
        ImGui::SetNextWindowSize(viewport->Size);
        
        ImGuiWindowFlags window_flags = ImGuiWindowFlags_NoDecoration | ImGuiWindowFlags_NoMove | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoSavedSettings | ImGuiWindowFlags_NoBringToFrontOnFocus;

        ImGui::Begin("Main", nullptr, window_flags);

        ImGui::Text("ARM NEON Performance Analysis");
        ImGui::Separator();

        if (ImGui::Button("Run Benchmarks", ImVec2(200, 40))) {
            results = run_all_benchmarks();
            max_time = 0.0f;
            for (const auto& r : results) {
                if (r.scalar_time_ms > max_time) max_time = r.scalar_time_ms;
                if (r.neon_time_ms > max_time) max_time = r.neon_time_ms;
            }
        }

        ImGui::SameLine();
        if (!results.empty()) {
            const auto& last = results.back();
            float speedup = last.neon_time_ms > 0 ? last.scalar_time_ms / last.neon_time_ms : 0;
            ImGui::Text("  Speedup (N=1M): %.2fx", speedup);
        }

        ImGui::Separator();
        
        if (!results.empty()) {
            ImGui::TextColored(ImVec4(1.0f, 0.4f, 0.4f, 1.0f), "Red: Scalar");
            ImGui::SameLine();
            ImGui::Text(" | ");
            ImGui::SameLine();
            ImGui::TextColored(ImVec4(0.4f, 1.0f, 0.4f, 1.0f), "Green: NEON");
            
            DrawPerformanceGraph(results, max_time);

            ImGui::Separator();
            ImGui::Text("Detailed Data Table:");
            ImGui::PushStyleVar(ImGuiStyleVar_CellPadding, ImVec2(8.0f, 8.0f));
            if (ImGui::BeginTable("ResultsTable", 4, ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg | ImGuiTableFlags_Resizable)) {
                ImGui::TableSetupColumn("Array Size (N)");
                ImGui::TableSetupColumn("Scalar Time (ms)");
                ImGui::TableSetupColumn("NEON Time (ms)");
                ImGui::TableSetupColumn("Speedup (x)");
                ImGui::TableHeadersRow();

                for (const auto& r : results) {
                    ImGui::TableNextRow();
                    ImGui::TableSetColumnIndex(0);
                    ImGui::Text("%zu", r.array_size);

                    ImGui::TableSetColumnIndex(1);
                    ImGui::Text("%.4f", r.scalar_time_ms);

                    ImGui::TableSetColumnIndex(2);
                    ImGui::Text("%.4f", r.neon_time_ms);

                    ImGui::TableSetColumnIndex(3);
                    float speedup = r.neon_time_ms > 0 ? r.scalar_time_ms / r.neon_time_ms : 0;
                    if (speedup >= 3.0f) 
                        ImGui::TextColored(ImVec4(0, 1, 0, 1), "%.2fx", speedup);
                    else
                        ImGui::TextColored(ImVec4(1, 1, 0, 1), "%.2fx", speedup);
                }
                ImGui::EndTable();
            }
            ImGui::PopStyleVar();
        } else {
            ImGui::Text("Click the button to generate performance data.");
        }

        ImGui::End();

        ImGui::Render();
        int display_w, display_h;
        glfwGetFramebufferSize(window, &display_w, &display_h);
        glViewport(0, 0, display_w, display_h);
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);
        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());

        glfwSwapBuffers(window);
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImGui::DestroyContext();
    glfwDestroyWindow(window);
    glfwTerminate();

    return 0;
}
