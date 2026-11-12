/* ov006 row 0x02202eb0: 164 bytes.
 *
 * What it does: Copies a measured block.
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x9c -> constant 0xfe00ff00 (image word 0xfe00ff00)
 *   pool +0xa0 -> constant 0x01ff0000 (image word 0x01ff0000)
 *   branch +0x0e -> +0x2a
 *   branch +0x5c -> +0x96
 *   back edge +0x90 -> +0x60
 *   test +0x0c cmp r1, #0x0
 *   test +0x5a cmp r0, #0x1
 *   test +0x8e cmp r2, r0
 *   0 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02202eb0; the literal pool and
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



asm u32 native_ov006_02202eb0 (register u32 a0)
{
    push {r3, r4, r5, r6, r7, lr}
    sub sp, #0x10
    mov lr, r0
    add r0, r3, #0x0
    mov r3, lr
    ldr r3, [r3, #0x8]
    cmp r1, #0x0
    blt ov006_02202eb0_L2a
    lsl r4, r1, #0x3
    lsl r1, r2, #0x17
    lsl r0, r0, #0x18
    ldr r5, [r3, r4]
    ldr r2, =0xfe00ff00
    lsr r0, r0, #0x18
    and r2, r5
    lsr r1, r1, #0x7
    orr r0, r2
    orr r0, r1
    add sp, #0x10
    str r0, [r3, r4]
    pop {r3, r4, r5, r6, r7, pc}
ov006_02202eb0_L2a:
    ldr r5, [r3, #0]
    ldr r1, =0x01ff0000
    and r1, r5
    lsr r4, r1, #0x10
    lsl r1, r5, #0x18
    lsr r7, r1, #0x18
    lsl r1, r2, #0x17
    lsr r6, r1, #0x7
    ldr r5, [r3, #0]
    ldr r1, =0xfe00ff00
    str r7, [sp, #0x8]
    and r1, r5
    lsl r5, r0, #0x18
    lsr r5, r5, #0x18
    orr r1, r5
    orr r1, r6
    str r1, [r3, #0]
    sub r1, r2, r4
    sub r7, r0, r7
    mov r0, lr
    ldrb r0, [r0, #0xc]
    mov r2, #0x1
    str r4, [sp, #0xc]
    mov r12, r1
    cmp r0, #0x1
    ble ov006_02202eb0_L96
    add r3, #0x8
ov006_02202eb0_L60:
    ldr r0, [r3, #0]
    ldr r1, =0x01ff0000
    ldr r4, [r3, #0]
    and r1, r0
    lsl r0, r0, #0x18
    lsr r5, r0, #0x18
    lsr r1, r1, #0x10
    mov r0, r12
    add r0, r1, r0
    lsl r0, r0, #0x17
    lsr r6, r0, #0x7
    ldr r0, =0xfe00ff00
    add r2, r2, #0x1
    and r0, r4
    add r4, r5, r7
    lsl r4, r4, #0x18
    lsr r4, r4, #0x18
    orr r0, r4
    orr r0, r6
    str r0, [r3, #0]
    mov r0, lr
    ldrb r0, [r0, #0xc]
    add r3, #0x8
    cmp r2, r0
    blt ov006_02202eb0_L60
    str r5, [sp]
    str r1, [sp, #0x4]
ov006_02202eb0_L96:
    add sp, #0x10
    pop {r3, r4, r5, r6, r7, pc}
    mov r8, r8
}
