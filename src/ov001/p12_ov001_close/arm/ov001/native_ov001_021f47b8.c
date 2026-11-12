/* ov001 row 0x021f47b8: 892 bytes.
 *
 * What it does: 221 instructions; 29 call(s) to 0x0207afec, 0x021db438, 0x021f4adc, +26 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 29 calls (221 instructions, 29 calls, 12 branches, 20 back edges, 2 literal slots).
 *
 *   pool +0x374 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x378 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x34 -> +0x54
 *   branch +0x6c -> +0x324
 *   branch +0x84 -> +0x310
 *   branch +0xb0 -> +0xe0
 *   branch +0xdc -> +0x134
 *   branch +0xf0 -> +0x130
 *   back edge +0x12c -> +0xf8
 *   branch +0x140 -> +0x16c
 *   branch +0x150 -> +0x16c
 *   branch +0x1bc -> +0x2a4
 *   branch +0x1c8 -> +0x218
 *   branch +0x214 -> +0x2d4
 *   branch +0x2a0 -> +0x2d4
 *   branch +0x2ac -> +0x2d4
 *   branch +0x2dc -> +0x310
 *   back edge +0x320 -> +0x78
 *   branch +0x334 -> +0x34c
 *   branch +0x358 -> +0x368
 *   test +0x28 cmp r10, #0
 *   test +0x68 cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xec cmp r0, #0
 *   test +0x128 cmp r6, r0
 *   test +0x13c cmp r0, #0
 *   test +0x14c cmp r0, #0
 *   test +0x1b8 cmp r0, #0
 *   test +0x1c4 tst r0, #32
 *   test +0x1e0 cmp r1, #0
 *   test +0x2a8 cmp r0, #0
 *   test +0x2d8 cmp r0, #0
 *   test +0x318 cmp r5, r0
 *   test +0x328 cmp r0, #0
 *   test +0x354 cmp r0, #0
 *   0 block transfer(s), 32 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f47b8; the literal pool and
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

extern void native_fn_0207afec(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f0950(void);
extern void native_fn_02044424(void);
extern void native_fn_021f0534(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021dc9d4(void);
extern void native_fn_021f2464(void);
extern void native_fn_0220f600(void);
extern void native_fn_021ee7b0(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_021f47b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    mov r9, r2
    str r0, [sp, #0x1c]
    mov r10, r1
    mov r1, #0
    mov r0, r9
    str r1, [sp, #0x28]
    bl native_fn_0207afec
    str r0, [sp, #0x20]
    cmp r10, #0
    movne r0, #1
    strne r0, [sp, #0x34]
    bne ov001_021f47b8_L54
    ldr r0, [sp, #0x1c]
    mov r1, #0
    ldrb r0, [r0, #0x31e]
    bl native_fn_021db438
    mov r10, r0
    mov r0, #3
    str r0, [sp, #0x34]
ov001_021f47b8_L54:
    mov r0, #0
    str r0, [sp, #0x30]
    str r0, [sp, #0x2c]
    mov r5, r0
    ldr r0, [sp, #0x34]
    cmp r0, #0
    ble ov001_021f47b8_L324
    mov r0, r9, lsl #16
    mov r8, r0, asr #16
ov001_021f47b8_L78:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f47b8_L310
    mov r1, #0
    mov r0, r10
    mov r2, r1
    bl native_fn_021d9494
    ldr r0, [sp, #0x20]
    ldr r4, =0x0223989c
    ldrb r0, [r0, #0x1e]
    str r0, [sp, #0x24]
    ldrb r0, [r4, #0x10]
    cmp r0, #0
    bne ov001_021f47b8_Le0
    ldrb r2, [r4, #0x29]
    ldr r0, [sp, #0x1c]
    mov r1, r10
    str r2, [sp]
    ldr r2, [r4, #0x5c]
    mov r3, r8
    mov r2, r2, lsl #16
    mov r2, r2, asr #16
    bl native_fn_021f0950
    str r0, [sp, #0x44]
    b ov001_021f47b8_L134
ov001_021f47b8_Le0:
    ldrsb r0, [r4, #43]
    mov r7, #0
    mov r6, r7
    cmp r0, #0
    ble ov001_021f47b8_L130
    ldr r11, =0x022399b8
ov001_021f47b8_Lf8:
    ldrb r0, [r4, #0x29]
    mov r1, r10
    mov r3, r8
    str r0, [sp]
    ldr r0, [r11, r5, lsl #2]
    ldr r2, [r4, #0x5c]
    mov r2, r2, lsl #16
    mov r2, r2, asr #16
    bl native_fn_021f0950
    add r7, r7, r0
    add r6, r6, #1
    ldrsb r0, [r4, #43]
    cmp r6, r0
    blt ov001_021f47b8_Lf8
ov001_021f47b8_L130:
    str r7, [sp, #0x44]
ov001_021f47b8_L134:
    mov r0, #2048
    bl native_fn_02044424
    cmp r0, #0
    beq ov001_021f47b8_L16c
    ldr r0, [sp, #0x1c]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    bne ov001_021f47b8_L16c
    ldr r0, [sp, #0x44]
    mov r1, r9
    mov r0, r0, lsl #1
    str r0, [sp, #0x44]
    bl native_fn_021f0534
    str r0, [sp, #0x44]
ov001_021f47b8_L16c:
    add r0, sp, #68
    str r0, [sp]
    add r1, sp, #56
    str r1, [sp, #0x4]
    add r0, sp, #64
    str r0, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    add r0, sp, #60
    str r1, [sp, #0x10]
    str r0, [sp, #0x14]
    str r1, [sp, #0x18]
    ldr r0, =0x0223989c
    ldr r1, [sp, #0x1c]
    ldrb r3, [r0, #0x10]
    mov r0, r9
    mov r2, r10
    bl native_fn_021e1a60
    ldr r0, [sp, #0x3c]
    cmp r0, #0
    beq ov001_021f47b8_L2a4
    bl native_fn_021e29e8
    tst r0, #32
    bne ov001_021f47b8_L218
    ldr r1, [sp, #0x44]
    mov r0, r10
    mov r2, r9
    bl native_fn_021f0f0c
    ldr r1, [sp, #0x40]
    cmp r1, #0
    streq r0, [sp, #0x44]
    ldr r1, [sp, #0x44]
    ldr r2, [sp, #0x24]
    mov r0, r10
    bl native_fn_021ee7d4
    ldr r1, [sp, #0x44]
    ldrb r0, [r10, #0x31e]
    rsb r2, r1, #0
    ldrb r1, [r10, #0x31f]
    bl native_fn_022024d4
    mov r0, #1
    str r0, [sp, #0x28]
    b ov001_021f47b8_L2d4
ov001_021f47b8_L218:
    ldr r1, [sp, #0x44]
    mov r0, r10
    mov r2, r9
    bl native_fn_021f0eb4
    mov r4, r0
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r2, r4
    bl native_fn_022024d4
    mov r0, #0
    str r0, [sp]
    ldr r3, [sp, #0x20]
    mov r1, r4
    ldrb r3, [r3, #0x1e]
    mov r0, r10
    mov r2, r9
    bl native_fn_021ee78c
    mov r0, r10
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    ldr r0, =0x0223989c
    ldr r0, [r0, #0x84]
    bl native_fn_021dc9d4
    mov r4, r0
    mov r0, r9
    bl native_fn_021f2464
    str r0, [sp]
    ldr r0, =0x0223989c
    mov r3, r4
    ldr r0, [r0, #0x84]
    mov r1, r10
    mov r2, r9
    bl native_fn_0220f600
    b ov001_021f47b8_L2d4
ov001_021f47b8_L2a4:
    ldr r0, [sp, #0x40]
    cmp r0, #0
    bne ov001_021f47b8_L2d4
    mov r1, #0
    mov r0, r10
    sub r2, r1, #1
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee7b0
    ldr r0, [sp, #0x2c]
    add r0, r0, #1
    str r0, [sp, #0x2c]
ov001_021f47b8_L2d4:
    ldr r0, [sp, #0x40]
    cmp r0, #0
    beq ov001_021f47b8_L310
    ldr r1, =0x0223989c
    ldr r3, =0x022399b8
    ldrsb r4, [r1, #43]
    ldrh r2, [sp, #56]
    add r0, r10, #768
    str r10, [r3, r4, lsl #2]
    add r3, r4, #1
    strb r3, [r1, #0x2b]
    strh r2, [r0, #74]
    ldr r0, [sp, #0x30]
    add r0, r0, #1
    str r0, [sp, #0x30]
ov001_021f47b8_L310:
    ldr r0, [sp, #0x34]
    add r5, r5, #1
    cmp r5, r0
    add r10, r10, #1088
    blt ov001_021f47b8_L78
ov001_021f47b8_L324:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    ldrle r0, =0x0223989c
    movle r1, #0
    ble ov001_021f47b8_L34c
    mov r0, #243
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x0223989c
    mov r1, #1
ov001_021f47b8_L34c:
    strb r1, [r0, #0x10]
    ldr r0, [sp, #0x2c]
    cmp r0, #0
    ble ov001_021f47b8_L368
    mov r0, #242
    mov r1, #1
    bl native_fn_021f949c
ov001_021f47b8_L368:
    ldr r0, [sp, #0x28]
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
