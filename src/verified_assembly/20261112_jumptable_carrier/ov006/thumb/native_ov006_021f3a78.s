/* ov006 row 0x021f3a78: 152 bytes.
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
.extern native_fn_02202dc0
.extern native_fn_02202ff0
.extern native_fn_02202f54
.extern native_fn_02202eb0
.extern native_data_0220b272
.extern native_data_0220b270
.global native_ov006_021f3a78
.type native_ov006_021f3a78, @function
native_ov006_021f3a78:
    push {r4, lr}
    ldr r0, .L_pool_021f3b00
    ldr r1, .L_pool_021f3b04
    ldr r0, [r0, #0]
    ldrsb r1, [r0, r1]
    sub r1, #0x2f
    cmp r1, #0x5
    bhi .L_021f3ab4
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x000a
    .hword 0x000e
    .hword 0x0012
    .hword 0x0016
    .hword 0x001a
    .hword 0x001a
    mov r4, #0x42
    b .L_021f3ab6
    mov r4, #0x41
    b .L_021f3ab6
    mov r4, #0x43
    b .L_021f3ab6
    mov r4, #0x41
    b .L_021f3ab6
    mov r4, #0x45
    b .L_021f3ab6
.L_021f3ab4:
    mov r4, #0x40
.L_021f3ab6:
    mov r1, #0x45
    lsl r1, r1, #0x2
    ldr r0, [r0, r1]
    mov r1, #0x0
    bl native_fn_02202dc0
    add r2, r0, #0x0
    mov r0, #0x0
    add r1, r4, #0x0
    bl native_fn_02202ff0
    ldr r0, .L_pool_021f3b00
    mov r2, #0x2
    ldr r1, [r0, #0]
    mov r0, #0x45
    lsl r0, r0, #0x2
    ldr r0, [r1, r0]
    mov r1, #0x0
    mvn r1, r1
    bl native_fn_02202f54
    ldr r0, .L_pool_021f3b00
    ldr r3, .L_pool_021f3b08
    ldr r2, [r0, #0]
    ldr r0, .L_pool_021f3b04
    ldrsb r1, [r2, r0]
    sub r0, #0xd
    ldr r0, [r2, r0]
    lsl r4, r1, #0x2
    ldr r2, .L_pool_021f3b0c
    mov r1, #0x0
    ldrh r2, [r2, r4]
    ldrh r3, [r3, r4]
    mvn r1, r1
    bl native_fn_02202eb0
    pop {r4, pc}
.L_pool_021f3b00:
    .word 0x0221c05c
.L_pool_021f3b04:
    .word 0x00000121
.L_pool_021f3b08:
    .word native_data_0220b272
.L_pool_021f3b0c:
    .word native_data_0220b270
.size native_ov006_021f3a78, .-native_ov006_021f3a78
