/* ov000 row 0x021f3fec: 292 bytes.
 *
 * What it does: 72 instructions; no calls; no back edge; returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x120 -> constant 0x02236ed8 (image word 0x02236ed8)
 *   branch +0x24 -> +0x114
 *   test +0x20 cmp r0, #0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f3fec; the literal pool and
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



asm u32 native_ov000_021f3fec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #16
    ldr r4, =0x02236ed8
    mov r7, #636
    ldr r4, [r4, #0x4]
    mov lr, #0
    mla r12, r0, r7, r4
    ldrb r0, [r12, #0x278]
    cmp r0, #0
    beq ov000_021f3fec_L114
    sub r0, r7, #226
    sub r4, r7, #226
    str r0, [sp, #0x8]
    umull r0, r6, r1, r0
    umull r11, r5, r2, r4
    str r4, [sp, #0x4]
    str r4, [sp]
    umull r7, r4, r3, r4
    mla r6, r1, r14, r6
    adds r0, r0, #2048
    str r7, [sp, #0xc]
    mov r7, r0, lsr #12
    ldr r0, [sp, #0x8]
    mov r10, r1, asr #31
    mla r6, r10, r0, r6
    adc r0, r6, lr
    orr r7, r7, r0, lsl #20
    adds r0, r11, #2048
    mov r6, r0, lsr #12
    mla r5, r2, r14, r5
    ldr r0, [sp, #0x4]
    mov r9, r2, asr #31
    mla r5, r9, r0, r5
    adc r0, r5, lr
    orr r6, r6, r0, lsl #20
    ldr r0, [sp, #0xc]
    str r7, [r12, #0x7c]
    adds r0, r0, #2048
    mov r5, r0, lsr #12
    mla r4, r3, r14, r4
    ldr r0, [sp]
    mov r8, r3, asr #31
    mla r4, r8, r0, r4
    adc r0, r4, lr
    str r6, [r12, #0x80]
    orr r5, r5, r0, lsl #20
    str r5, [r12, #0x84]
    ldr r0, [r12, #0x11c]
    smull r4, r1, r0, r1
    adds r4, r4, #2048
    adc r0, r1, lr
    mov r1, r4, lsr #12
    orr r1, r1, r0, lsl #20
    str r1, [r12, #0x11c]
    ldr r0, [r12, #0x120]
    smull r2, r1, r0, r2
    adds r2, r2, #2048
    adc r0, r1, lr
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    str r1, [r12, #0x120]
    ldr r0, [r12, #0x124]
    smull r2, r1, r0, r3
    adds r2, r2, #2048
    adc r0, r1, lr
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    str r1, [r12, #0x124]
    mov lr, #1
ov000_021f3fec_L114:
    mov r0, lr
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
