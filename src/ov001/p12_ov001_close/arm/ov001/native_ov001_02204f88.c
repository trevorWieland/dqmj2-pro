/* ov001 row 0x02204f88: 1728 bytes.
 *
 * What it does: 432 instructions; 35 call(s) to 0x021db530, 0x0202a37c, 0x02204fec, +32 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (432 instructions, 35 calls, 28 branches, 32 back edges, 0 literal slots).
 *
 *   back edge +0x90 -> +0x64
 *   branch +0xb8 -> +0x1c4
 *   branch +0xd8 -> +0x320
 *   branch +0x114 -> +0x144
 *   branch +0x140 -> +0x184
 *   branch +0x164 -> +0x170
 *   branch +0x190 -> +0x320
 *   back edge +0x1bc -> +0xe4
 *   branch +0x1c0 -> +0x320
 *   branch +0x1cc -> +0x1e8
 *   branch +0x1e4 -> +0x23c
 *   back edge +0x20c -> +0x1f4
 *   branch +0x244 -> +0x320
 *   branch +0x280 -> +0x2b0
 *   branch +0x2ac -> +0x2ec
 *   branch +0x2d0 -> +0x2dc
 *   branch +0x2f8 -> +0x320
 *   back edge +0x31c -> +0x250
 *   branch +0x33c -> +0x3b0
 *   branch +0x34c -> +0x35c
 *   branch +0x358 -> +0x364
 *   branch +0x39c -> +0x3b0
 *   back edge +0x3c0 -> +0x338
 *   branch +0x430 -> +0x5e8
 *   branch +0x43c -> +0x478
 *   branch +0x474 -> +0x4ac
 *   branch +0x4d0 -> +0x5c8
 *   branch +0x530 -> +0x580
 *   branch +0x540 -> +0x550
 *   branch +0x54c -> +0x558
 *   back edge +0x590 -> +0x528
 *   back edge +0x600 -> +0x418
 *   branch +0x614 -> +0x694
 *   branch +0x660 -> +0x674
 *   branch +0x670 -> +0x694
 *   back edge +0x6a8 -> +0x60c
 *   test +0x88 cmp r0, #20
 *   test +0xb4 cmp r4, #0
 *   test +0xcc cmp r9, r0, asr #16
 *   test +0x110 cmp r11, #0
 *   test +0x15c cmp r6, #4
 *   test +0x168 cmp r6, #1
 *   test +0x18c cmp r1, r0
 *   test +0x1ac cmp r0, r9
 *   test +0x1c8 tst r3, #16
 *   test +0x1f4 tst r3, r1, lsl r0
 *   test +0x208 cmp r0, #3
 *   test +0x240 cmp r0, r9
 *   test +0x27c cmp r11, #0
 *   test +0x2c8 cmp r6, #4
 *   test +0x2d4 cmp r6, #1
 *   test +0x2f4 cmp r1, r0
 *   test +0x30c cmp r0, r9
 *   test +0x320 cmp r4, #0
 *   test +0x338 tst r5, r11, lsl r9
 *   test +0x340 cmp r4, #0
 *   test +0x374 cmp r1, r0
 *   test +0x384 cmp r1, r0
 *   test +0x390 cmp r4, #0
 *   test +0x3a4 cmp r1, r0
 *   test +0x3bc cmp r9, #3
 *   test +0x42c tst r5, r2, lsl r0
 *   test +0x434 cmp r4, #0
 *   test +0x4cc cmp r0, r1
 *   test +0x4d8 cmp r4, #1
 *   test +0x4ec cmpeq r0, r1
 *   test +0x50c cmp r1, r0
 *   test +0x51c cmp r1, r0
 *   test +0x52c tst r5, r0, lsl r6
 *   test +0x534 cmp r4, #0
 *   test +0x568 cmp r1, r2
 *   test +0x574 cmp r1, r2
 *   test +0x58c cmp r6, #3
 *   test +0x5fc cmp r0, #3
 *   test +0x610 cmp r0, r6
 *   test +0x65c cmp r0, #0
 *   test +0x6a0 cmp r5, #20
 *   1 block transfer(s), 48 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02204f88; the literal pool and
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

extern void native_fn_021db530(void);
extern void native_fn_0202a37c(void);
extern void native_fn_02204df0(void);
extern void native_fn_02204d60(void);
extern void native_fn_02202398(void);
extern void native_fn_02204e24(void);
extern void native_fn_02202384(void);
extern void native_fn_02205648(void);
extern void native_fn_022057a8(void);
extern void native_fn_0205f98c(void);
extern void native_fn_022023a8(void);
extern void native_fn_02048a60(void);
extern void native_fn_02048a94(void);
extern void native_fn_02048a9c(void);
extern void native_fn_02204ee0(void);


asm u32 native_ov001_02204f88 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #60
    mov r10, r0
    ldr r0, [r10, #0x2c]
    mov r0, r0, lsl #24
    mov r4, r0, asr #24
    mov r0, r4
    bl native_fn_021db530
    ldr r1, [r10, #0x30]
    mov r0, #2
    mov r3, r1, lsl #24
    mov r1, #244
    mov r2, #4
    ldr r5, [r10, #0x44]
    mov r8, r3, asr #24
    mov r11, #1
    bl native_fn_0202a37c
    mov r7, r0
    str r0, [r10, #0x40]
    mov r0, #0
    mov r1, r7
    mvn r9, #0
    mov r6, r0
    mov r3, #255
    mov r2, r11
ov001_02204f88_L64:
    strb r9, [r1]
    strb r6, [r1, #0x1]
    strb r3, [r1, #0x4]
    add r0, r0, #1
    strb r3, [r1, #0x5]
    mov r0, r0, lsl #24
    strb r2, [r1, #0x6]
    mov r0, r0, asr #24
    strb r6, [r1, #0x7]
    cmp r0, #20
    add r1, r1, #12
    blt ov001_02204f88_L64
    str r6, [r7, #0xf0]
    ldrsh r9, [r10, #20]
    ldrsh r2, [r10, #22]
    mov r0, r10
    mov r1, #18
    str r2, [sp, #0x2c]
    bl native_fn_02204df0
    str r0, [sp, #0x30]
    cmp r4, #0
    bne ov001_02204f88_L1c4
    mov r0, #6
    mul r0, r8, r0
    add r0, r0, #88
    mov r0, r0, lsl #16
    cmp r9, r0, asr #16
    mov r0, r0, asr #16
    str r0, [sp, #0x1c]
    ble ov001_02204f88_L320
    mvn r0, #0
    str r0, [sp, #0x34]
ov001_02204f88_Le4:
    ldrsb r1, [r10, #36]
    ldr r3, [sp, #0x30]
    mov r0, r10
    str r9, [sp]
    ldr r2, [sp, #0x2c]
    str r2, [sp, #0x4]
    mov r2, #7
    str r2, [sp, #0x8]
    mov r2, r1
    bl native_fn_02204d60
    str r0, [sp, #0x24]
    cmp r11, #0
    beq ov001_02204f88_L144
    and r0, r9, #248
    sub r0, r0, #4
    mov r11, #0
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    mov r0, r10
    mov r1, r11
    mov r6, #1
    bl native_fn_02204df0
    str r0, [sp, #0x30]
    b ov001_02204f88_L184
ov001_02204f88_L144:
    ldr r0, [sp, #0x1c]
    sub r1, r9, r0
    mov r0, r1, asr #2
    add r0, r1, r0, lsr #29
    mov r0, r0, lsl #21
    mov r6, r0, asr #24
    cmp r6, #4
    movgt r6, #4
    bgt ov001_02204f88_L170
    cmp r6, #1
    movlt r6, #1
ov001_02204f88_L170:
    add r0, r9, #7
    and r0, r0, #248
    sub r0, r0, r6, lsl #3
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
ov001_02204f88_L184:
    ldr r1, [sp, #0x24]
    ldr r0, [sp, #0x34]
    cmp r1, r0
    beq ov001_02204f88_L320
    mov r0, #12
    mla r2, r1, r0, r7
    strb r6, [r2, #0x6]
    mov r0, #2
    strb r0, [r2, #0x7]
    ldr r0, [sp, #0x1c]
    cmp r0, r9
    ldr r0, [r7, #0xf0]
    add r0, r0, r6
    str r0, [r7, #0xf0]
    blt ov001_02204f88_Le4
    b ov001_02204f88_L320
ov001_02204f88_L1c4:
    ldr r3, [r10, #0x44]
    tst r3, #16
    bne ov001_02204f88_L1e8
    mov r0, r8, lsl #3
    rsb r0, r0, #192
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    str r0, [sp, #0x1c]
    b ov001_02204f88_L23c
ov001_02204f88_L1e8:
    mov r2, #0
    mov r0, r2
    mov r1, #2
ov001_02204f88_L1f4:
    tst r3, r1, lsl r0
    movne r2, r0
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    cmp r0, #3
    blt ov001_02204f88_L1f4
    sub r0, r8, r2
    mov r0, r0, lsl #24
    movs r0, r0, asr #24
    rsbmi r0, r0, #0
    movmi r0, r0, lsl #24
    movmi r0, r0, asr #24
    mov r0, r0, lsl #3
    add r0, r0, #176
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    str r0, [sp, #0x1c]
ov001_02204f88_L23c:
    ldr r0, [sp, #0x1c]
    cmp r0, r9
    ble ov001_02204f88_L320
    mvn r0, #0
    str r0, [sp, #0x38]
ov001_02204f88_L250:
    ldrsb r1, [r10, #36]
    ldr r3, [sp, #0x30]
    mov r0, r10
    str r9, [sp]
    ldr r2, [sp, #0x2c]
    str r2, [sp, #0x4]
    mov r2, #7
    str r2, [sp, #0x8]
    mov r2, r1
    bl native_fn_02204d60
    str r0, [sp, #0x10]
    cmp r11, #0
    beq ov001_02204f88_L2b0
    and r0, r9, #248
    add r0, r0, #16
    mov r11, #0
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
    mov r0, r10
    mov r1, r11
    mov r6, #1
    bl native_fn_02204df0
    str r0, [sp, #0x30]
    b ov001_02204f88_L2ec
ov001_02204f88_L2b0:
    ldr r0, [sp, #0x1c]
    sub r1, r0, r9
    mov r0, r1, asr #2
    add r0, r1, r0, lsr #29
    mov r0, r0, lsl #21
    mov r6, r0, asr #24
    cmp r6, #4
    movgt r6, #4
    bgt ov001_02204f88_L2dc
    cmp r6, #1
    movlt r6, #1
ov001_02204f88_L2dc:
    and r0, r9, #248
    add r0, r0, r6, lsl #3
    mov r0, r0, lsl #16
    mov r9, r0, asr #16
ov001_02204f88_L2ec:
    ldr r1, [sp, #0x10]
    ldr r0, [sp, #0x38]
    cmp r1, r0
    beq ov001_02204f88_L320
    mov r0, #12
    mla r0, r1, r0, r7
    strb r6, [r0, #0x6]
    ldr r0, [sp, #0x1c]
    cmp r0, r9
    ldr r0, [r7, #0xf0]
    add r0, r0, r6
    str r0, [r7, #0xf0]
    bgt ov001_02204f88_L250
ov001_02204f88_L320:
    cmp r4, #0
    moveq r0, #0
    movne r0, #8
    and r6, r0, #255
    mov r9, #0
    mov r11, #2
ov001_02204f88_L338:
    tst r5, r11, lsl r9
    beq ov001_02204f88_L3b0
    cmp r4, #0
    mov r0, r4
    mov r1, r9
    bne ov001_02204f88_L35c
    bl native_fn_02202398
    add r0, r0, #12
    b ov001_02204f88_L364
ov001_02204f88_L35c:
    bl native_fn_02202398
    add r0, r0, #4
ov001_02204f88_L364:
    add r0, r0, r8, lsl #3
    mov r0, r0, lsl #16
    ldr r1, [sp, #0x2c]
    mov r0, r0, asr #16
    cmp r1, r0
    orrgt r1, r6, #1
    andgt r6, r1, #255
    ldr r1, [sp, #0x2c]
    cmp r1, r0
    orrlt r1, r6, #4
    andlt r6, r1, #255
    cmp r4, #0
    orreq r0, r6, #2
    andeq r6, r0, #255
    beq ov001_02204f88_L3b0
    ldr r1, [sp, #0x2c]
    cmp r1, r0
    orreq r0, r6, #2
    andeq r6, r0, #255
ov001_02204f88_L3b0:
    add r0, r9, #1
    mov r0, r0, lsl #24
    mov r9, r0, asr #24
    cmp r9, #3
    blt ov001_02204f88_L338
    mov r0, r10
    mov r1, r6
    bl native_fn_02204e24
    mov r3, r0
    ldrsb r1, [r10, #36]
    ldr r0, [sp, #0x1c]
    mov r2, #6
    str r0, [sp]
    ldr r0, [sp, #0x2c]
    stmib sp, {r0, r2}
    mov r0, r10
    mov r2, r1
    bl native_fn_02204d60
    ldr r0, [sp, #0x1c]
    ldr r1, [r7, #0xf0]
    add r0, r0, #8
    str r0, [sp, #0x20]
    add r0, r1, #1
    str r0, [r7, #0xf0]
    mov r0, #0
    str r0, [sp, #0x14]
ov001_02204f88_L418:
    ldr r0, [r7, #0xf0]
    mov r2, #2
    mov r1, r0, lsl #24
    ldr r0, [sp, #0x14]
    mov r6, r1, asr #24
    tst r5, r2, lsl r0
    beq ov001_02204f88_L5e8
    cmp r4, #0
    mov r0, r4
    bne ov001_02204f88_L478
    ldr r1, [sp, #0x14]
    bl native_fn_02202398
    add r0, r0, #12
    add r0, r0, r8, lsl #3
    mov r1, r0, lsl #16
    mov r1, r1, asr #16
    mov r0, r4
    str r1, [sp, #0xc]
    bl native_fn_02202384
    sub r0, r0, #14
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    str r0, [sp, #0x28]
    b ov001_02204f88_L4ac
ov001_02204f88_L478:
    ldr r1, [sp, #0x14]
    bl native_fn_02202398
    add r0, r0, #4
    add r0, r0, r8, lsl #3
    mov r1, r0, lsl #16
    mov r1, r1, asr #16
    mov r0, r4
    str r1, [sp, #0xc]
    bl native_fn_02202384
    sub r0, r0, #13
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    str r0, [sp, #0x28]
ov001_02204f88_L4ac:
    str r6, [sp]
    ldr r1, [sp, #0x1c]
    ldr r2, [sp, #0x2c]
    ldr r3, [sp, #0xc]
    mov r0, r10
    bl native_fn_02205648
    mvn r1, #0
    str r0, [sp, #0x18]
    cmp r0, r1
    beq ov001_02204f88_L5c8
    mov r0, #0
    cmp r4, #1
    orr r9, r0, #2
    ldreqsh r1, [r10, #22]
    ldreq r0, [sp, #0xc]
    mov r6, #0
    cmpeq r0, r1
    orreq r0, r9, #8
    andeq r9, r0, #255
    ldr r0, [sp, #0x18]
    mov r1, #12
    mla r11, r0, r1, r7
    ldrsh r1, [r11, #10]
    ldr r0, [sp, #0x2c]
    cmp r1, r0
    orrgt r0, r9, #1
    andgt r9, r0, #255
    ldr r0, [sp, #0x2c]
    cmp r1, r0
    orrlt r0, r9, #4
    andlt r9, r0, #255
ov001_02204f88_L528:
    mov r0, #2
    tst r5, r0, lsl r6
    beq ov001_02204f88_L580
    cmp r4, #0
    mov r0, r4
    mov r1, r6
    bne ov001_02204f88_L550
    bl native_fn_02202398
    add r0, r0, #12
    b ov001_02204f88_L558
ov001_02204f88_L550:
    bl native_fn_02202398
    add r0, r0, #4
ov001_02204f88_L558:
    add r0, r0, r8, lsl #3
    mov r0, r0, lsl #16
    ldrsh r1, [r11, #10]
    mov r2, r0, asr #16
    cmp r1, r2
    orrgt r0, r9, #1
    andgt r9, r0, #255
    cmp r1, r2
    orrlt r0, r9, #4
    andlt r9, r0, #255
ov001_02204f88_L580:
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #3
    blt ov001_02204f88_L528
    ldr r0, [sp, #0x18]
    mov r1, #12
    mla r6, r0, r1, r7
    mov r0, r10
    mov r1, r9
    bl native_fn_02204e24
    strb r0, [r6, #0x2]
    mov r0, #6
    strb r0, [r6, #0x3]
    ldrsb r0, [r6, #1]
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
ov001_02204f88_L5c8:
    ldr r0, [sp, #0x20]
    str r6, [sp]
    mov r2, r0, lsl #16
    ldr r1, [sp, #0xc]
    ldr r3, [sp, #0x28]
    mov r0, r10
    mov r2, r2, asr #16
    bl native_fn_022057a8
ov001_02204f88_L5e8:
    ldr r0, [sp, #0x14]
    add r0, r0, #1
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    str r0, [sp, #0x14]
    cmp r0, #3
    blt ov001_02204f88_L418
    mov r5, #0
    mvn r6, #0
ov001_02204f88_L60c:
    ldrsb r0, [r7]
    cmp r0, r6
    beq ov001_02204f88_L694
    ldr r0, [r10, #0x1c]
    and r1, r5, #255
    bl native_fn_0205f98c
    ldrb r1, [r7, #0x2]
    mov r4, r0
    bl native_fn_022023a8
    ldrsh r1, [r7, #8]
    ldrsh r2, [r7, #10]
    mov r0, r4
    bl native_fn_02048a60
    ldrb r1, [r7, #0x3]
    mov r0, r4
    bl native_fn_02048a94
    mov r0, r4
    ldrb r1, [r10, #0x21]
    bl native_fn_02048a9c
    ldr r0, [r10, #0x38]
    cmp r0, #0
    bne ov001_02204f88_L674
    ldr r0, [r4, #0x7c]
    bic r0, r0, #2
    str r0, [r4, #0x7c]
    b ov001_02204f88_L694
ov001_02204f88_L674:
    ldrb r2, [r7, #0x6]
    mov r0, r10
    mov r1, r5
    sub r2, r2, #1
    bl native_fn_02204ee0
    ldr r0, [r4, #0x7c]
    orr r0, r0, #2
    str r0, [r4, #0x7c]
ov001_02204f88_L694:
    add r0, r5, #1
    mov r0, r0, lsl #24
    mov r5, r0, asr #24
    cmp r5, #20
    add r7, r7, #12
    blt ov001_02204f88_L60c
    mov r0, #0
    strh r0, [r10, #24]
    strh r0, [r10, #26]
    add sp, sp, #60
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
