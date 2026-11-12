/* ov001 row 0x021f39cc: 2116 bytes.
 *
 * What it does: 525 instructions; 58 call(s) to 0x0207afec, 0x021db438, 0x021f3a58, +55 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 58 calls (525 instructions, 58 calls, 38 branches, 41 back edges, 4 literal slots).
 *
 *   pool +0x834 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x838 -> constant 0x0223995c (image word 0x0223995c)
 *   pool +0x83c -> constant 0x02239968 (image word 0x02239968)
 *   pool +0x840 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x38 -> +0x64
 *   branch +0x60 -> +0x6c
 *   back edge +0x9c -> +0x8c
 *   branch +0xac -> +0x6f4
 *   branch +0xc4 -> +0x6d8
 *   branch +0xfc -> +0x128
 *   branch +0x124 -> +0x6d8
 *   branch +0x13c -> +0x168
 *   branch +0x164 -> +0x6d8
 *   branch +0x17c -> +0x1cc
 *   branch +0x1c8 -> +0x214
 *   branch +0x220 -> +0x230
 *   branch +0x22c -> +0x348
 *   branch +0x23c -> +0x290
 *   branch +0x28c -> +0x2c4
 *   branch +0x2d0 -> +0x2ec
 *   branch +0x2f4 -> +0x3ec
 *   branch +0x344 -> +0x3ec
 *   branch +0x364 -> +0x3ec
 *   branch +0x378 -> +0x3ec
 *   back edge +0x3e8 -> +0x380
 *   branch +0x3f4 -> +0x5a8
 *   branch +0x40c -> +0x41c
 *   branch +0x420 -> +0x438
 *   branch +0x43c -> +0x504
 *   branch +0x468 -> +0x498
 *   branch +0x470 -> +0x498
 *   branch +0x500 -> +0x544
 *   branch +0x518 -> +0x544
 *   branch +0x55c -> +0x57c
 *   branch +0x578 -> +0x58c
 *   branch +0x5b0 -> +0x668
 *   branch +0x5c0 -> +0x668
 *   branch +0x5d0 -> +0x654
 *   branch +0x650 -> +0x6a8
 *   branch +0x664 -> +0x6a8
 *   branch +0x670 -> +0x6a8
 *   branch +0x6bc -> +0x6d8
 *   back edge +0x6f0 -> +0xb8
 *   branch +0x6fc -> +0x70c
 *   branch +0x714 -> +0x724
 *   branch +0x72c -> +0x73c
 *   branch +0x744 -> +0x79c
 *   branch +0x758 -> +0x778
 *   branch +0x774 -> +0x784
 *   back edge +0x780 -> +0x750
 *   branch +0x788 -> +0x7a8
 *   branch +0x798 -> +0x7a8
 *   branch +0x7b0 -> +0x7c0
 *   branch +0x7cc -> +0x808
 *   branch +0x7e0 -> +0x808
 *   branch +0x818 -> +0x828
 *   test +0x34 cmp r9, #0
 *   test +0x44 cmp r0, #0
 *   test +0x98 cmp r2, #3
 *   test +0xa8 cmp r0, #0
 *   test +0xc0 cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x138 cmp r0, #0
 *   test +0x170 cmp r0, #2
 *   test +0x174 cmpne r0, #3
 *   test +0x21c cmp r1, #0
 *   test +0x228 cmp r0, #0
 *   test +0x238 cmp r1, #2
 *   test +0x254 cmp r1, r0
 *   test +0x2cc cmp r0, #0
 *   test +0x2e4 cmp r0, #0
 *   test +0x2f0 cmp r0, #0
 *   test +0x30c cmp r1, r0
 *   test +0x35c cmp r0, #6
 *   test +0x374 cmp r0, #0
 *   test +0x388 cmp r1, r0
 *   test +0x3e4 cmp r5, r0
 *   test +0x3f0 cmp r0, #0
 *   test +0x408 cmp r0, #0
 *   test +0x41c cmp r7, #0
 *   test +0x428 tst r0, #32
 *   test +0x438 cmp r7, #0
 *   test +0x464 cmp r0, #0
 *   test +0x46c cmp r6, #0
 *   test +0x498 cmp r6, #0
 *   test +0x4b0 cmp r6, #0
 *   test +0x504 cmp r7, #0
 *   test +0x550 cmp r3, #1
 *   test +0x558 cmp r0, #0
 *   test +0x5ac cmp r0, #0
 *   test +0x5b8 cmp r0, #249
 *   test +0x5bc cmpeq r7, #0
 *   test +0x5cc cmp r0, #0
 *   test +0x66c cmp r0, #0
 *   test +0x6ac cmp r0, #0
 *   test +0x6b8 cmpne r0, #0
 *   test +0x6ec cmp r1, r0
 *   test +0x6f8 cmp r0, #0
 *   test +0x710 cmp r0, #0
 *   test +0x728 cmp r0, #0
 *   test +0x740 cmp r0, #0
 *   test +0x754 cmp r0, #0
 *   test +0x77c cmp r2, #3
 *   test +0x7ac cmp r0, #0
 *   test +0x7c8 cmp r0, #0
 *   test +0x7dc cmp r0, #0
 *   test +0x814 cmp r0, #0
 *   0 block transfer(s), 73 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f39cc; the literal pool and
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
extern void native_fn_021f08a0(void);
extern void native_fn_021f0858(void);
extern void native_fn_021e19e4(void);
extern void native_fn_021f0d10(void);
extern void native_fn_021dc59c(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021f0eb4(void);
extern void native_fn_021e13c8(void);
extern void native_fn_021d9494(void);
extern void native_fn_021dc9d4(void);
extern void native_fn_021f2464(void);
extern void native_fn_0220f600(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbd30(void);
extern void native_fn_0207b244(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021f949c(void);
extern void native_fn_021f94d8(void);
extern void native_fn_0207b004(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021dc940(void);


asm u32 native_ov001_021f39cc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #104
    mov r10, r0
    mov r0, #0
    str r0, [sp, #0x2c]
    mov r8, r2
    mov r9, r1
    ldr r1, [sp, #0x2c]
    mov r0, r8
    str r3, [sp, #0x1c]
    strh r1, [sp, #72]
    bl native_fn_0207afec
    str r0, [sp, #0x28]
    cmp r9, #0
    bne ov001_021f39cc_L64
    ldrb r0, [r10, #0x31e]
    mov r1, #0
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    bl native_fn_021db438
    mov r9, r0
    mov r0, #3
    str r0, [sp, #0x44]
    b ov001_021f39cc_L6c
ov001_021f39cc_L64:
    mov r0, #1
    str r0, [sp, #0x44]
ov001_021f39cc_L6c:
    mov r0, #0
    str r0, [sp, #0x40]
    str r0, [sp, #0x3c]
    str r0, [sp, #0x38]
    str r0, [sp, #0x34]
    mov r2, r0
    str r0, [sp, #0x30]
    add r1, sp, #92
ov001_021f39cc_L8c:
    ldr r0, [sp, #0x30]
    str r0, [r1, r2, lsl #2]
    add r2, r2, #1
    cmp r2, #3
    blt ov001_021f39cc_L8c
    str r0, [sp, #0x20]
    ldr r0, [sp, #0x44]
    cmp r0, #0
    ble ov001_021f39cc_L6f4
    mov r0, r8, lsl #16
    mov r11, r0, asr #16
ov001_021f39cc_Lb8:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_021f39cc_L6d8
    mov r0, r9
    mov r1, r8
    ldr r2, =0x0223989c
    ldrb r2, [r2, #0x10]
    bl native_fn_021f2304
    mov r1, r0
    ldrb r0, [r9, #0x31e]
    bl native_fn_021db438
    mov r4, r0
    mov r0, r10
    mov r1, r8
    bl native_fn_021e1410
    cmp r0, #0
    beq ov001_021f39cc_L128
    mov r1, #0
    mov r0, r4
    mov r2, r8
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee78c
    ldr r0, [sp, #0x3c]
    add r0, r0, #1
    str r0, [sp, #0x3c]
    b ov001_021f39cc_L6d8
ov001_021f39cc_L128:
    mov r0, r10
    mov r1, r4
    mov r2, r8
    bl native_fn_021e1468
    cmp r0, #0
    beq ov001_021f39cc_L168
    mov r1, #0
    mov r0, r4
    mov r2, r8
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee78c
    ldr r0, [sp, #0x3c]
    add r0, r0, #1
    str r0, [sp, #0x3c]
    b ov001_021f39cc_L6d8
ov001_021f39cc_L168:
    ldr r1, =0x0223989c
    ldrb r0, [r1, #0x35]
    cmp r0, #2
    cmpne r0, #3
    mov r0, #0
    beq ov001_021f39cc_L1cc
    str r0, [sp]
    add r2, sp, #72
    str r2, [sp, #0x4]
    add r0, sp, #88
    str r0, [sp, #0x8]
    add r0, r4, #844
    str r0, [sp, #0xc]
    add r2, sp, #80
    str r2, [sp, #0x10]
    add r0, sp, #84
    str r0, [sp, #0x14]
    add r2, sp, #76
    str r2, [sp, #0x18]
    ldrb r3, [r1, #0x10]
    mov r0, r8
    mov r1, r10
    mov r2, r4
    bl native_fn_021e1a60
    b ov001_021f39cc_L214
ov001_021f39cc_L1cc:
    str r0, [sp]
    add r1, sp, #72
    str r1, [sp, #0x4]
    add r0, sp, #88
    str r0, [sp, #0x8]
    add r0, r4, #844
    str r0, [sp, #0xc]
    add r1, sp, #80
    str r1, [sp, #0x10]
    add r0, sp, #84
    str r0, [sp, #0x14]
    add r1, sp, #76
    str r1, [sp, #0x18]
    mov r0, r8
    mov r1, r10
    mov r2, r4
    mov r3, #1
    bl native_fn_021e1a60
ov001_021f39cc_L214:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x10]
    cmp r1, #0
    beq ov001_021f39cc_L230
    ldrb r0, [r0, #0x13]
    cmp r0, #0
    beq ov001_021f39cc_L348
ov001_021f39cc_L230:
    ldr r0, =0x0223989c
    ldrb r1, [r0, #0x35]
    cmp r1, #2
    beq ov001_021f39cc_L290
    ldr r2, =0x0223989c
    ldrb r1, [r4, #0x31f]
    ldrb r0, [r9, #0x31f]
    ldrb r5, [r2, #0x29]
    mov r3, #0
    cmp r1, r0
    str r5, [sp]
    movne r6, #1
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    moveq r6, #0
    str r6, [sp, #0xc]
    ldr r2, [r2, #0x5c]
    mov r0, r10
    mov r2, r2, lsl #16
    mov r1, r4
    mov r3, r11
    mov r2, r2, asr #16
    bl native_fn_021f08a0
    b ov001_021f39cc_L2c4
ov001_021f39cc_L290:
    ldrb r3, [r0, #0x29]
    mov r2, #0
    mov r1, #3
    str r3, [sp]
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    ldr r1, [r0, #0x5c]
    mov r0, r10
    mov r1, r1, lsl #16
    mov r2, r1, asr #16
    mov r1, r4
    mov r3, r11
    bl native_fn_021f0858
ov001_021f39cc_L2c4:
    mov r7, r0
    ldr r0, [sp, #0x58]
    cmp r0, #0
    beq ov001_021f39cc_L2ec
    mov r0, r8
    mov r1, r10
    mov r2, r4
    bl native_fn_021e19e4
    cmp r0, #0
    movne r7, #0
ov001_021f39cc_L2ec:
    ldr r0, [sp, #0x58]
    cmp r0, #0
    beq ov001_021f39cc_L3ec
    ldr r2, =0x0223989c
    ldrb r1, [r4, #0x31f]
    ldrb r0, [r9, #0x31f]
    ldrb r5, [r2, #0x29]
    mov r3, #0
    cmp r1, r0
    str r5, [sp]
    movne r6, #1
    str r3, [sp, #0x4]
    str r3, [sp, #0x8]
    moveq r6, #0
    str r6, [sp, #0xc]
    ldr r2, [r2, #0x5c]
    mov r0, r10
    mov r2, r2, lsl #16
    mov r1, r4
    mov r3, r11
    mov r2, r2, asr #16
    bl native_fn_021f08a0
    b ov001_021f39cc_L3ec
ov001_021f39cc_L348:
    mov r0, r10
    mov r1, r4
    mov r2, r8
    mov r3, #0
    bl native_fn_021f0d10
    cmp r0, #6
    mov r7, #0
    beq ov001_021f39cc_L3ec
    ldr r0, =0x0223989c
    mov r5, r7
    ldrsb r0, [r0, #43]
    cmp r0, #0
    ble ov001_021f39cc_L3ec
    ldr r6, =0x0223995c
ov001_021f39cc_L380:
    ldrb r1, [r4, #0x31f]
    ldrb r0, [r9, #0x31f]
    cmp r1, r0
    ldr r0, =0x0223989c
    movne r2, #1
    ldrb r3, [r0, #0x29]
    moveq r2, #0
    mov r0, r10
    str r3, [sp]
    ldrb r12, [r6], #1
    mov r1, r4
    mov r3, r11
    str r12, [sp, #0x4]
    mov r12, #1
    str r12, [sp, #0x8]
    str r2, [sp, #0xc]
    ldr r2, =0x02239968
    ldr r2, [r2, r5, lsl #2]
    mov r2, r2, lsl #16
    mov r2, r2, asr #16
    bl native_fn_021f08a0
    add r7, r7, r0
    ldr r0, =0x0223989c
    add r5, r5, #1
    ldrsb r0, [r0, #43]
    cmp r5, r0
    blt ov001_021f39cc_L380
ov001_021f39cc_L3ec:
    ldr r0, [sp, #0x54]
    cmp r0, #0
    beq ov001_021f39cc_L5a8
    mov r0, #0
    str r0, [sp, #0x24]
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    bne ov001_021f39cc_L41c
    mov r0, r4
    mov r1, r8
    bl native_fn_021dc59c
ov001_021f39cc_L41c:
    cmp r7, #0
    bge ov001_021f39cc_L438
    bl native_fn_021e29e8
    tst r0, #32
    mvnne r0, #0
    mulne r0, r7, r0
    movne r7, r0
ov001_021f39cc_L438:
    cmp r7, #0
    ble ov001_021f39cc_L504
    mov r0, r4
    mov r1, r7
    mov r2, r8
    bl native_fn_021f0eb4
    mov r0, r0, lsl #16
    mov r6, r0, asr #16
    mov r0, r4
    mov r1, r8
    bl native_fn_021e13c8
    cmp r0, #0
    bne ov001_021f39cc_L498
    cmp r6, #0
    ble ov001_021f39cc_L498
    mov r0, r4
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    mov r0, #1
    str r0, [sp, #0x2c]
    ldr r0, [sp, #0x40]
    add r0, r0, #1
    str r0, [sp, #0x40]
ov001_021f39cc_L498:
    cmp r6, #0
    ldrle r0, [sp, #0x30]
    ldr r1, =0x0223989c
    addle r0, r0, #1
    strle r0, [sp, #0x30]
    ldrb r0, [r4, #0x31f]
    cmp r6, #0
    movlt r3, #0
    add r0, r10, r0, lsl #1
    add r0, r0, #768
    ldrsh r2, [r0, #78]
    movge r3, r6
    add r2, r2, r3
    strh r2, [r0, #78]
    ldr r0, [r1, #0x84]
    bl native_fn_021dc9d4
    mov r5, r0
    mov r0, r8
    bl native_fn_021f2464
    str r0, [sp]
    ldr r0, =0x0223989c
    mov r3, r5
    ldr r0, [r0, #0x84]
    mov r1, r4
    mov r2, r8
    bl native_fn_0220f600
    b ov001_021f39cc_L544
ov001_021f39cc_L504:
    cmp r7, #0
    ldrge r0, [sp, #0x30]
    mov r6, #0
    addge r0, r0, #1
    strge r0, [sp, #0x30]
    bge ov001_021f39cc_L544
    mov r0, r4
    rsb r1, r7, #0
    mov r2, r8
    bl native_fn_021f0f0c
    rsb r7, r0, #0
    ldr r0, [sp, #0x34]
    add r0, r0, #1
    str r0, [sp, #0x34]
    mov r0, #1
    str r0, [sp, #0x24]
ov001_021f39cc_L544:
    ldr r0, [sp, #0x28]
    ldrb r3, [r0, #0x1e]
    ldr r0, [sp, #0x24]
    cmp r3, #1
    movne r7, r6
    cmp r0, #0
    bne ov001_021f39cc_L57c
    mov r0, #0
    str r0, [sp]
    mov r0, r4
    mov r1, r7
    mov r2, r8
    bl native_fn_021ee78c
    b ov001_021f39cc_L58c
ov001_021f39cc_L57c:
    mov r2, r3
    mov r0, r4
    rsb r1, r7, #0
    bl native_fn_021ee7d4
ov001_021f39cc_L58c:
    ldrb r0, [r4, #0x31e]
    ldrb r1, [r4, #0x31f]
    mov r2, r7
    bl native_fn_022024d4
    ldrb r0, [r4, #0x357]
    add r0, r0, #1
    strb r0, [r4, #0x357]
ov001_021f39cc_L5a8:
    ldr r0, [sp, #0x58]
    cmp r0, #0
    beq ov001_021f39cc_L668
    ldrh r0, [sp, #72]
    cmp r0, #249
    cmpeq r7, #0
    beq ov001_021f39cc_L668
    mov r0, r4
    bl native_fn_021dbd24
    cmp r0, #0
    ble ov001_021f39cc_L654
    ldr r0, =0x0223989c
    ldr r1, =0x022399b8
    ldrsb r5, [r0, #43]
    mov r0, r4
    str r4, [r1, r5, lsl #2]
    bl native_fn_021dbd30
    mov r1, r0
    ldr r0, =0x0223989c
    ldr r2, [r4, #0x1e8]
    ldrh r0, [r0, #80]
    add r2, r2, #70
    bl native_fn_0207b244
    ldr r1, =0x02239968
    ldr r2, [sp, #0x4c]
    str r0, [r1, r5, lsl #2]
    ldr r1, =0x0223989c
    ldr r0, =0x0223995c
    ldrsb r3, [r1, #43]
    strb r2, [r0, r5]
    ldrh r2, [sp, #72]
    add r3, r3, #1
    add r0, r4, #768
    strb r3, [r1, #0x2b]
    strh r2, [r0, #74]
    ldr r0, [sp, #0x38]
    ldrb r1, [r4, #0x31f]
    add r0, r0, #1
    str r0, [sp, #0x38]
    mov r2, #1
    add r0, sp, #92
    str r2, [r0, r1, lsl #2]
    b ov001_021f39cc_L6a8
ov001_021f39cc_L654:
    ldrb r1, [r4, #0x31f]
    mov r2, #0
    add r0, sp, #92
    str r2, [r0, r1, lsl #2]
    b ov001_021f39cc_L6a8
ov001_021f39cc_L668:
    ldr r0, [sp, #0x54]
    cmp r0, #0
    bne ov001_021f39cc_L6a8
    mov r1, #0
    ldr r3, [sp, #0x28]
    str r1, [sp]
    ldrb r3, [r3, #0x1e]
    mov r0, r4
    mov r2, r8
    bl native_fn_021ee78c
    ldr r0, [sp, #0x30]
    add r0, r0, #1
    str r0, [sp, #0x30]
    ldrb r0, [r4, #0x357]
    add r0, r0, #1
    strb r0, [r4, #0x357]
ov001_021f39cc_L6a8:
    ldr r0, [sp, #0x50]
    cmp r0, #0
    addne r0, r4, #768
    ldrneh r0, [r0, #76]
    cmpne r0, #0
    beq ov001_021f39cc_L6d8
    bl native_fn_0205d790
    mov r2, r0
    add r0, r4, #768
    ldrh r0, [r0, #76]
    mov r1, r4
    bl native_fn_021eec7c
ov001_021f39cc_L6d8:
    ldr r0, [sp, #0x20]
    add r9, r9, #1088
    add r1, r0, #1
    ldr r0, [sp, #0x44]
    str r1, [sp, #0x20]
    cmp r1, r0
    blt ov001_021f39cc_Lb8
ov001_021f39cc_L6f4:
    ldr r0, [sp, #0x40]
    cmp r0, #0
    ble ov001_021f39cc_L70c
    mov r0, #239
    mov r1, #1
    bl native_fn_021f949c
ov001_021f39cc_L70c:
    ldr r0, [sp, #0x3c]
    cmp r0, #0
    ble ov001_021f39cc_L724
    mov r0, #228
    mov r1, #1
    bl native_fn_021f949c
ov001_021f39cc_L724:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    ble ov001_021f39cc_L73c
    mov r0, #19
    mov r1, #1
    bl native_fn_021f94d8
ov001_021f39cc_L73c:
    ldr r0, [sp, #0x38]
    cmp r0, #0
    ble ov001_021f39cc_L79c
    mov r2, #0
    add r1, sp, #92
ov001_021f39cc_L750:
    ldr r0, [r1, r2, lsl #2]
    cmp r0, #0
    beq ov001_021f39cc_L778
    mov r0, #243
    mov r1, #1
    bl native_fn_021f949c
    ldr r0, [sp, #0x1c]
    mov r1, #1
    str r1, [r0]
    b ov001_021f39cc_L784
ov001_021f39cc_L778:
    add r2, r2, #1
    cmp r2, #3
    blt ov001_021f39cc_L750
ov001_021f39cc_L784:
    movs r0, #1
    bne ov001_021f39cc_L7a8
    ldr r0, [sp, #0x1c]
    mov r1, #0
    str r1, [r0]
    b ov001_021f39cc_L7a8
ov001_021f39cc_L79c:
    ldr r0, [sp, #0x1c]
    mov r1, #0
    str r1, [r0]
ov001_021f39cc_L7a8:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    ble ov001_021f39cc_L7c0
    mov r0, #242
    mov r1, #1
    bl native_fn_021f949c
ov001_021f39cc_L7c0:
    ldr r0, =0x0223989c
    ldrb r0, [r0, #0x10]
    cmp r0, #0
    bne ov001_021f39cc_L808
    mov r0, r8
    mov r1, #536870912
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f39cc_L808
    mov r0, #0
    str r0, [sp]
    add r0, r10, #512
    ldrsb r2, [r0, #52]
    mov r1, #8
    mov r0, r10
    rsb r2, r2, #0
    sub r3, r1, #9
    bl native_fn_021dbf98
ov001_021f39cc_L808:
    mov r0, r8
    mov r1, #128
    bl native_fn_0207b004
    cmp r0, #0
    beq ov001_021f39cc_L828
    mov r0, r10
    mov r1, #26
    bl native_fn_021dc940
ov001_021f39cc_L828:
    ldr r0, [sp, #0x2c]
    add sp, sp, #104
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
