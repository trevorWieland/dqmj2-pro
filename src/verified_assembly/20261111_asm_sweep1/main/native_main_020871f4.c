/* main row 0x020871f4: 48 bytes.
 *
 * Decoded shape: straight-line leaf.
 *
 *   memory +0x00 ldr r2, [r0, #0x44]
 *
 * Why transcribed rather than written as C: packed-bit extraction not understood well enough to write as C
 * Recorded in docs/authoring/2026-11-11-main-rows-1.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020871f4; the literal pool and
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


asm u32 native_main_020871f4 (register u32 a0)
{
    ldr r2, [r0, #0x44]
    mov r1, #0
    mov r0, r2, lsl #0x19
    orr r0, r1, r0, lsr #31
    and r1, r0, #0xff
    mov r0, r2, lsl #0x15
    orr r0, r1, r0, lsr #29
    and r1, r0, #0xff
    mov r0, r2, lsl #0x12
    orr r0, r1, r0, lsr #31
    and r0, r0, #0xff
    bx lr
}
