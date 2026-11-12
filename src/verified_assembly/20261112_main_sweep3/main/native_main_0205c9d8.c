/* main row 0x0205c9d8: 52 bytes.
 *
 * What it does: 2 loads, 0 stores; 1 local pool word (0x021043ac); 2 branches, 2 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x30 -> constant 0x021043ac (image word 0x021043ac)
 *   back edge +0x28 -> +0x0c
 *   test +0x10 cmp r1, #0
 *   test +0x20 cmp r2, #0x20
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205c9d8; the literal pool and
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



asm u32 native_main_0205c9d8 (register u32 a0)
{
    ldr r3, =0x021043ac
    mvn r0, #0
    mov r2, #0
main_0205c9d8_Lc:
    ldrb r1, [r3]
    cmp r1, #0
    moveq r0, r2
    bxeq lr
    add r2, r2, #1
    cmp r2, #0x20
    add r3, r3, #0x11c
    blt main_0205c9d8_Lc
    bx lr
}
