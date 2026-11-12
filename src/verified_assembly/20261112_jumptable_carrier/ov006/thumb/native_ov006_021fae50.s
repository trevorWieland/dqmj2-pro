/* ov006 row 0x021fae50: 104 bytes.
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
.global native_ov006_021fae50
.type native_ov006_021fae50, @function
native_ov006_021fae50:
    push {r4, lr}
    add r4, r0, #0x0
    bl native_fn_021fedc8
    mov r1, #0x1
    cmp r4, #0xa
    bhi .L_021faeb4
    add r2, r4, r4
    add r2, pc
    ldrh r2, [r2, #0x6]
    lsl r2, r2, #0x10
    asr r2, r2, #0x10
    add pc, r2
    .hword 0x0020
    .hword 0x0020
    .hword 0x0048
    .hword 0x0048
    .hword 0x0032
    .hword 0x0032
    .hword 0x0032
    .hword 0x0014
    .hword 0x0048
    .hword 0x003e
    .hword 0x003e
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021faeb4
    mov r1, #0x0
    b .L_021faeb4
    add r0, #0xe7
    ldrb r0, [r0, #0]
    add r0, #0xff
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    cmp r0, #0x1
    bhi .L_021faeb4
    mov r1, #0x0
    b .L_021faeb4
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq .L_021faeb4
    mov r1, #0x0
    b .L_021faeb4
    add r0, #0xf6
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq .L_021faeb4
    mov r1, #0x0
.L_021faeb4:
    add r0, r1, #0x0
    pop {r4, pc}
.size native_ov006_021fae50, .-native_ov006_021fae50
