/* ov006 row 0x021ed1c8: 272 bytes.
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
.extern native_fn_021edcb8
.extern native_fn_021ecf8c
.extern native_fn_021ed0e0
.extern native_fn_021ed198
.extern native_data_0220d3d8
.global native_ov006_021ed1c8
.type native_ov006_021ed1c8, @function
native_ov006_021ed1c8:
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    add r6, r2, #0x0
    str r0, [sp]
    add r4, r1, #0x0
    mov r5, #0x0
    str r3, [sp, #0x4]
    cmp r6, #0x0
    bgt .L_021ed1e0
    add sp, #0x14
    sub r0, r5, #0x2
    pop {r4, r5, r6, r7, pc}
.L_021ed1e0:
    ldr r7, .L_pool_021ed2d0
.L_021ed1e2:
    ldr r2, [sp]
    ldrb r0, [r4, #0]
    ldrb r2, [r7, r2]
    add r1, r4, #0x0
    cmp r0, r2
    beq .L_021ed206
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    add r0, r0, #0x4
    sub r6, r6, r0
    add r4, r4, r0
    cmp r6, #0x0
    bgt .L_021ed1e2
    mov r0, #0x3
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ed206:
    ldrh r0, [r1, #0x2]
    add r4, r4, #0x4
    bl native_fn_021edcb8
    add r7, r0, #0x0
    mov r1, #0x35
    ldr r0, [sp]
    lsl r1, r1, #0x4
    mul r1, r0
    ldr r0, [sp, #0x4]
    add r6, r0, r1
    ldr r0, [sp, #0x28]
    str r0, [sp, #0x8]
    ldr r0, [sp]
    add r0, r0, #0x3
    lsl r0, r0, #0x7
    str r0, [sp, #0xc]
    add r0, r6, #0x0
    str r0, [sp, #0x10]
    add r0, #0x8
    str r0, [sp, #0x10]
.L_021ed230:
    ldrb r0, [r4, #0]
    cmp r0, #0xa
    bhi .L_021ed2aa
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0066
    .hword 0x0066
    .hword 0x0066
    .hword 0x0014
    .hword 0x0022
    .hword 0x0034
    .hword 0x0046
    .hword 0x0066
    .hword 0x0066
    .hword 0x0066
    .hword 0x0058
    ldr r1, [sp, #0x10]
    add r0, r4, #0x0
    bl native_fn_021ecf8c
    mov r1, #0x1
    orr r5, r1
    b .L_021ed2ae
    mov r1, #0x4e
    lsl r1, r1, #0x2
    add r0, r4, #0x0
    add r1, r6, r1
    bl native_fn_021ecf8c
    mov r1, #0x2
    orr r5, r1
    b .L_021ed2ae
    mov r1, #0x9a
    lsl r1, r1, #0x2
    add r0, r4, #0x0
    add r1, r6, r1
    bl native_fn_021ed0e0
    mov r1, #0x4
    orr r5, r1
    b .L_021ed2ae
    mov r1, #0xb6
    lsl r1, r1, #0x2
    add r0, r4, #0x0
    add r1, r6, r1
    bl native_fn_021ed0e0
    mov r1, #0x8
    orr r5, r1
    b .L_021ed2ae
    ldr r2, [sp, #0x8]
    ldr r1, [sp, #0xc]
    add r0, r4, #0x0
    add r1, r2, r1
    bl native_fn_021ed198
    b .L_021ed2ae
.L_021ed2aa:
    mov r0, #0x2
    mvn r0, r0
.L_021ed2ae:
    cmp r0, #0x0
    bne .L_021ed2cc
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    add r0, r0, #0x4
    sub r7, r7, r0
    add r4, r4, r0
    cmp r7, #0x0
    bgt .L_021ed230
    ldr r0, .L_pool_021ed2d4
    ldr r1, [r0, #0x30]
    orr r1, r5
    str r1, [r0, #0x30]
    mov r0, #0x0
.L_021ed2cc:
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
.L_pool_021ed2d0:
    .word native_data_0220d3d8
.L_pool_021ed2d4:
    .word 0x02219b4c
.size native_ov006_021ed1c8, .-native_ov006_021ed1c8
