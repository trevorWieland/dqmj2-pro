/* ov000 row 0x021e60e0: 52 bytes.
 *
 * Decoded shape: guarded entry: bxeq at +0x18 returns before the body.
 *
 *   pool +0x30 -> native_data_02232568 (image word 0x02232568)
 *   back edge +0x28 -> +0x0c
 *   test +0x10 cmp r1, #0
 *   test +0x20 cmp r2, #0x10
 *   memory +0x0c ldrb r1, [r3]
 *
 * Why transcribed rather than written as C: scan rotated with an entry test the image does not have (43-byte
 * diff)
 * Recorded in docs/authoring/2026-11-11-ov000-pass2.md.
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e60e0; the literal pool and
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

extern u8 native_data_02232568[];


asm u32 native_ov000_021e60e0 (register u32 a0)
{
    mov r0, #0
    ldr r3, =native_data_02232568
    mov r2, r0
ov000_021e60e0_Lc:
    ldrb r1, [r3]
    cmp r1, #0
    moveq r0, r3
    bxeq lr
    add r2, r2, #1
    cmp r2, #0x10
    add r3, r3, #0x10
    blt ov000_021e60e0_Lc
    bx lr
}
