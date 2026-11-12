/* main row 0x0207cd98: 32 bytes.
 *
 * What it does: Index bounds check against 100, then returns table[index]; returns 0
 * when out of range.
 *
 * Decoded shape: guarded entry: bxge at +0x08 returns before the body.
 *
 *   pool +0x1c -> native_data_021c67a8 (image word 0x021c67a8)
 *   test +0x00 cmp r0, #0x64
 *   memory +0x10 ldr r1, [r1]
 *   memory +0x14 ldr r0, [r1, r0, lsl #2]
 *
 * Why transcribed rather than written as C: C predicates the table load (`ldrlo`); the image keeps `bxge lr`
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0207cd98; the literal pool and
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

extern u8 native_data_021c67a8[];


asm u32 native_main_0207cd98 (register u32 a0)
{
    cmp r0, #0x64
    movge r0, #0
    bxge lr
    ldr r1, =native_data_021c67a8
    ldr r1, [r1]
    ldr r0, [r1, r0, lsl #2]
    bx lr
}
