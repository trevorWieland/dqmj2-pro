/* ov001 row 0x021eb200: 1916 bytes.
 *
 * What it does: 476 instructions; 62 call(s) to 0x0207afec, 0x021eab48, 0x021e9a60, +59 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 62 calls (476 instructions, 62 calls, 51 branches, 41 back edges, 3 literal slots).
 *
 *   pool +0x770 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x774 -> constant 0x02238e14 (image word 0x02238e14)
 *   pool +0x778 -> constant 0x02238e44 (image word 0x02238e44)
 *   branch +0x28 -> +0x124
 *   branch +0x60 -> +0x74
 *   branch +0x80 -> +0x8c
 *   branch +0xbc -> +0xcc
 *   branch +0xe4 -> +0x114
 *   branch +0x120 -> +0x148
 *   branch +0x128 -> +0x148
 *   branch +0x134 -> +0x13c
 *   branch +0x154 -> +0x3f0
 *   branch +0x190 -> +0x1a0
 *   branch +0x1a4 -> +0x2bc
 *   branch +0x1c8 -> +0x1d8
 *   branch +0x20c -> +0x24c
 *   branch +0x21c -> +0x24c
 *   branch +0x228 -> +0x24c
 *   branch +0x268 -> +0x2a4
 *   branch +0x274 -> +0x284
 *   branch +0x2d0 -> +0x3f0
 *   branch +0x31c -> +0x350
 *   branch +0x33c -> +0x3c0
 *   branch +0x34c -> +0x3c0
 *   branch +0x380 -> +0x3a0
 *   branch +0x3b0 -> +0x3c0
 *   branch +0x3d8 -> +0x3f0
 *   branch +0x3fc -> +0x418
 *   branch +0x414 -> +0x4e8
 *   branch +0x41c -> +0x4e8
 *   branch +0x480 -> +0x498
 *   branch +0x494 -> +0x4bc
 *   branch +0x4ac -> +0x4bc
 *   branch +0x4cc -> +0x4dc
 *   branch +0x4f4 -> +0x508
 *   branch +0x514 -> +0x548
 *   branch +0x52c -> +0x548
 *   branch +0x540 -> +0x548
 *   branch +0x554 -> +0x584
 *   branch +0x574 -> +0x584
 *   branch +0x590 -> +0x5c8
 *   branch +0x5a4 -> +0x5c8
 *   branch +0x5d4 -> +0x618
 *   branch +0x5e8 -> +0x604
 *   branch +0x600 -> +0x618
 *   branch +0x624 -> +0x65c
 *   branch +0x63c -> +0x680
 *   branch +0x650 -> +0x680
 *   branch +0x658 -> +0x680
 *   branch +0x660 -> +0x680
 *   branch +0x68c -> +0x764
 *   branch +0x698 -> +0x764
 *   branch +0x6a4 -> +0x6ac
 *   branch +0x6c0 -> +0x6e4
 *   branch +0x700 -> +0x70c
 *   branch +0x714 -> +0x71c
 *   branch +0x724 -> +0x72c
 *   branch +0x740 -> +0x750
 *   test +0x24 cmp r1, #0
 *   test +0x54 cmp r0, #0
 *   test +0x7c cmp r0, #0
 *   test +0x94 cmp r1, #0
 *   test +0xb8 cmp r0, #0
 *   test +0xe0 cmp r2, r1
 *   test +0x124 cmp r1, #5
 *   test +0x130 cmp r0, #0
 *   test +0x150 cmp r0, #10
 *   test +0x180 cmp r3, r2
 *   test +0x1a0 cmp r4, r0
 *   test +0x1c4 cmp r0, #0
 *   test +0x208 cmp r0, #0
 *   test +0x218 cmp r1, #119
 *   test +0x224 cmp r0, #0
 *   test +0x25c cmp r0, #180
 *   test +0x264 cmpeq r0, #0
 *   test +0x270 cmp r0, #0
 *   test +0x2cc cmp r4, r1
 *   test +0x2d8 cmp r1, #0
 *   test +0x318 tst r2, #2
 *   test +0x338 cmp r0, #0
 *   test +0x354 cmp r0, #0
 *   test +0x37c cmp r1, #0
 *   test +0x3ac cmp r0, #0
 *   test +0x3d4 cmp r0, #0
 *   test +0x3f8 cmp r0, #200
 *   test +0x418 cmp r0, #210
 *   test +0x47c tst r2, #2
 *   test +0x49c cmp r0, #0
 *   test +0x4c8 cmp r0, #0
 *   test +0x4f0 cmp r1, #20
 *   test +0x510 cmp r1, #25
 *   test +0x528 cmp r1, #30
 *   test +0x53c cmp r0, #0
 *   test +0x550 cmp r1, #30
 *   test +0x564 cmp r0, #0
 *   test +0x58c cmp r1, #40
 *   test +0x5a0 cmp r0, #0
 *   test +0x5d0 cmp r1, #50
 *   test +0x5dc cmp r1, #0
 *   test +0x5f0 cmp r1, #30
 *   test +0x608 cmp r1, #30
 *   test +0x620 cmp r1, #60
 *   test +0x638 cmp r1, #30
 *   test +0x64c cmp r0, #0
 *   test +0x65c cmp r1, #70
 *   test +0x670 cmp r0, #0
 *   test +0x688 cmp r0, #100
 *   test +0x694 cmp r0, #0
 *   test +0x6a0 cmp r0, #0
 *   test +0x6bc cmp r0, #0
 *   test +0x6fc cmp r0, #0
 *   test +0x710 cmp r0, #0
 *   test +0x720 cmp r0, #0
 *   test +0x73c cmp r1, #0
 *   0 block transfer(s), 51 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eb200; the literal pool and
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
extern void native_fn_021eab48(void);
extern void native_fn_021e9a60(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_0207b674(void);
extern void native_fn_021d9534(void);
extern void native_fn_021d9494(void);
extern void native_fn_0205c904(void);
extern void native_fn_021e9b84(void);
extern void native_fn_021eb024(void);
extern void native_fn_021e9de0(void);
extern void native_fn_0205d790(void);
extern void native_fn_021e9cd8(void);
extern void native_fn_021f14e4(void);
extern void native_fn_021eaa88(void);
extern void native_fn_021eab0c(void);
extern void native_fn_021dc9d4(void);
extern void native_fn_0220f600(void);
extern void native_fn_021e2390(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021ea398(void);
extern void native_fn_021ea428(void);
extern void native_fn_021e19c8(void);
extern void native_fn_021d7e80(void);
extern void native_fn_0220f530(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021dbb14(void);
extern void native_fn_021dbb9c(void);
extern void native_fn_022168e8(void);
extern void native_fn_021e9d70(void);
extern void native_fn_021eab34(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021dc5d4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_021dc940(void);


asm u32 native_ov001_021eb200 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, lr}
    sub sp, sp, #12
    ldr r0, =0x02238d7c
    ldrh r0, [r0, #54]
    bl native_fn_0207afec
    mov r5, r0
    bl native_fn_021eab48
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #0
    bne ov001_021eb200_L124
    ldrb r0, [r0, #0xa]
    bl native_fn_021e9a60
    ldr r1, =0x02238d7c
    mov r2, #0
    str r2, [r1, #0x40]
    str r2, [r1, #0x5c]
    ldr r0, =0x02238e14
    str r2, [r1, #0x44]
    bl native_fn_0202ac08
    ldrsh r0, [r5, #12]
    cmp r0, #0
    ldreq r0, =0x02238d7c
    moveq r1, #10
    beq ov001_021eb200_L74
    mov r1, #0
    bl native_fn_021eea10
    ldr r0, =0x02238d7c
    mov r1, #5
ov001_021eb200_L74:
    strb r1, [r0, #0xd]
    ldrsh r0, [r5, #14]
    cmp r0, #0
    beq ov001_021eb200_L8c
    mov r1, #0
    bl native_fn_021eea10
ov001_021eb200_L8c:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x19]
    cmp r1, #0
    movne r1, #200
    strneb r1, [r0, #0xd]
    ldr r1, =0x02238d7c
    mov r0, #48
    ldr r1, [r1, #0x54]
    ldr r1, [r1, #0x1e8]
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_021eb200_Lcc
    mov r0, #180
    mov r1, #0
    bl native_fn_021eea10
ov001_021eb200_Lcc:
    ldr r1, =0x02238d7c
    ldr r0, [r1, #0x60]
    ldr r2, [r1, #0x54]
    ldrb r1, [r0, #0x31e]
    ldrb r2, [r2, #0x31e]
    cmp r2, r1
    bne ov001_021eb200_L114
    mov r1, #1
    mov r2, r1
    mov r3, #0
    bl native_fn_021d9534
    mov r1, #0
    ldr r2, =0x02238d7c
    sub r0, r0, #5
    str r0, [r2, #0x3c]
    ldr r0, [r2, #0x60]
    mov r2, r1
    bl native_fn_021d9494
ov001_021eb200_L114:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x19]
    strb r1, [r0, #0x1f]
    b ov001_021eb200_L148
ov001_021eb200_L124:
    cmp r1, #5
    bne ov001_021eb200_L148
    ldrsh r0, [r5, #10]
    cmp r0, #0
    beq ov001_021eb200_L13c
    bl native_fn_0205c904
ov001_021eb200_L13c:
    ldr r0, =0x02238d7c
    mov r1, #10
    strb r1, [r0, #0xd]
ov001_021eb200_L148:
    ldr r2, =0x02238d7c
    ldrb r0, [r2, #0xd]
    cmp r0, #10
    bne ov001_021eb200_L3f0
    mov r1, #1
    ldr r0, [r2, #0x60]
    ldr r3, [r2, #0x5c]
    mov r2, r1
    bl native_fn_021d9534
    ldr r1, =0x02238d7c
    ldr r6, [r1, #0x60]
    ldr r2, [r1, #0x54]
    ldrb r3, [r6, #0x31e]
    ldrb r2, [r2, #0x31e]
    cmp r3, r2
    ldreq r4, [r1, #0x3c]
    addeq r2, r4, #1
    streq r2, [r1, #0x3c]
    beq ov001_021eb200_L1a0
    ldr r1, [r6, #0x60]
    ldr r1, [r1]
    mov r4, r1, asr #12
ov001_021eb200_L1a0:
    cmp r4, r0
    bne ov001_021eb200_L2bc
    ldr r1, =0x02238d7c
    mov r0, r6
    ldrh r1, [r1, #54]
    bl native_fn_021e9b84
    ldr r1, =0x02238d7c
    strb r0, [r1, #0x18]
    ldr r0, [r1, #0x40]
    cmp r0, #0
    bne ov001_021eb200_L1d8
    ldr r1, [r1, #0x54]
    mov r0, r5
    bl native_fn_021eb024
ov001_021eb200_L1d8:
    mov r0, #100
    str r0, [sp]
    mov r0, #1
    ldr r1, =0x02238d7c
    str r0, [sp, #0x4]
    ldrb r0, [r1, #0x1d]
    str r0, [sp, #0x8]
    ldrh r2, [r1, #54]
    ldrb r3, [r1, #0x18]
    ldr r0, [r1, #0x60]
    ldr r1, [r1, #0x54]
    bl native_fn_021e9de0
    cmp r0, #0
    beq ov001_021eb200_L24c
    ldr r0, =0x02238d7c
    ldrh r1, [r0, #54]
    cmp r1, #119
    bne ov001_021eb200_L24c
    ldrb r0, [r0, #0x18]
    cmp r0, #0
    beq ov001_021eb200_L24c
    ldrsh r6, [r5, #14]
    mov r0, r6
    bl native_fn_0205d790
    ldr r1, =0x02238d7c
    mov r2, r0
    ldr r1, [r1, #0x54]
    mov r0, r6
    bl native_fn_021e9cd8
ov001_021eb200_L24c:
    ldr r1, =0x02238d7c
    ldr r0, [r1, #0x54]
    add r0, r0, #768
    ldrh r0, [r0, #76]
    cmp r0, #180
    ldreq r0, [r1, #0x44]
    cmpeq r0, #0
    bne ov001_021eb200_L2a4
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb200_L284
    ldr r0, =0x02238d7c
    ldrh r0, [r0, #54]
    bl native_fn_021eaa88
ov001_021eb200_L284:
    mov r0, #11
    mov r1, #0
    mov r2, #48
    mov r3, #2
    bl native_fn_021eab0c
    ldr r0, =0x02238d7c
    mov r1, #1
    str r1, [r0, #0x44]
ov001_021eb200_L2a4:
    ldr r0, =0x02238d7c
    add r1, r4, #1
    str r1, [r0, #0x5c]
    ldr r1, [r0, #0x40]
    add r1, r1, #1
    str r1, [r0, #0x40]
ov001_021eb200_L2bc:
    ldr r2, =0x02238d7c
    ldr r0, [r2, #0x60]
    add r1, r0, #768
    ldrh r1, [r1, #70]
    cmp r4, r1
    blt ov001_021eb200_L3f0
    ldrsb r1, [r2, #11]
    cmp r1, #0
    movgt r1, #1
    movle r1, #0
    strb r1, [r2, #0x19]
    bl native_fn_021dc9d4
    mov r2, #1
    ldr r1, =0x02238d7c
    str r2, [sp]
    mov r3, r0
    ldrh r2, [r1, #54]
    ldr r0, [r1, #0x60]
    ldr r1, [r1, #0x54]
    bl native_fn_0220f600
    ldr r1, =0x02238d7c
    ldr r0, [r1, #0x54]
    ldr r2, [r0, #0x33c]
    tst r2, #2
    beq ov001_021eb200_L350
    mov r0, #60
    strb r0, [r1, #0xd]
    mov r0, #0
    strb r0, [r1, #0xc]
    ldr r0, [r1, #0x60]
    bl native_fn_021dc9d4
    cmp r0, #0
    beq ov001_021eb200_L3c0
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl native_fn_021e2390
    b ov001_021eb200_L3c0
ov001_021eb200_L350:
    bl native_fn_021dbd24
    cmp r0, #0
    ldrle r0, =0x02238d7c
    movle r1, #20
    ldrgt r0, =0x02238d7c
    movgt r1, #50
    strb r1, [r0, #0xd]
    ldr r0, =0x02238d7c
    mov r1, #0
    strb r1, [r0, #0xc]
    ldrb r1, [r0, #0x19]
    cmp r1, #0
    beq ov001_021eb200_L3a0
    ldr r0, [r0, #0x54]
    mov r1, #249
    bl native_fn_021ea398
    ldr r0, =0x02238d7c
    mov r1, #176
    ldr r0, [r0, #0x54]
    bl native_fn_021ea398
ov001_021eb200_L3a0:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_021dc9d4
    cmp r0, #0
    beq ov001_021eb200_L3c0
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl native_fn_021e2390
ov001_021eb200_L3c0:
    ldr r0, =0x02238d7c
    ldrh r1, [r0, #54]
    ldr r0, [r0, #0x54]
    bl native_fn_021ea428
    bl native_fn_021e19c8
    cmp r0, #0
    beq ov001_021eb200_L3f0
    ldr r0, =0x02238d7c
    ldr r1, [r0, #0x54]
    ldr r0, [r1, #0x33c]
    bic r0, r0, #536
    str r0, [r1, #0x33c]
ov001_021eb200_L3f0:
    ldr r1, =0x02238d7c
    ldrb r0, [r1, #0xd]
    cmp r0, #200
    bne ov001_021eb200_L418
    ldr r0, [r1, #0x54]
    bl native_fn_021d7e80
    ldr r0, =0x02238d7c
    mov r1, #210
    strb r1, [r0, #0xd]
    b ov001_021eb200_L4e8
ov001_021eb200_L418:
    cmp r0, #210
    bne ov001_021eb200_L4e8
    mov r0, #100
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r3, #0
    str r3, [sp, #0x8]
    ldrh r2, [r1, #54]
    ldr r0, [r1, #0x60]
    ldr r1, [r1, #0x54]
    bl native_fn_021e9de0
    ldr r0, =0x02238d7c
    mov r1, #0
    strb r1, [r0, #0x19]
    ldr r0, [r0, #0x54]
    mov r1, #1
    bl native_fn_0220f530
    ldr r0, =0x02238d7c
    ldrh r1, [r0, #54]
    ldr r0, [r0, #0x54]
    bl native_fn_021ea428
    ldr r1, =0x02238d7c
    ldr r0, [r1, #0x54]
    ldr r2, [r0, #0x33c]
    tst r2, #2
    beq ov001_021eb200_L498
    mov r0, #60
    strb r0, [r1, #0xd]
    mov r0, #0
    strb r0, [r1, #0xc]
    b ov001_021eb200_L4bc
ov001_021eb200_L498:
    bl native_fn_021dbd24
    cmp r0, #0
    ldrgt r0, =0x02238d7c
    movgt r1, #50
    strgtb r1, [r0, #0xd]
    bgt ov001_021eb200_L4bc
    ldr r0, =0x02238d7c
    mov r1, #20
    strb r1, [r0, #0xd]
ov001_021eb200_L4bc:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    bl native_fn_021dc9d4
    cmp r0, #0
    beq ov001_021eb200_L4dc
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl native_fn_021e2390
ov001_021eb200_L4dc:
    ldr r0, =0x02238d7c
    mov r1, #0
    strb r1, [r0, #0xc]
ov001_021eb200_L4e8:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #20
    bne ov001_021eb200_L508
    mov r1, #0
    strb r1, [r0, #0xc]
    mov r1, #25
    strb r1, [r0, #0xd]
ov001_021eb200_L508:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #25
    bne ov001_021eb200_L548
    ldrb r1, [r0, #0xc]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0xc]
    cmp r1, #30
    bls ov001_021eb200_L548
    mov r1, #30
    strb r1, [r0, #0xd]
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb200_L548
    bl ov001_clear_state_flag4_021f14a4
ov001_021eb200_L548:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #30
    bne ov001_021eb200_L584
    ldr r0, [r0, #0x54]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb14
    cmp r0, #0
    ldreq r0, =0x02238d7c
    moveq r1, #50
    streqb r1, [r0, #0xd]
    beq ov001_021eb200_L584
    ldr r0, =0x02238d7c
    mov r1, #40
    strb r1, [r0, #0xd]
ov001_021eb200_L584:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #40
    bne ov001_021eb200_L5c8
    ldr r0, [r0, #0x54]
    ldrb r1, [r0, #0x31e]
    bl native_fn_021dbb9c
    cmp r0, #0
    beq ov001_021eb200_L5c8
    ldr r0, =0x02238d7c
    ldr r2, =0x02238e44
    ldr r1, [r0, #0x54]
    mov r4, #1
    ldrb r3, [r1, #0x31f]
    mov r1, #100
    strb r4, [r2, r3]
    strb r1, [r0, #0xd]
ov001_021eb200_L5c8:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #50
    bne ov001_021eb200_L618
    ldrb r1, [r0, #0x19]
    cmp r1, #0
    ldrb r1, [r0, #0xc]
    add r2, r1, #1
    bne ov001_021eb200_L604
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0xc]
    movhs r1, #100
    strhsb r1, [r0, #0xd]
    b ov001_021eb200_L618
ov001_021eb200_L604:
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0xc]
    movhs r1, #100
    strhsb r1, [r0, #0xd]
ov001_021eb200_L618:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0xd]
    cmp r1, #60
    bne ov001_021eb200_L65c
    ldrb r1, [r0, #0xc]
    add r2, r1, #1
    and r1, r2, #255
    strb r2, [r0, #0xc]
    cmp r1, #30
    bls ov001_021eb200_L680
    mov r1, #70
    strb r1, [r0, #0xd]
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb200_L680
    bl ov001_clear_state_flag4_021f14a4
    b ov001_021eb200_L680
ov001_021eb200_L65c:
    cmp r1, #70
    bne ov001_021eb200_L680
    ldr r0, [r0, #0x54]
    ldrb r1, [r0, #0x31e]
    bl native_fn_022168e8
    cmp r0, #0
    ldrne r0, =0x02238d7c
    movne r1, #100
    strneb r1, [r0, #0xd]
ov001_021eb200_L680:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0xd]
    cmp r0, #100
    bne ov001_021eb200_L764
    bl native_fn_021e9d70
    cmp r0, #0
    beq ov001_021eb200_L764
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb200_L6ac
    bl ov001_clear_state_flag4_021f14a4
ov001_021eb200_L6ac:
    bl native_fn_021eab34
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021eb200_L6e4
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    bl native_fn_021dc5d4
    ldr r0, =0x02238d7c
    mov r1, #0
    ldr r0, [r0, #0x54]
    add r0, r0, #768
    strh r1, [r0, #76]
ov001_021eb200_L6e4:
    ldr r1, =0x02238d7c
    mov r0, #48
    ldr r1, [r1, #0x54]
    ldr r1, [r1, #0x1e8]
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_021eb200_L70c
    mov r0, #180
    bl native_fn_021eeb70
ov001_021eb200_L70c:
    ldrsh r0, [r5, #12]
    cmp r0, #0
    beq ov001_021eb200_L71c
    bl native_fn_021eeb70
ov001_021eb200_L71c:
    ldrsh r0, [r5, #14]
    cmp r0, #0
    beq ov001_021eb200_L72c
    bl native_fn_021eeb70
ov001_021eb200_L72c:
    ldr r0, =0x02238e14
    bl native_fn_0202ac4c
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x1f]
    cmp r1, #0
    bne ov001_021eb200_L750
    ldr r0, [r0, #0x60]
    mov r1, #8
    bl native_fn_021dc940
ov001_021eb200_L750:
    ldr r0, =0x02238d7c
    mov r1, #12
    strb r1, [r0, #0x13]
    mov r1, #0
    strb r1, [r0, #0xd]
ov001_021eb200_L764:
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, pc}
}
