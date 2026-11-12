/* main row 0x02080420: 36 bytes.
 *
 * What it does: 3 loads, 2 stores; 1 local pool word (0x021c6e10); returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x20 -> constant 0x021c6e10 (image word 0x021c6e10)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02080420; the literal pool and
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



asm u32 native_main_02080420 (register u32 a0)
{
    ldrh r2, [r1]
    ldr r3, =0x021c6e10
    ldrh r1, [r1, #2]
    mov r12, r0, lsl #4
    add r0, r3, r0, lsl #4
    strh r2, [r3, r12]
    strh r1, [r0, #2]
    bx lr
}
