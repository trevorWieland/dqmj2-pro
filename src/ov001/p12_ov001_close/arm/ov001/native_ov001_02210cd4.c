/* ov001 row 0x02210cd4: 196 bytes.
 *
 * What it does: 47 instructions; no calls; no back edge; returns through bx lr; 2 literal slot(s) in the extent
 *
 * Decoded shape: branched body (47 instructions, 0 calls, 1 branch, 0 back edges, 2 literal slots).
 *
 *   pool +0xbc -> constant 0x0223e118 (image word 0x0223e118)
 *   pool +0xc0 -> constant 0x04000040 (image word 0x04000040)
 *   branch +0x14 -> +0x60
 *   test +0x08 cmp r0, #0
 *   test +0x10 cmp r0, #1
 *   test +0x2c cmp r3, #32
 *   test +0x60 cmp r0, #2
 *   test +0x68 cmp r0, #3
 *   test +0x84 cmp r3, #32
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02210cd4; the literal pool and
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



asm u32 native_ov001_02210cd4 (register u32 a0)
{
    ldr r1, =0x0223e118
    ldrb r0, [r1]
    cmp r0, #0
    bxeq lr
    cmp r0, #1
    bne ov001_02210cd4_L60
    ldrsb r2, [r1, #1]
    mov r12, #255
    add r2, r2, #3
    strb r2, [r1, #0x1]
    ldrsb r3, [r1, #1]
    cmp r3, #32
    movge r2, #2
    movge r3, #32
    strgeb r2, [r1]
    mov r2, r3, lsl #8
    rsb r1, r3, #192
    ldr r3, =0x04000040
    and r2, r2, #65280
    and r1, r1, #255
    strh r12, [r3]
    orr r1, r2, r1
    strh r1, [r3, #4]
    bx lr
ov001_02210cd4_L60:
    cmp r0, #2
    bxeq lr
    cmp r0, #3
    bxne lr
    ldrsb r2, [r1, #1]
    mov r12, #255
    add r2, r2, #3
    strb r2, [r1, #0x1]
    ldrsb r3, [r1, #1]
    cmp r3, #32
    movge r2, #0
    movge r3, #32
    strgeb r2, [r1]
    rsb r1, r3, #32
    mov r2, r1, lsl #8
    add r1, r3, #160
    ldr r3, =0x04000040
    and r2, r2, #65280
    and r1, r1, #255
    strh r12, [r3]
    orr r1, r2, r1
    strh r1, [r3, #4]
    bx lr
}
