/* ov001 row 0x021f6088: 932 bytes.
 *
 * What it does: 230 instructions; 23 call(s) to 0x0207afec, 0x021db438, 0x021f6338, +20 more; loops (back edge at +0x4c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 23 calls (230 instructions, 23 calls, 17 branches, 16 back edges, 3 literal slots).
 *
 *   pool +0x398 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x39c -> constant 0x0223995c (image word 0x0223995c)
 *   pool +0x3a0 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x54 -> +0x8c
 *   branch +0x68 -> +0x78
 *   branch +0x88 -> +0x90
 *   branch +0xa0 -> +0x2b0
 *   branch +0xb4 -> +0x2a0
 *   branch +0x148 -> +0x1fc
 *   branch +0x14c -> +0x1a8
 *   branch +0x1b0 -> +0x1e8
 *   branch +0x1f8 -> +0x294
 *   branch +0x204 -> +0x240
 *   branch +0x23c -> +0x260
 *   branch +0x24c -> +0x260
 *   branch +0x26c -> +0x294
 *   back edge +0x2ac -> +0xa8
 *   branch +0x2c0 -> +0x330
 *   branch +0x2e0 -> +0x320
 *   branch +0x2f0 -> +0x320
 *   branch +0x2fc -> +0x320
 *   back edge +0x32c -> +0x2d4
 *   branch +0x334 -> +0x344
 *   branch +0x34c -> +0x35c
 *   test +0x50 cmp r9, #0
 *   test +0x6c cmp r0, #0
 *   test +0x90 cmp r6, #0
 *   test +0x9c cmpgt r6, #0
 *   test +0xb0 cmp r0, #0
 *   test +0x13c cmp r1, #0
 *   test +0x144 cmpne r0, #0
 *   test +0x1ac cmp r0, #0
 *   test +0x200 cmp r0, #0
 *   test +0x244 cmp r0, #0
 *   test +0x248 cmpne r1, #0
 *   test +0x268 cmp r0, #0
 *   test +0x2a4 cmp r5, r6
 *   test +0x2b0 cmp r6, #0
 *   test +0x2bc cmpgt r6, #0
 *   test +0x2dc cmp r0, #0
 *   test +0x2ec cmp r0, #0
 *   test +0x2f8 cmp r0, #0
 *   test +0x324 cmp r8, r6
 *   test +0x330 cmp r11, #0
 *   test +0x348 cmp r0, #0
 *   test +0x360 cmp r0, #0
 *   0 block transfer(s), 36 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f6088; the literal pool and
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
extern void native_fn_021f2304(void);
extern void native_fn_021f4fa4(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021d9494(void);
extern void native_fn_021db788(void);
extern void native_fn_022024d4(void);
extern void native_fn_021f2464(void);
extern void native_fn_0220f600(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021ee7b0(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_021f6088 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #88
    mov r8, r2
    mov r2, #0
    str r2, [sp, #0x24]
    ldr r11, [sp, #0x24]
    mov r10, r0
    mov r9, r1
    mov r1, r11
    add r3, sp, #76
    add r2, sp, #64
    mov r0, r8
    str r1, [sp, #0x20]
    str r1, [r3]
    str r1, [r3, #0x4]
    str r1, [r3, #0x8]
    str r1, [r2]
    str r1, [r2, #0x4]
    str r1, [r2, #0x8]
    bl native_fn_0207afec
    cmp r9, #0
    bne ov001_021f6088_L8c
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    ldrb r0, [r10, #0x31e]
    beq ov001_021f6088_L78
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
ov001_021f6088_L78:
    mov r1, #0
    bl native_fn_021db438
    mov r9, r0
    mov r6, #3
    b ov001_021f6088_L90
ov001_021f6088_L8c:
    mov r6, #1
ov001_021f6088_L90:
    cmp r6, #0
    str r9, [sp, #0x1c]
    mov r5, #0
    cmpgt r6, #0
    ble ov001_021f6088_L2b0
    ldr r4, =0x0223989c
ov001_021f6088_La8:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f6088_L2a0
    ldrb r2, [r4, #0x10]
    mov r0, r9
    mov r1, r8
    bl native_fn_021f2304
    mov r1, r0
    ldrb r0, [r9, #0x31e]
    bl native_fn_021db438
    mov r7, r0
    mov r0, r10
    mov r1, r7
    mov r2, r8
    bl native_fn_021f4fa4
    str r0, [sp, #0x3c]
    add r0, sp, #60
    str r0, [sp]
    add r0, sp, #40
    str r0, [sp, #0x4]
    add r0, sp, #56
    str r0, [sp, #0x8]
    add r0, r7, #844
    str r0, [sp, #0xc]
    add r0, sp, #48
    str r0, [sp, #0x10]
    add r0, sp, #52
    str r0, [sp, #0x14]
    add r0, sp, #44
    str r0, [sp, #0x18]
    ldrb r3, [r4, #0x10]
    mov r0, r8
    mov r1, r10
    mov r2, r7
    bl native_fn_021e1a60
    ldr r1, [sp, #0x3c]
    cmp r1, #0
    ldrne r0, [sp, #0x34]
    cmpne r0, #0
    beq ov001_021f6088_L1fc
    beq ov001_021f6088_L1a8
    add r0, r7, #256
    ldrsh r11, [r0, #240]
    mov r0, r7
    mov r1, #4
    mov r2, #0
    bl native_fn_021d9494
    mov r0, r7
    mov r1, #0
    bl native_fn_021db788
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    mov r2, r11
    bl native_fn_022024d4
    mov r0, r8
    bl native_fn_021f2464
    str r0, [sp]
    ldr r0, [r4, #0x84]
    mov r1, r7
    mov r2, r8
    mov r3, #0
    bl native_fn_0220f600
    mov r11, #1
ov001_021f6088_L1a8:
    ldr r0, [sp, #0x38]
    cmp r0, #0
    beq ov001_021f6088_L1e8
    ldrsb r0, [r4, #43]
    ldr r3, [sp, #0x2c]
    ldr r1, =0x0223995c
    add r2, r7, #768
    strb r3, [r1, r0]
    add r1, r0, #1
    strb r1, [r4, #0x2b]
    ldr r1, =0x022399b8
    str r7, [r1, r0, lsl #2]
    ldrh r1, [sp, #40]
    mov r0, #1
    str r0, [sp, #0x24]
    strh r1, [r2, #74]
ov001_021f6088_L1e8:
    ldrb r2, [r7, #0x31f]
    mov r1, #1
    add r0, sp, #76
    str r1, [r0, r2, lsl #2]
    b ov001_021f6088_L294
ov001_021f6088_L1fc:
    ldr r0, [sp, #0x38]
    cmp r0, #0
    beq ov001_021f6088_L240
    ldrsb r0, [r4, #43]
    ldr r3, [sp, #0x2c]
    ldr r1, =0x0223995c
    add r2, r7, #768
    strb r3, [r1, r0]
    add r1, r0, #1
    strb r1, [r4, #0x2b]
    ldr r1, =0x022399b8
    str r7, [r1, r0, lsl #2]
    ldrh r1, [sp, #40]
    mov r0, #1
    str r0, [sp, #0x24]
    strh r1, [r2, #74]
    b ov001_021f6088_L260
ov001_021f6088_L240:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    cmpne r1, #0
    bne ov001_021f6088_L260
    ldrb r2, [r7, #0x31f]
    mov r1, #1
    add r0, sp, #64
    str r1, [r0, r2, lsl #2]
ov001_021f6088_L260:
    add r0, r7, #768
    ldrh r0, [r0, #76]
    cmp r0, #0
    beq ov001_021f6088_L294
    bl native_fn_0205d790
    mov r2, r0
    add r0, r7, #768
    ldrh r0, [r0, #76]
    mov r1, r7
    bl native_fn_021eec7c
    add r1, r7, #768
    mov r0, #0
    strh r0, [r1, #76]
ov001_021f6088_L294:
    ldrb r0, [r7, #0x357]
    add r0, r0, #1
    strb r0, [r7, #0x357]
ov001_021f6088_L2a0:
    add r5, r5, #1
    cmp r5, r6
    add r9, r9, #1088
    blt ov001_021f6088_La8
ov001_021f6088_L2b0:
    cmp r6, #0
    ldr r9, [sp, #0x1c]
    mov r8, #0
    cmpgt r6, #0
    ble ov001_021f6088_L330
    mov r10, r8
    mvn r4, #0
    add r5, sp, #64
    add r7, sp, #76
ov001_021f6088_L2d4:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f6088_L320
    ldrb r1, [r9, #0x31f]
    ldr r0, [r7, r1, lsl #2]
    cmp r0, #0
    bne ov001_021f6088_L320
    ldr r0, [r5, r1, lsl #2]
    cmp r0, #0
    beq ov001_021f6088_L320
    mov r3, #1
    mov r12, r3
    mov r0, r9
    mov r1, r10
    mov r2, r4
    str r10, [sp]
    str r12, [sp, #0x20]
    bl native_fn_021ee7b0
ov001_021f6088_L320:
    add r8, r8, #1
    cmp r8, r6
    add r9, r9, #1088
    blt ov001_021f6088_L2d4
ov001_021f6088_L330:
    cmp r11, #0
    beq ov001_021f6088_L344
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
ov001_021f6088_L344:
    ldr r0, [sp, #0x20]
    cmp r0, #0
    beq ov001_021f6088_L35c
    mov r0, #242
    mov r1, #1
    bl native_fn_021f949c
ov001_021f6088_L35c:
    ldr r0, [sp, #0x24]
    cmp r0, #0
    ldreq r0, =0x0223989c
    moveq r1, #0
    streqb r1, [r0, #0x10]
    addeq sp, sp, #88
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #243
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, =0x0223989c
    mov r1, #1
    strb r1, [r0, #0x10]
    add sp, sp, #88
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
