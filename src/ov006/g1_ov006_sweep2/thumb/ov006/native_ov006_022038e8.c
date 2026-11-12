/* ov006 row 0x022038e8: 30 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022038e8; the literal pool and
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



asm u32 native_ov006_022038e8 (register u32 a0)
{
    push {r3, r4}
    ldrh r3, [r0, #0]
    strh r3, [r2, #0]
    ldrh r3, [r0, #0x2]
    strh r3, [r2, #0x2]
    ldrh r4, [r0, #0]
    ldrh r3, [r1, #0]
    add r3, r4, r3
    strh r3, [r2, #0x4]
    ldrh r3, [r0, #0x2]
    ldrh r0, [r1, #0x2]
    add r0, r3, r0
    strh r0, [r2, #0x6]
    pop {r3, r4}
    bx lr
}
