/* ov006 row 0x022011d4: 116 bytes.
 *
 * What it does: 56 instructions; 1 call(s) to 0x022011e6; loops (back edge at +0x66); returns through bx lr; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill.
 *
 *   pool +0x70 -> constant 0x0221c160 (image word 0x0221c160)
 *   branch +0x18 -> +0x5e
 *   branch +0x2a -> +0x5e
 *   branch +0x32 -> +0x5e
 *   branch +0x3a -> +0x5e
 *   branch +0x42 -> +0x5e
 *   branch +0x4a -> +0x5e
 *   branch +0x52 -> +0x5e
 *   back edge +0x66 -> +0x12
 *   test +0x16 tst r1, r3
 *   test +0x28 cmp r6, r5
 *   test +0x30 cmp r6, r5
 *   test +0x38 cmp r6, r5
 *   test +0x40 cmp r6, r5
 *   test +0x48 cmp r6, r5
 *   test +0x50 cmp r5, r1
 *   test +0x64 cmp r2, #0x2
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022011d4; the literal pool and
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



asm u32 native_ov006_022011d4 (register u32 a0)
{
    push {r4, r5, r6, r7}
    add r4, r0, #0x0
    ldr r0, =0x0221c160
    mov r2, #0x1
    ldr r0, [r0, #0]
    mov r12, r0
    ldrh r3, [r0, #0x2]
    mov r0, r12
    add r0, #0x24
ov006_022011d4_L12:
    mov r1, #0x1
    lsl r1, r2
    tst r1, r3
    beq ov006_022011d4_L5e
    sub r5, r2, #0x1
    mov r1, #0x1e
    add r7, r5, #0x0
    mul r7, r1
    ldrb r6, [r4, #0]
    ldrb r5, [r0, r7]
    add r1, r0, r7
    cmp r6, r5
    bne ov006_022011d4_L5e
    ldrb r6, [r4, #0x1]
    ldrb r5, [r1, #0x1]
    cmp r6, r5
    bne ov006_022011d4_L5e
    ldrb r6, [r4, #0x2]
    ldrb r5, [r1, #0x2]
    cmp r6, r5
    bne ov006_022011d4_L5e
    ldrb r6, [r4, #0x3]
    ldrb r5, [r1, #0x3]
    cmp r6, r5
    bne ov006_022011d4_L5e
    ldrb r6, [r4, #0x4]
    ldrb r5, [r1, #0x4]
    cmp r6, r5
    bne ov006_022011d4_L5e
    ldrb r5, [r4, #0x5]
    ldrb r1, [r1, #0x5]
    cmp r5, r1
    bne ov006_022011d4_L5e
    mov r0, r12
    add r0, r0, r7
    ldrh r0, [r0, #0x2a]
    pop {r4, r5, r6, r7}
    bx lr
ov006_022011d4_L5e:
    add r1, r2, #0x1
    lsl r1, r1, #0x10
    lsr r2, r1, #0x10
    cmp r2, #0x2
    blo ov006_022011d4_L12
    mov r0, #0x0
    pop {r4, r5, r6, r7}
    bx lr
    mov r8, r8
}
