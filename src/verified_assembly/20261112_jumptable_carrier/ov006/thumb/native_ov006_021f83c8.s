/* ov006 row 0x021f83c8: 432 bytes.
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
.extern native_fn_021fe6c4
.extern native_fn_021f23f4
.extern native_fn_021f2a4c
.extern native_fn_021fe6b8
.extern native_fn_02002480
.extern native_fn_021f8800
.extern native_fn_021f23e4
.extern native_fn_021ff6d4
.extern native_fn_020024bc
.extern native_fn_021f8b3c
.extern native_fn_0220490c
.extern native_fn_021f8a18
.extern native_fn_021f8a98
.global native_ov006_021f83c8
.type native_ov006_021f83c8, @function
native_ov006_021f83c8:
    push {r3, lr}
    ldr r0, .L_pool_021f856c
    ldr r0, [r0, #0x4]
    ldr r1, [r0, #0x38]
    cmp r1, #0x0
    beq .L_021f83d6
    b .L_021f8568
.L_021f83d6:
    add r1, r0, #0x0
    add r1, #0x55
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    beq .L_021f83ec
    add r1, r0, #0x0
    add r1, #0x55
    ldrb r1, [r1, #0]
    add r0, #0x55
    sub r1, r1, #0x1
    strb r1, [r0, #0]
.L_021f83ec:
    bl native_fn_021fe6c4
    cmp r0, #0x7
    bhi .L_021f842c
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0166
    .hword 0x000e
    .hword 0x001e
    .hword 0x005c
    .hword 0x00d0
    .hword 0x015c
    .hword 0x010e
    .hword 0x015c
    ldr r0, .L_pool_021f856c
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x57
    strb r1, [r0, #0]
    bl native_fn_021f23f4
    pop {r3, pc}
    ldr r0, .L_pool_021f856c
    ldr r0, [r0, #0x4]
    add r0, #0x55
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq .L_021f842e
.L_021f842c:
    b .L_021f8568
.L_021f842e:
    bl native_fn_021f2a4c
    bl native_fn_021fe6b8
    ldr r1, .L_pool_021f856c
    ldr r2, [r1, #0x4]
    add r1, r2, #0x0
    add r1, #0x40
    ldrh r1, [r1, #0]
    add r2, #0x53
    mul r0, r1
    ldrb r1, [r2, #0]
    blx native_fn_02002480
    ldr r1, .L_pool_021f856c
    strh r0, [r1, #0x2]
    bl native_fn_021f8800
    ldr r0, .L_pool_021f856c
    mov r1, #0x4
    ldr r0, [r0, #0x4]
    add r0, #0x55
    strb r1, [r0, #0]
    pop {r3, pc}
    ldr r0, .L_pool_021f856c
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, #0x57
    strb r1, [r0, #0]
    bl native_fn_021f23e4
    bl native_fn_021fe6b8
    ldr r1, .L_pool_021f856c
    ldr r2, [r1, #0x4]
    add r1, r2, #0x0
    add r1, #0x40
    ldrh r1, [r1, #0]
    add r2, #0x53
    mul r0, r1
    ldrb r1, [r2, #0]
    blx native_fn_02002480
    ldr r1, .L_pool_021f856c
    strh r0, [r1, #0x2]
    mov r0, #0x13
    bl native_fn_021ff6d4
    bl native_fn_021f8800
    ldr r0, .L_pool_021f856c
    mov r1, #0x1c
    ldrh r0, [r0, #0x2]
    blx native_fn_020024bc
    cmp r0, #0x0
    bne .L_021f84a6
    bl native_fn_021f8b3c
    pop {r3, pc}
.L_021f84a6:
    cmp r0, #0xe
    bge .L_021f84be
    mov r0, #0x0
    ldr r1, .L_pool_021f8570
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021f856c
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
    pop {r3, pc}
.L_021f84be:
    mov r0, #0x0
    ldr r1, .L_pool_021f8574
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021f856c
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
    pop {r3, pc}
    ldr r0, .L_pool_021f856c
    ldrh r1, [r0, #0x2]
    cmp r1, #0x0
    bne .L_021f84f6
    ldr r0, [r0, #0x4]
    add r0, #0x58
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021f8568
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021f856c
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x58
    strb r1, [r0, #0]
    pop {r3, pc}
.L_021f84f6:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021f8570
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021f856c
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
    pop {r3, pc}
    ldr r1, .L_pool_021f856c
    ldr r2, [r1, #0x4]
    add r0, r2, #0x0
    add r0, #0x51
    ldrb r0, [r0, #0]
    cmp r0, #0x4
    bls .L_021f852a
    add r0, r2, #0x0
    add r0, #0x40
    ldrh r1, [r1, #0x2]
    ldrh r0, [r0, #0]
    cmp r1, r0
    bne .L_021f8544
.L_021f852a:
    add r2, #0x58
    ldrb r0, [r2, #0]
    cmp r0, #0x0
    bne .L_021f8568
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021f856c
    mov r1, #0x1
    ldr r0, [r0, #0x4]
    add r0, #0x58
    strb r1, [r0, #0]
    pop {r3, pc}
.L_021f8544:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021f8574
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021f856c
    ldr r1, [r1, #0x4]
    str r0, [r1, #0x38]
    pop {r3, pc}
    ldr r0, .L_pool_021f856c
    mov r1, #0x0
    ldr r0, [r0, #0x4]
    add r0, #0x58
    strb r1, [r0, #0]
.L_021f8568:
    pop {r3, pc}
    mov r8, r8
.L_pool_021f856c:
    .word 0x0221c0d8
.L_pool_021f8570:
    .word native_fn_021f8a18+1
.L_pool_021f8574:
    .word native_fn_021f8a98+1
.size native_ov006_021f83c8, .-native_ov006_021f83c8
