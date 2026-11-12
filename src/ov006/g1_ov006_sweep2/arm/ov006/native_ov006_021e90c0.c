/* ov006 row 0x021e90c0: 112 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x64 -> constant 0x02218f38 (image word 0x02218f38)
 *   pool +0x68 -> constant 0x02218d90 (image word 0x02218d90)
 *   pool +0x6c -> constant 0x02218ea8 (image word 0x02218ea8)
 *   test +0x10 cmp r0, #2
 *   test +0x30 cmp r0, #2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021e90c0; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_ov006_021e90c0 (register u32 a0)
{
    ldr r0, =0x02218f38
    ldr r1, =0x02218d90
    ldr r0, [r0, #0x7c]
    and r0, r0, #2
    cmp r0, #2
    moveq r2, #1
    movne r2, #0
    str r2, [r1, #0x38]
    ldr r0, =0x02218ea8
    ldr r1, =0x02218f38
    ldr r0, [r0, #0x7c]
    and r0, r0, #2
    cmp r0, #2
    moveq r2, #1
    ldr r0, =0x02218d90
    movne r2, #0
    str r2, [r0, #0x1c]
    ldr r2, [r1, #0x7c]
    ldr r0, =0x02218ea8
    bic r2, r2, #2
    str r2, [r1, #0x7c]
    ldr r1, [r0, #0x7c]
    bic r1, r1, #2
    str r1, [r0, #0x7c]
    bx lr
}
