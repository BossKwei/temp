# Minimal version of CMake
cmake_minimum_required (VERSION 3.7)

# Flags
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG} -D_GLIBCXX_DEBUG")
 
# Build type
if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
	message(STATUS "Setting build type to 'Debug' as none was specified.")
	set(CMAKE_BUILD_TYPE Debug CACHE STRING "Choose the type of build." FORCE)
	# Set the possible values of build type for cmake-gui
	set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release")
endif ()
 
# Define project name
project (OpenCL_Example)

# set (CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/")
 
find_package(OpenCL REQUIRED)

include_directories(${OPENCL_INCLUDE_DIR})

# Set up executable
add_executable (opencl_example src/main.cpp)
target_link_libraries(opencl_example ${OpenCL_LIBRARY})

