# Minimal version of CMake
cmake_minimum_required (VERSION 3.7)

 
# Define project name
project (exec)


# Set up executable
add_executable(exec main.cpp)
target_link_libraries(exec dlib)
