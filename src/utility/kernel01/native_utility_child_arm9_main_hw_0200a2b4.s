.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a2b4
.type native_utility_child_arm9_main_hw_0200a2b4, @function
native_utility_child_arm9_main_hw_0200a2b4:
local_0200a2b4:
    mrc p15, 0, r2, c5, c0, 2
local_0200a2b8:
    bic r2, r2, r0
local_0200a2bc:
    orr r2, r2, r1
local_0200a2c0:
    mcr p15, 0, r2, c5, c0, 2
local_0200a2c4:
    bx lr
.size native_utility_child_arm9_main_hw_0200a2b4, .-native_utility_child_arm9_main_hw_0200a2b4
