.section .text
.arm
.global native_utility_child_arm9_main_hw_02009eac
.type native_utility_child_arm9_main_hw_02009eac, @function
native_utility_child_arm9_main_hw_02009eac:
local_02009eac:
    mov ip, #0
local_02009eb0:
    add r1, r1, r0
local_02009eb4:
    bic r0, r0, #0x1f
local_02009eb8:
    mcr p15, 0, ip, c7, c10, 4
local_02009ebc:
    mcr p15, 0, r0, c7, c14, 1
local_02009ec0:
    add r0, r0, #0x20
local_02009ec4:
    cmp r0, r1
local_02009ec8:
    blt local_02009eb8
local_02009ecc:
    bx lr
.size native_utility_child_arm9_main_hw_02009eac, .-native_utility_child_arm9_main_hw_02009eac
