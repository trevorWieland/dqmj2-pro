/* ov001 row 0x021ec03c: 1508 bytes.
 *
 * What it does: 373 instructions; 44 call(s) to 0x0207afec, 0x021db438, 0x021db8d0, +41 more; loops (back edge at +0x14); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: block fill (373 instructions, 44 calls, 21 branches, 18 back edges, 4 literal slots).
 *
 *   pool +0x5d4 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x5d8 -> constant 0x02238e50 (image word 0x02238e50)
 *   pool +0x5dc -> constant 0x02238de0 (image word 0x02238de0)
 *   pool +0x5e0 -> constant 0x00000438 (image word 0x00000438)
 *   branch +0x70 -> +0x524
 *   branch +0xac -> +0xe4
 *   branch +0xe0 -> +0x524
 *   branch +0xf8 -> +0x130
 *   branch +0x12c -> +0x524
 *   branch +0x194 -> +0x200
 *   branch +0x1fc -> +0x298
 *   branch +0x21c -> +0x298
 *   branch +0x230 -> +0x298
 *   back edge +0x294 -> +0x238
 *   branch +0x2a4 -> +0x2c0
 *   branch +0x2c8 -> +0x2d4
 *   branch +0x2d0 -> +0x3e4
 *   branch +0x2e0 -> +0x2f0
 *   branch +0x2f4 -> +0x35c
 *   branch +0x358 -> +0x3c0
 *   branch +0x35c -> +0x398
 *   branch +0x394 -> +0x3c0
 *   branch +0x3ec -> +0x478
 *   branch +0x3fc -> +0x478
 *   branch +0x414 -> +0x438
 *   back edge +0x434 -> +0x420
 *   branch +0x43c -> +0x464
 *   branch +0x490 -> +0x4c4
 *   branch +0x4d8 -> +0x524
 *   branch +0x4e4 -> +0x504
 *   back edge +0x538 -> +0x5c
 *   branch +0x558 -> +0x568
 *   branch +0x570 -> +0x580
 *   branch +0x588 -> +0x598
 *   branch +0x5a0 -> +0x5b0
 *   test +0x24 cmp r1, #0
 *   test +0x6c cmp r0, #0
 *   test +0xa8 cmp r0, #0
 *   test +0xf4 cmp r0, #0
 *   test +0x190 cmp r1, #0
 *   test +0x1b4 cmp r0, r11
 *   test +0x1e8 cmp r1, #0
 *   test +0x214 cmp r0, #6
 *   test +0x22c cmp r0, #0
 *   test +0x244 cmp r0, r11
 *   test +0x290 cmp r7, r0
 *   test +0x2a0 cmp r0, #0
 *   test +0x2c4 cmp r0, #0
 *   test +0x2cc cmp r9, #0
 *   test +0x2dc cmp r0, #0
 *   test +0x2f0 cmp r9, #0
 *   test +0x3e8 cmp r0, #0
 *   test +0x3f4 cmp r0, #249
 *   test +0x3f8 cmpeq r9, #0
 *   test +0x410 cmp r9, #0
 *   test +0x428 cmp r2, r6
 *   test +0x430 cmp r7, r9
 *   test +0x438 cmp r8, #0
 *   test +0x47c cmp r0, #0
 *   test +0x484 cmpeq r0, #0
 *   test +0x48c cmpeq r0, #0
 *   test +0x4cc cmp r0, #0
 *   test +0x4d4 cmpne r0, #0
 *   test +0x4e0 cmp r0, #0
 *   test +0x534 cmp r0, #3
 *   test +0x554 cmp r0, #0
 *   test +0x56c cmp r0, #0
 *   test +0x584 cmp r0, #0
 *   test +0x59c cmp r0, #0
 *   test +0x5b4 cmp r0, #0
 *   1 block transfer(s), 46 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ec03c; the literal pool and
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
extern void native_fn_021e1410(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021e1468(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021e9b84(void);
extern void native_fn_021f0818(void);
extern void native_fn_021f0534(void);
extern void native_fn_021f0d10(void);
extern void native_fn_021dc59c(void);
extern void native_fn_021eb024(void);
extern void native_fn_021db718(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_0205d790(void);
extern void native_fn_021e9cd8(void);
extern void native_fn_021d78a4(void);
extern void native_fn_021f949c(void);
extern void native_fn_021f94d8(void);


asm u32 native_ov001_021ec03c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #84
    mov r10, r1
    str r0, [sp, #0x1c]
    mov r0, r10
    bl native_fn_0207afec
    ldr r1, [sp, #0x1c]
    str r0, [sp, #0x24]
    ldrb r1, [r1, #0x31e]
    cmp r1, #0
    moveq r0, #1
    movne r0, #0
    mov r1, #0
    bl native_fn_021db438
    mov r1, #0
    mov r5, r0
    mov r0, r1
    str r1, [sp, #0x38]
    str r0, [sp, #0x34]
    str r0, [sp, #0x30]
    str r0, [sp, #0x2c]
    str r0, [sp, #0x28]
    str r0, [sp, #0x3c]
ov001_021ec03c_L5c:
    mov r1, #0
    mov r0, r5
    str r1, [sp, #0x20]
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021ec03c_L524
    ldr r2, =0x02238d7c
    mov r0, r5
    ldrh r1, [r2, #54]
    ldrb r2, [r2, #0x19]
    bl native_fn_021f2304
    mov r11, r0
    ldrb r0, [r5, #0x31e]
    mov r1, r11
    bl native_fn_021db438
    mov r6, r0
    ldr r0, [sp, #0x1c]
    mov r1, r10
    bl native_fn_021e1410
    cmp r0, #0
    beq ov001_021ec03c_Le4
    mov r1, #0
    mov r0, r5
    mov r2, r10
    str r1, [sp]
    mov r3, #1
    bl native_fn_021ee78c
    ldr r0, [sp, #0x34]
    ldrb r1, [r5, #0x357]
    add r0, r0, #1
    str r0, [sp, #0x34]
    add r0, r1, #1
    strb r0, [r5, #0x357]
    b ov001_021ec03c_L524
ov001_021ec03c_Le4:
    ldr r0, [sp, #0x1c]
    mov r1, r6
    mov r2, r10
    bl native_fn_021e1468
    cmp r0, #0
    beq ov001_021ec03c_L130
    mov r1, #0
    mov r0, r5
    mov r2, r10
    str r1, [sp]
    mov r3, #1
    bl native_fn_021ee78c
    ldr r0, [sp, #0x34]
    ldrb r1, [r5, #0x357]
    add r0, r0, #1
    str r0, [sp, #0x34]
    add r0, r1, #1
    strb r0, [r5, #0x357]
    b ov001_021ec03c_L524
ov001_021ec03c_L130:
    mov r0, #0
    str r0, [sp]
    add r1, sp, #64
    str r1, [sp, #0x4]
    add r0, sp, #76
    str r0, [sp, #0x8]
    add r0, r6, #844
    str r0, [sp, #0xc]
    add r1, sp, #72
    str r1, [sp, #0x10]
    add r0, sp, #80
    str r0, [sp, #0x14]
    add r1, sp, #68
    str r1, [sp, #0x18]
    ldr r3, =0x02238d7c
    ldr r1, [sp, #0x1c]
    ldrb r7, [r3, #0x19]
    ldrb r3, [r3, #0x14]
    mov r0, r10
    mov r2, r6
    orr r3, r7, r3
    bl native_fn_021e1a60
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x19]
    cmp r1, #0
    bne ov001_021ec03c_L200
    ldrh r1, [r0, #54]
    ldr r0, [sp, #0x1c]
    bl native_fn_021e9b84
    mov r4, r0
    ldrb r0, [r5, #0x31f]
    mov r7, #0
    ldr r1, =0x02238d7c
    cmp r0, r11
    str r7, [sp]
    ldrb r3, [r1, #0x14]
    movne r8, #1
    moveq r8, #0
    stmib sp, {r3, r7, r8}
    ldr r0, [sp, #0x1c]
    mov r1, r6
    mov r2, r10
    mov r3, r4
    bl native_fn_021f0818
    ldr r1, =0x02238d7c
    ldrb r1, [r1, #0x2]
    cmp r1, #0
    movne r0, r0, lsl #1
    mov r1, r10
    bl native_fn_021f0534
    mov r9, r0
    b ov001_021ec03c_L298
ov001_021ec03c_L200:
    ldr r0, [sp, #0x1c]
    mov r1, r6
    mov r2, r10
    mov r3, #0
    bl native_fn_021f0d10
    cmp r0, #6
    mov r9, #0
    beq ov001_021ec03c_L298
    ldr r0, =0x02238d7c
    mov r7, r9
    ldrsb r0, [r0, #11]
    cmp r0, #0
    ble ov001_021ec03c_L298
    ldr r8, =0x02238e50
ov001_021ec03c_L238:
    ldrb r0, [r5, #0x31f]
    ldrb r3, [r8], #1
    mov r1, r6
    cmp r0, r11
    str r3, [sp]
    ldr r3, =0x02238d7c
    movne r0, #1
    ldrb r12, [r3, #0x14]
    moveq r0, #0
    mov r2, r10
    str r12, [sp, #0x4]
    mov r12, #1
    str r12, [sp, #0x8]
    str r0, [sp, #0xc]
    ldr r0, =0x02238de0
    mov r3, r4
    ldr r0, [r0, r7, lsl #2]
    bl native_fn_021f0818
    add r9, r9, r0
    ldr r0, =0x02238d7c
    add r7, r7, #1
    ldrsb r0, [r0, #11]
    cmp r7, r0
    blt ov001_021ec03c_L238
ov001_021ec03c_L298:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x19]
    cmp r0, #0
    bne ov001_021ec03c_L2c0
    mov r0, r6
    mov r1, r10
    bl native_fn_021dc59c
    ldr r1, [sp, #0x48]
    orr r0, r1, r0
    str r0, [sp, #0x48]
ov001_021ec03c_L2c0:
    ldr r0, [sp, #0x50]
    cmp r0, #0
    bne ov001_021ec03c_L2d4
    cmp r9, #0
    bne ov001_021ec03c_L3e4
ov001_021ec03c_L2d4:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x15]
    cmp r0, #0
    bne ov001_021ec03c_L2f0
    ldr r0, [sp, #0x24]
    mov r1, r6
    bl native_fn_021eb024
ov001_021ec03c_L2f0:
    cmp r9, #0
    ble ov001_021ec03c_L35c
    mov r0, r6
    rsb r1, r9, #0
    bl native_fn_021db718
    mov r0, r6
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    ldr r3, [sp, #0x24]
    str r4, [sp]
    ldrb r3, [r3, #0x1e]
    mov r0, r6
    mov r1, r9
    mov r2, r10
    bl native_fn_021ee78c
    ldr r0, [sp, #0x38]
    ldrb r1, [r6, #0x31f]
    add r0, r0, #1
    str r0, [sp, #0x38]
    ldr r0, [sp, #0x1c]
    add r0, r0, r1, lsl #1
    add r0, r0, #768
    ldrsh r1, [r0, #78]
    add r1, r1, r9
    strh r1, [r0, #78]
    b ov001_021ec03c_L3c0
ov001_021ec03c_L35c:
    bge ov001_021ec03c_L398
    mov r0, r6
    rsb r1, r9, #0
    mov r2, r10
    bl native_fn_021f0f0c
    mov r9, r0
    ldr r2, [sp, #0x24]
    mov r0, r6
    ldrb r2, [r2, #0x1e]
    mov r1, r9
    bl native_fn_021ee7d4
    ldr r0, [sp, #0x2c]
    add r0, r0, #1
    str r0, [sp, #0x2c]
    b ov001_021ec03c_L3c0
ov001_021ec03c_L398:
    ldr r0, [sp, #0x24]
    str r4, [sp]
    ldrb r3, [r0, #0x1e]
    mov r0, r6
    mov r1, r9
    mov r2, r10
    bl native_fn_021ee78c
    ldr r0, [sp, #0x28]
    add r0, r0, #1
    str r0, [sp, #0x28]
ov001_021ec03c_L3c0:
    mov r1, #1
    str r1, [sp, #0x20]
    ldrb r0, [r6, #0x31e]
    ldrb r1, [r6, #0x31f]
    mov r2, r9
    bl native_fn_022024d4
    ldrb r0, [r5, #0x357]
    add r0, r0, #1
    strb r0, [r5, #0x357]
ov001_021ec03c_L3e4:
    ldr r0, [sp, #0x4c]
    cmp r0, #0
    beq ov001_021ec03c_L478
    ldrh r0, [sp, #64]
    cmp r0, #249
    cmpeq r9, #0
    beq ov001_021ec03c_L478
    mov r8, #0
    mov r7, r8
    ldr r1, =0x02238d7c
    ldrsb r9, [r1, #11]
    cmp r9, #0
    ble ov001_021ec03c_L438
    ldr r3, =0x02238de0
    mov r1, #1
ov001_021ec03c_L420:
    ldr r2, [r3, r7, lsl #2]
    add r7, r7, #1
    cmp r2, r6
    moveq r8, r1
    cmp r7, r9
    blt ov001_021ec03c_L420
ov001_021ec03c_L438:
    cmp r8, #0
    bne ov001_021ec03c_L464
    ldr r1, =0x02238d7c
    ldr r7, [sp, #0x44]
    ldrsb r8, [r1, #11]
    ldr r3, =0x02238e50
    ldr r2, =0x02238de0
    strb r7, [r3, r8]
    str r6, [r2, r8, lsl #2]
    add r2, r8, #1
    strb r2, [r1, #0xb]
ov001_021ec03c_L464:
    add r1, r5, #768
    strh r0, [r1, #74]
    ldr r0, [sp, #0x30]
    add r0, r0, #1
    str r0, [sp, #0x30]
ov001_021ec03c_L478:
    ldr r0, [sp, #0x50]
    cmp r0, #0
    ldreq r0, [sp, #0x20]
    cmpeq r0, #0
    ldreq r0, [sp, #0x4c]
    cmpeq r0, #0
    bne ov001_021ec03c_L4c4
    mov r1, #0
    ldr r0, [sp, #0x24]
    str r1, [sp]
    ldrb r3, [r0, #0x1e]
    mov r0, r6
    mov r2, r10
    bl native_fn_021ee78c
    ldr r0, [sp, #0x28]
    add r0, r0, #1
    str r0, [sp, #0x28]
    mov r0, #1
    str r0, [sp, #0x20]
ov001_021ec03c_L4c4:
    add r0, r6, #768
    ldrh r0, [r0, #76]
    cmp r0, #0
    ldrne r0, [sp, #0x48]
    cmpne r0, #0
    beq ov001_021ec03c_L524
    ldr r0, [sp, #0x20]
    cmp r0, #0
    bne ov001_021ec03c_L504
    ldr r0, [sp, #0x24]
    str r4, [sp]
    ldrb r3, [r0, #0x1e]
    mov r0, r6
    mov r1, #0
    mov r2, r10
    bl native_fn_021ee78c
ov001_021ec03c_L504:
    add r0, r6, #768
    ldrh r0, [r0, #76]
    bl native_fn_0205d790
    mov r2, r0
    add r0, r6, #768
    ldrh r0, [r0, #76]
    mov r1, r6
    bl native_fn_021e9cd8
ov001_021ec03c_L524:
    ldr r0, [sp, #0x3c]
    add r5, r5, #1088
    add r0, r0, #1
    str r0, [sp, #0x3c]
    cmp r0, #3
    blt ov001_021ec03c_L5c
    ldr r1, =0x00000438
    mov r0, #0
    mov r2, #100
    mov r3, #3072
    bl native_fn_021d78a4
    ldr r0, [sp, #0x38]
    cmp r0, #0
    ble ov001_021ec03c_L568
    mov r0, #239
    mov r1, #0
    bl native_fn_021f949c
ov001_021ec03c_L568:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    ble ov001_021ec03c_L580
    mov r0, #228
    mov r1, #0
    bl native_fn_021f949c
ov001_021ec03c_L580:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    ble ov001_021ec03c_L598
    mov r0, #243
    mov r1, #0
    bl native_fn_021f949c
ov001_021ec03c_L598:
    ldr r0, [sp, #0x28]
    cmp r0, #0
    ble ov001_021ec03c_L5b0
    mov r0, #242
    mov r1, #0
    bl native_fn_021f949c
ov001_021ec03c_L5b0:
    ldr r0, [sp, #0x2c]
    cmp r0, #0
    addle sp, sp, #84
    ldmleia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
    mov r0, #19
    mov r1, #0
    bl native_fn_021f94d8
    add sp, sp, #84
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
