.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fe41c
.type native_utility_child_arm7_wram_hw_037fe41c, @function
native_utility_child_arm7_wram_hw_037fe41c:
local_037fe41c:
    mrs r0, cpsr
local_037fe420:
    orr r1, r0, #0x80
local_037fe424:
    msr cpsr_c, r1
local_037fe428:
    and r0, r0, #0x80
local_037fe42c:
    bx lr
.size native_utility_child_arm7_wram_hw_037fe41c, .-native_utility_child_arm7_wram_hw_037fe41c
