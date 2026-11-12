/* ov000 row 0x021e8cb4: 164 bytes.
 *
 * What it does: 39 instructions; no calls; no back edge; returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x9c -> constant 0x0223526c (image word 0x0223526c)
 *   pool +0xa0 -> constant 0x0000019a (image word 0x0000019a)
 *   test +0x14 cmp r0, #0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8cb4; the literal pool and
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



asm u32 native_ov000_021e8cb4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r4, =0x0223526c
    mov r12, #716
    mla r12, r0, r12, r4
    ldrb r0, [r12, #0x274]
    cmp r0, #0
    moveq r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, pc}
    ldr lr, =0x0000019a
    mov r0, r1, asr #31
    umull r4, r6, r1, r14
    adds r7, r4, #2048
    mla r6, r0, r14, r6
    umull r4, r5, r2, r14
    mov r1, r2, asr #31
    adc r2, r6, #0
    mov r0, r7, lsr #12
    adds r6, r4, #2048
    orr r0, r0, r2, lsl #20
    mla r5, r1, r14, r5
    umull r4, r2, r3, r14
    mov r1, r3, asr #31
    adc r5, r5, #0
    mov r6, r6, lsr #12
    mla r2, r1, r14, r2
    adds r3, r4, #2048
    adc r1, r2, #0
    mov r2, r3, lsr #12
    str r0, [r12, #0x7c]
    orr r6, r6, r5, lsl #20
    str r6, [r12, #0x80]
    orr r2, r2, r1, lsl #20
    str r2, [r12, #0x84]
    str r0, [r12, #0x290]
    str r6, [r12, #0x294]
    str r2, [r12, #0x298]
    str r0, [r12, #0x290]
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
