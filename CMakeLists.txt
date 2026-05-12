cmake_minimum_required(VERSION 3.14)
project(neon_lab VERSION 1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

set(IMGUI_DIR ${CMAKE_CURRENT_SOURCE_DIR}/third_party/imgui)

set(IMGUI_SRCS
    ${IMGUI_DIR}/imgui.cpp
    ${IMGUI_DIR}/imgui_draw.cpp
    ${IMGUI_DIR}/imgui_tables.cpp
    ${IMGUI_DIR}/imgui_widgets.cpp
    ${IMGUI_DIR}/imgui_demo.cpp
    ${IMGUI_DIR}/backends/imgui_impl_glfw.cpp
    ${IMGUI_DIR}/backends/imgui_impl_opengl3.cpp
)

find_package(glfw3 REQUIRED)
find_package(OpenGL REQUIRED)

add_executable(neon_lab
    src/main.cpp
    src/neon_lab.cpp
    src/neon_lab.h
    ${IMGUI_SRCS}
)

target_include_directories(neon_lab PRIVATE
    ${IMGUI_DIR}
    ${IMGUI_DIR}/backends
    src
)

target_link_libraries(neon_lab PRIVATE
    glfw
    OpenGL::GL
    ${CMAKE_DL_LIBS}
)
