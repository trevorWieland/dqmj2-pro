/* ov006 row 0x021ee9a4: 780 bytes.
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
.extern native_fn_02089ef8
.extern native_fn_02089cf4
.extern native_fn_02089b64
.global native_ov006_021ee9a4
.type native_ov006_021ee9a4, @function
native_ov006_021ee9a4:
    push {r3, lr}
    cmp r0, #0x0
    bne .L_021ee9ac
    b .L_021eeca6
.L_021ee9ac:
    mov r1, #0x0
    ldrsh r2, [r0, r1]
    cmp r2, #0x9
    bls .L_021ee9b6
    b .L_021eec98
.L_021ee9b6:
    add r2, r2, r2
    add r2, pc
    ldrh r2, [r2, #0x6]
    lsl r2, r2, #0x10
    asr r2, r2, #0x10
    add pc, r2
    .hword 0x02d4
    .hword 0x0012
    .hword 0x0262
    .hword 0x0098
    .hword 0x0106
    .hword 0x00d0
    .hword 0x01ae
    .hword 0x029e
    .hword 0x02b4
    .hword 0x02c2
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021eea48
    ldr r2, .L_pool_021eeca8
    ldr r0, [r2, #0x2c]
    cmp r0, #0x4
    bne .L_021ee9f8
    mov r0, #0x3
    str r0, [r2, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eea8c
    mov r0, #0x6
    blx r2
    pop {r3, pc}
.L_021ee9f8:
    cmp r0, #0x6
    bne .L_021eea20
    ldr r0, [r2, #0x44]
    ldr r1, [r2, #0x48]
    ldr r2, [r2, #0x60]
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021eea8c
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eea8c
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eea20:
    cmp r0, #0x8
    bne .L_021eea8c
    ldr r0, [r2, #0x4c]
    ldr r1, [r2, #0x28]
    ldr r2, [r2, #0x58]
    bl native_fn_02089ef8
    cmp r0, #0x3
    beq .L_021eea8c
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eea8c
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eea48:
    ldr r0, .L_pool_021eeca8
    mov r3, #0x1
    str r3, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r3, [r0, #0]
    cmp r3, #0x0
    beq .L_021eea8c
    add r0, r2, #0x0
    blx r3
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021eea7e
    ldr r0, .L_pool_021eeca8
    ldr r2, [r0, #0x2c]
    cmp r2, #0x6
    bne .L_021eea8c
    mov r2, #0x5
    str r2, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eea8c
    mov r0, #0x8
    blx r2
    pop {r3, pc}
.L_021eea7e:
    ldr r0, .L_pool_021eeca8
    mov r2, #0x3
    str r2, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    bne .L_021eea8e
.L_021eea8c:
    b .L_021eeca6
.L_021eea8e:
    mov r0, #0x9
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021eeab6
    ldr r0, .L_pool_021eeca8
    ldr r2, [r0, #0x2c]
    cmp r2, #0x8
    bne .L_021eeb8e
    mov r2, #0x7
    str r2, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0xc
    blx r2
    pop {r3, pc}
.L_021eeab6:
    ldr r0, .L_pool_021eeca8
    mov r2, #0x3
    str r2, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0xd
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021eeb5e
    ldr r2, .L_pool_021eeca8
    ldr r0, [r2, #0x2c]
    cmp r0, #0x4
    bne .L_021eeaec
    mov r0, #0x3
    str r0, [r2, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0xa
    blx r2
    pop {r3, pc}
.L_021eeaec:
    cmp r0, #0x6
    bne .L_021eeb14
    ldr r0, [r2, #0x44]
    ldr r1, [r2, #0x48]
    ldr r2, [r2, #0x60]
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021eeb8e
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eeb14:
    cmp r0, #0x2
    bne .L_021eeb36
    bl native_fn_02089cf4
    cmp r0, #0x3
    beq .L_021eeb8e
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eeb36:
    cmp r0, #0x8
    bne .L_021eeb8e
    ldr r0, [r2, #0x4c]
    ldr r1, [r2, #0x28]
    ldr r2, [r2, #0x58]
    bl native_fn_02089ef8
    cmp r0, #0x3
    beq .L_021eeb8e
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eeb5e:
    ldr r0, .L_pool_021eeca8
    mov r2, #0x3
    str r2, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeb8e
    mov r0, #0xb
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021eec12
    ldr r2, .L_pool_021eeca8
    ldr r0, [r2, #0x2c]
    cmp r0, #0x4
    bne .L_021eeb96
    mov r0, #0x3
    str r0, [r2, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    bne .L_021eeb90
.L_021eeb8e:
    b .L_021eeca6
.L_021eeb90:
    mov r0, #0xe
    blx r2
    pop {r3, pc}
.L_021eeb96:
    cmp r0, #0x6
    bne .L_021eebbe
    ldr r0, [r2, #0x44]
    ldr r1, [r2, #0x48]
    ldr r2, [r2, #0x60]
    bl native_fn_02089d8c
    cmp r0, #0x3
    beq .L_021eeca6
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eebbe:
    cmp r0, #0x2
    bne .L_021eebe0
    bl native_fn_02089cf4
    cmp r0, #0x3
    beq .L_021eeca6
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eebe0:
    cmp r0, #0x8
    bne .L_021eec08
    ldr r0, [r2, #0x4c]
    ldr r1, [r2, #0x28]
    ldr r2, [r2, #0x58]
    bl native_fn_02089ef8
    cmp r0, #0x3
    beq .L_021eeca6
    ldr r0, .L_pool_021eeca8
    mov r1, #0x3
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x2
    mov r1, #0x0
    blx r2
    pop {r3, pc}
.L_021eec08:
    cmp r0, #0x7
    bne .L_021eeca6
    mov r0, #0x3
    str r0, [r2, #0x2c]
    pop {r3, pc}
.L_021eec12:
    ldr r0, .L_pool_021eeca8
    mov r2, #0x3
    str r2, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0xf
    blx r2
    pop {r3, pc}
    mov r2, #0x2
    ldrsh r0, [r0, r2]
    cmp r0, #0x0
    bne .L_021eec4e
    ldr r0, .L_pool_021eeca8
    ldr r0, [r0, #0x2c]
    cmp r0, #0x2
    bne .L_021eeca6
    bl native_fn_02089b64
    ldr r0, .L_pool_021eeca8
    mov r1, #0x0
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x14
    blx r2
    pop {r3, pc}
.L_021eec4e:
    ldr r0, .L_pool_021eeca8
    mov r3, #0x3
    str r3, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r3, [r0, #0]
    cmp r3, #0x0
    beq .L_021eeca6
    add r0, r2, #0x0
    blx r3
    pop {r3, pc}
    ldr r0, .L_pool_021eeca8
    ldr r0, [r0, #0x2c]
    cmp r0, #0x5
    bne .L_021eeca6
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x5
    blx r2
    pop {r3, pc}
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x4
    blx r2
    pop {r3, pc}
    ldr r0, .L_pool_021eeca8
    str r1, [r0, #0x2c]
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x3
    blx r2
    pop {r3, pc}
.L_021eec98:
    ldr r0, .L_pool_021eecac
    ldr r2, [r0, #0]
    cmp r2, #0x0
    beq .L_021eeca6
    mov r0, #0x1
    mov r1, #0x0
    blx r2
.L_021eeca6:
    pop {r3, pc}
.L_pool_021eeca8:
    .word 0x0221aad0
.L_pool_021eecac:
    .word 0x0221ab50
.size native_ov006_021ee9a4, .-native_ov006_021ee9a4
