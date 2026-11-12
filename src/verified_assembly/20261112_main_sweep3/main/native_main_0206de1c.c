/* main row 0x0206de1c: 40 bytes.
 *
 * What it does: 3 loads, 1 store; 2 local pool words (0x021c4f60, 0x0206de44); tail-branches out
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x20 -> constant 0x021c4f60 (image word 0x021c4f60)
 *   pool +0x24 -> native_fn_0206de44 (image word 0x0206de44)
 *   test +0x00 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0206de1c; the literal pool and
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

extern void native_fn_0206de44(void);


asm u32 native_main_0206de1c (register u32 a0)
{
    cmp r0, #0
    ldrne r0, =0x021c4f60
    ldr r12, =native_fn_0206de44
    ldreq r0, =0x021c4f60
    moveq r1, #0
    str r1, [r0, #8]
    mov r0, #1
    bx r12
}
