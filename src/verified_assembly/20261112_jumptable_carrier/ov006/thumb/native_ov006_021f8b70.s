/* ov006 row 0x021f8b70: 220 bytes.
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
.extern native_fn_021ff6d4
.extern native_fn_0220490c
.extern native_fn_021f8c94
.extern native_fn_021f8800
.extern native_fn_021fe6d0
.extern native_fn_021f8b3c
.extern native_fn_021f8a18
.global native_ov006_021f8b70
.type native_ov006_021f8b70, @function
native_ov006_021f8b70:
    push {r4, lr}
    ldr r1, .L_pool_021f8c44
    mov r4, #0x1
    ldrb r2, [r1, #0]
    cmp r2, #0x4
    bhi .L_021f8c16
    add r3, r2, r2
    add r3, pc
    ldrh r3, [r3, #0x6]
    lsl r3, r3, #0x10
    asr r3, r3, #0x10
    add pc, r3
    .hword 0x0008
    .hword 0x0046
    .hword 0x0046
    .hword 0x0064
    .hword 0x0074
    cmp r0, #0x1
    bne .L_021f8bbc
    ldrh r0, [r1, #0x2]
    cmp r0, #0x0
    bne .L_021f8ba2
    mov r0, #0x4
    strb r0, [r1, #0]
    b .L_021f8c16
.L_021f8ba2:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021f8c48
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021f8c44
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
    pop {r4, pc}
.L_021f8bbc:
    ldr r0, [r1, #0x4]
    add r0, #0x51
    ldrb r0, [r0, #0]
    cmp r0, #0x1
    bls .L_021f8bcc
    add r0, r2, #0x1
    strb r0, [r1, #0]
    b .L_021f8c16
.L_021f8bcc:
    mov r4, #0x0
    b .L_021f8c16
    cmp r0, #0x1
    bne .L_021f8bda
    sub r0, r2, #0x1
    strb r0, [r1, #0]
    b .L_021f8c16
.L_021f8bda:
    ldr r0, [r1, #0x4]
    add r0, #0x51
    ldrb r3, [r0, #0]
    add r0, r2, #0x1
    cmp r3, r0
    ble .L_021f8bea
    strb r0, [r1, #0]
    b .L_021f8c16
.L_021f8bea:
    mov r4, #0x0
    b .L_021f8c16
    cmp r0, #0x1
    bne .L_021f8bf8
    sub r0, r2, #0x1
    strb r0, [r1, #0]
    b .L_021f8c16
.L_021f8bf8:
    bl native_fn_021f8c94
    pop {r4, pc}
    cmp r0, #0x1
    bne .L_021f8c06
    mov r4, #0x0
    b .L_021f8c16
.L_021f8c06:
    mov r0, #0x0
    strh r0, [r1, #0x2]
    strb r0, [r1, #0]
    bl native_fn_021f8800
    mov r0, #0x0
    bl native_fn_021fe6d0
.L_021f8c16:
    cmp r4, #0x0
    bne .L_021f8c38
    ldr r0, .L_pool_021f8c44
    ldr r0, [r0, #0x4]
    add r0, #0x59
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021f8c42
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021f8c44
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x59
    strb r1, [r0, #0]
    pop {r4, pc}
.L_021f8c38:
    mov r0, #0x8
    bl native_fn_021ff6d4
    bl native_fn_021f8b3c
.L_021f8c42:
    pop {r4, pc}
.L_pool_021f8c44:
    .word 0x0221c0d8
.L_pool_021f8c48:
    .word native_fn_021f8a18+1
.size native_ov006_021f8b70, .-native_ov006_021f8b70
