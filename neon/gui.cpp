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

    IMGUI_CHECKVERSION();
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

        if (ImGui::Button("Run Benchmark")) {
            run_benchmarks(data);
        }

        if (ImPlot::BeginPlot("Execution Time")) {
            ImPlot::SetupAxes("Array Size", "Time (us)");
            ImPlot::SetupAxisScale(ImAxis_X1, ImPlotScale_Log10);

            ImPlot::PlotLine("Scalar", data.sizes.data(), data.scalar_times.data(), data.sizes.size());
            ImPlot::PlotLine("NEON", data.sizes.data(), data.neon_times.data(), data.sizes.size());

            ImPlot::EndPlot();
        }

        if (ImPlot::BeginPlot("Speedup")) {
            ImPlot::SetupAxes("Array Size", "Speedup");
            ImPlot::SetupAxisScale(ImAxis_X1, ImPlotScale_Log10);

            ImPlot::PlotLine("Speedup", data.sizes.data(), data.speedups.data(), data.sizes.size());

            ImPlot::EndPlot();
        }

        if (ImGui::BeginTable("Results", 4)) {
            ImGui::TableSetupColumn("Size");
            ImGui::TableSetupColumn("Scalar (us)");
            ImGui::TableSetupColumn("NEON (us)");
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