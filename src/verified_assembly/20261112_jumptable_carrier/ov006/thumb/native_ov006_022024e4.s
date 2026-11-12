/* ov006 row 0x022024e4: 352 bytes.
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
.extern native_fn_02201820
.extern native_fn_02201b78
.extern native_fn_022026d8
.extern native_fn_022027dc
.extern native_fn_02202884
.global native_ov006_022024e4
.type native_ov006_022024e4, @function
native_ov006_022024e4:
    push {r3, r4, r5, lr}
    bl native_fn_02201820
    cmp r0, #0x6
    bls .L_022024f0
    b .L_02202634
.L_022024f0:
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0136
    .hword 0x000c
    .hword 0x0136
    .hword 0x0136
    .hword 0x0026
    .hword 0x0026
    .hword 0x0026
    ldr r0, .L_pool_02202638
    ldr r3, .L_pool_0220263c
    ldr r2, [r0, #0]
    mov r0, #0x4
    ldrh r1, [r2, r3]
    add r3, r3, #0x2
    ldrh r2, [r2, r3]
    add r1, r1, #0x1
    lsl r1, r1, #0x10
    lsr r1, r1, #0x10
    bl native_fn_02201b78
    pop {r3, r4, r5, pc}
    ldr r0, .L_pool_02202638
    ldr r2, .L_pool_02202640
    ldr r3, [r0, #0]
    mov r0, #0x2
    lsl r0, r0, #0x8
    ldrh r1, [r3, r0]
    ldr r2, [r3, r2]
    mov r3, #0x1c
    lsr r5, r1, #0x1f
    lsl r4, r1, #0x1c
    sub r4, r4, r5
    ror r4, r3
    add r3, r5, r4
    lsl r3, r3, #0x6
    mov r0, #0x0
    add r2, r2, r3
    bl native_fn_022026d8
    bl native_fn_022027dc
    ldr r0, .L_pool_02202638
    mov r1, #0xa9
    ldr r3, [r0, #0]
    lsl r1, r1, #0x4
    ldrb r0, [r3, r1]
    cmp r0, #0x1b
    beq .L_02202634
    mov r0, #0x81
    lsl r0, r0, #0x2
    ldr r2, [r3, r0]
    sub r0, #0x24
    cmp r2, r0
    bls .L_0220256c
    mov r0, #0x1b
    strb r0, [r3, r1]
    pop {r3, r4, r5, pc}
.L_0220256c:
    bl native_fn_02202884
    cmp r0, #0x10
    beq .L_0220257c
    bl native_fn_02202884
    cmp r0, #0x20
    bne .L_0220258e
.L_0220257c:
    bl native_fn_02202884
    ldr r0, .L_pool_02202638
    mov r2, #0xa
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_0220258e:
    bl native_fn_02202884
    cmp r0, #0x40
    bne .L_022025a4
    ldr r0, .L_pool_02202638
    mov r2, #0xb
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_022025a4:
    bl native_fn_02202884
    cmp r0, #0xff
    bne .L_022025ba
    ldr r0, .L_pool_02202638
    mov r2, #0x1b
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_022025ba:
    bl native_fn_02202884
    cmp r0, #0x50
    bne .L_022025d0
    ldr r0, .L_pool_02202638
    mov r2, #0x15
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_022025d0:
    bl native_fn_02202884
    cmp r0, #0x60
    bne .L_022025e6
    ldr r0, .L_pool_02202638
    mov r2, #0x18
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_022025e6:
    bl native_fn_02202884
    cmp r0, #0x70
    bne .L_022025fc
    ldr r0, .L_pool_02202638
    mov r2, #0x1b
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_022025fc:
    bl native_fn_02202884
    cmp r0, #0x0
    bne .L_02202612
    ldr r0, .L_pool_02202638
    mov r2, #0x8
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_02202612:
    bl native_fn_02202884
    cmp r0, #0xbd
    bne .L_02202628
    ldr r0, .L_pool_02202638
    mov r2, #0x9
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
    pop {r3, r4, r5, pc}
.L_02202628:
    ldr r0, .L_pool_02202638
    mov r2, #0x1f
    ldr r1, [r0, #0]
    mov r0, #0xa9
    lsl r0, r0, #0x4
    strb r2, [r1, r0]
.L_02202634:
    pop {r3, r4, r5, pc}
    mov r8, r8
.L_pool_02202638:
    .word 0x0221c16c
.L_pool_0220263c:
    .word 0x00000648
.L_pool_02202640:
    .word 0x00000aa4
.size native_ov006_022024e4, .-native_ov006_022024e4
