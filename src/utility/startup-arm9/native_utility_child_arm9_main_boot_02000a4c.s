.extern native_utility_child_arm9_data_02000bb4
.section .text
.arm
.global native_utility_child_arm9_main_boot_02000a4c
.type native_utility_child_arm9_main_boot_02000a4c, @function
native_utility_child_arm9_main_boot_02000a4c:
.global native_utility_child_arm9_arm_02000ac4
local_02000a4c:
    ldr r0, local_02000ac0
local_02000a50:
    ldr r1, [r0]
local_02000a54:
    ldr r2, [r0, #4]
local_02000a58:
    ldr r3, [r0, #8]
local_02000a5c:
    cmp r1, r2
local_02000a60:
    beq local_02000abc
local_02000a64:
    ldr r5, [r1], #4
local_02000a68:
    ldr r7, [r1], #4
local_02000a6c:
    add r6, r5, r7
local_02000a70:
    mov r4, r5
local_02000a74:
    cmp r4, r6
local_02000a78:
    ldrmi r7, [r3], #4
local_02000a7c:
    strmi r7, [r4], #4
local_02000a80:
    bmi local_02000a74
local_02000a84:
    ldr r7, [r1], #4
local_02000a88:
    add r6, r4, r7
local_02000a8c:
    mov r7, #0
local_02000a90:
    cmp r4, r6
local_02000a94:
    strlo r7, [r4], #4
local_02000a98:
    blo local_02000a90
local_02000a9c:
    bic r4, r5, #0x1f
local_02000aa0:
    mcr p15, 0, r7, c7, c10, 4
local_02000aa4:
    mcr p15, 0, r4, c7, c5, 1
local_02000aa8:
    mcr p15, 0, r4, c7, c14, 1
local_02000aac:
    add r4, r4, #0x20
local_02000ab0:
    cmp r4, r6
local_02000ab4:
    blt local_02000aa0
local_02000ab8:
    b local_02000a5c
local_02000abc:
    b local_02000ac4
local_02000ac0:
    .word native_utility_child_arm9_data_02000bb4
local_02000ac4:
native_utility_child_arm9_arm_02000ac4:
    bx lr
.size native_utility_child_arm9_main_boot_02000a4c, .-native_utility_child_arm9_main_boot_02000a4c
