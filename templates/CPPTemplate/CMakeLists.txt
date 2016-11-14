cmake_minimum_required(VERSION 2.8)
project("proj")

if(EXISTS ${CMAKE_CURRENT_SOURCE_DIR}/build/conanbuildinfo.cmake)
    include(${CMAKE_CURRENT_SOURCE_DIR}/build/conanbuildinfo.cmake)
else()
    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
endif()
conan_basic_setup()

SET(VERSION_MAJOR "0")
SET(VERSION_MINOR "1")
SET(VERSION_PATCH "0")

SET (CMAKE_BUILD_TYPE Debug) # 默认构建Debug模式

include_directories(src include)

set( CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/bin )
set( CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib )
set( CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib )


file(GLOB_RECURSE source_files
        ${CMAKE_CURRENT_SOURCE_DIR}/src/*.cpp
    )
list(REMOVE_ITEM  source_files  ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp)


# 生成动态库目标
add_library(${PROJECT_NAME} SHARED ${source_files})
# 生成静态库目标
add_library(${PROJECT_NAME}_static STATIC ${source_files})

add_executable(${PROJECT_NAME}_run ${CMAKE_CURRENT_SOURCE_DIR}/src/main.cpp)
target_link_libraries(${PROJECT_NAME}_run ${PROJECT_NAME})


# 指定静态库的输出名称
set_target_properties(${PROJECT_NAME}_static PROPERTIES OUTPUT_NAME "${PROJECT_NAME}")

# 指定可执行文件的输出名称
set_target_properties(${PROJECT_NAME}_run PROPERTIES OUTPUT_NAME "${PROJECT_NAME}")

# 使动态库和静态库同时存在
set_target_properties(${PROJECT_NAME} PROPERTIES CLEAN_DIRECT_OUTPUT 1)
set_target_properties(${PROJECT_NAME}_static PROPERTIES CLEAN_DIRECT_OUTPUT 1)

# 指定动态库版本
# VERSION 动态库版本
# SOVERSION API版本
set_target_properties(${PROJECT_NAME} PROPERTIES VERSION 1.0 SOVERSION 1)



add_subdirectory(doc)
add_subdirectory(test)
