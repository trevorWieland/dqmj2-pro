/* ov001 row 0x021e29f8: 80 bytes.
 *
 * What it does: 19 instructions; no calls; no back edge; returns through bx lr; 1 literal slot(s) in the extent
 *
 * Decoded shape: branched body (19 instructions, 0 calls, 1 branch, 0 back edges, 1 literal slot).
 *
 *   pool +0x4c -> constant 0x022388ec (image word 0x022388ec)
 *   branch +0x0c -> +0x20
 *   test +0x08 tst r3, r0
 *   test +0x24 cmp r1, #0
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e29f8; the literal pool and
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



asm u32 native_ov001_021e29f8 (register u32 a0)
{
    ldr r2, =0x022388ec
    ldrb r3, [r2, #0x10]
    tst r3, r0
    beq ov001_021e29f8_L20
    ldrb r12, [r2, #0x24]
    mvn r3, r0
    and r3, r12, r3
    strb r3, [r2, #0x24]
ov001_021e29f8_L20:
    ldr r2, =0x022388ec
    cmp r1, #0
    ldrb r1, [r2, #0x10]
    orr r1, r1, r0
    strb r1, [r2, #0x10]
    ldrb r1, [r2, #0x2f]
    mvneq r0, r0
    andeq r0, r1, r0
    orrne r0, r1, r0
    strb r0, [r2, #0x2f]
    bx lr
}
