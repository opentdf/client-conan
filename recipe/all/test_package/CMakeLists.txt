cmake_minimum_required(VERSION 3.15)
project(test_package)

set(CMAKE_CXX_STANDARD 17)

#include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
#conan_basic_setup(TARGETS)

find_package(opentdf-client CONFIG REQUIRED)

add_executable(${PROJECT_NAME} test_package.cpp)
target_link_libraries(${PROJECT_NAME} opentdf-client::opentdf-client)


#cmake_minimum_required(VERSION 3.15)
#project(compressor C)

#find_package(ZLIB REQUIRED)

#add_executable(${PROJECT_NAME} src/main.c)
#target_link_libraries(${PROJECT_NAME} ZLIB::ZLIB)
