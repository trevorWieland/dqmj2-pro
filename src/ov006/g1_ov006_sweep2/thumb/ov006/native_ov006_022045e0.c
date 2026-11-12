/* ov006 row 0x022045e0: 40 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x08 -> +0x1c
 *   branch +0x10 -> +0x1c
 *   back edge +0x1a -> +0x0c
 *   test +0x06 cmp r3, #0x0
 *   test +0x0e cmp r2, #0x0
 *   test +0x18 cmp r4, r3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022045e0; the literal pool and
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



asm u32 native_ov006_022045e0 (register u32 a0)
{
    push {r4, r5}
    sub r3, r2, #0x1
    mov r4, #0x0
    cmp r3, #0x0
    ble ov006_022045e0_L1c
    add r5, r0, #0x0
ov006_022045e0_Lc:
    ldrb r2, [r1, r4]
    cmp r2, #0x0
    beq ov006_022045e0_L1c
    add r4, r4, #0x1
    strh r2, [r5, #0]
    add r5, r5, #0x2
    cmp r4, r3
    blt ov006_022045e0_Lc
ov006_022045e0_L1c:
    mov r2, #0x0
    lsl r1, r4, #0x1
    strh r2, [r0, r1]
    add r0, r4, #0x0
    pop {r4, r5}
    bx lr
}
