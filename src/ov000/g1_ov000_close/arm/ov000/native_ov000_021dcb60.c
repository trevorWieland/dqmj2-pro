/* ov000 row 0x021dcb60: 392 bytes.
 *
 * What it does: 98 instructions; 4 call(s) to 0x0200235c, 0x0200235c, 0x0200235c, +1 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x28 -> +0x120
 *   branch +0x50 -> +0xf0
 *   branch +0x70 -> +0x170
 *   branch +0xec -> +0x170
 *   branch +0x11c -> +0x170
 *   branch +0x130 -> +0x170
 *   test +0x18 cmp r8, r2
 *   test +0x4c cmp r1, r3
 *   test +0x6c cmp r8, r1
 *   test +0x12c cmp r1, r3
 *   test +0x170 cmp r9, #0
 *   0 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dcb60; the literal pool and
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

extern void native_fn_0200235c(void);


asm u32 native_ov000_021dcb60 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r6, r2
    ldr r2, [r3]
    ldr r8, [r6]
    mov r7, r0
    mov r11, r1
    cmp r8, r2
    ldr r5, [sp, #0x28]
    ldr r4, [sp, #0x2c]
    mov r9, #0
    beq ov000_021dcb60_L120
    ldr r12, [r6, #0x8]
    ldr r0, [r3, #0x8]
    sub r1, r8, r2
    sub r0, r12, r0
    bl native_fn_0200235c
    ldr r3, [r4]
    ldr r1, [r5]
    mov r8, r0
    cmp r1, r3
    beq ov000_021dcb60_Lf0
    ldr r2, [r5, #0x8]
    ldr r0, [r4, #0x8]
    sub r1, r1, r3
    sub r0, r2, r0
    bl native_fn_0200235c
    mov r1, r0
    cmp r8, r1
    beq ov000_021dcb60_L170
    ldr r2, [r6]
    ldr r0, [r5]
    smull r2, r3, r8, r2
    adds r4, r2, #2048
    smull r2, r0, r1, r0
    adc r3, r3, #0
    adds r2, r2, #2048
    mov r4, r4, lsr #12
    orr r4, r4, r3, lsl #20
    adc r0, r0, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    ldr r3, [r5, #0x8]
    sub r2, r4, r2
    ldr r0, [r6, #0x8]
    add r2, r3, r2
    sub r0, r2, r0
    sub r1, r8, r1
    bl native_fn_0200235c
    ldr r1, [r6]
    str r0, [sp]
    sub r0, r0, r1
    smull r1, r0, r8, r0
    adds r1, r1, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    ldr r2, [r6, #0x8]
    orr r1, r1, r0, lsl #20
    add r10, r2, r1
    mov r9, #1
    b ov000_021dcb60_L170
ov000_021dcb60_Lf0:
    ldr r0, [r6]
    ldr r3, [r6, #0x8]
    sub r0, r1, r0
    smull r2, r0, r8, r0
    adds r2, r2, #2048
    adc r0, r0, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    str r1, [sp]
    add r10, r3, r2
    mov r9, #1
    b ov000_021dcb60_L170
ov000_021dcb60_L120:
    ldr r3, [r4]
    ldr r1, [r5]
    str r8, [sp]
    cmp r1, r3
    beq ov000_021dcb60_L170
    ldr r2, [r5, #0x8]
    ldr r0, [r4, #0x8]
    sub r1, r1, r3
    sub r0, r2, r0
    bl native_fn_0200235c
    ldr r1, [r5]
    ldr r3, [r5, #0x8]
    sub r1, r8, r1
    smull r2, r1, r0, r1
    adds r2, r2, #2048
    adc r0, r1, #0
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    add r10, r3, r1
    mov r9, #1
ov000_021dcb60_L170:
    cmp r9, #0
    ldrne r0, [sp]
    strne r0, [r7]
    strne r10, [r11]
    mov r0, r9
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
