/* main row 0x020cf7c0: 28 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x18 -> native_data_020e2fb4 (image word 0x020e2fb4)
 *   test +0x08 cmp r1, #0
 *   memory +0x04 ldr r1, [r1, #8]
 *   memory +0x0c ldrbne r0, [r1, r0, lsl #1]
 *
 * Why transcribed rather than written as C: the pair test is `ldr`+`cmp` in the image; C uses `tst` after
 * the modelled pointer load
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020cf7c0; the literal pool and
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

extern u8 native_data_020e2fb4[];


asm u32 native_main_020cf7c0 (register u32 a0)
{
    ldr r1, =native_data_020e2fb4
    ldr r1, [r1, #8]
    cmp r1, #0
    ldrneb r0, [r1, r0, lsl #1]
    moveq r0, #0
    bx lr
}
