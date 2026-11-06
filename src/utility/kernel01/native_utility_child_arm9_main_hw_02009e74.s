.section .text
.arm
.global native_utility_child_arm9_main_hw_02009e74
.type native_utility_child_arm9_main_hw_02009e74, @function
native_utility_child_arm9_main_hw_02009e74:
local_02009e74:
    add r1, r1, r0
local_02009e78:
    bic r0, r0, #0x1f
local_02009e7c:
    mcr p15, 0, r0, c7, c6, 1
local_02009e80:
    add r0, r0, #0x20
local_02009e84:
    cmp r0, r1
local_02009e88:
    blt local_02009e7c
local_02009e8c:
    bx lr
.size native_utility_child_arm9_main_hw_02009e74, .-native_utility_child_arm9_main_hw_02009e74
