/* ov000 row 0x021dcf94: 476 bytes.
 *
 * What it does: 119 instructions; 4 call(s) to 0x021dcd34, 0x0200236c, 0x021dd024, +1 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x2c -> +0x1d0
 *   branch +0x84 -> +0x90
 *   branch +0x94 -> +0xac
 *   branch +0xa8 -> +0xd8
 *   branch +0xb0 -> +0xc8
 *   branch +0xc4 -> +0xd8
 *   test +0x7c cmp r8, #100
 *   test +0x88 cmp r8, #400
 *   test +0x90 cmp r7, #0
 *   test +0xac cmp r7, #1
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dcf94; the literal pool and
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

extern void native_fn_021dcd34(void);
extern void native_fn_0200236c(void);
extern void native_fn_02002618(void);


asm u32 native_ov000_021dcf94 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #28
    ldr r7, [sp, #0x38]
    mov r4, r3
    add r3, sp, #16
    mov r6, r0
    mov r5, r1
    mov r9, r2
    str r7, [sp]
    bl native_fn_021dcd34
    movs r7, r0
    bmi ov000_021dcf94_L1d0
    ldr r2, [r6]
    ldr r1, [r5]
    ldr r3, [r6, #0x8]
    ldr r0, [r5, #0x8]
    sub r2, r2, r1
    sub r0, r3, r0
    smull r1, r3, r2, r2
    adds r8, r1, #2048
    smull r2, r1, r0, r0
    adc r3, r3, #0
    adds r2, r2, #2048
    mov r8, r8, lsr #12
    adc r0, r1, #0
    mov r1, r2, lsr #12
    orr r8, r8, r3, lsl #20
    orr r1, r1, r0, lsl #20
    add r0, r8, r1
    bl native_fn_0200236c
    mov r8, r0
    cmp r8, #100
    movlt r8, #100
    blt ov000_021dcf94_L90
    cmp r8, #400
    movgt r8, #400
ov000_021dcf94_L90:
    cmp r7, #0
    bne ov000_021dcf94_Lac
    ldr r1, [r9]
    ldr r3, [r9, #0x8]
    ldr r2, [r9, #0xc]
    ldr r9, [r9, #0x14]
    b ov000_021dcf94_Ld8
ov000_021dcf94_Lac:
    cmp r7, #1
    bne ov000_021dcf94_Lc8
    ldr r1, [r9, #0xc]
    ldr r3, [r9, #0x14]
    ldr r2, [r9, #0x18]
    ldr r9, [r9, #0x20]
    b ov000_021dcf94_Ld8
ov000_021dcf94_Lc8:
    ldr r1, [r9, #0x18]
    ldr r3, [r9, #0x20]
    ldr r2, [r9]
    ldr r9, [r9, #0x8]
ov000_021dcf94_Ld8:
    sub r7, r2, r1
    sub r2, r9, r3
    add r0, sp, #4
    mov r3, #0
    mov r1, r0
    str r7, [sp, #0x4]
    str r3, [sp, #0x8]
    str r2, [sp, #0xc]
    bl native_fn_02002618
    ldr r2, [r6]
    ldr r1, [r5]
    ldr r3, [r6, #0x8]
    sub r1, r2, r1
    ldr r0, [sp, #0x4]
    ldr r2, [r5, #0x8]
    smull r9, r7, r0, r1
    ldr r6, [sp, #0xc]
    sub r1, r3, r2
    smlal r9, r7, r6, r1
    adds r2, r9, #2048
    adc r1, r7, #0
    mov r2, r2, lsr #12
    orrs r2, r2, r1, lsl #20
    rsbmi r8, r8, #0
    umull r3, r6, r8, r0
    mov r7, r0, asr #31
    mla r6, r8, r7, r6
    mov r7, r8, asr #31
    ldr r1, [sp, #0x8]
    adds r9, r3, #2048
    mla r6, r7, r0, r6
    smull r0, r3, r8, r1
    adc r7, r6, #0
    adds r6, r0, #2048
    ldr r2, [sp, #0xc]
    mov r1, r9, lsr #12
    orr r1, r1, r7, lsl #20
    smull r2, r0, r8, r2
    adc r3, r3, #0
    adds r2, r2, #2048
    mov r6, r6, lsr #12
    orr r6, r6, r3, lsl #20
    adc r0, r0, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    str r1, [sp, #0x4]
    str r6, [sp, #0x8]
    str r2, [sp, #0xc]
    ldr r2, [r5]
    mov r0, #1
    add r1, r1, r2
    str r1, [r4]
    ldr r2, [sp, #0x8]
    ldr r1, [r5, #0x4]
    add r1, r2, r1
    str r1, [r4, #0x4]
    ldr r2, [sp, #0xc]
    ldr r1, [r5, #0x8]
    add sp, sp, #28
    add r1, r2, r1
    str r1, [r4, #0x8]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov000_021dcf94_L1d0:
    mov r0, #0
    add sp, sp, #28
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
