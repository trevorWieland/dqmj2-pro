/* ov000 row 0x021dd54c: 1884 bytes.
 *
 * What it does: 469 instructions; 8 call(s) to 0x02002618, 0x021dd50c, 0x021ddc94, +5 more; loops (back edge at +0x88); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x754 -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x758 -> constant 0x00313063 (image word 0x00313063)
 *   branch +0x28 -> +0x748
 *   branch +0x9c -> +0x748
 *   branch +0xc4 -> +0x724
 *   branch +0x120 -> +0x708
 *   branch +0x234 -> +0x708
 *   branch +0x2ac -> +0x708
 *   branch +0x3ec -> +0x6f8
 *   branch +0x5b4 -> +0x6f8
 *   branch +0x704 -> +0x724
 *   back edge +0x720 -> +0xd8
 *   branch +0x734 -> +0x748
 *   test +0x20 cmp r4, #0
 *   test +0x98 cmp r0, #0
 *   test +0xb4 cmp r0, #0
 *   test +0x11c cmp r1, #0
 *   test +0x6f8 cmp r0, #0
 *   test +0x71c cmp r1, r0
 *   test +0x728 cmp r0, #0
 *   test +0x730 cmpne r0, #0
 *   5 block transfer(s), 45 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dd54c; the literal pool and
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

extern void native_fn_02002618(void);
extern void native_fn_021dd50c(void);
extern void native_fn_0200235c(void);


asm u32 native_ov000_021dd54c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #184
    ldr r3, =0x0223142c
    mov r5, r0
    ldr r4, [r3, #0x7a0]
    mov r0, #0
    mov r3, r1
    str r2, [sp]
    cmp r4, #0
    str r0, [sp, #0x14]
    beq ov000_021dd54c_L748
    add r6, sp, #172
    ldmia r3, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    ldr r2, [r5]
    ldr r1, [r3]
    add r0, sp, #160
    sub r8, r2, r1
    str r8, [sp, #0xa0]
    ldr r6, [r5, #0x4]
    ldr r2, [r3, #0x4]
    mov r1, r0
    sub r7, r6, r2
    smull r2, r6, r7, r7
    str r7, [sp, #0xa4]
    smlal r2, r6, r8, r8
    ldr r5, [r5, #0x8]
    ldr r3, [r3, #0x8]
    sub r3, r5, r3
    smlal r2, r6, r3, r3
    mov r2, r2, lsr #12
    orr r2, r2, r6, lsl #20
    str r3, [sp, #0xa8]
    str r2, [sp, #0x4]
    bl native_fn_02002618
    ldr r1, =0x00313063
    mov r0, r4
    bl native_fn_021dd50c
    cmp r0, #0
    blt ov000_021dd54c_L748
    mov r1, #12
    mla r2, r0, r1, r4
    ldr r0, [r2, #0x10]
    ldr r1, [r2, #0xc]
    str r0, [sp, #0x18]
    cmp r0, #0
    mov r0, #0
    add r4, r4, r1
    str r0, [sp, #0x1c]
    ble ov000_021dd54c_L724
    ldr r0, [sp, #0xb0]
    str r0, [sp, #0x10]
    ldr r0, [sp, #0xb4]
    str r0, [sp, #0xc]
ov000_021dd54c_Ld8:
    ldr r0, [sp, #0xa4]
    ldmia r4, {r10, r12}
    smull r5, r3, r12, r0
    ldr r1, [sp, #0xa0]
    ldr r8, [r4, #0x8]
    smlal r5, r3, r10, r1
    ldr r2, [sp, #0xa8]
    mov r0, #2048
    smlal r5, r3, r8, r2
    adds r1, r5, r0
    mov r0, #0
    adc r0, r3, r0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    mov r11, r12, asr #31
    mov r9, r10, asr #31
    mov r7, r8, asr #31
    cmp r1, #0
    ble ov000_021dd54c_L708
    ldr r3, [r4, #0xc]
    ldr r0, [sp, #0xac]
    ldr r2, [r4, #0x10]
    sub r6, r3, r0
    ldr r0, [sp, #0x10]
    sub r5, r2, r0
    mov r0, r6, asr #31
    str r0, [sp, #0x20]
    ldr r2, [r4, #0x14]
    ldr r0, [sp, #0xc]
    sub r3, r2, r0
    mov r0, r5, asr #31
    str r0, [sp, #0x24]
    mov lr, r3, asr #31
    umull r2, r0, r8, r3
    mla r0, r8, r14, r0
    mla r0, r7, r3, r0
    ldr r8, [sp, #0x20]
    umull r7, r3, r10, r6
    mla r3, r10, r8, r3
    mla r3, r9, r6, r3
    ldr r6, [sp, #0x24]
    umull r9, r8, r12, r5
    mla r8, r12, r6, r8
    mla r8, r11, r5, r8
    adds r5, r7, r9
    adc r3, r3, r8
    adds r5, r2, r5
    adc r2, r0, r3
    mov r0, #2048
    adds r3, r5, r0
    mov r0, #0
    adc r2, r2, r0
    mov r0, r3, lsr #12
    orr r0, r0, r2, lsl #20
    bl native_fn_0200235c
    ldr r7, [sp, #0xa0]
    ldr r6, [sp, #0xa4]
    smull r5, r2, r0, r7
    adds r5, r5, #2048
    adc r1, r2, #0
    mov r2, r5, lsr #12
    smull r9, r5, r0, r6
    adds r9, r9, #2048
    orr r2, r2, r1, lsl #20
    ldr r3, [sp, #0xa8]
    adc r5, r5, #0
    mov r1, r9, lsr #12
    orr r1, r1, r5, lsl #20
    smull r9, r5, r0, r3
    mov r0, #2048
    adds r9, r9, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    smull r10, r9, r6, r1
    orr r5, r5, r0, lsl #20
    smlal r10, r9, r7, r2
    smlal r10, r9, r3, r5
    mov r0, #2048
    adds r3, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r3, r3, lsr #12
    orrs r3, r3, r0, lsl #20
    mov r8, r2, asr #31
    mov r11, r1, asr #31
    mov r0, r5, asr #31
    bmi ov000_021dd54c_L708
    ldr r3, [sp, #0x10]
    ldr r6, [sp, #0xac]
    add r10, r3, r1
    add r3, r6, r2
    ldr r6, [sp, #0xc]
    str r3, [sp, #0x94]
    add r9, r6, r5
    umull r7, r6, r5, r5
    mla r6, r5, r0, r6
    mla r6, r0, r5, r6
    umull r5, r0, r2, r2
    mla r0, r2, r8, r0
    mla r0, r8, r2, r0
    umull r8, r2, r1, r1
    mla r2, r1, r11, r2
    mla r2, r11, r1, r2
    adds r5, r5, r8
    adc r0, r0, r2
    adds r1, r7, r5
    adc r0, r6, r0
    mov r2, r1, lsr #12
    mov r1, r0, asr #12
    orr r2, r2, r0, lsl #20
    ldr r0, [sp, #0x4]
    str r10, [sp, #0x98]
    subs r0, r0, r2
    ldr r0, [sp, #0x4]
    str r9, [sp, #0x9c]
    rscs r0, r1, r0, asr #31
    blt ov000_021dd54c_L708
    ldr r1, [r4, #0xc]
    ldr r0, [r4, #0x10]
    sub r8, r1, r3
    ldr r1, [r4, #0x14]
    sub r7, r0, r10
    ldr r0, [r4, #0x18]
    sub r6, r1, r9
    ldr r1, [r4, #0x1c]
    sub r5, r0, r3
    ldr r0, [r4, #0x20]
    sub lr, r1, r10
    sub r12, r0, r9
    mov r0, lr, asr #31
    str r0, [sp, #0x28]
    mov r0, r6, asr #31
    str r0, [sp, #0x2c]
    mov r0, r12, asr #31
    str r0, [sp, #0x30]
    mov r0, r7, asr #31
    str r0, [sp, #0x34]
    mov r0, r8, asr #31
    str r0, [sp, #0x38]
    mov r0, r5, asr #31
    str r0, [sp, #0x3c]
    ldr r0, [r4, #0x4]
    smull r2, r1, r8, r14
    str r0, [sp, #0x40]
    ldr r0, [r4]
    str r0, [sp, #0x48]
    ldr r0, [sp, #0x40]
    mov r0, r0, asr #31
    str r0, [sp, #0x44]
    ldr r0, [sp, #0x48]
    mov r0, r0, asr #31
    str r0, [sp, #0x4c]
    ldr r0, [r4, #0x8]
    str r0, [sp, #0x50]
    mov r0, r0, asr #31
    str r0, [sp, #0x54]
    smull r0, r11, r7, r5
    subs r0, r2, r0
    sbc r1, r1, r11
    adds r0, r0, #2048
    adc r1, r1, #0
    mov r0, r0, lsr #12
    orr r0, r0, r1, lsl #20
    str r0, [sp, #0x58]
    smull r2, r1, r7, r12
    smull r0, r11, r6, r14
    subs r0, r2, r0
    sbc r1, r1, r11
    adds r0, r0, #2048
    adc r1, r1, #0
    mov r0, r0, lsr #12
    orr r0, r0, r1, lsl #20
    str r0, [sp, #0x84]
    smull r11, r0, r8, r12
    smull r2, r1, r6, r5
    subs r2, r2, r11
    str r0, [sp, #0x5c]
    sbc r0, r1, r0
    adds r1, r2, #2048
    mov r2, r1, lsr #12
    adc r0, r0, #0
    ldr r1, [sp, #0x40]
    orr r2, r2, r0, lsl #20
    smull r11, r0, r1, r2
    ldr r2, [sp, #0x48]
    ldr r1, [sp, #0x84]
    smlal r11, r0, r2, r1
    ldr r2, [sp, #0x50]
    ldr r1, [sp, #0x58]
    smlal r11, r0, r2, r1
    adds r1, r11, #2048
    mov r2, #0
    adc r0, r0, #0
    mov r1, r1, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, r2
    bmi ov000_021dd54c_L6f8
    ldr r1, [r4, #0x24]
    ldr r0, [r4, #0x28]
    sub r3, r1, r3
    ldr r1, [r4, #0x2c]
    sub r2, r0, r10
    mov r0, r2, asr #31
    sub r1, r1, r9
    str r0, [sp, #0x88]
    mov r0, r1, asr #31
    str r0, [sp, #0x8c]
    mov r0, r3, asr #31
    str r0, [sp, #0x60]
    umull r9, r0, r5, r2
    str r9, [sp, #0x70]
    ldr r9, [sp, #0x88]
    mla r0, r5, r9, r0
    ldr r9, [sp, #0x3c]
    mla r0, r9, r2, r0
    umull r9, r10, r14, r3
    str r10, [sp, #0x74]
    ldr r10, [sp, #0x70]
    subs r11, r10, r9
    ldr r10, [sp, #0x60]
    ldr r9, [sp, #0x74]
    mla r9, r14, r10, r9
    ldr r10, [sp, #0x28]
    mla r9, r10, r3, r9
    str r9, [sp, #0x74]
    sbc r0, r0, r9
    adds r9, r11, #2048
    adc r0, r0, #0
    mov r11, r9, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x6c]
    mov r0, r11, asr #31
    ldr r9, [sp, #0x50]
    str r0, [sp, #0x90]
    umull r10, r0, r9, r11
    str r10, [sp, #0x64]
    mov r10, r9
    ldr r9, [sp, #0x90]
    mla r0, r10, r9, r0
    ldr r9, [sp, #0x54]
    mla r0, r9, r11, r0
    str r0, [sp, #0x68]
    umull r0, r9, r14, r1
    str r0, [sp, #0x7c]
    ldr r0, [sp, #0x8c]
    ldr r10, [sp, #0x7c]
    mla r9, r14, r0, r9
    ldr r0, [sp, #0x28]
    mla r9, r0, r1, r9
    umull r11, r0, r12, r2
    subs r10, r10, r11
    ldr r11, [sp, #0x88]
    mla r0, r12, r11, r0
    ldr r11, [sp, #0x30]
    mla r0, r11, r2, r0
    sbc r9, r9, r0
    mov r0, #2048
    adds r10, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r10, r10, lsr #12
    orr r10, r10, r0, lsl #20
    ldr r0, [sp, #0x48]
    mov lr, r10, asr #31
    umull r9, r11, r0, r10
    mla r11, r0, r14, r11
    ldr r0, [sp, #0x4c]
    str r9, [sp, #0x78]
    mla r11, r0, r10, r11
    umull r0, r9, r12, r3
    str r0, [sp, #0x80]
    ldr r0, [sp, #0x60]
    ldr r10, [sp, #0x80]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x30]
    mla r9, r0, r3, r9
    umull r12, r0, r5, r1
    subs r10, r10, r12
    ldr r12, [sp, #0x8c]
    mla r0, r5, r12, r0
    ldr r5, [sp, #0x3c]
    ldr r12, [sp, #0x40]
    mla r0, r5, r1, r0
    sbc r5, r9, r0
    mov r0, #2048
    adds r9, r10, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orr r5, r5, r0, lsl #20
    umull r10, r9, r12, r5
    ldr r12, [sp, #0x78]
    mov r0, r5, asr #31
    adds r10, r12, r10
    ldr r12, [sp, #0x40]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x44]
    mla r9, r0, r5, r9
    ldr r0, [sp, #0x64]
    adc r5, r11, r9
    adds r9, r0, r10
    ldr r0, [sp, #0x68]
    adc r5, r0, r5
    mov r0, #2048
    adds r9, r9, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orrs r5, r5, r0, lsl #20
    movmi r0, #0
    bmi ov000_021dd54c_L6f8
    ldr r5, [sp, #0x34]
    umull r9, r0, r3, r7
    mla r0, r3, r5, r0
    ldr r5, [sp, #0x60]
    mla r0, r5, r7, r0
    umull r5, r10, r2, r8
    subs r5, r9, r5
    ldr r9, [sp, #0x38]
    mla r10, r2, r9, r10
    ldr r9, [sp, #0x88]
    mla r10, r9, r8, r10
    sbc r9, r0, r10
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r9, r0
    mov r9, r5, lsr #12
    orr r9, r9, r0, lsl #20
    ldr r10, [sp, #0x50]
    mov r11, r9, asr #31
    umull r5, r0, r10, r9
    mla r0, r10, r11, r0
    ldr r10, [sp, #0x54]
    ldr r11, [sp, #0x2c]
    mla r0, r10, r9, r0
    umull r10, r9, r2, r6
    mla r9, r2, r11, r9
    ldr r2, [sp, #0x88]
    mla r9, r2, r6, r9
    umull r11, r2, r1, r7
    subs r10, r10, r11
    ldr r11, [sp, #0x34]
    mla r2, r1, r11, r2
    ldr r11, [sp, #0x8c]
    mla r2, r11, r7, r2
    sbc r7, r9, r2
    adds r9, r10, #2048
    adc r7, r7, #0
    mov r2, r9, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x48]
    mov r11, r2, asr #31
    umull r10, r9, r7, r2
    mla r9, r7, r11, r9
    ldr r7, [sp, #0x4c]
    ldr r11, [sp, #0x38]
    mla r9, r7, r2, r9
    umull r7, r2, r1, r8
    mla r2, r1, r11, r2
    ldr r1, [sp, #0x8c]
    mla r2, r1, r8, r2
    ldr r1, [sp, #0x2c]
    umull r11, r8, r3, r6
    mla r8, r3, r1, r8
    ldr r1, [sp, #0x60]
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
    ldr r1, [sp, #0x44]
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
ov000_021dd54c_L6f8:
    cmp r0, #0
    movne r0, #1
    strne r0, [sp, #0x14]
    bne ov000_021dd54c_L724
ov000_021dd54c_L708:
    ldr r0, [sp, #0x1c]
    add r4, r4, #68
    add r1, r0, #1
    ldr r0, [sp, #0x18]
    str r1, [sp, #0x1c]
    cmp r1, r0
    blt ov000_021dd54c_Ld8
ov000_021dd54c_L724:
    ldr r0, [sp, #0x14]
    cmp r0, #0
    ldrne r0, [sp]
    cmpne r0, #0
    beq ov000_021dd54c_L748
    ldr r3, [sp]
    add r0, sp, #148
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021dd54c_L748:
    ldr r0, [sp, #0x14]
    add sp, sp, #184
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
