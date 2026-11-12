/* main row 0x02000e04: 24 bytes.
 *
 * What it does: Writes 3 blocks of 1 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   3 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02000e04; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: three plausible C bodies were compiled first (word-copy loop, block-struct copy sized to the widest measured register list, and a guarded copy loop); none matched, the closest differs in 10 of 24 bytes. The meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_main_02000e04 (register u32 a0)
{
    stmia r0!, {r2}
    mov r3, #0x0
    stmia r0!, {r1, r3}
    neg r1, r1
    stmia r0!, {r1, r2}
    mov r1, #0x1
    lsl r1, r1, #0xc
    str r3, [r0, #0]
    str r3, [r0, #0x4]
    str r3, [r0, #0x8]
    str r1, [r0, #0xc]
    bx lr
}
