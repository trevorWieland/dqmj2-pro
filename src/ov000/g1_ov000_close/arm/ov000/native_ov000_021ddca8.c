/* ov000 row 0x021ddca8: 1700 bytes.
 *
 * What it does: 423 instructions; 6 call(s) to 0x021dd50c, 0x021de338, 0x021de314, +3 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x69c -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x6a0 -> constant 0x00323063 (image word 0x00323063)
 *   branch +0x24 -> +0x690
 *   branch +0x38 -> +0x690
 *   branch +0x6c -> +0x66c
 *   branch +0xbc -> +0x650
 *   branch +0x1a0 -> +0x650
 *   branch +0x1e4 -> +0x650
 *   branch +0x330 -> +0x640
 *   branch +0x4fc -> +0x640
 *   branch +0x64c -> +0x66c
 *   back edge +0x668 -> +0x80
 *   branch +0x67c -> +0x690
 *   test +0x1c cmp r5, #0
 *   test +0x34 cmp r0, #0
 *   test +0x5c cmp r0, #0
 *   test +0x640 cmp r0, #0
 *   test +0x664 cmp r1, r0
 *   test +0x670 cmp r0, #0
 *   test +0x678 cmpne r0, #0
 *   5 block transfer(s), 40 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021ddca8; the literal pool and
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

extern void native_fn_021dd50c(void);
extern void native_fn_0200235c(void);


asm u32 native_ov000_021ddca8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #160
    ldr r2, =0x0223142c
    mov r6, r0
    ldr r5, [r2, #0x7a0]
    mov r0, #0
    str r1, [sp]
    cmp r5, #0
    str r0, [sp, #0xc]
    beq ov000_021ddca8_L690
    ldr r1, =0x00323063
    mov r0, r5
    bl native_fn_021dd50c
    cmp r0, #0
    blt ov000_021ddca8_L690
    mov r1, #12
    mla r3, r0, r1, r5
    add r4, sp, #148
    ldmia r6, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
    ldr r0, [r3, #0x10]
    ldr r1, [r3, #0xc]
    str r0, [sp, #0x10]
    cmp r0, #0
    mov r0, #0
    add r4, r5, r1
    str r0, [sp, #0x14]
    ble ov000_021ddca8_L66c
    ldr r0, [sp, #0x98]
    str r0, [sp, #0x8]
    ldr r0, [sp, #0x9c]
    str r0, [sp, #0x4]
ov000_021ddca8_L80:
    mov r0, #20480
    ldmia r4, {r7, r9}
    umull r1, r2, r9, r0
    mov r0, #2048
    adds r0, r1, r0
    mov r1, r0, lsr #12
    mov r8, r9, asr #31
    mov r0, #20480
    mla r2, r8, r0, r2
    ldr r5, [r4, #0x8]
    mov r0, #0
    adc r0, r2, r0
    mov r6, r7, asr #31
    mov r3, r5, asr #31
    orrs r1, r1, r0, lsl #20
    beq ov000_021ddca8_L650
    ldr r2, [r4, #0x10]
    ldr r0, [sp, #0x8]
    ldr r10, [r4, #0x14]
    sub r2, r2, r0
    ldr r0, [sp, #0x4]
    ldr r12, [r4, #0xc]
    sub r0, r10, r0
    mov r10, r2, asr #31
    ldr r11, [sp, #0x94]
    str r10, [sp, #0x1c]
    sub r10, r12, r11
    mov r11, r10, asr #31
    str r11, [sp, #0x18]
    mov lr, r0, asr #31
    umull r12, r11, r5, r0
    mla r11, r5, r14, r11
    mla r11, r3, r0, r11
    ldr r5, [sp, #0x18]
    umull r3, r0, r7, r10
    mla r0, r7, r5, r0
    mla r0, r6, r10, r0
    ldr r5, [sp, #0x1c]
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
    mov r1, #20480
    umull r5, r3, r0, r1
    mov r2, r0, asr #31
    mov r0, #20480
    mla r3, r2, r0, r3
    mov r0, #2048
    adds r1, r5, r0
    mov r0, #0
    adc r0, r3, r0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    mov r2, #20480
    umull r5, r3, r1, r2
    adds r2, r5, #2048
    mov r5, r2, lsr #12
    mov r0, r1, asr #31
    mov r2, #20480
    mla r3, r0, r2, r3
    adc r2, r3, #0
    orrs r5, r5, r2, lsl #20
    bmi ov000_021ddca8_L650
    ldr r2, [sp, #0x4]
    ldr r10, [sp, #0x94]
    str r2, [sp, #0x90]
    ldr r2, [sp, #0x8]
    str r10, [sp, #0x88]
    add r9, r2, r1
    umull r3, r2, r1, r1
    mla r2, r1, r0, r2
    mla r2, r0, r1, r2
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    mov r0, #102400
    subs r0, r0, r3
    mov r0, #0
    str r9, [sp, #0x8c]
    sbcs r0, r0, r2, asr #12
    blt ov000_021ddca8_L650
    ldr r0, [r4, #0x10]
    ldr r1, [r4, #0xc]
    sub r7, r0, r9
    ldr r2, [r4, #0x14]
    ldr r0, [sp, #0x4]
    sub r8, r1, r10
    ldr r1, [r4, #0x18]
    sub r6, r2, r0
    ldr r0, [r4, #0x1c]
    sub r5, r1, r10
    sub lr, r0, r9
    ldr r1, [r4, #0x20]
    ldr r0, [sp, #0x4]
    sub r12, r1, r0
    mov r0, lr, asr #31
    str r0, [sp, #0x20]
    mov r0, r6, asr #31
    str r0, [sp, #0x24]
    mov r0, r12, asr #31
    str r0, [sp, #0x28]
    mov r0, r7, asr #31
    str r0, [sp, #0x2c]
    mov r0, r8, asr #31
    str r0, [sp, #0x30]
    mov r0, r5, asr #31
    str r0, [sp, #0x34]
    ldr r0, [r4, #0x4]
    str r0, [sp, #0x38]
    ldr r0, [r4]
    str r0, [sp, #0x40]
    ldr r0, [sp, #0x38]
    mov r0, r0, asr #31
    str r0, [sp, #0x3c]
    ldr r0, [sp, #0x40]
    mov r0, r0, asr #31
    str r0, [sp, #0x44]
    ldr r0, [r4, #0x8]
    str r0, [sp, #0x48]
    ldr r2, [sp, #0x48]
    smull r1, r0, r8, r14
    mov r2, r2, asr #31
    str r2, [sp, #0x4c]
    smull r3, r2, r7, r5
    subs r1, r1, r3
    sbc r2, r0, r2
    mov r0, #2048
    adds r3, r1, r0
    mov r0, #0
    adc r1, r2, r0
    mov r0, r3, lsr #12
    orr r0, r0, r1, lsl #20
    str r0, [sp, #0x78]
    smull r3, r2, r7, r12
    smull r0, r1, r6, r14
    subs r0, r3, r0
    sbc r2, r2, r1
    adds r1, r0, #2048
    mov r0, #0
    adc r0, r2, r0
    mov r3, r1, lsr #12
    orr r3, r3, r0, lsl #20
    smull r11, r0, r8, r12
    smull r2, r1, r6, r5
    subs r2, r2, r11
    str r0, [sp, #0x50]
    sbc r0, r1, r0
    adds r1, r2, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    ldr r2, [sp, #0x38]
    orr r1, r1, r0, lsl #20
    smull r1, r0, r2, r1
    ldr r2, [sp, #0x40]
    smlal r1, r0, r2, r3
    ldr r3, [sp, #0x48]
    ldr r2, [sp, #0x78]
    smlal r1, r0, r3, r2
    adds r2, r1, #2048
    adc r0, r0, #0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    bmi ov000_021ddca8_L640
    ldr r0, [r4, #0x28]
    ldr r1, [r4, #0x24]
    sub r2, r0, r9
    mov r0, r2, asr #31
    sub r3, r1, r10
    str r0, [sp, #0x7c]
    ldr r1, [r4, #0x2c]
    ldr r0, [sp, #0x4]
    sub r1, r1, r0
    mov r0, r1, asr #31
    str r0, [sp, #0x80]
    mov r0, r3, asr #31
    str r0, [sp, #0x54]
    umull r9, r0, r5, r2
    str r9, [sp, #0x64]
    ldr r9, [sp, #0x7c]
    mla r0, r5, r9, r0
    ldr r9, [sp, #0x34]
    mla r0, r9, r2, r0
    umull r9, r10, r14, r3
    str r10, [sp, #0x68]
    ldr r10, [sp, #0x64]
    subs r11, r10, r9
    ldr r10, [sp, #0x54]
    ldr r9, [sp, #0x68]
    mla r9, r14, r10, r9
    ldr r10, [sp, #0x20]
    mla r9, r10, r3, r9
    str r9, [sp, #0x68]
    sbc r0, r0, r9
    adds r9, r11, #2048
    adc r0, r0, #0
    mov r11, r9, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x60]
    mov r0, r11, asr #31
    ldr r9, [sp, #0x48]
    str r0, [sp, #0x84]
    umull r10, r0, r9, r11
    str r10, [sp, #0x58]
    mov r10, r9
    ldr r9, [sp, #0x84]
    mla r0, r10, r9, r0
    ldr r9, [sp, #0x4c]
    mla r0, r9, r11, r0
    str r0, [sp, #0x5c]
    umull r0, r9, r14, r1
    str r0, [sp, #0x70]
    ldr r0, [sp, #0x80]
    ldr r10, [sp, #0x70]
    mla r9, r14, r0, r9
    ldr r0, [sp, #0x20]
    mla r9, r0, r1, r9
    umull r11, r0, r12, r2
    subs r10, r10, r11
    ldr r11, [sp, #0x7c]
    mla r0, r12, r11, r0
    ldr r11, [sp, #0x28]
    mla r0, r11, r2, r0
    sbc r9, r9, r0
    mov r0, #2048
    adds r10, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r10, r10, lsr #12
    orr r10, r10, r0, lsl #20
    ldr r0, [sp, #0x40]
    mov lr, r10, asr #31
    umull r9, r11, r0, r10
    mla r11, r0, r14, r11
    ldr r0, [sp, #0x44]
    str r9, [sp, #0x6c]
    mla r11, r0, r10, r11
    umull r0, r9, r12, r3
    str r0, [sp, #0x74]
    ldr r0, [sp, #0x54]
    ldr r10, [sp, #0x74]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x28]
    mla r9, r0, r3, r9
    umull r12, r0, r5, r1
    subs r10, r10, r12
    ldr r12, [sp, #0x80]
    mla r0, r5, r12, r0
    ldr r5, [sp, #0x34]
    ldr r12, [sp, #0x38]
    mla r0, r5, r1, r0
    sbc r5, r9, r0
    mov r0, #2048
    adds r9, r10, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orr r5, r5, r0, lsl #20
    umull r10, r9, r12, r5
    ldr r12, [sp, #0x6c]
    mov r0, r5, asr #31
    adds r10, r12, r10
    ldr r12, [sp, #0x38]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x3c]
    mla r9, r0, r5, r9
    ldr r0, [sp, #0x58]
    adc r5, r11, r9
    adds r9, r0, r10
    ldr r0, [sp, #0x5c]
    adc r5, r0, r5
    mov r0, #2048
    adds r9, r9, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orrs r5, r5, r0, lsl #20
    movmi r0, #0
    bmi ov000_021ddca8_L640
    ldr r5, [sp, #0x2c]
    umull r9, r0, r3, r7
    mla r0, r3, r5, r0
    ldr r5, [sp, #0x54]
    mla r0, r5, r7, r0
    umull r5, r10, r2, r8
    subs r5, r9, r5
    ldr r9, [sp, #0x30]
    mla r10, r2, r9, r10
    ldr r9, [sp, #0x7c]
    mla r10, r9, r8, r10
    sbc r9, r0, r10
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r9, r0
    mov r9, r5, lsr #12
    orr r9, r9, r0, lsl #20
    ldr r10, [sp, #0x48]
    mov r11, r9, asr #31
    umull r5, r0, r10, r9
    mla r0, r10, r11, r0
    ldr r10, [sp, #0x4c]
    ldr r11, [sp, #0x24]
    mla r0, r10, r9, r0
    umull r10, r9, r2, r6
    mla r9, r2, r11, r9
    ldr r2, [sp, #0x7c]
    mla r9, r2, r6, r9
    umull r11, r2, r1, r7
    subs r10, r10, r11
    ldr r11, [sp, #0x2c]
    mla r2, r1, r11, r2
    ldr r11, [sp, #0x80]
    mla r2, r11, r7, r2
    sbc r7, r9, r2
    adds r9, r10, #2048
    adc r7, r7, #0
    mov r2, r9, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x40]
    mov r11, r2, asr #31
    umull r10, r9, r7, r2
    mla r9, r7, r11, r9
    ldr r7, [sp, #0x44]
    ldr r11, [sp, #0x30]
    mla r9, r7, r2, r9
    umull r7, r2, r1, r8
    mla r2, r1, r11, r2
    ldr r1, [sp, #0x80]
    mla r2, r1, r8, r2
    ldr r1, [sp, #0x24]
    umull r11, r8, r3, r6
    mla r8, r3, r1, r8
    ldr r1, [sp, #0x54]
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
    ldr r1, [sp, #0x3c]
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
ov000_021ddca8_L640:
    cmp r0, #0
    movne r0, #1
    strne r0, [sp, #0xc]
    bne ov000_021ddca8_L66c
ov000_021ddca8_L650:
    ldr r0, [sp, #0x14]
    add r4, r4, #68
    add r1, r0, #1
    ldr r0, [sp, #0x10]
    str r1, [sp, #0x14]
    cmp r1, r0
    blt ov000_021ddca8_L80
ov000_021ddca8_L66c:
    ldr r0, [sp, #0xc]
    cmp r0, #0
    ldrne r0, [sp]
    cmpne r0, #0
    beq ov000_021ddca8_L690
    ldr r3, [sp]
    add r0, sp, #136
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021ddca8_L690:
    ldr r0, [sp, #0xc]
    add sp, sp, #160
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
