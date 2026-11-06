.section .text
.arm
.global native_utility_child_arm9_main_hw_02009e90
.type native_utility_child_arm9_main_hw_02009e90, @function
native_utility_child_arm9_main_hw_02009e90:
local_02009e90:
    add r1, r1, r0
local_02009e94:
    bic r0, r0, #0x1f
local_02009e98:
    mcr p15, 0, r0, c7, c10, 1
local_02009e9c:
    add r0, r0, #0x20
local_02009ea0:
    cmp r0, r1
local_02009ea4:
    blt local_02009e98
local_02009ea8:
    bx lr
.size native_utility_child_arm9_main_hw_02009e90, .-native_utility_child_arm9_main_hw_02009e90
