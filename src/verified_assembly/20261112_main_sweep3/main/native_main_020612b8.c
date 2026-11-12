/* main row 0x020612b8: 52 bytes.
 *
 * What it does: 2 loads, 2 stores; 3 branches, 2 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x08 -> +0x20
 *   test +0x00 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020612b8; the literal pool and
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



asm u32 native_main_020612b8 (register u32 a0)
{
    cmp r0, #0
    mov r1, #0x4000000
    bne main_020612b8_L20
    ldr r0, [r1]
    bic r0, r0, #0x1f00
    orr r0, r0, #0x100
    str r0, [r1]
    bx lr
main_020612b8_L20:
    ldr r0, [r1]
    bic r0, r0, #0x1f00
    orr r0, r0, #0xf00
    str r0, [r1]
    bx lr
}
