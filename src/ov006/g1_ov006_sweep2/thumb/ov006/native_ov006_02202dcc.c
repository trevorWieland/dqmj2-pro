/* ov006 row 0x02202dcc: 132 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x80 -> constant 0xc1fffcff (image word 0xc1fffcff)
 *   branch +0x0a -> +0x40
 *   branch +0x12 -> +0x2c
 *   branch +0x1a -> +0x2c
 *   branch +0x46 -> +0x7c
 *   branch +0x50 -> +0x66
 *   branch +0x58 -> +0x66
 *   branch +0x64 -> +0x72
 *   back edge +0x7a -> +0x4e
 *   test +0x08 cmp r1, #0x0
 *   test +0x10 cmp r0, r2
 *   test +0x18 cmp r0, r2
 *   test +0x44 cmp r1, #0x0
 *   test +0x4e cmp r0, r1
 *   test +0x56 cmp r0, r6
 *   test +0x78 cmp r2, r6
 *   0 block transfer(s), 4 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202dcc; the literal pool and
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



asm u32 native_ov006_02202dcc (register u32 a0)
{
    push {r4, r5, r6, r7}
    add r4, r0, #0x0
    add r0, r2, #0x0
    ldr r5, [r4, #0x8]
    cmp r1, #0x0
    blt ov006_02202dcc_L40
    mov r2, #0x1
    lsl r2, r2, #0x8
    cmp r0, r2
    beq ov006_02202dcc_L2c
    mov r2, #0x3
    lsl r2, r2, #0x8
    cmp r0, r2
    beq ov006_02202dcc_L2c
    lsl r3, r1, #0x3
    ldr r2, [r5, r3]
    ldr r1, =0xc1fffcff
    and r1, r2
    orr r0, r1
    str r0, [r5, r3]
    pop {r4, r5, r6, r7}
    bx lr
ov006_02202dcc_L2c:
    lsl r1, r1, #0x3
    lsl r4, r3, #0x19
    ldr r3, [r5, r1]
    ldr r2, =0xc1fffcff
    and r2, r3
    orr r0, r2
    orr r0, r4
    str r0, [r5, r1]
    pop {r4, r5, r6, r7}
    bx lr
ov006_02202dcc_L40:
    ldrb r1, [r4, #0xc]
    mov r2, #0x0
    cmp r1, #0x0
    ble ov006_02202dcc_L7c
    mov r1, #0x1
    lsl r3, r3, #0x19
    lsl r1, r1, #0x8
ov006_02202dcc_L4e:
    cmp r0, r1
    beq ov006_02202dcc_L66
    mov r6, #0x3
    lsl r6, r6, #0x8
    cmp r0, r6
    beq ov006_02202dcc_L66
    ldr r7, [r5, #0]
    ldr r6, =0xc1fffcff
    and r6, r7
    orr r6, r0
    str r6, [r5, #0]
    b ov006_02202dcc_L72
ov006_02202dcc_L66:
    ldr r7, [r5, #0]
    ldr r6, =0xc1fffcff
    and r6, r7
    orr r6, r0
    orr r6, r3
    str r6, [r5, #0]
ov006_02202dcc_L72:
    ldrb r6, [r4, #0xc]
    add r2, r2, #0x1
    add r5, #0x8
    cmp r2, r6
    blt ov006_02202dcc_L4e
ov006_02202dcc_L7c:
    pop {r4, r5, r6, r7}
    bx lr
}
