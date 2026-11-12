/* main row 0x020259e8: 64 bytes.
 *
 * What it does: 2 branches; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x04 -> +0x24
 *   branch +0x10 -> +0x38
 *   test +0x00 tst r0, #0x80000000
 *   test +0x28 cmp r2, r0, lsl #1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020259e8; the literal pool and
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



asm u32 native_main_020259e8 (register u32 a0)
{
    tst r0, #0x80000000
    bne main_020259e8_L24
    mov r1, #0x9e
    subs r1, r1, r0, lsr #23
    blt main_020259e8_L38
    mov r2, r0, lsl #8
    orr r0, r2, #0x80000000
    mov r0, r0, lsr r1
    bx lr
main_020259e8_L24:
    mov r2, #0xff000000
    cmp r2, r0, lsl #1
    movhs r0, #0
    mvnlo r0, #0
    bx lr
main_020259e8_L38:
    mvn r0, #0
    bx lr
}
