.section .text
.thumb
.global native_utility_child_arm7_wram_hw_038028b6
.type native_utility_child_arm7_wram_hw_038028b6, @function
native_utility_child_arm7_wram_hw_038028b6:
local_038028b6:
    add r1, r0, #0
local_038028b8:
    mov r0, #1
local_038028ba:
    swi 8
local_038028bc:
    bx lr
.size native_utility_child_arm7_wram_hw_038028b6, .-native_utility_child_arm7_wram_hw_038028b6
