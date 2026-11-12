/* ov000 row 0x021df2d4: 232 bytes.
 *
 * What it does: 56 instructions; 3 call(s) to 0x0201f274, 0x0201f274, 0x021df370; loops (back edge at +0x14); returns through pop {r3, r4, r5, r6, r7, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe0 -> constant 0x66666667 (image word 0x66666667)
 *   pool +0xe4 -> native_data_0222e32c (image word 0x0222e32c)
 *   branch +0x34 -> +0x5c
 *   branch +0x40 -> +0x5c
 *   branch +0x4c -> +0x5c
 *   branch +0xc4 -> +0xd8
 *   back edge +0xd4 -> +0x9c
 *   test +0x28 cmp r7, #83
 *   test +0x38 cmp r7, #75
 *   test +0x44 cmp r7, #87
 *   test +0x50 cmp r7, #119
 *   test +0xa4 cmp r0, r2, lsr #29
 *   test +0xb0 cmpeq r2, r4, asr #24
 *   test +0xbc cmpeq r2, r1, asr #16
 *   test +0xcc cmp r12, #153
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021df2d4; the literal pool and
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

extern void native_fn_0201f274(void);
extern u8 native_data_0222e32c[];


asm u32 native_ov000_021df2d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    mov r6, r0
    add r0, r6, #1
    ldrsb r7, [r6]
    mvn r5, #0
    bl native_fn_0201f274
    mov r4, r0, lsl #24
    add r0, r6, #4
    bl native_fn_0201f274
    mov r0, r0, lsl #16
    cmp r7, #83
    mov r6, r0, asr #16
    moveq r0, #0
    beq ov000_021df2d4_L5c
    cmp r7, #75
    moveq r0, #1
    beq ov000_021df2d4_L5c
    cmp r7, #87
    moveq r0, #2
    beq ov000_021df2d4_L5c
    cmp r7, #119
    moveq r0, #2
    movne r0, r5
ov000_021df2d4_L5c:
    ldr r12, =0x66666667
    mov r1, r6, lsr #31
    smull r2, r14, r12, r6
    add lr, r1, lr, asr #2
    mov r3, #10
    smull r1, r2, r3, r14
    sub lr, r6, r1
    sub r1, r6, lr
    mov r1, r1, lsl #16
    mov r3, r1, asr #16
    smull r1, r2, r12, r3
    mov r1, r3, lsr #31
    add r2, r1, r2, asr #2
    ldr r6, =native_data_0222e32c
    mov r1, r2, lsl #16
    mov r12, #0
ov000_021df2d4_L9c:
    ldrh r3, [r6]
    mov r2, r3, lsl #29
    cmp r0, r2, lsr #29
    moveq r2, r3, lsl #25
    moveq r2, r2, lsr #28
    cmpeq r2, r4, asr #24
    moveq r2, r3, lsl #21
    moveq r2, r2, lsr #28
    cmpeq r2, r1, asr #16
    moveq r5, r12
    beq ov000_021df2d4_Ld8
    add r12, r12, #1
    cmp r12, #153
    add r6, r6, #14
    blt ov000_021df2d4_L9c
ov000_021df2d4_Ld8:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
