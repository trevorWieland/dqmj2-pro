/* ov006 row 0x021fe9b8: 124 bytes.
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
.extern native_data_0220b99c
.global native_ov006_021fe9b8
.type native_ov006_021fe9b8, @function
native_ov006_021fe9b8:
    ldr r2, .L_pool_021fea2c
    ldr r3, [r2, #0]
    ldrh r3, [r3, #0x10]
    strh r3, [r1, #0]
    add r3, #0xc
    strh r3, [r1, #0x4]
    cmp r0, #0x4
    bhi .L_021fea28
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0052
    .hword 0x0008
    .hword 0x0022
    .hword 0x0032
    .hword 0x0044
    ldr r0, [r2, #0]
    ldrh r3, [r0, #0x12]
    ldrb r0, [r0, #0x1a]
    add r0, r3, r0
    strh r0, [r1, #0x2]
    ldr r0, [r2, #0]
    ldrh r3, [r1, #0x2]
    ldrb r2, [r0, #0x1b]
    ldr r0, .L_pool_021fea30
    ldrb r0, [r0, r2]
    add r0, r3, r0
    strh r0, [r1, #0x6]
    bx lr
    ldr r0, [r2, #0]
    ldrh r0, [r0, #0x12]
    sub r0, #0xd
    strh r0, [r1, #0x2]
    ldr r0, [r2, #0]
    ldrh r0, [r0, #0x12]
    strh r0, [r1, #0x6]
    bx lr
    ldr r0, [r2, #0]
    ldrh r2, [r0, #0x12]
    ldrb r0, [r0, #0x19]
    add r0, r2, r0
    strh r0, [r1, #0x2]
    ldrh r0, [r1, #0x2]
    add r0, #0xd
    strh r0, [r1, #0x6]
    bx lr
    ldr r0, [r2, #0]
    ldrh r3, [r0, #0x12]
    strh r3, [r1, #0x2]
    ldr r0, [r2, #0]
    ldrb r0, [r0, #0x19]
    add r0, r3, r0
    strh r0, [r1, #0x6]
.L_021fea28:
    bx lr
    mov r8, r8
.L_pool_021fea2c:
    .word 0x0221c140
.L_pool_021fea30:
    .word native_data_0220b99c
.size native_ov006_021fe9b8, .-native_ov006_021fe9b8
