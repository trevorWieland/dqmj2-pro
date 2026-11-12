/* main row 0x0200197c: 52 bytes.
 *
 * What it does: Copies four 12-byte records from r0 to r1, skipping one source word
 * after each chunk.
 *
 * Decoded shape: aggregate fill: 4 writeback block stores.
 *
 *   block +0x00: ldm {r2, r3, ip}
 *   block +0x08: stm {r2, r3, ip}
 *   block +0x0c: ldm {r2, r3, ip}
 *   block +0x14: stm {r2, r3, ip}
 *   4 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0200197c; the literal pool and
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


asm u32 native_main_0200197c (register u32 a0)
{
    ldmia r0!, {r2, r3, ip}
    add r0, r0, #4
    stmia r1!, {r2, r3, ip}
    ldmia r0!, {r2, r3, ip}
    add r0, r0, #4
    stmia r1!, {r2, r3, ip}
    ldmia r0!, {r2, r3, ip}
    add r0, r0, #4
    stmia r1!, {r2, r3, ip}
    ldmia r0!, {r2, r3, ip}
    add r0, r0, #4
    stmia r1!, {r2, r3, ip}
    bx lr
}
