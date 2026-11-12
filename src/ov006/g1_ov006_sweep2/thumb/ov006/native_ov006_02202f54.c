/* ov006 row 0x02202f54: 68 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x40 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   branch +0x06 -> +0x1c
 *   branch +0x22 -> +0x3a
 *   back edge +0x38 -> +0x28
 *   test +0x04 cmp r1, #0x0
 *   test +0x20 cmp r4, #0x0
 *   test +0x36 cmp r1, r5
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202f54; the literal pool and
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



asm u32 native_ov006_02202f54 (register u32 a0)
{
    push {r4, r5}
    ldr r3, [r0, #0x8]
    cmp r1, #0x0
    blt ov006_02202f54_L1c
    lsl r4, r1, #0x3
    add r0, r3, #0x4
    ldrh r3, [r0, r4]
    ldr r1, =0xfffff3ff
    and r3, r1
    lsl r1, r2, #0xa
    orr r1, r3
    strh r1, [r0, r4]
    pop {r4, r5}
    bx lr
ov006_02202f54_L1c:
    ldrb r4, [r0, #0xc]
    mov r1, #0x0
    cmp r4, #0x0
    ble ov006_02202f54_L3a
    ldr r4, =0xfffff3ff
    lsl r2, r2, #0xa
ov006_02202f54_L28:
    ldrh r5, [r3, #0x4]
    add r1, r1, #0x1
    and r5, r4
    orr r5, r2
    strh r5, [r3, #0x4]
    ldrb r5, [r0, #0xc]
    add r3, #0x8
    cmp r1, r5
    blt ov006_02202f54_L28
ov006_02202f54_L3a:
    pop {r4, r5}
    bx lr
    mov r8, r8
}
