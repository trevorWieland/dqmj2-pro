/* main row 0x02007360: 32 bytes.
 *
 * What it does: Polls the video timing: saves the word at 0x04000208, stores 0x04000000 there, waits for VCOUNT (0x04000006) to read zero, then restores the saved word.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x14 -> +0x0c
 *   test +0x10 cmp r0, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02007360; the literal pool and
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



asm u32 native_main_02007360 (register u32 a0)
{
    mov r12, #0x4000000
    ldr r1, [r12, #0x208]
    str r12, [r12, #0x208]
main_02007360_Lc:
    ldrh r0, [r12, #6]
    cmp r0, #0
    bne main_02007360_Lc
    str r1, [r12, #0x208]
    bx lr
}
