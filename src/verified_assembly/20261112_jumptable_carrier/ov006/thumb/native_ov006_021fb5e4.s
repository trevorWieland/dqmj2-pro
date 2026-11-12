/* ov006 row 0x021fb5e4: 460 bytes.
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
.extern native_fn_021ff6d4
.extern native_fn_021fabe4
.extern native_fn_021fe6d0
.extern native_fn_0220490c
.extern native_fn_021fb4cc
.extern native_fn_021fb550
.extern native_fn_021fb39c
.extern native_fn_021fb414
.global native_ov006_021fb5e4
.type native_ov006_021fb5e4, @function
native_ov006_021fb5e4:
    push {r3, r4, r5, lr}
    add r4, r0, #0x0
    bl native_fn_021fedc8
    ldr r1, .L_pool_021fb7a4
    mov r5, #0x0
    ldrb r1, [r1, #0]
    cmp r1, #0x8
    bne .L_021fb606
    add r0, #0xf5
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021fb606
    cmp r4, #0x0
    beq .L_021fb67a
    cmp r4, #0x2
    beq .L_021fb67a
.L_021fb606:
    cmp r1, #0x0
    bgt .L_021fb60e
    beq .L_021fb62a
    b .L_021fb700
.L_021fb60e:
    add r0, r1, #0x0
    sub r0, #0xa
    cmp r0, #0x3
    bhi .L_021fb700
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0024
    .hword 0x0046
    .hword 0x0088
    .hword 0x0088
.L_021fb62a:
    cmp r4, #0x1
    bne .L_021fb636
    ldr r0, .L_pool_021fb7a4
    mov r1, #0xb
    strb r1, [r0, #0]
    b .L_021fb790
.L_021fb636:
    cmp r4, #0x3
    bne .L_021fb644
    ldr r0, .L_pool_021fb7a4
    ldrb r1, [r0, #0x2]
    add r1, r1, #0x1
    strb r1, [r0, #0x2]
    b .L_021fb790
.L_021fb644:
    mov r5, #0x2
    b .L_021fb790
    cmp r4, #0x1
    bne .L_021fb656
    ldr r0, .L_pool_021fb7a4
    ldrb r1, [r0, #0x2]
    sub r1, r1, #0x1
    strb r1, [r0, #0x2]
    b .L_021fb790
.L_021fb656:
    cmp r4, #0x3
    bne .L_021fb666
    ldr r0, .L_pool_021fb7a4
    ldr r1, [r0, #0x8]
    add r1, #0x42
    ldrb r1, [r1, #0]
    strb r1, [r0, #0]
    b .L_021fb790
.L_021fb666:
    mov r5, #0x2
    b .L_021fb790
    cmp r4, #0x1
    bne .L_021fb68e
    ldr r0, .L_pool_021fb7a4
    ldr r0, [r0, #0x8]
    add r0, #0x47
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq .L_021fb67c
.L_021fb67a:
    b .L_021fb7a2
.L_021fb67c:
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021fb7a4
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, r4, r5, pc}
.L_021fb68e:
    cmp r4, #0x3
    bne .L_021fb6a8
    ldr r0, .L_pool_021fb7a4
    mov r1, #0x0
    strb r1, [r0, #0]
    strb r1, [r0, #0x2]
    strh r1, [r0, #0x4]
    bl native_fn_021fabe4
    mov r0, #0x0
    bl native_fn_021fe6d0
    b .L_021fb790
.L_021fb6a8:
    mov r5, #0x2
    b .L_021fb790
    ldr r0, .L_pool_021fb7a4
    ldr r2, [r0, #0x8]
    add r2, #0x42
    strb r1, [r2, #0]
    cmp r4, #0x1
    bne .L_021fb6d0
    mov r1, #0xa
    strb r1, [r0, #0]
    mov r1, #0x3
    strb r1, [r0, #0x2]
    mov r1, #0x91
    strh r1, [r0, #0x4]
    bl native_fn_021fabe4
    mov r0, #0x37
    bl native_fn_021fe6d0
    b .L_021fb790
.L_021fb6d0:
    cmp r4, #0x3
    bne .L_021fb6f0
    ldr r0, [r0, #0x8]
    add r0, #0x47
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021fb7a2
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021fb7a4
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x47
    strb r1, [r0, #0]
    pop {r3, r4, r5, pc}
.L_021fb6f0:
    cmp r1, #0xc
    bne .L_021fb6fa
    mov r1, #0xd
    strb r1, [r0, #0]
    b .L_021fb790
.L_021fb6fa:
    mov r1, #0xc
    strb r1, [r0, #0]
    b .L_021fb790
.L_021fb700:
    cmp r4, #0x1
    bne .L_021fb72c
    ldr r0, .L_pool_021fb7a4
    ldrb r1, [r0, #0x2]
    cmp r1, #0x0
    beq .L_021fb712
    sub r1, r1, #0x1
    strb r1, [r0, #0x2]
    b .L_021fb790
.L_021fb712:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021fb7a8
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021fb7a4
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, r4, r5, pc}
.L_021fb72c:
    cmp r4, #0x3
    bne .L_021fb758
    ldr r0, .L_pool_021fb7a4
    ldrb r1, [r0, #0x2]
    cmp r1, #0x3
    bhs .L_021fb73e
    add r1, r1, #0x1
    strb r1, [r0, #0x2]
    b .L_021fb790
.L_021fb73e:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021fb7ac
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021fb7a4
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, r4, r5, pc}
.L_021fb758:
    mov r5, #0x2
    cmp r1, #0x2
    bne .L_021fb766
    ldr r0, .L_pool_021fb7a4
    mov r1, #0x3
    strb r1, [r0, #0]
    b .L_021fb786
.L_021fb766:
    cmp r1, #0x3
    bne .L_021fb770
    ldr r0, .L_pool_021fb7a4
    strb r5, [r0, #0]
    b .L_021fb786
.L_021fb770:
    cmp r1, #0x7
    bne .L_021fb77c
    ldr r0, .L_pool_021fb7a4
    mov r1, #0x8
    strb r1, [r0, #0]
    b .L_021fb786
.L_021fb77c:
    cmp r1, #0x8
    bne .L_021fb790
    ldr r0, .L_pool_021fb7a4
    mov r1, #0x7
    strb r1, [r0, #0]
.L_021fb786:
    mov r0, #0x8
    bl native_fn_021ff6d4
    bl native_fn_021fb4cc
.L_021fb790:
    cmp r5, #0x2
    beq .L_021fb7a2
    mov r0, #0x8
    bl native_fn_021ff6d4
    cmp r5, #0x0
    bne .L_021fb7a2
    bl native_fn_021fb550
.L_021fb7a2:
    pop {r3, r4, r5, pc}
.L_pool_021fb7a4:
    .word 0x0221c0ec
.L_pool_021fb7a8:
    .word native_fn_021fb39c+1
.L_pool_021fb7ac:
    .word native_fn_021fb414+1
.size native_ov006_021fb5e4, .-native_ov006_021fb5e4
