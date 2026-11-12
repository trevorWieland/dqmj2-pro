/* main row 0x020287f4: 36 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x20 -> native_data_020edf90 (image word 0x020edf90)
 *   memory +0x08 ldr r3, [r1, #0x9c]
 *   memory +0x18 str r2, [r1, #0x9c]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: nibble replace: `bic` vs the image `orr`+`eor`
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020287f4; the literal pool and
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

extern u8 native_data_020edf90[];


asm u32 native_main_020287f4 (register u32 a0)
{
    ldr r1, =native_data_020edf90
    and r2, r0, #0xf
    ldr r3, [r1, #0x9c]
    and r0, r3, #0xf
    bic r3, r3, #0xf
    orr r2, r3, r2
    str r2, [r1, #0x9c]
    bx lr
}
