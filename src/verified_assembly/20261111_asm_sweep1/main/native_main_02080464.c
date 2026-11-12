/* main row 0x02080464: 32 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x1c -> native_data_021c6e10 (image word 0x021c6e10)
 *   memory +0x04 ldr r2, [r1]
 *   memory +0x08 ldr r1, [r1, #4]
 *   memory +0x10 str r2, [r0, #8]
 *   memory +0x14 str r1, [r0, #0xc]
 *   2 store instruction(s)
 *
 * Why transcribed rather than written as C: same record family, four bytes long
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02080464; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_021c6e10[];


asm u32 native_main_02080464 (register u32 a0)
{
    ldr r3, =native_data_021c6e10
    ldr r2, [r1]
    ldr r1, [r1, #4]
    add r0, r3, r0, lsl #4
    str r2, [r0, #8]
    str r1, [r0, #0xc]
    bx lr
}
