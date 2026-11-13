/* ov001 row 0x021f521c: 1428 bytes.
 *
 * What it does: 354 instructions; 32 call(s) to 0x0207afec, 0x021db438, 0x021f531c, +29 more; loops (back edge at +0x54); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 32 calls (354 instructions, 32 calls, 37 branches, 25 back edges, 3 literal slots).
 *
 *   pool +0x588 -> constant 0x0223989c (image word 0x0223989c)
 *   pool +0x58c -> constant 0x0223995c (image word 0x0223995c)
 *   pool +0x590 -> constant 0x022399b8 (image word 0x022399b8)
 *   branch +0x60 -> +0xa8
 *   branch +0x84 -> +0x94
 *   branch +0xa4 -> +0xac
 *   branch +0xb8 -> +0x100
 *   branch +0xd4 -> +0xf0
 *   back edge +0xfc -> +0xc8
 *   branch +0x118 -> +0x47c
 *   branch +0x128 -> +0x464
 *   branch +0x1b4 -> +0x378
 *   branch +0x1e8 -> +0x2cc
 *   branch +0x1f0 -> +0x230
 *   branch +0x1fc -> +0x228
 *   back edge +0x224 -> +0x204
 *   branch +0x22c -> +0x240
 *   branch +0x258 -> +0x274
 *   branch +0x29c -> +0x2b4
 *   branch +0x2a4 -> +0x2e8
 *   branch +0x2b0 -> +0x2e8
 *   branch +0x2c8 -> +0x2e8
 *   branch +0x2d4 -> +0x2e8
 *   branch +0x2f0 -> +0x458
 *   branch +0x300 -> +0x314
 *   branch +0x310 -> +0x320
 *   branch +0x31c -> +0x35c
 *   branch +0x358 -> +0x364
 *   branch +0x374 -> +0x458
 *   branch +0x380 -> +0x394
 *   branch +0x39c -> +0x404
 *   branch +0x3ac -> +0x3bc
 *   branch +0x3b8 -> +0x3f8
 *   branch +0x3f4 -> +0x41c
 *   branch +0x400 -> +0x41c
 *   branch +0x408 -> +0x41c
 *   branch +0x428 -> +0x458
 *   back edge +0x478 -> +0x11c
 *   branch +0x48c -> +0x4fc
 *   branch +0x4b0 -> +0x4ec
 *   branch +0x4c0 -> +0x4ec
 *   branch +0x4cc -> +0x4ec
 *   back edge +0x4f8 -> +0x4a4
 *   branch +0x504 -> +0x53c
 *   branch +0x518 -> +0x534
 *   branch +0x524 -> +0x534
 *   branch +0x544 -> +0x554
 *   branch +0x564 -> +0x578
 *   test +0x5c cmp r9, #0
 *   test +0x74 cmpne r0, #2
 *   test +0x7c cmp r1, #0
 *   test +0x88 cmp r0, #0
 *   test +0xb0 cmp r4, #0
 *   test +0xd0 cmp r0, #0
 *   test +0xf4 cmp r6, r4
 *   test +0x114 cmp r4, #0
 *   test +0x124 cmp r0, #0
 *   test +0x1b0 cmp r0, #0
 *   test +0x1c8 cmp r2, r1
 *   test +0x1d4 cmpeq r2, r1
 *   test +0x1e4 cmp r1, #0
 *   test +0x1ec cmp r8, #170
 *   test +0x1f4 cmp r0, #0
 *   test +0x220 cmp r7, r0
 *   test +0x244 cmp r0, #0
 *   test +0x250 cmpne r1, r0
 *   test +0x254 cmpne r6, #0
 *   test +0x298 cmp r0, #1
 *   test +0x2a0 cmp r6, #0
 *   test +0x2d0 cmp r0, #0
 *   test +0x2ec cmp r0, #0
 *   test +0x2fc cmp r0, #0
 *   test +0x30c cmp r0, #0
 *   test +0x318 cmp r0, #0
 *   test +0x37c cmp r3, #0
 *   test +0x398 cmp r0, #0
 *   test +0x3a8 cmp r0, #0
 *   test +0x3b4 cmp r0, #0
 *   test +0x404 cmp r3, #0
 *   test +0x424 cmp r0, #0
 *   test +0x474 cmp r0, r4
 *   test +0x47c cmp r4, #0
 *   test +0x488 cmpgt r4, #0
 *   test +0x4ac cmp r0, #0
 *   test +0x4bc cmp r0, #0
 *   test +0x4c8 cmp r0, #0
 *   test +0x4f0 cmp r10, r4
 *   test +0x500 cmp r0, #0
 *   test +0x510 cmp r0, #6
 *   test +0x51c cmp r0, #10
 *   test +0x528 cmp r0, #9
 *   test +0x540 cmp r0, #0
 *   test +0x55c cmp r0, #0
 *   0 block transfer(s), 51 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f521c; the literal pool and
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
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f2304(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021f4fa4(void);
extern void native_fn_021e1950(void);
extern void native_fn_021f5078(void);
extern void native_fn_021d9494(void);
extern void native_fn_021e2078(void);
extern void native_fn_021e24f8(void);
extern void native_fn_021dc108(void);
extern void native_fn_0205d790(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_021dc5d4(void);
extern void native_fn_021ee7b0(void);
extern void native_fn_021f949c(void);


asm u32 native_ov001_021f521c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #116
    mov r10, r0
    ldr r0, [sp, #0x98]
    mov r6, #0
    add r5, sp, #92
    add r4, sp, #80
    str r0, [sp, #0x98]
    mov r8, r2
    mov r9, r1
    ldr r1, [sp, #0x98]
    mov r0, r8
    str r6, [sp, #0x4c]
    str r6, [r5]
    str r6, [r5, #0x4]
    str r6, [r5, #0x8]
    str r6, [r4]
    str r6, [r4, #0x4]
    str r6, [r4, #0x8]
    str r3, [sp, #0x1c]
    str r6, [r1]
    bl native_fn_0207afec
    str r0, [sp, #0x28]
    cmp r9, #0
    bne ov001_021f521c_La8
    ldrh r0, [r0, #8]
    mov r1, #1
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    cmpne r0, #2
    movne r1, r6
    cmp r1, #0
    ldrb r0, [r10, #0x31e]
    bne ov001_021f521c_L94
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
ov001_021f521c_L94:
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r9, r0
    mov r4, #3
    b ov001_021f521c_Lac
ov001_021f521c_La8:
    mov r4, #1
ov001_021f521c_Lac:
    str r9, [sp, #0x24]
    cmp r4, #0
    mov r6, #0
    ble ov001_021f521c_L100
    ldr r11, =0x0223989c
    mov r7, r9
    add r5, sp, #104
ov001_021f521c_Lc8:
    mov r0, r7
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f521c_Lf0
    ldrb r2, [r11, #0x10]
    mov r0, r7
    mov r1, r8
    bl native_fn_021f2304
    ldrb r1, [r7, #0x31f]
    str r0, [r5, r1, lsl #2]
ov001_021f521c_Lf0:
    add r6, r6, #1
    cmp r6, r4
    add r7, r7, #1088
    blt ov001_021f521c_Lc8
ov001_021f521c_L100:
    mov r0, #0
    str r0, [sp, #0x2c]
    str r0, [sp, #0x34]
    str r0, [sp, #0x30]
    str r0, [sp, #0x20]
    cmp r4, #0
    ble ov001_021f521c_L47c
ov001_021f521c_L11c:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f521c_L464
    ldrb r2, [r9, #0x31f]
    add r1, sp, #104
    ldrb r0, [r9, #0x31e]
    ldr r1, [r1, r2, lsl #2]
    bl ov001_side_slot_record_021db438
    mov r5, r0
    mov r0, #0
    str r0, [sp, #0x4c]
    add r1, sp, #76
    str r1, [sp]
    add r0, sp, #56
    str r0, [sp, #0x4]
    add r1, sp, #72
    str r1, [sp, #0x8]
    add r0, r5, #844
    str r0, [sp, #0xc]
    add r1, sp, #64
    str r1, [sp, #0x10]
    add r0, sp, #68
    str r0, [sp, #0x14]
    add r1, sp, #60
    str r1, [sp, #0x18]
    ldr r3, =0x0223989c
    mov r0, r8
    ldrb r3, [r3, #0x10]
    mov r1, r10
    mov r2, r5
    bl native_fn_021e1a60
    mov r0, r10
    mov r1, r5
    mov r2, r8
    bl native_fn_021f4fa4
    str r0, [sp, #0x4c]
    cmp r0, #0
    beq ov001_021f521c_L378
    ldr r1, =0x0223989c
    ldrb r2, [r9, #0x31f]
    ldr r3, [r1, #0x78]
    ldrb r1, [r3, #0x31f]
    cmp r2, r1
    ldreqb r1, [r3, #0x31e]
    ldreqb r2, [r9, #0x31e]
    cmpeq r2, r1
    moveq r6, #1
    ldr r1, [sp, #0x44]
    movne r6, #0
    cmp r1, #0
    beq ov001_021f521c_L2cc
    cmp r8, #170
    beq ov001_021f521c_L230
    cmp r0, #0
    mov r7, #0
    ble ov001_021f521c_L228
    mov r11, #1
ov001_021f521c_L204:
    mov r0, r8
    mov r1, r5
    mov r2, r11
    mov r3, r6
    bl native_fn_021e1950
    add r7, r7, #1
    ldr r0, [sp, #0x4c]
    cmp r7, r0
    blt ov001_021f521c_L204
ov001_021f521c_L228:
    mov r6, #1
    b ov001_021f521c_L240
ov001_021f521c_L230:
    mov r0, r10
    mov r1, r9
    bl native_fn_021f5078
    mov r6, r0
ov001_021f521c_L240:
    ldr r0, [sp, #0x1c]
    cmp r0, #0
    ldrneb r1, [r10, #0x31e]
    ldrneb r0, [r5, #0x31e]
    cmpne r1, r0
    cmpne r6, #0
    beq ov001_021f521c_L274
    mov r0, r5
    mov r1, #4
    mov r2, #0
    bl native_fn_021d9494
    mov r0, #1
    str r0, [sp, #0x34]
ov001_021f521c_L274:
    ldrb r2, [r5, #0x31f]
    mov r3, #1
    add r1, sp, #92
    mov r0, r8
    str r3, [r1, r2, lsl #2]
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_021f521c_L2b4
    cmp r6, #0
    beq ov001_021f521c_L2e8
    mov r0, r5
    bl native_fn_021e2078
    b ov001_021f521c_L2e8
ov001_021f521c_L2b4:
    ldr r0, [sp, #0x98]
    mov r1, #1
    str r1, [r0]
    mov r0, r5
    bl native_fn_021e24f8
    b ov001_021f521c_L2e8
ov001_021f521c_L2cc:
    ldr r0, [sp, #0x48]
    cmp r0, #0
    bne ov001_021f521c_L2e8
    ldrb r1, [r5, #0x31f]
    mov r2, #1
    add r0, sp, #80
    str r2, [r0, r1, lsl #2]
ov001_021f521c_L2e8:
    ldr r0, [sp, #0x48]
    cmp r0, #0
    beq ov001_021f521c_L458
    mov r0, r5
    bl native_fn_021dc108
    cmp r0, #0
    beq ov001_021f521c_L314
    add r0, r5, #512
    ldrsb r0, [r0, #55]
    cmp r0, #0
    beq ov001_021f521c_L320
ov001_021f521c_L314:
    ldr r0, [sp, #0x44]
    cmp r0, #0
    bne ov001_021f521c_L35c
ov001_021f521c_L320:
    ldr r0, =0x0223989c
    ldr r3, [sp, #0x3c]
    ldrsb r6, [r0, #43]
    ldr r2, =0x0223995c
    ldr r1, =0x022399b8
    strb r3, [r2, r6]
    str r5, [r1, r6, lsl #2]
    add r1, r6, #1
    strb r1, [r0, #0x2b]
    mov r0, #1
    ldrh r2, [sp, #56]
    add r1, r5, #768
    str r0, [sp, #0x2c]
    strh r2, [r1, #74]
    b ov001_021f521c_L364
ov001_021f521c_L35c:
    mov r0, #0
    str r0, [sp, #0x2c]
ov001_021f521c_L364:
    ldrb r1, [r5, #0x31f]
    mov r2, #1
    add r0, sp, #92
    str r2, [r0, r1, lsl #2]
    b ov001_021f521c_L458
ov001_021f521c_L378:
    ldr r3, [sp, #0x44]
    cmp r3, #0
    beq ov001_021f521c_L394
    ldrb r1, [r5, #0x31f]
    mov r2, #1
    add r0, sp, #80
    str r2, [r0, r1, lsl #2]
ov001_021f521c_L394:
    ldr r0, [sp, #0x48]
    cmp r0, #0
    beq ov001_021f521c_L404
    mov r0, r5
    bl native_fn_021dc108
    cmp r0, #0
    bne ov001_021f521c_L3bc
    ldr r0, [sp, #0x44]
    cmp r0, #0
    bne ov001_021f521c_L3f8
ov001_021f521c_L3bc:
    ldr r0, =0x0223989c
    ldr r3, [sp, #0x3c]
    ldrsb r6, [r0, #43]
    ldr r2, =0x0223995c
    ldr r1, =0x022399b8
    strb r3, [r2, r6]
    str r5, [r1, r6, lsl #2]
    add r1, r6, #1
    strb r1, [r0, #0x2b]
    mov r0, #1
    ldrh r2, [sp, #56]
    add r1, r5, #768
    str r0, [sp, #0x2c]
    strh r2, [r1, #74]
    b ov001_021f521c_L41c
ov001_021f521c_L3f8:
    mov r0, #0
    str r0, [sp, #0x2c]
    b ov001_021f521c_L41c
ov001_021f521c_L404:
    cmp r3, #0
    bne ov001_021f521c_L41c
    ldrb r1, [r5, #0x31f]
    mov r2, #1
    add r0, sp, #80
    str r2, [r0, r1, lsl #2]
ov001_021f521c_L41c:
    add r0, r5, #768
    ldrh r0, [r0, #76]
    cmp r0, #0
    beq ov001_021f521c_L458
    bl native_fn_0205d790
    mov r2, r0
    add r0, r5, #768
    ldrh r0, [r0, #76]
    mov r1, r5
    bl ov001_effect_resource_create_021eec7c
    mov r0, r5
    bl native_fn_021dc5d4
    mov r1, #0
    add r0, r5, #768
    strh r1, [r0, #76]
ov001_021f521c_L458:
    ldrb r0, [r5, #0x357]
    add r0, r0, #1
    strb r0, [r5, #0x357]
ov001_021f521c_L464:
    ldr r0, [sp, #0x20]
    add r9, r9, #1088
    add r0, r0, #1
    str r0, [sp, #0x20]
    cmp r0, r4
    blt ov001_021f521c_L11c
ov001_021f521c_L47c:
    cmp r4, #0
    ldr r9, [sp, #0x24]
    mov r10, #0
    cmpgt r4, #0
    ble ov001_021f521c_L4fc
    mov r6, #1
    mov r11, r10
    mvn r5, #0
    add r7, sp, #80
    add r8, sp, #92
ov001_021f521c_L4a4:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021f521c_L4ec
    ldrb r1, [r9, #0x31f]
    ldr r0, [r8, r1, lsl #2]
    cmp r0, #0
    bne ov001_021f521c_L4ec
    ldr r0, [r7, r1, lsl #2]
    cmp r0, #0
    beq ov001_021f521c_L4ec
    mov r0, r9
    mov r1, r11
    mov r2, r5
    mov r3, r6
    str r11, [sp]
    str r6, [sp, #0x30]
    bl native_fn_021ee7b0
ov001_021f521c_L4ec:
    add r10, r10, #1
    cmp r10, r4
    add r9, r9, #1088
    blt ov001_021f521c_L4a4
ov001_021f521c_L4fc:
    ldr r0, [sp, #0x34]
    cmp r0, #0
    beq ov001_021f521c_L53c
    ldr r0, [sp, #0x28]
    ldrb r0, [r0, #0x21]
    cmp r0, #6
    moveq r0, #230
    beq ov001_021f521c_L534
    cmp r0, #10
    moveq r0, #231
    beq ov001_021f521c_L534
    cmp r0, #9
    moveq r0, #232
    movne r0, #238
ov001_021f521c_L534:
    mov r1, #0
    bl native_fn_021f949c
ov001_021f521c_L53c:
    ldr r0, [sp, #0x30]
    cmp r0, #0
    beq ov001_021f521c_L554
    mov r0, #242
    mov r1, #0
    bl native_fn_021f949c
ov001_021f521c_L554:
    ldr r0, [sp, #0x2c]
    mov r1, #0
    cmp r0, #0
    ldreq r0, =0x0223989c
    beq ov001_021f521c_L578
    mov r0, #243
    bl native_fn_021f949c
    ldr r0, =0x0223989c
    mov r1, #1
ov001_021f521c_L578:
    strb r1, [r0, #0x10]
    ldr r0, [sp, #0x4c]
    add sp, sp, #116
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
