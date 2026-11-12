/* ov000 row 0x021da5e4: 2080 bytes.
 *
 * What it does: 518 instructions; 7 call(s) to 0x021da4d4, 0x021dadcc, 0x021dada8, +4 more; loops (back edge at +0x54); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x818 -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x81c -> constant 0x022303ec (image word 0x022303ec)
 *   branch +0x70 -> +0x94
 *   branch +0x90 -> +0xb0
 *   branch +0xc0 -> +0x7e8
 *   branch +0x11c -> +0x7c4
 *   branch +0x154 -> +0x7a8
 *   branch +0x19c -> +0x7a8
 *   branch +0x290 -> +0x7a8
 *   branch +0x3f8 -> +0x70c
 *   branch +0x5c8 -> +0x70c
 *   branch +0x710 -> +0x7a8
 *   branch +0x768 -> +0x7a8
 *   back edge +0x7c0 -> +0x148
 *   back edge +0x7e4 -> +0xdc
 *   branch +0x7f8 -> +0x80c
 *   test +0x1c cmp r0, #0
 *   test +0x6c cmp r0, #1
 *   test +0xb4 cmp r0, #0
 *   test +0x118 cmp r0, #0
 *   test +0x150 tst r1, r0
 *   test +0x70c cmp r0, #0
 *   test +0x7bc cmp r1, r0
 *   test +0x7d4 cmp r1, r0
 *   test +0x7ec cmp r0, #0
 *   test +0x7f4 cmpne r0, #0
 *   7 block transfer(s), 62 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021da5e4; the literal pool and
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

extern void native_fn_021da4d4(void);
extern void native_fn_0200235c(void);
extern void native_fn_021da520(void);


asm u32 native_ov000_021da5e4 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #228
    ldr r4, =0x0223142c
    str r0, [sp, #0x4]
    ldr r0, [r4, #0x79c]
    str r1, [sp, #0x8]
    str r0, [sp, #0x1c]
    cmp r0, #0
    mov r0, #0
    str r2, [sp, #0xc]
    str r3, [sp, #0x10]
    str r0, [sp, #0x30]
    addeq sp, sp, #228
    ldmeqia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x1c]
    ldrsh r0, [r0, #8]
    str r0, [sp, #0x3c]
    mov r0, r1
    ldrsb r1, [r0, #1]
    ldr r0, =0x022303ec
    ldr r2, [sp, #0x3c]
    bl native_fn_021da4d4
    ldr r0, [sp, #0x4]
    add r3, sp, #216
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0x10]
    cmp r0, #1
    bne ov000_021da5e4_L94
    ldr r1, [sp, #0xdc]
    mov r0, #26214400
    str r0, [sp, #0x28]
    add r0, r1, #163840
    str r0, [sp, #0xdc]
    mov r0, #0
    str r0, [sp, #0x2c]
    b ov000_021da5e4_Lb0
ov000_021da5e4_L94:
    ldr r1, [sp, #0xdc]
    mov r0, #40960
    str r0, [sp, #0x28]
    add r0, r1, #20480
    str r0, [sp, #0xdc]
    mov r0, #0
    str r0, [sp, #0x2c]
ov000_021da5e4_Lb0:
    ldr r0, [sp, #0x3c]
    cmp r0, #0
    mov r0, #0
    str r0, [sp, #0x44]
    ble ov000_021da5e4_L7e8
    ldr r0, [sp, #0xdc]
    str r0, [sp, #0x20]
    ldr r0, [sp, #0xe0]
    str r0, [sp, #0x14]
    ldr r0, =0x022303ec
    str r0, [sp, #0x24]
ov000_021da5e4_Ldc:
    ldr r0, [sp, #0x24]
    mov r2, #12
    ldrsb r0, [r0]
    str r0, [sp, #0x34]
    mov r0, #0
    str r0, [sp, #0x40]
    ldr r1, [sp, #0x34]
    ldr r0, [sp, #0x1c]
    mla r0, r1, r2, r0
    ldr r1, [r0, #0xc]
    ldr r0, [r0, #0x10]
    str r0, [sp, #0x38]
    ldr r0, [sp, #0x1c]
    add r4, r0, r1
    ldr r0, [sp, #0x38]
    cmp r0, #0
    ble ov000_021da5e4_L7c4
    mvn r0, #0
    str r0, [sp, #0xa4]
    mov r0, r0, lsl #12
    str r0, [sp, #0xb0]
    ldr r0, [sp, #0xa4]
    mov r0, r0, lsl #12
    str r0, [sp, #0xac]
    ldr r0, [sp, #0xa4]
    mov r0, r0, lsl #12
    str r0, [sp, #0xa8]
ov000_021da5e4_L148:
    ldrb r1, [r4, #0x42]
    ldr r0, [sp, #0x10]
    tst r1, r0
    beq ov000_021da5e4_L7a8
    ldr r0, [sp, #0xa8]
    ldmia r4, {r7, r9}
    umull r1, r2, r9, r0
    mov r0, #2048
    adds r0, r1, r0
    mov r1, r0, lsr #12
    ldr r0, [sp, #0xa4]
    ldr r5, [r4, #0x8]
    mla r2, r9, r0, r2
    ldr r0, [sp, #0xa8]
    mov r8, r9, asr #31
    mla r2, r8, r0, r2
    mov r0, #0
    adc r0, r2, r0
    mov r6, r7, asr #31
    mov r3, r5, asr #31
    orrs r1, r1, r0, lsl #20
    beq ov000_021da5e4_L7a8
    ldr r2, [r4, #0x10]
    ldr r0, [sp, #0x20]
    ldr r10, [r4, #0x14]
    sub r2, r2, r0
    ldr r0, [sp, #0x14]
    ldr r12, [r4, #0xc]
    sub r0, r10, r0
    mov r10, r2, asr #31
    ldr r11, [sp, #0xd8]
    str r10, [sp, #0x4c]
    sub r10, r12, r11
    mov r11, r10, asr #31
    str r11, [sp, #0x48]
    mov lr, r0, asr #31
    umull r12, r11, r5, r0
    mla r11, r5, r14, r11
    mla r11, r3, r0, r11
    ldr r5, [sp, #0x48]
    umull r3, r0, r7, r10
    mla r0, r7, r5, r0
    mla r0, r6, r10, r0
    ldr r5, [sp, #0x4c]
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
    ldr r1, [sp, #0xb0]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    ldr r1, [sp, #0xa4]
    mla r3, r0, r1, r3
    ldr r0, [sp, #0xb0]
    mla r3, r2, r0, r3
    mov r0, #2048
    adds r2, r5, r0
    mov r0, #0
    adc r1, r3, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    ldr r1, [sp, #0xac]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    adds r1, r5, #2048
    mov r5, r1, lsr #12
    ldr r1, [sp, #0xa4]
    mla r3, r0, r1, r3
    ldr r1, [sp, #0xac]
    mla r3, r2, r1, r3
    adc r1, r3, #0
    orrs r5, r5, r1, lsl #20
    bmi ov000_021da5e4_L7a8
    ldr r1, [sp, #0x20]
    ldr r10, [sp, #0xd8]
    add r0, r1, r0
    str r0, [sp, #0x18]
    str r0, [sp, #0xc4]
    ldr r0, [sp, #0x14]
    ldr r2, [r4, #0x10]
    str r0, [sp, #0xc8]
    ldr r0, [r4, #0xc]
    ldr r1, [r4, #0x14]
    sub r8, r0, r10
    ldr r0, [sp, #0x18]
    str r10, [sp, #0xc0]
    sub r7, r2, r0
    ldr r0, [sp, #0x14]
    sub r6, r1, r0
    ldr r0, [r4, #0x18]
    ldr r1, [r4, #0x1c]
    sub r5, r0, r10
    ldr r0, [sp, #0x18]
    sub lr, r1, r0
    mov r0, lr, asr #31
    str r0, [sp, #0x50]
    ldr r1, [r4, #0x20]
    ldr r0, [sp, #0x14]
    sub r12, r1, r0
    mov r0, r6, asr #31
    str r0, [sp, #0x54]
    mov r0, r12, asr #31
    str r0, [sp, #0x58]
    mov r0, r7, asr #31
    str r0, [sp, #0x5c]
    mov r0, r8, asr #31
    str r0, [sp, #0x60]
    mov r0, r5, asr #31
    str r0, [sp, #0x64]
    ldr r0, [r4, #0x4]
    str r0, [sp, #0x68]
    ldr r0, [r4]
    str r0, [sp, #0x70]
    ldr r0, [sp, #0x68]
    mov r0, r0, asr #31
    str r0, [sp, #0x6c]
    ldr r0, [sp, #0x70]
    mov r0, r0, asr #31
    str r0, [sp, #0x74]
    ldr r0, [r4, #0x8]
    str r0, [sp, #0x78]
    ldr r2, [sp, #0x78]
    smull r1, r0, r8, r14
    mov r2, r2, asr #31
    str r2, [sp, #0x7c]
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
    ldr r2, [sp, #0x68]
    orr r0, r0, r1, lsl #20
    smull r1, r0, r2, r0
    ldr r2, [sp, #0x70]
    smlal r1, r0, r2, r3
    ldr r2, [sp, #0x78]
    smlal r1, r0, r2, r9
    adds r2, r1, #2048
    adc r0, r0, #0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    bmi ov000_021da5e4_L70c
    ldr r0, [r4, #0x24]
    ldr r1, [r4, #0x28]
    sub r3, r0, r10
    ldr r0, [sp, #0x18]
    sub r2, r1, r0
    mov r0, r2, asr #31
    str r0, [sp, #0xb4]
    ldr r1, [r4, #0x2c]
    ldr r0, [sp, #0x14]
    sub r1, r1, r0
    mov r0, r1, asr #31
    str r0, [sp, #0xb8]
    mov r0, r3, asr #31
    str r0, [sp, #0x80]
    umull r9, r0, r5, r2
    str r9, [sp, #0x90]
    ldr r9, [sp, #0xb4]
    mla r0, r5, r9, r0
    ldr r9, [sp, #0x64]
    mla r0, r9, r2, r0
    umull r9, r10, r14, r3
    str r10, [sp, #0x94]
    ldr r10, [sp, #0x90]
    subs r11, r10, r9
    ldr r10, [sp, #0x80]
    ldr r9, [sp, #0x94]
    mla r9, r14, r10, r9
    ldr r10, [sp, #0x50]
    mla r9, r10, r3, r9
    str r9, [sp, #0x94]
    sbc r0, r0, r9
    adds r9, r11, #2048
    adc r0, r0, #0
    mov r11, r9, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x8c]
    mov r0, r11, asr #31
    ldr r9, [sp, #0x78]
    str r0, [sp, #0xbc]
    umull r10, r0, r9, r11
    str r10, [sp, #0x84]
    mov r10, r9
    ldr r9, [sp, #0xbc]
    mla r0, r10, r9, r0
    ldr r9, [sp, #0x7c]
    mla r0, r9, r11, r0
    str r0, [sp, #0x88]
    umull r0, r9, r14, r1
    str r0, [sp, #0x9c]
    ldr r0, [sp, #0xb8]
    ldr r10, [sp, #0x9c]
    mla r9, r14, r0, r9
    ldr r0, [sp, #0x50]
    mla r9, r0, r1, r9
    umull r11, r0, r12, r2
    subs r10, r10, r11
    ldr r11, [sp, #0xb4]
    mla r0, r12, r11, r0
    ldr r11, [sp, #0x58]
    mla r0, r11, r2, r0
    sbc r9, r9, r0
    mov r0, #2048
    adds r10, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r10, r10, lsr #12
    orr r10, r10, r0, lsl #20
    ldr r0, [sp, #0x70]
    mov lr, r10, asr #31
    umull r9, r11, r0, r10
    mla r11, r0, r14, r11
    ldr r0, [sp, #0x74]
    str r9, [sp, #0x98]
    mla r11, r0, r10, r11
    umull r0, r9, r12, r3
    str r0, [sp, #0xa0]
    ldr r0, [sp, #0x80]
    ldr r10, [sp, #0xa0]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x58]
    mla r9, r0, r3, r9
    umull r12, r0, r5, r1
    subs r10, r10, r12
    ldr r12, [sp, #0xb8]
    mla r0, r5, r12, r0
    ldr r5, [sp, #0x64]
    ldr r12, [sp, #0x68]
    mla r0, r5, r1, r0
    sbc r5, r9, r0
    mov r0, #2048
    adds r9, r10, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orr r5, r5, r0, lsl #20
    umull r10, r9, r12, r5
    ldr r12, [sp, #0x98]
    mov r0, r5, asr #31
    adds r10, r12, r10
    ldr r12, [sp, #0x68]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x6c]
    mla r9, r0, r5, r9
    ldr r0, [sp, #0x84]
    adc r5, r11, r9
    adds r9, r0, r10
    ldr r0, [sp, #0x88]
    adc r5, r0, r5
    mov r0, #2048
    adds r9, r9, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orrs r5, r5, r0, lsl #20
    movmi r0, #0
    bmi ov000_021da5e4_L70c
    ldr r5, [sp, #0x5c]
    umull r9, r0, r3, r7
    mla r0, r3, r5, r0
    ldr r5, [sp, #0x80]
    mla r0, r5, r7, r0
    umull r5, r10, r2, r8
    subs r5, r9, r5
    ldr r9, [sp, #0x60]
    mla r10, r2, r9, r10
    ldr r9, [sp, #0xb4]
    mla r10, r9, r8, r10
    sbc r9, r0, r10
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r9, r0
    mov r9, r5, lsr #12
    orr r9, r9, r0, lsl #20
    ldr r10, [sp, #0x78]
    mov r11, r9, asr #31
    umull r5, r0, r10, r9
    mla r0, r10, r11, r0
    ldr r10, [sp, #0x7c]
    ldr r11, [sp, #0x54]
    mla r0, r10, r9, r0
    umull r10, r9, r2, r6
    mla r9, r2, r11, r9
    ldr r2, [sp, #0xb4]
    mla r9, r2, r6, r9
    umull r11, r2, r1, r7
    subs r10, r10, r11
    ldr r11, [sp, #0x5c]
    mla r2, r1, r11, r2
    ldr r11, [sp, #0xb8]
    mla r2, r11, r7, r2
    sbc r7, r9, r2
    adds r9, r10, #2048
    adc r7, r7, #0
    mov r2, r9, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x70]
    mov r11, r2, asr #31
    umull r10, r9, r7, r2
    mla r9, r7, r11, r9
    ldr r7, [sp, #0x74]
    ldr r11, [sp, #0x60]
    mla r9, r7, r2, r9
    umull r7, r2, r1, r8
    mla r2, r1, r11, r2
    ldr r1, [sp, #0xb8]
    mla r2, r1, r8, r2
    ldr r1, [sp, #0x54]
    umull r11, r8, r3, r6
    mla r8, r3, r1, r8
    ldr r1, [sp, #0x80]
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
    ldr r1, [sp, #0x6c]
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
ov000_021da5e4_L70c:
    cmp r0, #0
    beq ov000_021da5e4_L7a8
    ldr r0, [sp, #0x4]
    ldr r5, [sp, #0xc0]
    ldr r1, [r0, #0x4]
    ldr r6, [r0]
    ldr r0, [sp, #0x18]
    sub r0, r1, r0
    smull r2, r1, r0, r0
    ldr r0, [sp, #0x4]
    ldr r3, [r0, #0x8]
    sub r0, r6, r5
    smlal r2, r1, r0, r0
    ldr r0, [sp, #0x14]
    sub r0, r3, r0
    smlal r2, r1, r0, r0
    mov r3, r2, lsr #12
    ldr r0, [sp, #0x28]
    orr r3, r3, r1, lsl #20
    subs r0, r3, r0
    ldr r0, [sp, #0x2c]
    mov r2, r1, asr #12
    sbcs r0, r2, r0
    bge ov000_021da5e4_L7a8
    add r0, sp, #192
    str r2, [sp, #0x2c]
    add r5, sp, #204
    ldmia r0, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldr r0, [sp, #0x1c]
    str r3, [sp, #0x28]
    str r0, [sp]
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x34]
    ldr r2, [sp, #0x40]
    mov r3, r4
    bl native_fn_021da520
    mov r0, #1
    str r0, [sp, #0x30]
ov000_021da5e4_L7a8:
    ldr r0, [sp, #0x40]
    add r4, r4, #68
    add r1, r0, #1
    ldr r0, [sp, #0x38]
    str r1, [sp, #0x40]
    cmp r1, r0
    blt ov000_021da5e4_L148
ov000_021da5e4_L7c4:
    ldr r0, [sp, #0x44]
    add r1, r0, #1
    ldr r0, [sp, #0x3c]
    str r1, [sp, #0x44]
    cmp r1, r0
    ldr r0, [sp, #0x24]
    add r0, r0, #1
    str r0, [sp, #0x24]
    blt ov000_021da5e4_Ldc
ov000_021da5e4_L7e8:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    ldrne r0, [sp, #0xc]
    cmpne r0, #0
    beq ov000_021da5e4_L80c
    ldr r3, [sp, #0xc]
    add r0, sp, #204
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021da5e4_L80c:
    ldr r0, [sp, #0x30]
    add sp, sp, #228
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
