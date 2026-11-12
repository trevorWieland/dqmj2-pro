/* main row 0x020930f4: 52 bytes.
 *
 * What it does: 5 loads, 1 store; returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020930f4; the literal pool and
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



asm u32 native_main_020930f4 (register u32 a0)
{
    push {r3, r4, r5, r6}
    add r2, r0, #2
    lsl r2, r2, #0x1c
    lsr r2, r2, #0x1a
    ldr r3, [r1, r2]
    add r2, r0, #0
    add r2, #0xd
    lsl r5, r0, #2
    mov r6, #8
    lsl r2, r2, #0x1c
    eor r0, r6
    lsr r2, r2, #0x1a
    lsl r0, r0, #2
    ldr r2, [r1, r2]
    ldr r0, [r1, r0]
    ldr r4, [r1, r5]
    eor r0, r2
    eor r0, r3
    eor r0, r4
    lsl r2, r0, #1
    lsr r0, r0, #0x1f
    orr r0, r2
    str r0, [r1, r5]
    ldr r0, [r1, r5]
    pop {r3, r4, r5, r6}
    bx lr
}
