/* main row 0x020d3b50: 44 bytes.
 *
 * What it does: Canonicalises the 0x30 and 0xc0 bit groups of its second argument (OR in each group when either bit is set, truncating to 16 bits), then ORs and XORs that value into its first argument, so the first argument is returned unchanged.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   test +0x00 tst r1, #0x30
 *   test +0x10 tst r1, #0xc0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020d3b50; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_020d3b50 (register u32 a0)
{
    tst r1, #0x30
    orrne r1, r1, #0x30
    movne r1, r1, lsl #0x10
    movne r1, r1, lsr #0x10
    tst r1, #0xc0
    orrne r1, r1, #0xc0
    movne r1, r1, lsl #0x10
    movne r1, r1, lsr #0x10
    orr r0, r0, r1
    eor r0, r0, r1
    bx lr
}
