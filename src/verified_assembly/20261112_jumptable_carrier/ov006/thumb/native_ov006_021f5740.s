/* ov006 row 0x021f5740: 112 bytes.
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
.extern native_fn_021f215c
.extern native_fn_02008430
.global native_ov006_021f5740
.type native_ov006_021f5740, @function
native_ov006_021f5740:
    push {r3, lr}
    sub sp, #0xe8
    ldr r1, .L_pool_021f57ac
    ldr r1, [r1, #0]
    ldr r1, [r1, #0]
    cmp r1, #0x7
    bhi .L_021f57a8
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x000e
    .hword 0x000e
    .hword 0x0014
    .hword 0x000e
    .hword 0x001a
    .hword 0x000e
    .hword 0x0020
    .hword 0x004a
    add sp, #0xe8
    mov r0, #0x0
    pop {r3, pc}
    add sp, #0xe8
    mov r0, #0x1
    pop {r3, pc}
    add sp, #0xe8
    mov r0, #0x2
    pop {r3, pc}
    add r0, sp, #0x0
    bl native_fn_021f215c
    cmp r0, #0x1
    beq .L_021f578a
    blx native_fn_02008430
.L_021f578a:
    ldr r0, [sp, #0x20]
    cmp r0, #0x0
    blt .L_021f57a0
    cmp r0, #0x3
    bgt .L_021f57a0
    ldr r0, [sp, #0x24]
    cmp r0, #0x1
    bne .L_021f57a0
    add sp, #0xe8
    mov r0, #0x3
    pop {r3, pc}
.L_021f57a0:
    add sp, #0xe8
    mov r0, #0x5
    pop {r3, pc}
    mov r0, #0x4
.L_021f57a8:
    add sp, #0xe8
    pop {r3, pc}
.L_pool_021f57ac:
    .word 0x0221c094
.size native_ov006_021f5740, .-native_ov006_021f5740
