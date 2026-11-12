/* main row 0x0203c830: 52 bytes.
 *
 * What it does: 2 loads, 0 stores; 1 local pool word (0x020f5c18); 2 branches, 2 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x30 -> constant 0x020f5c18 (image word 0x020f5c18)
 *   back edge +0x28 -> +0x0c
 *   test +0x10 cmp r1, #0
 *   test +0x20 cmp r2, #0x40
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0203c830; the literal pool and
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



asm u32 native_main_0203c830 (register u32 a0)
{
    mov r0, #0
    ldr r3, =0x020f5c18
    mov r2, r0
main_0203c830_Lc:
    ldr r1, [r3]
    cmp r1, #0
    moveq r0, r3
    bxeq lr
    add r2, r2, #1
    cmp r2, #0x40
    add r3, r3, #0xc
    blt main_0203c830_Lc
    bx lr
}
