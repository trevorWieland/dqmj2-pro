/* ov006 row 0x021f5428: 28 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x10 -> +0x18
 *   test +0x0e cmp r2, #0x0
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f5428; the literal pool and
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



asm u32 native_ov006_021f5428 (register u32 a0)
{
    push {r4, r5}
    ldr r4, [r0, #0x4]
    ldr r5, [r0, #0]
    lsl r0, r1, #0x10
    lsr r0, r0, #0xe
    ldr r0, [r5, r0]
    add r0, r4, r0
    cmp r2, #0x0
    blt ov006_021f5428_L18
    add r3, #0x30
    lsl r1, r2, #0x1
    strh r3, [r0, r1]
ov006_021f5428_L18:
    pop {r4, r5}
    bx lr
}
