/* ov006 row 0x022036ac: 116 bytes.
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
.extern native_fn_0203754c
.global native_ov006_022036ac
.type native_ov006_022036ac, @function
native_ov006_022036ac:
    push {r4, r5, r6, lr}
    sub sp, #0x10
    ldr r5, [r0, #0x1c]
    add r6, r3, #0x0
    add r4, sp, #0xc
    mov r3, #0x0
    strb r3, [r4, #0]
    strb r3, [r4, #0x1]
    ldr r4, [r5, #0]
    ldr r4, [r4, #0x8]
    ldrb r4, [r4, #0x7]
    cmp r4, #0x7
    bhi .L_02203700
    add r4, r4, r4
    add r4, pc
    ldrh r4, [r4, #0x6]
    lsl r4, r4, #0x10
    asr r4, r4, #0x10
    add pc, r4
    .hword 0x000e
    .hword 0x0016
    .hword 0x0016
    .hword 0x001e
    .hword 0x001e
    .hword 0x0026
    .hword 0x0026
    .hword 0x000e
    mov r4, #0x1
    add r3, sp, #0xc
    strb r4, [r3, #0]
    b .L_02203700
    mov r4, #0x1
    add r3, sp, #0xc
    strb r4, [r3, #0x1]
    b .L_02203700
    sub r4, r3, #0x1
    add r3, sp, #0xc
    strb r4, [r3, #0]
    b .L_02203700
    sub r4, r3, #0x1
    add r3, sp, #0xc
    strb r4, [r3, #0x1]
.L_02203700:
    ldr r3, [sp, #0x20]
    add r4, sp, #0xc
    str r3, [sp]
    ldr r3, [sp, #0x24]
    add r0, #0x18
    str r3, [sp, #0x4]
    ldrb r5, [r4, #0]
    add r3, sp, #0x8
    strb r5, [r3, #0]
    ldrb r4, [r4, #0x1]
    strb r4, [r3, #0x1]
    add r3, r6, #0x0
    blx native_fn_0203754c
    add sp, #0x10
    pop {r4, r5, r6, pc}
.size native_ov006_022036ac, .-native_ov006_022036ac
