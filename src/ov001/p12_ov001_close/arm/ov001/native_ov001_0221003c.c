/* ov001 row 0x0221003c: 1804 bytes.
 *
 * What it does: 451 instructions; 92 call(s) to 0x0207b674, 0x022100f4, 0x021dc108, +89 more; loops (back edge at +0x24); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: loop with 92 calls (451 instructions, 92 calls, 50 branches, 65 back edges, 0 literal slots).
 *
 *   branch +0x2c -> +0xb8
 *   branch +0x3c -> +0xb8
 *   branch +0x48 -> +0xb8
 *   branch +0x78 -> +0xac
 *   branch +0x88 -> +0xac
 *   branch +0x90 -> +0xac
 *   branch +0xa8 -> +0xb8
 *   back edge +0xb4 -> +0x60
 *   branch +0xdc -> +0xf0
 *   branch +0xec -> +0x134
 *   branch +0xfc -> +0x134
 *   branch +0x110 -> +0x134
 *   branch +0x120 -> +0x134
 *   branch +0x158 -> +0x1a0
 *   branch +0x168 -> +0x1a0
 *   branch +0x17c -> +0x1a0
 *   branch +0x18c -> +0x1a0
 *   branch +0x1b4 -> +0x1e8
 *   branch +0x1c4 -> +0x1e8
 *   branch +0x1d4 -> +0x1e8
 *   branch +0x1fc -> +0x230
 *   branch +0x20c -> +0x230
 *   branch +0x21c -> +0x230
 *   branch +0x244 -> +0x278
 *   branch +0x254 -> +0x278
 *   branch +0x264 -> +0x278
 *   branch +0x28c -> +0x2c0
 *   branch +0x29c -> +0x2c0
 *   branch +0x2ac -> +0x2c0
 *   branch +0x2d4 -> +0x308
 *   branch +0x2e4 -> +0x308
 *   branch +0x2f4 -> +0x308
 *   branch +0x31c -> +0x350
 *   branch +0x32c -> +0x350
 *   branch +0x33c -> +0x350
 *   branch +0x364 -> +0x398
 *   branch +0x374 -> +0x398
 *   branch +0x384 -> +0x398
 *   branch +0x3ac -> +0x3e0
 *   branch +0x3bc -> +0x3e0
 *   branch +0x3cc -> +0x3e0
 *   branch +0x3f4 -> +0x428
 *   branch +0x404 -> +0x428
 *   branch +0x414 -> +0x428
 *   branch +0x43c -> +0x470
 *   branch +0x44c -> +0x470
 *   branch +0x45c -> +0x470
 *   branch +0x484 -> +0x4b8
 *   branch +0x494 -> +0x4b8
 *   branch +0x4a4 -> +0x4b8
 *   branch +0x4cc -> +0x500
 *   branch +0x4dc -> +0x500
 *   branch +0x4ec -> +0x500
 *   branch +0x514 -> +0x548
 *   branch +0x524 -> +0x548
 *   branch +0x534 -> +0x548
 *   branch +0x55c -> +0x598
 *   branch +0x56c -> +0x598
 *   branch +0x584 -> +0x598
 *   branch +0x5ac -> +0x5e8
 *   branch +0x5bc -> +0x5e8
 *   branch +0x5d4 -> +0x5e8
 *   branch +0x5fc -> +0x64c
 *   branch +0x60c -> +0x64c
 *   branch +0x620 -> +0x64c
 *   branch +0x638 -> +0x64c
 *   branch +0x660 -> +0x6b4
 *   branch +0x670 -> +0x6b4
 *   branch +0x688 -> +0x6b4
 *   branch +0x6a0 -> +0x6b4
 *   branch +0x6c8 -> +0x704
 *   branch +0x6d8 -> +0x704
 *   branch +0x6f0 -> +0x704
 *   test +0x28 cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x44 cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x74 cmp r0, #0
 *   test +0x84 cmp r0, #0
 *   test +0x8c cmp r8, #0
 *   test +0xb0 cmp r5, #3
 *   test +0xc0 cmp r0, #0
 *   test +0xd8 cmp r0, #0
 *   test +0xe8 cmp r0, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x10c cmp r0, #0
 *   test +0x11c cmp r0, #2
 *   test +0x124 cmp r6, r8
 *   test +0x13c cmp r0, #0
 *   test +0x154 cmp r0, #0
 *   test +0x164 cmp r0, #0
 *   test +0x178 cmp r0, #0
 *   test +0x188 cmp r0, #2
 *   test +0x190 cmp r6, r8
 *   test +0x1b0 cmp r0, #0
 *   test +0x1c0 cmp r0, #0
 *   test +0x1d0 cmp r0, #1
 *   test +0x1d8 cmp r6, r8
 *   test +0x1f8 cmp r0, #0
 *   test +0x208 cmp r0, #0
 *   test +0x218 cmp r0, #1
 *   test +0x220 cmp r6, r8
 *   test +0x240 cmp r0, #0
 *   test +0x250 cmp r0, #0
 *   test +0x260 cmp r0, #1
 *   test +0x268 cmp r6, r8
 *   test +0x288 cmp r0, #0
 *   test +0x298 cmp r0, #0
 *   test +0x2a8 cmp r0, #1
 *   test +0x2b0 cmp r6, r8
 *   test +0x2d0 cmp r0, #0
 *   test +0x2e0 cmp r0, #0
 *   test +0x2f0 cmp r0, #5
 *   test +0x2f8 cmp r6, r8
 *   test +0x318 cmp r0, #0
 *   test +0x328 cmp r0, #0
 *   test +0x338 cmp r0, #1
 *   test +0x340 cmp r6, r8
 *   test +0x360 cmp r0, #0
 *   test +0x370 cmp r0, #0
 *   test +0x380 cmp r0, #1
 *   test +0x388 cmp r6, r8
 *   test +0x3a8 cmp r0, #0
 *   test +0x3b8 cmp r0, #0
 *   test +0x3c8 cmp r0, #5
 *   test +0x3d0 cmp r6, r8
 *   test +0x3f0 cmp r0, #0
 *   test +0x400 cmp r0, #0
 *   test +0x410 cmp r0, #5
 *   test +0x418 cmp r6, r8
 *   test +0x438 cmp r0, #0
 *   test +0x448 cmp r0, #0
 *   test +0x458 cmp r0, #5
 *   test +0x460 cmp r6, r8
 *   test +0x480 cmp r0, #0
 *   test +0x490 cmp r0, #0
 *   test +0x4a0 cmp r0, #5
 *   test +0x4a8 cmp r6, r8
 *   test +0x4c8 cmp r0, #0
 *   test +0x4d8 cmp r0, #0
 *   test +0x4e8 cmp r0, #5
 *   test +0x4f0 cmp r6, r8
 *   test +0x510 cmp r0, #0
 *   test +0x520 cmp r0, #0
 *   test +0x530 cmp r0, #5
 *   test +0x538 cmp r6, r8
 *   test +0x558 cmp r0, #0
 *   test +0x568 cmp r0, #0
 *   test +0x580 cmp r0, #0
 *   test +0x588 cmp r6, r8
 *   test +0x5a8 cmp r0, #0
 *   test +0x5b8 cmp r0, #0
 *   test +0x5d0 cmp r0, #0
 *   test +0x5d8 cmp r6, r8
 *   test +0x5f8 cmp r0, #0
 *   test +0x608 cmp r0, #0
 *   test +0x634 cmp r0, #0
 *   test +0x63c cmp r6, r8
 *   test +0x65c cmp r0, #0
 *   test +0x66c cmp r0, #0
 *   test +0x684 cmp r0, #1
 *   test +0x69c cmp r0, #0
 *   test +0x6a4 cmp r6, r8
 *   test +0x6c4 cmp r0, #0
 *   test +0x6d4 cmp r0, #0
 *   test +0x6ec cmp r0, #0
 *   test +0x6f4 cmp r6, r8
 *   0 block transfer(s), 22 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221003c; the literal pool and
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

extern void native_fn_0207b674(void);
extern void native_fn_021dc108(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_0207d95c(void);
extern void native_fn_0220ff30(void);
extern void native_fn_0203d294(void);
extern void native_fn_02210ad0(void);
extern void native_fn_02044414(void);


asm u32 native_ov001_0221003c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r10, r0
    ldr r0, [r10, #0x1e8]
    mov r11, r1
    add r1, r0, #70
    mov r0, #43
    mov r9, r2
    mov r8, r3
    mov r6, #0
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_Lb8
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_Lb8
    ldr r0, [r11]
    cmp r0, #0
    bne ov001_0221003c_Lb8
    ldrb r0, [r10, #0x31e]
    mov r5, #0
    cmp r0, #0
    moveq r7, #1
    movne r7, r6
ov001_0221003c_L60:
    mov r0, r7
    mov r1, r5
    bl native_fn_021db438
    mov r4, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221003c_Lac
    add r0, r4, #512
    ldrsb r0, [r0, #52]
    cmp r0, #0
    ble ov001_0221003c_Lac
    cmp r8, #0
    bls ov001_0221003c_Lac
    mov r0, #1
    str r0, [r11]
    mov r0, #43
    strb r0, [r9]
    add r6, r6, #1
    b ov001_0221003c_Lb8
ov001_0221003c_Lac:
    add r5, r5, #1
    cmp r5, #3
    blt ov001_0221003c_L60
ov001_0221003c_Lb8:
    ldrb r0, [r10, #0x31e]
    ldr r1, [r10, #0x1e8]
    cmp r0, #0
    moveq r4, #1
    mov r0, #87
    add r1, r1, #70
    movne r4, #0
    bl native_fn_0207b674
    cmp r0, #0
    bgt ov001_0221003c_Lf0
    ldrb r0, [r10, #0x1fd]
    bl native_fn_0207d95c
    cmp r0, #0
    beq ov001_0221003c_L134
ov001_0221003c_Lf0:
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L134
    mov r0, r4
    mov r1, #4
    bl native_fn_0220ff30
    cmp r0, #0
    beq ov001_0221003c_L134
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #2
    bge ov001_0221003c_L134
    cmp r6, r8
    movlo r0, #87
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L134:
    ldrb r0, [r10, #0x31e]
    ldr r1, [r10, #0x1e8]
    cmp r0, #0
    moveq r4, #0
    mov r0, #88
    add r1, r1, #70
    movne r4, #1
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L1a0
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L1a0
    mov r0, r4
    mov r1, #1
    bl native_fn_0220ff30
    cmp r0, #0
    beq ov001_0221003c_L1a0
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #2
    bge ov001_0221003c_L1a0
    cmp r6, r8
    movlo r0, #88
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L1a0:
    ldr r1, [r10, #0x1e8]
    mov r0, #57
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L1e8
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L1e8
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0221003c_L1e8
    cmp r6, r8
    movlo r0, #57
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L1e8:
    ldr r1, [r10, #0x1e8]
    mov r0, #243
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L230
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L230
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0221003c_L230
    cmp r6, r8
    movlo r0, #243
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L230:
    ldr r1, [r10, #0x1e8]
    mov r0, #244
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L278
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L278
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0221003c_L278
    cmp r6, r8
    movlo r0, #244
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L278:
    ldr r1, [r10, #0x1e8]
    mov r0, #245
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L2c0
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L2c0
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0221003c_L2c0
    cmp r6, r8
    movlo r0, #245
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L2c0:
    ldr r1, [r10, #0x1e8]
    mov r0, #195
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L308
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L308
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L308
    cmp r6, r8
    movlo r0, #195
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L308:
    ldr r1, [r10, #0x1e8]
    mov r0, #191
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L350
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L350
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0221003c_L350
    cmp r6, r8
    movlo r0, #191
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L350:
    ldr r1, [r10, #0x1e8]
    mov r0, #246
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L398
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L398
    mov r0, #10
    bl native_fn_0203d294
    cmp r0, #1
    bge ov001_0221003c_L398
    cmp r6, r8
    movlo r0, #246
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L398:
    ldr r1, [r10, #0x1e8]
    mov r0, #194
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L3e0
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L3e0
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L3e0
    cmp r6, r8
    movlo r0, #194
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L3e0:
    ldr r1, [r10, #0x1e8]
    mov r0, #247
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L428
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L428
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L428
    cmp r6, r8
    movlo r0, #247
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L428:
    ldr r1, [r10, #0x1e8]
    mov r0, #248
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L470
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L470
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L470
    cmp r6, r8
    movlo r0, #248
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L470:
    ldr r1, [r10, #0x1e8]
    mov r0, #249
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L4b8
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L4b8
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L4b8
    cmp r6, r8
    movlo r0, #249
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L4b8:
    ldr r1, [r10, #0x1e8]
    mov r0, #193
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L500
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L500
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L500
    cmp r6, r8
    movlo r0, #193
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L500:
    ldr r1, [r10, #0x1e8]
    mov r0, #196
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L548
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L548
    mov r0, #100
    bl native_fn_0203d294
    cmp r0, #5
    bge ov001_0221003c_L548
    cmp r6, r8
    movlo r0, #196
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L548:
    ldr r1, [r10, #0x1e8]
    mov r0, #192
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L598
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L598
    mov r0, r10
    mov r1, #100
    mov r2, #10
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0221003c_L598
    cmp r6, r8
    movlo r0, #192
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L598:
    ldr r1, [r10, #0x1e8]
    mov r0, #73
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L5e8
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L5e8
    mov r0, r10
    mov r1, #10
    mov r2, #1
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0221003c_L5e8
    cmp r6, r8
    movlo r0, #73
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L5e8:
    ldr r1, [r10, #0x1e8]
    mov r0, #38
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L64c
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L64c
    bl native_fn_02044414
    mov r1, r0, lsr #31
    rsb r0, r1, r0, lsl #31
    adds r0, r1, r0, ror #31
    bne ov001_0221003c_L64c
    mov r0, r10
    mov r1, #10
    mov r2, #2
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0221003c_L64c
    cmp r6, r8
    movlo r0, #38
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L64c:
    ldr r1, [r10, #0x1e8]
    mov r0, #71
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L6b4
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L6b4
    bl native_fn_02044414
    mov r1, r0, lsr #31
    rsb r0, r1, r0, lsl #31
    add r0, r1, r0, ror #31
    cmp r0, #1
    bne ov001_0221003c_L6b4
    mov r0, r10
    mov r1, #10
    mov r2, #2
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0221003c_L6b4
    cmp r6, r8
    movlo r0, #71
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L6b4:
    ldr r1, [r10, #0x1e8]
    mov r0, #50
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_0221003c_L704
    mov r0, r10
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_0221003c_L704
    mov r0, r10
    mov r1, #10
    mov r2, #2
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_0221003c_L704
    cmp r6, r8
    movlo r0, #50
    strlob r0, [r9, r6]
    addlo r6, r6, #1
ov001_0221003c_L704:
    and r0, r6, #255
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
