/* main row 0x0208a66c: 36 bytes.
 *
 * What it does: Counts the set bits of its argument with a CLZ-based clear-the-top-bit loop.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x20 -> +0x0c
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0208a66c; the literal pool and
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



asm u32 native_main_0208a66c (register u32 a0)
{
    mov r1, r0
    mov r0, #0
    mov r3, #1
main_0208a66c_Lc:
    clz r2, r1
    rsbs r2, r2, #0x1f
    bxlo lr
    bic r1, r1, r3, lsl r2
    add r0, r0, #1
    b main_0208a66c_Lc
}
