/* ov006 row 0x021eceac: 188 bytes.
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
.extern native_fn_021edbac
.extern native_fn_021edcb8
.extern native_fn_021edb9c
.extern native_fn_021ecf68
.extern native_fn_021edc90
.global native_ov006_021eceac
.type native_ov006_021eceac, @function
native_ov006_021eceac:
    push {r3, r4, r5, r6, r7, lr}
    add r5, r1, #0x0
    mov r2, #0x41
    add r6, r0, #0x0
    add r0, r5, #0x0
    mov r1, #0x0
    lsl r2, r2, #0x2
    bl native_fn_021edbac
    add r7, r5, #0x0
    add r4, r6, #0x0
    add r7, #0x80
.L_021ecec4:
    ldrh r0, [r4, #0x2]
    bl native_fn_021edcb8
    add r2, r0, #0x0
    cmp r2, #0x0
    bgt .L_021eced6
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021eced6:
    ldrb r0, [r4, #0]
    cmp r0, #0x6
    bhi .L_021ecf4c
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x000c
    .hword 0x0016
    .hword 0x0020
    .hword 0x002e
    .hword 0x002e
    .hword 0x003e
    .hword 0x0050
    add r0, r5, #0x0
    add r1, r4, #0x6
    bl native_fn_021edb9c
    b .L_021ecf52
    add r0, r7, #0x0
    add r1, r4, #0x6
    bl native_fn_021edb9c
    b .L_021ecf52
    mov r0, #0x1
    lsl r0, r0, #0x8
    add r0, r5, r0
    add r1, r4, #0x6
    bl native_fn_021edb9c
    b .L_021ecf52
    ldrb r0, [r4, #0x6]
    bl native_fn_021edcb8
    cmp r0, #0x0
    bgt .L_021ecf52
    mov r0, #0x1
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
    add r0, r4, #0x6
    add r1, r2, #0x0
    bl native_fn_021ecf68
    bl native_fn_021edc90
    ldr r1, .L_pool_021ecf64
    str r0, [r1, #0x34]
    b .L_021ecf52
    add r0, r4, #0x6
    add r1, r2, #0x0
    bl native_fn_021ecf68
    bl native_fn_021edc90
    ldr r1, .L_pool_021ecf64
    str r0, [r1, #0x38]
    b .L_021ecf52
.L_021ecf4c:
    mov r0, #0x0
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ecf52:
    ldrh r0, [r4, #0x4]
    cmp r0, #0x0
    beq .L_021ecf60
    bl native_fn_021edcb8
    add r4, r6, r0
    b .L_021ecec4
.L_021ecf60:
    mov r0, #0x0
    pop {r3, r4, r5, r6, r7, pc}
.L_pool_021ecf64:
    .word 0x02219b4c
.size native_ov006_021eceac, .-native_ov006_021eceac
