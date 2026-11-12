/* main row 0x02024504: 60 bytes.
 *
 * What it does: 2 branches, 1 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x14 -> +0x24
 *   test +0x00 cmp r0, #0
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02024504; the literal pool and
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



asm u32 native_main_02024504 (register u32 a0)
{
    cmp r0, #0
    mov r1, #0
    bxeq lr
    mov r3, #0x400
    add r3, r3, #0x1e
    bmi main_02024504_L24
    clz r12, r0
    movs r0, r0, lsl r12
    sub r3, r3, r12
main_02024504_L24:
    mov r1, r0
    mov r0, r1, lsl #0x15
    add r1, r1, r1
    mov r1, r1, lsr #0xc
    orr r1, r1, r3, lsl #20
    bx lr
}
