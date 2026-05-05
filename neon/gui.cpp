#include <GLFW/glfw3.h>
#include "imgui.h"
#include "implot.h"
#include "imgui_impl_glfw.h"
#include "imgui_impl_opengl3.h"
#include "neon_test.hpp"

int main() {
    if (!glfwInit()) return 1;

    GLFWwindow* window = glfwCreateWindow(1280, 720, "NEON Benchmark", NULL, NULL);
    glfwMakeContextCurrent(window);
    glfwSwapInterval(1);

    ImGui::CreateContext();
    ImPlot::CreateContext();

    ImGui_ImplGlfw_InitForOpenGL(window, true);
    ImGui_ImplOpenGL3_Init("#version 130");

    BenchData data;
    run_benchmarks(data);

    while (!glfwWindowShouldClose(window)) {
        glfwPollEvents();

        ImGui_ImplOpenGL3_NewFrame();
        ImGui_ImplGlfw_NewFrame();
        ImGui::NewFrame();

        ImGui::Begin("NEON Benchmark");

        if (ImGui::Button("Re-run benchmark")) {
            run_benchmarks(data);
        }

        if (ImPlot::BeginPlot("Execution Time", ImVec2(-1, 450))) {

            ImPlot::SetupAxes("Size", "Time (us)");
            ImPlot::SetupAxisScale(ImAxis_X1, ImPlotScale_Log10);
            ImPlot::SetupAxisScale(ImAxis_Y1, ImPlotScale_Log10);

            ImPlot::PushStyleVar(ImPlotStyleVar_MarkerSize, 6);

            ImPlot::SetNextMarkerStyle(ImPlotMarker_Circle);
            ImPlot::PlotLine("Scalar", data.sizes.data(), data.scalar_times.data(), data.sizes.size());
            ImPlot::PlotScatter("Scalar points", data.sizes.data(), data.scalar_times.data(), data.sizes.size());

            ImPlot::SetNextMarkerStyle(ImPlotMarker_Square);
            ImPlot::PlotLine("NEON", data.sizes.data(), data.neon_times.data(), data.sizes.size());
            ImPlot::PlotScatter("NEON points", data.sizes.data(), data.neon_times.data(), data.neon_times.size());

            ImPlot::PopStyleVar();

            ImPlot::EndPlot();
        }

        if (ImGui::BeginTable("Results", 5, ImGuiTableFlags_Borders | ImGuiTableFlags_RowBg)) {
            ImGui::TableSetupColumn("Size");
            ImGui::TableSetupColumn("Scalar");
            ImGui::TableSetupColumn("NEON");
            ImGui::TableSetupColumn("Diff");
            ImGui::TableSetupColumn("Speedup");
            ImGui::TableHeadersRow();

            for (size_t i = 0; i < data.sizes.size(); ++i) {
                ImGui::TableNextRow();

                ImGui::TableSetColumnIndex(0);
                ImGui::Text("%.0f", data.sizes[i]);

                ImGui::TableSetColumnIndex(1);
                ImGui::Text("%.2f", data.scalar_times[i]);

                ImGui::TableSetColumnIndex(2);
                ImGui::Text("%.2f", data.neon_times[i]);

                ImGui::TableSetColumnIndex(3);
                ImGui::Text("%.2f", data.diff[i]);

                ImGui::TableSetColumnIndex(4);
                ImGui::Text("%.2f", data.speedups[i]);
            }

            ImGui::EndTable();
        }

        ImGui::End();

        ImGui::Render();

        int w, h;
        glfwGetFramebufferSize(window, &w, &h);
        glViewport(0, 0, w, h);
        glClearColor(0.1f, 0.1f, 0.1f, 1.0f);
        glClear(GL_COLOR_BUFFER_BIT);

        ImGui_ImplOpenGL3_RenderDrawData(ImGui::GetDrawData());
        glfwSwapBuffers(window);
    }

    ImGui_ImplOpenGL3_Shutdown();
    ImGui_ImplGlfw_Shutdown();
    ImPlot::DestroyContext();
    ImGui::DestroyContext();

    glfwDestroyWindow(window);
    glfwTerminate();
    return 0;
}