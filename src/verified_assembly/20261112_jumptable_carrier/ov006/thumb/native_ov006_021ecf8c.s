/* ov006 row 0x021ecf8c: 338 bytes.
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
.extern native_fn_021edcb8
.extern native_fn_021edb9c
.global native_ov006_021ecf8c
.type native_ov006_021ecf8c, @function
native_ov006_021ecf8c:
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    add r6, r1, #0x0
    add r5, r0, #0x6
    add r0, r6, #0x0
    str r0, [sp, #0xc]
    add r0, #0x8
    str r0, [sp, #0xc]
    add r0, r6, #0x0
    str r0, [sp, #0x8]
    add r0, #0xf0
    str r0, [sp, #0x8]
    add r0, r6, #0x0
    str r0, [sp, #0x4]
    add r0, #0xb0
    str r0, [sp, #0x4]
    add r0, r6, #0x0
    str r0, [sp]
    add r0, #0x70
    add r7, r6, #0x0
    str r0, [sp]
    add r7, #0x30
    str r5, [sp, #0x10]
.L_021ecfba:
    ldrh r0, [r5, #0x2]
    bl native_fn_021edcb8
    add r4, r0, #0x0
    ldrb r0, [r5, #0]
    cmp r0, #0x21
    bgt .L_021ecff2
    bge .L_021ed010
    cmp r0, #0x15
    bgt .L_021ecfec
    add r1, r0, #0x0
    sub r1, #0x10
    bmi .L_021ed028
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0022
    .hword 0x0046
    .hword 0x003a
.L_021ecfec:
    cmp r0, #0x20
    beq .L_021ed010
    b .L_021ed028
.L_021ecff2:
    cmp r0, #0x23
    bgt .L_021ecffe
    bge .L_021ed010
    cmp r0, #0x22
    beq .L_021ed010
    b .L_021ed028
.L_021ecffe:
    cmp r0, #0x25
    beq .L_021ed01c
    b .L_021ed028
    cmp r4, #0x5
    bls .L_021ed028
    mov r0, #0x0
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ed010:
    cmp r4, #0xd
    bls .L_021ed028
    mov r0, #0x0
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ed01c:
    cmp r4, #0x21
    bls .L_021ed028
    mov r0, #0x0
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ed028:
    cmp r0, #0x21
    bgt .L_021ed056
    bge .L_021ed076
    cmp r0, #0x15
    bgt .L_021ed050
    add r1, r0, #0x0
    sub r1, #0x10
    bmi .L_021ed0c0
    add r1, r1, r1
    add r1, pc
    ldrh r1, [r1, #0x6]
    lsl r1, r1, #0x10
    asr r1, r1, #0x10
    add pc, r1
    .hword 0x0022
    .hword 0x0030
    .hword 0x003e
    .hword 0x004c
    .hword 0x007a
    .hword 0x005a
.L_021ed050:
    cmp r0, #0x20
    beq .L_021ed068
    b .L_021ed0c0
.L_021ed056:
    cmp r0, #0x23
    bgt .L_021ed062
    bge .L_021ed092
    cmp r0, #0x22
    beq .L_021ed084
    b .L_021ed0c0
.L_021ed062:
    cmp r0, #0x25
    beq .L_021ed0a0
    b .L_021ed0c0
.L_021ed068:
    add r0, r7, #0x0
    add r1, r5, #0x6
    add r2, r4, #0x0
    bl native_fn_021edb9c
    str r4, [r6, #0x4]
    b .L_021ed0c8
.L_021ed076:
    ldr r0, [sp]
    add r1, r5, #0x6
    add r2, r4, #0x0
    bl native_fn_021edb9c
    str r4, [r6, #0x4]
    b .L_021ed0c8
.L_021ed084:
    ldr r0, [sp, #0x4]
    add r1, r5, #0x6
    add r2, r4, #0x0
    bl native_fn_021edb9c
    str r4, [r6, #0x4]
    b .L_021ed0c8
.L_021ed092:
    ldr r0, [sp, #0x8]
    add r1, r5, #0x6
    add r2, r4, #0x0
    bl native_fn_021edb9c
    str r4, [r6, #0x4]
    b .L_021ed0c8
.L_021ed0a0:
    cmp r4, #0x0
    beq .L_021ed0b4
    add r0, r5, r4
    ldrb r0, [r0, #0x5]
    cmp r0, #0x0
    beq .L_021ed0b4
    mov r0, #0x0
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ed0b4:
    ldr r0, [sp, #0xc]
    add r1, r5, #0x6
    add r2, r4, #0x0
    bl native_fn_021edb9c
    b .L_021ed0c8
.L_021ed0c0:
    mov r0, #0x0
    add sp, #0x14
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ed0c8:
    ldrh r0, [r5, #0x4]
    cmp r0, #0x0
    beq .L_021ed0d8
    bl native_fn_021edcb8
    ldr r1, [sp, #0x10]
    add r5, r1, r0
    b .L_021ecfba
.L_021ed0d8:
    mov r0, #0x0
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
.size native_ov006_021ecf8c, .-native_ov006_021ecf8c
