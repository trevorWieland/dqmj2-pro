.section .text
.thumb
.global native_utility_child_arm7_wram_hw_038028be
.type native_utility_child_arm7_wram_hw_038028be, @function
native_utility_child_arm7_wram_hw_038028be:
local_038028be:
    add r1, r0, #0
local_038028c0:
    mov r0, #0
local_038028c2:
    swi 8
local_038028c4:
    bx lr
.size native_utility_child_arm7_wram_hw_038028be, .-native_utility_child_arm7_wram_hw_038028be
