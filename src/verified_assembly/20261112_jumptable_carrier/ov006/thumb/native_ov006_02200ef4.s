/* ov006 row 0x02200ef4: 492 bytes.
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
.extern native_fn_022010ec
.extern native_fn_02007ff4
.extern native_fn_02008008
.extern native_fn_02201130
.extern native_fn_02200ed4
.extern native_fn_02200c6c
.extern native_fn_02200c0c
.extern native_fn_0201434c
.extern native_fn_02008e0c
.extern native_fn_02200cec
.extern native_fn_022010e0
.extern native_fn_02008430
.global native_ov006_02200ef4
.type native_ov006_02200ef4, @function
native_ov006_02200ef4:
    push {r4, r5, r6, lr}
    add r4, r0, #0x0
    add r5, r2, #0x0
    cmp r1, #0xe
    bls .L_02200f00
    b .L_022010cc
.L_02200f00:
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x01be
    .hword 0x01c2
    .hword 0x001c
    .hword 0x006a
    .hword 0x01c2
    .hword 0x01c2
    .hword 0x01c2
    .hword 0x012a
    .hword 0x01c2
    .hword 0x0144
    .hword 0x00be
    .hword 0x01c2
    .hword 0x0162
    .hword 0x019a
    .hword 0x0102
    bl native_fn_022010ec
    cmp r0, #0x2
    bne .L_02200f80
    ldr r0, .L_pool_022010d4
    ldr r6, [r0, #0]
    blx native_fn_02007ff4
    mov r1, #0x1
    ldrh r2, [r6, #0x2]
    lsl r1, r4
    orr r1, r2
    strh r1, [r6, #0x2]
    blx native_fn_02008008
    sub r2, r4, #0x1
    add r1, r2, #0x0
    ldr r2, .L_pool_022010d4
    mov r0, #0x1e
    ldr r6, [r2, #0]
    ldrb r3, [r5, #0xa]
    mul r1, r0
    add r6, #0x24
    strb r3, [r6, r1]
    ldrb r3, [r5, #0xb]
    add r0, r6, r1
    strb r3, [r0, #0x1]
    ldrb r3, [r5, #0xc]
    strb r3, [r0, #0x2]
    ldrb r3, [r5, #0xd]
    strb r3, [r0, #0x3]
    ldrb r3, [r5, #0xe]
    strb r3, [r0, #0x4]
    ldrb r3, [r5, #0xf]
    strb r3, [r0, #0x5]
    ldr r0, [r2, #0]
    add r0, r0, r1
    strh r4, [r0, #0x2a]
    pop {r4, r5, r6, pc}
    bl native_fn_02201130
    cmp r0, #0x6
    bne .L_02200f82
.L_02200f80:
    b .L_022010d0
.L_02200f82:
    mov r0, #0x1
    lsl r0, r4
    mvn r0, r0
    lsl r0, r0, #0x10
    lsr r4, r0, #0x10
    blx native_fn_02007ff4
    ldr r1, .L_pool_022010d4
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x2]
    and r2, r4
    strh r2, [r3, #0x2]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x4]
    and r2, r4
    strh r2, [r3, #0x4]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x6]
    and r2, r4
    strh r2, [r3, #0x6]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0x8]
    and r2, r4
    strh r2, [r3, #0x8]
    ldr r3, [r1, #0]
    ldrh r2, [r3, #0xa]
    and r2, r4
    strh r2, [r3, #0xa]
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0xc]
    and r1, r4
    strh r1, [r2, #0xc]
    blx native_fn_02008008
    bl native_fn_02200ed4
    pop {r4, r5, r6, pc}
    bl native_fn_022010ec
    cmp r0, #0x2
    beq .L_02200fdc
    add r0, r4, #0x0
    bl native_fn_02200c6c
    pop {r4, r5, r6, pc}
.L_02200fdc:
    ldr r0, .L_pool_022010d4
    ldr r2, [r0, #0]
    mov r0, #0x1
    ldrh r1, [r2, #0x4]
    lsl r0, r4
    orr r0, r1
    strh r0, [r2, #0x4]
    add r0, r4, #0x0
    bl native_fn_02200c0c
    add r0, r4, #0x0
    blx native_fn_0201434c
    cmp r0, #0x0
    beq .L_022010d0
    ldr r1, .L_pool_022010d4
    sub r2, r4, #0x1
    ldr r3, [r1, #0]
    mov r1, #0x1e
    mul r1, r2
    add r3, #0xe
    add r1, r3, r1
    mov r2, #0x16
    blx native_fn_02008e0c
    pop {r4, r5, r6, pc}
    ldr r1, .L_pool_022010d4
    mov r0, #0x1
    ldr r5, [r1, #0]
    lsl r0, r4
    ldrh r3, [r5, #0x4]
    mvn r2, r0
    and r2, r3
    strh r2, [r5, #0x4]
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0x6]
    orr r0, r1
    strh r0, [r2, #0x6]
    bl native_fn_022010ec
    cmp r0, #0x3
    bne .L_022010d0
    add r0, r4, #0x0
    bl native_fn_02200cec
    pop {r4, r5, r6, pc}
    ldr r1, .L_pool_022010d4
    mov r0, #0x1
    lsl r0, r4
    ldr r4, [r1, #0]
    mvn r2, r0
    ldrh r3, [r4, #0x8]
    and r2, r3
    strh r2, [r4, #0x8]
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0xa]
    orr r0, r1
    strh r0, [r2, #0xa]
    pop {r4, r5, r6, pc}
    ldr r1, .L_pool_022010d4
    mov r0, #0x1
    lsl r0, r4
    ldr r4, [r1, #0]
    mvn r2, r0
    ldrh r3, [r4, #0xa]
    and r2, r3
    strh r2, [r4, #0xa]
    ldr r2, [r1, #0]
    ldrh r1, [r2, #0xc]
    orr r0, r1
    strh r0, [r2, #0xc]
    bl native_fn_02200ed4
    pop {r4, r5, r6, pc}
    bl native_fn_022010ec
    cmp r0, #0x4
    bne .L_02201080
    mov r0, #0x5
    bl native_fn_022010e0
    b .L_02201086
.L_02201080:
    mov r0, #0x0
    bl native_fn_022010e0
.L_02201086:
    ldr r0, .L_pool_022010d4
    ldr r2, [r0, #0]
    ldr r0, .L_pool_022010d8
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq .L_02201096
    mov r1, #0x0
    str r1, [r2, r0]
.L_02201096:
    ldr r0, .L_pool_022010d4
    ldr r2, [r0, #0]
    ldr r0, .L_pool_022010dc
    ldr r1, [r2, r0]
    cmp r1, #0x0
    beq .L_022010d0
    mov r1, #0x0
    str r1, [r2, r0]
    pop {r4, r5, r6, pc}
    ldrh r0, [r5, #0]
    cmp r0, #0x8
    bgt .L_022010c0
    bge .L_022010d0
    cmp r0, #0x2
    bgt .L_022010d0
    cmp r0, #0x1
    blt .L_022010d0
    beq .L_022010c4
    cmp r0, #0x2
    beq .L_022010c4
    pop {r4, r5, r6, pc}
.L_022010c0:
    cmp r0, #0x9
    bne .L_022010d0
.L_022010c4:
    mov r0, #0x7
    bl native_fn_022010e0
    pop {r4, r5, r6, pc}
.L_022010cc:
    blx native_fn_02008430
.L_022010d0:
    pop {r4, r5, r6, pc}
    mov r8, r8
.L_pool_022010d4:
    .word 0x0221c160
.L_pool_022010d8:
    .word 0x0001b144
.L_pool_022010dc:
    .word 0x0001b140
.size native_ov006_02200ef4, .-native_ov006_02200ef4
