/* ov000 row 0x0220daf8: 1196 bytes.
 *
 * What it does: 296 instructions; 20 call(s) to 0x021d8a50, 0x021d8aa0, 0x02002618, +17 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x4a0 -> constant 0x00000fff (image word 0x00000fff)
 *   pool +0x4a4 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x4a8 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x14 -> +0x204
 *   branch +0x90 -> +0xa8
 *   branch +0xa4 -> +0xb4
 *   branch +0x20c -> +0x318
 *   branch +0x320 -> +0x34c
 *   branch +0x354 -> +0x458
 *   branch +0x460 -> +0x494
 *   test +0x10 cmp r0, #0
 *   test +0x88 cmp r4, #0
 *   test +0x208 cmp r0, #10
 *   test +0x308 cmp r0, #32
 *   test +0x31c cmp r0, #20
 *   test +0x350 cmp r0, #21
 *   test +0x44c cmp r0, #32
 *   test +0x45c cmp r0, #100
 *   6 block transfer(s), 29 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220daf8; the literal pool and
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

extern void native_fn_021d8a50(void);
extern void native_fn_021d8aa0(void);
extern void native_fn_02002618(void);
extern void native_fn_0203d294(void);
extern void native_fn_02000ce8(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02028044(void);
extern void native_fn_0200103c(void);
extern void native_fn_021e07b8(void);
extern void native_fn_020420c4(void);
extern void native_fn_02042c0c(void);
extern void native_fn_0220a2a4(void);
extern void native_fn_02209c68(void);


asm u32 native_ov000_0220daf8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #48
    mov r5, r0
    ldrb r0, [r5, #0x279]
    cmp r0, #0
    bne ov000_0220daf8_L204
    mov r0, #0
    bl native_fn_021d8a50
    mov r4, r0
    mov r0, #0
    bl native_fn_021d8aa0
    ldr r3, [r0]
    ldr r1, [r4]
    mov r2, #0
    sub r1, r3, r1
    str r1, [sp, #0x24]
    ldr r3, [r0, #0x4]
    ldr r1, [r4, #0x4]
    sub r1, r3, r1
    str r1, [sp, #0x28]
    ldr r3, [r0, #0x8]
    ldr r1, [r4, #0x8]
    add r0, sp, #36
    sub r3, r3, r1
    mov r1, r0
    str r3, [sp, #0x2c]
    str r2, [sp, #0x28]
    bl native_fn_02002618
    mvn r0, #-2147483648
    bl native_fn_0203d294
    and r1, r0, #63
    add r0, sp, #0
    sub r4, r1, #32
    bl native_fn_02000ce8
    cmp r4, #0
    mov r0, r4, lsl #12
    ble ov000_0220daf8_La8
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_0220daf8_Lb4
ov000_0220daf8_La8:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_0220daf8_Lb4:
    bl native_fn_020259b4
    mov r1, r0
    add r0, sp, #0
    bl native_fn_02028044
    add r0, sp, #36
    add r1, sp, #0
    mov r2, r0
    bl native_fn_0200103c
    ldr r2, [sp, #0x24]
    mov r1, #40960
    umull r14, r12, r2, r1
    mov r0, r2, asr #31
    adds r2, lr, #2048
    mla r12, r0, r1, r12
    ldr r4, [sp, #0x28]
    adc r0, r12, #0
    mov r2, r2, lsr #12
    orr r2, r2, r0, lsl #20
    str r2, [sp, #0x24]
    mov r0, #0
    umull r14, r12, r4, r1
    mov r2, r4, asr #31
    adds r4, lr, #2048
    mla r12, r2, r1, r12
    ldr r3, [sp, #0x2c]
    adc r2, r12, #0
    mov r4, r4, lsr #12
    orr r4, r4, r2, lsl #20
    str r4, [sp, #0x28]
    umull r12, r4, r3, r1
    mov r2, r3, asr #31
    mla r4, r2, r1, r4
    adds r2, r12, #2048
    adc r1, r4, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    sub r0, r0, #-2147483647
    str r2, [sp, #0x2c]
    bl native_fn_0203d294
    ldr r1, =0x00000fff
    ldr r2, [sp, #0x28]
    and r0, r0, r1
    add r0, r0, #32768
    add r0, r2, r0
    str r0, [sp, #0x28]
    ldr r2, [r5, #0x70]
    ldr r1, [sp, #0x24]
    mov r0, #0
    add r1, r2, r1
    str r1, [r5, #0x70]
    ldr r2, [r5, #0x74]
    ldr r1, [sp, #0x28]
    add r1, r2, r1
    str r1, [r5, #0x74]
    ldr r2, [r5, #0x78]
    ldr r1, [sp, #0x2c]
    add r1, r2, r1
    str r1, [r5, #0x78]
    bl native_fn_021e07b8
    mov r1, r0
    mov r0, r5
    bl native_fn_020420c4
    mov r0, r5
    mov r1, #31
    bl native_fn_02042c0c
    add r0, r5, #112
    add lr, r5, #656
    ldmia r0, {r0, r1, r2}
    stmia lr, {r0, r1, r2}
    add r12, r5, #680
    add r4, r5, #668
    ldmia r12, {r0, r1, r2}
    stmia r4, {r0, r1, r2}
    mov r3, #1
    mov r0, r5
    mov r1, #2
    mov r2, #0
    strb r3, [r5, #0x2c1]
    bl native_fn_0220a2a4
    mov r1, #0
    add r0, r5, #512
    strh r1, [r0, #122]
    mov r0, #10
    strb r0, [r5, #0x279]
ov000_0220daf8_L204:
    ldrb r0, [r5, #0x279]
    cmp r0, #10
    bne ov000_0220daf8_L318
    add r3, r5, #512
    ldrsh r0, [r3, #122]
    mov r1, #90
    ldr r2, =0x0b60b60b
    mov r4, r0, lsl #12
    mov r0, r4, asr #4
    add r0, r4, r0, lsr #27
    mov r0, r0, asr #5
    mul r1, r0, r1
    mov r0, #182
    umull r12, r4, r1, r2
    mla r4, r1, r0, r4
    mov r0, r1, asr #31
    mla r4, r0, r2, r4
    adds r0, r12, #0
    adc r0, r4, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r2, r0, lsl #1
    ldr r1, =0x020d3fe0
    mov r0, r2, lsl #1
    ldrsh r12, [r1, r0]
    add r0, r2, #1
    mov r0, r0, lsl #1
    ldrsh r0, [r1, r0]
    ldr r4, [r5, #0x294]
    ldr r1, [r5, #0x2a0]
    rsb r0, r0, #4096
    sub r1, r1, r4
    smull r2, r1, r12, r1
    adds r2, r2, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    add r1, r4, r2
    str r1, [r5, #0x74]
    ldr r12, [r5, #0x290]
    ldr r2, [r5, #0x29c]
    mov r1, #0
    sub r2, r2, r12
    smull r4, r2, r0, r2
    adds r4, r4, #2048
    adc r2, r2, #0
    mov r4, r4, lsr #12
    orr r4, r4, r2, lsl #20
    add r2, r12, r4
    str r2, [r5, #0x70]
    ldr r12, [r5, #0x298]
    ldr r2, [r5, #0x2a4]
    sub r2, r2, r12
    smull r4, r2, r0, r2
    adds r4, r4, #2048
    adc r0, r2, #0
    mov r2, r4, lsr #12
    orr r2, r2, r0, lsl #20
    add r0, r12, r2
    str r0, [r5, #0x78]
    ldrsh r0, [r3, #122]
    add r0, r0, #1
    strh r0, [r3, #122]
    ldrsh r0, [r3, #122]
    cmp r0, #32
    strgth r1, [r3, #122]
    movgt r0, #20
    strgtb r0, [r5, #0x279]
ov000_0220daf8_L318:
    ldrb r0, [r5, #0x279]
    cmp r0, #20
    bne ov000_0220daf8_L34c
    ldr r2, [r5, #0x29c]
    ldr r1, [r5, #0x290]
    mov r0, #21
    rsb r1, r1, r2, lsl #1
    str r1, [r5, #0x290]
    ldr r2, [r5, #0x2a4]
    ldr r1, [r5, #0x298]
    rsb r1, r1, r2, lsl #1
    str r1, [r5, #0x298]
    strb r0, [r5, #0x279]
ov000_0220daf8_L34c:
    ldrb r0, [r5, #0x279]
    cmp r0, #21
    bne ov000_0220daf8_L458
    add r3, r5, #512
    ldrsh r0, [r3, #122]
    mov r1, #90
    ldr r2, =0x0b60b60b
    mov r4, r0, lsl #12
    mov r0, r4, asr #4
    add r0, r4, r0, lsr #27
    mov r0, r0, asr #5
    mul r1, r0, r1
    mov r0, #182
    umull r12, r4, r1, r2
    mla r4, r1, r0, r4
    mov r0, r1, asr #31
    mla r4, r0, r2, r4
    adds r0, r12, #0
    adc r0, r4, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r2, r0, lsl #1
    mov r0, r2, lsl #1
    ldr r1, =0x020d3fe0
    ldr lr, [r5, #0x29c]
    ldr r4, [r5, #0x290]
    add r2, r2, #1
    ldrsh r0, [r1, r0]
    sub r4, r4, lr
    mov r2, r2, lsl #1
    smull r12, r4, r0, r4
    adds r12, r12, #2048
    adc r4, r4, #0
    mov r12, r12, lsr #12
    orr r12, r12, r4, lsl #20
    add r4, lr, r12
    str r4, [r5, #0x70]
    ldrsh r1, [r1, r2]
    ldr r12, [r5, #0x2a4]
    ldr r2, [r5, #0x298]
    rsb r4, r1, #4096
    sub r1, r2, r12
    smull r2, r1, r0, r1
    adds r2, r2, #2048
    adc r0, r1, #0
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    add r0, r12, r1
    str r0, [r5, #0x78]
    ldr r2, [r5, #0x2a0]
    ldr r0, [r5, #0x294]
    sub r0, r0, r2
    smull r1, r0, r4, r0
    adds r1, r1, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    add r0, r2, r1
    str r0, [r5, #0x74]
    ldrsh r0, [r3, #122]
    add r0, r0, #1
    strh r0, [r3, #122]
    ldrsh r0, [r3, #122]
    cmp r0, #32
    movgt r0, #100
    strgtb r0, [r5, #0x279]
ov000_0220daf8_L458:
    ldrb r0, [r5, #0x279]
    cmp r0, #100
    bne ov000_0220daf8_L494
    mov r4, #0
    strb r4, [r5, #0x2c1]
    add r0, r5, #680
    add r3, r5, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, r5
    mov r1, r4
    bl native_fn_02042c0c
    mov r0, r5
    mov r1, #3
    bl native_fn_02209c68
ov000_0220daf8_L494:
    mov r0, #0
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, pc}
}
