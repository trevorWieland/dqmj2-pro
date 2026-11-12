/* ov006 row 0x021eff34: 180 bytes.
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
.global native_ov006_021eff34
.type native_ov006_021eff34, @function
native_ov006_021eff34:
    push {r4, r5, r6, r7}
    add r4, r2, #0x0
    mov r2, #0x0
    add r5, r1, #0x0
    add r3, r2, #0x0
    cmp r4, #0x0
    ble .L_021effe2
    mov r7, #0x1f
.L_021eff44:
    ldrsb r1, [r5, r3]
    cmp r1, #0x63
    bgt .L_021eff9a
    bge .L_021effb2
    cmp r1, #0x61
    bgt .L_021eff94
    bge .L_021effb2
    add r6, r1, #0x0
    sub r6, #0x30
    cmp r6, #0x16
    bhi .L_021effbe
    add r6, r6, r6
    add r6, pc
    ldrh r6, [r6, #0x6]
    lsl r6, r6, #0x10
    asr r6, r6, #0x10
    add pc, r6
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0044
    .hword 0x0056
    .hword 0x0056
    .hword 0x0056
    .hword 0x0056
    .hword 0x0056
    .hword 0x0056
    .hword 0x0056
    .hword 0x0050
    .hword 0x0050
    .hword 0x0050
    .hword 0x0050
    .hword 0x0050
    .hword 0x0050
.L_021eff94:
    cmp r1, #0x62
    beq .L_021effb2
    b .L_021effbe
.L_021eff9a:
    cmp r1, #0x65
    bgt .L_021effa6
    bge .L_021effb2
    cmp r1, #0x64
    beq .L_021effb2
    b .L_021effbe
.L_021effa6:
    cmp r1, #0x66
    beq .L_021effb2
    b .L_021effbe
    sub r1, #0x30
    add r2, r2, r1
    b .L_021effc4
.L_021effb2:
    sub r1, #0x57
    add r2, r2, r1
    b .L_021effc4
    sub r1, #0x37
    add r2, r2, r1
    b .L_021effc4
.L_021effbe:
    mov r0, #0x0
    pop {r4, r5, r6, r7}
    bx lr
.L_021effc4:
    lsr r6, r3, #0x1f
    lsl r1, r3, #0x1f
    sub r1, r1, r6
    ror r1, r7
    add r1, r6, r1
    bne .L_021effd4
    lsl r2, r2, #0x4
    b .L_021effdc
.L_021effd4:
    add r6, r3, r6
    asr r1, r6, #0x1
    strb r2, [r0, r1]
    mov r2, #0x0
.L_021effdc:
    add r3, r3, #0x1
    cmp r3, r4
    blt .L_021eff44
.L_021effe2:
    mov r0, #0x1
    pop {r4, r5, r6, r7}
    bx lr
.size native_ov006_021eff34, .-native_ov006_021eff34
