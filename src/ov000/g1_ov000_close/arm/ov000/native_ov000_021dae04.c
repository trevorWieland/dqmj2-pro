/* ov000 row 0x021dae04: 856 bytes.
 *
 * What it does: 212 instructions; 7 call(s) to 0x021da4d4, 0x021db148, 0x021db124, +4 more; loops (back edge at +0x50); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x350 -> constant 0x0223142c (image word 0x0223142c)
 *   pool +0x354 -> constant 0x0223040c (image word 0x0223040c)
 *   branch +0x6c -> +0x90
 *   branch +0x8c -> +0xac
 *   branch +0xbc -> +0x344
 *   branch +0x114 -> +0x320
 *   branch +0x138 -> +0x30c
 *   branch +0x184 -> +0x30c
 *   branch +0x280 -> +0x30c
 *   branch +0x2dc -> +0x30c
 *   back edge +0x31c -> +0x12c
 *   back edge +0x340 -> +0xd8
 *   test +0x1c cmp r0, #0
 *   test +0x68 cmp r0, #1
 *   test +0xb0 cmp r0, #0
 *   test +0x110 cmp r0, #0
 *   test +0x134 tst r1, r0
 *   test +0x314 cmp r4, r0
 *   test +0x330 cmp r1, r0
 *   3 block transfer(s), 32 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021dae04; the literal pool and
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


asm u32 native_ov000_021dae04 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #104
    ldr r3, =0x0223142c
    str r0, [sp, #0x4]
    ldr r0, [r3, #0x79c]
    str r1, [sp, #0x8]
    str r0, [sp, #0x10]
    cmp r0, #0
    mov r0, #0
    str r2, [sp, #0xc]
    str r0, [sp, #0x28]
    addeq sp, sp, #104
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldr r0, [sp, #0x10]
    ldrsh r0, [r0, #8]
    str r0, [sp, #0x34]
    mov r0, r1
    ldrsb r1, [r0, #1]
    ldr r0, =0x0223040c
    ldr r2, [sp, #0x34]
    bl native_fn_021da4d4
    ldr r0, [sp, #0x4]
    add r3, sp, #92
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    ldr r0, [sp, #0xc]
    cmp r0, #1
    bne ov000_021dae04_L90
    ldr r1, [sp, #0x60]
    mov r0, #26214400
    str r0, [sp, #0x20]
    add r0, r1, #163840
    str r0, [sp, #0x60]
    mov r0, #0
    str r0, [sp, #0x24]
    b ov000_021dae04_Lac
ov000_021dae04_L90:
    ldr r1, [sp, #0x60]
    mov r0, #40960
    str r0, [sp, #0x20]
    add r0, r1, #20480
    str r0, [sp, #0x60]
    mov r0, #0
    str r0, [sp, #0x24]
ov000_021dae04_Lac:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    mov r0, #0
    str r0, [sp, #0x38]
    ble ov000_021dae04_L344
    ldr r0, [sp, #0x60]
    str r0, [sp, #0x18]
    ldr r0, [sp, #0x64]
    str r0, [sp, #0x14]
    ldr r0, =0x0223040c
    str r0, [sp, #0x1c]
ov000_021dae04_Ld8:
    ldr r0, [sp, #0x1c]
    mov r2, #12
    ldrsb r0, [r0]
    mov r4, #0
    str r0, [sp, #0x2c]
    mov r1, r0
    ldr r0, [sp, #0x10]
    mla r0, r1, r2, r0
    ldr r1, [r0, #0xc]
    ldr r0, [r0, #0x10]
    str r0, [sp, #0x30]
    ldr r0, [sp, #0x10]
    add r5, r0, r1
    ldr r0, [sp, #0x30]
    cmp r0, #0
    ble ov000_021dae04_L320
    mvn r6, #0
    mov r0, r6, lsl #12
    str r0, [sp, #0x54]
    str r0, [sp, #0x50]
    str r0, [sp, #0x58]
ov000_021dae04_L12c:
    ldrb r1, [r5, #0x42]
    ldr r0, [sp, #0xc]
    tst r1, r0
    beq ov000_021dae04_L30c
    ldmia r5, {r0, r9}
    str r0, [sp, #0x3c]
    mov r0, r0, asr #31
    str r0, [sp, #0x40]
    ldr r0, [sp, #0x58]
    ldr r7, [r5, #0x8]
    umull r1, r2, r9, r0
    mov r0, #2048
    adds r0, r1, r0
    mov r1, r0, lsr #12
    mla r2, r9, r6, r2
    ldr r0, [sp, #0x58]
    mov r8, r9, asr #31
    mla r2, r8, r0, r2
    mov r0, #0
    adc r0, r2, r0
    mov lr, r7, asr #31
    orrs r1, r1, r0, lsl #20
    beq ov000_021dae04_L30c
    ldr r3, [r5, #0x10]
    ldr r0, [sp, #0x18]
    ldr r2, [r5, #0x14]
    sub r12, r3, r0
    ldr r0, [sp, #0x14]
    ldr r10, [r5, #0xc]
    sub r2, r2, r0
    mov r0, r2, asr #31
    str r0, [sp, #0x48]
    mov r0, r12, asr #31
    ldr r3, [sp, #0x5c]
    str r0, [sp, #0x4c]
    sub r0, r10, r3
    umull r10, r3, r7, r2
    str r10, [sp, #0x44]
    ldr r10, [sp, #0x48]
    mov r11, r0, asr #31
    mla r3, r7, r10, r3
    ldr r10, [sp, #0x3c]
    mla r3, r14, r2, r3
    umull r7, r2, r10, r0
    mla r2, r10, r11, r2
    ldr r10, [sp, #0x40]
    mla r2, r10, r0, r2
    umull r11, r10, r9, r12
    ldr r0, [sp, #0x4c]
    adds r7, r7, r11
    mla r10, r9, r0, r10
    mla r10, r8, r12, r10
    ldr r0, [sp, #0x44]
    adc r2, r2, r10
    adds r7, r0, r7
    mov r0, #2048
    adc r2, r3, r2
    adds r3, r7, r0
    mov r0, #0
    adc r2, r2, r0
    mov r0, r3, lsr #12
    orr r0, r0, r2, lsl #20
    bl native_fn_0200235c
    ldr r1, [sp, #0x54]
    mov r2, r0, asr #31
    umull r3, r1, r0, r1
    mla r1, r0, r6, r1
    ldr r0, [sp, #0x54]
    mla r1, r2, r0, r1
    mov r0, #2048
    adds r2, r3, r0
    mov r0, #0
    adc r1, r1, r0
    mov r0, r2, lsr #12
    orr r0, r0, r1, lsl #20
    ldr r1, [sp, #0x50]
    mov r2, r0, asr #31
    umull r7, r3, r0, r1
    adds r1, r7, #2048
    mov r7, r1, lsr #12
    mla r3, r0, r6, r3
    ldr r1, [sp, #0x50]
    mla r3, r2, r1, r3
    adc r1, r3, #0
    orrs r7, r7, r1, lsl #20
    bmi ov000_021dae04_L30c
    ldr r1, [sp, #0x18]
    ldr r7, [sp, #0x5c]
    add r1, r1, r0
    ldr r0, [sp, #0x4]
    ldr r2, [r0, #0x4]
    ldr r8, [r0]
    sub r0, r2, r1
    smull r2, r1, r0, r0
    ldr r0, [sp, #0x4]
    ldr r3, [r0, #0x8]
    sub r0, r8, r7
    smlal r2, r1, r0, r0
    ldr r0, [sp, #0x14]
    sub r0, r3, r0
    smlal r2, r1, r0, r0
    mov r3, r2, lsr #12
    ldr r0, [sp, #0x20]
    orr r3, r3, r1, lsl #20
    subs r0, r3, r0
    ldr r0, [sp, #0x24]
    mov r2, r1, asr #12
    sbcs r0, r2, r0
    bge ov000_021dae04_L30c
    ldr r0, [sp, #0x10]
    str r3, [sp, #0x20]
    str r0, [sp]
    str r2, [sp, #0x24]
    ldr r0, [sp, #0x8]
    ldr r1, [sp, #0x2c]
    mov r2, r4
    mov r3, r5
    bl native_fn_021da520
    mov r0, #1
    str r0, [sp, #0x28]
ov000_021dae04_L30c:
    ldr r0, [sp, #0x30]
    add r4, r4, #1
    cmp r4, r0
    add r5, r5, #68
    blt ov000_021dae04_L12c
ov000_021dae04_L320:
    ldr r0, [sp, #0x38]
    add r1, r0, #1
    ldr r0, [sp, #0x34]
    str r1, [sp, #0x38]
    cmp r1, r0
    ldr r0, [sp, #0x1c]
    add r0, r0, #1
    str r0, [sp, #0x1c]
    blt ov000_021dae04_Ld8
ov000_021dae04_L344:
    ldr r0, [sp, #0x28]
    add sp, sp, #104
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
