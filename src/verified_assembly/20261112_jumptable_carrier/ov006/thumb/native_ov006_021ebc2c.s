/* ov006 row 0x021ebc2c: 2584 bytes.
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
.extern native_fn_021ec688
.extern native_fn_021ec6e0
.extern native_fn_021ec65c
.extern native_fn_021eca04
.extern native_fn_021ebb2c
.extern native_fn_021edfe4
.extern native_fn_021ec914
.extern native_fn_021ee32c
.extern native_fn_021ec990
.extern native_fn_021ebb1c
.extern native_fn_021ee15c
.extern native_fn_021edb00
.extern native_fn_021ec9d4
.extern native_fn_021edc34
.extern native_fn_021edc30
.extern native_fn_021edc50
.extern native_fn_021edc78
.extern native_fn_021edc3c
.extern native_fn_02026144
.extern native_data_02208884
.extern native_data_0220d3dc
.extern native_fn_021edc48
.extern native_fn_021edb58
.extern native_fn_021ec644
.extern native_fn_021ed2e8
.extern native_fn_021edd54
.extern native_fn_021edd60
.extern native_fn_021edbcc
.extern native_fn_021edbb8
.extern native_fn_021edcb8
.extern native_fn_021eca30
.extern native_fn_021ec6ec
.extern native_fn_021ec6f8
.global native_ov006_021ebc2c
.type native_ov006_021ebc2c, @function
native_ov006_021ebc2c:
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0xc8
    ldr r1, .L_pool_021ebf80
    str r0, [sp, #0x8]
    ldrh r2, [r1, #0]
    ldrh r1, [r1, #0x2]
    add r0, sp, #0x2c
    strh r2, [r0, #0x30]
    strh r1, [r0, #0x32]
    mov r0, #0x0
    add r1, sp, #0x58
    strh r0, [r1, #0]
    str r0, [sp, #0x24]
    strh r0, [r1, #0x2]
    mov r0, #0x1
    str r0, [sp, #0x54]
    ldr r0, [sp, #0x24]
    ldr r1, [sp, #0x24]
    str r0, [sp, #0x50]
    str r0, [sp, #0x1c]
    add r0, sp, #0xb0
    mov r2, #0x18
    bl native_fn_021edbac
    ldr r1, .L_pool_021ebf84
    ldr r0, [sp, #0x8]
    ldrsh r0, [r0, r1]
    add r1, sp, #0x2c
    strh r0, [r1, #0x30]
    mov r0, #0x30
    ldrsh r2, [r1, r0]
    sub r0, #0x31
    cmp r2, r0
    bne .L_021ebc74
    mov r0, #0xa
    strh r0, [r1, #0x30]
.L_021ebc74:
    ldr r1, .L_pool_021ebf88
    ldr r0, [sp, #0x8]
    ldrsh r0, [r0, r1]
    add r1, sp, #0x2c
    strh r0, [r1, #0x2c]
    mov r0, #0x2c
    ldrsh r2, [r1, r0]
    sub r0, #0x2d
    cmp r2, r0
    bne .L_021ebc8c
    mov r0, #0xa
    strh r0, [r1, #0x2c]
.L_021ebc8c:
    mov r1, #0x42
    ldr r0, [sp, #0x8]
    lsl r1, r1, #0x2
    ldrsh r0, [r0, r1]
    add r1, sp, #0x2c
    strh r0, [r1, #0x32]
    mov r0, #0x32
    ldrsh r2, [r1, r0]
    sub r0, #0x33
    cmp r2, r0
    bne .L_021ebca6
    mov r0, #0x64
    strh r0, [r1, #0x32]
.L_021ebca6:
    mov r1, #0x43
    ldr r0, [sp, #0x8]
    lsl r1, r1, #0x2
    ldrsh r0, [r0, r1]
    add r1, sp, #0x2c
    strh r0, [r1, #0x2e]
    mov r0, #0x2e
    ldrsh r2, [r1, r0]
    sub r0, #0x2f
    cmp r2, r0
    bne .L_021ebcc0
    mov r0, #0x64
    strh r0, [r1, #0x2e]
.L_021ebcc0:
    ldr r1, .L_pool_021ebf8c
    ldr r0, [sp, #0x8]
    ldrsh r0, [r0, r1]
    mov r1, #0x0
    mvn r1, r1
    str r0, [sp, #0xc]
    cmp r0, r1
    bne .L_021ebcd6
    mov r0, #0x7d
    lsl r0, r0, #0x4
    str r0, [sp, #0xc]
.L_021ebcd6:
    ldr r0, [sp, #0x8]
    bl native_fn_021ec688
    ldr r0, .L_pool_021ebf90
    ldr r1, [r0, #0x2c]
    mov r0, #0x1
    and r0, r1
    cmp r0, #0x1
    beq .L_021ebd02
    mov r0, #0x13
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebd02:
    mov r4, #0x0
    add r0, r4, #0x0
    bl native_fn_021eca04
    add r1, sp, #0x2c
    mov r0, #0x32
    ldrsh r6, [r1, r0]
    mov r0, #0x30
    ldrsh r7, [r1, r0]
    ldr r5, .L_pool_021ebf90
.L_021ebd16:
    ldr r0, [r5, #0x4]
    cmp r0, #0x0
    beq .L_021ebd24
    bl native_fn_021ebb2c
    mov r0, #0x0
    str r0, [r5, #0x4]
.L_021ebd24:
    ldr r0, .L_pool_021ebf98
    bl native_fn_021edfe4
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne .L_021ebd46
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebd46:
    ldr r0, [r5, #0x4]
    bl native_fn_021ec914
    cmp r0, #0x4
    bne .L_021ebd64
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0x2
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebd64:
    cmp r0, #0x0
    beq .L_021ebd8e
    cmp r4, r7
    blt .L_021ebd80
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0x1
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebd80:
    add r0, r6, #0x0
    bl native_fn_021ee32c
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    b .L_021ebd16
.L_021ebd8e:
    mov r0, #0x1
    bl native_fn_021eca04
    add r0, sp, #0x74
    mov r1, #0x0
    mov r2, #0x3c
    bl native_fn_021edbac
    add r0, sp, #0x74
    bl native_fn_021ec990
    cmp r0, #0x0
    beq .L_021ebdbc
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebdbc:
    mov r0, #0x58
    bl native_fn_021ebb1c
    ldr r1, .L_pool_021ebf90
    cmp r0, #0x0
    str r0, [r1, #0xc]
    bne .L_021ebdde
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebdde:
    mov r1, #0x0
    mov r2, #0x58
    bl native_fn_021edbac
    add r1, sp, #0x2c
    mov r0, #0x30
    ldrsh r5, [r1, r0]
    mov r4, #0x0
    cmp r5, #0x0
    ble .L_021ebe36
    ldr r7, .L_pool_021ebf90
.L_021ebdf4:
    ldr r1, [r7, #0xc]
    add r0, sp, #0x74
    bl native_fn_021ee15c
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne .L_021ebe18
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebe18:
    cmp r0, #0x0
    bne .L_021ebe26
    bne .L_021ebe36
    ldr r0, [r7, #0xc]
    ldr r0, [r0, #0]
    cmp r0, #0x1
    beq .L_021ebe36
.L_021ebe26:
    add r0, r6, #0x0
    bl native_fn_021ee32c
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    cmp r4, r5
    blt .L_021ebdf4
.L_021ebe36:
    add r0, sp, #0x2c
    mov r1, #0x30
    ldrsh r0, [r0, r1]
    cmp r4, r0
    bne .L_021ebe54
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    add r1, #0xe6
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebe54:
    ldr r0, .L_pool_021ebf9c
    mov r1, #0xff
    mvn r1, r1
    add r2, r0, #0x0
    bl native_fn_021edb00
    cmp r0, #0x0
    beq .L_021ebe7e
    mov r0, #0xc
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebe7e:
    bl native_fn_021ec65c
    mov r3, #0x11
    ldr r2, [sp, #0x8]
    lsl r3, r3, #0x4
    mov r0, #0x3
    add r1, sp, #0xb0
    add r2, r2, r3
    bl native_fn_021ec9d4
    mov r0, #0x2
    add r1, r0, #0x0
    mov r2, #0x0
    bl native_fn_021edc34
    ldr r1, .L_pool_021ebfa0
    cmp r0, #0x0
    str r0, [r1, #0]
    bge .L_021ebeb8
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebeb8:
    mov r1, #0x4
    str r1, [sp]
    ldr r1, .L_pool_021ebfa4
    mov r2, #0x1
    add r3, sp, #0x54
    bl native_fn_021edc30
    cmp r0, #0x0
    bge .L_021ebee4
    mov r0, #0xb
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebee4:
    add r0, sp, #0x2c
    mov r1, #0x0
    mov r2, #0x8
    bl native_fn_021edbac
    mov r1, #0x2
    add r0, sp, #0x2c
    strb r1, [r0, #0x1]
    ldr r0, .L_pool_021ebf9c
    bl native_fn_021edc50
    str r0, [sp, #0x30]
    ldr r0, .L_pool_021ebfa8
    bl native_fn_021edc78
    add r1, sp, #0x2c
    strh r0, [r1, #0x2]
    ldr r0, .L_pool_021ebfa0
    add r1, sp, #0x2c
    ldr r0, [r0, #0]
    mov r2, #0x8
    bl native_fn_021edc3c
    cmp r0, #0x0
    bge .L_021ebf2a
    ldr r1, .L_pool_021ebf94
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebf2a:
    ldr r0, .L_pool_021ebf90
    mov r1, #0x0
    ldr r0, [r0, #0x14]
    mov r2, #0x14
    str r0, [sp, #0x18]
    add r0, sp, #0x60
    bl native_fn_021edbac
    ldr r0, .L_pool_021ebf9c
    mov r1, #0xfa
    str r0, [sp, #0x70]
    sub r0, #0x64
    str r0, [sp, #0x60]
    ldr r0, [sp, #0xc]
    lsl r1, r1, #0x2
    blx native_fn_02026144
    str r0, [sp, #0x14]
    mov r1, #0xfa
    ldr r0, [sp, #0xc]
    lsl r1, r1, #0x2
    blx native_fn_02026144
    mov r0, #0xfa
    lsl r0, r0, #0x2
    mul r0, r1
    str r0, [sp, #0x10]
    mov r1, #0x30
    add r0, sp, #0x2c
    ldrsh r7, [r0, r1]
    ldr r5, .L_pool_021ebf90
.L_021ebf68:
    ldr r0, [sp, #0x24]
    cmp r0, #0x1
    bne .L_021ebf78
    ldr r1, .L_pool_021ebfac
    mov r0, #0x1c
    ldrsb r0, [r1, r0]
    cmp r0, #0x1
    bne .L_021ebf7a
.L_021ebf78:
    b .L_021ec1f4
.L_021ebf7a:
    ldr r0, .L_pool_021ebfa0
    b .L_021ebfb0
    mov r8, r8
.L_pool_021ebf80:
    .word native_data_02208884
.L_pool_021ebf84:
    .word 0x00000106
.L_pool_021ebf88:
    .word 0x0000010a
.L_pool_021ebf8c:
    .word 0x0000010e
.L_pool_021ebf90:
    .word 0x02219b4c
.L_pool_021ebf94:
    .word 0x00000116
.L_pool_021ebf98:
    .word 0x02219b50
.L_pool_021ebf9c:
    .word 0xc0a80b65
.L_pool_021ebfa0:
    .word native_data_0220d3dc
.L_pool_021ebfa4:
    .word 0x0000ffff
.L_pool_021ebfa8:
    .word 0x00005790
.L_pool_021ebfac:
    .word 0x02219b6c
.L_021ebfb0:
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    cmp r0, r1
    beq .L_021ebfbe
    bl native_fn_021edc48
.L_021ebfbe:
    mov r1, #0x0
    ldr r0, .L_pool_021ec2f0
    mvn r1, r1
    str r1, [r0, #0]
    bl native_fn_021edb58
    cmp r0, #0x0
    beq .L_021ebfe2
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ebfe2:
    mov r0, #0x58
    bl native_fn_021ebb1c
    str r0, [r5, #0x4]
    cmp r0, #0x0
    bne .L_021ec002
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec002:
    ldr r0, [r5, #0x4]
    cmp r0, #0x0
    beq .L_021ec010
    bl native_fn_021ebb2c
    mov r0, #0x0
    str r0, [r5, #0x4]
.L_021ec010:
    ldr r0, .L_pool_021ec2f8
    bl native_fn_021edfe4
    mov r1, #0x0
    mvn r1, r1
    str r0, [sp, #0x28]
    cmp r0, r1
    bne .L_021ec034
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec034:
    ldr r0, [r5, #0x4]
    bl native_fn_021ec914
    cmp r0, #0x4
    bne .L_021ec052
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0x2
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec052:
    cmp r0, #0x0
    beq .L_021ec07c
    cmp r4, r7
    blt .L_021ec06e
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0x1
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec06e:
    add r0, r6, #0x0
    bl native_fn_021ee32c
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    b .L_021ec002
.L_021ec07c:
    mov r0, #0x0
    ldr r1, [sp, #0x28]
    mvn r0, r0
    cmp r1, r0
    bne .L_021ec09a
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec09a:
    mov r0, #0x58
    bl native_fn_021ebb1c
    str r0, [r5, #0xc]
    cmp r0, #0x0
    bne .L_021ec0ba
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec0ba:
    mov r1, #0x0
    mov r2, #0x58
    bl native_fn_021edbac
    mov r4, #0x0
    cmp r7, #0x0
    ble .L_021ec10a
.L_021ec0c8:
    ldr r1, [r5, #0xc]
    add r0, sp, #0x74
    bl native_fn_021ee15c
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne .L_021ec0ec
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec0ec:
    cmp r0, #0x0
    bne .L_021ec0fa
    bne .L_021ec10a
    ldr r0, [r5, #0xc]
    ldr r0, [r0, #0]
    cmp r0, #0x1
    beq .L_021ec10a
.L_021ec0fa:
    add r0, r6, #0x0
    bl native_fn_021ee32c
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    cmp r4, r7
    blt .L_021ec0c8
.L_021ec10a:
    cmp r4, r7
    bne .L_021ec122
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec122:
    ldr r0, [r5, #0x34]
    ldr r1, [r5, #0x38]
    bl native_fn_021ec644
    ldr r1, [r5, #0x38]
    add r2, r0, #0x0
    str r0, [sp, #0x1c]
    bl native_fn_021edb00
    cmp r0, #0x0
    beq .L_021ec152
    mov r0, #0xc
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec152:
    ldr r0, .L_pool_021ec2fc
    mov r1, #0x1
    strb r1, [r0, #0x1c]
    bl native_fn_021ec65c
    mov r0, #0x2
    add r1, r0, #0x0
    mov r2, #0x0
    bl native_fn_021edc34
    ldr r1, .L_pool_021ec2f0
    cmp r0, #0x0
    str r0, [r1, #0]
    bge .L_021ec182
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec182:
    mov r1, #0x4
    str r1, [sp]
    ldr r1, .L_pool_021ec300
    mov r2, #0x1
    add r3, sp, #0x54
    bl native_fn_021edc30
    cmp r0, #0x0
    bge .L_021ec1ae
    mov r0, #0xb
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec1ae:
    add r0, sp, #0x2c
    mov r1, #0x0
    mov r2, #0x8
    bl native_fn_021edbac
    mov r1, #0x2
    add r0, sp, #0x2c
    strb r1, [r0, #0x1]
    ldr r0, [sp, #0x1c]
    bl native_fn_021edc50
    str r0, [sp, #0x30]
    ldr r0, .L_pool_021ec304
    bl native_fn_021edc78
    add r1, sp, #0x2c
    strh r0, [r1, #0x2]
    ldr r0, .L_pool_021ec2f0
    add r1, sp, #0x2c
    ldr r0, [r0, #0]
    mov r2, #0x8
    bl native_fn_021edc3c
    cmp r0, #0x0
    bge .L_021ec1f4
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec1f4:
    ldr r3, .L_pool_021ec2f0
    ldr r0, [sp, #0x24]
    ldr r3, [r3, #0]
    add r1, sp, #0x60
    add r2, sp, #0xb0
    bl native_fn_021ed2e8
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne .L_021ec22a
    mov r1, #0x1
    ldr r0, [sp, #0x24]
    lsl r1, r1, #0xc
    add r0, r0, r1
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ec2f4
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec22a:
    ldr r0, [sp, #0x18]
    ldr r2, .L_pool_021ec308
    mov r1, #0x0
    bl native_fn_021edbac
    add r0, sp, #0x3c
    bl native_fn_021edd54
    ldr r0, .L_pool_021ec2f0
    add r1, sp, #0x3c
    ldr r0, [r0, #0]
    bl native_fn_021edd60
    ldr r0, [sp, #0x14]
    mov r2, #0x0
    str r0, [sp, #0x34]
    ldr r0, [sp, #0x10]
    add r1, sp, #0x3c
    str r0, [sp, #0x38]
    add r0, sp, #0x34
    str r0, [sp]
    ldr r0, .L_pool_021ec2f0
    add r3, r2, #0x0
    ldr r0, [r0, #0]
    add r0, r0, #0x1
    bl native_fn_021edbcc
    cmp r0, #0x0
    bgt .L_021ec2a4
    ldr r0, [sp, #0x50]
    add r1, sp, #0x2c
    add r2, r0, #0x1
    str r2, [sp, #0x50]
    mov r0, #0x2c
    ldrsh r0, [r1, r0]
    cmp r2, r0
    ble .L_021ec29a
    ldr r0, [sp, #0x24]
    cmp r0, #0x0
    bne .L_021ec282
    mov r0, #0xf
    bl native_fn_021ec6e0
    b .L_021ec294
.L_021ec282:
    cmp r0, #0x1
    bne .L_021ec28e
    mov r0, #0x10
    bl native_fn_021ec6e0
    b .L_021ec294
.L_021ec28e:
    mov r0, #0x11
    bl native_fn_021ec6e0
.L_021ec294:
    mov r5, #0x0
    mvn r5, r5
    b .L_021ec582
.L_021ec29a:
    mov r0, #0x2e
    ldrsh r0, [r1, r0]
    bl native_fn_021ee32c
    b .L_021ebf68
.L_021ec2a4:
    mov r0, #0x8
    str r0, [sp, #0x44]
    add r0, sp, #0x48
    str r0, [sp]
    add r0, sp, #0x44
    str r0, [sp, #0x4]
    ldr r0, .L_pool_021ec2f0
    ldr r1, [sp, #0x18]
    ldr r0, [r0, #0]
    ldr r2, .L_pool_021ec30c
    add r1, #0xc
    mov r3, #0x0
    bl native_fn_021edbb8
    ldr r1, .L_pool_021ec2f0
    lsl r0, r0, #0x10
    ldr r2, [r1, #0]
    ldr r1, [sp, #0x18]
    lsr r0, r0, #0x10
    str r2, [r1, #0]
    bl native_fn_021edcb8
    ldr r1, [sp, #0x18]
    add r2, sp, #0x50
    str r0, [r1, #0x4]
    ldr r0, .L_pool_021ec2f0
    add r3, sp, #0xb0
    ldr r0, [r0, #0]
    str r0, [sp]
    ldr r0, [sp, #0x24]
    bl native_fn_021eca30
    str r0, [sp, #0x20]
    cmp r0, #0x64
    bne .L_021ec310
    mov r5, #0x0
    b .L_021ec582
    mov r8, r8
.L_pool_021ec2f0:
    .word native_data_0220d3dc
.L_pool_021ec2f4:
    .word 0x00000116
.L_pool_021ec2f8:
    .word 0x02219b50
.L_pool_021ec2fc:
    .word 0x02219b6c
.L_pool_021ec300:
    .word 0x0000ffff
.L_pool_021ec304:
    .word 0x00005790
.L_pool_021ec308:
    .word 0x000005f8
.L_pool_021ec30c:
    .word 0x000005dc
.L_021ec310:
    mov r5, #0x0
    mvn r5, r5
    cmp r0, r5
    bne .L_021ec31a
    b .L_021ec582
.L_021ec31a:
    ldr r1, [sp, #0x24]
    cmp r1, r0
    bne .L_021ec322
    b .L_021ec544
.L_021ec322:
    cmp r0, #0x2
    beq .L_021ec328
    b .L_021ec53e
.L_021ec328:
    ldr r0, .L_pool_021ec62c
    ldr r0, [r0, #0]
    cmp r0, r5
    beq .L_021ec334
    bl native_fn_021edc48
.L_021ec334:
    mov r1, #0x0
    ldr r0, .L_pool_021ec62c
    mvn r1, r1
    str r1, [r0, #0]
    bl native_fn_021edb58
    cmp r0, #0x0
    beq .L_021ec358
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec358:
    mov r0, #0x4
    mov r4, #0x0
    bl native_fn_021eca04
    add r1, sp, #0x2c
    mov r0, #0x30
    ldrsh r7, [r1, r0]
    ldr r5, .L_pool_021ec634
.L_021ec368:
    ldr r0, [r5, #0x4]
    cmp r0, #0x0
    beq .L_021ec376
    bl native_fn_021ebb2c
    mov r0, #0x0
    str r0, [r5, #0x4]
.L_021ec376:
    ldr r0, .L_pool_021ec638
    bl native_fn_021edfe4
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne .L_021ec398
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec398:
    ldr r0, [r5, #0x4]
    bl native_fn_021ec914
    cmp r0, #0x4
    bne .L_021ec3b6
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0x2
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec3b6:
    cmp r0, #0x0
    beq .L_021ec3e0
    cmp r4, r7
    blt .L_021ec3d2
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0x1
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec3d2:
    add r0, r6, #0x0
    bl native_fn_021ee32c
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    b .L_021ec368
.L_021ec3e0:
    mov r0, #0x58
    bl native_fn_021ebb1c
    ldr r1, .L_pool_021ec634
    cmp r0, #0x0
    str r0, [r1, #0xc]
    bne .L_021ec402
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec402:
    mov r1, #0x0
    mov r2, #0x58
    bl native_fn_021edbac
    add r1, sp, #0x2c
    mov r0, #0x30
    ldrsh r5, [r1, r0]
    mov r4, #0x0
    cmp r5, #0x0
    ble .L_021ec45a
    ldr r7, .L_pool_021ec634
.L_021ec418:
    ldr r1, [r7, #0xc]
    add r0, sp, #0x74
    bl native_fn_021ee15c
    mov r1, #0x0
    mvn r1, r1
    cmp r0, r1
    bne .L_021ec43c
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec43c:
    cmp r0, #0x0
    bne .L_021ec44a
    bne .L_021ec45a
    ldr r0, [r7, #0xc]
    ldr r0, [r0, #0]
    cmp r0, #0x1
    beq .L_021ec45a
.L_021ec44a:
    add r0, r6, #0x0
    bl native_fn_021ee32c
    add r0, r4, #0x1
    lsl r0, r0, #0x10
    asr r4, r0, #0x10
    cmp r4, r5
    blt .L_021ec418
.L_021ec45a:
    add r0, sp, #0x2c
    mov r1, #0x30
    ldrsh r0, [r0, r1]
    cmp r4, r0
    bne .L_021ec478
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    add r1, #0xe6
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec478:
    ldr r1, .L_pool_021ec634
    ldr r0, [sp, #0x1c]
    ldr r1, [r1, #0x38]
    add r2, r0, #0x0
    bl native_fn_021edb00
    cmp r0, #0x0
    beq .L_021ec4a2
    mov r0, #0xc
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec4a2:
    bl native_fn_021ec65c
    mov r0, #0x2
    add r1, r0, #0x0
    mov r2, #0x0
    bl native_fn_021edc34
    ldr r1, .L_pool_021ec62c
    cmp r0, #0x0
    str r0, [r1, #0]
    bge .L_021ec4cc
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec4cc:
    mov r1, #0x4
    str r1, [sp]
    ldr r1, .L_pool_021ec63c
    mov r2, #0x1
    add r3, sp, #0x54
    bl native_fn_021edc30
    cmp r0, #0x0
    bge .L_021ec4f8
    mov r0, #0xb
    bl native_fn_021ec6e0
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec4f8:
    add r0, sp, #0x2c
    mov r1, #0x0
    mov r2, #0x8
    bl native_fn_021edbac
    mov r1, #0x2
    add r0, sp, #0x2c
    strb r1, [r0, #0x1]
    ldr r0, [sp, #0x1c]
    bl native_fn_021edc50
    str r0, [sp, #0x30]
    ldr r0, .L_pool_021ec640
    bl native_fn_021edc78
    add r1, sp, #0x2c
    strh r0, [r1, #0x2]
    ldr r0, .L_pool_021ec62c
    add r1, sp, #0x2c
    ldr r0, [r0, #0]
    mov r2, #0x8
    bl native_fn_021edc3c
    cmp r0, #0x0
    bge .L_021ec53e
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec53e:
    ldr r0, [sp, #0x20]
    str r0, [sp, #0x24]
    b .L_021ebf2a
.L_021ec544:
    str r0, [sp, #0x24]
    add r1, sp, #0x2c
    mov r0, #0x2c
    ldrsh r0, [r1, r0]
    ldr r2, [sp, #0x50]
    cmp r2, r0
    ble .L_021ec578
    ldr r0, [sp, #0x20]
    cmp r0, #0x0
    bne .L_021ec560
    mov r0, #0xf
    bl native_fn_021ec6e0
    b .L_021ec572
.L_021ec560:
    cmp r0, #0x1
    bne .L_021ec56c
    mov r0, #0x10
    bl native_fn_021ec6e0
    b .L_021ec572
.L_021ec56c:
    mov r0, #0x11
    bl native_fn_021ec6e0
.L_021ec572:
    mov r5, #0x0
    mvn r5, r5
    b .L_021ec582
.L_021ec578:
    mov r0, #0x2e
    ldrsh r0, [r1, r0]
    bl native_fn_021ee32c
    b .L_021ebf2a
.L_021ec582:
    ldr r0, .L_pool_021ec62c
    mov r1, #0x0
    ldr r0, [r0, #0]
    mvn r1, r1
    cmp r0, r1
    beq .L_021ec592
    bl native_fn_021edc48
.L_021ec592:
    mov r1, #0x0
    ldr r0, .L_pool_021ec62c
    mvn r1, r1
    str r1, [r0, #0]
    bl native_fn_021edb58
    cmp r0, #0x0
    beq .L_021ec5b6
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0xf
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec5b6:
    cmp r5, #0x0
    beq .L_021ec606
    bl native_fn_021ec6ec
    sub r0, #0xf
    cmp r0, #0x6
    bhi .L_021ec5f2
    add r0, r0, r0
    add r0, pc
    ldrh r0, [r0, #0x6]
    lsl r0, r0, #0x10
    asr r0, r0, #0x10
    add pc, r0
    .hword 0x000c
    .hword 0x0010
    .hword 0x0014
    .hword 0x0020
    .hword 0x0020
    .hword 0x0018
    .hword 0x001c
    mov r2, #0x3
    b .L_021ec5f4
    mov r2, #0x4
    b .L_021ec5f4
    mov r2, #0x5
    b .L_021ec5f4
    mov r2, #0x7
    b .L_021ec5f4
    mov r2, #0x8
    b .L_021ec5f4
.L_021ec5f2:
    mov r2, #0xf
.L_021ec5f4:
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec606:
    ldr r0, [sp, #0x8]
    bl native_fn_021ec6f8
    cmp r0, #0x0
    beq .L_021ec624
    ldr r1, .L_pool_021ec630
    ldr r0, [sp, #0x8]
    mov r2, #0x6
    strb r2, [r0, r1]
    bl native_fn_021ec65c
    mov r0, #0x0
    add sp, #0xc8
    mvn r0, r0
    pop {r3, r4, r5, r6, r7, pc}
.L_021ec624:
    mov r0, #0x0
    add sp, #0xc8
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
.L_pool_021ec62c:
    .word native_data_0220d3dc
.L_pool_021ec630:
    .word 0x00000116
.L_pool_021ec634:
    .word 0x02219b4c
.L_pool_021ec638:
    .word 0x02219b50
.L_pool_021ec63c:
    .word 0x0000ffff
.L_pool_021ec640:
    .word 0x00005790
.size native_ov006_021ebc2c, .-native_ov006_021ebc2c
