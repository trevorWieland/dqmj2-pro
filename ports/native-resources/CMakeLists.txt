cmake_minimum_required(VERSION 3.22)
project(j2p_native_resources LANGUAGES C)

get_filename_component(J2P_ROOT "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)
set(J2P_RESOURCE_ROOT "${J2P_ROOT}/ports/runtime/resource64")
add_library(j2p_native_resources SHARED
    "${J2P_ROOT}/ports/common/guest_memory/guest_memory_20261106.c"
    "${J2P_ROOT}/ports/runtime/card_cache64/card_cache_wire_v2_20261106.c"
    "${J2P_ROOT}/ports/runtime/card_reader64/card_reader_wire_20261106.c"
    "${J2P_ROOT}/ports/runtime/card_reader64/host_readonly_file_20261106.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_resource_bridge_20261106.c"
    "${J2P_ROOT}/src/runtime/20261031_resource_load/native_main_0203cb8c.c"
    "${J2P_ROOT}/src/runtime/20261031_overlay_file_size250/file_size.c"
    "${J2P_ROOT}/src/runtime/20261031_allocation_dispatch_word_index/native_main_0202a37c.c"
    "${J2P_RESOURCE_ROOT}/resource_thunk_prototype_20261106.c"
    "${J2P_RESOURCE_ROOT}/g3d_dictionary_wire_20261106.c"
    "${J2P_RESOURCE_ROOT}/g3d_texture_material_20261106.c"
    "${J2P_ROOT}/src/runtime/20261102_texture_pattern436/native_main_02034248.c"
    "${J2P_ROOT}/src/runtime/20261102_texture_pattern436/native_main_02034320.c"
    "${J2P_RESOURCE_ROOT}/g3d_texture_inline_exports_20261106.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_20261106.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200a7cc.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200a968.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200aa00.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200ab2c.c"
    "${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200b0bc.c"
)
target_include_directories(j2p_native_resources PUBLIC
    "${J2P_ROOT}/ports/common/guest_memory"
    "${J2P_ROOT}/ports/runtime/card_reader64"
    "${J2P_RESOURCE_ROOT}"
)
set_target_properties(j2p_native_resources PROPERTIES
    C_STANDARD 11
    C_STANDARD_REQUIRED ON
    C_EXTENSIONS OFF
    WINDOWS_EXPORT_ALL_SYMBOLS ON
)
if(CMAKE_C_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(j2p_native_resources PRIVATE -Wall -Wextra -Werror -fstrict-aliasing)
    set_source_files_properties("${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200a7cc.c"
        "${J2P_RESOURCE_ROOT}/nitrofs_views_20261106/fs_0200ab2c.c"
        PROPERTIES COMPILE_OPTIONS "-Wno-sign-compare")
else()
    message(FATAL_ERROR "This target requires a qualified Clang or GCC C11 compiler")
endif()
if(WIN32)
    target_link_libraries(j2p_native_resources PRIVATE kernel32)
else()
    target_compile_definitions(j2p_native_resources PRIVATE _POSIX_C_SOURCE=200809L)
    target_link_options(j2p_native_resources PRIVATE "-Wl,--no-undefined")
endif()
if(ANDROID)
    target_link_options(j2p_native_resources PRIVATE
        "-Wl,-z,max-page-size=16384"
        "-Wl,-z,common-page-size=16384"
        "-Wl,-z,noexecstack"
    )
endif()

include(CTest)
if(BUILD_TESTING AND NOT CMAKE_CROSSCOMPILING)
    find_package(Python3 REQUIRED COMPONENTS Interpreter)
    add_test(NAME synthetic_resource_contract
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_LIST_DIR}/test_resources.py"
            --library "$<TARGET_FILE:j2p_native_resources>"
            --work "${CMAKE_CURRENT_BINARY_DIR}/synthetic-fixtures"
    )
endif()
