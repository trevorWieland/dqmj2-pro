/* ov006 row 0x021edfe4: 376 bytes.
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
.extern native_fn_021ee6ac
.extern native_fn_02007c68
.extern native_fn_02007da4
.extern native_fn_02006eb8
.extern native_fn_021ee668
.extern native_fn_021ee79c
.extern native_fn_021edd68
.extern native_fn_02007e10
.extern native_fn_021ede3c
.global native_ov006_021edfe4
.type native_ov006_021edfe4, @function
native_ov006_021edfe4:
    push {r4, r5, r6, r7, lr}
    sub sp, #0x44
    str r0, [sp, #0x4]
    mov r0, #0x0
    mvn r0, r0
    str r0, [sp, #0x10]
    mov r0, #0x1
    str r0, [sp, #0xc]
    mov r6, #0x0
    ldr r0, .L_pool_021ee148
    add r7, r6, #0x0
    ldr r1, [r0, #0]
    add r5, r6, #0x0
    cmp r1, #0x0
    beq .L_021ee008
    ldr r0, [r0, #0xc]
    cmp r0, #0x0
    bne .L_021ee010
.L_021ee008:
    mov r0, #0x0
    add sp, #0x44
    mvn r0, r0
    pop {r4, r5, r6, r7, pc}
.L_021ee010:
    mov r0, #0x3
    lsl r0, r0, #0xc
    blx r1
    add r4, r0, #0x0
    bne .L_021ee020
    add sp, #0x44
    sub r0, r6, #0x1
    pop {r4, r5, r6, r7, pc}
.L_021ee020:
    add r0, r6, #0x0
    ldr r3, .L_pool_021ee14c
    add r1, r0, #0x0
    add r2, r0, #0x0
    str r4, [sp, #0x8]
    bl native_fn_021ee6ac
    cmp r0, #0x0
    bne .L_021ee034
    b .L_021ee138
.L_021ee034:
    add r0, sp, #0x18
    blx native_fn_02007c68
    mov r0, #0x13
    str r0, [sp]
    ldr r1, .L_pool_021ee150
    ldr r3, .L_pool_021ee154
    add r0, sp, #0x18
    add r2, r6, #0x0
    blx native_fn_02007da4
.L_021ee04a:
    ldr r0, .L_pool_021ee158
    add r1, sp, #0x14
    mov r2, #0x1
    blx native_fn_02006eb8
    ldr r0, [sp, #0x14]
    cmp r0, #0x13
    bhi .L_021ee11e
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x006c
    .hword 0x0044
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x006c
    .hword 0x00b6
    .hword 0x0066
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x00b6
    .hword 0x006c
    .hword 0x0026
    cmp r6, #0x0
    bne .L_021ee0d4
    cmp r5, #0x0
    beq .L_021ee0a0
    add r0, r4, #0x0
    mov r1, #0x40
    bl native_fn_021ee668
    add r7, r0, #0x0
.L_021ee0a0:
    bl native_fn_021ee79c
    cmp r0, #0x0
    beq .L_021ee11e
    mov r6, #0x1
    b .L_021ee0d4
    cmp r6, #0x0
    bne .L_021ee0d4
    cmp r5, #0x8
    bge .L_021ee0b8
    add r5, r5, #0x1
    b .L_021ee0d4
.L_021ee0b8:
    add r0, r4, #0x0
    mov r1, #0x40
    bl native_fn_021ee668
    add r7, r0, #0x0
    bl native_fn_021ee79c
    cmp r0, #0x0
    beq .L_021ee11e
    mov r6, #0x1
    b .L_021ee0d4
    mov r0, #0x0
    str r0, [sp, #0xc]
    str r0, [sp, #0x10]
.L_021ee0d4:
    ldr r0, [sp, #0xc]
    cmp r0, #0x0
    bne .L_021ee04a
    cmp r7, #0x0
    beq .L_021ee0f2
    sub r1, r7, #0x1
    mov r0, #0x54
    mul r0, r1
    ldr r1, .L_pool_021ee148
    add r0, #0x58
    ldr r1, [r1, #0]
    blx r1
    cmp r0, #0x0
    bne .L_021ee0fe
    b .L_021ee11e
.L_021ee0f2:
    ldr r1, .L_pool_021ee148
    mov r0, #0x58
    ldr r1, [r1, #0]
    blx r1
    cmp r0, #0x0
    beq .L_021ee11e
.L_021ee0fe:
    ldr r1, [sp, #0x4]
    mov r6, #0x0
    str r0, [r1, #0]
    str r7, [r0, #0]
    cmp r7, #0x0
    ble .L_021ee11e
    add r5, r0, #0x4
.L_021ee10c:
    add r0, r4, #0x0
    add r1, r5, #0x0
    bl native_fn_021edd68
    add r6, r6, #0x1
    add r4, #0xc0
    add r5, #0x54
    cmp r6, r7
    blt .L_021ee10c
.L_021ee11e:
    add r0, sp, #0x18
    blx native_fn_02007e10
    ldr r5, .L_pool_021ee158
    add r4, sp, #0x14
    mov r6, #0x0
.L_021ee12a:
    add r0, r5, #0x0
    add r1, r4, #0x0
    add r2, r6, #0x0
    blx native_fn_02006eb8
    cmp r0, #0x1
    beq .L_021ee12a
.L_021ee138:
    ldr r1, .L_pool_021ee148
    ldr r0, [sp, #0x8]
    ldr r1, [r1, #0xc]
    blx r1
    ldr r0, [sp, #0x10]
    add sp, #0x44
    pop {r4, r5, r6, r7, pc}
    mov r8, r8
.L_pool_021ee148:
    .word 0x0221a920
.L_pool_021ee14c:
    .word 0x0030bffe
.L_pool_021ee150:
    .word 0x003fec42
.L_pool_021ee154:
    .word native_fn_021ede3c+1
.L_pool_021ee158:
    .word 0x0221a940
.size native_ov006_021edfe4, .-native_ov006_021edfe4
