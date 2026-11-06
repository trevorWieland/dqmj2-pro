.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fe45c
.type native_utility_child_arm7_wram_hw_037fe45c, @function
native_utility_child_arm7_wram_hw_037fe45c:
local_037fe45c:
    mrs r1, cpsr
local_037fe460:
    bic r2, r1, #0xc0
local_037fe464:
    orr r2, r2, r0
local_037fe468:
    msr cpsr_c, r2
local_037fe46c:
    and r0, r1, #0xc0
local_037fe470:
    bx lr
.size native_utility_child_arm7_wram_hw_037fe45c, .-native_utility_child_arm7_wram_hw_037fe45c
