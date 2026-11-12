/* ov006 row 0x021ee600: 104 bytes.
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
.extern native_fn_0208a060
.extern native_fn_02089ba0
.extern native_fn_021ee348
.global native_ov006_021ee600
.type native_ov006_021ee600, @function
native_ov006_021ee600:
    push {r3, lr}
    ldr r1, .L_pool_021ee660
    ldr r0, [r1, #0x18]
    cmp r0, #0x8
    bhi .L_021ee656
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x003e
    .hword 0x002e
    .hword 0x003e
    .hword 0x003e
    .hword 0x003e
    .hword 0x0010
    .hword 0x003e
    .hword 0x0022
    .hword 0x003e
    mov r0, #0x0
    add r1, r0, #0x0
    add r2, r0, #0x0
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021ee65a
    mov r0, #0x0
    pop {r3, pc}
    bl native_fn_0208a060
    cmp r0, #0x3
    beq .L_021ee65a
    mov r0, #0x0
    pop {r3, pc}
    ldr r0, [r1, #0x8]
    ldr r1, .L_pool_021ee664
    bl native_fn_02089ba0
    cmp r0, #0x3
    beq .L_021ee65a
    mov r0, #0x0
    pop {r3, pc}
.L_021ee656:
    mov r0, #0x0
    pop {r3, pc}
.L_021ee65a:
    mov r0, #0x1
    pop {r3, pc}
    mov r8, r8
.L_pool_021ee660:
    .word 0x0221aa80
.L_pool_021ee664:
    .word native_fn_021ee348+1
.size native_ov006_021ee600, .-native_ov006_021ee600
