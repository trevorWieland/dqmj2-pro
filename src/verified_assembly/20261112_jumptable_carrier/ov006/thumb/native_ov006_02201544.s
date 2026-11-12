/* ov006 row 0x02201544: 196 bytes.
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
.extern native_fn_022012c0
.extern native_fn_02201270
.extern native_fn_02201608
.extern native_fn_02013460
.extern native_data_0220e730
.extern native_data_0220e710
.global native_ov006_02201544
.type native_ov006_02201544, @function
native_ov006_02201544:
    push {r3, lr}
    ldrh r1, [r0, #0x2]
    cmp r1, #0x0
    beq .L_0220155a
    add r0, r1, #0x0
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    pop {r3, pc}
.L_0220155a:
    ldrh r2, [r0, #0x4]
    add r0, r2, #0x0
    sub r0, #0xa
    cmp r0, #0x3
    bhi .L_022015e4
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0006
    .hword 0x0082
    .hword 0x0072
    .hword 0x0072
    ldr r0, .L_pool_022015f8
    ldr r1, [r0, #0x4]
    ldr r0, [r1, #0x44]
    cmp r0, #0x2
    bne .L_022015ae
    ldr r0, [r1, #0x40]
    cmp r0, #0x4
    bne .L_022015a8
    bl native_fn_02201608
    cmp r0, #0x0
    bne .L_022015f4
    ldr r0, .L_pool_022015f8
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_022015a0
    mov r0, #0x2
    ldr r1, .L_pool_022015fc
    lsl r0, r0, #0x1a
    blx r2
.L_022015a0:
    mov r0, #0x9
    bl native_fn_02201270
    pop {r3, pc}
.L_022015a8:
    cmp r0, #0x6
    bne .L_022015dc
    pop {r3, pc}
.L_022015ae:
    cmp r0, #0x4
    bne .L_022015dc
    mov r0, #0x1
    str r0, [sp]
    ldr r0, .L_pool_02201600
    mov r2, #0x7
    add r0, r1, r0
    mov r1, #0xd
    mov r3, #0x44
    blx native_fn_02013460
    cmp r0, #0x0
    beq .L_022015d4
    bl native_fn_022012c0
    mov r0, #0x9
    bl native_fn_02201270
    pop {r3, pc}
.L_022015d4:
    mov r0, #0x5
    bl native_fn_02201270
    pop {r3, pc}
.L_022015dc:
    mov r0, #0x4
    bl native_fn_02201270
    pop {r3, pc}
.L_022015e4:
    ldr r0, .L_pool_022015f8
    ldr r3, [r0, #0]
    cmp r3, #0x0
    beq .L_022015f4
    mov r0, #0x2
    ldr r1, .L_pool_02201604
    lsl r0, r0, #0x1a
    blx r3
.L_022015f4:
    pop {r3, pc}
    mov r8, r8
.L_pool_022015f8:
    .word 0x0221c164
.L_pool_022015fc:
    .word native_data_0220e730
.L_pool_02201600:
    .word 0x000013e0
.L_pool_02201604:
    .word native_data_0220e710
.size native_ov006_02201544, .-native_ov006_02201544
