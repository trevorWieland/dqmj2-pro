.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a68c
.type native_utility_child_arm9_main_hw_0200a68c, @function
native_utility_child_arm9_main_hw_0200a68c:
local_0200a68c:
    mrs r1, cpsr
local_0200a690:
    bic r2, r1, #0xc0
local_0200a694:
    orr r2, r2, r0
local_0200a698:
    msr cpsr_c, r2
local_0200a69c:
    and r0, r1, #0xc0
local_0200a6a0:
    bx lr
.size native_utility_child_arm9_main_hw_0200a68c, .-native_utility_child_arm9_main_hw_0200a68c
