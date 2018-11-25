cmake_minimum_required(VERSION 3.12)
project(cpp_project)

find_package(Threads)

set(CMAKE_CXX_STANDARD 11)
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -D_GLIBCXX_DEBUG")

add_executable(
        cpp_project
        main.cpp)

target_link_libraries(
        cpp_project
        ${CMAKE_THREAD_LIBS_INIT}
)