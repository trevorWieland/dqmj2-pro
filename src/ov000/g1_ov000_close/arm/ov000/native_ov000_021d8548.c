/* ov000 row 0x021d8548: 1040 bytes.
 *
 * What it does: 246 instructions; 10 call(s) to 0x02028158, 0x021d8700, 0x021d8700, +7 more; loops (back edge at +0xe8); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 14 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x3d8 -> constant 0x02230318 (image word 0x02230318)
 *   pool +0x3dc -> constant 0x0223033c (image word 0x0223033c)
 *   pool +0x3e0 -> constant 0x000002e1 (image word 0x000002e1)
 *   pool +0x3e4 -> constant 0x00000451 (image word 0x00000451)
 *   pool +0x3e8 -> constant 0x000005c2 (image word 0x000005c2)
 *   pool +0x3ec -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x3f0 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x3f4 -> constant 0x022303a4 (image word 0x022303a4)
 *   pool +0x3f8 -> constant 0x022303b0 (image word 0x022303b0)
 *   pool +0x3fc -> constant 0x02230398 (image word 0x02230398)
 *   pool +0x400 -> constant 0x022303bc (image word 0x022303bc)
 *   pool +0x404 -> constant 0x022303c8 (image word 0x022303c8)
 *   pool +0x408 -> constant 0x02230358 (image word 0x02230358)
 *   pool +0x40c -> constant 0x02230364 (image word 0x02230364)
 *   branch +0x100 -> +0x1b8
 *   branch +0x110 -> +0x1b8
 *   branch +0x120 -> +0x1b8
 *   branch +0x1c8 -> +0x1ec
 *   branch +0x264 -> +0x2f8
 *   branch +0x27c -> +0x290
 *   branch +0x2a0 -> +0x2b8
 *   branch +0x2b4 -> +0x2f8
 *   branch +0x2c4 -> +0x2f8
 *   branch +0x2e4 -> +0x2f8
 *   test +0x0c cmp r0, #0
 *   test +0xf8 cmp r0, #820
 *   test +0x108 cmp r0, #16384
 *   test +0x118 cmp r0, #131072
 *   test +0x124 cmp r4, #0
 *   test +0x1bc cmp r5, r0
 *   test +0x260 cmp r6, #0
 *   test +0x278 cmp r0, #0
 *   test +0x29c cmp r0, #0
 *   test +0x2c0 cmp r0, #0
 *   test +0x2e0 cmp r0, #0
 *   16 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d8548; the literal pool and
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

extern void native_fn_02028158(void);
extern void native_fn_0200235c(void);
extern void native_fn_021d8378(void);
extern void native_fn_021dd54c(void);
extern void native_fn_021ddca8(void);
extern void native_fn_021e07ac(void);
extern void native_fn_021de34c(void);


asm u32 native_ov000_021d8548 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #24
    mov r6, r1
    cmp r0, #0
    ldrne r1, =0x02230318
    ldr r3, =0x0223033c
    strne r0, [r1, #0x8]
    ldr r0, =0x02230318
    add r4, sp, #12
    ldr r0, [r0, #0x8]
    ldmia r0, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
    ldr r1, [sp, #0x10]
    ldr r0, [r3, #0x58]
    ldr r2, [sp, #0xc]
    add r4, r1, r0
    str r4, [sp, #0x10]
    ldr r0, [r3, #0x8c]
    ldr r1, [r3, #0x90]
    sub r5, r2, r0
    sub r8, r4, r1
    ldr r0, =0x000002e1
    mov r1, r5, asr #31
    umull r2, r4, r5, r0
    adds r7, r2, #2048
    mla r4, r1, r0, r4
    umull r2, r5, r8, r0
    mov r1, r8, asr #31
    mla r5, r1, r0, r5
    adc r4, r4, #0
    mov r8, r7, lsr #12
    adds r7, r2, #2048
    ldr r9, [sp, #0x14]
    ldr r2, [r3, #0x94]
    ldr r1, [r3, #0x68]
    orr r8, r8, r4, lsl #20
    sub r9, r9, r2
    add r1, r1, r8
    str r1, [r3, #0x68]
    umull r4, r2, r9, r0
    mov r1, r9, asr #31
    mla r2, r1, r0, r2
    adc r5, r5, #0
    mov r7, r7, lsr #12
    adds r4, r4, #2048
    adc r1, r2, #0
    mov r2, r4, lsr #12
    ldr r0, [r3, #0x6c]
    orr r7, r7, r5, lsl #20
    add r0, r0, r7
    str r0, [r3, #0x6c]
    ldr r0, [r3, #0x70]
    orr r2, r2, r1, lsl #20
    add r0, r0, r2
    str r0, [r3, #0x70]
    ldr r1, [r3, #0x98]
    ldr r0, [r3, #0x4c]
    sub r0, r1, r0
    bl native_fn_02028158
    mov r4, r0
    add r0, r4, #154
    add r0, r0, #256
    cmp r0, #820
    ldrlo r5, =0x000002e1
    blo ov000_021d8548_L1b8
    add r0, r4, #8192
    cmp r0, #16384
    ldrlo r5, =0x00000451
    blo ov000_021d8548_L1b8
    add r0, r4, #65536
    cmp r0, #131072
    ldrlo r5, =0x000005c2
    blo ov000_021d8548_L1b8
    cmp r4, #0
    rsblt r0, r4, #0
    movge r0, r4
    sub r1, r0, #65536
    mov r0, #70
    mul r0, r1, r0
    mov r1, #671744
    bl native_fn_0200235c
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r5, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r5, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r0, r0, lsl #1
    add r1, r0, #1
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #1
    ldrsh r3, [r0, r1]
    ldr r0, =0x000005c2
    smull r2, r1, r3, r3
    adds r2, r2, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    umull r5, r3, r2, r0
    mov r1, r2, asr #31
    adds r2, r5, #2048
    mla r3, r1, r0, r3
    adc r0, r3, #0
    mov r5, r2, lsr #12
    orr r5, r5, r0, lsl #20
ov000_021d8548_L1b8:
    ldr r0, =0x000002e1
    cmp r5, r0
    ldreq r0, =0x0223033c
    ldreq r1, [r0, #0x98]
    beq ov000_021d8548_L1ec
    smull r0, r1, r4, r5
    adds r2, r0, #2048
    ldr r0, =0x0223033c
    adc r1, r1, #0
    mov r2, r2, lsr #12
    ldr r3, [r0, #0x4c]
    orr r2, r2, r1, lsl #20
    add r1, r3, r2
ov000_021d8548_L1ec:
    str r1, [r0, #0x4c]
    ldr r0, =0x0223033c
    mov r4, r5, asr #31
    ldr r1, [r0, #0x9c]
    ldr r3, [r0, #0x50]
    sub r7, r1, r3
    smull r2, r1, r7, r5
    adds r2, r2, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    add r1, r3, r2
    str r1, [r0, #0x50]
    ldr r2, [r0, #0xa0]
    ldr r1, [r0, #0x54]
    sub r2, r2, r1
    add r1, r1, r2
    str r1, [r0, #0x54]
    ldr r7, [r0, #0x58]
    ldr r1, [r0, #0xa4]
    sub r1, r1, r7
    smull r3, r2, r1, r5
    adds r3, r3, #2048
    adc r1, r2, #0
    mov r2, r3, lsr #12
    orr r2, r2, r1, lsl #20
    add r1, r7, r2
    str r1, [r0, #0x58]
    bl native_fn_021d8378
    cmp r6, #0
    beq ov000_021d8548_L2f8
    ldr r0, =0x022303a4
    ldr r1, =0x022303b0
    add r2, sp, #0
    bl native_fn_021dd54c
    cmp r0, #0
    beq ov000_021d8548_L290
    ldr r3, =0x022303b0
    add r0, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021d8548_L290:
    ldr r0, =0x022303b0
    add r1, sp, #0
    bl native_fn_021ddca8
    cmp r0, #0
    beq ov000_021d8548_L2b8
    ldr r3, =0x022303b0
    add r0, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    b ov000_021d8548_L2f8
ov000_021d8548_L2b8:
    ldr r0, =0x0223033c
    ldrb r0, [r0, #0xa8]
    cmp r0, #0
    beq ov000_021d8548_L2f8
    bl native_fn_021e07ac
    mov r1, r0
    ldr r0, =0x022303b0
    add r2, sp, #0
    add r1, r1, #528
    bl native_fn_021de34c
    cmp r0, #0
    beq ov000_021d8548_L2f8
    ldr r3, =0x022303b0
    add r0, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_021d8548_L2f8:
    ldr r6, =0x0223033c
    ldr r3, =0x02230398
    ldr r1, [r6, #0x74]
    ldr lr, [r6, #0x5c]
    ldr r0, [r6, #0x78]
    sub r7, r1, lr
    ldr r2, [r6, #0x60]
    umull r1, r8, r5, r7
    sub r12, r0, r2
    mov r0, r7, asr #31
    mla r8, r5, r0, r8
    adds r9, r1, #2048
    mla r8, r4, r7, r8
    ldr r1, [r6, #0x7c]
    ldr r0, [r6, #0x64]
    mov r7, r12, asr #31
    sub r1, r1, r0
    adc r8, r8, #0
    mov r9, r9, lsr #12
    orr r9, r9, r8, lsl #20
    add lr, lr, r9
    umull r9, r8, r5, r12
    str lr, [r6, #0x5c]
    mla r8, r5, r7, r8
    mla r8, r4, r12, r8
    adds r9, r9, #2048
    adc r7, r8, #0
    mov r8, r9, lsr #12
    orr r8, r8, r7, lsl #20
    add r2, r2, r8
    umull r14, r12, r5, r1
    str r2, [r6, #0x60]
    adds r2, lr, #2048
    mov lr, r2, lsr #12
    mov r2, r1, asr #31
    mla r12, r5, r2, r12
    mla r12, r4, r1, r12
    adc r1, r12, #0
    orr lr, lr, r1, lsl #20
    add r0, r0, lr
    str r0, [r6, #0x64]
    ldr r4, =0x022303bc
    ldmia r3, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
    ldr r12, =0x022303a4
    ldr r6, =0x022303c8
    ldr r5, =0x02230358
    ldr r4, =0x02230364
    ldmia r12, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    ldmia r3, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldmia r12, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
