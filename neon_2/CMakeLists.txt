cmake_minimum_required(VERSION 3.16)

project(armneon_visualizer LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

find_package(PkgConfig REQUIRED)
pkg_check_modules(SDL2 REQUIRED IMPORTED_TARGET sdl2)
find_package(OpenGL REQUIRED)

add_executable(armneon_app
    src/ARMNEON_imgui.cpp
    third_party/imgui/imgui.cpp
    third_party/imgui/imgui_draw.cpp
    third_party/imgui/imgui_tables.cpp
    third_party/imgui/imgui_widgets.cpp
    third_party/imgui/backends/imgui_impl_sdl2.cpp
    third_party/imgui/backends/imgui_impl_opengl3.cpp
)

target_include_directories(armneon_app PRIVATE
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party/imgui
    ${CMAKE_CURRENT_SOURCE_DIR}/third_party/imgui/backends
)

target_compile_definitions(armneon_app PRIVATE
    ARMNEON_BENCHMARK_SOURCE_PATH="${CMAKE_CURRENT_SOURCE_DIR}/src/ARMNEON.cpp"
)

target_link_libraries(armneon_app PRIVATE
    PkgConfig::SDL2
    OpenGL::GL
    dl
)
