/* ov006 row 0x02201d08: 180 bytes.
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
.extern native_fn_02201270
.extern native_fn_02201cf4
.extern native_fn_022016e8
.extern native_fn_02201720
.extern native_fn_02201634
.extern native_fn_02201658
.extern native_data_0220e868
.extern native_data_0220e88c
.global native_ov006_02201d08
.type native_ov006_02201d08, @function
native_ov006_02201d08:
    push {r3, lr}
    ldr r0, .L_pool_02201db0
    ldr r1, [r0, #0x4]
    ldr r2, [r1, #0x40]
    cmp r2, #0x1
    bne .L_02201d24
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_02201dae
    mov r0, #0x2
    ldr r1, .L_pool_02201db4
    lsl r0, r0, #0x1a
    blx r2
    pop {r3, pc}
.L_02201d24:
    ldr r3, [r0, #0]
    cmp r3, #0x0
    beq .L_02201d32
    mov r0, #0x2
    ldr r1, .L_pool_02201db8
    lsl r0, r0, #0x1a
    blx r3
.L_02201d32:
    ldr r0, .L_pool_02201db0
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x40]
    cmp r0, #0x6
    beq .L_02201d50
    cmp r0, #0x5
    beq .L_02201d50
    cmp r0, #0x4
    beq .L_02201d50
    mov r0, #0x3
    bl native_fn_02201270
    bl native_fn_02201cf4
    pop {r3, pc}
.L_02201d50:
    mov r0, #0x3
    bl native_fn_02201270
    ldr r0, .L_pool_02201db0
    ldr r0, [r0, #0x4]
    ldr r0, [r0, #0x44]
    cmp r0, #0x5
    bhi .L_02201dae
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0034
    .hword 0x0018
    .hword 0x0026
    .hword 0x000a
    .hword 0x0034
    .hword 0x0018
    bl native_fn_022016e8
    cmp r0, #0x0
    bne .L_02201dae
    bl native_fn_02201cf4
    pop {r3, pc}
    bl native_fn_02201720
    cmp r0, #0x0
    bne .L_02201dae
    bl native_fn_02201cf4
    pop {r3, pc}
    bl native_fn_02201634
    cmp r0, #0x0
    bne .L_02201dae
    bl native_fn_02201cf4
    pop {r3, pc}
    bl native_fn_02201658
    cmp r0, #0x0
    bne .L_02201dae
    bl native_fn_02201cf4
.L_02201dae:
    pop {r3, pc}
.L_pool_02201db0:
    .word 0x0221c164
.L_pool_02201db4:
    .word native_data_0220e868
.L_pool_02201db8:
    .word native_data_0220e88c
.size native_ov006_02201d08, .-native_ov006_02201d08
