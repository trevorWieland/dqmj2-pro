/* ov001 row 0x021e9de0: 1464 bytes.
 *
 * What it does: 360 instructions; 36 call(s) to 0x0207afec, 0x021e1410, 0x021ee78c, +33 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: block fill (360 instructions, 36 calls, 33 branches, 15 back edges, 6 literal slots).
 *
 *   pool +0x5a0 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x5a4 -> constant 0x02238e50 (image word 0x02238e50)
 *   pool +0x5a8 -> constant 0x02238de0 (image word 0x02238de0)
 *   pool +0x5ac -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x5b0 -> constant 0x00000438 (image word 0x00000438)
 *   pool +0x5b4 -> constant 0x00000ccd (image word 0x00000ccd)
 *   branch +0x58 -> +0xa4
 *   branch +0x6c -> +0xa4
 *   branch +0xa0 -> +0x594
 *   branch +0xb0 -> +0x100
 *   branch +0xc8 -> +0x100
 *   branch +0xfc -> +0x594
 *   branch +0x164 -> +0x200
 *   branch +0x184 -> +0x25c
 *   branch +0x198 -> +0x25c
 *   back edge +0x1f8 -> +0x1a4
 *   branch +0x1fc -> +0x25c
 *   branch +0x268 -> +0x284
 *   branch +0x28c -> +0x2a4
 *   branch +0x294 -> +0x2a4
 *   branch +0x2a0 -> +0x3c0
 *   branch +0x2b4 -> +0x2f4
 *   branch +0x2d4 -> +0x2e8
 *   branch +0x2f0 -> +0x314
 *   branch +0x2f4 -> +0x314
 *   branch +0x318 -> +0x33c
 *   branch +0x338 -> +0x350
 *   branch +0x378 -> +0x390
 *   branch +0x3c8 -> +0x454
 *   branch +0x3d8 -> +0x454
 *   branch +0x3f0 -> +0x414
 *   back edge +0x410 -> +0x3fc
 *   branch +0x418 -> +0x440
 *   branch +0x450 -> +0x490
 *   branch +0x464 -> +0x490
 *   branch +0x4a4 -> +0x4ec
 *   branch +0x4c8 -> +0x4ec
 *   branch +0x504 -> +0x580
 *   branch +0x510 -> +0x524
 *   branch +0x520 -> +0x580
 *   branch +0x530 -> +0x580
 *   branch +0x538 -> +0x558
 *   branch +0x554 -> +0x580
 *   branch +0x568 -> +0x580
 *   branch +0x584 -> +0x594
 *   test +0x48 cmp r1, #0
 *   test +0x68 cmp r0, #0
 *   test +0xac cmp r0, #0
 *   test +0xc4 cmp r0, #0
 *   test +0x160 cmp r1, #0
 *   test +0x17c cmp r0, #6
 *   test +0x194 cmp r0, #0
 *   test +0x1f4 cmp r4, r0
 *   test +0x248 cmp r3, #0
 *   test +0x264 cmp r0, #0
 *   test +0x288 cmp r0, #0
 *   test +0x290 cmp r6, #0
 *   test +0x29c cmp r0, #0
 *   test +0x2a8 cmp r9, #217
 *   test +0x2b0 cmp r6, #0
 *   test +0x2d0 cmp r0, #0
 *   test +0x314 cmp r4, #0
 *   test +0x370 cmp r0, #1
 *   test +0x374 cmpne r8, #0
 *   test +0x3c4 cmp r0, #0
 *   test +0x3d0 cmp r0, #249
 *   test +0x3d4 cmpeq r6, #0
 *   test +0x3ec cmp r7, #0
 *   test +0x404 cmp r2, r10
 *   test +0x40c cmp r4, r7
 *   test +0x414 cmp r5, #0
 *   test +0x458 cmp r0, #0
 *   test +0x460 cmpeq r0, #0
 *   test +0x498 cmp r0, #0
 *   test +0x4a0 cmpne r1, #0
 *   test +0x4c4 cmp r0, #0
 *   test +0x4f8 cmp r0, #0
 *   test +0x50c cmp r0, #0
 *   test +0x524 cmp r6, #0
 *   test +0x534 cmp r8, #0
 *   test +0x540 cmp r0, #1
 *   test +0x55c cmp r0, #0
 *   test +0x56c cmp r6, #20
 *   test +0x580 cmp r6, #0
 *   2 block transfer(s), 44 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e9de0; the literal pool and
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
extern void native_fn_021e1410(void);
extern void native_fn_021ee78c(void);
extern void native_fn_021f949c(void);
extern void native_fn_021e1468(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021f0d10(void);
extern void native_fn_021f0818(void);
extern void native_fn_021f0534(void);
extern void native_fn_021dc59c(void);
extern void native_fn_021e19c8(void);
extern void native_fn_021db718(void);
extern void native_fn_021e13c8(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f0f0c(void);
extern void native_fn_021ee7d4(void);
extern void native_fn_022024d4(void);
extern void native_fn_021d78a4(void);
extern void native_fn_0205d790(void);
extern void native_fn_021e9cd8(void);
extern void native_fn_021f94d8(void);


asm u32 native_ov001_021e9de0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    ldr r5, =0x02238d7c
    mov r4, r0
    ldrh r0, [r5, #54]
    mov r10, r1
    mov r1, #0
    mov r9, r2
    mov r8, r3
    ldr r7, [sp, #0x78]
    str r1, [sp, #0x30]
    bl native_fn_0207afec
    mov r1, #0
    str r1, [sp, #0x28]
    mov r1, r5
    ldrb r1, [r1, #0x19]
    str r0, [sp, #0x2c]
    ldr r0, [sp, #0x28]
    cmp r1, #0
    str r0, [sp, #0x24]
    str r0, [sp, #0x20]
    str r0, [sp, #0x3c]
    bne ov001_021e9de0_La4
    mov r0, r4
    mov r1, r9
    bl native_fn_021e1410
    cmp r0, #0
    beq ov001_021e9de0_La4
    mov r1, #0
    mov r0, r10
    mov r2, r9
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee78c
    ldr r1, [sp, #0x74]
    mov r0, #228
    bl native_fn_021f949c
    ldrb r0, [r10, #0x357]
    add r0, r0, #1
    strb r0, [r10, #0x357]
    b ov001_021e9de0_L594
ov001_021e9de0_La4:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x19]
    cmp r0, #0
    bne ov001_021e9de0_L100
    mov r0, r4
    mov r1, r10
    mov r2, r9
    bl native_fn_021e1468
    cmp r0, #0
    beq ov001_021e9de0_L100
    mov r1, #0
    mov r0, r10
    mov r2, r9
    mov r3, #1
    str r1, [sp]
    bl native_fn_021ee78c
    ldr r1, [sp, #0x74]
    mov r0, #228
    bl native_fn_021f949c
    ldrb r0, [r10, #0x357]
    add r0, r0, #1
    strb r0, [r10, #0x357]
    b ov001_021e9de0_L594
ov001_021e9de0_L100:
    mov r0, #0
    str r0, [sp]
    add r1, sp, #52
    str r1, [sp, #0x4]
    add r0, sp, #64
    str r0, [sp, #0x8]
    add r0, r10, #844
    str r0, [sp, #0xc]
    add r1, sp, #60
    str r1, [sp, #0x10]
    add r0, sp, #68
    str r0, [sp, #0x14]
    add r1, sp, #56
    str r1, [sp, #0x18]
    ldr r0, =0x02238d7c
    mov r1, r4
    ldrb r3, [r0, #0x19]
    ldrb r2, [r0, #0x14]
    mov r0, r9
    orr r3, r3, r2
    mov r2, r10
    bl native_fn_021e1a60
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x19]
    cmp r1, #0
    beq ov001_021e9de0_L200
    mov r0, r4
    mov r1, r10
    mov r2, r9
    mov r3, #1
    bl native_fn_021f0d10
    cmp r0, #6
    mov r6, #0
    beq ov001_021e9de0_L25c
    ldr r0, =0x02238d7c
    mov r4, r6
    ldrsb r0, [r0, #11]
    cmp r0, #0
    ble ov001_021e9de0_L25c
    ldr r5, =0x02238e50
    mov r11, #1
ov001_021e9de0_L1a4:
    ldr r0, =0x02238de0
    mov r1, r10
    ldr r0, [r0, r4, lsl #2]
    mov r2, r9
    strb r11, [r0, #0x356]
    ldrb r0, [r5], #1
    mov r3, r8
    str r0, [sp]
    mov r0, #0
    stmib sp, {r0, r11}
    ldr r0, =0x02238de0
    str r7, [sp, #0xc]
    ldr r0, [r0, r4, lsl #2]
    bl native_fn_021f0818
    mov r1, r9
    bl native_fn_021f0534
    add r6, r6, r0
    ldr r0, =0x02238d7c
    add r4, r4, #1
    ldrsb r0, [r0, #11]
    cmp r4, r0
    blt ov001_021e9de0_L1a4
    b ov001_021e9de0_L25c
ov001_021e9de0_L200:
    mov r3, #0
    str r3, [sp]
    ldrb r2, [r0, #0x14]
    mov r0, r4
    mov r1, r10
    stmib sp, {r2, r3}
    mov r2, r9
    mov r3, r8
    str r7, [sp, #0xc]
    bl native_fn_021f0818
    ldr r2, [sp, #0x70]
    ldr r1, =0x02238d7c
    mul r4, r0, r2
    ldrb r3, [r1, #0x2]
    ldr r2, =0x51eb851f
    smull r1, r0, r2, r4
    mov r1, r4, lsr #31
    add r0, r1, r0, asr #5
    cmp r3, #0
    movne r0, r0, lsl #1
    mov r1, r9
    bl native_fn_021f0534
    mov r6, r0
ov001_021e9de0_L25c:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x19]
    cmp r0, #0
    bne ov001_021e9de0_L284
    mov r0, r10
    mov r1, r9
    bl native_fn_021dc59c
    ldr r1, [sp, #0x3c]
    orr r0, r1, r0
    str r0, [sp, #0x3c]
ov001_021e9de0_L284:
    ldr r0, [sp, #0x44]
    cmp r0, #0
    bne ov001_021e9de0_L2a4
    cmp r6, #0
    beq ov001_021e9de0_L2a4
    bl native_fn_021e19c8
    cmp r0, #0
    beq ov001_021e9de0_L3c0
ov001_021e9de0_L2a4:
    mov r4, #0
    cmp r9, #217
    moveq r8, r4
    cmp r6, #0
    ble ov001_021e9de0_L2f4
    mov r0, r10
    rsb r1, r6, #0
    bl native_fn_021db718
    mov r0, r10
    mov r1, r9
    bl native_fn_021e13c8
    cmp r0, #0
    bne ov001_021e9de0_L2e8
    mov r0, r10
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
ov001_021e9de0_L2e8:
    mov r0, #1
    str r0, [sp, #0x30]
    b ov001_021e9de0_L314
ov001_021e9de0_L2f4:
    bge ov001_021e9de0_L314
    mov r0, r10
    mov r2, r9
    rsb r1, r6, #0
    bl native_fn_021f0f0c
    mov r4, #1
    str r4, [sp, #0x24]
    rsb r6, r0, #0
ov001_021e9de0_L314:
    cmp r4, #0
    bne ov001_021e9de0_L33c
    ldr r0, [sp, #0x2c]
    str r8, [sp]
    ldrb r3, [r0, #0x1e]
    mov r0, r10
    mov r1, r6
    mov r2, r9
    bl native_fn_021ee78c
    b ov001_021e9de0_L350
ov001_021e9de0_L33c:
    ldr r0, [sp, #0x2c]
    rsb r1, r6, #0
    ldrb r2, [r0, #0x1e]
    mov r0, r10
    bl native_fn_021ee7d4
ov001_021e9de0_L350:
    ldrb r0, [r10, #0x31e]
    ldrb r1, [r10, #0x31f]
    mov r3, #1
    mov r2, r6
    str r3, [sp, #0x20]
    bl native_fn_022024d4
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0xa]
    cmp r0, #1
    cmpne r8, #0
    beq ov001_021e9de0_L390
    ldr r1, =0x00000438
    ldr r3, =0x00000ccd
    mov r0, #0
    mov r2, #100
    bl native_fn_021d78a4
ov001_021e9de0_L390:
    ldrb r1, [r10, #0x357]
    ldr r0, =0x02238d7c
    add r1, r1, #1
    strb r1, [r10, #0x357]
    ldr r0, [r0, #0x60]
    ldrb r1, [r10, #0x31f]
    add r0, r0, #78
    add r2, r0, #768
    mov r1, r1, lsl #1
    ldrsh r0, [r2, r1]
    add r0, r0, r6
    strh r0, [r2, r1]
ov001_021e9de0_L3c0:
    ldr r0, [sp, #0x40]
    cmp r0, #0
    beq ov001_021e9de0_L454
    ldrh r0, [sp, #52]
    cmp r0, #249
    cmpeq r6, #0
    beq ov001_021e9de0_L454
    ldr r1, =0x02238d7c
    mov r5, #0
    ldrsb r7, [r1, #11]
    mov r4, r5
    cmp r7, #0
    ble ov001_021e9de0_L414
    ldr r3, =0x02238de0
    mov r1, #1
ov001_021e9de0_L3fc:
    ldr r2, [r3, r4, lsl #2]
    add r4, r4, #1
    cmp r2, r10
    moveq r5, r1
    cmp r4, r7
    blt ov001_021e9de0_L3fc
ov001_021e9de0_L414:
    cmp r5, #0
    bne ov001_021e9de0_L440
    ldr r1, =0x02238d7c
    ldr r4, [sp, #0x38]
    ldrsb r5, [r1, #11]
    ldr r3, =0x02238e50
    ldr r2, =0x02238de0
    strb r4, [r3, r5]
    add r3, r5, #1
    strb r3, [r1, #0xb]
    str r10, [r2, r5, lsl #2]
ov001_021e9de0_L440:
    add r1, r10, #768
    strh r0, [r1, #74]
    mov r0, #1
    str r0, [sp, #0x28]
    b ov001_021e9de0_L490
ov001_021e9de0_L454:
    ldr r0, [sp, #0x44]
    cmp r0, #0
    ldreq r0, [sp, #0x20]
    cmpeq r0, #0
    bne ov001_021e9de0_L490
    mov r1, #0
    ldr r0, [sp, #0x2c]
    str r1, [sp]
    ldrb r3, [r0, #0x1e]
    mov r0, r10
    mov r2, r9
    bl native_fn_021ee78c
    mov r0, #1
    str r0, [sp, #0x20]
    mov r6, #0
ov001_021e9de0_L490:
    add r0, r10, #768
    ldrh r0, [r0, #76]
    cmp r0, #0
    ldrne r1, [sp, #0x3c]
    cmpne r1, #0
    beq ov001_021e9de0_L4ec
    bl native_fn_0205d790
    add r1, r10, #768
    mov r2, r0
    ldrh r0, [r1, #76]
    mov r1, r10
    bl native_fn_021e9cd8
    ldr r0, [sp, #0x20]
    cmp r0, #0
    bne ov001_021e9de0_L4ec
    mov r1, #0
    ldr r0, [sp, #0x2c]
    str r1, [sp]
    ldrb r3, [r0, #0x1e]
    mov r0, r10
    mov r2, r9
    bl native_fn_021ee78c
    mov r6, #0
ov001_021e9de0_L4ec:
    mov r0, r10
    mov r1, r9
    bl native_fn_021e13c8
    cmp r0, #0
    movne r0, #241
    strne r0, [sp, #0x1c]
    bne ov001_021e9de0_L580
    ldr r0, [sp, #0x24]
    cmp r0, #0
    beq ov001_021e9de0_L524
    mov r0, #19
    mov r1, #0
    bl native_fn_021f94d8
    b ov001_021e9de0_L580
ov001_021e9de0_L524:
    cmp r6, #0
    moveq r0, #242
    streq r0, [sp, #0x1c]
    beq ov001_021e9de0_L580
    cmp r8, #0
    beq ov001_021e9de0_L558
    ldrb r0, [r10, #0x31e]
    cmp r0, #1
    moveq r0, #223
    streq r0, [sp, #0x1c]
    movne r0, #226
    strne r0, [sp, #0x1c]
    b ov001_021e9de0_L580
ov001_021e9de0_L558:
    ldr r0, [sp, #0x28]
    cmp r0, #0
    movne r0, #243
    strne r0, [sp, #0x1c]
    bne ov001_021e9de0_L580
    cmp r6, #20
    movge r0, #239
    strge r0, [sp, #0x1c]
    movlt r0, #238
    strlt r0, [sp, #0x1c]
ov001_021e9de0_L580:
    cmp r6, #0
    blt ov001_021e9de0_L594
    ldr r1, [sp, #0x74]
    ldr r0, [sp, #0x1c]
    bl native_fn_021f949c
ov001_021e9de0_L594:
    ldr r0, [sp, #0x30]
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
