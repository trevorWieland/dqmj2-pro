.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a6b0
.type native_utility_child_arm9_main_hw_0200a6b0, @function
native_utility_child_arm9_main_hw_0200a6b0:
local_0200a6b0:
    mrs r0, cpsr
local_0200a6b4:
    and r0, r0, #0x1f
local_0200a6b8:
    bx lr
.size native_utility_child_arm9_main_hw_0200a6b0, .-native_utility_child_arm9_main_hw_0200a6b0
