/* main row 0x02093128: 44 bytes.
 *
 * What it does: 2 loads, 4 stores; 1 local pool word (0x00000000); 2 branches, 1 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x28 -> constant 0x00000000 (image word 0x00000000)
 *   branch +0x06 -> +0x24
 *   back edge +0x22 -> +0x08
 *   test +0x20 cmp r4, r2
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02093128; the literal pool and
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



asm u32 native_main_02093128 (register u32 a0)
{
    push {r4, r5}
    lsr r2, r2, #2
    ldr r4, =0x00000000
    beq main_02093128_L24
main_02093128_L8:
    ldr r3, [r1, #0]
    add r4, r4, #1
    lsr r5, r3, #0x18
    strb r5, [r0, #0]
    lsr r5, r3, #0x10
    strb r5, [r0, #1]
    lsr r5, r3, #8
    strb r5, [r0, #2]
    add r5, r0, #3
    add r1, r1, #4
    add r0, r0, #4
    strb r3, [r5, #0]
    cmp r4, r2
    blo main_02093128_L8
main_02093128_L24:
    pop {r4, r5}
    bx lr
}
