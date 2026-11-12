/* ov000 row 0x021db15c: 2000 bytes.
 *
 * What it does: 499 instructions; 5 call(s) to 0x021db8f8, 0x021db8d4, 0x0200235c, +2 more; loops (back edge at +0x1fc); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x7cc -> constant 0x0223142c (image word 0x0223142c)
 *   branch +0x58 -> +0x7c
 *   branch +0x78 -> +0x98
 *   branch +0xa8 -> +0x79c
 *   branch +0xec -> +0x778
 *   branch +0x124 -> +0x75c
 *   branch +0x16c -> +0x75c
 *   branch +0x260 -> +0x75c
 *   branch +0x3c8 -> +0x6dc
 *   branch +0x598 -> +0x6dc
 *   branch +0x6e0 -> +0x75c
 *   branch +0x738 -> +0x75c
 *   back edge +0x774 -> +0x118
 *   back edge +0x798 -> +0xc4
 *   branch +0x7ac -> +0x7c0
 *   test +0x1c cmp r0, #0
 *   test +0x54 cmp r0, #1
 *   test +0x9c cmp r0, #0
 *   test +0xe0 cmp r0, #0
 *   test +0x120 tst r1, r0
 *   test +0x6dc cmp r0, #0
 *   test +0x770 cmp r1, r0
 *   test +0x788 cmp r1, r0
 *   test +0x7a0 cmp r0, #0
 *   test +0x7a8 cmpne r0, #0
 *   7 block transfer(s), 59 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021db15c; the literal pool and
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


asm u32 native_ov000_021db15c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #216
    ldr r3, =0x0223142c
    str r0, [sp]
    ldr r0, [r3, #0x79c]
    str r1, [sp, #0x4]
    str r0, [sp, #0x14]
    cmp r0, #0
    mov r0, #0
    str r2, [sp, #0x8]
    str r0, [sp, #0x28]
    addeq sp, sp, #216
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x14]
    add r3, sp, #204
    ldrsh r0, [r0, #8]
    str r0, [sp, #0x30]
    ldr r0, [sp]
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0x8]
    cmp r0, #1
    bne ov000_021db15c_L7c
    ldr r0, [sp, #0x28]
    ldr r1, [sp, #0xd0]
    str r0, [sp, #0x24]
    add r0, r1, #163840
    str r0, [sp, #0xd0]
    mov r0, #26214400
    str r0, [sp, #0x20]
    b ov000_021db15c_L98
ov000_021db15c_L7c:
    ldr r0, [sp, #0x28]
    ldr r1, [sp, #0xd0]
    str r0, [sp, #0x24]
    add r0, r1, #20480
    str r0, [sp, #0xd0]
    mov r0, #40960
    str r0, [sp, #0x20]
ov000_021db15c_L98:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    mov r0, #0
    str r0, [sp, #0x38]
    ble ov000_021db15c_L79c
    ldr r0, [sp, #0xd0]
    str r0, [sp, #0x18]
    ldr r0, [sp, #0xd4]
    str r0, [sp, #0xc]
    ldr r0, [sp, #0x14]
    str r0, [sp, #0x1c]
ov000_021db15c_Lc4:
    ldr r0, [sp, #0x1c]
    ldr r1, [r0, #0xc]
    ldr r0, [r0, #0x10]
    str r0, [sp, #0x2c]
    ldr r0, [sp, #0x14]
    add r4, r0, r1
    ldr r0, [sp, #0x2c]
    cmp r0, #0
    mov r0, #0
    str r0, [sp, #0x34]
    ble ov000_021db15c_L778
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
ov000_021db15c_L118:
    ldrb r1, [r4, #0x42]
    ldr r0, [sp, #0x8]
    tst r1, r0
    beq ov000_021db15c_L75c
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
    beq ov000_021db15c_L75c
    ldr r2, [r4, #0x10]
    ldr r0, [sp, #0x18]
    ldr r10, [r4, #0x14]
    sub r2, r2, r0
    ldr r0, [sp, #0xc]
    ldr r12, [r4, #0xc]
    sub r0, r10, r0
    mov r10, r2, asr #31
    ldr r11, [sp, #0xcc]
    str r10, [sp, #0x40]
    sub r10, r12, r11
    mov r11, r10, asr #31
    str r11, [sp, #0x3c]
    mov lr, r0, asr #31
    umull r12, r11, r5, r0
    mla r11, r5, r14, r11
    mla r11, r3, r0, r11
    ldr r5, [sp, #0x3c]
    umull r3, r0, r7, r10
    mla r0, r7, r5, r0
    mla r0, r6, r10, r0
    ldr r5, [sp, #0x40]
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
    adds r2, r5, r0
    mov r0, #0
    adc r1, r3, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    ldr r1, [sp, #0xa0]
    mov r2, r0, asr #31
    umull r5, r3, r0, r1
    adds r1, r5, #2048
    mov r5, r1, lsr #12
    ldr r1, [sp, #0x98]
    mla r3, r0, r1, r3
    ldr r1, [sp, #0xa0]
    mla r3, r2, r1, r3
    adc r1, r3, #0
    orrs r5, r5, r1, lsl #20
    bmi ov000_021db15c_L75c
    ldr r1, [sp, #0x18]
    ldr r10, [sp, #0xcc]
    add r0, r1, r0
    str r0, [sp, #0x10]
    str r0, [sp, #0xb8]
    ldr r0, [sp, #0xc]
    ldr r2, [r4, #0x10]
    str r0, [sp, #0xbc]
    ldr r0, [r4, #0xc]
    ldr r1, [r4, #0x14]
    sub r8, r0, r10
    ldr r0, [sp, #0x10]
    str r10, [sp, #0xb4]
    sub r7, r2, r0
    ldr r0, [sp, #0xc]
    sub r6, r1, r0
    ldr r0, [r4, #0x18]
    ldr r1, [r4, #0x1c]
    sub r5, r0, r10
    ldr r0, [sp, #0x10]
    sub lr, r1, r0
    mov r0, lr, asr #31
    str r0, [sp, #0x44]
    ldr r1, [r4, #0x20]
    ldr r0, [sp, #0xc]
    sub r12, r1, r0
    mov r0, r6, asr #31
    str r0, [sp, #0x48]
    mov r0, r12, asr #31
    str r0, [sp, #0x4c]
    mov r0, r7, asr #31
    str r0, [sp, #0x50]
    mov r0, r8, asr #31
    str r0, [sp, #0x54]
    mov r0, r5, asr #31
    str r0, [sp, #0x58]
    ldr r0, [r4, #0x4]
    str r0, [sp, #0x5c]
    ldr r0, [r4]
    str r0, [sp, #0x64]
    ldr r0, [sp, #0x5c]
    mov r0, r0, asr #31
    str r0, [sp, #0x60]
    ldr r0, [sp, #0x64]
    mov r0, r0, asr #31
    str r0, [sp, #0x68]
    ldr r0, [r4, #0x8]
    str r0, [sp, #0x6c]
    ldr r2, [sp, #0x6c]
    smull r1, r0, r8, r14
    mov r2, r2, asr #31
    str r2, [sp, #0x70]
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
    ldr r2, [sp, #0x5c]
    orr r0, r0, r1, lsl #20
    smull r1, r0, r2, r0
    ldr r2, [sp, #0x64]
    smlal r1, r0, r2, r3
    ldr r2, [sp, #0x6c]
    smlal r1, r0, r2, r9
    adds r2, r1, #2048
    adc r0, r0, #0
    mov r1, r2, lsr #12
    orrs r1, r1, r0, lsl #20
    movmi r0, #0
    bmi ov000_021db15c_L6dc
    ldr r0, [r4, #0x24]
    ldr r1, [r4, #0x28]
    sub r3, r0, r10
    ldr r0, [sp, #0x10]
    sub r2, r1, r0
    mov r0, r2, asr #31
    str r0, [sp, #0xa8]
    ldr r1, [r4, #0x2c]
    ldr r0, [sp, #0xc]
    sub r1, r1, r0
    mov r0, r1, asr #31
    str r0, [sp, #0xac]
    mov r0, r3, asr #31
    str r0, [sp, #0x74]
    umull r9, r0, r5, r2
    str r9, [sp, #0x84]
    ldr r9, [sp, #0xa8]
    mla r0, r5, r9, r0
    ldr r9, [sp, #0x58]
    mla r0, r9, r2, r0
    umull r9, r10, r14, r3
    str r10, [sp, #0x88]
    ldr r10, [sp, #0x84]
    subs r11, r10, r9
    ldr r10, [sp, #0x74]
    ldr r9, [sp, #0x88]
    mla r9, r14, r10, r9
    ldr r10, [sp, #0x44]
    mla r9, r10, r3, r9
    str r9, [sp, #0x88]
    sbc r0, r0, r9
    adds r9, r11, #2048
    adc r0, r0, #0
    mov r11, r9, lsr #12
    orr r11, r11, r0, lsl #20
    str r0, [sp, #0x80]
    mov r0, r11, asr #31
    ldr r9, [sp, #0x6c]
    str r0, [sp, #0xb0]
    umull r10, r0, r9, r11
    str r10, [sp, #0x78]
    mov r10, r9
    ldr r9, [sp, #0xb0]
    mla r0, r10, r9, r0
    ldr r9, [sp, #0x70]
    mla r0, r9, r11, r0
    str r0, [sp, #0x7c]
    umull r0, r9, r14, r1
    str r0, [sp, #0x90]
    ldr r0, [sp, #0xac]
    ldr r10, [sp, #0x90]
    mla r9, r14, r0, r9
    ldr r0, [sp, #0x44]
    mla r9, r0, r1, r9
    umull r11, r0, r12, r2
    subs r10, r10, r11
    ldr r11, [sp, #0xa8]
    mla r0, r12, r11, r0
    ldr r11, [sp, #0x4c]
    mla r0, r11, r2, r0
    sbc r9, r9, r0
    mov r0, #2048
    adds r10, r10, r0
    mov r0, #0
    adc r0, r9, r0
    mov r10, r10, lsr #12
    orr r10, r10, r0, lsl #20
    ldr r0, [sp, #0x64]
    mov lr, r10, asr #31
    umull r9, r11, r0, r10
    mla r11, r0, r14, r11
    ldr r0, [sp, #0x68]
    str r9, [sp, #0x8c]
    mla r11, r0, r10, r11
    umull r0, r9, r12, r3
    str r0, [sp, #0x94]
    ldr r0, [sp, #0x74]
    ldr r10, [sp, #0x94]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x4c]
    mla r9, r0, r3, r9
    umull r12, r0, r5, r1
    subs r10, r10, r12
    ldr r12, [sp, #0xac]
    mla r0, r5, r12, r0
    ldr r5, [sp, #0x58]
    ldr r12, [sp, #0x5c]
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
    ldr r12, [sp, #0x5c]
    mla r9, r12, r0, r9
    ldr r0, [sp, #0x60]
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
    bmi ov000_021db15c_L6dc
    ldr r5, [sp, #0x50]
    umull r9, r0, r3, r7
    mla r0, r3, r5, r0
    ldr r5, [sp, #0x74]
    mla r0, r5, r7, r0
    umull r5, r10, r2, r8
    subs r5, r9, r5
    ldr r9, [sp, #0x54]
    mla r10, r2, r9, r10
    ldr r9, [sp, #0xa8]
    mla r10, r9, r8, r10
    sbc r9, r0, r10
    mov r0, #2048
    adds r5, r5, r0
    mov r0, #0
    adc r0, r9, r0
    mov r9, r5, lsr #12
    orr r9, r9, r0, lsl #20
    ldr r10, [sp, #0x6c]
    mov r11, r9, asr #31
    umull r5, r0, r10, r9
    mla r0, r10, r11, r0
    ldr r10, [sp, #0x70]
    ldr r11, [sp, #0x48]
    mla r0, r10, r9, r0
    umull r10, r9, r2, r6
    mla r9, r2, r11, r9
    ldr r2, [sp, #0xa8]
    mla r9, r2, r6, r9
    umull r11, r2, r1, r7
    subs r10, r10, r11
    ldr r11, [sp, #0x50]
    mla r2, r1, r11, r2
    ldr r11, [sp, #0xac]
    mla r2, r11, r7, r2
    sbc r7, r9, r2
    adds r9, r10, #2048
    adc r7, r7, #0
    mov r2, r9, lsr #12
    orr r2, r2, r7, lsl #20
    ldr r7, [sp, #0x64]
    mov r11, r2, asr #31
    umull r10, r9, r7, r2
    mla r9, r7, r11, r9
    ldr r7, [sp, #0x68]
    ldr r11, [sp, #0x54]
    mla r9, r7, r2, r9
    umull r7, r2, r1, r8
    mla r2, r1, r11, r2
    ldr r1, [sp, #0xac]
    mla r2, r1, r8, r2
    ldr r1, [sp, #0x48]
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
    ldr r1, [sp, #0x60]
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
ov000_021db15c_L6dc:
    cmp r0, #0
    beq ov000_021db15c_L75c
    ldr r0, [sp]
    ldr r5, [sp, #0xb4]
    ldr r1, [r0, #0x4]
    ldr r6, [r0]
    ldr r0, [sp, #0x10]
    sub r0, r1, r0
    smull r2, r1, r0, r0
    ldr r0, [sp]
    ldr r3, [r0, #0x8]
    sub r0, r6, r5
    smlal r2, r1, r0, r0
    ldr r0, [sp, #0xc]
    sub r0, r3, r0
    smlal r2, r1, r0, r0
    mov r3, r2, lsr #12
    ldr r0, [sp, #0x20]
    orr r3, r3, r1, lsl #20
    subs r0, r3, r0
    ldr r0, [sp, #0x24]
    mov r2, r1, asr #12
    sbcs r0, r2, r0
    bge ov000_021db15c_L75c
    mov r0, #1
    str r3, [sp, #0x20]
    str r0, [sp, #0x28]
    add r0, sp, #180
    str r2, [sp, #0x24]
    add r3, sp, #192
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021db15c_L75c:
    ldr r0, [sp, #0x34]
    add r4, r4, #68
    add r1, r0, #1
    ldr r0, [sp, #0x2c]
    str r1, [sp, #0x34]
    cmp r1, r0
    blt ov000_021db15c_L118
ov000_021db15c_L778:
    ldr r0, [sp, #0x38]
    add r1, r0, #1
    ldr r0, [sp, #0x30]
    str r1, [sp, #0x38]
    cmp r1, r0
    ldr r0, [sp, #0x1c]
    add r0, r0, #12
    str r0, [sp, #0x1c]
    blt ov000_021db15c_Lc4
ov000_021db15c_L79c:
    ldr r0, [sp, #0x28]
    cmp r0, #0
    ldrne r0, [sp, #0x4]
    cmpne r0, #0
    beq ov000_021db15c_L7c0
    ldr r3, [sp, #0x4]
    add r0, sp, #192
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021db15c_L7c0:
    ldr r0, [sp, #0x28]
    add sp, sp, #216
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
