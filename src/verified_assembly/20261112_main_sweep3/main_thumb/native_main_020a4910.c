/* main row 0x020a4910: 40 bytes.
 *
 * What it does: 0 loads, 1 store; 1 branch, 1 backward; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   back edge +0x22 -> +0x14
 *   test +0x20 cmp r4, #4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020a4910; the literal pool and
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



asm u32 native_main_020a4910 (register u32 a0)
{
    push {r3, r4, r5, r6}
    mov r2, #0
    mvn r2, r2
    add r3, r2, #0
    lsr r3, r0
    add r5, r3, #0
    mov r4, #0
    eor r5, r2
    add r6, r4, #0
    mov r0, #0x18
main_020a4910_L14:
    sub r2, r0, r6
    add r3, r5, #0
    lsr r3, r2
    strb r3, [r1, r4]
    add r4, r4, #1
    add r6, #8
    cmp r4, #4
    blt main_020a4910_L14
    pop {r3, r4, r5, r6}
    bx lr
}
