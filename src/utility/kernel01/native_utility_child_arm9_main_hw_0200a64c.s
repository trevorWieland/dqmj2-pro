.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a64c
.type native_utility_child_arm9_main_hw_0200a64c, @function
native_utility_child_arm9_main_hw_0200a64c:
local_0200a64c:
    mrs r0, cpsr
local_0200a650:
    orr r1, r0, #0x80
local_0200a654:
    msr cpsr_c, r1
local_0200a658:
    and r0, r0, #0x80
local_0200a65c:
    bx lr
.size native_utility_child_arm9_main_hw_0200a64c, .-native_utility_child_arm9_main_hw_0200a64c
