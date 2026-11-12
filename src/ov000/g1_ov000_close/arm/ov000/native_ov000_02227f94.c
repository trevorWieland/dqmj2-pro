/* ov000 row 0x02227f94: 360 bytes.
 *
 * What it does: 90 instructions; 5 call(s) to 0x02227fc4, 0x022280fc, 0x02228060, +2 more; loops (back edge at +0x44); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   back edge +0x44 -> +0x30
 *   branch +0x8c -> +0x104
 *   branch +0x98 -> +0xcc
 *   back edge +0xc8 -> +0xa8
 *   branch +0xd4 -> +0xf0
 *   branch +0xec -> +0x104
 *   branch +0x10c -> +0x120
 *   back edge +0x12c -> +0x58
 *   test +0x40 cmp r3, #3
 *   test +0x88 cmp r0, r3
 *   test +0x90 cmp r7, #0
 *   test +0xac cmp r0, lr
 *   test +0xb4 cmpeq lr, r12
 *   test +0xc4 cmp r2, r7
 *   test +0xd0 cmp r3, r1
 *   test +0xfc cmp r2, r1
 *   test +0x108 cmp r1, r9
 *   test +0x114 cmp r0, r1
 *   test +0x128 cmp r7, #3
 *   0 block transfer(s), 13 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02227f94; the literal pool and
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

extern void native_fn_022280fc(void);


asm u32 native_ov000_02227f94 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #48
    mov r4, #0
    str r1, [sp, #0xc]
    str r2, [sp, #0x10]
    mov r9, r3
    ldr r8, [sp, #0x58]
    mov r11, r0
    mov r3, r4
    mvn r2, #0
    add r1, sp, #36
    add r5, sp, #24
ov000_02227f94_L30:
    add r0, r3, #1
    str r2, [r1, r3, lsl #2]
    str r2, [r5, r3, lsl #2]
    and r3, r0, #255
    cmp r3, #3
    blo ov000_02227f94_L30
    mov r0, #11
    add r6, sp, #21
    strb r0, [r8]
    mov r7, #0
ov000_02227f94_L58:
    add r1, sp, #20
    add r0, sp, #21
    str r1, [sp]
    add r0, r0, r7
    str r0, [sp, #0x4]
    ldr r2, [sp, #0x10]
    ldr r1, [sp, #0xc]
    mov r0, r11
    mov r3, r7
    str r5, [sp, #0x8]
    bl native_fn_022280fc
    mvn r3, #0
    cmp r0, r3
    beq ov000_02227f94_L104
    cmp r7, #0
    mov r2, #0
    bls ov000_02227f94_Lcc
    add r10, sp, #24
    ldr r12, [r10, r7, lsl #2]
    add r1, sp, #36
ov000_02227f94_La8:
    ldr lr, [r1, r2, lsl #2]
    cmp r0, lr
    ldreq lr, [r10, r2, lsl #2]
    cmpeq lr, r12
    moveq r3, r2
    add r2, r2, #1
    and r2, r2, #255
    cmp r2, r7
    blo ov000_02227f94_La8
ov000_02227f94_Lcc:
    mvn r1, #0
    cmp r3, r1
    bne ov000_02227f94_Lf0
    add r1, sp, #36
    str r0, [r1, r4, lsl #2]
    add r5, r5, #4
    add r6, r6, #1
    add r4, r4, #1
    b ov000_02227f94_L104
ov000_02227f94_Lf0:
    add r10, sp, #21
    ldrb r2, [r6]
    ldrb r1, [r10, r3]
    cmp r2, r1
    strhib r2, [r10, r3]
ov000_02227f94_L104:
    sub r1, r4, #1
    cmp r1, r9
    bne ov000_02227f94_L120
    mvn r1, #0
    cmp r0, r1
    ldrneb r0, [sp, #0x14]
    strneb r0, [r8]
ov000_02227f94_L120:
    add r0, r7, #1
    and r7, r0, #255
    cmp r7, #3
    blo ov000_02227f94_L58
    add r1, sp, #21
    ldrb r3, [r1, r9]
    add r0, sp, #36
    ldr r2, [sp, #0x5c]
    ldr r0, [r0, r9, lsl #2]
    add r1, sp, #24
    strb r3, [r2]
    ldr r2, [r1, r9, lsl #2]
    ldr r1, [sp, #0x60]
    mov r0, r0, lsl #16
    str r2, [r1]
    mov r0, r0, asr #16
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
