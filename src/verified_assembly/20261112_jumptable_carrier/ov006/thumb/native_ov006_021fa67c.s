/* ov006 row 0x021fa67c: 260 bytes.
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
.extern native_fn_021fae50
.extern native_fn_021ff6d4
.extern native_fn_021fa780
.extern native_fn_021fa7d0
.extern native_fn_021fb7b0
.extern native_fn_021fb86c
.extern native_fn_02200344
.extern native_fn_021f52cc
.extern native_fn_021fb358
.extern native_fn_021faeb8
.extern native_fn_021fb080
.extern native_fn_021fe6e8
.extern native_fn_021fb8e8
.extern native_data_0220b7fc
.extern native_fn_021fa980
.global native_ov006_021fa67c
.type native_ov006_021fa67c, @function
native_ov006_021fa67c:
    push {r3, r4, lr}
    sub sp, #0x4
    add r4, r0, #0x0
    bl native_fn_021fae50
    cmp r0, #0x0
    bne .L_021fa694
    mov r0, #0x9
    bl native_fn_021ff6d4
    add sp, #0x4
    pop {r3, r4, pc}
.L_021fa694:
    cmp r4, #0x8
    bhi .L_021fa6e6
    add r0, r4, r4
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x0040
    .hword 0x0040
    .hword 0x0010
    .hword 0x0010
    .hword 0x0040
    .hword 0x0040
    .hword 0x0040
    .hword 0x0028
    .hword 0x0028
    mov r0, #0x6
    bl native_fn_021ff6d4
    sub r1, r4, #0x2
    mov r0, #0x1
    eor r1, r0
    bne .L_021fa6c6
    mov r0, #0x0
.L_021fa6c6:
    bl native_fn_021fa780
    add sp, #0x4
    pop {r3, r4, pc}
    mov r0, #0x6
    bl native_fn_021ff6d4
    sub r1, r4, #0x7
    mov r0, #0x1
    eor r1, r0
    bne .L_021fa6de
    mov r0, #0x0
.L_021fa6de:
    bl native_fn_021fa7d0
    add sp, #0x4
    pop {r3, r4, pc}
.L_021fa6e6:
    ldr r0, .L_pool_021fa770
    ldr r0, [r0, #0x8]
    add r0, #0x40
    strb r4, [r0, #0]
    add r0, r4, #0x0
    sub r0, #0xb
    cmp r0, #0x1
    bhi .L_021fa736
    bl native_fn_021fb7b0
    bl native_fn_021fb86c
    cmp r0, #0x0
    bne .L_021fa722
    mov r0, #0x9
    bl native_fn_021ff6d4
    mov r1, #0x1
    mov r0, #0x0
    str r0, [sp]
    mov r0, #0x6
    add r2, r1, #0x0
    sub r3, r1, #0x2
    bl native_fn_02200344
    ldr r0, .L_pool_021fa774
    bl native_fn_021f52cc
    add sp, #0x4
    pop {r3, r4, pc}
.L_021fa722:
    cmp r4, #0xb
    bne .L_021fa72e
    mov r0, #0x6
    bl native_fn_021ff6d4
    b .L_021fa762
.L_021fa72e:
    mov r0, #0xe
    bl native_fn_021ff6d4
    b .L_021fa762
.L_021fa736:
    cmp r4, #0xd
    bne .L_021fa746
    bl native_fn_021fb7b0
    mov r0, #0x7
    bl native_fn_021ff6d4
    b .L_021fa762
.L_021fa746:
    mov r0, #0x6
    bl native_fn_021ff6d4
    ldr r0, .L_pool_021fa778
    ldrb r0, [r0, r4]
    bl native_fn_021fb358
    add r2, r0, #0x0
    mov r0, #0x0
    mov r1, #0x1
    bl native_fn_021faeb8
    bl native_fn_021fb080
.L_021fa762:
    bl native_fn_021fe6e8
    ldr r0, .L_pool_021fa77c
    bl native_fn_021f52cc
    add sp, #0x4
    pop {r3, r4, pc}
.L_pool_021fa770:
    .word 0x0221c0ec
.L_pool_021fa774:
    .word native_fn_021fb8e8+1
.L_pool_021fa778:
    .word native_data_0220b7fc
.L_pool_021fa77c:
    .word native_fn_021fa980+1
.size native_ov006_021fa67c, .-native_ov006_021fa67c
