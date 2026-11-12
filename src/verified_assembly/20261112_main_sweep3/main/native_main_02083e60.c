/* main row 0x02083e60: 52 bytes.
 *
 * What it does: 4 loads, 1 store; 1 local pool word (0x021c72a0); 1 branch; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x30 -> constant 0x021c72a0 (image word 0x021c72a0)
 *   branch +0x0c -> +0x24
 *   test +0x04 cmp r0, #0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02083e60; the literal pool and
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



asm u32 native_main_02083e60 (register u32 a0)
{
    ldr r1, =0x021c72a0
    cmp r0, #0
    ldrh r3, [r1, #0x12]
    bgt main_02083e60_L24
    ldrb r0, [r1, #3]
    ldrh r2, [r1, #6]
    add r0, r0, #1
    mul r0, r2, r0
    add r0, r0, #4
main_02083e60_L24:
    strh r0, [r1, #0x12]
    mov r0, r3
    bx lr
}
