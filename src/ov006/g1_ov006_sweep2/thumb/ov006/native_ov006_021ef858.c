/* ov006 row 0x021ef858: 110 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x38 -> +0x44
 *   back edge +0x42 -> +0x3a
 *   branch +0x60 -> +0x68
 *   test +0x36 cmp r0, r2
 *   test +0x40 cmp r4, r2
 *   test +0x5e cmp r1, r2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ef858; the literal pool and
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



asm u32 native_ov006_021ef858 (register u32 a0)
{
    push {r3, r4, r5, r6}
    ldrh r5, [r0, #0]
    mov r3, #0x0
    asr r4, r5, #0x8
    lsl r4, r4, #0x18
    lsr r6, r4, #0x18
    lsl r4, r5, #0x8
    mov r5, #0xff
    lsl r5, r5, #0x8
    and r4, r5
    orr r4, r6
    lsl r4, r4, #0x10
    lsr r4, r4, #0x10
    str r4, [r1, #0]
    ldrh r6, [r0, #0x2]
    asr r1, r6, #0x8
    lsl r1, r1, #0x18
    lsr r4, r1, #0x18
    lsl r1, r6, #0x8
    and r1, r5
    orr r1, r4
    lsl r1, r1, #0x10
    lsr r4, r1, #0x10
    add r1, r0, #0x6
    str r4, [r2, #0]
    add r2, r1, r4
    add r4, r0, #0x0
    cmp r0, r2
    bhs ov006_021ef858_L44
ov006_021ef858_L3a:
    ldrb r1, [r4, #0]
    add r4, r4, #0x1
    add r3, r3, r1
    cmp r4, r2
    blo ov006_021ef858_L3a
ov006_021ef858_L44:
    ldrh r5, [r2, #0]
    lsl r1, r3, #0x10
    lsr r1, r1, #0x10
    asr r2, r5, #0x8
    lsl r2, r2, #0x18
    lsr r4, r2, #0x18
    mov r2, #0xff
    lsl r3, r5, #0x8
    lsl r2, r2, #0x8
    and r2, r3
    orr r2, r4
    lsl r2, r2, #0x10
    lsr r2, r2, #0x10
    cmp r1, r2
    beq ov006_021ef858_L68
    mov r0, #0x0
    pop {r3, r4, r5, r6}
    bx lr
ov006_021ef858_L68:
    add r0, r0, #0x6
    pop {r3, r4, r5, r6}
    bx lr
}
