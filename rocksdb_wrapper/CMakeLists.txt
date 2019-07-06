# Minimal version of CMake
cmake_minimum_required (VERSION 3.7)

# Flags
set(CMAKE_CXX_STANDARD 11)
# set(CMAKE_CXX_COMPILER /usr/bin/clang++-6.0)

set(CMAKE_BUILD_TYPE Debug)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -pg")
set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -pg")
set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -pg")
set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -pg")

#
project(demo_2)

#
include_directories(${PROJECT_SOURCE_DIR}/include)

#
add_executable(main src/main.cpp)
target_link_libraries(main PUBLIC "/usr/lib/librocksdb.so")

add_library(wrapper SHARED src/wrapper.cpp)
target_link_libraries(wrapper PUBLIC "/usr/lib/librocksdb.so")
