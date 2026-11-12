/* ov006 row 0x021f0170: 996 bytes.
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
.extern native_fn_02006b7c
.extern native_fn_021ef564
.extern native_fn_021f2170
.extern native_fn_021ef210
.extern native_fn_020902d0
.extern native_fn_020902f0
.extern native_fn_021f1ef0
.extern native_fn_02090464
.extern native_fn_021efc64
.extern native_fn_02090378
.extern native_fn_021efa98
.extern native_fn_021efbbc
.extern native_fn_021ef84c
.extern native_fn_021efb6c
.extern native_fn_021ef918
.extern native_fn_021f1ec8
.extern native_fn_021efa70
.extern native_fn_021ef94c
.extern native_fn_021efd60
.extern native_fn_021ef014
.extern native_data_0220d480
.extern native_fn_021effe8
.global native_ov006_021f0170
.type native_ov006_021f0170, @function
native_ov006_021f0170:
    push {r4, r5, r6, r7, lr}
    sub sp, #0x2c
    mov r4, #0x0
    sub r0, r4, #0x5
    str r0, [sp, #0x8]
    ldr r0, .L_pool_021f04b8
    mov r1, #0x1
    str r4, [sp, #0xc]
    str r4, [sp, #0x4]
    add r6, r4, #0x0
    str r1, [r0, #0x1c]
    b .L_021f0522
.L_021f0188:
    mov r0, #0x7d
    lsl r0, r0, #0x2
    blx native_fn_02006b7c
    ldr r0, .L_pool_021f04b8
    ldr r0, [r0, #0x1c]
    cmp r0, #0xa
    bls .L_021f019a
    b .L_021f0522
.L_021f019a:
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x037a
    .hword 0x0014
    .hword 0x0034
    .hword 0x004a
    .hword 0x0098
    .hword 0x0100
    .hword 0x0124
    .hword 0x01ce
    .hword 0x022a
    .hword 0x02b2
    .hword 0x0350
    bl native_fn_021ef564
    str r0, [sp, #0x8]
    cmp r0, #0x1
    beq .L_021f01ca
    mov r6, #0x1
    b .L_021f0522
.L_021f01ca:
    ldr r0, .L_pool_021f04b8
    mov r1, #0x3
    str r1, [r0, #0x38]
    bl native_fn_021f2170
    ldr r0, .L_pool_021f04b8
    mov r1, #0x2
    str r1, [r0, #0x1c]
    b .L_021f0522
    bl native_fn_021ef210
    str r0, [sp, #0x8]
    cmp r0, #0x1
    beq .L_021f01ea
    mov r6, #0x1
    b .L_021f0522
.L_021f01ea:
    ldr r0, .L_pool_021f04b8
    mov r1, #0x3
    str r1, [r0, #0x1c]
    b .L_021f0522
    mov r0, #0x2
    add r1, r0, #0x0
    mov r2, #0x0
    bl native_fn_020902d0
    add r4, r0, #0x0
    bpl .L_021f020a
    mov r0, #0x1
    mvn r0, r0
    str r0, [sp, #0x8]
    mov r6, #0x1
    b .L_021f0522
.L_021f020a:
    add r5, sp, #0x24
    mov r1, #0x0
    str r1, [r5, #0]
    str r1, [r5, #0x4]
    mov r3, #0x8
    add r2, sp, #0x10
    strb r3, [r2, #0x14]
    mov r3, #0x2
    strb r3, [r2, #0x15]
    ldr r3, .L_pool_021f04bc
    strh r3, [r2, #0x16]
    str r1, [sp, #0x28]
    add r1, r5, #0x0
    bl native_fn_020902f0
    str r0, [sp, #0x8]
    cmp r0, #0x0
    bge .L_021f0238
    mov r0, #0x1
    mvn r0, r0
    str r0, [sp, #0x8]
    mov r6, #0x1
    b .L_021f0522
.L_021f0238:
    ldr r0, .L_pool_021f04b8
    mov r1, #0x4
    str r1, [r0, #0x1c]
    b .L_021f0522
    bl native_fn_021f1ef0
    ldr r1, .L_pool_021f04c0
    ldr r1, [r1, #0xc]
    cmp r0, r1
    blo .L_021f025c
    add r0, r4, #0x0
    bl native_fn_02090464
    mov r0, #0x2
    mvn r0, r0
    str r0, [sp, #0x8]
    mov r6, #0x1
    b .L_021f0522
.L_021f025c:
    mov r1, #0x8
    add r0, sp, #0x10
    strb r1, [r0, #0xc]
    ldr r0, .L_pool_021f04c4
    add r1, sp, #0x1c
    bl native_fn_021efc64
    add r0, sp, #0x1c
    mov r2, #0x2
    str r0, [sp]
    ldr r1, .L_pool_021f04c8
    add r0, r4, #0x0
    lsl r2, r2, #0xa
    mov r3, #0x4
    bl native_fn_02090378
    cmp r0, #0x0
    ble .L_021f035a
    ldr r0, .L_pool_021f04c8
    ldr r1, .L_pool_021f04cc
    bl native_fn_021efa98
    cmp r0, #0x0
    beq .L_021f035a
    bl native_fn_021f1ef0
    ldr r1, .L_pool_021f04d0
    add r1, r0, r1
    ldr r0, .L_pool_021f04c0
    str r1, [r0, #0xc]
    ldr r0, .L_pool_021f04b8
    mov r1, #0x5
    str r1, [r0, #0x1c]
    mov r1, #0x4
    str r1, [r0, #0x38]
    bl native_fn_021f2170
    b .L_021f0522
    ldr r0, .L_pool_021f04c8
    bl native_fn_021efbbc
    add r3, r0, #0x0
    ldr r0, .L_pool_021f04b8
    ldr r2, .L_pool_021f04c8
    str r3, [r0, #0x14]
    add r0, r4, #0x0
    add r1, sp, #0x1c
    bl native_fn_021ef84c
    bl native_fn_021f1ef0
    str r0, [sp, #0xc]
    ldr r0, .L_pool_021f04b8
    mov r1, #0x6
    str r1, [r0, #0x1c]
    b .L_021f0522
    bl native_fn_021f1ef0
    ldr r1, .L_pool_021f04c0
    ldr r1, [r1, #0xc]
    cmp r0, r1
    blo .L_021f02e8
    add r0, r4, #0x0
    bl native_fn_02090464
    mov r0, #0x3
    mvn r0, r0
    str r0, [sp, #0x8]
    mov r6, #0x1
    b .L_021f0522
.L_021f02e8:
    add r0, sp, #0x1c
    mov r2, #0x2
    str r0, [sp]
    ldr r1, .L_pool_021f04c8
    add r0, r4, #0x0
    lsl r2, r2, #0xa
    mov r3, #0x4
    bl native_fn_02090378
    cmp r0, #0x0
    ble .L_021f035c
    ldr r0, .L_pool_021f04c8
    ldr r2, .L_pool_021f04d4
    ldr r3, .L_pool_021f04c4
    mov r1, #0x3
    bl native_fn_021efb6c
    cmp r0, #0x0
    beq .L_021f035c
    ldr r0, .L_pool_021f04d4
    add r1, sp, #0x18
    add r2, sp, #0x14
    bl native_fn_021ef918
    add r5, r0, #0x0
    ldr r1, [sp, #0x18]
    ldr r0, .L_pool_021f04d8
    cmp r1, r0
    bne .L_021f035a
    bl native_fn_021f1ef0
    ldr r2, .L_pool_021f04dc
    str r0, [sp, #0x10]
    mov r1, #0x8
.L_021f032c:
    ldrb r0, [r5, #0]
    add r5, r5, #0x1
    strb r0, [r2, #0]
    add r2, r2, #0x1
    sub r1, r1, #0x1
    bne .L_021f032c
    ldr r0, .L_pool_021f04e0
    add r1, sp, #0x10
    mov r2, #0x4
    bl native_fn_021f1ec8
    mov r0, #0x0
    str r0, [sp, #0x4]
    ldr r0, .L_pool_021f04b8
    mov r1, #0x7
    str r1, [r0, #0x1c]
    mov r1, #0x5
    str r1, [r0, #0x38]
    ldr r0, .L_pool_021f04c0
    sub r1, r1, #0x6
    str r1, [r0, #0xc]
    bl native_fn_021f2170
.L_021f035a:
    b .L_021f0522
.L_021f035c:
    bl native_fn_021f1ef0
    mov r2, #0xfa
    ldr r1, [sp, #0xc]
    lsl r2, r2, #0x2
    add r1, r1, r2
    cmp r0, r1
    bhs .L_021f036e
    b .L_021f0522
.L_021f036e:
    ldr r0, .L_pool_021f04b8
    mov r1, #0x5
    str r1, [r0, #0x1c]
    b .L_021f0522
    ldr r0, .L_pool_021f04d4
    ldr r1, .L_pool_021f04e4
    ldr r2, .L_pool_021f04e0
    mov r3, #0x8
    bl native_fn_021efa70
    ldr r3, .L_pool_021f04b8
    ldr r2, .L_pool_021f04d4
    str r0, [r3, #0x34]
    ldr r0, .L_pool_021f04c4
    mov r1, #0x4
    str r0, [sp]
    ldr r0, .L_pool_021f04c8
    ldr r3, [r3, #0x34]
    bl native_fn_021ef94c
    add r3, r0, #0x0
    ldr r0, .L_pool_021f04b8
    ldr r2, .L_pool_021f04c8
    str r3, [r0, #0x14]
    add r0, r4, #0x0
    add r1, sp, #0x1c
    bl native_fn_021ef84c
    bl native_fn_021f1ef0
    str r0, [sp, #0xc]
    mov r0, #0x0
    mov r5, #0x12
    ldr r7, .L_pool_021f04e8
    add r1, r0, #0x0
    add r2, r0, #0x0
    add r3, r0, #0x0
    mov r12, r5
.L_021f03ba:
    stmia r7!, {r0, r1, r2, r3}
    mov r5, r12
    sub r5, r5, #0x1
    stmia r7!, {r0, r1, r2, r3}
    mov r12, r5
    bne .L_021f03ba
    stmia r7!, {r0, r1, r2, r3}
    str r0, [r7, #0]
    ldr r0, .L_pool_021f04b8
    mov r1, #0x8
    str r1, [r0, #0x1c]
    b .L_021f0522
    add r0, sp, #0x1c
    mov r2, #0x2
    str r0, [sp]
    ldr r1, .L_pool_021f04c8
    add r0, r4, #0x0
    lsl r2, r2, #0xa
    mov r3, #0x4
    bl native_fn_02090378
    cmp r0, #0x0
    ble .L_021f0428
    ldr r0, .L_pool_021f04c8
    ldr r2, .L_pool_021f04d4
    ldr r3, .L_pool_021f04dc
    mov r1, #0x5
    bl native_fn_021efb6c
    ldr r1, .L_pool_021f04b8
    cmp r0, #0x0
    str r0, [r1, #0x34]
    beq .L_021f0428
    ldr r0, .L_pool_021f04d4
    bl native_fn_021efd60
    cmp r0, #0x0
    beq .L_021f0428
    ldr r1, .L_pool_021f04ec
    mov r0, #0x14
    ldrsb r0, [r1, r0]
    cmp r0, #0x0
    beq .L_021f0416
    mov r1, #0x1
    ldr r0, .L_pool_021f04b8
    b .L_021f041a
.L_021f0416:
    ldr r0, .L_pool_021f04b8
    mov r1, #0x0
.L_021f041a:
    strb r1, [r0, #0]
    mov r0, #0x0
    str r0, [sp, #0x4]
    ldr r0, .L_pool_021f04b8
    mov r1, #0x9
    str r1, [r0, #0x1c]
    b .L_021f0522
.L_021f0428:
    bl native_fn_021f1ef0
    mov r2, #0xfa
    ldr r1, [sp, #0xc]
    lsl r2, r2, #0x2
    add r1, r1, r2
    cmp r0, r1
    blo .L_021f0522
    ldr r0, [sp, #0x4]
    add r0, r0, #0x1
    str r0, [sp, #0x4]
    cmp r0, #0xa
    blt .L_021f0452
    add r0, r4, #0x0
    bl native_fn_02090464
    mov r0, #0x1
    mvn r0, r0
    str r0, [sp, #0x8]
    mov r6, #0x1
    b .L_021f0522
.L_021f0452:
    ldr r0, .L_pool_021f04b8
    mov r1, #0x7
    str r1, [r0, #0x1c]
    b .L_021f0522
    ldr r0, .L_pool_021f04d4
    ldr r1, .L_pool_021f04f0
    ldr r2, .L_pool_021f04f4
    mov r3, #0x1
    bl native_fn_021efa70
    ldr r3, .L_pool_021f04b8
    ldr r2, .L_pool_021f04d4
    str r0, [r3, #0x34]
    ldr r0, .L_pool_021f04dc
    mov r1, #0x6
    str r0, [sp]
    ldr r0, .L_pool_021f04c8
    ldr r3, [r3, #0x34]
    bl native_fn_021ef94c
    ldr r1, .L_pool_021f04b8
    str r0, [r1, #0x14]
    bl native_fn_021ef014
    cmp r0, #0x7
    beq .L_021f049c
    bl native_fn_021f1ef0
    mov r1, #0xfa
    lsl r1, r1, #0x2
    add r0, r0, r1
    str r0, [sp, #0xc]
    mov r0, #0xa
    ldr r1, .L_pool_021f04b8
    str r0, [sp, #0x4]
    str r0, [r1, #0x1c]
    b .L_021f0522
.L_021f049c:
    ldr r3, .L_pool_021f04b8
    ldr r2, .L_pool_021f04c8
    ldr r3, [r3, #0x14]
    add r0, r4, #0x0
    add r1, sp, #0x1c
    bl native_fn_021ef84c
    bl native_fn_021f1ef0
    str r0, [sp, #0xc]
    ldr r0, .L_pool_021f04b8
    mov r1, #0xa
    str r1, [r0, #0x1c]
    b .L_021f0522
.L_pool_021f04b8:
    .word 0x0221aad0
.L_pool_021f04bc:
    .word 0x000001e6
.L_pool_021f04c0:
    .word native_data_0220d480
.L_pool_021f04c4:
    .word 0x0221af90
.L_pool_021f04c8:
    .word 0x0221b804
.L_pool_021f04cc:
    .word 0x0221ab20
.L_pool_021f04d0:
    .word 0x00007530
.L_pool_021f04d4:
    .word 0x0221b004
.L_pool_021f04d8:
    .word 0x00000101
.L_pool_021f04dc:
    .word 0x0221afa0
.L_pool_021f04e0:
    .word 0x0221afa8
.L_pool_021f04e4:
    .word 0x00000102
.L_pool_021f04e8:
    .word 0x0221ad24
.L_pool_021f04ec:
    .word 0x0221ae10
.L_pool_021f04f0:
    .word 0x00000301
.L_pool_021f04f4:
    .word 0x0221aad0
    bl native_fn_021f1ef0
    mov r2, #0xfa
    ldr r1, [sp, #0xc]
    lsl r2, r2, #0x2
    add r1, r1, r2
    cmp r0, r1
    blo .L_021f0522
    ldr r0, [sp, #0x4]
    add r0, r0, #0x1
    str r0, [sp, #0x4]
    cmp r0, #0xa
    blt .L_021f051c
    mov r6, #0x1
    bl native_fn_021effe8
    str r0, [sp, #0x8]
    b .L_021f0522
.L_021f051c:
    ldr r0, .L_pool_021f0550
    mov r1, #0x9
    str r1, [r0, #0x1c]
.L_021f0522:
    cmp r6, #0x0
    bne .L_021f0530
    ldr r0, .L_pool_021f0550
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    bne .L_021f0530
    b .L_021f0188
.L_021f0530:
    cmp r4, #0x0
    beq .L_021f053a
    add r0, r4, #0x0
    bl native_fn_02090464
.L_021f053a:
    ldr r0, .L_pool_021f0550
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    beq .L_021f0548
    mov r0, #0x7
    mvn r0, r0
    str r0, [sp, #0x8]
.L_021f0548:
    ldr r0, [sp, #0x8]
    add sp, #0x2c
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
.L_pool_021f0550:
    .word 0x0221aad0
.size native_ov006_021f0170, .-native_ov006_021f0170
