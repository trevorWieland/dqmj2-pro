/* ov006 row 0x022039a4: 220 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xcc -> constant 0x04001040 (image word 0x04001040)
 *   pool +0xd0 -> constant 0x04001042 (image word 0x04001042)
 *   pool +0xd4 -> constant 0x04000040 (image word 0x04000040)
 *   pool +0xd8 -> constant 0x04000042 (image word 0x04000042)
 *   branch +0x04 -> +0x68
 *   branch +0x0a -> +0x3a
 *   branch +0x6c -> +0x9c
 *   test +0x02 cmp r0, #0x1
 *   test +0x06 cmp r1, #0x0
 *   test +0x68 cmp r1, #0x0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x022039a4; the literal pool and
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



asm u32 native_ov006_022039a4 (register u32 a0)
{
    push {r4, r5}
    cmp r0, #0x1
    bne ov006_022039a4_L68
    cmp r1, #0x0
    ldrh r3, [r2, #0x6]
    bne ov006_022039a4_L3a
    ldrh r0, [r2, #0]
    mov r4, #0xff
    ldrh r1, [r2, #0x2]
    lsl r0, r0, #0x8
    add r5, r0, #0x0
    ldrh r0, [r2, #0x4]
    lsl r4, r4, #0x8
    and r5, r4
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    add r2, r5, #0x0
    orr r2, r0
    ldr r0, =0x04001040
    lsl r1, r1, #0x8
    strh r2, [r0, #0]
    add r2, r1, #0x0
    lsl r1, r3, #0x18
    and r2, r4
    lsr r1, r1, #0x18
    orr r1, r2
    strh r1, [r0, #0x4]
    pop {r4, r5}
    bx lr
ov006_022039a4_L3a:
    ldrh r0, [r2, #0]
    mov r4, #0xff
    ldrh r1, [r2, #0x2]
    lsl r0, r0, #0x8
    add r5, r0, #0x0
    ldrh r0, [r2, #0x4]
    lsl r4, r4, #0x8
    and r5, r4
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    add r2, r5, #0x0
    orr r2, r0
    ldr r0, =0x04001042
    lsl r1, r1, #0x8
    strh r2, [r0, #0]
    add r2, r1, #0x0
    lsl r1, r3, #0x18
    and r2, r4
    lsr r1, r1, #0x18
    orr r1, r2
    strh r1, [r0, #0x4]
    pop {r4, r5}
    bx lr
ov006_022039a4_L68:
    cmp r1, #0x0
    ldrh r3, [r2, #0x6]
    bne ov006_022039a4_L9c
    ldrh r0, [r2, #0]
    mov r4, #0xff
    ldrh r1, [r2, #0x2]
    lsl r0, r0, #0x8
    add r5, r0, #0x0
    ldrh r0, [r2, #0x4]
    lsl r4, r4, #0x8
    and r5, r4
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    add r2, r5, #0x0
    orr r2, r0
    ldr r0, =0x04000040
    lsl r1, r1, #0x8
    strh r2, [r0, #0]
    add r2, r1, #0x0
    lsl r1, r3, #0x18
    and r2, r4
    lsr r1, r1, #0x18
    orr r1, r2
    strh r1, [r0, #0x4]
    pop {r4, r5}
    bx lr
ov006_022039a4_L9c:
    ldrh r0, [r2, #0]
    mov r4, #0xff
    ldrh r1, [r2, #0x2]
    lsl r0, r0, #0x8
    add r5, r0, #0x0
    ldrh r0, [r2, #0x4]
    lsl r4, r4, #0x8
    and r5, r4
    lsl r0, r0, #0x18
    lsr r0, r0, #0x18
    add r2, r5, #0x0
    orr r2, r0
    ldr r0, =0x04000042
    lsl r1, r1, #0x8
    strh r2, [r0, #0]
    add r2, r1, #0x0
    lsl r1, r3, #0x18
    and r2, r4
    lsr r1, r1, #0x18
    orr r1, r2
    strh r1, [r0, #0x4]
    pop {r4, r5}
    bx lr
    mov r8, r8
}
