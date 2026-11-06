.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a638
.type native_utility_child_arm9_main_hw_0200a638, @function
native_utility_child_arm9_main_hw_0200a638:
local_0200a638:
    mrs r0, cpsr
local_0200a63c:
    bic r1, r0, #0x80
local_0200a640:
    msr cpsr_c, r1
local_0200a644:
    and r0, r0, #0x80
local_0200a648:
    bx lr
.size native_utility_child_arm9_main_hw_0200a638, .-native_utility_child_arm9_main_hw_0200a638
