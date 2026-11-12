/* ov000 row 0x022127c4: 64 bytes.
 *
 * Decoded shape: loop with no calls.
 *
 *   pool +0x3c -> native_data_0224373c (image word 0x0224373c)
 *   pool +0x3c -> native_data_0224373c (image word 0x0224373c)
 *   back edge +0x34 -> +0x0c
 *   test +0x10 cmp r1, #0
 *   test +0x2c cmp r2, #8
 *   memory +0x0c ldrb r1, [r3, #0xdc]
 *
 * Why transcribed rather than written as C: matched-record return recomputed from the wrong live index
 * (46-byte diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x022127c4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts
 * the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern u8 native_data_0224373c[];


asm u32 native_ov000_022127c4 (register u32 a0)
{
    mov r0, #0
    ldr r3, =native_data_0224373c
    mov r2, r0
ov000_022127c4_Lc:
    ldrb r1, [r3, #0xdc]
    cmp r1, #0
    bne ov000_022127c4_L28
    ldr r1, =native_data_0224373c
    mov r0, #0xe0
    mla r0, r2, r0, r1
    bx lr
ov000_022127c4_L28:
    add r2, r2, #1
    cmp r2, #8
    add r3, r3, #0xe0
    blt ov000_022127c4_Lc
    bx lr
}
