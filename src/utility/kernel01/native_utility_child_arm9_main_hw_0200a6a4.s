.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a6a4
.type native_utility_child_arm9_main_hw_0200a6a4, @function
native_utility_child_arm9_main_hw_0200a6a4:
local_0200a6a4:
    mrs r0, cpsr
local_0200a6a8:
    and r0, r0, #0x80
local_0200a6ac:
    bx lr
.size native_utility_child_arm9_main_hw_0200a6a4, .-native_utility_child_arm9_main_hw_0200a6a4
