/* ov006 row 0x022022f0: 124 bytes.
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
.extern native_fn_0220182c
.extern native_fn_022019d0
.extern native_fn_02201cf4
.extern native_fn_02008430
.global native_ov006_022022f0
.type native_ov006_022022f0, @function
native_ov006_022022f0:
    push {r3, lr}
    bl native_fn_02201820
    cmp r0, #0x9
    bhi .L_02202358
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0036
    .hword 0x0012
    .hword 0x0050
    .hword 0x0054
    .hword 0x0050
    .hword 0x0050
    .hword 0x0050
    .hword 0x0018
    .hword 0x0050
    .hword 0x004a
    bl native_fn_0220182c
    pop {r3, pc}
    bl native_fn_022019d0
    ldr r2, .L_pool_02202360
    ldr r1, .L_pool_02202364
    ldr r3, [r2, #0]
    strh r0, [r3, r1]
    ldr r1, [r2, #0]
    ldr r0, .L_pool_02202368
    mov r3, #0x0
    str r3, [r1, r0]
    ldr r1, [r2, #0]
    mov r3, #0x3
    sub r0, #0x8
    strb r3, [r1, r0]
    pop {r3, pc}
    ldr r1, .L_pool_02202360
    ldr r0, .L_pool_02202368
    ldr r2, [r1, #0]
    mov r3, #0x0
    str r3, [r2, r0]
    ldr r1, [r1, #0]
    mov r2, #0x3
    sub r0, #0x8
    strb r2, [r1, r0]
    pop {r3, pc}
    bl native_fn_02201cf4
    pop {r3, pc}
.L_02202358:
    blx native_fn_02008430
    pop {r3, pc}
    mov r8, r8
.L_pool_02202360:
    .word 0x0221c16c
.L_pool_02202364:
    .word 0x0000064a
.L_pool_02202368:
    .word 0x00000a98
.size native_ov006_022022f0, .-native_ov006_022022f0
