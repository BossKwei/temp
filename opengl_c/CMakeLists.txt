cmake_minimum_required(VERSION 3.12)
project(glfw_example C)

set(CMAKE_C_STANDARD 99)
SET (CMAKE_C_COMPILER "clang-6.0")
set(CMAKE_C_FLAGS_DEBUG "${CMAKE_C_FLAGS_DEBUG} -D_GLIBC_DEBUG")

# set(CMAKE_CXX_STANDARD 11)
# SET (CMAKE_C_COMPILER "clang++-6.0")
# set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -D_GLIBCXX_DEBUG")

find_package(glfw3 3.2 REQUIRED)
find_package(OpenGL REQUIRED)

include_directories(
        ${OPENGL_INCLUDE_DIR}
)

add_executable(
        untitled_0
        untitled_0.c
        glad.c
)

target_link_libraries(
        untitled_0
        -lglfw -lm
)


add_executable(
        untitled_1
        untitled_1.c
        glad.c
)

target_link_libraries(
        untitled_1
        -lglfw -lm
)

add_executable(
        untitled_2
        untitled_2.c
        glad.c
)

target_link_libraries(
        untitled_2
        -lglfw -lm
)

add_executable(
        untitled_3
        untitled_3.c
        glad.c
)

target_link_libraries(
        untitled_3
        -lglfw -lm
)


add_executable(
        untitled_4
        untitled_4.c
        glad.c
)

target_link_libraries(
        untitled_4
        -lglfw -lm
)
