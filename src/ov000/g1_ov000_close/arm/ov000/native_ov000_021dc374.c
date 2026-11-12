/* ov000 row 0x021dc374: 2028 bytes.
 *
 * What it does: 506 instructions; 8 call(s) to 0x021da4d4, 0x021dcb2c, 0x021dcb14, +5 more; loops (back edge at +0x54); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x7e8 -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x88 -> +0x7b8
 *   branch +0xd8 -> +0x7a0
 *   branch +0x110 -> +0x784
 *   branch +0x160 -> +0x174
 *   branch +0x170 -> +0x784
 *   branch +0x1b8 -> +0x784
 *   branch +0x2ac -> +0x784
 *   branch +0x2f0 -> +0x784
 *   branch +0x43c -> +0x74c
 *   branch +0x608 -> +0x74c
 *   branch +0x750 -> +0x784
 *   branch +0x780 -> +0x7a0
 *   back edge +0x79c -> +0x104
 *   back edge +0x7b4 -> +0x94
 *   branch +0x7c8 -> +0x7dc
 *   test +0x1c cmp r0, #0
 *   test +0x70 cmp r0, #0
 *   test +0xd4 cmp r0, #0
 *   test +0x10c tst r1, r0
 *   test +0x15c cmp r0, #0
 *   test +0x74c cmp r0, #0
 *   test +0x798 cmp r1, r0
 *   test +0x7b0 cmp r1, r0
 *   test +0x7bc cmp r0, #0
 *   test +0x7c4 cmpne r0, #0
 *   5 block transfer(s), 55 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dc374; the literal pool and
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


asm u32 native_ov000_021dc374 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #240
    ldr r4, =0x0223142c
    str r0, [sp, #0x4]
    ldr r0, [r4, #0x79c]
    str r1, [sp, #0x8]
    str r0, [sp, #0x14]
    cmp r0, #0
    mov r0, #0
    str r2, [sp, #0xc]
    str r3, [sp, #0x10]
    str r0, [sp, #0x20]
    addeq sp, sp, #240
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x14]
    ldrsh r0, [r0, #8]
    str r0, [sp, #0x2c]
    mov r0, r1
    ldrsb r1, [r0, #1]
    ldr r2, [sp, #0x2c]
    add r0, sp, #184
    bl native_fn_021da4d4
    ldr r0, [sp, #0x4]
    add r3, sp, #228
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0x2c]
    ldr r1, [sp, #0xe8]
    cmp r0, #0
    add r0, r1, #4096
    str r0, [sp, #0x1c]
    str r0, [sp, #0xe8]
    mov r0, #0
    str r0, [sp, #0x34]
    ble ov000_021dc374_L7b8
    ldr r0, [sp, #0xec]
    str r0, [sp, #0x18]
ov000_021dc374_L94:
    ldr r0, [sp, #0x34]
    add r1, sp, #184
    ldrsb r0, [r1, r0]
    mov r2, #12
    str r0, [sp, #0x24]
    mov r0, #0
    str r0, [sp, #0x30]
    ldr r1, [sp, #0x24]
    ldr r0, [sp, #0x14]
    mla r0, r1, r2, r0
    ldr r1, [r0, #0xc]
    ldr r0, [r0, #0x10]
    str r0, [sp, #0x28]
    ldr r0, [sp, #0x14]
    add r4, r0, r1
    ldr r0, [sp, #0x28]
    cmp r0, #0
    ble ov000_021dc374_L7a0
    mvn r0, #0
    str r0, [sp, #0x98]
    mov r0, r0, lsl #12
    str r0, [sp, #0xa4]
    ldr r0, [sp, #0x98]
    mov r0, r0, lsl #12
    str r0, [sp, #0xa0]
    ldr r0, [sp, #0x98]
    mov r0, r0, lsl #12
    str r0, [sp, #0x9c]
ov000_021dc374_L104:
    ldrb r1, [r4, #0x42]
    ldr r0, [sp, #0x10]
    tst r1, r0
    beq ov000_021dc374_L784
    ldr r0, [sp, #0x4]
    ldr r1, [r4, #0x34]
    ldr r2, [r0, #0x4]
    ldr r6, [r0]
    sub r0, r2, r1
    smull r2, r1, r0, r0
    ldr r0, [sp, #0x4]
    ldr r3, [r4, #0x30]
    ldr r5, [r0, #0x8]
    sub r0, r6, r3
    smlal r2, r1, r0, r0
    ldr r3, [r4, #0x38]
    ldr r0, [sp, #0x8]
    sub r3, r5, r3
    smlal r2, r1, r3, r3
    ldrsb r0, [r0]
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    cmp r0, #0
    beq ov000_021dc374_L174
    subs r0, r2, #589824
    mov r0, #0
    rscs r0, r0, r1, asr #12
    bge ov000_021dc374_L784
ov000_021dc374_L174:
    ldr r0, [sp, #0x9c]
    ldmia r4, {r7, r9}
    umull r1, r2, r9, r0
    mov r0, #2048
    adds r0, r1, r0
    mov r1, r0, lsr #12
    ldr r0, [sp, #0x98]
    ldr r5, [r4, #0x8]
    mla r2, r9, r0, r2
    ldr r0, [sp, #0x9c]
    mov r8, r9, asr #31
    mla r2, r8, r0, r2
    mov r0, #0
    adc r0, r2, r0
    mov r6, r7, asr #31
    mov r3, r5, asr #31
    orrs r1, r1, r0, lsl #20
    beq ov000_021dc374_L784
    ldr r2, [r4, #0x10]
    ldr r0, [sp, #0x1c]
    ldr r10, [r4, #0x14]
    sub r2, r2, r0
    ldr r0, [sp, #0x18]
    ldr r12, [r4, #0xc]
    sub r0, r10, r0
    mov r10, r2, asr #31
    ldr r11, [sp, #0xe4]
    str r10, [sp, #0x3c]
    sub r10, r12, r11
    mov r11, r10, asr #31
    str r11, [sp, #0x38]
    mov lr, r0, asr #31
    umull r12, r11, r5, r0
    mla r11, r5, r14, r11
    mla r11, r3, r0, r11
    ldr r5, [sp, #0x38]
    umull r3, r0, r7, r10
    mla r0, r7, r5, r0
    mla r0, r6, r10, r0
    ldr r5, [sp, #0x3c]
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
    ldr r1, [sp, #0xa4]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    ldr r1, [sp, #0x98]
    mla r3, r0, r1, r3
    ldr r0, [sp, #0xa4]
    mla r3, r2, r0, r3
    mov r0, #2048
    adds r1, r5, r0
    mov r0, #0
    adc r0, r3, r0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    ldr r2, [sp, #0xa0]
    mov r0, r1, asr #31
    umull r5, r3, r1, r2
    adds r2, r5, #2048
    mov r5, r2, lsr #12
    ldr r2, [sp, #0x98]
    mla r3, r1, r2, r3
    ldr r2, [sp, #0xa0]
    mla r3, r0, r2, r3
    adc r2, r3, #0
    orrs r5, r5, r2, lsl #20
    bmi ov000_021dc374_L784
    ldr r2, [sp, #0x18]
    ldr r10, [sp, #0xe4]
    str r2, [sp, #0xe0]
    ldr r2, [sp, #0x1c]
    str r10, [sp, #0xd8]
    add r9, r2, r1
    umull r3, r2, r1, r1
    mla r2, r1, r0, r2
    mla r2, r0, r1, r2
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    mov r0, #16384
    subs r0, r0, r3
    mov r0, #0
    str r9, [sp, #0xdc]
    sbcs r0, r0, r2, asr #12
    blt ov000_021dc374_L784
    ldr r0, [r4, #0x10]
    ldr r1, [r4, #0xc]
    sub r7, r0, r9
    ldr r2, [r4, #0x14]
    ldr r0, [sp, #0x18]
    sub r8, r1, r10
    ldr r1, [r4, #0x18]
    sub r6, r2, r0
    ldr r0, [r4, #0x1c]
    sub r5, r1, r10
    sub lr, r0, r9
    ldr r1, [r4, #0x20]
    ldr r0, [sp, #0x18]
    sub r12, r1, r0
    mov r0, lr, asr #31
    str r0, [sp, #0x40]
    mov r0, r6, asr #31
    str r0, [sp, #0x44]
    mov r0, r12, asr #31
    str r0, [sp, #0x48]
    mov r0, r7, asr #31
    str r0, [sp, #0x4c]
    mov r0, r8, asr #31
    str r0, [sp, #0x50]
    mov r0, r5, asr #31
    str r0, [sp, #0x54]
    ldr r0, [r4, #0x4]
    str r0, [sp, #0x58]
    ldr r0, [r4]
    str r0, [sp, #0x60]
    ldr r0, [sp, #0x58]
    mov r0, r0, asr #31
    str r0, [sp, #0x5c]
    ldr r0, [sp, #0x60]
    mov r0, r0, asr #31
    str r0, [sp, #0x64]
    ldr r0, [r4, #0x8]
    str r0, [sp, #0x68]
    ldr r2, [sp, #0x68]
    smull r1, r0, r8, r14
    mov r2, r2, asr #31
    str r2, [sp, #0x6c]
    smull r3, r2, r7, r5
    subs r1, r1, r3
    sbc r2, r0, r2
    mov r0, #2048
    adds r3, r1, r0
    mov r0, #0
    adc r1, r2, r0
    mov r0, r3, lsr #12
    orr r0, r0, r1, lsl #20
    str r0, [sp, #0xa8]
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
    str r0, [sp, #0x70]
    sbc r0, r1, r0
    adds r1, r2, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    ldr r2, [sp, #0x58]
    orr r1, r1, r0, lsl #20
    smull r1, r0, r2, r1
    ldr r2, [sp, #0x60]
    smlal r1, r0, r2, r3
    ldr r3, [sp, #0x68]
    ldr r2, [sp, #0xa8]
    smlal r1, r0, r3, r2
    adds r2, r1, #2048
    adc r0, r0, #0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    bmi ov000_021dc374_L74c
    ldr r0, [r4, #0x28]
    ldr r1, [r4, #0x24]
    sub r2, r0, r9
    mov r0, r2, asr #31
    sub r3, r1, r10
    str r0, [sp, #0xac]
    ldr r1, [r4, #0x2c]
    ldr r0, [sp, #0x18]
    sub r1, r1, r0
    mov r0, r1, asr #31
    str r0, [sp, #0xb0]
    mov r0, r3, asr #31
    str r0, [sp, #0x74]
    umull r9, r0, r5, r2
    str r9, [sp, #0x84]
    ldr r9, [sp, #0xac]
    mla r0, r5, r9, r0
    ldr r9, [sp, #0x54]
    mla r0, r9, r2, r0
    umull r9, r10, r14, r3
    str r10, [sp, #0x88]
    ldr r10, [sp, #0x84]
    subs r11, r10, r9
    ldr r10, [sp, #0x74]
    ldr r9, [sp, #0x88]
    mla r9, r14, r10, r9
    ldr r10, [sp, #0x40]
    mla r9, r10, r3, r9
    str r9, [sp, #0x88]
    sbc r0, r0, r9
    adds r9, r11, #2048
    adc r0, r0, #0
    mov r11, r9, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x80]
    mov r0, r11, asr #31
    ldr r9, [sp, #0x68]
    str r0, [sp, #0xb4]
    umull r10, r0, r9, r11
    str r10, [sp, #0x78]
    mov r10, r9
    ldr r9, [sp, #0xb4]
    mla r0, r10, r9, r0
    ldr r9, [sp, #0x6c]
    mla r0, r9, r11, r0
    str r0, [sp, #0x7c]
    umull r0, r9, r14, r1
    str r0, [sp, #0x90]
    ldr r0, [sp, #0xb0]
    ldr r10, [sp, #0x90]
    mla r9, r14, r0, r9
    ldr r0, [sp, #0x40]
    mla r9, r0, r1, r9
    umull r11, r0, r12, r2
    subs r10, r10, r11
    ldr r11, [sp, #0xac]
    mla r0, r12, r11, r0
    ldr r11, [sp, #0x48]
    mla r0, r11, r2, r0
    sbc r9, r9, r0
    mov r0, #2048
    adds r10, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r10, r10, lsr #12
    orr r10, r10, r0, lsl #20
    ldr r0, [sp, #0x60]
    mov lr, r10, asr #31
    umull r9, r11, r0, r10
    mla r11, r0, r14, r11
    ldr r0, [sp, #0x64]
    str r9, [sp, #0x8c]
    mla r11, r0, r10, r11
    umull r0, r9, r12, r3
    str r0, [sp, #0x94]
    ldr r0, [sp, #0x74]
    ldr r10, [sp, #0x94]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x48]
    mla r9, r0, r3, r9
    umull r12, r0, r5, r1
    subs r10, r10, r12
    ldr r12, [sp, #0xb0]
    mla r0, r5, r12, r0
    ldr r5, [sp, #0x54]
    ldr r12, [sp, #0x58]
    mla r0, r5, r1, r0
    sbc r5, r9, r0
    mov r0, #2048
    adds r9, r10, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orr r5, r5, r0, lsl #20
    umull r10, r9, r12, r5
    ldr r12, [sp, #0x8c]
    mov r0, r5, asr #31
    adds r10, r12, r10
    ldr r12, [sp, #0x58]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x5c]
    mla r9, r0, r5, r9
    ldr r0, [sp, #0x78]
    adc r5, r11, r9
    adds r9, r0, r10
    ldr r0, [sp, #0x7c]
    adc r5, r0, r5
    mov r0, #2048
    adds r9, r9, r0
    mov r0, #0
    adc r0, r5, r0
    mov r5, r9, lsr #12
    orrs r5, r5, r0, lsl #20
    movmi r0, #0
    bmi ov000_021dc374_L74c
    ldr r5, [sp, #0x4c]
    umull r9, r0, r3, r7
    mla r0, r3, r5, r0
    ldr r5, [sp, #0x74]
    mla r0, r5, r7, r0
    umull r5, r10, r2, r8
    subs r5, r9, r5
    ldr r9, [sp, #0x50]
    mla r10, r2, r9, r10
    ldr r9, [sp, #0xac]
    mla r10, r9, r8, r10
    sbc r9, r0, r10
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r9, r0
    mov r9, r5, lsr #12
    orr r9, r9, r0, lsl #20
    ldr r10, [sp, #0x68]
    mov r11, r9, asr #31
    umull r5, r0, r10, r9
    mla r0, r10, r11, r0
    ldr r10, [sp, #0x6c]
    ldr r11, [sp, #0x44]
    mla r0, r10, r9, r0
    umull r10, r9, r2, r6
    mla r9, r2, r11, r9
    ldr r2, [sp, #0xac]
    mla r9, r2, r6, r9
    umull r11, r2, r1, r7
    subs r10, r10, r11
    ldr r11, [sp, #0x4c]
    mla r2, r1, r11, r2
    ldr r11, [sp, #0xb0]
    mla r2, r11, r7, r2
    sbc r7, r9, r2
    adds r9, r10, #2048
    adc r7, r7, #0
    mov r2, r9, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x60]
    mov r11, r2, asr #31
    umull r10, r9, r7, r2
    mla r9, r7, r11, r9
    ldr r7, [sp, #0x64]
    ldr r11, [sp, #0x50]
    mla r9, r7, r2, r9
    umull r7, r2, r1, r8
    mla r2, r1, r11, r2
    ldr r1, [sp, #0xb0]
    mla r2, r1, r8, r2
    ldr r1, [sp, #0x44]
    umull r11, r8, r3, r6
    mla r8, r3, r1, r8
    ldr r1, [sp, #0x74]
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
    ldr r1, [sp, #0x5c]
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
ov000_021dc374_L74c:
    cmp r0, #0
    beq ov000_021dc374_L784
    mov r3, r4
    ldr r4, [sp, #0x14]
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x24]
    ldr r2, [sp, #0x30]
    str r4, [sp]
    bl native_fn_021da520
    ldr r0, [sp, #0x2c]
    str r0, [sp, #0x34]
    mov r0, #1
    str r0, [sp, #0x20]
    b ov000_021dc374_L7a0
ov000_021dc374_L784:
    ldr r0, [sp, #0x30]
    add r4, r4, #68
    add r1, r0, #1
    ldr r0, [sp, #0x28]
    str r1, [sp, #0x30]
    cmp r1, r0
    blt ov000_021dc374_L104
ov000_021dc374_L7a0:
    ldr r0, [sp, #0x34]
    add r1, r0, #1
    ldr r0, [sp, #0x2c]
    str r1, [sp, #0x34]
    cmp r1, r0
    blt ov000_021dc374_L94
ov000_021dc374_L7b8:
    ldr r0, [sp, #0x20]
    cmp r0, #0
    ldrne r0, [sp, #0xc]
    cmpne r0, #0
    beq ov000_021dc374_L7dc
    ldr r3, [sp, #0xc]
    add r0, sp, #216
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021dc374_L7dc:
    ldr r0, [sp, #0x20]
    add sp, sp, #240
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
