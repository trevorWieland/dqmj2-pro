/* ov006 row 0x022027dc: 168 bytes.
 *
 * What it does: Writes one block of 4 registers through a writeback base pointer.
 *
 * Decoded shape: block fill.
 *
 *   pool +0x98 -> constant 0x0221c16c (image word 0x0221c16c)
 *   pool +0x9c -> constant 0x00000a93 (image word 0x00000a93)
 *   pool +0xa0 -> constant 0x00000a94 (image word 0x00000a94)
 *   pool +0xa4 -> constant 0x00000202 (image word 0x00000202)
 *   branch +0x14 -> +0x8c
 *   branch +0x22 -> +0x8c
 *   branch +0x2a -> +0x6a
 *   branch +0x30 -> +0x94
 *   branch +0x46 -> +0x8c
 *   branch +0x5e -> +0x8c
 *   branch +0x68 -> +0x8c
 *   branch +0x74 -> +0x8c
 *   back edge +0x92 -> +0x08
 *   test +0x12 cmp r1, #0x0
 *   test +0x20 cmp r4, #0x1
 *   test +0x28 cmp r6, #0x1
 *   test +0x2e cmp r1, #0x10
 *   test +0x44 tst r2, r3
 *   test +0x5c cmp r1, #0x24
 *   test +0x72 cmp r1, #0xbd
 *   test +0x90 cmp r4, #0x10
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022027dc; the literal pool and
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



asm u32 native_ov006_022027dc (register u32 a0)
{
    push {r4, r5, r6, r7}
    mov r4, #0x0
    ldr r0, =0x0221c16c
    add r5, r4, #0x0
ov006_022027dc_L8:
    ldr r3, [r0, #0]
    mov r1, #0x82
    add r2, r3, r5
    lsl r1, r1, #0x2
    ldr r1, [r2, r1]
    cmp r1, #0x0
    beq ov006_022027dc_L8c
    mov r1, #0x1
    lsl r1, r1, #0x8
    add r2, r3, r1
    mov r1, #0x44
    mul r1, r4
    cmp r4, #0x1
    bne ov006_022027dc_L8c
    ldr r6, =0x00000a93
    ldrb r6, [r3, r6]
    cmp r6, #0x1
    bne ov006_022027dc_L6a
    ldrh r1, [r2, r1]
    cmp r1, #0x10
    bne ov006_022027dc_L94
    ldr r1, =0x00000a94
    ldr r1, [r3, r1]
    add r2, r1, #0x1
    ldr r1, =0x00000a94
    str r2, [r3, r1]
    ldr r1, [r0, #0]
    ldr r2, =0x00000a94
    ldr r3, [r1, r2]
    mov r2, #0x1
    tst r2, r3
    bne ov006_022027dc_L8c
    mov r2, #0x2
    lsl r2, r2, #0x8
    ldrh r2, [r1, r2]
    add r3, r2, #0x1
    mov r2, #0x2
    lsl r2, r2, #0x8
    strh r3, [r1, r2]
    ldr r3, [r0, #0]
    add r1, r2, #0x0
    ldrh r1, [r3, r1]
    cmp r1, #0x24
    blo ov006_022027dc_L8c
    mov r1, #0x2
    mov r2, #0x0
    lsl r1, r1, #0x8
    strh r2, [r3, r1]
    b ov006_022027dc_L8c
ov006_022027dc_L6a:
    ldr r6, =0x00000202
    mov r7, #0xbc
    strh r7, [r3, r6]
    ldrh r1, [r2, r1]
    cmp r1, #0xbd
    bne ov006_022027dc_L8c
    ldr r3, [r0, #0]
    ldr r1, =0x00000a93
    mov r2, #0x1
    strb r2, [r3, r1]
    ldr r3, [r0, #0]
    lsl r2, r2, #0x9
    mov r1, #0x0
    strh r1, [r3, r2]
    ldr r3, [r0, #0]
    ldr r2, =0x00000a94
    str r1, [r3, r2]
ov006_022027dc_L8c:
    add r4, r4, #0x1
    add r5, r5, #0x4
    cmp r4, #0x10
    blt ov006_022027dc_L8
ov006_022027dc_L94:
    pop {r4, r5, r6, r7}
    bx lr
}
