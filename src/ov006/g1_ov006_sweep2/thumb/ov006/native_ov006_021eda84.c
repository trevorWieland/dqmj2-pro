/* ov006 row 0x021eda84: 36 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x0c -> +0x20
 *   back edge +0x1e -> +0x10
 *   test +0x0a cmp r4, #0x0
 *   test +0x1c cmp r3, r4
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021eda84; the literal pool and
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



asm u32 native_ov006_021eda84 (register u32 a0)
{
    push {r4, r5}
    lsr r3, r2, #0x1f
    add r3, r2, r3
    asr r4, r3, #0x1
    mov r3, #0x0
    cmp r4, #0x0
    ble ov006_021eda84_L20
    add r5, r1, r4
ov006_021eda84_L10:
    ldrsb r1, [r0, r3]
    ldrb r2, [r5, #0]
    add r3, r3, #0x1
    eor r1, r2
    strb r1, [r5, #0]
    add r5, r5, #0x1
    cmp r3, r4
    blt ov006_021eda84_L10
ov006_021eda84_L20:
    pop {r4, r5}
    bx lr
}
