/* ov000 row 0x021e6db8: 760 bytes.
 *
 * What it does: 188 instructions; 3 call(s) to 0x0202859c, 0x020285c8, 0x02002618; loops (back edge at +0x40); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x2f0 -> native_data_0222b894 (image word 0x0222b894)
 *   pool +0x2f4 -> native_data_0222b8a0 (image word 0x0222b8a0)
 *   branch +0xb4 -> +0xd4
 *   branch +0xd0 -> +0x1e8
 *   branch +0xf4 -> +0x114
 *   branch +0x110 -> +0x1e8
 *   test +0x98 cmp lr, r0
 *   test +0xa4 cmpeq r1, r0
 *   test +0xb0 cmpeq r1, r0
 *   test +0xd8 cmp lr, r0
 *   test +0xe4 cmpeq r1, r0
 *   test +0xf0 cmpeq r1, r0
 *   6 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e6db8; the literal pool and
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

extern u8 native_data_0222b894[];
extern u8 native_data_0222b8a0[];
extern void native_fn_0202859c(void);
extern void native_fn_020285c8(void);
extern void native_fn_02002618(void);


asm u32 native_ov000_021e6db8 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #52
    ldr r9, =native_data_0222b894
    ldr r7, =native_data_0222b8a0
    add r8, sp, #16
    add r6, sp, #4
    str r0, [sp]
    mov r5, r1
    mov r4, r2
    ldmia r9, {r0, r1, r2}
    stmia r8, {r0, r1, r2}
    ldmia r7, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    mov r0, #0
    mov r1, r0
    mov r11, r3
    bl native_fn_0202859c
    mov r6, r0
    mov r0, #0
    mov r1, r0
    bl native_fn_020285c8
    ldr r2, [r0]
    ldr r1, [r6]
    sub r1, r2, r1
    str r1, [sp, #0x28]
    ldr r2, [r0, #0x4]
    ldr r1, [r6, #0x4]
    sub r1, r2, r1
    str r1, [sp, #0x2c]
    ldr r2, [r0, #0x8]
    ldr r1, [r6, #0x8]
    add r0, sp, #40
    sub r1, r2, r1
    str r1, [sp, #0x30]
    mov r1, r0
    bl native_fn_02002618
    ldr lr, [sp, #0x28]
    ldr r0, [sp, #0x10]
    cmp lr, r0
    ldreq r1, [sp, #0x2c]
    ldreq r0, [sp, #0x14]
    cmpeq r1, r0
    ldreq r1, [sp, #0x30]
    ldreq r0, [sp, #0x18]
    cmpeq r1, r0
    bne ov000_021e6db8_Ld4
    mov r3, #0
    mov r12, r3
    mov r1, r3
    mov r8, r3
    sub r7, r3, #4096
    mov r2, #4096
    b ov000_021e6db8_L1e8
ov000_021e6db8_Ld4:
    ldr r0, [sp, #0x4]
    cmp lr, r0
    ldreq r1, [sp, #0x2c]
    ldreq r0, [sp, #0x8]
    cmpeq r1, r0
    ldreq r1, [sp, #0x30]
    ldreq r0, [sp, #0xc]
    cmpeq r1, r0
    bne ov000_021e6db8_L114
    mov r3, #0
    mov r2, #4096
    mov r12, r3
    mov r1, r3
    mov r8, r3
    mov r7, r2
    b ov000_021e6db8_L1e8
ov000_021e6db8_L114:
    ldr r3, [sp, #0x18]
    ldr r1, [sp, #0x2c]
    ldr r9, [sp, #0x14]
    ldr r0, [sp, #0x30]
    ldr r7, [sp, #0x10]
    smull r10, r8, r9, r0
    smull r6, r2, r3, r1
    subs r6, r10, r6
    sbc r8, r8, r2
    adds r2, r6, #2048
    smull r12, r10, r3, r14
    smull r6, r3, r7, r0
    adc r8, r8, #0
    subs r6, r12, r6
    sbc r3, r10, r3
    adds r6, r6, #2048
    mov r2, r2, lsr #12
    orr r2, r2, r8, lsl #20
    smull r10, r8, r7, r1
    adc r7, r3, #0
    mov r3, r6, lsr #12
    orr r3, r3, r7, lsl #20
    smull r7, r6, r9, r14
    subs r7, r10, r7
    sbc r6, r8, r6
    adds r7, r7, #2048
    adc r6, r6, #0
    mov r12, r7, lsr #12
    orr r12, r12, r6, lsl #20
    smull r9, r8, r1, r12
    smull r7, r6, r1, r2
    smull r10, r1, r0, r3
    subs r9, r9, r10
    sbc r1, r8, r1
    adds r9, r9, #2048
    adc r8, r1, #0
    mov r1, r9, lsr #12
    orr r1, r1, r8, lsl #20
    smull r9, r8, r0, r2
    smull r10, r0, r14, r12
    subs r9, r9, r10
    sbc r0, r8, r0
    adds r8, r9, #2048
    adc r0, r0, #0
    mov r8, r8, lsr #12
    orr r8, r8, r0, lsl #20
    smull r9, r0, r14, r3
    subs r7, r9, r7
    sbc r0, r0, r6
    adds r6, r7, #2048
    adc r0, r0, #0
    mov r7, r6, lsr #12
    orr r7, r7, r0, lsl #20
ov000_021e6db8_L1e8:
    smull r6, r10, r11, r14
    adds r6, r6, #2048
    ldr r0, [sp, #0x2c]
    ldr r9, [sp, #0x30]
    smull r14, r0, r11, r0
    adc r10, r10, #0
    mov r6, r6, lsr #12
    orr r6, r6, r10, lsl #20
    smull r10, r9, r11, r9
    adds r11, lr, #2048
    adc r0, r0, #0
    mov r11, r11, lsr #12
    orr r11, r11, r0, lsl #20
    adds r0, r10, #2048
    adc r9, r9, #0
    mov r0, r0, lsr #12
    orr r0, r0, r9, lsl #20
    smull r9, r1, r4, r1
    adds r9, r9, #2048
    adc r1, r1, #0
    mov r9, r9, lsr #12
    orr r9, r9, r1, lsl #20
    str r6, [sp, #0x28]
    add r6, r6, r9
    smull r9, r8, r4, r8
    smull r7, r1, r4, r7
    adds r9, r9, #2048
    adc r4, r8, #0
    adds r7, r7, #2048
    mov r8, r9, lsr #12
    orr r8, r8, r4, lsl #20
    adc r1, r1, #0
    mov r7, r7, lsr #12
    orr r7, r7, r1, lsl #20
    str r0, [sp, #0x30]
    add r1, r0, r7
    smull r2, r0, r5, r2
    adds r2, r2, #2048
    adc r0, r0, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    add r0, r6, r2
    str r0, [sp, #0x1c]
    smull r6, r2, r5, r3
    smull r3, r0, r5, r12
    adds r5, r6, #2048
    adc r2, r2, #0
    adds r3, r3, #2048
    mov r5, r5, lsr #12
    adc r0, r0, #0
    mov r3, r3, lsr #12
    orr r3, r3, r0, lsl #20
    add r1, r1, r3
    add r4, r11, r8
    orr r5, r5, r2, lsl #20
    add r2, r4, r5
    ldr r3, [sp]
    str r11, [sp, #0x2c]
    add r0, sp, #28
    str r2, [sp, #0x20]
    str r1, [sp, #0x24]
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r3
    add sp, sp, #52
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
