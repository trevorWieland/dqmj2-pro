/* ov001 row 0x021dc064: 164 bytes.
 *
 * What it does: 41 instructions; no calls; no back edge; returns through bx lr
 *
 * Decoded shape: straight-line scalar (41 instructions, 0 calls, 0 branches, 0 back edges, 0 literal slots).
 *
 *   test +0x04 cmp r1, #0
 *   test +0x14 cmp r1, #0
 *   test +0x24 cmp r1, #0
 *   test +0x34 cmp r1, #0
 *   test +0x44 cmp r1, #0
 *   test +0x54 cmp r1, #0
 *   test +0x64 cmp r1, #0
 *   test +0x74 cmp r1, #0
 *   test +0x84 cmp r1, #0
 *   test +0x94 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021dc064; the literal pool and
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



asm u32 native_ov001_021dc064 (register u32 a0)
{
    ldrsb r1, [r0, #10]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #9]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #12]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #13]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #14]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #15]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #34]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #35]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r1, [r0, #36]
    cmp r1, #0
    movne r0, #0
    bxne lr
    ldrsb r0, [r0, #32]
    cmp r0, #0
    movne r0, #0
    moveq r0, #1
    bx lr
}
