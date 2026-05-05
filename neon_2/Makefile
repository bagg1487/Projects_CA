CXX ?= g++
CXXFLAGS := -std=c++17 -O2

SDL_CFLAGS := $(shell pkg-config --cflags sdl2 2>/dev/null)
SDL_LIBS := $(shell pkg-config --libs sdl2 2>/dev/null)
GL_LIBS := $(shell pkg-config --libs gl 2>/dev/null)

ifeq ($(strip $(SDL_CFLAGS)),)
SDL_CFLAGS := -I/usr/include/SDL2 -D_REENTRANT
endif

ifeq ($(strip $(SDL_LIBS)),)
SDL_LIBS := -lSDL2
endif

ifeq ($(strip $(GL_LIBS)),)
GL_LIBS := -lGL
endif

TARGET := armneon_app
SRC := \
	src/ARMNEON_imgui.cpp \
	third_party/imgui/imgui.cpp \
	third_party/imgui/imgui_draw.cpp \
	third_party/imgui/imgui_tables.cpp \
	third_party/imgui/imgui_widgets.cpp \
	third_party/imgui/backends/imgui_impl_sdl2.cpp \
	third_party/imgui/backends/imgui_impl_opengl3.cpp

INCLUDES := \
	-Ithird_party/imgui \
	-Ithird_party/imgui/backends \
	$(SDL_CFLAGS)

LIBS := $(SDL_LIBS) $(GL_LIBS) -ldl

.PHONY: all run clean

all: $(TARGET)

$(TARGET): $(SRC)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(SRC) $(LIBS) -o $(TARGET)

run: $(TARGET)
	./$(TARGET)

clean:
	rm -f $(TARGET)
