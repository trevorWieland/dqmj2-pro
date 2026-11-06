.section .text
.arm
.global native_utility_child_arm9_main_hw_02009e40
.type native_utility_child_arm9_main_hw_02009e40, @function
native_utility_child_arm9_main_hw_02009e40:
local_02009e40:
    mov ip, #0
local_02009e44:
    mov r1, #0
local_02009e48:
    mov r0, #0
local_02009e4c:
    orr r2, r1, r0
local_02009e50:
    mcr p15, 0, ip, c7, c10, 4
local_02009e54:
    mcr p15, 0, r2, c7, c14, 2
local_02009e58:
    add r0, r0, #0x20
local_02009e5c:
    cmp r0, #0x400
local_02009e60:
    blt local_02009e4c
local_02009e64:
    add r1, r1, #0x40000000
local_02009e68:
    cmp r1, #0
local_02009e6c:
    bne local_02009e48
local_02009e70:
    bx lr
.size native_utility_child_arm9_main_hw_02009e40, .-native_utility_child_arm9_main_hw_02009e40
