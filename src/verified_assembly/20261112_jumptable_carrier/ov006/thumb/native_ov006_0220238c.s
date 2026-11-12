/* ov006 row 0x0220238c: 308 bytes.
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
.extern native_fn_022010ec
.extern native_fn_02200b58
.extern native_fn_022010f8
.extern native_fn_02200df0
.extern native_fn_02200e30
.extern native_fn_02200ec4
.extern native_fn_02201820
.extern native_fn_02201dbc
.global native_ov006_0220238c
.type native_ov006_0220238c, @function
native_ov006_0220238c:
    push {r3, lr}
    bl native_fn_022010ec
    cmp r0, #0x7
    bls .L_02202398
    b .L_022024b2
.L_02202398:
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x00da
    .hword 0x000e
    .hword 0x0020
    .hword 0x0080
    .hword 0x010c
    .hword 0x00ba
    .hword 0x010c
    .hword 0x00c8
    ldr r0, .L_pool_022024b4
    ldr r1, .L_pool_022024b8
    ldr r2, [r0, #0]
    ldr r0, .L_pool_022024bc
    ldrh r1, [r2, r1]
    add r0, r2, r0
    bl native_fn_02200b58
    pop {r3, pc}
    mov r0, #0x2
    bl native_fn_022010f8
    cmp r0, #0x0
    beq .L_022023de
    ldr r0, .L_pool_022024b4
    mov r2, #0x5
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
.L_022023de:
    mov r0, #0x3
    bl native_fn_022010f8
    cmp r0, #0x0
    bne .L_022023f2
    mov r0, #0x4
    bl native_fn_022010f8
    cmp r0, #0x0
    beq .L_02202400
.L_022023f2:
    ldr r0, .L_pool_022024b4
    mov r2, #0x6
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
.L_02202400:
    ldr r0, .L_pool_022024b4
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    ldrb r0, [r1, r0]
    cmp r0, #0x5
    bne .L_022024b2
    mov r0, #0x2
    bl native_fn_022010f8
    cmp r0, #0x0
    bne .L_022024b2
    ldr r0, .L_pool_022024b4
    mov r2, #0xd
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
    bl native_fn_02200df0
    cmp r0, #0x0
    beq .L_02202434
    bl native_fn_02200e30
    pop {r3, pc}
.L_02202434:
    ldr r0, .L_pool_022024b4
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    ldrb r0, [r1, r0]
    add r0, #0xfa
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    cmp r0, #0x1
    bhi .L_022024b2
    mov r0, #0x3
    bl native_fn_022010f8
    cmp r0, #0x0
    bne .L_022024b2
    ldr r0, .L_pool_022024b4
    mov r2, #0x12
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
    ldr r0, .L_pool_022024b4
    mov r2, #0x7
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
    bl native_fn_02200ec4
    ldr r0, .L_pool_022024b4
    mov r2, #0x1
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
    bl native_fn_02201820
    cmp r0, #0x0
    beq .L_02202498
    cmp r0, #0x1
    beq .L_02202492
    cmp r0, #0x3
    beq .L_022024b2
    b .L_022024a6
.L_02202492:
    bl native_fn_02201dbc
    pop {r3, pc}
.L_02202498:
    ldr r0, .L_pool_022024b4
    mov r2, #0x1f
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, pc}
.L_022024a6:
    ldr r0, .L_pool_022024b4
    mov r2, #0x1f
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
.L_022024b2:
    pop {r3, pc}
.L_pool_022024b4:
    .word 0x0221c16c
.L_pool_022024b8:
    .word 0x0000064a
.L_pool_022024bc:
    .word 0x00000ab4
.size native_ov006_0220238c, .-native_ov006_0220238c
