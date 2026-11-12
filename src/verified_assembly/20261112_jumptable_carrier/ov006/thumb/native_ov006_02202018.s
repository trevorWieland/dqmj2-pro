/* ov006 row 0x02202018: 660 bytes.
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
.extern native_fn_02201fbc
.extern native_fn_022022f0
.extern native_fn_0220236c
.extern native_fn_0220238c
.extern native_fn_022024c0
.extern native_fn_022024e4
.extern native_fn_02202644
.extern native_fn_02202658
.extern native_fn_02018604
.extern native_fn_02201820
.extern native_fn_02201dbc
.extern native_fn_02201d08
.extern native_fn_02026350
.global native_ov006_02202018
.type native_ov006_02202018, @function
native_ov006_02202018:
    push {r4, lr}
    ldr r1, .L_pool_022022a4
    mov r0, #0xa9
    ldr r2, [r1, #0]
    lsl r0, r0, #0x4
    ldrb r3, [r2, r0]
    cmp r3, #0x22
    bls .L_0220202a
    b .L_022022a0
.L_0220202a:
    add r3, r3, r3
    add r3, pc
    ldrh r3, [r3, #0x6]
    lsl r3, r3, #0x10
    asr r3, r3, #0x10
    add pc, r3
    .hword 0x0268
    .hword 0x0044
    .hword 0x006e
    .hword 0x0074
    .hword 0x0086
    .hword 0x0098
    .hword 0x0098
    .hword 0x009e
    .hword 0x00a4
    .hword 0x00a4
    .hword 0x00a4
    .hword 0x00aa
    .hword 0x0268
    .hword 0x0268
    .hword 0x0268
    .hword 0x0268
    .hword 0x00b0
    .hword 0x00c0
    .hword 0x00dc
    .hword 0x00f4
    .hword 0x0268
    .hword 0x0124
    .hword 0x013c
    .hword 0x0268
    .hword 0x016e
    .hword 0x0186
    .hword 0x0268
    .hword 0x01b6
    .hword 0x01ce
    .hword 0x0268
    .hword 0x0264
    .hword 0x0268
    .hword 0x021c
    .hword 0x0234
    .hword 0x0268
    add r3, r0, #0x0
    add r3, #0x1c
    ldrb r3, [r2, r3]
    cmp r3, #0x1
    bne .L_02202092
    mov r1, #0x0
    add r0, #0x1c
    strb r1, [r2, r0]
    bl native_fn_02201fbc
    pop {r4, pc}
.L_02202092:
    cmp r3, #0x2
    bne .L_02202192
    add r3, r0, #0x0
    mov r4, #0x0
    add r3, #0x1c
    strb r4, [r2, r3]
    ldr r1, [r1, #0]
    mov r2, #0x22
    strb r2, [r1, r0]
    pop {r4, pc}
    bl native_fn_022022f0
    pop {r4, pc}
    bl native_fn_0220236c
    ldr r0, .L_pool_022022a4
    mov r2, #0x4
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0x8
    ldr r1, [r2, r1]
    add r0, #0x8
    add r1, r1, #0x1
    str r1, [r2, r0]
    bl native_fn_0220238c
    pop {r4, pc}
    bl native_fn_0220238c
    pop {r4, pc}
    bl native_fn_022024c0
    pop {r4, pc}
    bl native_fn_022024e4
    pop {r4, pc}
    bl native_fn_02202644
    pop {r4, pc}
    add r3, r0, #0x0
    mov r4, #0x0
    add r3, #0xc
    str r4, [r2, r3]
    ldr r1, [r1, #0]
    mov r2, #0x11
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0xc
    ldr r3, [r2, r1]
    add r1, r0, #0x0
    add r1, #0xc
    ldr r1, [r2, r1]
    add r0, #0xc
    add r1, r1, #0x1
    str r1, [r2, r0]
    cmp r3, #0x1e
    bls .L_02202192
    bl native_fn_02202658
    pop {r4, pc}
    blx native_fn_02018604
    ldr r1, .L_pool_022022a4
    ldr r0, .L_pool_022022a8
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x16
    sub r0, #0xc
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0xc
    ldr r3, [r2, r1]
    add r1, r0, #0x0
    add r1, #0xc
    ldr r1, [r2, r1]
    add r0, #0xc
    add r1, r1, #0x1
    str r1, [r2, r0]
    cmp r3, #0x1e
    bls .L_02202192
    bl native_fn_02201820
    cmp r0, #0x1
    bne .L_02202192
    bl native_fn_02201dbc
    ldr r0, .L_pool_022022a4
    mov r2, #0x14
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r4, pc}
    bl native_fn_02201d08
    ldr r1, .L_pool_022022a4
    ldr r0, .L_pool_022022a8
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x16
    sub r0, #0xc
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0xc
    ldr r3, [r2, r1]
    add r1, r0, #0x0
    add r1, #0xc
    ldr r1, [r2, r1]
    add r0, #0xc
    add r1, r1, #0x1
    str r1, [r2, r0]
    cmp r3, #0x1e
    bls .L_02202192
    bl native_fn_02201820
    cmp r0, #0x1
    beq .L_02202194
.L_02202192:
    b .L_022022a0
.L_02202194:
    bl native_fn_02201dbc
    ldr r0, .L_pool_022022a4
    mov r2, #0x17
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r4, pc}
    bl native_fn_02201d08
    ldr r1, .L_pool_022022a4
    ldr r0, .L_pool_022022a8
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x19
    sub r0, #0xc
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0xc
    ldr r3, [r2, r1]
    add r1, r0, #0x0
    add r1, #0xc
    ldr r1, [r2, r1]
    add r0, #0xc
    add r1, r1, #0x1
    str r1, [r2, r0]
    cmp r3, #0x1e
    bls .L_022022a0
    bl native_fn_02201820
    cmp r0, #0x1
    bne .L_022022a0
    bl native_fn_02201dbc
    ldr r0, .L_pool_022022a4
    mov r2, #0x1a
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r4, pc}
    bl native_fn_02201d08
    ldr r1, .L_pool_022022a4
    ldr r0, .L_pool_022022a8
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x1c
    sub r0, #0xc
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0xc
    ldr r3, [r2, r1]
    add r1, r0, #0x0
    add r1, #0xc
    ldr r1, [r2, r1]
    add r0, #0xc
    add r1, r1, #0x1
    str r1, [r2, r0]
    cmp r3, #0x1e
    bls .L_022022a0
    bl native_fn_02201820
    cmp r0, #0x1
    bne .L_02202236
    bl native_fn_02201dbc
    ldr r0, .L_pool_022022a4
    mov r2, #0x1d
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r4, pc}
.L_02202236:
    ldr r0, .L_pool_022022a4
    ldr r1, [r0, #0]
    ldr r0, .L_pool_022022a8
    ldr r4, [r1, r0]
    mov r1, #0x1e
    add r0, r4, #0x0
    blx native_fn_02026350
    cmp r1, #0x1
    bne .L_022022a0
    cmp r4, #0x37
    bls .L_022022a0
    bl native_fn_02201d08
    pop {r4, pc}
    bl native_fn_02201d08
    ldr r1, .L_pool_022022a4
    ldr r0, .L_pool_022022a8
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x21
    sub r0, #0xc
    strb r2, [r1, r0]
    pop {r4, pc}
    add r1, r0, #0x0
    add r1, #0xc
    ldr r3, [r2, r1]
    add r1, r0, #0x0
    add r1, #0xc
    ldr r1, [r2, r1]
    add r0, #0xc
    add r1, r1, #0x1
    str r1, [r2, r0]
    cmp r3, #0x1e
    bls .L_022022a0
    bl native_fn_02201820
    cmp r0, #0x1
    bne .L_022022a0
    bl native_fn_02201dbc
    ldr r0, .L_pool_022022a4
    mov r2, #0x22
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r4, pc}
    bl native_fn_02201d08
.L_022022a0:
    pop {r4, pc}
    mov r8, r8
.L_pool_022022a4:
    .word 0x0221c16c
.L_pool_022022a8:
    .word 0x00000a9c
.size native_ov006_02202018, .-native_ov006_02202018
