/* ov006 row 0x021edf14: 152 bytes.
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
.extern native_fn_021ee810
.extern native_fn_02006eb8
.extern native_fn_02007ff4
.extern native_fn_02008008
.global native_ov006_021edf14
.type native_ov006_021edf14, @function
native_ov006_021edf14:
    push {r3, r4, r5, r6, r7, lr}
    ldr r0, .L_pool_021edfa4
    mov r4, #0x1
    ldr r0, [r0, #0xc]
    sub r5, r4, #0x2
    cmp r0, #0x0
    bne .L_021edf26
    add r0, r5, #0x0
    pop {r3, r4, r5, r6, r7, pc}
.L_021edf26:
    bl native_fn_021ee810
    cmp r0, #0x0
    bne .L_021edf32
    sub r0, r4, #0x2
    pop {r3, r4, r5, r6, r7, pc}
.L_021edf32:
    ldr r7, .L_pool_021edfa8
    ldr r6, .L_pool_021edfa4
.L_021edf36:
    add r0, r7, #0x0
    add r1, sp, #0x0
    mov r2, #0x1
    blx native_fn_02006eb8
    ldr r0, [sp]
    cmp r0, #0x14
    bhi .L_021edf88
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0036
    .hword 0x0036
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0034
    .hword 0x0028
    ldr r0, [r6, #0x8]
    mov r4, #0x0
    ldr r1, [r6, #0xc]
    add r5, r4, #0x0
    blx r1
    b .L_021edf8a
.L_021edf88:
    mov r4, #0x0
.L_021edf8a:
    cmp r4, #0x0
    bne .L_021edf36
    blx native_fn_02007ff4
    ldr r1, .L_pool_021edfa4
    mov r2, #0x0
    str r2, [r1, #0]
    str r2, [r1, #0xc]
    blx native_fn_02008008
    add r0, r5, #0x0
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
.L_pool_021edfa4:
    .word 0x0221a920
.L_pool_021edfa8:
    .word 0x0221a940
.size native_ov006_021edf14, .-native_ov006_021edf14
