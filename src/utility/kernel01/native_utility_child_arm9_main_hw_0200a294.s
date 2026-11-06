.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a294
.type native_utility_child_arm9_main_hw_0200a294, @function
native_utility_child_arm9_main_hw_0200a294:
local_0200a294:
    mrc p15, 0, r0, c1, c0, 0
local_0200a298:
    orr r0, r0, #1
local_0200a29c:
    mcr p15, 0, r0, c1, c0, 0
local_0200a2a0:
    bx lr
.size native_utility_child_arm9_main_hw_0200a294, .-native_utility_child_arm9_main_hw_0200a294
