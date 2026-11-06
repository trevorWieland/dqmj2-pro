.section .text
.arm
.global native_utility_child_arm9_main_hw_02009edc
.type native_utility_child_arm9_main_hw_02009edc, @function
native_utility_child_arm9_main_hw_02009edc:
local_02009edc:
    add r1, r1, r0
local_02009ee0:
    bic r0, r0, #0x1f
local_02009ee4:
    mcr p15, 0, r0, c7, c5, 1
local_02009ee8:
    add r0, r0, #0x20
local_02009eec:
    cmp r0, r1
local_02009ef0:
    blt local_02009ee4
local_02009ef4:
    bx lr
.size native_utility_child_arm9_main_hw_02009edc, .-native_utility_child_arm9_main_hw_02009edc
