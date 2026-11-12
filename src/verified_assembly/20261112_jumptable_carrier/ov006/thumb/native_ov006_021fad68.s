/* ov006 row 0x021fad68: 232 bytes.
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
.extern native_fn_021fae50
.extern native_fn_021faeb8
.global native_ov006_021fad68
.type native_ov006_021fad68, @function
native_ov006_021fad68:
    push {r4, r5, r6, lr}
    add r4, r0, #0x0
    add r6, r1, #0x0
    bl native_fn_021fedc8
    cmp r4, #0x8
    bhi .L_021fae3a
    add r1, r4, r4
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0010
    .hword 0x0010
    .hword 0x0022
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0066
    .hword 0x00a4
    .hword 0x00a4
    mov r4, #0x0
    add r0, r4, #0x0
    add r5, r4, #0x0
    bl native_fn_021fae50
    cmp r0, #0x0
    bne .L_021fae3e
    mov r5, #0x2
    b .L_021fae3e
    add r0, #0xf5
    ldrb r0, [r0, #0]
    mov r1, #0x0
    add r5, r1, #0x0
    cmp r0, #0x0
    beq .L_021fadb8
    mov r4, #0x1
    mov r0, #0x4
    b .L_021fadbc
.L_021fadb8:
    mov r4, #0x2
    mov r0, #0x3
.L_021fadbc:
    ldr r2, .L_pool_021fae4c
    ldr r3, [r2, #0x8]
    ldrb r2, [r3, #0x4]
    cmp r2, #0x0
    beq .L_021fadc8
    mov r5, #0x1
.L_021fadc8:
    ldrb r2, [r3, #0x5]
    cmp r2, #0x0
    beq .L_021fadd0
    mov r1, #0x1
.L_021fadd0:
    add r2, r6, #0x0
    bl native_fn_021faeb8
    b .L_021fae3e
    add r0, #0xf5
    ldrb r0, [r0, #0]
    mov r4, #0x0
    cmp r0, #0x0
    beq .L_021fade6
    mov r5, #0x2
    b .L_021fae3e
.L_021fade6:
    add r5, r4, #0x0
    b .L_021fae3e
    add r2, r0, #0x0
    add r2, #0xf6
    ldrb r2, [r2, #0]
    mov r1, #0x0
    add r5, r1, #0x0
    cmp r2, #0x0
    beq .L_021fadfe
    mov r4, #0x1
    mov r0, #0x4
    b .L_021fae0c
.L_021fadfe:
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021fae08
    mov r5, #0x2
.L_021fae08:
    mov r4, #0x2
    mov r0, #0x3
.L_021fae0c:
    ldr r2, .L_pool_021fae4c
    ldr r3, [r2, #0x8]
    ldrb r2, [r3, #0x6]
    cmp r2, #0x0
    beq .L_021fae18
    mov r5, #0x1
.L_021fae18:
    ldrb r2, [r3, #0x7]
    cmp r2, #0x0
    beq .L_021fae20
    mov r1, #0x1
.L_021fae20:
    add r2, r6, #0x0
    bl native_fn_021faeb8
    b .L_021fae3e
    add r0, #0xf6
    ldrb r0, [r0, #0]
    mov r4, #0x0
    cmp r0, #0x0
    beq .L_021fae36
    mov r5, #0x2
    b .L_021fae3e
.L_021fae36:
    add r5, r4, #0x0
    b .L_021fae3e
.L_021fae3a:
    mov r4, #0x0
    mov r5, #0x2
.L_021fae3e:
    add r0, r4, #0x0
    add r1, r5, #0x0
    add r2, r6, #0x0
    bl native_fn_021faeb8
    pop {r4, r5, r6, pc}
    mov r8, r8
.L_pool_021fae4c:
    .word 0x0221c0ec
.size native_ov006_021fad68, .-native_ov006_021fad68
