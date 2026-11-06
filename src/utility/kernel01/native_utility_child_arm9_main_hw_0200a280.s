.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a280
.type native_utility_child_arm9_main_hw_0200a280, @function
native_utility_child_arm9_main_hw_0200a280:
local_0200a280:
    mrc p15, 0, r0, c9, c1, 0
local_0200a284:
    ldr r1, local_0200a290
local_0200a288:
    and r0, r0, r1
local_0200a28c:
    bx lr
local_0200a290: .word 0xfffff000
.size native_utility_child_arm9_main_hw_0200a280, .-native_utility_child_arm9_main_hw_0200a280
