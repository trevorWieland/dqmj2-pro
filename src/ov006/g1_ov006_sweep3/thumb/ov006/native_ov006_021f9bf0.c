/* ov006 row 0x021f9bf0: 224 bytes.
 *
 * What it does: 105 instructions; 9 call(s) to 0x021f9c30, 0x021f9c3c, 0x021f9c22, +6 more; loops (back edge at +0x4a); returns through pop {r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0xd8 -> native_data_0220b688 (image word 0x0220b688)
 *   pool +0xdc -> constant 0x0221c0e4 (image word 0x0221c0e4)
 *   branch +0x2c -> +0x4c
 *   branch +0x38 -> +0x40
 *   branch +0x42 -> +0x4c
 *   back edge +0x4a -> +0x32
 *   back edge +0x52 -> +0x26
 *   branch +0x6e -> +0xc4
 *   branch +0x84 -> +0x98
 *   branch +0x90 -> +0xa8
 *   branch +0xa4 -> +0xa8
 *   back edge +0xac -> +0x82
 *   back edge +0xbc -> +0x7c
 *   branch +0xca -> +0xd2
 *   test +0x2a cmp r0, #0x20
 *   test +0x36 cmp r1, r0
 *   test +0x40 cmp r1, r0
 *   test +0x48 cmp r4, #0x3
 *   test +0x50 cmp r3, #0x4
 *   test +0x6a cmp r0, #0x1
 *   test +0x82 cmp r1, #0x0
 *   test +0x8e tst r3, r5
 *   test +0xa2 tst r3, r5
 *   test +0xaa cmp r2, #0x8
 *   test +0xba cmp r0, #0x4
 *   test +0xc8 cmp r0, #0x0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f9bf0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220b688[];
extern void native_fn_021ff5c4(void);
extern void native_fn_021f530c(void);
extern void native_fn_020a4990(void);


asm u32 native_ov006_021f9bf0 (register u32 a0)
{
    push {r4, r5, r6, r7, lr}
    sub sp, #0x14
    ldr r1, =native_data_0220b688
    mov r3, #0x0
    ldrb r2, [r1, #0]
    add r0, sp, #0x8
    add r5, r3, #0x0
    strb r2, [r0, #0x8]
    ldrb r2, [r1, #0x1]
    strb r2, [r0, #0x9]
    ldrb r2, [r1, #0x2]
    ldrb r1, [r1, #0x3]
    strb r2, [r0, #0xa]
    strb r1, [r0, #0xb]
    ldr r0, =0x0221c0e4
    ldr r0, [r0, #0]
    add r7, r0, #0x0
    str r0, [sp, #0x4]
    add r7, #0x8
ov006_021f9bf0_L26:
    ldrb r0, [r7, r5]
    add r2, r7, r5
    cmp r0, #0x20
    beq ov006_021f9bf0_L4c
    mov r4, #0x0
    add r6, sp, #0x10
ov006_021f9bf0_L32:
    ldrb r1, [r2, r4]
    ldrb r0, [r6, #0]
    cmp r1, r0
    bls ov006_021f9bf0_L40
    add sp, #0x14
    mov r0, #0x0
    pop {r4, r5, r6, r7, pc}
ov006_021f9bf0_L40:
    cmp r1, r0
    blo ov006_021f9bf0_L4c
    add r4, r4, #0x1
    add r6, r6, #0x1
    cmp r4, #0x3
    blt ov006_021f9bf0_L32
ov006_021f9bf0_L4c:
    add r3, r3, #0x1
    add r5, r5, #0x3
    cmp r3, #0x4
    blt ov006_021f9bf0_L26
    ldr r0, [sp, #0x4]
    add r1, sp, #0x8
    add r0, #0x8
    str r0, [sp, #0x4]
    bl native_fn_021ff5c4
    add r0, sp, #0xc
    mov r1, #0x0
    bl native_fn_021f530c
    ldr r0, [sp, #0xc]
    cmp r0, #0x1
    add r0, sp, #0x8
    bne ov006_021f9bf0_Lc4
    mov r1, #0x0
    mov r4, #0x1
    str r1, [sp]
    mov r12, r0
    add r6, r4, #0x0
    mov r7, #0x7
ov006_021f9bf0_L7c:
    mov r0, r12
    ldrb r0, [r0, #0]
    mov r2, #0x0
ov006_021f9bf0_L82:
    cmp r1, #0x0
    beq ov006_021f9bf0_L98
    sub r3, r7, r2
    add r5, r6, #0x0
    lsl r5, r3
    add r3, r0, #0x0
    tst r3, r5
    beq ov006_021f9bf0_La8
    add sp, #0x14
    mov r0, #0x0
    pop {r4, r5, r6, r7, pc}
ov006_021f9bf0_L98:
    mov r3, #0x7
    sub r3, r3, r2
    add r5, r4, #0x0
    lsl r5, r3
    add r3, r0, #0x0
    tst r3, r5
    bne ov006_021f9bf0_La8
    add r1, r4, #0x0
ov006_021f9bf0_La8:
    add r2, r2, #0x1
    cmp r2, #0x8
    blt ov006_021f9bf0_L82
    mov r0, r12
    add r0, r0, #0x1
    mov r12, r0
    ldr r0, [sp]
    add r0, r0, #0x1
    str r0, [sp]
    cmp r0, #0x4
    blt ov006_021f9bf0_L7c
    add sp, #0x14
    mov r0, #0x1
    pop {r4, r5, r6, r7, pc}
ov006_021f9bf0_Lc4:
    bl native_fn_020a4990
    cmp r0, #0x0
    beq ov006_021f9bf0_Ld2
    add sp, #0x14
    mov r0, #0x1
    pop {r4, r5, r6, r7, pc}
ov006_021f9bf0_Ld2:
    mov r0, #0x0
    add sp, #0x14
    pop {r4, r5, r6, r7, pc}
}
