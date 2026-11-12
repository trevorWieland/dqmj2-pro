/* ov006 row 0x021ef8c8: 78 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x08 -> +0x10
 *   test +0x06 cmp r0, r1
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef8c8; the literal pool and
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



asm u32 native_ov006_021ef8c8 (register u32 a0)
{
    push {r3, r4, r5, r6}
    add r4, r0, #0x0
    ldr r0, [r4, #0]
    cmp r0, r1
    blo ov006_021ef8c8_L10
    mov r0, #0x0
    pop {r3, r4, r5, r6}
    bx lr
ov006_021ef8c8_L10:
    ldrh r5, [r0, #0]
    asr r1, r5, #0x8
    lsl r1, r1, #0x18
    lsr r6, r1, #0x18
    lsl r1, r5, #0x8
    mov r5, #0xff
    lsl r5, r5, #0x8
    and r1, r5
    orr r1, r6
    lsl r1, r1, #0x10
    lsr r1, r1, #0x10
    str r1, [r2, #0]
    ldrh r6, [r0, #0x2]
    add r0, r0, #0x4
    asr r1, r6, #0x8
    lsl r1, r1, #0x18
    lsr r2, r1, #0x18
    lsl r1, r6, #0x8
    and r1, r5
    orr r1, r2
    lsl r1, r1, #0x10
    lsr r2, r1, #0x10
    str r2, [r3, #0]
    add r2, #0xb
    mov r1, #0x7
    bic r2, r1
    sub r1, r2, #0x4
    add r1, r0, r1
    str r1, [r4, #0]
    pop {r3, r4, r5, r6}
    bx lr
}
