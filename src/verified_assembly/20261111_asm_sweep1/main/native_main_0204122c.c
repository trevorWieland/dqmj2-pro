/* main row 0x0204122c: 32 bytes.
 *
 * What it does: Clears the pointed-to word and returns 1 when it is non-zero; returns 0
 * without writing when it is already zero.
 *
 * Decoded shape: guarded entry: bxeq at +0x0c returns before the body.
 *
 *   test +0x04 cmp r1, #0
 *   memory +0x00 ldr r1, [r0]
 *   memory +0x14 str r1, [r0]
 *   1 store instruction(s)
 *
 * Why transcribed rather than written as C: C if-converts the early return into `movne/strne/movne`; the
 * image keeps `moveq`+`bxeq lr`
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204122c; the literal pool and
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


asm u32 native_main_0204122c (register u32 a0)
{
    ldr r1, [r0]
    cmp r1, #0
    moveq r0, #0
    bxeq lr
    mov r1, #0
    str r1, [r0]
    mov r0, #1
    bx lr
}
