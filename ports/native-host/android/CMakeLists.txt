cmake_minimum_required(VERSION 3.22)
project(j2p_dualsurface LANGUAGES C)
get_filename_component(J2P_ROOT "${CMAKE_CURRENT_LIST_DIR}/../../.." ABSOLUTE)
set(BUILD_TESTING OFF CACHE BOOL "" FORCE)
set(J2P_BUILD_ROMFREE_PROBE OFF CACHE BOOL "" FORCE)
add_subdirectory("${J2P_ROOT}/ports/native-scene-matrices" "${CMAKE_CURRENT_BINARY_DIR}/c7")
find_package(Python3 REQUIRED COMPONENTS Interpreter)
set(FIXTURES "${CMAKE_CURRENT_BINARY_DIR}/generated/fixtures.h")
add_custom_command(OUTPUT "${FIXTURES}"
    COMMAND "${Python3_EXECUTABLE}" "${J2P_ROOT}/ports/native-scene-matrices/tests/native/generate_fixtures.py" "${FIXTURES}"
    DEPENDS "${J2P_ROOT}/ports/native-scene-matrices/tests/native/generate_fixtures.py"
        "${J2P_ROOT}/ports/native-scene-matrices/tests/position/copied-position-fixtures.json"
        "${J2P_ROOT}/ports/native-scene-matrices/tests/scene/copied-synthetic-fixtures-v2.json"
        "${J2P_ROOT}/ports/native-scene-matrices/tests/warm/warm_api.py"
        "${J2P_ROOT}/ports/native-scene-matrices/tests/warm/synthetic_cases.py" VERBATIM)
add_library(j2p_probe OBJECT "${J2P_ROOT}/ports/native-scene-matrices/tests/native/probe.c" "${FIXTURES}")
target_compile_definitions(j2p_probe PRIVATE main=j2p_probe_run)
target_include_directories(j2p_probe PRIVATE "${CMAKE_CURRENT_BINARY_DIR}/generated")
target_link_libraries(j2p_probe PRIVATE j2p_native_scene_matrices)
set_target_properties(j2p_probe PROPERTIES POSITION_INDEPENDENT_CODE ON)
add_library(j2p_dualsurface SHARED native/bridge_android.c ../common/host_session.c $<TARGET_OBJECTS:j2p_probe>)
target_include_directories(j2p_dualsurface PUBLIC native ../common)
target_link_libraries(j2p_dualsurface PRIVATE j2p_native_scene_matrices android log)
set_target_properties(j2p_dualsurface PROPERTIES C_STANDARD 11 C_STANDARD_REQUIRED ON C_EXTENSIONS OFF)
target_compile_options(j2p_dualsurface PRIVATE -Wall -Wextra -Werror -Wpedantic -fstrict-aliasing)
target_link_options(j2p_dualsurface PRIVATE -Wl,--no-undefined -Wl,-z,max-page-size=16384 -Wl,-z,common-page-size=16384 -Wl,-z,noexecstack)
