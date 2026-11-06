.extern native_utility_child_arm9_arm_0200098c
.extern native_utility_child_arm9_arm_020009a0
.extern native_utility_child_arm9_arm_02000a4c
.extern native_utility_child_arm9_arm_02000ac8
.extern native_utility_child_arm9_arm_02000bb0
.extern native_utility_child_arm9_arm_020111e4
.extern native_utility_child_arm9_data_01ff8000
.extern native_utility_child_arm9_data_02000bb4
.extern native_utility_child_arm9_data_027e0000
.extern native_utility_child_arm9_thumb_02000bd9
.extern native_utility_child_arm9_thumb_020111e8
.section .text
.arm
.global native_utility_child_arm9_main_boot_02000850
.type native_utility_child_arm9_main_boot_02000850, @function
native_utility_child_arm9_main_boot_02000850:
local_02000850:
    mov ip, #0x4000000
local_02000854:
    str ip, [ip, #0x208]
local_02000858:
    ldrh r0, [ip, #6]
local_0200085c:
    cmp r0, #0
local_02000860:
    bne local_02000858
local_02000864:
    bl native_utility_child_arm9_arm_02000ac8
local_02000868:
    mov r0, #0x13
local_0200086c:
    msr cpsr_c, r0
local_02000870:
    ldr r0, local_02000968
local_02000874:
    add r0, r0, #0x3fc0
local_02000878:
    mov sp, r0
local_0200087c:
    mov r0, #0x12
local_02000880:
    msr cpsr_c, r0
local_02000884:
    ldr r0, local_02000968
local_02000888:
    add r0, r0, #0x3fc0
local_0200088c:
    sub r0, r0, #0x40
local_02000890:
    sub sp, r0, #4
local_02000894:
    tst sp, #4
local_02000898:
    subeq sp, sp, #4
local_0200089c:
    ldr r1, local_0200096c
local_020008a0:
    sub r1, r0, r1
local_020008a4:
    mov r0, #0x1f
local_020008a8:
    msr cpsr_fsxc, r0
local_020008ac:
    sub sp, r1, #4
local_020008b0:
    mov r0, #0
local_020008b4:
    ldr r1, local_02000968
local_020008b8:
    mov r2, #0x4000
local_020008bc:
    bl native_utility_child_arm9_arm_0200098c
local_020008c0:
    mov r0, #0
local_020008c4:
    ldr r1, local_02000970
local_020008c8:
    mov r2, #0x400
local_020008cc:
    bl native_utility_child_arm9_arm_0200098c
local_020008d0:
    mov r0, #0x200
local_020008d4:
    ldr r1, local_02000974
local_020008d8:
    mov r2, #0x400
local_020008dc:
    bl native_utility_child_arm9_arm_0200098c
local_020008e0:
    ldr r1, local_02000978
local_020008e4:
    ldr r0, [r1, #0x14]
local_020008e8:
    bl native_utility_child_arm9_arm_020009a0
local_020008ec:
    bl native_utility_child_arm9_arm_02000a4c
local_020008f0:
    ldr r0, local_02000978
local_020008f4:
    ldr r1, [r0, #0xc]
local_020008f8:
    ldr r2, [r0, #0x10]
local_020008fc:
    mov r3, r1
local_02000900:
    mov r0, #0
local_02000904:
    cmp r1, r2
local_02000908:
    strlo r0, [r1], #4
local_0200090c:
    blo local_02000904
local_02000910:
    bic r1, r3, #0x1f
local_02000914:
    mcr p15, 0, r0, c7, c10, 4
local_02000918:
    mcr p15, 0, r1, c7, c5, 1
local_0200091c:
    mcr p15, 0, r1, c7, c14, 1
local_02000920:
    add r1, r1, #0x20
local_02000924:
    cmp r1, r2
local_02000928:
    blt local_02000914
local_0200092c:
    ldr r1, local_0200097c
local_02000930:
    str r0, [r1]
local_02000934:
    ldr r1, local_02000968
local_02000938:
    add r1, r1, #0x3fc0
local_0200093c:
    add r1, r1, #0x3c
local_02000940:
    ldr r0, local_02000980
local_02000944:
    str r0, [r1]
local_02000948:
    bl native_utility_child_arm9_arm_020111e4
local_0200094c:
    bl native_utility_child_arm9_arm_02000bb0
local_02000950:
    blx native_utility_child_arm9_thumb_020111e8
local_02000954:
    ldr r1, local_02000984
local_02000958:
    ldr lr, local_02000988
local_0200095c:
    tst sp, #4
local_02000960:
    subne sp, sp, #4
local_02000964:
    bx r1
local_02000968:
    .word native_utility_child_arm9_data_027e0000
local_0200096c:
    .word 0x400
local_02000970:
    .word 0x5000000
local_02000974:
    .word 0x7000000
local_02000978:
    .word native_utility_child_arm9_data_02000bb4
local_0200097c:
    .word 0x27fff9c
local_02000980:
    .word native_utility_child_arm9_data_01ff8000
local_02000984:
    .word native_utility_child_arm9_thumb_02000bd9
local_02000988:
    .word 0xffff0000
.size native_utility_child_arm9_main_boot_02000850, .-native_utility_child_arm9_main_boot_02000850
