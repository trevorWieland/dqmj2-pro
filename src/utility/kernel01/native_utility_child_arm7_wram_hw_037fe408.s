.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fe408
.type native_utility_child_arm7_wram_hw_037fe408, @function
native_utility_child_arm7_wram_hw_037fe408:
local_037fe408:
    mrs r0, cpsr
local_037fe40c:
    bic r1, r0, #0x80
local_037fe410:
    msr cpsr_c, r1
local_037fe414:
    and r0, r0, #0x80
local_037fe418:
    bx lr
.size native_utility_child_arm7_wram_hw_037fe408, .-native_utility_child_arm7_wram_hw_037fe408
