.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fe448
.type native_utility_child_arm7_wram_hw_037fe448, @function
native_utility_child_arm7_wram_hw_037fe448:
local_037fe448:
    mrs r0, cpsr
local_037fe44c:
    orr r1, r0, #0xc0
local_037fe450:
    msr cpsr_c, r1
local_037fe454:
    and r0, r0, #0xc0
local_037fe458:
    bx lr
.size native_utility_child_arm7_wram_hw_037fe448, .-native_utility_child_arm7_wram_hw_037fe448
