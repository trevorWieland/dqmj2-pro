/* ov000 row 0x0221ed54: 180 bytes.
 *
 * What it does: 44 instructions; 3 call(s) to 0x0221ed88, 0x0205e7a8, 0x0205e7a8; loops (back edge at +0x28); returns through pop {r4, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xb0 -> constant 0x022463a0 (image word 0x022463a0)
 *   branch +0x14 -> +0x34
 *   branch +0x1c -> +0x2c
 *   branch +0x44 -> +0x74
 *   branch +0x60 -> +0x74
 *   back edge +0x70 -> +0x54
 *   branch +0x98 -> +0xa8
 *   test +0x10 cmp r3, r2
 *   test +0x18 cmp r1, #0
 *   test +0x40 cmp r2, #0
 *   test +0x58 cmp r0, r3
 *   test +0x6c cmp r0, #0
 *   test +0x8c cmp r1, #0
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221ed54; the literal pool and
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


asm u32 native_ov000_0221ed54 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    ldr r0, =0x022463a0
    ldrsb r3, [r0, #2]
    ldrsb r2, [r0, #1]
    cmp r3, r2
    blt ov000_0221ed54_L34
    cmp r1, #0
    beq ov000_0221ed54_L2c
    mvn r0, #0
    mov r1, #83
    bl native_fn_0205e7a8
ov000_0221ed54_L2c:
    mov r0, #1
    ldmia sp!, {r4, pc}
ov000_0221ed54_L34:
    ldr r4, [r0, #0xc]
    mov r12, #0
    ldrb r2, [r4]
    cmp r2, #0
    beq ov000_0221ed54_L74
    ldr r0, [r0, #0x4]
    mov r2, r4
    ldrb r3, [r0, r3, lsl #1]
ov000_0221ed54_L54:
    ldrb r0, [r2]
    cmp r0, r3
    moveq lr, r12
    beq ov000_0221ed54_L74
    ldrb r0, [r2, #0x7]!
    add r12, r12, #1
    cmp r0, #0
    bne ov000_0221ed54_L54
ov000_0221ed54_L74:
    rsb r0, lr, lr, lsl #3
    add r2, r4, r0
    mov r3, #0
    ldr r0, =0x022463a0
    strb r3, [r2, #0x3]
    ldrsb r2, [r0, #2]
    cmp r1, #0
    add r1, r2, #1
    strb r1, [r0, #0x2]
    beq ov000_0221ed54_La8
    sub r0, r3, #1
    mov r1, #83
    bl native_fn_0205e7a8
ov000_0221ed54_La8:
    mov r0, #0
    ldmia sp!, {r4, pc}
}
