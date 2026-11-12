/* main row 0x02008bf8: 28 bytes.
 *
 * What it does: Halfword copy loop: copies a halfword from [r0 + i] to [r1 + i] while i < r2, stepping i by 2 with the test at the top.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x14 -> +0x04
 *   test +0x04 cmp r12, r2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02008bf8; the literal pool and
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



asm u32 native_main_02008bf8 (register u32 a0)
{
    mov r12, #0
main_02008bf8_L4:
    cmp r12, r2
    ldrlth r3, [r0, r12]
    strlth r3, [r1, r12]
    addlt r12, r12, #2
    blt main_02008bf8_L4
    bx lr
}
