
.section .text
.arm
.global native_utility_child_arm9_main_boot_02000ac8
.type native_utility_child_arm9_main_boot_02000ac8, @function
native_utility_child_arm9_main_boot_02000ac8:
local_02000ac8:
    mrc p15, 0, r0, c1, c0, 0
local_02000acc:
    ldr r1, local_02000b80
local_02000ad0:
    bic r0, r0, r1
local_02000ad4:
    mcr p15, 0, r0, c1, c0, 0
local_02000ad8:
    mov r0, #0
local_02000adc:
    mcr p15, 0, r0, c7, c5, 0
local_02000ae0:
    mcr p15, 0, r0, c7, c6, 0
local_02000ae4:
    mcr p15, 0, r0, c7, c10, 4
local_02000ae8:
    ldr r0, local_02000b84
local_02000aec:
    mcr p15, 0, r0, c6, c0, 0
local_02000af0:
    ldr r0, local_02000b88
local_02000af4:
    mcr p15, 0, r0, c6, c1, 0
local_02000af8:
    ldr r0, local_02000b8c
local_02000afc:
    mcr p15, 0, r0, c6, c2, 0
local_02000b00:
    ldr r0, local_02000b90
local_02000b04:
    mcr p15, 0, r0, c6, c3, 0
local_02000b08:
    ldr r0, local_02000b94
local_02000b0c:
    orr r0, r0, #0x1a
local_02000b10:
    orr r0, r0, #1
local_02000b14:
    mcr p15, 0, r0, c6, c4, 0
local_02000b18:
    ldr r0, local_02000b98
local_02000b1c:
    mcr p15, 0, r0, c6, c5, 0
local_02000b20:
    ldr r0, local_02000b9c
local_02000b24:
    mcr p15, 0, r0, c6, c6, 0
local_02000b28:
    ldr r0, local_02000ba0
local_02000b2c:
    mcr p15, 0, r0, c6, c7, 0
local_02000b30:
    mov r0, #0x20
local_02000b34:
    mcr p15, 0, r0, c9, c1, 1
local_02000b38:
    ldr r0, local_02000b94
local_02000b3c:
    orr r0, r0, #0xa
local_02000b40:
    mcr p15, 0, r0, c9, c1, 0
local_02000b44:
    mov r0, #0x42
local_02000b48:
    mcr p15, 0, r0, c2, c0, 1
local_02000b4c:
    mov r0, #0x42
local_02000b50:
    mcr p15, 0, r0, c2, c0, 0
local_02000b54:
    mov r0, #2
local_02000b58:
    mcr p15, 0, r0, c3, c0, 0
local_02000b5c:
    ldr r0, local_02000ba4
local_02000b60:
    mcr p15, 0, r0, c5, c0, 3
local_02000b64:
    ldr r0, local_02000ba8
local_02000b68:
    mcr p15, 0, r0, c5, c0, 2
local_02000b6c:
    mrc p15, 0, r0, c1, c0, 0
local_02000b70:
    ldr r1, local_02000bac
local_02000b74:
    orr r0, r0, r1
local_02000b78:
    mcr p15, 0, r0, c1, c0, 0
local_02000b7c:
    bx lr
local_02000b80:
    .word 0xf9005
local_02000b84:
    .word 0x4000033
local_02000b88:
    .word 0x200002d
local_02000b8c:
    .word 0x27e0021
local_02000b90:
    .word 0x8000035
local_02000b94:
    .word 0x27e0000
local_02000b98:
    .word 0x100002f
local_02000b9c:
    .word 0xffff001d
local_02000ba0:
    .word 0x27ff017
local_02000ba4:
    .word 0x5100011
local_02000ba8:
    .word 0x15111011
local_02000bac:
    .word 0x5707d
.size native_utility_child_arm9_main_boot_02000ac8, .-native_utility_child_arm9_main_boot_02000ac8
