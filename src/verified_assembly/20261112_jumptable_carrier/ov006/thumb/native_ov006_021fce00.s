/* ov006 row 0x021fce00: 324 bytes.
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
.extern native_fn_021ff6d4
.extern native_fn_021fcdb4
.global native_ov006_021fce00
.type native_ov006_021fce00, @function
native_ov006_021fce00:
    push {r4, lr}
    ldr r1, .L_pool_021fcf40
    mov r2, #0x1
    ldrb r3, [r1, #0]
    cmp r3, #0x6
    bls .L_021fce0e
    b .L_021fcf2e
.L_021fce0e:
    add r3, r3, r3
    add r3, pc
    ldrh r3, [r3, #0x6]
    lsl r3, r3, #0x10
    asr r3, r3, #0x10
    add pc, r3
    .hword 0x000c
    .hword 0x0034
    .hword 0x005c
    .hword 0x0084
    .hword 0x009e
    .hword 0x00c6
    .hword 0x00ec
    ldr r3, [r1, #0x4]
    mov r4, #0x0
    strb r4, [r3, #0x1c]
    cmp r0, #0x0
    bne .L_021fce38
    mov r0, #0x2
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce38:
    cmp r0, #0x2
    bne .L_021fce40
    strb r2, [r1, #0]
    b .L_021fcf2e
.L_021fce40:
    cmp r0, #0x1
    bne .L_021fce4a
    mov r0, #0x3
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce4a:
    mov r0, #0x4
    strb r0, [r1, #0]
    b .L_021fcf2e
    ldr r3, [r1, #0x4]
    cmp r0, #0x0
    strb r2, [r3, #0x1c]
    bne .L_021fce5e
    mov r0, #0x0
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce5e:
    cmp r0, #0x2
    bne .L_021fce68
    mov r0, #0x2
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce68:
    cmp r0, #0x1
    bne .L_021fce72
    mov r0, #0x3
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce72:
    mov r0, #0x5
    strb r0, [r1, #0]
    b .L_021fcf2e
    ldr r3, [r1, #0x4]
    mov r4, #0x2
    strb r4, [r3, #0x1c]
    cmp r0, #0x0
    bne .L_021fce86
    strb r2, [r1, #0]
    b .L_021fcf2e
.L_021fce86:
    cmp r0, #0x2
    bne .L_021fce90
    mov r0, #0x0
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce90:
    cmp r0, #0x1
    bne .L_021fce9a
    mov r0, #0x3
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fce9a:
    mov r0, #0x6
    strb r0, [r1, #0]
    b .L_021fcf2e
    ldr r3, [r1, #0x4]
    ldrb r4, [r3, #0x1c]
    add r3, r4, #0x4
    cmp r0, #0x1
    bne .L_021fceae
    strb r3, [r1, #0]
    b .L_021fcf2e
.L_021fceae:
    cmp r0, #0x3
    bne .L_021fceb6
    strb r4, [r1, #0]
    b .L_021fcf2e
.L_021fceb6:
    mov r2, #0x0
    b .L_021fcf2e
    ldr r3, [r1, #0x4]
    mov r4, #0x0
    strb r4, [r3, #0x1c]
    cmp r0, #0x0
    bne .L_021fceca
    mov r0, #0x6
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fceca:
    cmp r0, #0x2
    bne .L_021fced4
    mov r0, #0x5
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fced4:
    cmp r0, #0x1
    bne .L_021fcedc
    strb r4, [r1, #0]
    b .L_021fcf2e
.L_021fcedc:
    mov r0, #0x3
    strb r0, [r1, #0]
    b .L_021fcf2e
    ldr r3, [r1, #0x4]
    cmp r0, #0x0
    strb r2, [r3, #0x1c]
    bne .L_021fcef0
    mov r0, #0x4
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fcef0:
    cmp r0, #0x2
    bne .L_021fcefa
    mov r0, #0x6
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fcefa:
    cmp r0, #0x1
    bne .L_021fcf02
    strb r2, [r1, #0]
    b .L_021fcf2e
.L_021fcf02:
    mov r0, #0x3
    strb r0, [r1, #0]
    b .L_021fcf2e
    ldr r3, [r1, #0x4]
    mov r4, #0x2
    strb r4, [r3, #0x1c]
    cmp r0, #0x0
    bne .L_021fcf18
    mov r0, #0x5
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fcf18:
    cmp r0, #0x2
    bne .L_021fcf22
    mov r0, #0x4
    strb r0, [r1, #0]
    b .L_021fcf2e
.L_021fcf22:
    cmp r0, #0x1
    bne .L_021fcf2a
    strb r4, [r1, #0]
    b .L_021fcf2e
.L_021fcf2a:
    mov r0, #0x3
    strb r0, [r1, #0]
.L_021fcf2e:
    cmp r2, #0x0
    beq .L_021fcf3c
    mov r0, #0x8
    bl native_fn_021ff6d4
    bl native_fn_021fcdb4
.L_021fcf3c:
    pop {r4, pc}
    mov r8, r8
.L_pool_021fcf40:
    .word 0x0221c10c
.size native_ov006_021fce00, .-native_ov006_021fce00
