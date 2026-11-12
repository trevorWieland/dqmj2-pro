/* ov006 row 0x021ee348: 696 bytes.
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
.extern native_fn_02089d8c
.extern native_fn_02089ef8
.extern native_fn_02089cf4
.extern native_fn_02089b64
.global native_ov006_021ee348
.type native_ov006_021ee348, @function
native_ov006_021ee348:
    push {r3, lr}
    cmp r0, #0x0
    bne .L_021ee350
    b .L_021ee5f8
.L_021ee350:
    mov r1, #0x0
    ldrsh r2, [r0, r1]
    cmp r2, #0x7
    bls .L_021ee35a
    b .L_021ee5ea
.L_021ee35a:
    add r2, r2, r2
    add r2, pc
    ldrh r2, [r2, #0x6]
    lsl r2, r2, #0x10
    asr r2, r2, #0x10
    add pc, r2
    .hword 0x0282
    .hword 0x000e
    .hword 0x0236
    .hword 0x008e
    .hword 0x00f2
    .hword 0x00c0
    .hword 0x0192
    .hword 0x026e
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021ee3e2
    ldr r2, .L_pool_021ee5fc
    ldr r0, [r2, #0x18]
    cmp r0, #0x4
    bne .L_021ee396
    mov r0, #0x3
    str r0, [r2, #0x18]
    ldr r2, [r2, #0x1c]
    cmp r2, #0x0
    beq .L_021ee3ee
    mov r0, #0x6
    blx r2
    pop {r3, pc}
.L_021ee396:
    cmp r0, #0x6
    bne .L_021ee3bc
    ldr r0, [r2, #0x10]
    ldr r1, [r2, #0x14]
    ldr r2, [r2, #0x4]
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021ee3ee
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee3ee
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee3bc:
    cmp r0, #0x8
    bne .L_021ee3ee
    ldr r0, [r2, #0x20]
    ldr r1, [r2, #0x24]
    ldr r2, [r2, #0xc]
    bl native_fn_02089ef8
    cmp r0, #0x3
    beq .L_021ee3ee
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee3ee
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee3e2:
    ldr r0, .L_pool_021ee5fc
    mov r3, #0x1
    str r3, [r0, #0x18]
    ldr r3, [r0, #0x1c]
    cmp r3, #0x0
    bne .L_021ee3f0
.L_021ee3ee:
    b .L_021ee5f8
.L_021ee3f0:
    add r0, r2, #0x0
    blx r3
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021ee416
    ldr r0, .L_pool_021ee5fc
    ldr r2, [r0, #0x18]
    cmp r2, #0x6
    bne .L_021ee4f2
    mov r2, #0x5
    str r2, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0x8
    blx r2
    pop {r3, pc}
.L_021ee416:
    ldr r0, .L_pool_021ee5fc
    mov r2, #0x3
    str r2, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0x9
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021ee448
    ldr r0, .L_pool_021ee5fc
    ldr r2, [r0, #0x18]
    cmp r2, #0x8
    bne .L_021ee4f2
    mov r2, #0x7
    str r2, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0xc
    blx r2
    pop {r3, pc}
.L_021ee448:
    ldr r0, .L_pool_021ee5fc
    mov r2, #0x3
    str r2, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0xd
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021ee4e6
    ldr r2, .L_pool_021ee5fc
    ldr r0, [r2, #0x18]
    cmp r0, #0x4
    bne .L_021ee47a
    mov r0, #0x3
    str r0, [r2, #0x18]
    ldr r2, [r2, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0xa
    blx r2
    pop {r3, pc}
.L_021ee47a:
    cmp r0, #0x6
    bne .L_021ee4a0
    ldr r0, [r2, #0x10]
    ldr r1, [r2, #0x14]
    ldr r2, [r2, #0x4]
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021ee4f2
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee4a0:
    cmp r0, #0x2
    bne .L_021ee4c0
    bl native_fn_02089cf4
    cmp r0, #0x3
    beq .L_021ee4f2
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee4c0:
    cmp r0, #0x8
    bne .L_021ee4f2
    ldr r0, [r2, #0x20]
    ldr r1, [r2, #0x24]
    ldr r2, [r2, #0xc]
    bl native_fn_02089ef8
    cmp r0, #0x3
    beq .L_021ee4f2
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee4f2
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee4e6:
    ldr r0, .L_pool_021ee5fc
    mov r2, #0x3
    str r2, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    bne .L_021ee4f4
.L_021ee4f2:
    b .L_021ee5f8
.L_021ee4f4:
    mov r0, #0xb
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021ee58c
    ldr r2, .L_pool_021ee5fc
    ldr r0, [r2, #0x18]
    cmp r0, #0x4
    bne .L_021ee51a
    mov r0, #0x3
    str r0, [r2, #0x18]
    ldr r2, [r2, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0xe
    blx r2
    pop {r3, pc}
.L_021ee51a:
    cmp r0, #0x6
    bne .L_021ee540
    ldr r0, [r2, #0x10]
    ldr r1, [r2, #0x14]
    ldr r2, [r2, #0x4]
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021ee5f8
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee540:
    cmp r0, #0x2
    bne .L_021ee560
    bl native_fn_02089cf4
    cmp r0, #0x3
    beq .L_021ee5f8
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee560:
    cmp r0, #0x8
    bne .L_021ee586
    ldr r0, [r2, #0x20]
    ldr r1, [r2, #0x24]
    ldr r2, [r2, #0xc]
    bl native_fn_02089ef8
    cmp r0, #0x3
    beq .L_021ee5f8
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x3
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021ee586:
    mov r0, #0x3
    str r0, [r2, #0x18]
    pop {r3, pc}
.L_021ee58c:
    ldr r0, .L_pool_021ee5fc
    mov r2, #0x3
    str r2, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0xf
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021ee5c4
    ldr r0, .L_pool_021ee5fc
    ldr r0, [r0, #0x18]
    cmp r0, #0x2
    bne .L_021ee5f8
    bl native_fn_02089b64
    ldr r0, .L_pool_021ee5fc
    mov r1, #0x0
    str r1, [r0, #0x18]
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0x14
    blx r2
    pop {r3, pc}
.L_021ee5c4:
    ldr r0, .L_pool_021ee5fc
    mov r3, #0x3
    str r3, [r0, #0x18]
    ldr r3, [r0, #0x1c]
    cmp r3, #0x0
    beq .L_021ee5f8
    add r0, r2, #0x0
    blx r3
    pop {r3, pc}
    ldr r0, .L_pool_021ee5fc
    ldr r2, [r0, #0x18]
    cmp r2, #0x5
    bne .L_021ee5f8
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0x5
    blx r2
    pop {r3, pc}
.L_021ee5ea:
    ldr r0, .L_pool_021ee5fc
    ldr r2, [r0, #0x1c]
    cmp r2, #0x0
    beq .L_021ee5f8
    mov r0, #0x1
    mov r1, #0x0
    blx r2
.L_021ee5f8:
    pop {r3, pc}
    mov r8, r8
.L_pool_021ee5fc:
    .word 0x0221aa80
.size native_ov006_021ee348, .-native_ov006_021ee348
