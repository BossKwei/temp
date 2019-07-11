# Minimal version of CMake
cmake_minimum_required (VERSION 3.7)

 
# Define project name
project (exec)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Debug)
set(CMAKE_COLOR_MAKEFILE ON)
set(CMAKE_VERBOSE_MAKEFILE ON)

add_subdirectory(${PROJECT_SOURCE_DIR}/3rd_party/dlib)
include_directories(${PROJECT_SOURCE_DIR}/3rd_party/dlib)

# Set up executable
add_executable(exec src/main.cpp)
target_link_libraries(exec dlib)
