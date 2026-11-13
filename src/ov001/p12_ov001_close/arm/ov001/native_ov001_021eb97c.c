/* ov001 row 0x021eb97c: 1360 bytes.
 *
 * What it does: 337 instructions; 49 call(s) to 0x0207afec, 0x0207afec, 0x021db438, +46 more; loops (back edge at +0x18); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: block fill (337 instructions, 49 calls, 36 branches, 33 back edges, 3 literal slots).
 *
 *   pool +0x544 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x548 -> constant 0x02238e14 (image word 0x02238e14)
 *   pool +0x54c -> constant 0x02238e44 (image word 0x02238e44)
 *   branch +0x50 -> +0xf0
 *   branch +0x98 -> +0xa8
 *   branch +0xac -> +0xe0
 *   branch +0xdc -> +0x538
 *   branch +0xec -> +0x538
 *   branch +0xf4 -> +0x118
 *   branch +0x114 -> +0x538
 *   branch +0x11c -> +0x234
 *   branch +0x138 -> +0x1f4
 *   branch +0x15c -> +0x178
 *   branch +0x1c0 -> +0x1f4
 *   branch +0x1cc -> +0x1d8
 *   back edge +0x200 -> +0x12c
 *   branch +0x230 -> +0x538
 *   branch +0x238 -> +0x268
 *   branch +0x250 -> +0x538
 *   branch +0x264 -> +0x538
 *   branch +0x26c -> +0x344
 *   branch +0x294 -> +0x2fc
 *   branch +0x2c8 -> +0x2f0
 *   branch +0x2d4 -> +0x2f0
 *   branch +0x310 -> +0x31c
 *   back edge +0x328 -> +0x288
 *   branch +0x340 -> +0x538
 *   branch +0x348 -> +0x420
 *   branch +0x360 -> +0x538
 *   branch +0x36c -> +0x374
 *   branch +0x384 -> +0x398
 *   branch +0x394 -> +0x3d4
 *   branch +0x3c4 -> +0x3d4
 *   branch +0x3f8 -> +0x40c
 *   back edge +0x418 -> +0x3e0
 *   branch +0x41c -> +0x538
 *   branch +0x424 -> +0x46c
 *   branch +0x458 -> +0x538
 *   branch +0x468 -> +0x538
 *   branch +0x470 -> +0x538
 *   branch +0x494 -> +0x4a8
 *   back edge +0x4b0 -> +0x47c
 *   branch +0x4bc -> +0x4c4
 *   branch +0x4d4 -> +0x4e8
 *   branch +0x4f4 -> +0x500
 *   branch +0x514 -> +0x524
 *   test +0x4c cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xa8 cmp r6, #0
 *   test +0xf0 cmp r0, #5
 *   test +0x104 cmp r0, #30
 *   test +0x118 cmp r0, #10
 *   test +0x134 cmp r0, #0
 *   test +0x158 cmp r0, #0
 *   test +0x170 cmp r0, #2
 *   test +0x18c cmp r6, r0
 *   test +0x1b4 cmp r0, #180
 *   test +0x1bc cmpeq r0, #0
 *   test +0x1c8 cmp r0, #0
 *   test +0x1fc cmp r5, #3
 *   test +0x20c cmp r1, #0
 *   test +0x234 cmp r0, #15
 *   test +0x24c cmp r0, #15
 *   test +0x268 cmp r0, #20
 *   test +0x290 cmp r0, #0
 *   test +0x2bc tst r0, #2
 *   test +0x2d0 cmp r0, #0
 *   test +0x30c cmp r0, #0
 *   test +0x320 cmp r10, #3
 *   test +0x344 cmp r0, #30
 *   test +0x35c cmp r0, #15
 *   test +0x368 cmp r0, #0
 *   test +0x380 cmp r0, #0
 *   test +0x3a4 cmp r0, #0
 *   test +0x3b4 cmp r0, #0
 *   test +0x3f4 cmp r0, #0
 *   test +0x404 cmp r0, #0
 *   test +0x410 cmp r8, #3
 *   test +0x420 cmp r0, #60
 *   test +0x438 cmp r0, #0
 *   test +0x44c cmp r0, #0
 *   test +0x454 cmp r4, #0
 *   test +0x46c cmp r0, #100
 *   test +0x490 cmp r0, #0
 *   test +0x4ac cmp r8, #3
 *   test +0x4b8 cmp r0, #0
 *   test +0x4d0 cmp r6, #0
 *   test +0x4f0 cmp r0, #0
 *   test +0x510 cmp r1, #0
 *   1 block transfer(s), 30 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021eb97c; the literal pool and
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
extern void native_fn_021eab48(void);
extern void native_fn_021d7f54(void);
extern void native_fn_021d9494(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_021eb024(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f2304(void);
extern void native_fn_02044cdc(void);
extern void native_fn_021e9de0(void);
extern void native_fn_021f14e4(void);
extern void native_fn_021eaa88(void);
extern void native_fn_021eab0c(void);
extern void native_fn_0220f600(void);
extern void native_fn_021ea398(void);
extern void native_fn_021ea428(void);
extern void native_fn_021e2390(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_021dbb14(void);
extern void native_fn_0220f868(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021dbb9c(void);
extern void native_fn_022168e8(void);
extern void native_fn_021dc5d4(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_021dc940(void);


asm u32 native_ov001_021eb97c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r1, =0x02238d7c
    ldrh r0, [r1, #54]
    ldr r1, [r1, #0x54]
    ldrb r5, [r1, #0x31e]
    bl native_fn_0207afec
    ldr r1, =0x02238d7c
    ldrsh r6, [r0, #12]
    ldrh r0, [r1, #54]
    bl native_fn_0207afec
    mov r7, r0
    mov r0, r5
    mov r1, #0
    bl ov001_side_slot_record_021db438
    mov r8, r0
    bl native_fn_021eab48
    ldr r4, =0x02238d7c
    ldrb r0, [r4, #0x8]
    cmp r0, #0
    bne ov001_021eb97c_Lf0
    mov r1, #0
    mov r0, r5
    str r1, [r4, #0x48]
    bl native_fn_021d7f54
    mov r0, r4
    ldr r0, [r0, #0x60]
    mov r1, #0
    mov r2, #1
    bl native_fn_021d9494
    mov r1, r4
    ldrb r2, [r1, #0x19]
    ldr r0, =0x02238e14
    strb r2, [r1, #0x1f]
    bl native_fn_0202ac08
    mov r0, r4
    ldrh r0, [r0, #54]
    cmp r0, #0
    bne ov001_021eb97c_La8
    mov r0, #180
    mov r1, #0
    bl native_fn_021eea10
ov001_021eb97c_La8:
    cmp r6, #0
    beq ov001_021eb97c_Le0
    mov r0, r6
    mov r1, #0
    bl native_fn_021eea10
    mov r0, r7
    mov r1, #0
    bl native_fn_021eb024
    ldr r0, =0x02238d7c
    mov r1, #5
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0, #0x6]
    b ov001_021eb97c_L538
ov001_021eb97c_Le0:
    ldr r0, =0x02238d7c
    mov r1, #10
    strb r1, [r0, #0x8]
    b ov001_021eb97c_L538
ov001_021eb97c_Lf0:
    cmp r0, #5
    bne ov001_021eb97c_L118
    ldrb r0, [r4, #0x6]
    add r1, r0, #1
    and r0, r1, #255
    cmp r0, #30
    strb r1, [r4, #0x6]
    movhs r0, #10
    strhsb r0, [r4, #0x8]
    b ov001_021eb97c_L538
ov001_021eb97c_L118:
    cmp r0, #10
    bne ov001_021eb97c_L234
    mov r5, #0
    mov r9, r8
    mov r11, r5
ov001_021eb97c_L12c:
    mov r0, r9
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021eb97c_L1f4
    ldrh r1, [r4, #54]
    ldrb r2, [r4, #0x19]
    mov r0, r9
    mov r7, #100
    bl native_fn_021f2304
    mov r6, r0
    ldrh r0, [r4, #54]
    cmp r0, #0
    beq ov001_021eb97c_L178
    ldr r0, [r4, #0x60]
    ldr r0, [r0, #0x1e8]
    ldrsh r0, [r0, #42]
    bl native_fn_02044cdc
    cmp r0, #2
    moveq r7, #150
ov001_021eb97c_L178:
    add r0, r6, r6, lsl #4
    add r10, r8, r0, lsl #6
    ldrb r0, [r9, #0x31f]
    mov r1, r10
    mov r3, r11
    cmp r6, r0
    movne r0, #1
    stmia sp, {r7, r11}
    moveq r0, #0
    str r0, [sp, #0x8]
    ldrh r2, [r4, #54]
    ldr r0, [r4, #0x60]
    bl native_fn_021e9de0
    add r0, r10, #768
    ldrh r0, [r0, #76]
    cmp r0, #180
    ldreq r0, [r4, #0x48]
    cmpeq r0, #0
    bne ov001_021eb97c_L1f4
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb97c_L1d8
    ldrh r0, [r4, #54]
    bl native_fn_021eaa88
ov001_021eb97c_L1d8:
    mov r0, #11
    mov r1, #0
    mov r2, #48
    mov r3, #2
    bl native_fn_021eab0c
    mov r0, #1
    str r0, [r4, #0x48]
ov001_021eb97c_L1f4:
    add r9, r9, #1088
    add r5, r5, #1
    cmp r5, #3
    blt ov001_021eb97c_L12c
    ldr r0, =0x02238d7c
    ldrsb r1, [r0, #11]
    cmp r1, #0
    movgt r1, #1
    movle r1, #0
    strb r1, [r0, #0x19]
    ldr r0, =0x02238d7c
    mov r1, #15
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0, #0x6]
    b ov001_021eb97c_L538
ov001_021eb97c_L234:
    cmp r0, #15
    bne ov001_021eb97c_L268
    ldrb r0, [r4, #0x6]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r4, #0x6]
    cmp r0, #15
    blo ov001_021eb97c_L538
    mov r0, #20
    strb r0, [r4, #0x8]
    mov r0, #0
    strb r0, [r4, #0x6]
    b ov001_021eb97c_L538
ov001_021eb97c_L268:
    cmp r0, #20
    bne ov001_021eb97c_L344
    mov r10, #0
    mov r9, #1
    mov r5, #249
    mov r11, #176
    mov r7, #60
    mov r6, r10
ov001_021eb97c_L288:
    mov r0, r8
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021eb97c_L2fc
    ldr r0, [r4, #0x60]
    mov r1, r8
    add r2, r0, r10, lsl #1
    str r9, [sp]
    add r3, r2, #768
    ldrh r2, [r4, #54]
    ldrsh r3, [r3, #78]
    bl native_fn_0220f600
    ldr r0, [r8, #0x33c]
    tst r0, #2
    strneb r7, [r4, #0x8]
    strneb r6, [r4, #0x6]
    bne ov001_021eb97c_L2f0
    ldrb r0, [r4, #0x19]
    cmp r0, #0
    beq ov001_021eb97c_L2f0
    mov r0, r8
    mov r1, r5
    bl native_fn_021ea398
    mov r0, r8
    mov r1, r11
    bl native_fn_021ea398
ov001_021eb97c_L2f0:
    ldrh r1, [r4, #54]
    mov r0, r8
    bl native_fn_021ea428
ov001_021eb97c_L2fc:
    ldr r0, [r4, #0x60]
    add r0, r0, r10, lsl #1
    add r0, r0, #768
    ldrsh r0, [r0, #78]
    cmp r0, #0
    ble ov001_021eb97c_L31c
    mov r0, r8
    bl native_fn_021e2390
ov001_021eb97c_L31c:
    add r10, r10, #1
    cmp r10, #3
    add r8, r8, #1088
    blt ov001_021eb97c_L288
    ldr r0, =0x02238d7c
    mov r1, #30
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0, #0x6]
    b ov001_021eb97c_L538
ov001_021eb97c_L344:
    cmp r0, #30
    bne ov001_021eb97c_L420
    ldrb r0, [r4, #0x6]
    add r1, r0, #1
    and r0, r1, #255
    strb r1, [r4, #0x6]
    cmp r0, #15
    blo ov001_021eb97c_L538
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb97c_L374
    bl ov001_clear_state_flag4_021f14a4
ov001_021eb97c_L374:
    mov r1, r5
    mov r0, #0
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_021eb97c_L398
    ldr r0, =0x02238d7c
    mov r1, #60
    strb r1, [r0, #0x8]
    b ov001_021eb97c_L3d4
ov001_021eb97c_L398:
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x60]
    ldrb r0, [r0, #0x31e]
    cmp r0, #0
    moveq r0, #1
    movne r0, #0
    bl native_fn_0220f868
    cmp r0, #0
    ldreq r0, =0x02238d7c
    moveq r1, #100
    streqb r1, [r0, #0x8]
    beq ov001_021eb97c_L3d4
    ldr r0, =0x02238d7c
    mov r1, #60
    strb r1, [r0, #0x8]
ov001_021eb97c_L3d4:
    ldr r7, =0x02238e44
    mov r8, #0
    mov r4, #1
ov001_021eb97c_L3e0:
    mov r0, r5
    mov r1, r8
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021eb97c_L40c
    mov r0, r6
    bl native_fn_021dbd24
    cmp r0, #0
    streqb r4, [r7]
ov001_021eb97c_L40c:
    add r8, r8, #1
    cmp r8, #3
    add r7, r7, #1
    blt ov001_021eb97c_L3e0
    b ov001_021eb97c_L538
ov001_021eb97c_L420:
    cmp r0, #60
    bne ov001_021eb97c_L46c
    mov r4, #0
    mov r0, r4
    mov r1, r5
    bl native_fn_021dbb9c
    cmp r0, #0
    moveq r4, #1
    mov r1, r5
    mov r0, #0
    bl native_fn_022168e8
    cmp r0, #0
    moveq r4, #1
    cmp r4, #0
    bne ov001_021eb97c_L538
    ldr r0, =0x02238d7c
    mov r1, #100
    strb r1, [r0, #0x8]
    b ov001_021eb97c_L538
ov001_021eb97c_L46c:
    cmp r0, #100
    bne ov001_021eb97c_L538
    mov r8, #0
    mov r4, r8
ov001_021eb97c_L47c:
    mov r0, r5
    mov r1, r8
    bl ov001_side_slot_record_021db438
    mov r7, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021eb97c_L4a8
    mov r0, r7
    bl native_fn_021dc5d4
    add r0, r7, #768
    strh r4, [r0, #76]
ov001_021eb97c_L4a8:
    add r8, r8, #1
    cmp r8, #3
    blt ov001_021eb97c_L47c
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021eb97c_L4c4
    bl ov001_clear_state_flag4_021f14a4
ov001_021eb97c_L4c4:
    ldr r0, =0x02238d7c
    mov r1, #0
    str r1, [r0, #0x48]
    cmp r6, #0
    beq ov001_021eb97c_L4e8
    ldrh r0, [r0, #54]
    bl native_fn_0207afec
    ldrsh r0, [r0, #12]
    bl native_fn_021eeb70
ov001_021eb97c_L4e8:
    ldr r0, =0x02238d7c
    ldrh r0, [r0, #54]
    cmp r0, #0
    bne ov001_021eb97c_L500
    mov r0, #180
    bl native_fn_021eeb70
ov001_021eb97c_L500:
    ldr r0, =0x02238e14
    bl native_fn_0202ac4c
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x1f]
    cmp r1, #0
    bne ov001_021eb97c_L524
    ldr r0, [r0, #0x60]
    mov r1, #8
    bl native_fn_021dc940
ov001_021eb97c_L524:
    ldr r0, =0x02238d7c
    mov r1, #12
    strb r1, [r0, #0x13]
    mov r1, #0
    strb r1, [r0, #0x8]
ov001_021eb97c_L538:
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
