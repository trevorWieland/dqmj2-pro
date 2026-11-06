.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a678
.type native_utility_child_arm9_main_hw_0200a678, @function
native_utility_child_arm9_main_hw_0200a678:
local_0200a678:
    mrs r0, cpsr
local_0200a67c:
    orr r1, r0, #0xc0
local_0200a680:
    msr cpsr_c, r1
local_0200a684:
    and r0, r0, #0xc0
local_0200a688:
    bx lr
.size native_utility_child_arm9_main_hw_0200a678, .-native_utility_child_arm9_main_hw_0200a678
