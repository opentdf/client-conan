cmake_minimum_required(VERSION 3.1)
project(test_package)

set(CMAKE_CXX_STANDARD 17)

include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup(TARGETS)

find_package(opentdf-client CONFIG REQUIRED)

if("$ENV{VBUILD_CODE_COVERAGE}" STREQUAL "true")
    message(STATUS "Adding code coverage compilation flag")
    add_compile_options(--coverage)
else()
    message(STATUS "Skipping code coverage compilation flag")
endif()

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} opentdf-client::opentdf-client)

# Add gcov if code coverage is being done
if("$ENV{VBUILD_CODE_COVERAGE}" STREQUAL "true")
    target_link_libraries(${PROJECT_NAME} gcov)
endif()

