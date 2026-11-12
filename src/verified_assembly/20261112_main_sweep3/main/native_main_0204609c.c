/* main row 0x0204609c: 40 bytes.
 *
 * What it does: 1 load, 1 store; 1 local pool word (0x020f6ae8); 1 branch, 1 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x24 -> constant 0x020f6ae8 (image word 0x020f6ae8)
 *   back edge +0x1c -> +0x0c
 *   test +0x18 cmp r3, #2
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204609c; the literal pool and
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



asm u32 native_main_0204609c (register u32 a0)
{
    ldr r0, =0x020f6ae8
    mov r3, #0
    mvn r2, #0
main_0204609c_Lc:
    mov r1, r3, lsl #1
    add r3, r3, #1
    strh r2, [r0, r1]
    cmp r3, #2
    blt main_0204609c_Lc
    bx lr
}
