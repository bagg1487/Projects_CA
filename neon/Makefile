CXX = g++
CXXFLAGS = -O3 -std=c++17 -march=native
INCLUDES = -I. -I./imgui -I./imgui/backends -I./implot
LIBS = -lglfw -lGL -ldl -lpthread

IMGUI_DIR = ./imgui
IMPLOT_DIR = ./implot
BACKENDS_DIR = $(IMGUI_DIR)/backends

SRCS = gui.cpp \
       neon_test.cpp \
       $(IMGUI_DIR)/imgui.cpp \
       $(IMGUI_DIR)/imgui_draw.cpp \
       $(IMGUI_DIR)/imgui_tables.cpp \
       $(IMGUI_DIR)/imgui_widgets.cpp \
       $(BACKENDS_DIR)/imgui_impl_glfw.cpp \
       $(BACKENDS_DIR)/imgui_impl_opengl3.cpp \
       $(IMPLOT_DIR)/implot.cpp \
       $(IMPLOT_DIR)/implot_items.cpp

OBJS = $(SRCS:.cpp=.o)

TARGET = neon_bench

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(OBJS) -o $(TARGET) $(LIBS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -f $(OBJS) $(TARGET)

.PHONY: all clean