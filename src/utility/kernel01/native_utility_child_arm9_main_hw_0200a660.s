.section .text
.arm
.global native_utility_child_arm9_main_hw_0200a660
.type native_utility_child_arm9_main_hw_0200a660, @function
native_utility_child_arm9_main_hw_0200a660:
local_0200a660:
    mrs r1, cpsr
local_0200a664:
    bic r2, r1, #0x80
local_0200a668:
    orr r2, r2, r0
local_0200a66c:
    msr cpsr_c, r2
local_0200a670:
    and r0, r1, #0x80
local_0200a674:
    bx lr
.size native_utility_child_arm9_main_hw_0200a660, .-native_utility_child_arm9_main_hw_0200a660
