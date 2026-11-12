/* ov006 row 0x021fe338: 168 bytes.
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
.extern native_fn_021ff718
.extern native_fn_021ff6d4
.extern native_fn_02200344
.extern native_fn_021f23f4
.extern native_fn_021f52cc
.extern native_fn_02200028
.extern native_fn_021fe3e0
.extern native_fn_021fe234
.extern native_fn_021fe418
.global native_ov006_021fe338
.type native_ov006_021fe338, @function
native_ov006_021fe338:
    push {r3, lr}
    ldr r1, .L_pool_021fe3d0
    ldrb r2, [r1, #0]
    cmp r2, #0x0
    bne .L_021fe3cc
    cmp r0, #0x3
    bhi .L_021fe3cc
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0006
    .hword 0x0030
    .hword 0x0040
    .hword 0x0064
    mov r0, #0x3
    strb r0, [r1, #0]
    bl native_fn_021ff718
    mov r0, #0x12
    bl native_fn_021ff6d4
    mov r1, #0x1
    mov r0, #0x0
    str r0, [sp]
    mov r0, #0x10
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    bl native_fn_021f23f4
    ldr r0, .L_pool_021fe3d4
    bl native_fn_021f52cc
    pop {r3, pc}
    mov r0, #0x1
    strb r0, [r1, #0]
    bl native_fn_021ff718
    ldr r0, .L_pool_021fe3d8
    bl native_fn_021f52cc
    pop {r3, pc}
    bl native_fn_021ff718
    mov r0, #0x0
    bl native_fn_02200028
    mov r2, #0x1
    mov r1, #0x0
    mov r0, #0x11
    sub r3, r2, #0x2
    str r1, [sp]
    bl native_fn_02200344
    bl native_fn_021f23f4
    ldr r0, .L_pool_021fe3dc
    bl native_fn_021f52cc
    pop {r3, pc}
    mov r0, #0x2
    strb r0, [r1, #0]
    bl native_fn_021ff718
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021fe3d8
    bl native_fn_021f52cc
.L_021fe3cc:
    pop {r3, pc}
    mov r8, r8
.L_pool_021fe3d0:
    .word 0x0221c130
.L_pool_021fe3d4:
    .word native_fn_021fe3e0+1
.L_pool_021fe3d8:
    .word native_fn_021fe234+1
.L_pool_021fe3dc:
    .word native_fn_021fe418+1
.size native_ov006_021fe338, .-native_ov006_021fe338
