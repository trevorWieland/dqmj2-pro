/* ov000 row 0x021e58ec: 248 bytes.
 *
 * What it does: 62 instructions; no calls; no back edge; returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e58ec; the literal pool and
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



asm u32 native_ov000_021e58ec (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r6, [r0]
    ldr r7, [r1]
    ldr r5, [r0, #0x8]
    ldr r4, [r1, #0x8]
    ldr r1, [r2]
    ldr r0, [r2, #0x8]
    sub lr, r7, r6
    sub r2, r4, r5
    sub r7, r0, r5
    sub r1, r1, r6
    smull r9, r8, r2, r1
    smull r4, r0, r14, r7
    subs r9, r9, r4
    sbc r4, r8, r0
    adds r9, r9, #2048
    mov r0, #0
    adc r8, r4, r0
    subs r9, r9, r0
    mov r4, r1, asr #31
    str r4, [sp]
    sbcs r9, r8, r0
    mov r11, r2, asr #31
    mov r4, r7, asr #31
    mov r12, lr, asr #31
    movlt r0, #1
    ldmltia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r8, [r3]
    ldr r3, [r3, #0x8]
    sub r10, r8, r6
    mov r9, r10, asr #31
    sub r8, r3, r5
    umull r6, r5, r7, r10
    mla r5, r7, r9, r5
    mla r5, r4, r10, r5
    umull r4, r3, r1, r8
    mov r7, r8, asr #31
    mla r3, r1, r7, r3
    ldr r1, [sp]
    subs r4, r6, r4
    mla r3, r1, r8, r3
    sbc r3, r5, r3
    adds r1, r4, #2048
    adc r3, r3, r0
    subs r1, r1, r0
    sbcs r1, r3, r0
    movlt r0, #2
    ldmltia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    umull r5, r4, r8, r14
    umull r3, r1, r10, r2
    mla r4, r8, r12, r4
    mla r1, r10, r11, r1
    mla r4, r7, r14, r4
    mla r1, r9, r2, r1
    subs r3, r5, r3
    sbc r2, r4, r1
    adds r1, r3, #2048
    adc r2, r2, r0
    subs r1, r1, r0
    sbcs r1, r2, r0
    movlt r0, #3
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
