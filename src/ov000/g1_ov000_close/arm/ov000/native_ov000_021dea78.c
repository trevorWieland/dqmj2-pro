/* ov000 row 0x021dea78: 1880 bytes.
 *
 * What it does: 469 instructions; 6 call(s) to 0x021df1c0, 0x021df19c, 0x0200235c, +3 more; loops (back edge at +0x1c8); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x754 -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x7c -> +0x748
 *   branch +0xb8 -> +0x724
 *   branch +0x138 -> +0x708
 *   branch +0x22c -> +0x708
 *   branch +0x384 -> +0x698
 *   branch +0x554 -> +0x698
 *   branch +0x69c -> +0x708
 *   branch +0x6f4 -> +0x708
 *   back edge +0x720 -> +0xf4
 *   back edge +0x744 -> +0x90
 *   test +0x18 cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0x698 cmp r0, #0
 *   test +0x71c cmp r1, r0
 *   test +0x734 cmp r1, r0
 *   3 block transfer(s), 52 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dea78; the literal pool and
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


asm u32 native_ov000_021dea78 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #188
    ldr r1, =0x0223142c
    str r0, [sp]
    ldr r0, [r1, #0x7a4]
    str r0, [sp, #0x4]
    cmp r0, #0
    addeq sp, sp, #188
    moveq r0, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldrsh r0, [r0, #8]
    add r3, sp, #176
    str r0, [sp, #0x28]
    mov r0, #0
    str r0, [sp, #0x18]
    ldr r0, [sp]
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0x18]
    ldr r1, [sp, #0xb4]
    str r0, [sp, #0x20]
    add r0, r1, #163840
    str r0, [sp, #0xc]
    ldr r0, [sp, #0x18]
    str r0, [sp, #0x30]
    ldr r0, [sp, #0xc]
    str r0, [sp, #0xb4]
    ldr r0, [sp, #0x28]
    cmp r0, #0
    mov r0, #26214400
    str r0, [sp, #0x1c]
    ble ov000_021dea78_L748
    ldr r0, [sp, #0xb8]
    str r0, [sp, #0x8]
    ldr r0, [sp, #0x4]
    str r0, [sp, #0x10]
ov000_021dea78_L90:
    ldr r0, [sp, #0x10]
    ldr r1, [r0, #0xc]
    ldr r0, [r0, #0x10]
    str r0, [sp, #0x24]
    ldr r0, [sp, #0x4]
    add r4, r0, r1
    ldr r0, [sp, #0x24]
    cmp r0, #0
    mov r0, #0
    str r0, [sp, #0x2c]
    ble ov000_021dea78_L724
    mvn r0, #0
    str r0, [sp, #0x94]
    ldr r0, [sp, #0x30]
    and r0, r0, #255
    str r0, [sp, #0x90]
    ldr r0, [sp, #0x94]
    mov r0, r0, lsl #12
    str r0, [sp, #0xa0]
    ldr r0, [sp, #0x94]
    mov r0, r0, lsl #12
    str r0, [sp, #0x9c]
    ldr r0, [sp, #0x94]
    mov r0, r0, lsl #12
    str r0, [sp, #0x98]
ov000_021dea78_Lf4:
    ldr r0, [sp, #0x98]
    ldmia r4, {r7, r9}
    umull r1, r2, r9, r0
    mov r0, #2048
    adds r0, r1, r0
    mov r1, r0, lsr #12
    ldr r0, [sp, #0x94]
    ldr r5, [r4, #0x8]
    mla r2, r9, r0, r2
    ldr r0, [sp, #0x98]
    mov r8, r9, asr #31
    mla r2, r8, r0, r2
    mov r0, #0
    adc r0, r2, r0
    mov r6, r7, asr #31
    mov r3, r5, asr #31
    orrs r1, r1, r0, lsl #20
    beq ov000_021dea78_L708
    ldr r2, [r4, #0x10]
    ldr r0, [sp, #0xc]
    ldr r10, [r4, #0x14]
    sub r2, r2, r0
    ldr r0, [sp, #0x8]
    ldr r12, [r4, #0xc]
    sub r0, r10, r0
    mov r10, r2, asr #31
    ldr r11, [sp, #0xb0]
    str r10, [sp, #0x38]
    sub r10, r12, r11
    mov r11, r10, asr #31
    str r11, [sp, #0x34]
    mov lr, r0, asr #31
    umull r12, r11, r5, r0
    mla r11, r5, r14, r11
    mla r11, r3, r0, r11
    ldr r5, [sp, #0x34]
    umull r3, r0, r7, r10
    mla r0, r7, r5, r0
    mla r0, r6, r10, r0
    ldr r5, [sp, #0x38]
    umull r7, r6, r9, r2
    mla r6, r9, r5, r6
    mla r6, r8, r2, r6
    adds r2, r3, r7
    adc r0, r0, r6
    adds r3, r12, r2
    adc r2, r11, r0
    mov r0, #2048
    adds r3, r3, r0
    mov r0, #0
    adc r2, r2, r0
    mov r0, r3, lsr #12
    orr r0, r0, r2, lsl #20
    bl native_fn_0200235c
    ldr r1, [sp, #0xa0]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    ldr r1, [sp, #0x94]
    mla r3, r0, r1, r3
    ldr r0, [sp, #0xa0]
    mla r3, r2, r0, r3
    mov r0, #2048
    adds r2, r5, r0
    mov r0, #0
    adc r1, r3, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    ldr r1, [sp, #0x9c]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    adds r1, r5, #2048
    mov r5, r1, lsr #12
    ldr r1, [sp, #0x94]
    mla r3, r0, r1, r3
    ldr r1, [sp, #0x9c]
    mla r3, r2, r1, r3
    adc r1, r3, #0
    orrs r5, r5, r1, lsl #20
    bmi ov000_021dea78_L708
    ldr r1, [sp, #0xc]
    ldr r10, [sp, #0xb0]
    add r0, r1, r0
    str r0, [sp, #0x14]
    ldr r0, [r4, #0xc]
    ldr r1, [r4, #0x10]
    sub r8, r0, r10
    ldr r0, [sp, #0x14]
    ldr r2, [r4, #0x14]
    sub r7, r1, r0
    ldr r0, [sp, #0x8]
    ldr r1, [r4, #0x18]
    sub r6, r2, r0
    sub r5, r1, r10
    ldr r2, [r4, #0x1c]
    ldr r0, [sp, #0x14]
    ldr r1, [r4, #0x20]
    sub lr, r2, r0
    ldr r0, [sp, #0x8]
    sub r12, r1, r0
    mov r0, lr, asr #31
    str r0, [sp, #0x3c]
    mov r0, r6, asr #31
    str r0, [sp, #0x40]
    mov r0, r12, asr #31
    str r0, [sp, #0x44]
    mov r0, r7, asr #31
    str r0, [sp, #0x48]
    mov r0, r8, asr #31
    str r0, [sp, #0x4c]
    mov r0, r5, asr #31
    str r0, [sp, #0x50]
    ldr r0, [r4, #0x4]
    str r0, [sp, #0x54]
    ldr r0, [r4]
    str r0, [sp, #0x5c]
    ldr r0, [sp, #0x54]
    mov r0, r0, asr #31
    str r0, [sp, #0x58]
    ldr r0, [sp, #0x5c]
    mov r0, r0, asr #31
    str r0, [sp, #0x60]
    ldr r0, [r4, #0x8]
    str r0, [sp, #0x64]
    ldr r2, [sp, #0x64]
    smull r1, r0, r8, r14
    mov r2, r2, asr #31
    str r2, [sp, #0x68]
    smull r3, r2, r7, r5
    subs r3, r1, r3
    sbc r1, r0, r2
    mov r0, #2048
    adds r2, r3, r0
    mov r0, #0
    mov r9, r2, lsr #12
    adc r0, r1, r0
    orr r9, r9, r0, lsl #20
    smull r3, r2, r7, r12
    smull r0, r1, r6, r14
    subs r0, r3, r0
    sbc r2, r2, r1
    adds r1, r0, #2048
    mov r0, #0
    adc r0, r2, r0
    mov r3, r1, lsr #12
    orr r3, r3, r0, lsl #20
    smull r2, r1, r6, r5
    smull r0, r11, r8, r12
    subs r0, r2, r0
    sbc r1, r1, r11
    adds r0, r0, #2048
    adc r1, r1, #0
    mov r0, r0, lsr #12
    ldr r2, [sp, #0x54]
    orr r0, r0, r1, lsl #20
    smull r1, r0, r2, r0
    ldr r2, [sp, #0x5c]
    smlal r1, r0, r2, r3
    ldr r2, [sp, #0x64]
    smlal r1, r0, r2, r9
    adds r2, r1, #2048
    adc r0, r0, #0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    bmi ov000_021dea78_L698
    ldr r0, [r4, #0x24]
    ldr r1, [r4, #0x28]
    sub r3, r0, r10
    ldr r0, [sp, #0x14]
    sub r2, r1, r0
    mov r0, r2, asr #31
    str r0, [sp, #0xa4]
    ldr r1, [r4, #0x2c]
    ldr r0, [sp, #0x8]
    sub r1, r1, r0
    mov r0, r1, asr #31
    str r0, [sp, #0xa8]
    mov r0, r3, asr #31
    str r0, [sp, #0x6c]
    umull r9, r0, r5, r2
    str r9, [sp, #0x7c]
    ldr r9, [sp, #0xa4]
    mla r0, r5, r9, r0
    ldr r9, [sp, #0x50]
    mla r0, r9, r2, r0
    umull r9, r10, r14, r3
    str r10, [sp, #0x80]
    ldr r10, [sp, #0x7c]
    subs r11, r10, r9
    ldr r10, [sp, #0x6c]
    ldr r9, [sp, #0x80]
    mla r9, r14, r10, r9
    ldr r10, [sp, #0x3c]
    mla r9, r10, r3, r9
    str r9, [sp, #0x80]
    sbc r0, r0, r9
    adds r9, r11, #2048
    adc r0, r0, #0
    mov r11, r9, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x78]
    mov r0, r11, asr #31
    ldr r9, [sp, #0x64]
    str r0, [sp, #0xac]
    umull r10, r0, r9, r11
    str r10, [sp, #0x70]
    mov r10, r9
    ldr r9, [sp, #0xac]
    mla r0, r10, r9, r0
    ldr r9, [sp, #0x68]
    mla r0, r9, r11, r0
    str r0, [sp, #0x74]
    umull r0, r9, r14, r1
    str r0, [sp, #0x88]
    ldr r0, [sp, #0xa8]
    ldr r10, [sp, #0x88]
    mla r9, r14, r0, r9
    ldr r0, [sp, #0x3c]
    mla r9, r0, r1, r9
    umull r11, r0, r12, r2
    subs r10, r10, r11
    ldr r11, [sp, #0xa4]
    mla r0, r12, r11, r0
    ldr r11, [sp, #0x44]
    mla r0, r11, r2, r0
    sbc r9, r9, r0
    mov r0, #2048
    adds r10, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r10, r10, lsr #12
    orr r10, r10, r0, lsl #20
    ldr r0, [sp, #0x5c]
    mov lr, r10, asr #31
    umull r9, r11, r0, r10
    mla r11, r0, r14, r11
    ldr r0, [sp, #0x60]
    str r9, [sp, #0x84]
    mla r11, r0, r10, r11
    umull r0, r9, r12, r3
    str r0, [sp, #0x8c]
    ldr r0, [sp, #0x6c]
    ldr r10, [sp, #0x8c]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x44]
    mla r9, r0, r3, r9
    umull r12, r0, r5, r1
    subs r10, r10, r12
    ldr r12, [sp, #0xa8]
    mla r0, r5, r12, r0
    ldr r5, [sp, #0x50]
    ldr r12, [sp, #0x54]
    mla r0, r5, r1, r0
    sbc r5, r9, r0
    mov r0, #2048
    adds r9, r10, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orr r5, r5, r0, lsl #20
    umull r10, r9, r12, r5
    ldr r12, [sp, #0x84]
    mov r0, r5, asr #31
    adds r10, r12, r10
    ldr r12, [sp, #0x54]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x58]
    mla r9, r0, r5, r9
    ldr r0, [sp, #0x70]
    adc r5, r11, r9
    adds r9, r0, r10
    ldr r0, [sp, #0x74]
    adc r5, r0, r5
    mov r0, #2048
    adds r9, r9, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orrs r5, r5, r0, lsl #20
    movmi r0, #0
    bmi ov000_021dea78_L698
    ldr r5, [sp, #0x48]
    umull r9, r0, r3, r7
    mla r0, r3, r5, r0
    ldr r5, [sp, #0x6c]
    mla r0, r5, r7, r0
    umull r5, r10, r2, r8
    subs r5, r9, r5
    ldr r9, [sp, #0x4c]
    mla r10, r2, r9, r10
    ldr r9, [sp, #0xa4]
    mla r10, r9, r8, r10
    sbc r9, r0, r10
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r9, r0
    mov r9, r5, lsr #12
    orr r9, r9, r0, lsl #20
    ldr r10, [sp, #0x64]
    mov r11, r9, asr #31
    umull r5, r0, r10, r9
    mla r0, r10, r11, r0
    ldr r10, [sp, #0x68]
    ldr r11, [sp, #0x40]
    mla r0, r10, r9, r0
    umull r10, r9, r2, r6
    mla r9, r2, r11, r9
    ldr r2, [sp, #0xa4]
    mla r9, r2, r6, r9
    umull r11, r2, r1, r7
    subs r10, r10, r11
    ldr r11, [sp, #0x48]
    mla r2, r1, r11, r2
    ldr r11, [sp, #0xa8]
    mla r2, r11, r7, r2
    sbc r7, r9, r2
    adds r9, r10, #2048
    adc r7, r7, #0
    mov r2, r9, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x5c]
    mov r11, r2, asr #31
    umull r10, r9, r7, r2
    mla r9, r7, r11, r9
    ldr r7, [sp, #0x60]
    ldr r11, [sp, #0x4c]
    mla r9, r7, r2, r9
    umull r7, r2, r1, r8
    mla r2, r1, r11, r2
    ldr r1, [sp, #0xa8]
    mla r2, r1, r8, r2
    ldr r1, [sp, #0x40]
    umull r11, r8, r3, r6
    mla r8, r3, r1, r8
    ldr r1, [sp, #0x6c]
    subs r3, r7, r11
    mla r8, r1, r6, r8
    sbc r2, r2, r8
    adds r3, r3, #2048
    adc r1, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r1, lsl #20
    mov r1, r12
    mov r2, r3, asr #31
    umull r7, r6, r1, r3
    mla r6, r1, r2, r6
    ldr r1, [sp, #0x58]
    adds r2, r10, r7
    mla r6, r1, r3, r6
    adc r1, r9, r6
    adds r2, r5, r2
    adc r1, r0, r1
    mov r0, #2048
    adds r2, r2, r0
    mov r0, #0
    adc r0, r1, r0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    movpl r0, #1
ov000_021dea78_L698:
    cmp r0, #0
    beq ov000_021dea78_L708
    ldr r0, [sp]
    ldr r6, [sp, #0xb0]
    ldr r1, [r0, #0x4]
    ldr r0, [sp, #0x14]
    sub r0, r0, r1
    smull r2, r1, r0, r0
    ldr r0, [sp]
    ldr r5, [r0]
    ldr r3, [r0, #0x8]
    sub r0, r6, r5
    smlal r2, r1, r0, r0
    ldr r0, [sp, #0x8]
    sub r0, r0, r3
    smlal r2, r1, r0, r0
    mov r3, r2, lsr #12
    ldr r0, [sp, #0x1c]
    orr r3, r3, r1, lsl #20
    subs r0, r0, r3
    ldr r0, [sp, #0x20]
    mov r2, r1, asr #12
    sbcs r0, r0, r1, asr #12
    blt ov000_021dea78_L708
    ldr r0, [sp, #0x90]
    str r3, [sp, #0x1c]
    str r2, [sp, #0x20]
    str r0, [sp, #0x18]
ov000_021dea78_L708:
    ldr r0, [sp, #0x2c]
    add r4, r4, #68
    add r1, r0, #1
    ldr r0, [sp, #0x24]
    str r1, [sp, #0x2c]
    cmp r1, r0
    blt ov000_021dea78_Lf4
ov000_021dea78_L724:
    ldr r0, [sp, #0x30]
    add r1, r0, #1
    ldr r0, [sp, #0x28]
    str r1, [sp, #0x30]
    cmp r1, r0
    ldr r0, [sp, #0x10]
    add r0, r0, #12
    str r0, [sp, #0x10]
    blt ov000_021dea78_L90
ov000_021dea78_L748:
    ldr r0, [sp, #0x18]
    add sp, sp, #188
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
