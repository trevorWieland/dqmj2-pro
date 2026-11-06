.section .text
.arm
.global native_utility_child_arm7_wram_hw_037fe474
.type native_utility_child_arm7_wram_hw_037fe474, @function
native_utility_child_arm7_wram_hw_037fe474:
local_037fe474:
    mrs r0, cpsr
local_037fe478:
    and r0, r0, #0x1f
local_037fe47c:
    bx lr
.size native_utility_child_arm7_wram_hw_037fe474, .-native_utility_child_arm7_wram_hw_037fe474
