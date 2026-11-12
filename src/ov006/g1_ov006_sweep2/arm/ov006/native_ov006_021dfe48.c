/* ov006 row 0x021dfe48: 44 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x28 -> constant 0x0220f614 (image word 0x0220f614)
 *   back edge +0x20 -> +0x0c
 *   test +0x1c cmp r3, #4
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021dfe48; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity proves the instruction stream, not the meaning of the fields, blocks and callee contracts it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;



asm u32 native_ov006_021dfe48 (register u32 a0)
{
    mov r3, #0
    ldr r1, =0x0220f614
    mov r2, r3
ov006_021dfe48_Lc:
    str r2, [r1, r3, lsl #4]
    add r0, r1, r3, lsl #4
    add r3, r3, #1
    str r2, [r0, #0x4]
    cmp r3, #4
    blt ov006_021dfe48_Lc
    bx lr
}
