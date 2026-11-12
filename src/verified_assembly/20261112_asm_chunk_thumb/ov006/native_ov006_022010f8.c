/* ov006 row 0x022010f8: 56 bytes.
 *
 * What it does: Writes one block of 2 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x2c -> constant 0x0221c160 (image word 0x0221c160)
 *   pool +0x30 -> native_data_0220e2cc (image word 0x0220e2cc)
 *   pool +0x34 -> native_data2_0220e2cc (image word 0x0220e2cc)
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022010f8; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 8 of 56 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0220e2cc[];
extern u8 native_data2_0220e2cc[];


asm u32 native_ov006_022010f8 (register u32 a0)
{
    ldr r1, =0x0221c160
    ldr r3, [r1, #0]
    ldr r1, =native_data_0220e2cc
    add r2, r3, #0x2
    str r2, [r1, #0]
    add r2, r3, #0x4
    str r2, [r1, #0x4]
    add r2, r3, #0x6
    str r2, [r1, #0x8]
    add r2, r3, #0x0
    add r2, #0x8
    str r2, [r1, #0xc]
    add r2, r3, #0x0
    add r2, #0xa
    str r2, [r1, #0x10]
    add r3, #0xc
    str r3, [r1, #0x14]
    lsl r1, r0, #0x2
    ldr r0, =native_data2_0220e2cc
    ldr r0, [r0, r1]
    ldrh r0, [r0, #0]
    bx lr
}
