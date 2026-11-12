/* ov006 row 0x021ecf68: 34 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x0c -> +0x1c
 *   back edge +0x1a -> +0x0e
 *   test +0x0a cmp r1, #0x0
 *   test +0x18 cmp r4, r1
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x021ecf68; the literal pool and
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



asm u32 native_ov006_021ecf68 (register u32 a0)
{
    push {r4, r5}
    mov r3, #0x0
    sub r2, r1, #0x1
    add r5, r0, r2
    add r4, r3, #0x0
    cmp r1, #0x0
    ble ov006_021ecf68_L1c
ov006_021ecf68_Le:
    ldrb r0, [r5, #0]
    lsl r2, r3, #0x8
    add r4, r4, #0x1
    sub r5, r5, #0x1
    add r3, r2, r0
    cmp r4, r1
    blt ov006_021ecf68_Le
ov006_021ecf68_L1c:
    add r0, r3, #0x0
    pop {r4, r5}
    bx lr
}
