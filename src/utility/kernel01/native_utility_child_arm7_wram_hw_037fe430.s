.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fe430
.type native_utility_child_arm7_wram_hw_037fe430, @function
native_utility_child_arm7_wram_hw_037fe430:
local_037fe430:
    mrs r1, cpsr
local_037fe434:
    bic r2, r1, #0x80
local_037fe438:
    orr r2, r2, r0
local_037fe43c:
    msr cpsr_c, r2
local_037fe440:
    and r0, r1, #0x80
local_037fe444:
    bx lr
.size native_utility_child_arm7_wram_hw_037fe430, .-native_utility_child_arm7_wram_hw_037fe430
