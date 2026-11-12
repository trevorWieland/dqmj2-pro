/* ov006 row 0x02202e50: 96 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x58 -> constant 0xfffff3ff (image word 0xfffff3ff)
 *   pool +0x5c -> constant 0xffff0fff (image word 0xffff0fff)
 *   branch +0x08 -> +0x2a
 *   branch +0x30 -> +0x54
 *   back edge +0x52 -> +0x3a
 *   test +0x06 cmp r1, #0x0
 *   test +0x2e cmp r1, #0x0
 *   test +0x50 cmp r0, r7
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202e50; the literal pool and
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



asm u32 native_ov006_02202e50 (register u32 a0)
{
    push {r4, r5, r6, r7}
    add r5, r0, #0x0
    ldr r4, [r5, #0x8]
    cmp r1, #0x0
    blt ov006_02202e50_L2a
    lsl r0, r1, #0x3
    ldr r5, [r4, r0]
    ldr r1, =0xfffff3ff
    and r5, r1
    lsl r1, r2, #0xa
    orr r1, r5
    str r1, [r4, r0]
    add r4, r4, #0x4
    ldrh r2, [r4, r0]
    ldr r1, =0xffff0fff
    and r2, r1
    lsl r1, r3, #0xc
    orr r1, r2
    strh r1, [r4, r0]
    pop {r4, r5, r6, r7}
    bx lr
ov006_02202e50_L2a:
    ldrb r1, [r5, #0xc]
    mov r0, #0x0
    cmp r1, #0x0
    ble ov006_02202e50_L54
    lsl r1, r2, #0xa
    lsl r2, r3, #0xc
    ldr r3, =0xfffff3ff
    ldr r6, =0xffff0fff
ov006_02202e50_L3a:
    ldr r7, [r4, #0]
    add r0, r0, #0x1
    and r7, r3
    orr r7, r1
    str r7, [r4, #0]
    ldrh r7, [r4, #0x4]
    and r7, r6
    orr r7, r2
    strh r7, [r4, #0x4]
    ldrb r7, [r5, #0xc]
    add r4, #0x8
    cmp r0, r7
    blt ov006_02202e50_L3a
ov006_02202e50_L54:
    pop {r4, r5, r6, r7}
    bx lr
}
