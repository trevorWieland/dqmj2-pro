/* ov006 row 0x021f3b10: 724 bytes.
 *
 * What it does: switch dispatch through an inline table
 *
 * Carrier: mwasmarm .s with .hword table data.
 * The measured extent is code plus data inside the function. The data
 * runs are emitted as data, not decoded as instructions; every
 * instruction, branch target, pool word and table entry is read from
 * the image.
 *
 * Unknowns: the field roles and the meaning of the table entries are not established by byte identity.
 */
.section .text
.thumb
.extern native_data_0220b344
.extern native_fn_021f3a78
.extern native_fn_021ff6d4
.global native_ov006_021f3b10
.type native_ov006_021f3b10, @function
native_ov006_021f3b10:
    push {r4, r5, r6, lr}
    ldr r6, .L_pool_021f3d7c
    add r5, r0, #0x0
    ldr r3, [r6, #0]
    ldr r0, .L_pool_021f3d80
    ldr r1, .L_pool_021f3d84
    ldrsb r4, [r3, r0]
    lsl r2, r4, #0x2
    add r1, r1, r2
    ldrsb r1, [r5, r1]
    strb r1, [r3, r0]
    ldr r2, [r6, #0]
    ldrsb r1, [r2, r0]
    cmp r1, #0x2e
    bne .L_021f3b38
    cmp r5, #0x3
    bne .L_021f3b38
    sub r0, r0, #0x1
    strb r4, [r2, r0]
    b .L_021f3dd4
.L_021f3b38:
    cmp r1, #0x33
    bne .L_021f3b4c
    cmp r5, #0x1
    beq .L_021f3b44
    cmp r5, #0x3
    bne .L_021f3b4c
.L_021f3b44:
    mov r0, #0x12
    lsl r0, r0, #0x4
    strb r4, [r2, r0]
    b .L_021f3dd4
.L_021f3b4c:
    cmp r1, #0x34
    bne .L_021f3b66
    cmp r5, #0x1
    beq .L_021f3b58
    cmp r5, #0x3
    bne .L_021f3b66
.L_021f3b58:
    cmp r4, #0x2e
    bne .L_021f3b5e
    b .L_021f3dd4
.L_021f3b5e:
    mov r0, #0x12
    lsl r0, r0, #0x4
    strb r4, [r2, r0]
    b .L_021f3dd4
.L_021f3b66:
    mov r3, #0x0
    mvn r3, r3
    cmp r1, r3
    bne .L_021f3b90
    mov r0, #0x12
    lsl r0, r0, #0x4
    ldrsb r0, [r2, r0]
    cmp r0, #0x23
    beq .L_021f3b7c
    cmp r0, #0x32
    bne .L_021f3b86
.L_021f3b7c:
    mov r1, #0x23
    add r0, r1, #0x0
    add r0, #0xfe
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3b86:
    mov r1, #0x22
    add r0, r1, #0x0
    add r0, #0xff
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3b90:
    sub r0, r3, #0x1
    cmp r1, r0
    bne .L_021f3c14
    mov r0, #0x12
    lsl r0, r0, #0x4
    ldrsb r1, [r2, r0]
    cmp r1, #0x26
    bgt .L_021f3bc8
    bge .L_021f3bec
    cmp r1, #0x5
    bgt .L_021f3bc2
    cmp r1, #0x0
    blt .L_021f3c0a
    add r0, r1, r1
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0020
    .hword 0x002a
    .hword 0x0052
    .hword 0x0034
    .hword 0x003e
    .hword 0x0048
.L_021f3bc2:
    cmp r1, #0x24
    beq .L_021f3be2
    b .L_021f3c0a
.L_021f3bc8:
    cmp r1, #0x28
    bgt .L_021f3bd4
    bge .L_021f3c00
    cmp r1, #0x27
    beq .L_021f3bf6
    b .L_021f3c0a
.L_021f3bd4:
    cmp r1, #0x31
    bne .L_021f3c0a
    mov r1, #0x31
    add r0, r1, #0x0
    add r0, #0xf0
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3be2:
    mov r1, #0x24
    add r0, r1, #0x0
    add r0, #0xfd
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3bec:
    mov r1, #0x26
    add r0, r1, #0x0
    add r0, #0xfb
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3bf6:
    mov r1, #0x27
    add r0, r1, #0x0
    add r0, #0xfa
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3c00:
    mov r1, #0x28
    add r0, r1, #0x0
    add r0, #0xf9
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3c0a:
    mov r1, #0x25
    add r0, r1, #0x0
    add r0, #0xfc
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3c14:
    sub r0, r3, #0x2
    cmp r1, r0
    bne .L_021f3cb4
    mov r0, #0x12
    lsl r0, r0, #0x4
    ldrsb r1, [r2, r0]
    cmp r1, #0x23
    bgt .L_021f3c58
    bge .L_021f3ca0
    cmp r1, #0xb
    bgt .L_021f3c52
    cmp r1, #0x0
    blt .L_021f3caa
    add r0, r1, r1
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x006e
    .hword 0x006e
    .hword 0x006e
    .hword 0x006e
    .hword 0x006e
    .hword 0x006e
    .hword 0x003c
    .hword 0x0046
    .hword 0x006e
    .hword 0x0050
    .hword 0x005a
    .hword 0x0064
.L_021f3c52:
    cmp r1, #0x22
    beq .L_021f3ca0
    b .L_021f3caa
.L_021f3c58:
    cmp r1, #0x2a
    bgt .L_021f3c64
    bge .L_021f3c82
    cmp r1, #0x29
    beq .L_021f3c78
    b .L_021f3caa
.L_021f3c64:
    cmp r1, #0x32
    bgt .L_021f3caa
    cmp r1, #0x2c
    blt .L_021f3caa
    beq .L_021f3c8c
    cmp r1, #0x2d
    beq .L_021f3c96
    cmp r1, #0x32
    beq .L_021f3ca0
    b .L_021f3caa
.L_021f3c78:
    mov r1, #0x29
    add r0, r1, #0x0
    add r0, #0xf8
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3c82:
    mov r1, #0x2a
    add r0, r1, #0x0
    add r0, #0xf7
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3c8c:
    mov r1, #0x2c
    add r0, r1, #0x0
    add r0, #0xf5
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3c96:
    mov r1, #0x2d
    add r0, r1, #0x0
    add r0, #0xf4
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3ca0:
    mov r1, #0x2e
    add r0, r1, #0x0
    add r0, #0xf3
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3caa:
    mov r1, #0x2b
    add r0, r1, #0x0
    add r0, #0xf6
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3cb4:
    sub r0, r3, #0x3
    cmp r1, r0
    bne .L_021f3d2c
    mov r0, #0x12
    lsl r0, r0, #0x4
    ldrsb r1, [r2, r0]
    cmp r1, #0x26
    bgt .L_021f3cec
    bge .L_021f3d0c
    cmp r1, #0x5
    bgt .L_021f3ce6
    cmp r1, #0x0
    blt .L_021f3d24
    add r0, r1, r1
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0020
    .hword 0x0028
    .hword 0x0048
    .hword 0x0030
    .hword 0x0038
    .hword 0x0040
.L_021f3ce6:
    cmp r1, #0x24
    beq .L_021f3d04
    b .L_021f3d24
.L_021f3cec:
    cmp r1, #0x28
    bgt .L_021f3cf8
    bge .L_021f3d1c
    cmp r1, #0x27
    beq .L_021f3d14
    b .L_021f3d24
.L_021f3cf8:
    cmp r1, #0x31
    bne .L_021f3d24
    ldr r0, .L_pool_021f3d80
    mov r1, #0x0
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3d04:
    ldr r0, .L_pool_021f3d80
    mov r1, #0x1
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3d0c:
    ldr r0, .L_pool_021f3d80
    mov r1, #0x3
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3d14:
    ldr r0, .L_pool_021f3d80
    mov r1, #0x4
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3d1c:
    ldr r0, .L_pool_021f3d80
    mov r1, #0x5
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3d24:
    ldr r0, .L_pool_021f3d80
    mov r1, #0x2
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3d2c:
    sub r0, r3, #0x4
    cmp r1, r0
    bne .L_021f3dd4
    mov r0, #0x12
    lsl r0, r0, #0x4
    ldrsb r1, [r2, r0]
    cmp r1, #0x23
    bgt .L_021f3d70
    bge .L_021f3dc4
    cmp r1, #0xb
    bgt .L_021f3d6a
    cmp r1, #0x0
    blt .L_021f3dce
    add r0, r1, r1
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x007a
    .hword 0x007a
    .hword 0x007a
    .hword 0x007a
    .hword 0x007a
    .hword 0x007a
    .hword 0x0048
    .hword 0x0050
    .hword 0x007a
    .hword 0x0058
    .hword 0x0060
    .hword 0x0068
.L_021f3d6a:
    cmp r1, #0x22
    beq .L_021f3dbc
    b .L_021f3dce
.L_021f3d70:
    cmp r1, #0x2a
    bgt .L_021f3d88
    bge .L_021f3da4
    cmp r1, #0x29
    beq .L_021f3d9c
    b .L_021f3dce
.L_pool_021f3d7c:
    .word 0x0221c05c
.L_pool_021f3d80:
    .word 0x00000121
.L_pool_021f3d84:
    .word native_data_0220b344
.L_021f3d88:
    cmp r1, #0x32
    bgt .L_021f3dce
    cmp r1, #0x2c
    blt .L_021f3dce
    beq .L_021f3dac
    cmp r1, #0x2d
    beq .L_021f3db4
    cmp r1, #0x32
    beq .L_021f3dc4
    b .L_021f3dce
.L_021f3d9c:
    ldr r0, .L_pool_021f3de0
    mov r1, #0x6
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3da4:
    ldr r0, .L_pool_021f3de0
    mov r1, #0x7
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3dac:
    ldr r0, .L_pool_021f3de0
    mov r1, #0x9
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3db4:
    ldr r0, .L_pool_021f3de0
    mov r1, #0xa
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3dbc:
    ldr r0, .L_pool_021f3de0
    mov r1, #0xb
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3dc4:
    mov r1, #0x32
    add r0, r1, #0x0
    add r0, #0xef
    strb r1, [r2, r0]
    b .L_021f3dd4
.L_021f3dce:
    ldr r0, .L_pool_021f3de0
    mov r1, #0x8
    strb r1, [r2, r0]
.L_021f3dd4:
    bl native_fn_021f3a78
    mov r0, #0x8
    bl native_fn_021ff6d4
    pop {r4, r5, r6, pc}
.L_pool_021f3de0:
    .word 0x00000121
.size native_ov006_021f3b10, .-native_ov006_021f3b10
