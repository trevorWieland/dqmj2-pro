/* ov006 row 0x021fa620: 92 bytes.
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
.extern native_fn_021fedc8
.extern native_fn_021fb1dc
.extern native_fn_021fae50
.extern native_fn_021ff6d4
.extern native_fn_021fb5c4
.extern native_fn_021fb800
.extern native_fn_021fa67c
.global native_ov006_021fa620
.type native_ov006_021fa620, @function
native_ov006_021fa620:
    push {r4, lr}
    bl native_fn_021fedc8
    bl native_fn_021fb1dc
    add r4, r0, #0x0
    cmp r4, #0xe
    bne .L_021fa634
    mov r0, #0x0
    pop {r4, pc}
.L_021fa634:
    bl native_fn_021fae50
    cmp r0, #0x0
    bne .L_021fa646
    mov r0, #0x9
    bl native_fn_021ff6d4
    mov r0, #0x1
    pop {r4, pc}
.L_021fa646:
    add r0, r4, #0x0
    bl native_fn_021fb5c4
    cmp r4, #0x8
    bhi .L_021fa672
    add r0, r4, r4
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0014
    .hword 0x0014
    .hword 0x0010
    .hword 0x0010
    .hword 0x0014
    .hword 0x0014
    .hword 0x0014
    .hword 0x0010
    .hword 0x0010
    bl native_fn_021fb800
.L_021fa672:
    add r0, r4, #0x0
    bl native_fn_021fa67c
    mov r0, #0x1
    pop {r4, pc}
.size native_ov006_021fa620, .-native_ov006_021fa620
