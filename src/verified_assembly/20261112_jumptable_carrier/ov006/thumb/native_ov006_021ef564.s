/* ov006 row 0x021ef564: 660 bytes.
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
.extern native_fn_021f1f0c
.extern native_fn_021f1ef0
.extern native_fn_021eed5c
.extern native_fn_02007c68
.extern native_fn_02007da4
.extern native_fn_02006b7c
.extern native_fn_021ef0a0
.extern native_fn_021eed18
.extern native_fn_02007e10
.extern native_fn_0201b19c
.extern native_fn_021ef398
.extern native_fn_0201d6b8
.extern native_fn_021f1f74
.extern native_fn_021f2170
.extern native_fn_021f1f30
.extern native_data_0220d480
.extern native_fn_021ef108
.global native_ov006_021ef564
.type native_ov006_021ef564, @function
native_ov006_021ef564:
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x70
    mov r0, #0x0
    str r0, [sp, #0x8]
    str r0, [sp, #0x20]
    ldr r0, .L_pool_021ef7dc
    mov r4, #0x0
    ldr r1, [r0, #0x70]
    mov r0, #0x30
    mul r0, r1
    str r0, [sp, #0x10]
    add r0, #0x34
    str r0, [sp, #0x10]
    ldr r1, [sp, #0x10]
    mov r0, #0x1
    mvn r4, r4
    bl native_fn_021f1f0c
    str r0, [sp, #0xc]
    cmp r0, #0x0
    beq .L_021ef59c
    ldr r1, [sp, #0x10]
    mov r0, #0x1
    bl native_fn_021f1f0c
    str r0, [sp, #0x8]
    cmp r0, #0x0
    bne .L_021ef59e
.L_021ef59c:
    b .L_021ef7c2
.L_021ef59e:
    mov r0, #0x0
    str r0, [sp, #0x1c]
    b .L_021ef78a
.L_021ef5a4:
    bl native_fn_021f1ef0
    ldr r1, .L_pool_021ef7e0
    ldr r1, [r1, #0xc]
    cmp r0, r1
    bhs .L_021ef68e
    mov r0, #0x0
    ldr r3, .L_pool_021ef7e4
    add r1, r0, #0x0
    add r2, r0, #0x0
    bl native_fn_021eed5c
    cmp r0, #0x0
    bne .L_021ef5c6
    mov r4, #0x1
    mvn r4, r4
    b .L_021ef7c2
.L_021ef5c6:
    add r0, sp, #0x24
    blx native_fn_02007c68
    mov r0, #0x13
    str r0, [sp]
    ldr r1, .L_pool_021ef7e8
    ldr r3, .L_pool_021ef7ec
    add r0, sp, #0x24
    mov r2, #0x0
    blx native_fn_02007da4
    ldr r7, .L_pool_021ef7dc
    mov r5, #0x1
    mov r4, #0x0
    add r6, sp, #0x24
.L_021ef5e4:
    mov r0, #0xa
    blx native_fn_02006b7c
    bl native_fn_021f1ef0
    ldr r1, .L_pool_021ef7e0
    ldr r1, [r1, #0xc]
    cmp r0, r1
    bhs .L_021ef678
    ldr r0, [r7, #0x10]
    cmp r0, #0x0
    bne .L_021ef678
    bl native_fn_021ef0a0
    cmp r0, #0x0
    beq .L_021ef674
.L_021ef604:
    cmp r0, #0x13
    bhi .L_021ef66a
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0056
    .hword 0x002a
    .hword 0x0054
    .hword 0x0054
    .hword 0x0056
    .hword 0x0054
    .hword 0x0050
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0054
    .hword 0x0056
    .hword 0x0026
    mov r5, #0x0
    b .L_021ef66c
    ldr r0, [r7, #0x5c]
    ldr r1, [r7, #0x70]
    bl native_fn_021eed18
    cmp r0, r4
    ble .L_021ef66c
    add r4, r0, #0x0
    add r0, r6, #0x0
    blx native_fn_02007e10
    mov r0, #0x13
    str r0, [sp]
    ldr r1, .L_pool_021ef7e8
    ldr r3, .L_pool_021ef7ec
    add r0, r6, #0x0
    mov r2, #0x0
    blx native_fn_02007da4
    b .L_021ef66c
    mov r5, #0x0
    b .L_021ef66c
.L_021ef66a:
    mov r5, #0x0
.L_021ef66c:
    bl native_fn_021ef0a0
    cmp r0, #0x0
    bne .L_021ef604
.L_021ef674:
    cmp r5, #0x0
    bne .L_021ef5e4
.L_021ef678:
    add r0, sp, #0x24
    blx native_fn_02007e10
.L_021ef67e:
    bl native_fn_021ef0a0
    cmp r0, #0x0
    bne .L_021ef67e
    ldr r1, .L_pool_021ef7dc
    ldr r0, [r1, #0x10]
    cmp r0, #0x0
    beq .L_021ef690
.L_021ef68e:
    b .L_021ef79a
.L_021ef690:
    mov r0, #0x0
    str r0, [sp, #0x14]
    ldr r0, [r1, #0x70]
    cmp r4, r0
    blt .L_021ef6a0
    ldr r0, [sp, #0x14]
    sub r4, r0, #0x6
    b .L_021ef7c2
.L_021ef6a0:
    ldr r0, [sp, #0x14]
    ldr r5, [r1, #0x5c]
    str r0, [sp, #0x18]
    cmp r4, #0x0
    ble .L_021ef716
    ble .L_021ef716
    ldr r0, [sp, #0xc]
    ldr r7, [sp, #0xc]
    str r0, [sp, #0x4]
    add r0, #0x8
    add r6, r7, #0x0
    str r0, [sp, #0x4]
    add r6, #0x2c
.L_021ef6ba:
    add r1, r5, #0x0
    ldr r0, [sp, #0x4]
    add r1, #0xc
    mov r2, #0x20
    blx native_fn_0201b19c
    ldrh r0, [r5, #0xa]
    str r0, [r7, #0x4]
    ldrh r0, [r5, #0xa]
    add r1, r7, r0
    mov r0, #0x0
    strb r0, [r1, #0x8]
    ldrh r1, [r5, #0x2c]
    mov r0, #0x10
    tst r0, r1
    beq .L_021ef6de
    mov r0, #0x1
    b .L_021ef6e0
.L_021ef6de:
    mov r0, #0x0
.L_021ef6e0:
    strh r0, [r7, #0x32]
    ldrb r0, [r5, #0x4]
    add r7, #0x30
    strb r0, [r6, #0]
    ldrb r0, [r5, #0x5]
    strb r0, [r6, #0x1]
    ldrb r0, [r5, #0x6]
    strb r0, [r6, #0x2]
    ldrb r0, [r5, #0x7]
    strb r0, [r6, #0x3]
    ldrb r0, [r5, #0x8]
    strb r0, [r6, #0x4]
    ldrb r0, [r5, #0x9]
    add r5, #0xc0
    strb r0, [r6, #0x5]
    ldr r0, [sp, #0x4]
    add r6, #0x30
    add r0, #0x30
    str r0, [sp, #0x4]
    ldr r0, [sp, #0x14]
    add r0, r0, #0x1
    str r0, [sp, #0x14]
    ldr r0, [sp, #0x18]
    add r0, r0, #0x1
    str r0, [sp, #0x18]
    cmp r0, r4
    blt .L_021ef6ba
.L_021ef716:
    ldr r0, [sp, #0xc]
    str r4, [r0, #0]
    ldr r0, .L_pool_021ef7dc
    ldr r0, [r0, #0x38]
    cmp r0, #0x1
    beq .L_021ef770
    ldr r0, [sp, #0xc]
    ldr r1, [sp, #0x8]
    add r2, sp, #0x20
    bl native_fn_021ef398
    cmp r0, #0x0
    beq .L_021ef770
    ldr r0, [sp, #0xc]
    ldr r2, [sp, #0x20]
    add r1, r0, #0x4
    mov r0, #0x30
    mul r0, r2
    add r4, r1, r0
    ldr r0, .L_pool_021ef7dc
    add r1, r4, #0x4
    str r2, [r0, #0x18]
    ldr r0, .L_pool_021ef7f0
    blx native_fn_0201d6b8
    add r0, r4, #0x0
    add r4, #0x28
    ldrb r2, [r4, #0]
    ldr r1, .L_pool_021ef7f4
    add r0, #0x28
    strb r2, [r1, #0]
    ldrb r2, [r0, #0x1]
    strb r2, [r1, #0x1]
    ldrb r2, [r0, #0x2]
    strb r2, [r1, #0x2]
    ldrb r2, [r0, #0x3]
    strb r2, [r1, #0x3]
    ldrb r2, [r0, #0x4]
    strb r2, [r1, #0x4]
    ldrb r0, [r0, #0x5]
    strb r0, [r1, #0x5]
    add r0, sp, #0x50
    bl native_fn_021f1f74
    b .L_021ef79a
.L_021ef770:
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0xc]
    ldr r2, [sp, #0x10]
    blx native_fn_0201b19c
    ldr r0, .L_pool_021ef7dc
    mov r1, #0x2
    str r1, [r0, #0x38]
    bl native_fn_021f2170
    ldr r0, [sp, #0x1c]
    add r0, r0, #0x1
    str r0, [sp, #0x1c]
.L_021ef78a:
    ldr r0, [sp, #0x1c]
    cmp r0, #0x1e
    bge .L_021ef79a
    ldr r0, .L_pool_021ef7dc
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    bne .L_021ef79a
    b .L_021ef5a4
.L_021ef79a:
    ldr r0, [sp, #0x1c]
    cmp r0, #0x1e
    bge .L_021ef7ac
    bl native_fn_021f1ef0
    ldr r1, .L_pool_021ef7e0
    ldr r1, [r1, #0xc]
    cmp r0, r1
    bls .L_021ef7b2
.L_021ef7ac:
    mov r4, #0x2
    mvn r4, r4
    b .L_021ef7c2
.L_021ef7b2:
    ldr r0, .L_pool_021ef7dc
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    beq .L_021ef7c0
    mov r4, #0x7
    mvn r4, r4
    b .L_021ef7c2
.L_021ef7c0:
    mov r4, #0x1
.L_021ef7c2:
    ldr r0, [sp, #0xc]
    cmp r0, #0x0
    beq .L_021ef7cc
    bl native_fn_021f1f30
.L_021ef7cc:
    ldr r0, [sp, #0x8]
    cmp r0, #0x0
    beq .L_021ef7d6
    bl native_fn_021f1f30
.L_021ef7d6:
    add r0, r4, #0x0
    add sp, #0x70
    pop {r3, r4, r5, r6, r7, pc}
.L_pool_021ef7dc:
    .word 0x0221aad0
.L_pool_021ef7e0:
    .word native_data_0220d480
.L_pool_021ef7e4:
    .word 0x0030bffe
.L_pool_021ef7e8:
    .word 0x000ffb10
.L_pool_021ef7ec:
    .word native_fn_021ef108+1
.L_pool_021ef7f0:
    .word 0x0221afe0
.L_pool_021ef7f4:
    .word 0x0221af80
.size native_ov006_021ef564, .-native_ov006_021ef564
