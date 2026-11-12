/* ov000 row 0x021efa14: 136 bytes.
 *
 * What it does: 31 instructions; no calls; no back edge; returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x7c -> constant 0x02236c1c (image word 0x02236c1c)
 *   pool +0x80 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x84 -> native_data_0222ee80 (image word 0x0222ee80)
 *   branch +0x40 -> +0x60
 *   test +0x04 cmp r1, #0
 *   test +0x3c cmp r5, #2
 *   test +0x44 cmp lr, #0
 *   test +0x6c cmp r1, #0
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021efa14; the literal pool and
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

extern u8 native_data_0222ee80[];


asm u32 native_ov000_021efa14 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    cmp r1, #0
    ldreq r2, =0x02236c1c
    movne r4, r0
    ldreq r4, [r2, #0x14]
    ldr r3, =0x66666667
    sub lr, r0, r4
    smull r2, r5, r3, r14
    ldr r12, =0x02236c1c
    mov r2, lr, lsr #31
    str r4, [r12, #0xc]
    str r0, [r12, #0x14]
    adds r5, r2, r5, asr #2
    str r5, [r12, #0x10]
    rsbmi r5, r5, #0
    cmp r5, #2
    bge ov000_021efa14_L60
    cmp lr, #0
    movgt r0, #1
    mvnle r0, #0
    mov r0, r0, lsl #17
    ldr r2, =0x02236c1c
    mov r0, r0, asr #16
    str r0, [r2, #0x10]
ov000_021efa14_L60:
    ldr r0, =native_data_0222ee80
    mov r2, #1
    str r2, [r0]
    cmp r1, #0
    ldreq r0, =0x02236c1c
    streq r2, [r0, #0x8]
    ldmia sp!, {r3, r4, r5, pc}
}
