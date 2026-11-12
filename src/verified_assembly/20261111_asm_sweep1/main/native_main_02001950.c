/* main row 0x02001950: 44 bytes.
 *
 * What it does: Fills 0x38 bytes with a repeating 0x1000/0 pattern using writeback block
 * stores.
 *
 * Decoded shape: aggregate fill: 7 writeback block stores.
 *
 *   block +0x08: stm {r2, r3}
 *   block +0x10: stm {r1, r3}
 *   block +0x14: stm {r1, r2, r3}
 *   block +0x18: stm {r1, r3}
 *   7 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02001950; the literal pool and
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


asm u32 native_main_02001950 (register u32 a0)
{
    mov r2, #0x1000
    mov r3, #0
    stmia r0!, {r2, r3}
    mov r1, #0
    stmia r0!, {r1, r3}
    stmia r0!, {r1, r2, r3}
    stmia r0!, {r1, r3}
    stmia r0!, {r1, r2, r3}
    stmia r0!, {r1, r3}
    stmia r0!, {r1, r2}
    bx lr
}
