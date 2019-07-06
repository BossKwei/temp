# Minimal version of CMake
cmake_minimum_required (VERSION 3.7)

# Flags
set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_COLOR_MAKEFILE ON)
set(CMAKE_VERBOSE_MAKEFILE ON)

add_subdirectory(dlib)
add_subdirectory(exec)
