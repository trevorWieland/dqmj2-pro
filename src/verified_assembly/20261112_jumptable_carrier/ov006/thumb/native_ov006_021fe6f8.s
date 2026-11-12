/* ov006 row 0x021fe6f8: 244 bytes.
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
.extern native_fn_021fe930
.extern native_fn_021ff6d4
.extern native_fn_021ff6ec
.extern native_fn_0220410c
.extern native_fn_021fe8d0
.extern native_fn_021fe8ec
.extern native_fn_021fe7ec
.extern native_fn_021fe98c
.global native_ov006_021fe6f8
.type native_ov006_021fe6f8, @function
native_ov006_021fe6f8:
    push {r3, lr}
    ldr r0, .L_pool_021fe7e8
    mov r2, #0x0
    ldr r1, [r0, #0]
    strb r2, [r1, #0x1d]
    ldr r1, [r0, #0]
    ldrb r0, [r1, #0x1c]
    cmp r0, #0x3
    bhi .L_021fe7e6
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0006
    .hword 0x0076
    .hword 0x007c
    .hword 0x00a6
    ldrb r0, [r1, #0x1e]
    cmp r0, #0x0
    bne .L_021fe7e6
    bl native_fn_021fe930
    cmp r0, #0x4
    bhi .L_021fe7e6
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x00ac
    .hword 0x0008
    .hword 0x003e
    .hword 0x0046
    .hword 0x004e
    ldr r0, .L_pool_021fe7e8
    ldr r0, [r0, #0]
    ldrb r0, [r0, #0x1b]
    cmp r0, #0x0
    beq .L_021fe7e6
    mov r0, #0x16
    bl native_fn_021ff6d4
    mov r0, #0x0
    bl native_fn_021ff6ec
    ldr r0, .L_pool_021fe7e8
    mov r2, #0x1
    ldr r1, [r0, #0]
    strb r2, [r1, #0x1d]
    ldr r0, [r0, #0]
    add r0, #0x14
    bl native_fn_0220410c
    ldr r0, .L_pool_021fe7e8
    ldr r2, [r0, #0]
    ldrb r1, [r2, #0x1a]
    strb r1, [r2, #0x18]
    ldr r0, [r0, #0]
    mov r1, #0x1
    strb r1, [r0, #0x1c]
    pop {r3, pc}
    mov r0, #0x2
    bl native_fn_021fe8d0
    pop {r3, pc}
    mov r0, #0x3
    bl native_fn_021fe8d0
    pop {r3, pc}
    bl native_fn_021fe8ec
    pop {r3, pc}
    bl native_fn_021fe7ec
    pop {r3, pc}
    mov r0, #0x2
    bl native_fn_021fe98c
    cmp r0, #0x2
    beq .L_021fe7ae
    ldr r0, .L_pool_021fe7e8
    mov r2, #0x5
    ldr r1, [r0, #0]
    strb r2, [r1, #0x1d]
    ldr r0, [r0, #0]
    mov r1, #0x0
    strb r1, [r0, #0x1c]
    pop {r3, pc}
.L_021fe7ae:
    bl native_fn_021fe930
    cmp r0, #0x2
    bne .L_021fe7e6
    mov r0, #0x2
    bl native_fn_021fe8d0
    pop {r3, pc}
    mov r0, #0x3
    bl native_fn_021fe98c
    cmp r0, #0x3
    beq .L_021fe7d8
    ldr r0, .L_pool_021fe7e8
    mov r2, #0x7
    ldr r1, [r0, #0]
    strb r2, [r1, #0x1d]
    ldr r0, [r0, #0]
    mov r1, #0x0
    strb r1, [r0, #0x1c]
    pop {r3, pc}
.L_021fe7d8:
    bl native_fn_021fe930
    cmp r0, #0x3
    bne .L_021fe7e6
    mov r0, #0x3
    bl native_fn_021fe8d0
.L_021fe7e6:
    pop {r3, pc}
.L_pool_021fe7e8:
    .word 0x0221c140
.size native_ov006_021fe6f8, .-native_ov006_021fe6f8
