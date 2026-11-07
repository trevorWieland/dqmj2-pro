cmake_minimum_required(VERSION 3.22)
project(j2p_native_storage LANGUAGES C)

get_filename_component(J2P_ROOT "${CMAKE_CURRENT_LIST_DIR}/../.." ABSOLUTE)
add_library(j2p_native_storage SHARED
    "${J2P_ROOT}/ports/common/guest_memory/guest_memory_20261106.c"
    "${J2P_ROOT}/ports/runtime/card_cache64/card_cache_wire_v2_20261106.c"
    "${J2P_ROOT}/ports/runtime/card_reader64/card_reader_wire_20261106.c"
    "${J2P_ROOT}/ports/runtime/card_reader64/host_readonly_file_20261106.c"
)
target_include_directories(j2p_native_storage PUBLIC
    "${J2P_ROOT}/ports/common/guest_memory"
    "${J2P_ROOT}/ports/runtime/card_reader64"
)
target_compile_features(j2p_native_storage PUBLIC c_std_11)
set_target_properties(j2p_native_storage PROPERTIES
    C_EXTENSIONS OFF
    WINDOWS_EXPORT_ALL_SYMBOLS ON
)
if(CMAKE_C_COMPILER_ID MATCHES "Clang|GNU")
    target_compile_options(j2p_native_storage PRIVATE -Wall -Wextra -Werror -fstrict-aliasing)
elseif(MSVC)
    target_compile_options(j2p_native_storage PRIVATE /W4 /WX)
endif()
if(WIN32)
    target_link_libraries(j2p_native_storage PRIVATE kernel32)
else()
    target_compile_definitions(j2p_native_storage PRIVATE _POSIX_C_SOURCE=200809L)
endif()
if(ANDROID)
    target_link_options(j2p_native_storage PRIVATE
        "-Wl,--no-undefined"
        "-Wl,-z,max-page-size=16384"
        "-Wl,-z,common-page-size=16384"
    )
endif()

include(CTest)
if(BUILD_TESTING AND NOT CMAKE_CROSSCOMPILING)
    find_package(Python3 REQUIRED COMPONENTS Interpreter)
    add_test(NAME synthetic_storage_contract
        COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_LIST_DIR}/test_storage.py"
            --library "$<TARGET_FILE:j2p_native_storage>"
            --work "${CMAKE_CURRENT_BINARY_DIR}/synthetic-fixtures"
    )
endif()
