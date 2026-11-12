/* ov006 row 0x021fa7f8: 392 bytes.
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
.extern native_fn_021fe6c4
.extern native_fn_021f2a4c
.extern native_fn_021fe6b8
.extern native_fn_02026144
.extern native_fn_021fabe4
.extern native_fn_021ff6d4
.extern native_fn_020024bc
.extern native_fn_021fb550
.extern native_fn_0220490c
.extern native_fn_021fb39c
.extern native_fn_021fb414
.global native_ov006_021fa7f8
.type native_ov006_021fa7f8, @function
native_ov006_021fa7f8:
    push {r3, lr}
    ldr r0, .L_pool_021fa974
    ldr r0, [r0, #0x8]
    ldr r1, [r0, #0x38]
    cmp r1, #0x0
    beq .L_021fa806
    b .L_021fa970
.L_021fa806:
    add r1, r0, #0x0
    add r1, #0x41
    ldrb r1, [r1, #0]
    cmp r1, #0x0
    beq .L_021fa81c
    add r1, r0, #0x0
    add r1, #0x41
    ldrb r1, [r1, #0]
    add r0, #0x41
    sub r1, r1, #0x1
    strb r1, [r0, #0]
.L_021fa81c:
    bl native_fn_021fe6c4
    cmp r0, #0x7
    bhi .L_021fa858
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x013e
    .hword 0x000e
    .hword 0x001a
    .hword 0x0050
    .hword 0x00b8
    .hword 0x0134
    .hword 0x00f6
    .hword 0x0134
    ldr r0, .L_pool_021fa974
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x45
    strb r1, [r0, #0]
    pop {r3, pc}
    ldr r0, .L_pool_021fa974
    ldr r0, [r0, #0x8]
    add r0, #0x41
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    beq .L_021fa85a
.L_021fa858:
    b .L_021fa970
.L_021fa85a:
    bl native_fn_021f2a4c
    bl native_fn_021fe6b8
    mov r1, #0x91
    mul r1, r0
    add r0, r1, #0x0
    mov r1, #0x37
    blx native_fn_02026144
    ldr r1, .L_pool_021fa974
    strh r0, [r1, #0x4]
    bl native_fn_021fabe4
    ldr r0, .L_pool_021fa974
    mov r1, #0x4
    ldr r0, [r0, #0x8]
    add r0, #0x41
    strb r1, [r0, #0]
    pop {r3, pc}
    ldr r0, .L_pool_021fa974
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x45
    strb r1, [r0, #0]
    bl native_fn_021fe6b8
    mov r1, #0x91
    mul r1, r0
    add r0, r1, #0x0
    mov r1, #0x37
    blx native_fn_02026144
    ldr r1, .L_pool_021fa974
    strh r0, [r1, #0x4]
    mov r0, #0x13
    bl native_fn_021ff6d4
    bl native_fn_021fabe4
    ldr r0, .L_pool_021fa974
    mov r1, #0x1d
    ldrh r0, [r0, #0x4]
    blx native_fn_020024bc
    cmp r0, #0x0
    bne .L_021fa8be
    bl native_fn_021fb550
    pop {r3, pc}
.L_021fa8be:
    cmp r0, #0x10
    bge .L_021fa8d6
    mov r0, #0x0
    ldr r1, .L_pool_021fa978
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021fa974
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, pc}
.L_021fa8d6:
    mov r0, #0x0
    ldr r1, .L_pool_021fa97c
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021fa974
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, pc}
    ldr r0, .L_pool_021fa974
    ldrh r1, [r0, #0x4]
    cmp r1, #0x0
    bne .L_021fa90e
    ldr r0, [r0, #0x8]
    add r0, #0x46
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021fa970
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021fa974
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x46
    strb r1, [r0, #0]
    pop {r3, pc}
.L_021fa90e:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021fa978
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021fa974
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, pc}
    ldr r0, .L_pool_021fa974
    ldrh r1, [r0, #0x4]
    cmp r1, #0x91
    bne .L_021fa94c
    ldr r0, [r0, #0x8]
    add r0, #0x46
    ldrb r0, [r0, #0]
    cmp r0, #0x0
    bne .L_021fa970
    mov r0, #0x9
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021fa974
    mov r1, #0x1
    ldr r0, [r0, #0x8]
    add r0, #0x46
    strb r1, [r0, #0]
    pop {r3, pc}
.L_021fa94c:
    mov r0, #0x13
    bl native_fn_021ff6d4
    mov r0, #0x0
    ldr r1, .L_pool_021fa97c
    add r2, r0, #0x0
    mov r3, #0x78
    bl native_fn_0220490c
    ldr r1, .L_pool_021fa974
    ldr r1, [r1, #0x8]
    str r0, [r1, #0x38]
    pop {r3, pc}
    ldr r0, .L_pool_021fa974
    mov r1, #0x0
    ldr r0, [r0, #0x8]
    add r0, #0x46
    strb r1, [r0, #0]
.L_021fa970:
    pop {r3, pc}
    mov r8, r8
.L_pool_021fa974:
    .word 0x0221c0ec
.L_pool_021fa978:
    .word native_fn_021fb39c+1
.L_pool_021fa97c:
    .word native_fn_021fb414+1
.size native_ov006_021fa7f8, .-native_ov006_021fa7f8
