# Minimal version of CMake
cmake_minimum_required (VERSION 3.7)

# Define project name
project (dlib)

# Set up executable
add_library(dlib SHARED main.cpp)
