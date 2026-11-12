/* main row 0x020844d0: 44 bytes.
 *
 * What it does: Byte-index bounds check against block[0], then returns table +
 * 0xc4*index; returns 0 when out of range.
 *
 * Decoded shape: guarded entry: bxhs at +0x14 returns before the body.
 *
 *   pool +0x28 -> native_data_021c9600 (image word 0x021c9600)
 *   test +0x0c cmp r3, r2
 *   memory +0x08 ldrb r2, [r1]
 *   memory +0x18 ldr r2, [r1, #0x18]
 *
 * Why transcribed rather than written as C: C predicates the body (`movhs/ldrlo/movlo/mlalo`); the image
 * keeps `bxhs lr`
 * Recorded in docs/authoring/2026-11-11-main-rows-2.md.
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020844d0; the literal pool and
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

extern u8 native_data_021c9600[];


asm u32 native_main_020844d0 (register u32 a0)
{
    ldr r1, =native_data_021c9600
    and r3, r0, #0xff
    ldrb r2, [r1]
    cmp r3, r2
    movhs r0, #0
    bxhs lr
    ldr r2, [r1, #0x18]
    mov r1, #0xc4
    mla r0, r1, r0, r2
    bx lr
}
