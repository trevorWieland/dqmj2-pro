/* ov000 row 0x021e01e4: 204 bytes.
 *
 * What it does: 50 instructions; no calls; no back edge; returns through pop {r3, r4, r5, r6, r7, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xc8 -> constant 0x6bca1af3 (image word 0x6bca1af3)
 *   branch +0x14 -> +0xa4
 *   test +0x10 cmp r1, #19
 *   test +0xb8 cmp r1, r0, asr #12
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e01e4; the literal pool and
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



asm u32 native_ov000_021e01e4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r1, [r0, #0x60]
    ldr r1, [r1]
    mov r1, r1, asr #12
    cmp r1, #19
    bgt ov000_021e01e4_La4
    mov r2, #178
    mul r14, r1, r2
    ldr r12, [r0, #0x204]
    ldr r4, [r0, #0x1ec]
    ldr r3, [r0, #0x200]
    ldr r2, [r0, #0x1e8]
    sub r5, r12, r4
    ldr r12, =0x6bca1af3
    sub r4, r3, r2
    mov r2, r5, lsr #31
    smull r3, r5, r12, r5
    add r5, r2, r5, asr #3
    add r2, r5, #155
    add r5, r2, #1536
    mov r2, r4, lsr #31
    smull r3, r4, r12, r4
    ldr r3, [r0, #0x70]
    add r4, r2, r4, asr #3
    ldr r7, [r0, #0x208]
    ldr r6, [r0, #0x1f0]
    add r2, r3, r4
    sub r3, r7, r6
    str r2, [r0, #0x70]
    mul r4, r5, r1
    mul r14, r1, r14
    mov r2, r3, lsr #31
    smull r3, r5, r12, r3
    ldr r3, [r0, #0x78]
    add r5, r2, r5, asr #3
    add r2, r3, r5
    str r2, [r0, #0x78]
    ldr r3, [r0, #0x1ec]
    sub r2, r4, lr, asr #1
    add r2, r3, r2
    str r2, [r0, #0x74]
ov000_021e01e4_La4:
    ldr r0, [r0, #0x60]
    ldr r0, [r0, #0x8]
    ldrh r0, [r0, #4]
    mov r0, r0, lsl #12
    sub r0, r0, #1
    cmp r1, r0, asr #12
    movge r0, #1
    movlt r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
