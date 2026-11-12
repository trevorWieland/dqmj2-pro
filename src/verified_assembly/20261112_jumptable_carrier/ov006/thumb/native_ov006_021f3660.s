/* ov006 row 0x021f3660: 400 bytes.
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
.extern native_fn_02203eec
.extern native_fn_021f3b10
.extern native_fn_02203ebc
.extern native_fn_021ff6d4
.extern native_fn_021f3984
.extern native_fn_021f3494
.extern native_fn_021f34bc
.extern native_fn_02203f1c
.extern native_data_0220d790
.extern native_data_0220b1ac
.extern native_data_0220b160
.global native_ov006_021f3660
.type native_ov006_021f3660, @function
native_ov006_021f3660:
    push {r3, r4, r5, lr}
    mov r0, #0x20
    bl native_fn_02203eec
    cmp r0, #0x0
    beq .L_021f3672
    mov r0, #0x0
    bl native_fn_021f3b10
.L_021f3672:
    mov r0, #0x40
    bl native_fn_02203eec
    cmp r0, #0x0
    beq .L_021f3682
    mov r0, #0x1
    bl native_fn_021f3b10
.L_021f3682:
    mov r0, #0x10
    bl native_fn_02203eec
    cmp r0, #0x0
    beq .L_021f3692
    mov r0, #0x2
    bl native_fn_021f3b10
.L_021f3692:
    mov r0, #0x80
    bl native_fn_02203eec
    cmp r0, #0x0
    beq .L_021f36a2
    mov r0, #0x3
    bl native_fn_021f3b10
.L_021f36a2:
    mov r0, #0x1
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq .L_021f3760
    ldr r1, .L_pool_021f37d0
    ldr r0, .L_pool_021f37d4
    ldr r2, [r1, #0]
    ldrsb r4, [r2, r0]
    cmp r4, #0x2f
    bge .L_021f36ea
    add r3, r0, #0x3
    ldrb r3, [r2, r3]
    cmp r3, #0x0
    bne .L_021f36c8
    mov r0, #0x9
    bl native_fn_021ff6d4
    pop {r3, r4, r5, pc}
.L_021f36c8:
    sub r3, r0, #0x4
    ldrb r3, [r2, r3]
    lsl r5, r3, #0x2
    ldr r3, .L_pool_021f37d8
    ldr r3, [r3, r5]
    ldrb r4, [r3, r4]
    sub r3, r0, #0x5
    sub r0, r0, #0x4
    strb r4, [r2, r3]
    ldr r1, [r1, #0]
    ldrb r0, [r1, r0]
    cmp r0, #0x1
    bne .L_021f37ce
    mov r0, #0x0
    bl native_fn_021f3984
    pop {r3, r4, r5, pc}
.L_021f36ea:
    add r1, r4, #0x0
    sub r1, #0x2f
    cmp r1, #0x4
    bge .L_021f3756
    cmp r1, #0x3
    bhi .L_021f3736
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0006
    .hword 0x000c
    .hword 0x0012
    .hword 0x0022
    bl native_fn_021f3494
    pop {r3, r4, r5, pc}
    bl native_fn_021f34bc
    pop {r3, r4, r5, pc}
    add r0, r0, #0x3
    ldrb r0, [r2, r0]
    cmp r0, #0x0
    bne .L_021f3736
    mov r0, #0x9
    bl native_fn_021ff6d4
    pop {r3, r4, r5, pc}
    add r0, r0, #0x2
    ldrb r0, [r2, r0]
    cmp r0, #0x0
    bne .L_021f3736
    mov r0, #0x9
    bl native_fn_021ff6d4
    pop {r3, r4, r5, pc}
.L_021f3736:
    ldr r0, .L_pool_021f37dc
    ldrb r0, [r2, r0]
    cmp r0, #0x1
    bne .L_021f3744
    mov r0, #0x0
    bl native_fn_021f3984
.L_021f3744:
    ldr r0, .L_pool_021f37e0
    sub r4, #0x2f
    ldrb r2, [r0, r4]
    ldr r0, .L_pool_021f37d0
    ldr r1, [r0, #0]
    mov r0, #0x47
    lsl r0, r0, #0x2
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_021f3756:
    ldr r1, .L_pool_021f37e4
    sub r4, #0x33
    ldrb r1, [r1, r4]
    sub r0, r0, #0x5
    strb r1, [r2, r0]
.L_021f3760:
    mov r0, #0x2
    bl native_fn_02203eec
    cmp r0, #0x0
    beq .L_021f379a
    ldr r0, .L_pool_021f37d0
    ldr r2, [r0, #0]
    ldr r0, .L_pool_021f37e8
    ldrb r1, [r2, r0]
    cmp r1, #0x0
    bne .L_021f3790
    add r0, r0, #0x2
    ldrb r0, [r2, r0]
    cmp r0, #0x0
    bne .L_021f37ce
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021f37d0
    mov r2, #0x1
    ldr r1, [r0, #0]
    ldr r0, .L_pool_021f37ec
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_021f3790:
    mov r1, #0x80
    add r0, r1, #0x0
    add r0, #0x9c
    strb r1, [r2, r0]
    b .L_021f37ae
.L_021f379a:
    mov r0, #0x2
    bl native_fn_02203f1c
    cmp r0, #0x0
    beq .L_021f37ae
    ldr r0, .L_pool_021f37d0
    mov r2, #0x0
    ldr r1, [r0, #0]
    ldr r0, .L_pool_021f37ec
    strb r2, [r1, r0]
.L_021f37ae:
    mov r0, #0x1
    lsl r0, r0, #0xa
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq .L_021f37be
    bl native_fn_021f3494
.L_021f37be:
    mov r0, #0x2
    lsl r0, r0, #0xa
    bl native_fn_02203ebc
    cmp r0, #0x0
    beq .L_021f37ce
    bl native_fn_021f34bc
.L_021f37ce:
    pop {r3, r4, r5, pc}
.L_pool_021f37d0:
    .word 0x0221c05c
.L_pool_021f37d4:
    .word 0x00000121
.L_pool_021f37d8:
    .word native_data_0220d790
.L_pool_021f37dc:
    .word 0x0000011d
.L_pool_021f37e0:
    .word native_data_0220b1ac
.L_pool_021f37e4:
    .word native_data_0220b160
.L_pool_021f37e8:
    .word 0x00000123
.L_pool_021f37ec:
    .word 0x00000125
.size native_ov006_021f3660, .-native_ov006_021f3660
