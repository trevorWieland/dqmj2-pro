/* ov006 row 0x021ede50: 196 bytes.
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
.extern native_fn_02006dfc
.extern native_fn_02007ff4
.extern native_fn_02008008
.extern native_fn_021ee8ec
.extern native_fn_02006eb8
.extern native_fn_021ede28
.global native_ov006_021ede50
.type native_ov006_021ede50, @function
native_ov006_021ede50:
    push {r3, r4, r5, r6, r7, lr}
    add r5, r0, #0x0
    add r6, r1, #0x0
    ldr r0, .L_pool_021edf00
    ldr r1, .L_pool_021edf04
    mov r2, #0x4
    mov r4, #0x1
    blx native_fn_02006dfc
    cmp r5, #0x0
    beq .L_021ede6a
    cmp r6, #0x0
    bne .L_021ede70
.L_021ede6a:
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ede70:
    blx native_fn_02007ff4
    ldr r1, .L_pool_021edf08
    str r5, [r1, #0]
    str r6, [r1, #0xc]
    blx native_fn_02008008
    ldr r1, .L_pool_021edf08
    ldr r0, .L_pool_021edf0c
    ldr r1, [r1, #0]
    blx r1
    add r1, r0, #0x0
    ldr r0, .L_pool_021edf08
    str r1, [r0, #0x8]
    bne .L_021ede92
    sub r0, r4, #0x2
    pop {r3, r4, r5, r6, r7, pc}
.L_021ede92:
    ldr r0, .L_pool_021edf10
    ldr r2, .L_pool_021edf0c
    bl native_fn_021ee8ec
    cmp r0, #0x0
    bne .L_021edea0
    mov r4, #0x0
.L_021edea0:
    cmp r4, #0x0
    beq .L_021edef0
    ldr r5, .L_pool_021edf00
    add r6, sp, #0x0
    mov r7, #0x1
.L_021edeaa:
    add r0, r5, #0x0
    add r1, r6, #0x0
    add r2, r7, #0x0
    blx native_fn_02006eb8
    ldr r0, [sp]
    cmp r0, #0xf
    bhi .L_021edeea
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0024
    .hword 0x0024
    .hword 0x001e
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
.L_021edeea:
    mov r4, #0x0
    cmp r4, #0x0
    bne .L_021edeaa
.L_021edef0:
    ldr r1, .L_pool_021edf08
    ldr r0, [r1, #0x8]
    ldr r1, [r1, #0xc]
    blx r1
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
.L_pool_021edf00:
    .word 0x0221a940
.L_pool_021edf04:
    .word 0x0221a930
.L_pool_021edf08:
    .word 0x0221a920
.L_pool_021edf0c:
    .word 0x00005890
.L_pool_021edf10:
    .word native_fn_021ede28+1
.size native_ov006_021ede50, .-native_ov006_021ede50
