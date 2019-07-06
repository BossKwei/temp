cmake_minimum_required(VERSION 3.8)
project(cuda_project)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_BUILD_TYPE Release)

# cuda suppport
set(CMAKE_CUDA_FLAGS "-arch=compute_61 -code=compute_61")
set(CMAKE_CUDA_COMPILER "/usr/bin/nvcc")
enable_language(CUDA)

find_package(Eigen3 REQUIRED)
include_directories(${EIGEN3_INCLUDE_DIR})

include_directories(${PROJECT_SOURCE_DIR}/include)

add_executable(main src/main.cu)
