/* main row 0x02005994: 36 bytes.
 *
 * What it does: Copies four consecutive 12-byte records from r0 to one destination r1.
 *
 * Decoded shape: straight-line leaf.
 *
 *   block +0x00: ldm {r2, r3, ip}
 *   block +0x08: ldm {r2, r3, ip}
 *   block +0x10: ldm {r2, r3, ip}
 *   block +0x18: ldm {r2, r3, ip}
 *   4 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02005994; the literal pool and
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


asm u32 native_main_02005994 (register u32 a0)
{
    ldmia r0!, {r2, r3, ip}
    stmia r1, {r2, r3, ip}
    ldmia r0!, {r2, r3, ip}
    stmia r1, {r2, r3, ip}
    ldmia r0!, {r2, r3, ip}
    stmia r1, {r2, r3, ip}
    ldmia r0!, {r2, r3, ip}
    stmia r1, {r2, r3, ip}
    bx lr
}
