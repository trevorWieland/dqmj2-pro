/* ov001 row 0x021ececc: 2420 bytes.
 *
 * What it does: 598 instructions; 83 call(s) to 0x0207afec, 0x021ea4c4, 0x0202ac08, +80 more; loops (back edge at +0x10); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 7 literal slot(s) in the extent
 *
 * Decoded shape: loop with 83 calls (598 instructions, 83 calls, 61 branches, 49 back edges, 7 literal slots).
 *
 *   pool +0x958 -> constant 0x02238d7c (image word 0x02238d7c)
 *   pool +0x95c -> constant 0x02238e14 (image word 0x02238e14)
 *   pool +0x960 -> constant 0x02238e4c (image word 0x02238e4c)
 *   pool +0x964 -> constant 0x02238e44 (image word 0x02238e44)
 *   pool +0x968 -> constant 0x02238e50 (image word 0x02238e50)
 *   pool +0x96c -> constant 0xff7ffdff (image word 0xff7ffdff)
 *   pool +0x970 -> constant 0x02238e48 (image word 0x02238e48)
 *   branch +0x3c -> +0x88
 *   branch +0x5c -> +0x68
 *   branch +0x84 -> +0x4d4
 *   branch +0x8c -> +0x4d4
 *   branch +0xc4 -> +0x468
 *   branch +0xdc -> +0x468
 *   branch +0xe8 -> +0x468
 *   branch +0xfc -> +0x178
 *   branch +0x174 -> +0x3e8
 *   branch +0x180 -> +0x1e0
 *   branch +0x1dc -> +0x3e8
 *   branch +0x1f4 -> +0x214
 *   branch +0x210 -> +0x3e8
 *   branch +0x228 -> +0x274
 *   branch +0x270 -> +0x3e8
 *   branch +0x288 -> +0x2b0
 *   branch +0x2ac -> +0x3e8
 *   branch +0x2dc -> +0x3e8
 *   branch +0x2f0 -> +0x340
 *   branch +0x308 -> +0x338
 *   branch +0x320 -> +0x338
 *   branch +0x33c -> +0x3e0
 *   branch +0x378 -> +0x3e0
 *   branch +0x384 -> +0x39c
 *   branch +0x3b4 -> +0x3c8
 *   branch +0x3f4 -> +0x408
 *   branch +0x44c -> +0x468
 *   back edge +0x478 -> +0xa8
 *   branch +0x480 -> +0x494
 *   branch +0x490 -> +0x4d4
 *   branch +0x49c -> +0x4b0
 *   branch +0x4ac -> +0x4d4
 *   branch +0x4c4 -> +0x4d4
 *   branch +0x4e0 -> +0x668
 *   branch +0x4ec -> +0x668
 *   branch +0x4f8 -> +0x668
 *   branch +0x508 -> +0x510
 *   branch +0x518 -> +0x574
 *   branch +0x548 -> +0x564
 *   back edge +0x56c -> +0x52c
 *   branch +0x570 -> +0x598
 *   branch +0x59c -> +0x5b0
 *   branch +0x5ac -> +0x668
 *   branch +0x5d8 -> +0x65c
 *   branch +0x5e4 -> +0x604
 *   branch +0x600 -> +0x64c
 *   branch +0x62c -> +0x640
 *   back edge +0x648 -> +0x610
 *   branch +0x658 -> +0x668
 *   branch +0x674 -> +0x6fc
 *   branch +0x69c -> +0x6fc
 *   branch +0x6d4 -> +0x6fc
 *   branch +0x708 -> +0x73c
 *   branch +0x748 -> +0x7d8
 *   branch +0x788 -> +0x7b0
 *   back edge +0x7c0 -> +0x780
 *   branch +0x7e4 -> +0x804
 *   branch +0x810 -> +0x864
 *   branch +0x828 -> +0x834
 *   back edge +0x844 -> +0x820
 *   branch +0x870 -> +0x8c8
 *   branch +0x884 -> +0x8b0
 *   branch +0x8ac -> +0x8c8
 *   branch +0x8d4 -> +0x90c
 *   branch +0x8e0 -> +0x90c
 *   branch +0x918 -> +0x94c
 *   branch +0x93c -> +0x944
 *   test +0x1c cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x58 cmp r0, #0
 *   test +0x88 cmp r0, #5
 *   test +0xc0 cmp r0, #0
 *   test +0xd8 cmp r1, #0
 *   test +0xe4 cmp r1, #0
 *   test +0xf8 cmp r0, #0
 *   test +0x17c cmp r0, #0
 *   test +0x1f0 cmp r0, #0
 *   test +0x260 cmp r11, #8
 *   test +0x284 cmp r0, #0
 *   test +0x2d8 cmp r0, #0
 *   test +0x2ec cmp r0, #255
 *   test +0x304 cmp r0, #0
 *   test +0x31c cmp r0, #0
 *   test +0x350 cmp r1, r0
 *   test +0x360 cmpeq r1, r0
 *   test +0x374 cmp r0, #0
 *   test +0x380 cmp r0, #0
 *   test +0x3b0 cmp r2, #0
 *   test +0x3f0 cmp r0, #0
 *   test +0x448 cmp r0, #249
 *   test +0x458 cmp r0, #249
 *   test +0x474 cmp r7, #3
 *   test +0x47c cmp r8, #0
 *   test +0x498 cmp r0, #0
 *   test +0x4b4 cmp r0, #0
 *   test +0x4dc cmp r0, #10
 *   test +0x4e8 cmp r0, #0
 *   test +0x4f4 cmp r0, #0
 *   test +0x504 cmp r0, #0
 *   test +0x514 cmp r0, #0
 *   test +0x544 cmp r0, #0
 *   test +0x55c tst r0, #2
 *   test +0x568 cmp r6, #3
 *   test +0x590 tst r0, #2
 *   test +0x598 cmp r4, #0
 *   test +0x5b8 cmp r0, #0
 *   test +0x5d4 cmp r0, #0
 *   test +0x5e0 cmp r0, #0
 *   test +0x628 cmp r0, #0
 *   test +0x644 cmp r8, #3
 *   test +0x670 cmp r0, #20
 *   test +0x67c cmp r0, #0
 *   test +0x698 cmp r0, #0
 *   test +0x6a8 cmp r0, #0
 *   test +0x6c4 cmp r0, #0
 *   test +0x704 cmp r0, #30
 *   test +0x710 cmp r0, #0
 *   test +0x72c cmp r0, #0
 *   test +0x744 cmp r0, #40
 *   test +0x784 cmp r0, #0
 *   test +0x7b4 cmp r8, #3
 *   test +0x7e0 cmp r1, #50
 *   test +0x7f4 cmp r1, #30
 *   test +0x80c cmp r0, #60
 *   test +0x824 cmp r0, #0
 *   test +0x838 cmp r7, #3
 *   test +0x86c cmp r1, #70
 *   test +0x880 cmp r2, #0
 *   test +0x8b8 cmp r1, #3
 *   test +0x8d0 cmp r0, #80
 *   test +0x8dc cmp r0, #0
 *   test +0x8f4 cmp r1, #3
 *   test +0x914 cmp r1, #100
 *   test +0x938 cmp r0, #0
 *   0 block transfer(s), 54 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021ececc; the literal pool and
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
extern void native_fn_021ea4c4(void);
extern void native_fn_0202ac08(void);
extern void native_fn_021eea10(void);
extern void native_fn_02008d78(void);
extern void ov001_side_slot_record_021db438(void);
extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_0220fdb4(void);
extern void native_fn_021db788(void);
extern void native_fn_022024d4(void);
extern void native_fn_0205d790(void);
extern void native_fn_021e9cd8(void);
extern void ov001_begin_state_transition_021f1354(void);
extern void ov001_select_mode_id_021f1438(void);
extern void native_fn_021ecc48(void);
extern void native_fn_0220e944(void);
extern void native_fn_021f949c(void);
extern void native_fn_021e2078(void);
extern void native_fn_021eccf0(void);
extern void native_fn_021dbf98(void);
extern void native_fn_0220ebf4(void);
extern void native_fn_021f1bf0(void);
extern void native_fn_021e1864(void);
extern void native_fn_02210ad0(void);
extern void native_fn_021e1950(void);
extern void native_fn_021d8dec(void);
extern void native_fn_0220f470(void);
extern void native_fn_021e1a60(void);
extern void native_fn_021e9d70(void);
extern void native_fn_02212290(void);
extern void native_fn_021f14e4(void);
extern void ov001_clear_state_flag4_021f14a4(void);
extern void native_fn_0220f530(void);
extern void native_fn_021dbb14(void);
extern void native_fn_022168e8(void);
extern void native_fn_021dbb9c(void);
extern void ov001_effect_resource_create_021eec7c(void);
extern void native_fn_0205d718(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);
extern void native_fn_021f1c38(void);
extern void native_fn_021f1c68(void);
extern void native_fn_021f90b4(void);


asm u32 native_ov001_021ececc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #48
    ldr r0, =0x02238d7c
    ldrh r0, [r0, #54]
    bl native_fn_0207afec
    mov r5, r0
    bl native_fn_021ea4c4
    cmp r0, #0
    movne r0, #1
    strne r0, [sp, #0x1c]
    moveq r0, #0
    ldr r4, =0x02238d7c
    streq r0, [sp, #0x1c]
    ldrb r0, [r4, #0x4]
    cmp r0, #0
    bne ov001_021ececc_L88
    ldr r0, =0x02238e14
    bl native_fn_0202ac08
    mov r0, #125
    mov r1, #0
    bl native_fn_021eea10
    ldrsh r0, [r5, #14]
    cmp r0, #0
    beq ov001_021ececc_L68
    mov r1, #0
    bl native_fn_021eea10
ov001_021ececc_L68:
    ldr r0, =0x02238e4c
    mov r1, #0
    mov r2, #3
    bl native_fn_02008d78
    ldr r0, =0x02238d7c
    mov r1, #5
    strb r1, [r0, #0x4]
    b ov001_021ececc_L4d4
ov001_021ececc_L88:
    cmp r0, #5
    bne ov001_021ececc_L4d4
    mov r8, #0
    ldr r9, =0x02238e44
    ldr r10, =0x02238e4c
    str r8, [sp, #0x24]
    str r8, [sp, #0x20]
    mov r7, r8
ov001_021ececc_La8:
    ldr r0, [r4, #0x54]
    mov r1, r7
    ldrb r0, [r0, #0x31e]
    bl ov001_side_slot_record_021db438
    mov r6, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021ececc_L468
    ldr r0, [r4, #0x60]
    add r1, r0, r7, lsl #1
    add r1, r1, #768
    ldrsh r1, [r1, #78]
    cmp r1, #0
    ble ov001_021ececc_L468
    ldrb r1, [r9]
    cmp r1, #0
    bne ov001_021ececc_L468
    mov r1, r6
    ldrh r2, [r4, #54]
    bl native_fn_0220fdb4
    cmp r0, #0
    beq ov001_021ececc_L178
    mov r0, r6
    mov r1, #0
    bl native_fn_021db788
    ldr r2, [r4, #0x60]
    ldrb r0, [r6, #0x31e]
    add r2, r2, r7, lsl #1
    add r2, r2, #768
    ldrb r1, [r6, #0x31f]
    ldrsh r2, [r2, #78]
    bl native_fn_022024d4
    mov r0, #125
    bl native_fn_0205d790
    mov r2, r0
    mov r0, #125
    mov r1, r6
    bl native_fn_021e9cd8
    mov r0, #11
    mov r1, #0
    mov r2, #69
    mov r3, #1
    bl ov001_begin_state_transition_021f1354
    mov r0, #2
    bl ov001_select_mode_id_021f1438
    mov r0, #0
    strb r0, [r4, #0x19]
    add r1, r6, #768
    strh r0, [r1, #74]
    strb r0, [r4, #0x5]
    mov r8, #1
    b ov001_021ececc_L3e8
ov001_021ececc_L178:
    bl native_fn_021ecc48
    cmp r0, #0
    beq ov001_021ececc_L1e0
    mov r0, r6
    mov r1, #0
    bl native_fn_021db788
    ldr r2, [r4, #0x60]
    ldrb r0, [r6, #0x31e]
    add r2, r2, r7, lsl #1
    add r2, r2, #768
    ldrb r1, [r6, #0x31f]
    ldrsh r2, [r2, #78]
    bl native_fn_022024d4
    mov r0, #125
    bl native_fn_0205d790
    mov r2, r0
    mov r0, #125
    mov r1, r6
    bl native_fn_021e9cd8
    mov r0, #0
    strb r0, [r4, #0x19]
    add r1, r6, #768
    strh r0, [r1, #74]
    strb r0, [r4, #0x5]
    mov r8, #1
    b ov001_021ececc_L3e8
ov001_021ececc_L1e0:
    ldr r0, [r4, #0x60]
    mov r1, r6
    ldrh r2, [r4, #54]
    bl native_fn_0220e944
    cmp r0, #0
    beq ov001_021ececc_L214
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
    mov r0, r6
    bl native_fn_021e2078
    mov r8, #1
    b ov001_021ececc_L3e8
ov001_021ececc_L214:
    ldrh r1, [r4, #54]
    mov r0, r6
    add r2, sp, #44
    bl native_fn_021eccf0
    movs r11, r0
    beq ov001_021ececc_L274
    mov r0, #0
    str r0, [sp]
    ldr r2, [sp, #0x2c]
    mov r0, r6
    mov r1, r11
    mov r3, #0
    bl native_fn_021dbf98
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
    mov r0, r6
    bl native_fn_021e2078
    mov r0, #1
    cmp r11, #8
    strb r0, [r10]
    streq r0, [sp, #0x24]
    movne r8, r0
    b ov001_021ececc_L3e8
ov001_021ececc_L274:
    ldr r0, [r4, #0x60]
    mov r1, r6
    ldrh r2, [r4, #54]
    bl native_fn_0220ebf4
    cmp r0, #0
    beq ov001_021ececc_L2b0
    mov r0, #1
    str r0, [sp, #0x20]
    mov r0, #78
    bl native_fn_021f1bf0
    mov r0, #1
    strb r0, [r10]
    mov r0, #0
    strb r0, [r4, #0x28]
    b ov001_021ececc_L3e8
ov001_021ececc_L2b0:
    mov r0, #0
    str r0, [sp]
    ldr r0, =0x02238e50
    mov r2, r6
    ldrb r0, [r0]
    mov r3, #1
    str r0, [sp, #0x4]
    ldrh r0, [r4, #54]
    ldr r1, [r4, #0x60]
    bl native_fn_021e1864
    cmp r0, #0
    beq ov001_021ececc_L3e8
    ldrh r0, [r4, #54]
    bl native_fn_0207afec
    ldrb r0, [r0, #0x21]
    cmp r0, #255
    bne ov001_021ececc_L340
    ldr r0, [r4, #0x60]
    mov r1, #2
    mov r2, #1
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_021ececc_L338
    mov r0, r6
    mov r1, #0
    bl native_fn_021db788
    ldrsh r0, [r5, #14]
    cmp r0, #0
    beq ov001_021ececc_L338
    bl native_fn_0205d790
    mov r2, r0
    ldrsh r0, [r5, #14]
    mov r1, r6
    bl native_fn_021e9cd8
ov001_021ececc_L338:
    mov r8, #1
    b ov001_021ececc_L3e0
ov001_021ececc_L340:
    ldr r2, [r4, #0x50]
    ldrb r0, [r6, #0x31e]
    ldrb r1, [r2, #0x31e]
    mov r3, #0
    cmp r1, r0
    ldreqb r1, [r2, #0x31f]
    ldreqb r0, [r6, #0x31f]
    mov r2, #0
    cmpeq r1, r0
    ldrh r0, [r4, #54]
    moveq r3, #1
    mov r1, r6
    bl native_fn_021e1950
    cmp r0, #0
    beq ov001_021ececc_L3e0
    ldrsh r0, [r5, #14]
    cmp r0, #0
    beq ov001_021ececc_L39c
    bl native_fn_0205d790
    mov r2, r0
    ldrsh r0, [r5, #14]
    mov r1, r6
    bl native_fn_021e9cd8
ov001_021ececc_L39c:
    ldrh r0, [r4, #54]
    bl native_fn_0207afec
    ldrb r0, [r0, #0x21]
    bl native_fn_021d8dec
    ldrh r2, [r0, #12]
    cmp r2, #0
    beq ov001_021ececc_L3c8
    mov r0, #1
    mov r1, #0
    mov r3, r0
    bl ov001_begin_state_transition_021f1354
ov001_021ececc_L3c8:
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
    mov r0, r6
    bl native_fn_021e2078
    mov r8, #1
ov001_021ececc_L3e0:
    mov r0, #0
    strb r0, [r4, #0x5]
ov001_021ececc_L3e8:
    mov r0, r6
    bl native_fn_0220f470
    cmp r0, #0
    bne ov001_021ececc_L408
    ldr r1, [r6, #0x33c]
    ldr r0, =0xff7ffdff
    and r0, r1, r0
    str r0, [r6, #0x33c]
ov001_021ececc_L408:
    mov r0, #0
    str r0, [sp]
    add r0, sp, #40
    str r0, [sp, #0x4]
    mov r0, #0
    str r0, [sp, #0x8]
    str r0, [sp, #0xc]
    str r0, [sp, #0x10]
    str r0, [sp, #0x14]
    str r0, [sp, #0x18]
    ldrh r0, [r4, #54]
    ldr r1, [r4, #0x60]
    mov r2, r6
    mov r3, #0
    bl native_fn_021e1a60
    ldrh r0, [sp, #40]
    cmp r0, #249
    beq ov001_021ececc_L468
    add r1, r6, #768
    ldrh r0, [r1, #74]
    cmp r0, #249
    moveq r0, #0
    streqb r0, [r4, #0x19]
    streqh r0, [r1, #74]
ov001_021ececc_L468:
    add r9, r9, #1
    add r10, r10, #1
    add r7, r7, #1
    cmp r7, #3
    blt ov001_021ececc_La8
    cmp r8, #0
    beq ov001_021ececc_L494
    ldr r0, =0x02238d7c
    mov r1, #10
    strb r1, [r0, #0x4]
    b ov001_021ececc_L4d4
ov001_021ececc_L494:
    ldr r0, [sp, #0x24]
    cmp r0, #0
    beq ov001_021ececc_L4b0
    ldr r0, =0x02238d7c
    mov r1, #40
    strb r1, [r0, #0x4]
    b ov001_021ececc_L4d4
ov001_021ececc_L4b0:
    ldr r0, [sp, #0x20]
    cmp r0, #0
    ldreq r0, =0x02238d7c
    moveq r1, #100
    streqb r1, [r0, #0x4]
    beq ov001_021ececc_L4d4
    ldr r0, =0x02238d7c
    mov r1, #70
    strb r1, [r0, #0x4]
ov001_021ececc_L4d4:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x4]
    cmp r0, #10
    bne ov001_021ececc_L668
    bl native_fn_021e9d70
    cmp r0, #0
    beq ov001_021ececc_L668
    bl native_fn_02212290
    cmp r0, #0
    bne ov001_021ececc_L668
    mov r4, #0
    bl native_fn_021f14e4
    cmp r0, #0
    beq ov001_021ececc_L510
    bl ov001_clear_state_flag4_021f14a4
ov001_021ececc_L510:
    ldr r0, [sp, #0x1c]
    cmp r0, #0
    beq ov001_021ececc_L574
    mov r8, #1
    ldr r7, =0x02238d7c
    mov r6, #0
    mov r9, r8
ov001_021ececc_L52c:
    ldr r0, [r7, #0x54]
    mov r1, r6
    ldrb r0, [r0, #0x31e]
    bl ov001_side_slot_record_021db438
    mov r10, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021ececc_L564
    mov r0, r10
    mov r1, r9
    bl native_fn_0220f530
    ldr r0, [r10, #0x33c]
    tst r0, #2
    movne r4, r8
ov001_021ececc_L564:
    add r6, r6, #1
    cmp r6, #3
    blt ov001_021ececc_L52c
    b ov001_021ececc_L598
ov001_021ececc_L574:
    ldr r0, =0x02238d7c
    mov r1, #1
    ldr r0, [r0, #0x54]
    bl native_fn_0220f530
    ldr r0, =0x02238d7c
    ldr r0, [r0, #0x54]
    ldr r0, [r0, #0x33c]
    tst r0, #2
    movne r4, #1
ov001_021ececc_L598:
    cmp r4, #0
    beq ov001_021ececc_L5b0
    ldr r0, =0x02238d7c
    mov r1, #20
    strb r1, [r0, #0x4]
    b ov001_021ececc_L668
ov001_021ececc_L5b0:
    ldr r0, [sp, #0x1c]
    ldr r1, =0x02238d7c
    cmp r0, #0
    movne r0, #0
    ldr r1, [r1, #0x54]
    ldreq r0, =0x02238d7c
    ldrb r1, [r1, #0x31e]
    ldreq r0, [r0, #0x54]
    bl native_fn_021dbb14
    cmp r0, #0
    beq ov001_021ececc_L65c
    ldr r0, [sp, #0x1c]
    cmp r0, #0
    bne ov001_021ececc_L604
    ldr r0, =0x02238d7c
    mov r2, #0
    ldr r1, [r0, #0x54]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    b ov001_021ececc_L64c
ov001_021ececc_L604:
    mov r8, #0
    ldr r4, =0x02238d7c
    mov r6, r8
ov001_021ececc_L610:
    ldr r0, [r4, #0x54]
    mov r1, r8
    ldrb r0, [r0, #0x31e]
    bl ov001_side_slot_record_021db438
    mov r7, r0
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_021ececc_L640
    ldrb r0, [r7, #0x31e]
    ldrb r1, [r7, #0x31f]
    mov r2, r6
    bl native_fn_022024d4
ov001_021ececc_L640:
    add r8, r8, #1
    cmp r8, #3
    blt ov001_021ececc_L610
ov001_021ececc_L64c:
    ldr r0, =0x02238d7c
    mov r1, #30
    strb r1, [r0, #0x4]
    b ov001_021ececc_L668
ov001_021ececc_L65c:
    ldr r0, =0x02238d7c
    mov r1, #100
    strb r1, [r0, #0x4]
ov001_021ececc_L668:
    ldr r1, =0x02238d7c
    ldrb r0, [r1, #0x4]
    cmp r0, #20
    bne ov001_021ececc_L6fc
    ldr r0, [sp, #0x1c]
    cmp r0, #0
    movne r0, #0
    ldreq r0, [r1, #0x54]
    ldr r1, =0x02238d7c
    ldr r1, [r1, #0x54]
    ldrb r1, [r1, #0x31e]
    bl native_fn_022168e8
    cmp r0, #0
    beq ov001_021ececc_L6fc
    ldr r0, [sp, #0x1c]
    ldr r1, =0x02238d7c
    cmp r0, #0
    movne r0, #0
    ldr r1, [r1, #0x54]
    ldreq r0, =0x02238d7c
    ldrb r1, [r1, #0x31e]
    ldreq r0, [r0, #0x54]
    bl native_fn_021dbb14
    cmp r0, #0
    ldreq r0, =0x02238d7c
    moveq r1, #100
    streqb r1, [r0, #0x4]
    beq ov001_021ececc_L6fc
    ldr r0, =0x02238d7c
    mov r2, #0
    ldr r1, [r0, #0x54]
    ldrb r0, [r1, #0x31e]
    ldrb r1, [r1, #0x31f]
    bl native_fn_022024d4
    ldr r0, =0x02238d7c
    mov r1, #30
    strb r1, [r0, #0x4]
ov001_021ececc_L6fc:
    ldr r1, =0x02238d7c
    ldrb r0, [r1, #0x4]
    cmp r0, #30
    bne ov001_021ececc_L73c
    ldr r0, [sp, #0x1c]
    cmp r0, #0
    movne r0, #0
    ldreq r0, [r1, #0x54]
    ldr r1, =0x02238d7c
    ldr r1, [r1, #0x54]
    ldrb r1, [r1, #0x31e]
    bl native_fn_021dbb9c
    cmp r0, #0
    ldrne r0, =0x02238d7c
    movne r1, #100
    strneb r1, [r0, #0x4]
ov001_021ececc_L73c:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x4]
    cmp r0, #40
    bne ov001_021ececc_L7d8
    ldr r0, =0x02238e14
    bl native_fn_0202ac08
    mov r0, #152
    mov r1, #0
    bl native_fn_021eea10
    mov r0, #152
    bl native_fn_0205d790
    ldr r6, =0x02238e4c
    ldr r7, =0x02238e48
    ldr r9, =0x02238d7c
    mov r4, r0
    mov r8, #0
    mov r10, #152
ov001_021ececc_L780:
    ldrb r0, [r6]
    cmp r0, #0
    beq ov001_021ececc_L7b0
    ldr r0, [r9, #0x54]
    mov r1, r8
    ldrb r0, [r0, #0x31e]
    bl ov001_side_slot_record_021db438
    mov r1, r0
    mov r0, r10
    mov r2, r4
    bl ov001_effect_resource_create_021eec7c
    strb r0, [r7]
ov001_021ececc_L7b0:
    add r8, r8, #1
    cmp r8, #3
    add r6, r6, #1
    add r7, r7, #1
    blt ov001_021ececc_L780
    ldr r0, =0x02238d7c
    mov r1, #50
    strb r1, [r0, #0x4]
    mov r1, #0
    strb r1, [r0, #0x5]
ov001_021ececc_L7d8:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x4]
    cmp r1, #50
    bne ov001_021ececc_L804
    ldrb r1, [r0, #0x5]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #30
    strb r2, [r0, #0x5]
    movhs r1, #60
    strhsb r1, [r0, #0x4]
ov001_021ececc_L804:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x4]
    cmp r0, #60
    bne ov001_021ececc_L864
    ldr r4, =0x02238e4c
    ldr r6, =0x02238e48
    mov r7, #0
ov001_021ececc_L820:
    ldrb r0, [r4]
    cmp r0, #0
    beq ov001_021ececc_L834
    ldrb r0, [r6]
    bl native_fn_0205d718
ov001_021ececc_L834:
    add r7, r7, #1
    cmp r7, #3
    add r4, r4, #1
    add r6, r6, #1
    blt ov001_021ececc_L820
    mov r0, #152
    bl native_fn_021eeb70
    ldr r0, =0x02238e14
    bl native_fn_0202ac4c
    ldr r0, =0x02238d7c
    mov r1, #100
    strb r1, [r0, #0x4]
ov001_021ececc_L864:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x4]
    cmp r1, #70
    bne ov001_021ececc_L8c8
    ldrb r1, [r0, #0x28]
    ldr r2, =0x02238e4c
    ldrb r2, [r2, r1]
    cmp r2, #0
    beq ov001_021ececc_L8b0
    ldr r0, [r0, #0x54]
    ldrb r0, [r0, #0x31e]
    bl ov001_side_slot_record_021db438
    bl native_fn_021f1c38
    mov r0, #2
    bl native_fn_021f1c68
    ldr r0, =0x02238d7c
    mov r1, #80
    strb r1, [r0, #0x4]
    b ov001_021ececc_L8c8
ov001_021ececc_L8b0:
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #3
    strb r2, [r0, #0x28]
    movhs r1, #100
    strhsb r1, [r0, #0x4]
ov001_021ececc_L8c8:
    ldr r0, =0x02238d7c
    ldrb r0, [r0, #0x4]
    cmp r0, #80
    bne ov001_021ececc_L90c
    bl native_fn_021f90b4
    cmp r0, #0
    beq ov001_021ececc_L90c
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x28]
    add r2, r1, #1
    and r1, r2, #255
    cmp r1, #3
    strb r2, [r0, #0x28]
    movhs r1, #100
    strhsb r1, [r0, #0x4]
    movlo r1, #70
    strlob r1, [r0, #0x4]
ov001_021ececc_L90c:
    ldr r0, =0x02238d7c
    ldrb r1, [r0, #0x4]
    cmp r1, #100
    bne ov001_021ececc_L94c
    mov r1, #0
    strb r1, [r0, #0x4]
    mov r1, #17
    strb r1, [r0, #0x13]
    mov r0, #125
    bl native_fn_021eeb70
    ldrsh r0, [r5, #14]
    cmp r0, #0
    beq ov001_021ececc_L944
    bl native_fn_021eeb70
ov001_021ececc_L944:
    ldr r0, =0x02238e14
    bl native_fn_0202ac4c
ov001_021ececc_L94c:
    mov r0, #0
    add sp, sp, #48
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
