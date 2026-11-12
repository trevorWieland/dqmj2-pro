/* ov006 row 0x021fcc90: 292 bytes.
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
.extern native_fn_02203188
.extern native_fn_021ffdd4
.extern native_fn_021f23c4
.extern native_fn_02202d64
.extern native_fn_021f2a4c
.extern native_fn_021f2774
.extern native_fn_02202b24
.extern native_fn_021f27d4
.extern native_fn_02203954
.extern native_fn_021f52d8
.extern native_fn_021f52cc
.extern native_fn_021fedc8
.extern native_fn_021f5300
.extern native_fn_021fb930
.extern native_fn_02203c20
.extern native_data_0220e058
.extern native_fn_021f5a4c
.extern native_fn_021fd11c
.extern native_fn_021fa164
.extern native_fn_021fde00
.global native_ov006_021fcc90
.type native_ov006_021fcc90, @function
native_ov006_021fcc90:
    push {r4, r5, r6, lr}
    mov r0, #0x1
    bl native_fn_02203188
    cmp r0, #0x0
    bne .L_021fcd92
    mov r0, #0x0
    bl native_fn_02203188
    cmp r0, #0x0
    bne .L_021fcd92
    bl native_fn_021ffdd4
    cmp r0, #0x0
    beq .L_021fcd92
    bl native_fn_021f23c4
    cmp r0, #0x0
    beq .L_021fcd92
    mov r5, #0x0
    ldr r6, .L_pool_021fcd94
    add r4, r5, #0x0
.L_021fccbc:
    ldr r0, [r6, #0x4]
    add r0, r0, r4
    ldr r0, [r0, #0x4]
    cmp r0, #0x0
    beq .L_021fccca
    bl native_fn_02202d64
.L_021fccca:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x3
    blo .L_021fccbc
    mov r5, #0x0
    ldr r6, .L_pool_021fcd94
    add r4, r5, #0x0
.L_021fccd8:
    ldr r0, [r6, #0x4]
    add r0, r0, r4
    ldr r0, [r0, #0x10]
    cmp r0, #0x0
    beq .L_021fcce6
    bl native_fn_02202d64
.L_021fcce6:
    add r5, r5, #0x1
    add r4, r4, #0x4
    cmp r5, #0x3
    blo .L_021fccd8
    bl native_fn_021f2a4c
    bl native_fn_021f2774
    ldr r0, .L_pool_021fcd94
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0]
    bl native_fn_02202b24
    ldr r0, .L_pool_021fcd98
    ldr r1, .L_pool_021fcd9c
    bl native_fn_021f27d4
    mov r0, #0x1
    add r1, r0, #0x0
    bl native_fn_02203954
    mov r0, #0x0
    mov r1, #0x14
    bl native_fn_02203954
    ldr r0, .L_pool_021fcd94
    ldr r1, [r0, #0x4]
    ldrb r1, [r1, #0x1d]
    cmp r1, #0x2
    bne .L_021fcd32
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_021f52d8
    ldr r0, .L_pool_021fcda0
    bl native_fn_021f52cc
    b .L_021fcd8c
.L_021fcd32:
    ldrb r0, [r0, #0]
    cmp r0, #0x3
    bhi .L_021fcd8c
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0006
    .hword 0x0006
    .hword 0x0006
    .hword 0x0038
    mov r0, #0x2
    mov r1, #0x0
    bl native_fn_021f52d8
    bl native_fn_021fedc8
    add r0, #0xe7
    ldrb r0, [r0, #0]
    cmp r0, #0xff
    bne .L_021fcd68
    ldr r0, .L_pool_021fcda4
    bl native_fn_021f52cc
    b .L_021fcd8c
.L_021fcd68:
    mov r0, #0x0
    add r1, r0, #0x0
    bl native_fn_021f5300
    mov r0, #0x0
    bl native_fn_021fb930
    ldr r0, .L_pool_021fcda8
    bl native_fn_021f52cc
    b .L_021fcd8c
    mov r0, #0x2
    mov r1, #0x1
    bl native_fn_021f52d8
    ldr r0, .L_pool_021fcdac
    bl native_fn_021f52cc
.L_021fcd8c:
    ldr r0, .L_pool_021fcdb0
    bl native_fn_02203c20
.L_021fcd92:
    pop {r4, r5, r6, pc}
.L_pool_021fcd94:
    .word 0x0221c10c
.L_pool_021fcd98:
    .word native_data_0220e058
.L_pool_021fcd9c:
    .word 0x0200494c
.L_pool_021fcda0:
    .word native_fn_021f5a4c+1
.L_pool_021fcda4:
    .word native_fn_021fd11c+1
.L_pool_021fcda8:
    .word native_fn_021fa164+1
.L_pool_021fcdac:
    .word native_fn_021fde00+1
.L_pool_021fcdb0:
    .word 0x0221c110
.size native_ov006_021fcc90, .-native_ov006_021fcc90
