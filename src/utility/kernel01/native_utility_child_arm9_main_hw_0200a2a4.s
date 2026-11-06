.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a2a4
.type native_utility_child_arm9_main_hw_0200a2a4, @function
native_utility_child_arm9_main_hw_0200a2a4:
local_0200a2a4:
    mrc p15, 0, r0, c1, c0, 0
local_0200a2a8:
    bic r0, r0, #1
local_0200a2ac:
    mcr p15, 0, r0, c1, c0, 0
local_0200a2b0:
    bx lr
.size native_utility_child_arm9_main_hw_0200a2a4, .-native_utility_child_arm9_main_hw_0200a2a4
