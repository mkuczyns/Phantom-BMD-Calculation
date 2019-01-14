# This is the root ITK CMakeLists file.
cmake_minimum_required(VERSION 2.8.12)
if(COMMAND CMAKE_POLICY)
  cmake_policy(SET CMP0003 NEW)
endif()


# This project is designed to be built outside the Insight source tree.
project(automatic_BMD_calculation)

# Find ITK.
find_package(ITK REQUIRED)
include(${ITK_USE_FILE})

add_executable(automatic_BMD_calculation automatic_BMD_calculation.cxx )

target_link_libraries(automatic_BMD_calculation ${ITK_LIBRARIES})
