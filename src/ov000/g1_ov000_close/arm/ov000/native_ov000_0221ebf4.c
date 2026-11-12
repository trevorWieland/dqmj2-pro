/* ov000 row 0x0221ebf4: 352 bytes.
 *
 * What it does: 87 instructions; 5 call(s) to 0x0221ec9c, 0x0205e7a8, 0x0221ecf8, +2 more; loops (back edge at +0xb0); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x15c -> constant 0x022463a0 (image word 0x022463a0)
 *   branch +0x20 -> +0xb8
 *   branch +0x80 -> +0xa8
 *   branch +0x88 -> +0xa8
 *   branch +0xb4 -> +0x150
 *   branch +0xd0 -> +0x104
 *   back edge +0x100 -> +0xe8
 *   branch +0x108 -> +0x134
 *   back edge +0x130 -> +0x110
 *   test +0x1c cmp r1, #0
 *   test +0x7c cmp r2, r1
 *   test +0x84 cmp lr, #0
 *   test +0xa0 cmp r3, r1
 *   test +0xcc cmp r12, r1
 *   test +0xec cmp r2, r3
 *   test +0xfc cmp r12, r1
 *   test +0x104 cmp r0, r1
 *   test +0x12c cmp r0, r1
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221ebf4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0205e7a8(void);


asm u32 native_ov000_0221ebf4 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r2, =0x022463a0
    ldr r1, [r0]
    ldr r12, [r2, #0xc]
    rsb r3, r1, r1, lsl #3
    add r4, r12, #3
    ldrb r1, [r4, r3]
    cmp r1, #0
    bne ov000_0221ebf4_Lb8
    ldrsb r1, [r2, #2]
    mov r3, #1
    sub r1, r1, #1
    strb r1, [r2, #0x2]
    ldr r1, [r0]
    rsb r1, r1, r1, lsl #3
    add r1, r12, r1
    strb r3, [r1, #0x3]
    ldr r1, [r0]
    ldr r4, [r2, #0xc]
    rsb r3, r1, r1, lsl #3
    add r1, r4, r3
    ldrsb lr, [r2, #2]
    ldr r12, [r2, #0x4]
    ldrb r2, [r4, r3]
    ldrb r1, [r1, #0x1]
    add r3, r12, lr, lsl #1
    strb r2, [r12, lr, lsl #1]
    strb r1, [r3, #0x1]
    ldrh r1, [r0, #14]
    ldr r2, [r0]
    sub r1, r1, #1
    cmp r2, r1
    bge ov000_0221ebf4_La8
    cmp lr, #0
    ble ov000_0221ebf4_La8
    add r3, r2, #1
    str r3, [r0]
    ldrh r2, [r0, #12]
    ldr r1, [r0, #0x4]
    add r1, r1, r2
    cmp r3, r1
    strge r1, [r0, #0x4]
ov000_0221ebf4_La8:
    mvn r0, #0
    mov r1, #82
    bl native_fn_0205e7a8
    b ov000_0221ebf4_L150
ov000_0221ebf4_Lb8:
    mov r1, #0
    strb r1, [r4, r3]
    ldrsb r3, [r2, #1]
    ldrsb r1, [r2, #2]
    sub r12, r3, #1
    cmp r12, r1
    blt ov000_0221ebf4_L104
    ldr r3, [r0]
    ldr r4, [r2, #0xc]
    rsb r3, r3, r3, lsl #3
    ldrb r3, [r4, r3]
    ldr r4, [r2, #0x4]
ov000_0221ebf4_Le8:
    ldrb r2, [r4, r12, lsl #1]
    cmp r2, r3
    moveq r0, r12
    moveq r12, r1
    sub r12, r12, #1
    cmp r12, r1
    bge ov000_0221ebf4_Le8
ov000_0221ebf4_L104:
    cmp r0, r1
    ble ov000_0221ebf4_L134
    ldr r2, =0x022463a0
ov000_0221ebf4_L110:
    ldr r4, [r2, #0x4]
    add lr, r4, r0, lsl #1
    ldrb r12, [lr, #-0x2]
    ldrb r3, [lr, #-0x1]
    strb r12, [r4, r0, lsl #1]
    sub r0, r0, #1
    strb r3, [lr, #0x1]
    cmp r0, r1
    bgt ov000_0221ebf4_L110
ov000_0221ebf4_L134:
    ldr r2, =0x022463a0
    mvn r0, #0
    ldrsb r3, [r2, #2]
    mov r1, #83
    add r3, r3, #1
    strb r3, [r2, #0x2]
    bl native_fn_0205e7a8
ov000_0221ebf4_L150:
    ldr r0, =0x022463a0
    ldrsb r0, [r0, #2]
    ldmia sp!, {r4, pc}
}
