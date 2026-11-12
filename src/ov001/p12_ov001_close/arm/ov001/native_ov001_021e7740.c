/* ov001 row 0x021e7740: 1608 bytes.
 *
 * What it does: 399 instructions; 52 call(s) to 0x020444ec, 0x01ffa824, 0x01ffa84c, +49 more; loops (back edge at +0x38); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 52 calls (399 instructions, 52 calls, 32 branches, 44 back edges, 3 literal slots).
 *
 *   pool +0x63c -> native_data_0222df0c (image word 0x0222df0c)
 *   pool +0x640 -> native_data_0222df13 (image word 0x0222df13)
 *   pool +0x644 -> constant 0x02238d40 (image word 0x02238d40)
 *   back edge +0x38 -> +0x1c
 *   back edge +0x6c -> +0x50
 *   branch +0x84 -> +0xa0
 *   branch +0x9c -> +0x12c
 *   branch +0xa8 -> +0xe4
 *   back edge +0xe0 -> +0xb4
 *   branch +0xec -> +0x1b4
 *   back edge +0x124 -> +0xf8
 *   branch +0x128 -> +0x1b4
 *   branch +0x134 -> +0x170
 *   back edge +0x16c -> +0x140
 *   branch +0x178 -> +0x1b4
 *   back edge +0x1b0 -> +0x184
 *   branch +0x1e0 -> +0x2fc
 *   branch +0x1f0 -> +0x2f0
 *   branch +0x224 -> +0x26c
 *   branch +0x22c -> +0x26c
 *   branch +0x268 -> +0x2e4
 *   branch +0x274 -> +0x2e4
 *   branch +0x28c -> +0x298
 *   branch +0x294 -> +0x2ac
 *   branch +0x2a0 -> +0x2e4
 *   branch +0x2a8 -> +0x2e4
 *   back edge +0x2ec -> +0x1f8
 *   back edge +0x2f8 -> +0x1e8
 *   branch +0x308 -> +0x340
 *   back edge +0x33c -> +0x30c
 *   back edge +0x348 -> +0x1d4
 *   branch +0x354 -> +0x378
 *   back edge +0x374 -> +0x360
 *   branch +0x388 -> +0x468
 *   branch +0x3a0 -> +0x458
 *   branch +0x3f4 -> +0x448
 *   branch +0x404 -> +0x448
 *   back edge +0x454 -> +0x3b0
 *   back edge +0x464 -> +0x398
 *   back edge +0x478 -> +0x380
 *   branch +0x498 -> +0x630
 *   branch +0x4e0 -> +0x620
 *   branch +0x4f4 -> +0x504
 *   branch +0x500 -> +0x518
 *   branch +0x508 -> +0x530
 *   branch +0x514 -> +0x530
 *   branch +0x52c -> +0x620
 *   branch +0x534 -> +0x5fc
 *   branch +0x544 -> +0x5d4
 *   branch +0x554 -> +0x5d4
 *   branch +0x580 -> +0x5bc
 *   back edge +0x5b8 -> +0x58c
 *   branch +0x5d8 -> +0x5ec
 *   branch +0x5e8 -> +0x620
 *   branch +0x5f8 -> +0x620
 *   branch +0x5fc -> +0x620
 *   branch +0x610 -> +0x620
 *   back edge +0x62c -> +0x4a0
 *   test +0x80 cmp r0, #0
 *   test +0x98 cmp r1, r0
 *   test +0xa0 cmp r5, #0
 *   test +0xd8 cmp r9, r5
 *   test +0xe4 cmp r4, #0
 *   test +0x11c cmp r8, r4
 *   test +0x12c cmp r4, #0
 *   test +0x164 cmp r9, r4
 *   test +0x170 cmp r5, #0
 *   test +0x1a8 cmp r8, r5
 *   test +0x1b8 tst r0, #4
 *   test +0x1dc cmp r0, r6
 *   test +0x1ec cmp r11, r6
 *   test +0x220 cmp r7, r1
 *   test +0x228 cmp r0, r1
 *   test +0x26c cmp r7, r1
 *   test +0x270 cmpeq r0, r1
 *   test +0x288 tst r0, #4
 *   test +0x290 cmp r7, r8
 *   test +0x29c tst r0, #4
 *   test +0x2a4 cmp r7, r8
 *   test +0x2e8 cmp r9, r6
 *   test +0x2f4 cmp r11, r6
 *   test +0x304 cmp r0, r6
 *   test +0x328 cmp r1, r0
 *   test +0x338 cmp r4, r6
 *   test +0x344 cmp r10, #6
 *   test +0x34c cmp r6, #0
 *   test +0x36c cmp r7, r6
 *   test +0x380 cmp r6, #0
 *   test +0x39c cmp r9, r6
 *   test +0x3e4 cmp r1, r11
 *   test +0x3f0 cmpeq r0, r1
 *   test +0x400 cmp r3, r2
 *   test +0x44c cmp r10, r6
 *   test +0x45c cmp r9, r6
 *   test +0x474 cmp r0, #6
 *   test +0x494 cmp r6, #0
 *   test +0x4dc cmp r1, #0
 *   test +0x4f0 cmp r7, #0
 *   test +0x4fc cmp r0, #0
 *   test +0x504 cmp r7, #1
 *   test +0x510 cmp r0, #0
 *   test +0x530 cmp r2, #0
 *   test +0x538 cmp r7, #0
 *   test +0x540 cmpeq r0, #0
 *   test +0x548 cmp r7, #1
 *   test +0x550 cmpeq r0, #0
 *   test +0x57c cmp r2, r0
 *   test +0x5b4 cmp r1, r0
 *   test +0x5d4 cmp r7, #0
 *   test +0x600 cmp r7, #0
 *   test +0x624 cmp r10, r6
 *   0 block transfer(s), 56 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021e7740; the literal pool and
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

extern u8 native_data_0222df0c[];
extern u8 native_data_0222df13[];
extern void native_fn_020444ec(void);
extern void native_fn_01ffa824(void);
extern void native_fn_01ffa84c(void);
extern void native_fn_021e76f8(void);
extern void native_fn_021e29e8(void);
extern void native_fn_021e76b4(void);
extern void native_fn_0207afec(void);
extern void native_fn_0203d294(void);
extern void ov001_side_slot_record_021db438(void);
extern void native_fn_021e865c(void);
extern void native_fn_02008e0c(void);


asm u32 native_ov001_021e7740 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #76
    ldr r6, =native_data_0222df0c
    add r7, sp, #59
    mov r5, r1
    mov r4, r3
    mov r2, #3
ov001_021e7740_L1c:
    ldrb r1, [r6]
    ldrb r0, [r6, #0x1]
    add r6, r6, #2
    strb r1, [r7]
    strb r0, [r7, #0x1]
    add r7, r7, #2
    subs r2, r2, #1
    bne ov001_021e7740_L1c
    ldrb r0, [r6]
    ldr r6, =native_data_0222df13
    add r3, sp, #52
    strb r0, [r7]
    mov r2, #3
ov001_021e7740_L50:
    ldrb r1, [r6]
    ldrb r0, [r6, #0x1]
    add r6, r6, #2
    strb r1, [r3]
    strb r0, [r3, #0x1]
    add r3, r3, #2
    subs r2, r2, #1
    bne ov001_021e7740_L50
    ldrb r0, [r6]
    mov r6, #0
    strb r0, [r3]
    bl native_fn_020444ec
    cmp r0, #0
    beq ov001_021e7740_La0
    bl native_fn_01ffa824
    mov r7, r0
    bl native_fn_01ffa84c
    and r1, r7, #255
    cmp r1, r0
    bhs ov001_021e7740_L12c
ov001_021e7740_La0:
    cmp r5, #0
    mov r9, #0
    ble ov001_021e7740_Le4
    ldr r7, =0x02238d40
    mov r8, r9
ov001_021e7740_Lb4:
    mov r0, r8
    mov r1, r9
    strb r8, [r7, r6, lsl #2]
    add r2, r7, r6, lsl #2
    strb r9, [r2, #0x1]
    bl native_fn_021e76f8
    add r1, r7, r6, lsl #2
    add r9, r9, #1
    strh r0, [r1, #2]
    cmp r9, r5
    add r6, r6, #1
    blt ov001_021e7740_Lb4
ov001_021e7740_Le4:
    cmp r4, #0
    mov r8, #0
    ble ov001_021e7740_L1b4
    ldr r5, =0x02238d40
    mov r7, #1
ov001_021e7740_Lf8:
    mov r0, r7
    mov r1, r8
    strb r7, [r5, r6, lsl #2]
    add r2, r5, r6, lsl #2
    strb r8, [r2, #0x1]
    bl native_fn_021e76f8
    add r1, r5, r6, lsl #2
    add r8, r8, #1
    strh r0, [r1, #2]
    cmp r8, r4
    add r6, r6, #1
    blt ov001_021e7740_Lf8
    b ov001_021e7740_L1b4
ov001_021e7740_L12c:
    cmp r4, #0
    mov r9, r6
    ble ov001_021e7740_L170
    ldr r7, =0x02238d40
    mov r8, #1
ov001_021e7740_L140:
    mov r0, r8
    mov r1, r9
    strb r8, [r7, r6, lsl #2]
    add r2, r7, r6, lsl #2
    strb r9, [r2, #0x1]
    bl native_fn_021e76f8
    add r1, r7, r6, lsl #2
    add r9, r9, #1
    strh r0, [r1, #2]
    cmp r9, r4
    add r6, r6, #1
    blt ov001_021e7740_L140
ov001_021e7740_L170:
    cmp r5, #0
    mov r8, #0
    ble ov001_021e7740_L1b4
    ldr r4, =0x02238d40
    mov r7, r8
ov001_021e7740_L184:
    mov r0, r7
    mov r1, r8
    strb r7, [r4, r6, lsl #2]
    add r2, r4, r6, lsl #2
    strb r8, [r2, #0x1]
    bl native_fn_021e76f8
    add r1, r4, r6, lsl #2
    add r8, r8, #1
    strh r0, [r1, #2]
    cmp r8, r5
    add r6, r6, #1
    blt ov001_021e7740_L184
ov001_021e7740_L1b4:
    bl native_fn_021e29e8
    tst r0, #4
    addne r0, sp, #52
    strne r0, [sp]
    addeq r0, sp, #59
    mov r10, #0
    streq r0, [sp]
    str r10, [sp, #0x20]
ov001_021e7740_L1d4:
    ldr r11, [sp, #0x20]
    mov r0, r11
    cmp r0, r6
    bge ov001_021e7740_L2fc
    ldr r5, =0x02238d40
ov001_021e7740_L1e8:
    mov r9, r11
    cmp r11, r6
    bge ov001_021e7740_L2f0
    add r4, r5, r11, lsl #2
ov001_021e7740_L1f8:
    mov r0, r11
    bl native_fn_021e76b4
    bl native_fn_0207afec
    ldrsb r7, [r0, #38]
    mov r0, r9
    bl native_fn_021e76b4
    bl native_fn_0207afec
    ldr r1, [sp]
    ldrsb r0, [r0, #38]
    ldrsb r1, [r1, r10]
    cmp r7, r1
    beq ov001_021e7740_L26c
    cmp r0, r1
    bne ov001_021e7740_L26c
    mov r8, r9, lsl #2
    add r7, r5, r9, lsl #2
    ldrh r3, [r5, r8]
    ldrh r2, [r7, #2]
    ldrh r1, [r4]
    ldrh r0, [r4, #2]
    strh r3, [sp, #72]
    strh r2, [sp, #74]
    strh r1, [r5, r8]
    ldrh r1, [sp, #72]
    strh r0, [r7, #2]
    ldrh r0, [sp, #74]
    strh r1, [r4]
    strh r0, [r4, #2]
    b ov001_021e7740_L2e4
ov001_021e7740_L26c:
    cmp r7, r1
    cmpeq r0, r1
    bne ov001_021e7740_L2e4
    add r0, r5, r9, lsl #2
    ldrsh r7, [r4, #2]
    ldrsh r8, [r0, #2]
    bl native_fn_021e29e8
    tst r0, #4
    bne ov001_021e7740_L298
    cmp r7, r8
    blt ov001_021e7740_L2ac
ov001_021e7740_L298:
    bl native_fn_021e29e8
    tst r0, #4
    beq ov001_021e7740_L2e4
    cmp r7, r8
    ble ov001_021e7740_L2e4
ov001_021e7740_L2ac:
    mov r8, r9, lsl #2
    add r7, r5, r9, lsl #2
    ldrh r3, [r5, r8]
    ldrh r2, [r7, #2]
    ldrh r1, [r4]
    ldrh r0, [r4, #2]
    strh r3, [sp, #40]
    strh r2, [sp, #42]
    strh r1, [r5, r8]
    ldrh r1, [sp, #40]
    strh r0, [r7, #2]
    ldrh r0, [sp, #42]
    strh r1, [r4]
    strh r0, [r4, #2]
ov001_021e7740_L2e4:
    add r9, r9, #1
    cmp r9, r6
    blt ov001_021e7740_L1f8
ov001_021e7740_L2f0:
    add r11, r11, #1
    cmp r11, r6
    blt ov001_021e7740_L1e8
ov001_021e7740_L2fc:
    ldr r4, [sp, #0x20]
    mov r0, r4
    cmp r0, r6
    bge ov001_021e7740_L340
ov001_021e7740_L30c:
    mov r0, r4
    bl native_fn_021e76b4
    bl native_fn_0207afec
    ldr r1, [sp]
    ldrsb r0, [r0, #38]
    ldrsb r1, [r1, r10]
    add r4, r4, #1
    cmp r1, r0
    ldreq r0, [sp, #0x20]
    addeq r0, r0, #1
    streq r0, [sp, #0x20]
    cmp r4, r6
    blt ov001_021e7740_L30c
ov001_021e7740_L340:
    add r10, r10, #1
    cmp r10, #6
    blt ov001_021e7740_L1d4
    cmp r6, #0
    mov r7, #0
    ble ov001_021e7740_L378
    add r5, sp, #66
    mov r4, #256
ov001_021e7740_L360:
    mov r0, r4
    bl native_fn_0203d294
    add r7, r7, #1
    cmp r7, r6
    strb r0, [r5], #1
    blt ov001_021e7740_L360
ov001_021e7740_L378:
    mov r0, #0
    str r0, [sp, #0xc]
ov001_021e7740_L380:
    cmp r6, #0
    mov r9, #0
    ble ov001_021e7740_L468
    add r7, sp, #66
    ldr r5, =0x02238d40
    str r7, [sp, #0x24]
ov001_021e7740_L398:
    mov r10, r9
    cmp r9, r6
    bge ov001_021e7740_L458
    ldr r0, [sp, #0x24]
    add r4, r5, r9, lsl #2
    add r8, r0, r9
ov001_021e7740_L3b0:
    ldrsh r0, [r4, #2]
    add r1, r5, r10, lsl #2
    ldrsh r11, [r1, #2]
    str r0, [sp, #0x4]
    mov r0, r9
    bl native_fn_021e76b4
    bl native_fn_0207afec
    ldrsb r0, [r0, #38]
    str r0, [sp, #0x8]
    mov r0, r10
    bl native_fn_021e76b4
    bl native_fn_0207afec
    ldr r1, [sp, #0x4]
    cmp r1, r11
    ldrsb r1, [r0, #38]
    ldreq r0, [sp, #0x8]
    cmpeq r0, r1
    bne ov001_021e7740_L448
    ldrb r3, [r7]
    ldrb r2, [r8]
    cmp r3, r2
    bhs ov001_021e7740_L448
    mov r1, r10, lsl #2
    add r0, r5, r10, lsl #2
    ldrh r11, [r5, r1]
    strb r3, [r8]
    ldrh r3, [r0, #2]
    strh r11, [sp, #44]
    ldrh r11, [r4]
    strh r3, [sp, #46]
    ldrh r3, [r4, #2]
    strb r2, [r7]
    ldrh r2, [sp, #44]
    strh r11, [r5, r1]
    strh r3, [r0, #2]
    ldrh r0, [sp, #46]
    strh r2, [r4]
    strh r0, [r4, #2]
ov001_021e7740_L448:
    add r10, r10, #1
    cmp r10, r6
    add r8, r8, #1
    blt ov001_021e7740_L3b0
ov001_021e7740_L458:
    add r9, r9, #1
    cmp r9, r6
    add r7, r7, #1
    blt ov001_021e7740_L398
ov001_021e7740_L468:
    ldr r0, [sp, #0xc]
    add r0, r0, #1
    str r0, [sp, #0xc]
    cmp r0, #6
    blt ov001_021e7740_L380
    mov r0, #0
    str r0, [sp, #0x1c]
    str r0, [sp, #0x18]
    str r0, [sp, #0x14]
    str r0, [sp, #0x10]
    mov r10, r0
    cmp r6, #0
    ble ov001_021e7740_L630
    ldr r11, =0x02238d40
ov001_021e7740_L4a0:
    ldr r0, =0x02238d40
    mov r2, r10, lsl #2
    add r1, r0, r10, lsl #2
    ldrsb r0, [r0, r2]
    ldrsb r1, [r1, #1]
    bl ov001_side_slot_record_021db438
    mov r4, r0
    mov r0, r10
    bl native_fn_021e76b4
    mov r0, r10
    bl native_fn_021e76b4
    bl native_fn_0207afec
    add r1, r4, #512
    ldrsb r1, [r1, #101]
    ldrsb r2, [r0, #38]
    cmp r1, #0
    beq ov001_021e7740_L620
    ldr r0, =0x02238d40
    mov r1, r10, lsl #2
    ldrsb r7, [r0, r1]
    cmp r7, #0
    bne ov001_021e7740_L504
    ldr r0, [sp, #0x14]
    cmp r0, #0
    bne ov001_021e7740_L518
ov001_021e7740_L504:
    cmp r7, #1
    bne ov001_021e7740_L530
    ldr r0, [sp, #0x10]
    cmp r0, #0
    beq ov001_021e7740_L530
ov001_021e7740_L518:
    ldr r1, =0x02238d40
    mov r0, r7
    add r1, r1, r10, lsl #2
    ldrsb r1, [r1, #1]
    bl native_fn_021e865c
    b ov001_021e7740_L620
ov001_021e7740_L530:
    cmp r2, #0
    bne ov001_021e7740_L5fc
    cmp r7, #0
    ldreq r0, [sp, #0x1c]
    cmpeq r0, #0
    beq ov001_021e7740_L5d4
    cmp r7, #1
    ldreq r0, [sp, #0x18]
    cmpeq r0, #0
    beq ov001_021e7740_L5d4
    add r1, sp, #48
    mov r0, r11
    mov r2, #4
    bl native_fn_02008e0c
    sub r8, r10, #1
    ldr r5, =0x02238d40
    mov r1, r8, lsl #2
    ldrsb r2, [sp, #48]
    ldrsb r0, [r5, r1]
    cmp r2, r0
    beq ov001_021e7740_L5bc
    add r9, r5, r1
    mov r4, #4
ov001_021e7740_L58c:
    add r1, r8, #1
    mov r0, r9
    add r1, r5, r1, lsl #2
    mov r2, r4
    bl native_fn_02008e0c
    sub r8, r8, #1
    mov r0, r8, lsl #2
    ldrsb r0, [r5, r0]
    sub r9, r9, #4
    ldrsb r1, [sp, #48]
    cmp r1, r0
    bne ov001_021e7740_L58c
ov001_021e7740_L5bc:
    ldr r2, =0x02238d40
    add r1, r8, #1
    add r1, r2, r1, lsl #2
    add r0, sp, #48
    mov r2, #4
    bl native_fn_02008e0c
ov001_021e7740_L5d4:
    cmp r7, #0
    bne ov001_021e7740_L5ec
    ldr r0, [sp, #0x1c]
    add r0, r0, #1
    str r0, [sp, #0x1c]
    b ov001_021e7740_L620
ov001_021e7740_L5ec:
    ldr r0, [sp, #0x18]
    add r0, r0, #1
    str r0, [sp, #0x18]
    b ov001_021e7740_L620
ov001_021e7740_L5fc:
    ble ov001_021e7740_L620
    cmp r7, #0
    ldrne r0, [sp, #0x10]
    addne r0, r0, #1
    strne r0, [sp, #0x10]
    bne ov001_021e7740_L620
    ldr r0, [sp, #0x14]
    add r0, r0, #1
    str r0, [sp, #0x14]
ov001_021e7740_L620:
    add r10, r10, #1
    cmp r10, r6
    add r11, r11, #4
    blt ov001_021e7740_L4a0
ov001_021e7740_L630:
    mov r0, r6
    add sp, sp, #76
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
