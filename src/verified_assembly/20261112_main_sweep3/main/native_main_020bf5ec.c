/* main row 0x020bf5ec: 48 bytes.
 *
 * What it does: 4 loads, 0 stores; 1 local pool word (0x021d4bec); returns to its caller
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x2c -> constant 0x021d4bec (image word 0x021d4bec)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020bf5ec; the literal pool and
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



asm u32 native_main_020bf5ec (register u32 a0)
{
    ldr r1, =0x021d4bec
    ldrb r2, [r0, #2]
    ldrb r3, [r1, #4]
    mov r1, #6
    smulbb r2, r2, r1
    smulbb r3, r3, r1
    add r1, r2, r2, lsr #31
    ldrb r2, [r0, #3]
    add r0, r3, r1, asr #1
    add r0, r2, r0
    bx lr
}
