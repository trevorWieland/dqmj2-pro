/* ov000 row 0x021de34c: 1788 bytes.
 *
 * What it does: 446 instructions; 4 call(s) to 0x021dea14, 0x0200235c, 0x021de9fc, +1 more; loops (back edge at +0x1a0); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x6f8 -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x78 -> +0x6c8
 *   branch +0x110 -> +0x6b0
 *   branch +0x204 -> +0x6b0
 *   branch +0x248 -> +0x6b0
 *   branch +0x394 -> +0x690
 *   branch +0x554 -> +0x690
 *   branch +0x694 -> +0x6b0
 *   branch +0x6ac -> +0x6c8
 *   back edge +0x6c4 -> +0xac
 *   branch +0x6d8 -> +0x6ec
 *   test +0x18 cmp r4, #0
 *   test +0x6c cmp r0, #0
 *   test +0x690 cmp r0, #0
 *   test +0x6c0 cmp r1, r0
 *   test +0x6cc cmp r0, #0
 *   test +0x6d4 cmpne r0, #0
 *   5 block transfer(s), 47 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021de34c; the literal pool and
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


asm u32 native_ov000_021de34c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #180
    ldr r3, =0x0223142c
    mov r5, r1
    ldr r4, [r3, #0x79c]
    mov r1, #0
    cmp r4, #0
    str r2, [sp]
    str r1, [sp, #0x14]
    addeq sp, sp, #180
    moveq r0, r1
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    add r3, sp, #168
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0x14]
    ldr r1, [sp, #0xac]
    str r0, [sp, #0x1c]
    add r0, r1, #12288
    str r0, [sp, #0xac]
    str r0, [sp, #0x8]
    ldrsb r0, [r5, #17]
    ldr r1, [r4, #0xc]
    str r0, [sp, #0x18]
    add r0, r5, #18
    str r0, [sp, #0x10]
    ldr r0, [sp, #0x18]
    cmp r0, #0
    add r0, r4, r1
    str r0, [sp, #0xc]
    ble ov000_021de34c_L6c8
    ldr r0, [sp, #0xb0]
    str r0, [sp, #0x4]
    mvn r0, #0
    str r0, [sp, #0x7c]
    mov r0, r0, lsl #12
    str r0, [sp, #0x88]
    ldr r0, [sp, #0x7c]
    mov r0, r0, lsl #12
    str r0, [sp, #0x84]
    ldr r0, [sp, #0x7c]
    mov r0, r0, lsl #12
    str r0, [sp, #0x80]
ov000_021de34c_Lac:
    ldr r0, [sp, #0x1c]
    mov r1, r0, lsl #1
    ldr r0, [sp, #0x10]
    ldrsh r1, [r0, r1]
    mov r0, #68
    smulbb r1, r1, r0
    ldr r0, [sp, #0xc]
    add r4, r0, r1
    ldmia r4, {r7, r9}
    ldr r0, [sp, #0x80]
    ldr r5, [r4, #0x8]
    umull r1, r2, r9, r0
    mov r0, #2048
    adds r0, r1, r0
    mov r1, r0, lsr #12
    ldr r0, [sp, #0x7c]
    mov r8, r9, asr #31
    mla r2, r9, r0, r2
    ldr r0, [sp, #0x80]
    mov r6, r7, asr #31
    mla r2, r8, r0, r2
    mov r0, #0
    adc r0, r2, r0
    mov r3, r5, asr #31
    orrs r1, r1, r0, lsl #20
    beq ov000_021de34c_L6b0
    ldr r2, [r4, #0x10]
    ldr r0, [sp, #0x8]
    ldr r10, [r4, #0x14]
    sub r2, r2, r0
    ldr r0, [sp, #0x4]
    ldr r12, [r4, #0xc]
    sub r0, r10, r0
    mov r10, r2, asr #31
    ldr r11, [sp, #0xa8]
    str r10, [sp, #0x24]
    sub r10, r12, r11
    mov r11, r10, asr #31
    str r11, [sp, #0x20]
    mov lr, r0, asr #31
    umull r12, r11, r5, r0
    mla r11, r5, r14, r11
    mla r11, r3, r0, r11
    ldr r5, [sp, #0x20]
    umull r3, r0, r7, r10
    mla r0, r7, r5, r0
    mla r0, r6, r10, r0
    ldr r5, [sp, #0x24]
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
    ldr r1, [sp, #0x88]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    ldr r1, [sp, #0x7c]
    mla r3, r0, r1, r3
    ldr r0, [sp, #0x88]
    mla r3, r2, r0, r3
    mov r0, #2048
    adds r1, r5, r0
    mov r0, #0
    adc r0, r3, r0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    ldr r2, [sp, #0x84]
    mov r0, r1, asr #31
    umull r5, r3, r1, r2
    adds r2, r5, #2048
    mov r5, r2, lsr #12
    ldr r2, [sp, #0x7c]
    mla r3, r1, r2, r3
    ldr r2, [sp, #0x84]
    mla r3, r0, r2, r3
    adc r2, r3, #0
    orrs r5, r5, r2, lsl #20
    bmi ov000_021de34c_L6b0
    ldr r2, [sp, #0x4]
    ldr r11, [sp, #0xa8]
    str r2, [sp, #0xa4]
    ldr r2, [sp, #0x8]
    str r11, [sp, #0x9c]
    add r10, r2, r1
    umull r3, r2, r1, r1
    mla r2, r1, r0, r2
    mla r2, r0, r1, r2
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    mov r0, #65536
    subs r0, r0, r3
    mov r0, #0
    str r10, [sp, #0xa0]
    sbcs r0, r0, r2, asr #12
    blt ov000_021de34c_L6b0
    ldr r0, [r4, #0x10]
    ldr r1, [r4, #0xc]
    sub r8, r0, r10
    ldr r2, [r4, #0x14]
    ldr r0, [sp, #0x4]
    sub r9, r1, r11
    ldr r1, [r4, #0x18]
    sub r7, r2, r0
    ldr r0, [r4, #0x1c]
    sub r6, r1, r11
    sub r5, r0, r10
    ldr r1, [r4, #0x20]
    ldr r0, [sp, #0x4]
    sub lr, r1, r0
    mov r0, r5, asr #31
    str r0, [sp, #0x28]
    mov r0, r7, asr #31
    str r0, [sp, #0x2c]
    mov r0, lr, asr #31
    str r0, [sp, #0x30]
    mov r0, r8, asr #31
    str r0, [sp, #0x34]
    mov r0, r9, asr #31
    str r0, [sp, #0x38]
    mov r0, r6, asr #31
    str r0, [sp, #0x3c]
    ldr r0, [r4, #0x4]
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
    ldr r2, [sp, #0x50]
    smull r1, r0, r9, r5
    mov r2, r2, asr #31
    str r2, [sp, #0x54]
    smull r3, r2, r8, r6
    subs r1, r1, r3
    sbc r2, r0, r2
    mov r0, #2048
    adds r3, r1, r0
    mov r0, #0
    adc r1, r2, r0
    mov r0, r3, lsr #12
    orr r0, r0, r1, lsl #20
    str r0, [sp, #0x8c]
    smull r3, r2, r8, r14
    smull r0, r1, r7, r5
    subs r0, r3, r0
    sbc r2, r2, r1
    adds r1, r0, #2048
    mov r0, #0
    adc r0, r2, r0
    mov r3, r1, lsr #12
    orr r3, r3, r0, lsl #20
    smull r12, r0, r9, r14
    smull r2, r1, r7, r6
    subs r2, r2, r12
    str r0, [sp, #0x58]
    sbc r0, r1, r0
    adds r1, r2, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    ldr r2, [sp, #0x40]
    orr r1, r1, r0, lsl #20
    smull r1, r0, r2, r1
    ldr r2, [sp, #0x48]
    smlal r1, r0, r2, r3
    ldr r3, [sp, #0x50]
    ldr r2, [sp, #0x8c]
    smlal r1, r0, r3, r2
    adds r2, r1, #2048
    adc r0, r0, #0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    bmi ov000_021de34c_L690
    ldr r0, [r4, #0x28]
    ldr r1, [r4, #0x24]
    sub r3, r0, r10
    ldr r2, [r4, #0x2c]
    ldr r0, [sp, #0x4]
    sub r12, r1, r11
    sub r2, r2, r0
    mov r0, r2, asr #31
    str r0, [sp, #0x90]
    mov r0, r12, asr #31
    str r0, [sp, #0x94]
    umull r4, r0, r6, r3
    mov r1, r3, asr #31
    str r4, [sp, #0x68]
    mla r0, r6, r1, r0
    ldr r4, [sp, #0x3c]
    mla r0, r4, r3, r0
    umull r4, r10, r5, r12
    str r10, [sp, #0x6c]
    ldr r10, [sp, #0x68]
    subs r11, r10, r4
    ldr r10, [sp, #0x6c]
    ldr r4, [sp, #0x94]
    mla r4, r5, r4, r10
    ldr r10, [sp, #0x28]
    mla r4, r10, r12, r4
    str r4, [sp, #0x6c]
    sbc r0, r0, r4
    adds r4, r11, #2048
    adc r0, r0, #0
    mov r11, r4, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x64]
    mov r0, r11, asr #31
    ldr r4, [sp, #0x50]
    str r0, [sp, #0x98]
    umull r10, r0, r4, r11
    str r10, [sp, #0x5c]
    mov r10, r4
    ldr r4, [sp, #0x98]
    mla r0, r10, r4, r0
    ldr r4, [sp, #0x54]
    mla r0, r4, r11, r0
    str r0, [sp, #0x60]
    umull r0, r4, r5, r2
    str r0, [sp, #0x74]
    ldr r0, [sp, #0x90]
    mla r4, r5, r0, r4
    ldr r0, [sp, #0x28]
    ldr r5, [sp, #0x74]
    mla r4, r0, r2, r4
    umull r10, r0, r14, r3
    subs r5, r5, r10
    mla r0, r14, r1, r0
    ldr r10, [sp, #0x30]
    mla r0, r10, r3, r0
    sbc r4, r4, r0
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r4, r0
    mov r5, r5, lsr #12
    orr r5, r5, r0, lsl #20
    ldr r0, [sp, #0x48]
    mov r11, r5, asr #31
    umull r4, r10, r0, r5
    mla r10, r0, r11, r10
    ldr r0, [sp, #0x4c]
    str r4, [sp, #0x70]
    mla r10, r0, r5, r10
    umull r0, r4, r14, r12
    str r0, [sp, #0x78]
    ldr r0, [sp, #0x94]
    ldr r5, [sp, #0x78]
    mla r4, r14, r0, r4
    ldr r0, [sp, #0x30]
    mla r4, r0, r12, r4
    umull r11, r0, r6, r2
    subs r5, r5, r11
    ldr r11, [sp, #0x90]
    mla r0, r6, r11, r0
    ldr r6, [sp, #0x3c]
    ldr r11, [sp, #0x40]
    mla r0, r6, r2, r0
    sbc r4, r4, r0
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r4, r0
    mov r4, r5, lsr #12
    orr r4, r4, r0, lsl #20
    umull r6, r5, r11, r4
    ldr r11, [sp, #0x70]
    mov r0, r4, asr #31
    adds r6, r11, r6
    ldr r11, [sp, #0x40]
    mla r5, r11, r0, r5
    ldr r0, [sp, #0x44]
    mla r5, r0, r4, r5
    ldr r0, [sp, #0x5c]
    adc r4, r10, r5
    adds r5, r0, r6
    ldr r0, [sp, #0x60]
    adc r4, r0, r4
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r4, r0
    mov r4, r5, lsr #12
    orrs r4, r4, r0, lsl #20
    movmi r0, #0
    bmi ov000_021de34c_L690
    ldr r0, [sp, #0x34]
    umull r6, r5, r12, r8
    mla r5, r12, r0, r5
    ldr r0, [sp, #0x94]
    mla r5, r0, r8, r5
    umull r0, r4, r3, r9
    subs r6, r6, r0
    ldr r0, [sp, #0x38]
    mla r4, r3, r0, r4
    mla r4, r1, r9, r4
    mov r0, #2048
    sbc r4, r5, r4
    adds r5, r6, r0
    mov r0, #0
    adc r0, r4, r0
    mov r5, r5, lsr #12
    orr r5, r5, r0, lsl #20
    ldr r6, [sp, #0x50]
    mov r10, r5, asr #31
    umull r4, r0, r6, r5
    mla r0, r6, r10, r0
    ldr r6, [sp, #0x54]
    ldr r10, [sp, #0x2c]
    mla r0, r6, r5, r0
    umull r6, r5, r3, r7
    mla r5, r3, r10, r5
    mla r5, r1, r7, r5
    umull r1, r10, r2, r8
    ldr r3, [sp, #0x34]
    subs r1, r6, r1
    mla r10, r2, r3, r10
    ldr r3, [sp, #0x90]
    mla r10, r3, r8, r10
    sbc r5, r5, r10
    adds r6, r1, #2048
    adc r3, r5, #0
    mov r1, r6, lsr #12
    orr r1, r1, r3, lsl #20
    ldr r3, [sp, #0x48]
    mov r8, r1, asr #31
    umull r6, r5, r3, r1
    mla r5, r3, r8, r5
    ldr r3, [sp, #0x4c]
    ldr r8, [sp, #0x38]
    mla r5, r3, r1, r5
    umull r3, r1, r2, r9
    mla r1, r2, r8, r1
    ldr r2, [sp, #0x90]
    mla r1, r2, r9, r1
    umull r9, r8, r12, r7
    ldr r2, [sp, #0x2c]
    subs r3, r3, r9
    mla r8, r12, r2, r8
    ldr r2, [sp, #0x94]
    mla r8, r2, r7, r8
    sbc r2, r1, r8
    adds r3, r3, #2048
    adc r1, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r1, lsl #20
    mov r1, r11
    mov r2, r3, asr #31
    umull r8, r7, r1, r3
    mla r7, r1, r2, r7
    ldr r1, [sp, #0x44]
    adds r2, r6, r8
    mla r7, r1, r3, r7
    adc r1, r5, r7
    adds r2, r4, r2
    adc r1, r0, r1
    mov r0, #2048
    adds r2, r2, r0
    mov r0, #0
    adc r0, r1, r0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    movpl r0, #1
ov000_021de34c_L690:
    cmp r0, #0
    beq ov000_021de34c_L6b0
    ldr r1, [sp, #0xa0]
    mov r0, #1
    str r0, [sp, #0x14]
    add r0, r1, #4096
    str r0, [sp, #0xa0]
    b ov000_021de34c_L6c8
ov000_021de34c_L6b0:
    ldr r0, [sp, #0x1c]
    add r1, r0, #1
    ldr r0, [sp, #0x18]
    str r1, [sp, #0x1c]
    cmp r1, r0
    blt ov000_021de34c_Lac
ov000_021de34c_L6c8:
    ldr r0, [sp, #0x14]
    cmp r0, #0
    ldrne r0, [sp]
    cmpne r0, #0
    beq ov000_021de34c_L6ec
    ldr r3, [sp]
    add r0, sp, #156
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021de34c_L6ec:
    ldr r0, [sp, #0x14]
    add sp, sp, #180
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
