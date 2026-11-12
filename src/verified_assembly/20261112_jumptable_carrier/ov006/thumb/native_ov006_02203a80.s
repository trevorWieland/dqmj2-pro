/* ov006 row 0x02203a80: 276 bytes.
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
.global native_ov006_02203a80
.type native_ov006_02203a80, @function
native_ov006_02203a80:
    push {r3, r4}
    cmp r1, #0x3
    bhi .L_02203b7a
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0006
    .hword 0x003e
    .hword 0x0078
    .hword 0x00b2
    cmp r0, #0x1
    bne .L_02203ab8
    ldr r0, .L_pool_02203b80
    ldrh r1, [r0, #0]
    mov r0, #0x3f
    bic r1, r0
    orr r1, r2
    cmp r3, #0x0
    beq .L_02203ab0
    mov r0, #0x20
    orr r1, r0
.L_02203ab0:
    ldr r0, .L_pool_02203b80
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
.L_02203ab8:
    ldr r0, .L_pool_02203b84
    ldrh r1, [r0, #0]
    mov r0, #0x3f
    bic r1, r0
    orr r1, r2
    cmp r3, #0x0
    beq .L_02203aca
    mov r0, #0x20
    orr r1, r0
.L_02203aca:
    ldr r0, .L_pool_02203b84
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
    cmp r0, #0x1
    ldr r0, .L_pool_02203b88
    bne .L_02203af2
    ldr r4, .L_pool_02203b80
    ldrh r1, [r4, #0]
    and r1, r0
    lsl r0, r2, #0x8
    orr r1, r0
    cmp r3, #0x0
    beq .L_02203aea
    lsr r0, r4, #0xd
    orr r1, r0
.L_02203aea:
    ldr r0, .L_pool_02203b80
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
.L_02203af2:
    ldr r4, .L_pool_02203b84
    ldrh r1, [r4, #0]
    and r1, r0
    lsl r0, r2, #0x8
    orr r1, r0
    cmp r3, #0x0
    beq .L_02203b04
    lsr r0, r4, #0xd
    orr r1, r0
.L_02203b04:
    ldr r0, .L_pool_02203b84
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
    cmp r0, #0x1
    ldr r0, .L_pool_02203b88
    bne .L_02203b2c
    ldr r4, .L_pool_02203b8c
    ldrh r1, [r4, #0]
    and r1, r0
    lsl r0, r2, #0x8
    orr r1, r0
    cmp r3, #0x0
    beq .L_02203b24
    lsr r0, r4, #0xd
    orr r1, r0
.L_02203b24:
    ldr r0, .L_pool_02203b8c
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
.L_02203b2c:
    ldr r4, .L_pool_02203b90
    ldrh r1, [r4, #0]
    and r1, r0
    lsl r0, r2, #0x8
    orr r1, r0
    cmp r3, #0x0
    beq .L_02203b3e
    lsr r0, r4, #0xd
    orr r1, r0
.L_02203b3e:
    ldr r0, .L_pool_02203b90
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
    cmp r0, #0x1
    bne .L_02203b64
    ldr r0, .L_pool_02203b8c
    ldrh r1, [r0, #0]
    mov r0, #0x3f
    bic r1, r0
    orr r1, r2
    cmp r3, #0x0
    beq .L_02203b5c
    mov r0, #0x20
    orr r1, r0
.L_02203b5c:
    ldr r0, .L_pool_02203b8c
    strh r1, [r0, #0]
    pop {r3, r4}
    bx lr
.L_02203b64:
    ldr r0, .L_pool_02203b90
    ldrh r1, [r0, #0]
    mov r0, #0x3f
    bic r1, r0
    orr r1, r2
    cmp r3, #0x0
    beq .L_02203b76
    mov r0, #0x20
    orr r1, r0
.L_02203b76:
    ldr r0, .L_pool_02203b90
    strh r1, [r0, #0]
.L_02203b7a:
    pop {r3, r4}
    bx lr
    mov r8, r8
.L_pool_02203b80:
    .word 0x04001048
.L_pool_02203b84:
    .word 0x04000048
.L_pool_02203b88:
    .word 0xffffc0ff
.L_pool_02203b8c:
    .word 0x0400104a
.L_pool_02203b90:
    .word 0x0400004a
.size native_ov006_02203a80, .-native_ov006_02203a80
