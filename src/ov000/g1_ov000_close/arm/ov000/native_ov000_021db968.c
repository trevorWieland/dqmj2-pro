/* ov000 row 0x021db968: 488 bytes.
 *
 * What it does: 122 instructions; 6 call(s) to 0x021dba18, 0x021db92c, 0x021dbab0, +3 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x2c -> +0xb0
 *   branch +0x44 -> +0xb0
 *   branch +0x98 -> +0xb0
 *   branch +0xc4 -> +0x148
 *   branch +0xdc -> +0x148
 *   branch +0x130 -> +0x148
 *   branch +0x15c -> +0x1e0
 *   branch +0x174 -> +0x1e0
 *   branch +0x1c8 -> +0x1e0
 *   test +0x18 cmp r7, r5
 *   test +0x28 cmp r9, #0
 *   test +0x40 cmp r0, #0
 *   test +0xa4 cmp r0, r5
 *   test +0xb0 cmp r7, r5
 *   test +0xc0 cmp r9, #0
 *   test +0xd8 cmp r0, #0
 *   test +0x13c cmp r0, r5
 *   test +0x148 cmp r7, r5
 *   test +0x158 cmp r4, #0
 *   test +0x170 cmp r0, #0
 *   test +0x1d4 cmp r0, r5
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021db968; the literal pool and
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

extern void native_fn_021db92c(void);


asm u32 native_ov000_021db968 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r5, [sp, #0x28]
    mov r7, r3
    ldr r6, [sp, #0x24]
    mov r8, r2
    add r4, r1, r0, lsl #3
    cmp r7, r5
    movge r0, r7
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    ldrsh r9, [r4]
    cmp r9, #0
    blt ov000_021db968_Lb0
    mov r0, r9
    mov r1, r8
    mov r2, r7
    bl native_fn_021db92c
    cmp r0, #0
    bne ov000_021db968_Lb0
    ldr r1, [sp, #0x20]
    mov r0, #68
    smlabb r0, r9, r0, r1
    ldr r2, [r6, #0x4]
    ldr r1, [r0, #0x34]
    ldr lr, [r6]
    sub r3, r2, r1
    smull r2, r1, r3, r3
    ldr r12, [r0, #0x30]
    ldr r3, [r6, #0x8]
    sub r12, lr, r12
    ldr r0, [r0, #0x38]
    smlal r2, r1, r12, r12
    sub r0, r3, r0
    smlal r2, r1, r0, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    subs r0, r0, #1048576
    mov r0, #0
    rscs r0, r0, r1, asr #12
    bge ov000_021db968_Lb0
    mov r1, r7, lsl #1
    add r0, r7, #1
    cmp r0, r5
    strh r9, [r8, r1]
    movlt r7, r0
ov000_021db968_Lb0:
    cmp r7, r5
    movge r0, r7
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    ldrsh r9, [r4, #2]
    cmp r9, #0
    blt ov000_021db968_L148
    mov r0, r9
    mov r1, r8
    mov r2, r7
    bl native_fn_021db92c
    cmp r0, #0
    bne ov000_021db968_L148
    ldr r1, [sp, #0x20]
    mov r0, #68
    smlabb r0, r9, r0, r1
    ldr r2, [r6, #0x4]
    ldr r1, [r0, #0x34]
    ldr lr, [r6]
    sub r3, r2, r1
    smull r2, r1, r3, r3
    ldr r12, [r0, #0x30]
    ldr r3, [r6, #0x8]
    sub r12, lr, r12
    ldr r0, [r0, #0x38]
    smlal r2, r1, r12, r12
    sub r0, r3, r0
    smlal r2, r1, r0, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    subs r0, r0, #1048576
    mov r0, #0
    rscs r0, r0, r1, asr #12
    bge ov000_021db968_L148
    mov r1, r7, lsl #1
    add r0, r7, #1
    cmp r0, r5
    strh r9, [r8, r1]
    movlt r7, r0
ov000_021db968_L148:
    cmp r7, r5
    movge r0, r7
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
    ldrsh r4, [r4, #4]
    cmp r4, #0
    blt ov000_021db968_L1e0
    mov r0, r4
    mov r1, r8
    mov r2, r7
    bl native_fn_021db92c
    cmp r0, #0
    bne ov000_021db968_L1e0
    ldr r1, [sp, #0x20]
    mov r0, #68
    smlabb r0, r4, r0, r1
    ldr r2, [r6, #0x4]
    ldr r1, [r0, #0x34]
    ldr r12, [r6]
    sub r3, r2, r1
    smull r2, r1, r3, r3
    ldr r9, [r0, #0x30]
    ldr r3, [r6, #0x8]
    sub r6, r12, r9
    ldr r0, [r0, #0x38]
    smlal r2, r1, r6, r6
    sub r0, r3, r0
    smlal r2, r1, r0, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    subs r0, r0, #1048576
    mov r0, #0
    rscs r0, r0, r1, asr #12
    bge ov000_021db968_L1e0
    mov r1, r7, lsl #1
    add r0, r7, #1
    cmp r0, r5
    strh r4, [r8, r1]
    movlt r7, r0
ov000_021db968_L1e0:
    mov r0, r7
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
