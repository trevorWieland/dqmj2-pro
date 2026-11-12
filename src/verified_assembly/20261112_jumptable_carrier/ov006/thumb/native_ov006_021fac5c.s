/* ov006 row 0x021fac5c: 266 bytes.
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
.extern native_fn_021fedc8
.extern native_fn_021faf60
.extern native_fn_02008d78
.extern native_fn_0201b208
.extern native_fn_021fb028
.global native_ov006_021fac5c
.type native_ov006_021fac5c, @function
native_ov006_021fac5c:
    push {r3, r4, r5, r6, lr}
    sub sp, #0x24
    add r6, r0, #0x0
    add r4, r1, #0x0
    bl native_fn_021fedc8
    cmp r6, #0x8
    bhi .L_021fad62
    add r1, r6, r6
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0010
    .hword 0x001c
    .hword 0x00e8
    .hword 0x007e
    .hword 0x0094
    .hword 0x00aa
    .hword 0x00e8
    .hword 0x00c0
    .hword 0x00d6
    add r0, #0x40
    add r1, r4, #0x0
    bl native_fn_021faf60
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    add r1, r0, #0x0
    add r1, #0xe6
    ldrb r1, [r1, #0]
    lsl r1, r1, #0x1e
    lsr r1, r1, #0x1e
    cmp r1, #0x3
    bhi .L_021facc6
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0006
    .hword 0x000a
    .hword 0x000e
    .hword 0x0012
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    mov r5, #0xa
    b .L_021facc6
    mov r5, #0x1a
    b .L_021facc6
    mov r5, #0x20
.L_021facc6:
    add r0, #0xe6
    ldrb r0, [r0, #0]
    lsl r0, r0, #0x18
    lsr r0, r0, #0x1a
    cmp r0, #0x1
    bne .L_021facd8
    lsr r0, r5, #0x1f
    add r0, r5, r0
    asr r5, r0, #0x1
.L_021facd8:
    add r0, sp, #0x0
    mov r1, #0x0
    mov r2, #0x21
    blx native_fn_02008d78
    add r0, sp, #0x0
    mov r1, #0x2a
    add r2, r5, #0x0
    blx native_fn_0201b208
    add r0, sp, #0x0
    add r1, r4, #0x0
    bl native_fn_021faf60
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    add r1, r0, #0x0
    add r1, #0xf5
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    bne .L_021fad62
    add r0, #0xc0
    add r1, r4, #0x0
    bl native_fn_021fb028
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    add r1, r0, #0x0
    add r1, #0xf5
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    bne .L_021fad62
    add r0, #0xf0
    add r1, r4, #0x0
    bl native_fn_021fb028
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    add r1, r0, #0x0
    add r1, #0xf5
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    bne .L_021fad62
    add r0, #0xc4
    add r1, r4, #0x0
    bl native_fn_021fb028
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    add r1, r0, #0x0
    add r1, #0xf6
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    bne .L_021fad62
    add r0, #0xc8
    add r1, r4, #0x0
    bl native_fn_021fb028
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
    add r1, r0, #0x0
    add r1, #0xf6
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    bne .L_021fad62
    add r0, #0xcc
    add r1, r4, #0x0
    bl native_fn_021fb028
.L_021fad62:
    add sp, #0x24
    pop {r3, r4, r5, r6, pc}
.size native_ov006_021fac5c, .-native_ov006_021fac5c
