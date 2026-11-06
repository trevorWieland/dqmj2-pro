.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a87c
.type native_utility_child_arm9_main_hw_0200a87c, @function
native_utility_child_arm9_main_hw_0200a87c:
local_0200a87c:
    mov r0, #0
local_0200a880:
    mcr p15, 0, r0, c7, c0, 4
local_0200a884:
    bx lr
.size native_utility_child_arm9_main_hw_0200a87c, .-native_utility_child_arm9_main_hw_0200a87c
