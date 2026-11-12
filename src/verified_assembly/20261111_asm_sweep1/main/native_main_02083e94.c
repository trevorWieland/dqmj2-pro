/* main row 0x02083e94: 32 bytes.
 *
 * What it does: Replaces the halfword at block+0x16 with block+6 when the argument is
 * zero, and returns the previous halfword.
 *
 * Decoded shape: straight-line leaf.
 *
 *   pool +0x1c -> native_data_021c72a0 (image word 0x021c72a0)
 *   test +0x04 cmp r0, #0
 *   memory +0x08 ldrh r2, [r1, #0x16]
 *   memory +0x0c ldrhle r0, [r1, #6]
 *   memory +0x10 strh r0, [r1, #0x16]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: C if-converts the halfword select into `ldrhle/strhle`; the
 * image keeps the unconditional pair with the conditional load
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02083e94; the literal pool and
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

extern u8 native_data_021c72a0[];


asm u32 native_main_02083e94 (register u32 a0)
{
    ldr r1, =native_data_021c72a0
    cmp r0, #0
    ldrh r2, [r1, #0x16]
    ldrleh r0, [r1, #6]
    strh r0, [r1, #0x16]
    mov r0, r2
    bx lr
}
