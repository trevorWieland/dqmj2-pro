/* main row 0x020a48e4: 44 bytes.
 *
 * What it does: 1 load, 0 stores; 3 branches, 2 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   branch +0x14 -> +0x18
 *   back edge +0x1c -> +0x0e
 *   back edge +0x22 -> +0x0a
 *   test +0x12 tst r7, r6
 *   test +0x1a cmp r4, #8
 *   test +0x20 cmp r3, #4
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a48e4; the literal pool and
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



asm u32 native_main_020a48e4 (register u32 a0)
{
    push {r4, r5, r6, r7}
    mov r3, #0
    add r2, r3, #0
    add r1, r3, #0
    mov r6, #1
main_020a48e4_La:
    ldrb r5, [r0, r3]
    add r4, r1, #0
main_020a48e4_Le:
    add r7, r5, #0
    asr r7, r4
    tst r7, r6
    beq main_020a48e4_L18
    add r2, r2, #1
main_020a48e4_L18:
    add r4, r4, #1
    cmp r4, #8
    blt main_020a48e4_Le
    add r3, r3, #1
    cmp r3, #4
    blt main_020a48e4_La
    lsl r0, r2, #0x18
    lsr r0, r0, #0x18
    pop {r4, r5, r6, r7}
    bx lr
}
