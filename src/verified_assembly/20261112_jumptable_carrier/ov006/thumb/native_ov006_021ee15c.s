/* ov006 row 0x021ee15c: 464 bytes.
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
.extern native_fn_02008d78
.extern native_fn_02008e0c
.extern native_fn_0208b154
.extern native_fn_021ee6ac
.extern native_fn_02007c68
.extern native_fn_02007da4
.extern native_fn_02006eb8
.extern native_fn_02007e10
.extern native_fn_021ee668
.extern native_fn_021eddf4
.extern native_fn_021ee868
.extern native_fn_021ede18
.extern native_fn_021ede3c
.global native_ov006_021ee15c
.type native_ov006_021ee15c, @function
native_ov006_021ee15c:
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x40
    mov r4, #0x1
    add r7, r0, #0x0
    sub r0, r4, #0x2
    str r0, [sp, #0xc]
    ldr r0, [r7, #0x24]
    mov r6, #0x0
    str r1, [sp, #0x4]
    cmp r0, #0x0
    bne .L_021ee176
    lsl r5, r4, #0x13
    b .L_021ee17e
.L_021ee176:
    cmp r0, #0x1
    bne .L_021ee17e
    mov r5, #0x3
    lsl r5, r5, #0x12
.L_021ee17e:
    mov r0, #0x3
    lsl r0, r0, #0x10
    orr r5, r0
    ldr r0, .L_pool_021ee310
    mov r1, #0x0
    mov r2, #0x60
    blx native_fn_02008d78
    ldr r0, [r7, #0x28]
    cmp r0, #0x5
    bne .L_021ee19c
    ldr r0, .L_pool_021ee310
    mov r1, #0x1
    strb r1, [r0, #0]
    b .L_021ee1bc
.L_021ee19c:
    cmp r0, #0xd
    bne .L_021ee1a8
    ldr r0, .L_pool_021ee310
    mov r1, #0x2
    strb r1, [r0, #0]
    b .L_021ee1bc
.L_021ee1a8:
    cmp r0, #0x10
    bne .L_021ee1b4
    ldr r0, .L_pool_021ee310
    mov r1, #0x3
    strb r1, [r0, #0]
    b .L_021ee1bc
.L_021ee1b4:
    mov r0, #0x0
    add sp, #0x40
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ee1bc:
    mov r1, #0x14
    ldr r2, .L_pool_021ee310
    mul r1, r6
    add r1, r1, #0x2
    add r0, r7, #0x0
    strb r6, [r2, #0x1]
    add r1, r2, r1
    ldr r2, [r7, #0x28]
    add r0, #0x2c
    blx native_fn_02008e0c
    bl native_fn_0208b154
    ldr r2, [r7, #0]
    ldr r3, .L_pool_021ee314
    mov r0, #0x0
    add r1, r7, #0x4
    bl native_fn_021ee6ac
    cmp r0, #0x0
    bne .L_021ee1e8
    b .L_021ee2f6
.L_021ee1e8:
    mov r0, #0x0
    str r0, [sp, #0x8]
    add r0, sp, #0x14
    blx native_fn_02007c68
    mov r0, #0x12
    str r0, [sp]
    ldr r1, .L_pool_021ee318
    ldr r3, .L_pool_021ee31c
    add r0, sp, #0x14
    mov r2, #0x0
    blx native_fn_02007da4
    b .L_021ee2d8
.L_021ee204:
    ldr r0, .L_pool_021ee320
    add r1, sp, #0x10
    mov r2, #0x1
    blx native_fn_02006eb8
    ldr r0, [sp, #0x10]
    cmp r0, #0x13
    bhi .L_021ee2d6
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x00b6
    .hword 0x002e
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x00b6
    .hword 0x00b4
    .hword 0x0074
    .hword 0x00b4
    .hword 0x008e
    .hword 0x0094
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x00b4
    .hword 0x0026
    .hword 0x002c
    cmp r6, #0x0
    bne .L_021ee2d8
    mov r4, #0x0
    b .L_021ee2d8
    cmp r6, #0x0
    bne .L_021ee2d8
    add r0, sp, #0x14
    blx native_fn_02007e10
    ldr r0, .L_pool_021ee324
    mov r1, #0x1
    bl native_fn_021ee668
    cmp r0, #0x1
    beq .L_021ee26a
    mov r4, #0x0
    b .L_021ee2d8
.L_021ee26a:
    ldr r1, .L_pool_021ee324
    add r0, r7, #0x0
    bl native_fn_021eddf4
    ldr r1, .L_pool_021ee328
    mov r0, #0x0
    ldrh r1, [r1, #0xa]
    b .L_021ee27c
.L_021ee27a:
    add r0, r0, #0x1
.L_021ee27c:
    cmp r0, r1
    blt .L_021ee27a
    ldr r0, .L_pool_021ee324
    ldr r1, .L_pool_021ee310
    add r2, r5, #0x0
    bl native_fn_021ee868
    cmp r0, #0x0
    bne .L_021ee292
    mov r4, #0x0
    b .L_021ee2d8
.L_021ee292:
    mov r6, #0x1
    b .L_021ee2d8
    ldr r1, .L_pool_021ee324
    add r0, r7, #0x0
    bl native_fn_021eddf4
    ldr r0, .L_pool_021ee324
    ldr r1, .L_pool_021ee310
    add r2, r5, #0x0
    bl native_fn_021ee868
    cmp r0, #0x0
    bne .L_021ee2d8
    mov r4, #0x0
    b .L_021ee2d8
    mov r4, #0x0
    str r4, [sp, #0xc]
    b .L_021ee2d8
    ldr r0, [sp, #0x8]
    add r0, r0, #0x1
    str r0, [sp, #0x8]
    cmp r0, #0x3
    bge .L_021ee2d2
    ldr r0, .L_pool_021ee324
    ldr r1, .L_pool_021ee310
    add r2, r5, #0x0
    bl native_fn_021ee868
    cmp r0, #0x0
    bne .L_021ee2d8
    mov r4, #0x0
    b .L_021ee2d8
.L_021ee2d2:
    mov r4, #0x0
    b .L_021ee2d8
.L_021ee2d6:
    mov r4, #0x0
.L_021ee2d8:
    cmp r4, #0x0
    bne .L_021ee204
    add r0, sp, #0x14
    blx native_fn_02007e10
    ldr r5, .L_pool_021ee320
    add r4, sp, #0x10
    mov r6, #0x0
.L_021ee2e8:
    add r0, r5, #0x0
    add r1, r4, #0x0
    add r2, r6, #0x0
    blx native_fn_02006eb8
    cmp r0, #0x1
    beq .L_021ee2e8
.L_021ee2f6:
    ldr r0, [sp, #0xc]
    cmp r0, #0x0
    bne .L_021ee300
    mov r2, #0x1
    b .L_021ee302
.L_021ee300:
    mov r2, #0x0
.L_021ee302:
    ldr r0, [sp, #0x4]
    ldr r1, .L_pool_021ee324
    bl native_fn_021ede18
    ldr r0, [sp, #0xc]
    add sp, #0x40
    pop {r3, r4, r5, r6, r7, pc}
.L_pool_021ee310:
    .word 0x0221aa20
.L_pool_021ee314:
    .word 0x0030bffe
.L_pool_021ee318:
    .word 0x003fec42
.L_pool_021ee31c:
    .word native_fn_021ede3c+1
.L_pool_021ee320:
    .word 0x0221a940
.L_pool_021ee324:
    .word 0x0221a960
.L_pool_021ee328:
    .word 0x0221a960
.size native_ov006_021ee15c, .-native_ov006_021ee15c
