/* ov006 row 0x021f1f40: 52 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x16 -> +0x1c
 *   branch +0x1a -> +0x1e
 *   back edge +0x28 -> +0x14
 *   test +0x14 cmp r5, #0x9
 *   test +0x26 cmp r4, #0x2
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021f1f40; the literal pool and
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



asm u32 native_ov006_021f1f40 (register u32 a0)
{
    push {r4, r5}
    lsl r1, r1, #0x18
    lsr r3, r1, #0x18
    mov r1, #0xf0
    and r1, r3
    asr r5, r1, #0x4
    mov r1, #0xf
    add r2, r0, #0x0
    mov r4, #0x0
    and r1, r3
ov006_021f1f40_L14:
    cmp r5, #0x9
    bgt ov006_021f1f40_L1c
    add r5, #0x30
    b ov006_021f1f40_L1e
ov006_021f1f40_L1c:
    add r5, #0x37
ov006_021f1f40_L1e:
    add r4, r4, #0x1
    strb r5, [r2, #0]
    add r2, r2, #0x1
    add r5, r1, #0x0
    cmp r4, #0x2
    blt ov006_021f1f40_L14
    mov r1, #0x0
    strb r1, [r2, #0]
    sub r0, r2, r0
    pop {r4, r5}
    bx lr
}
