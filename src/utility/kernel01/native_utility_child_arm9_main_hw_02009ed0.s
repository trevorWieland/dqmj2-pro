.section .text
.arm
.global native_utility_child_arm9_main_hw_02009ed0
.type native_utility_child_arm9_main_hw_02009ed0, @function
native_utility_child_arm9_main_hw_02009ed0:
local_02009ed0:
    mov r0, #0
local_02009ed4:
    mcr p15, 0, r0, c7, c10, 4
local_02009ed8:
    bx lr
.size native_utility_child_arm9_main_hw_02009ed0, .-native_utility_child_arm9_main_hw_02009ed0
