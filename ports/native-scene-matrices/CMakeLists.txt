cmake_minimum_required(VERSION 3.22)
project(j2p_native_scene_matrices LANGUAGES C)

get_filename_component(J2P_ROOT "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)
add_library(j2p_native_scene_matrices SHARED
    "${J2P_ROOT}/ports/common/guest_memory/guest_memory_20261106.c"
    "${J2P_ROOT}/ports/runtime/billboard_warm64/billboard_warm_20261107.c"
    "${J2P_ROOT}/ports/runtime/billboard_warm64/billboard_warm_math_20261107.c"
    "${J2P_ROOT}/ports/runtime/matrix64/matrix_20261106.c"
    "${J2P_ROOT}/ports/runtime/node_pose64/node_pose_arithmetic_20261106.c"
    "${J2P_ROOT}/ports/runtime/node_pose64/node_pose_decode_20261106.c"
    "${J2P_ROOT}/ports/runtime/node_pose64/node_pose_model_20261106.c"
    "${J2P_ROOT}/ports/runtime/static_matrix_plan64/static_matrix_frame_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_matrix_plan64/static_matrix_plan_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_matrix_plan64/static_matrix_walk_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_scene_events64/static_scene_bounds_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_scene_events64/static_scene_build_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_scene_events64/static_scene_material_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_scene_events64/static_scene_replay_20261107.c"
    "${J2P_ROOT}/ports/runtime/static_scene_events64/static_scene_walk_20261107.c"
    "${J2P_ROOT}/ports/runtime/stream_position64/position_display_20261107.c"
    "${J2P_ROOT}/ports/runtime/stream_position64/position_math_20261107.c"
    "${J2P_ROOT}/ports/runtime/stream_position64/position_walk_20261107.c"
    "${J2P_ROOT}/ports/runtime/stream_position64/stream_position_20261107.c"
)
target_include_directories(j2p_native_scene_matrices PUBLIC
    "${J2P_ROOT}/ports/common/guest_memory"
    "${J2P_ROOT}/ports/runtime/billboard_warm64"
    "${J2P_ROOT}/ports/runtime/matrix64"
    "${J2P_ROOT}/ports/runtime/node_pose64"
    "${J2P_ROOT}/ports/runtime/static_matrix_plan64"
    "${J2P_ROOT}/ports/runtime/static_scene_events64"
    "${J2P_ROOT}/ports/runtime/stream_position64"
)
set_target_properties(j2p_native_scene_matrices PROPERTIES
    C_STANDARD 11 C_STANDARD_REQUIRED ON C_EXTENSIONS OFF WINDOWS_EXPORT_ALL_SYMBOLS ON)
if(CMAKE_C_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(j2p_native_scene_matrices PRIVATE -Wall -Wextra -Werror -Wpedantic -fstrict-aliasing)
else()
    message(FATAL_ERROR "This target requires a qualified Clang or GCC C11 compiler")
endif()
if(NOT WIN32)
    target_link_options(j2p_native_scene_matrices PRIVATE "-Wl,--no-undefined")
endif()
if(ANDROID)
    target_link_options(j2p_native_scene_matrices PRIVATE
        "-Wl,-z,max-page-size=16384" "-Wl,-z,common-page-size=16384" "-Wl,-z,noexecstack")
endif()

include(CTest)
if(BUILD_TESTING AND NOT CMAKE_CROSSCOMPILING)
    find_package(Python3 REQUIRED COMPONENTS Interpreter)
    add_test(NAME synthetic_planner
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_LIST_DIR}/tests/planner/test_planner.py"
            "$<TARGET_FILE:j2p_native_scene_matrices>")
    add_test(NAME synthetic_scene
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_LIST_DIR}/tests/scene/test_scene.py"
            "$<TARGET_FILE:j2p_native_scene_matrices>")
    add_test(NAME synthetic_positions
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_LIST_DIR}/tests/position/test_positions.py"
            "$<TARGET_FILE:j2p_native_scene_matrices>")
    add_test(NAME synthetic_warm
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_LIST_DIR}/tests/test_warm.py"
            "$<TARGET_FILE:j2p_native_scene_matrices>")
endif()
