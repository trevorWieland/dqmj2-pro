/* ov000 row 0x02218d30: 1500 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (one load, one store).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x5c0 -> native_data_02245e54 (image word 0x02245e54)
 *   pool +0x5c4 -> native_data_02245f74 (image word 0x02245f74)
 *   pool +0x5c8 -> native_fn_0221930c (image word 0x0221930c)
 *   pool +0x5cc -> native_fn_0221938c (image word 0x0221938c)
 *   pool +0x5d0 -> native_data_0222fa08 (image word 0x0222fa08)
 *   pool +0x5d4 -> native_data_02245e94 (image word 0x02245e94)
 *   pool +0x5d8 -> constant 0x02101ae8 (image word 0x02101ae8)
 *   branch +0x30 -> +0x45c
 *   branch +0x34 -> +0x64
 *   branch +0x38 -> +0x110
 *   branch +0x3c -> +0x194
 *   branch +0x40 -> +0x14c
 *   branch +0x44 -> +0x16c
 *   branch +0x48 -> +0x268
 *   branch +0x4c -> +0x290
 *   branch +0x50 -> +0x378
 *   branch +0x54 -> +0x3a4
 *   branch +0x58 -> +0x3d8
 *   branch +0x5c -> +0x3f8
 *   branch +0x60 -> +0x434
 *   branch +0x6c -> +0xd4
 *   back edge +0xb8 -> +0xac
 *   branch +0xd0 -> +0x45c
 *   branch +0x10c -> +0x45c
 *   branch +0x118 -> +0x45c
 *   branch +0x12c -> +0x140
 *   branch +0x148 -> +0x45c
 *   branch +0x168 -> +0x45c
 *   branch +0x174 -> +0x45c
 *   branch +0x190 -> +0x45c
 *   branch +0x1a0 -> +0x1ac
 *   branch +0x1b8 -> +0x1e4
 *   branch +0x1bc -> +0x1d4
 *   branch +0x1c0 -> +0x1d4
 *   branch +0x1c4 -> +0x1d4
 *   branch +0x1c8 -> +0x1d4
 *   branch +0x1cc -> +0x1d4
 *   branch +0x1d0 -> +0x1d4
 *   branch +0x1e8 -> +0x204
 *   branch +0x210 -> +0x21c
 *   branch +0x228 -> +0x248
 *   branch +0x250 -> +0x45c
 *   branch +0x264 -> +0x45c
 *   branch +0x270 -> +0x45c
 *   branch +0x28c -> +0x45c
 *   branch +0x2ac -> +0x2d0
 *   branch +0x2b8 -> +0x2d0
 *   branch +0x2cc -> +0x45c
 *   branch +0x2d8 -> +0x45c
 *   branch +0x320 -> +0x340
 *   branch +0x33c -> +0x368
 *   branch +0x374 -> +0x45c
 *   branch +0x3a0 -> +0x45c
 *   branch +0x3b8 -> +0x3d0
 *   branch +0x3d4 -> +0x45c
 *   branch +0x3f4 -> +0x45c
 *   branch +0x400 -> +0x45c
 *   branch +0x430 -> +0x45c
 *   branch +0x43c -> +0x45c
 *   branch +0x46c -> +0x548
 *   branch +0x470 -> +0x548
 *   branch +0x474 -> +0x548
 *   branch +0x478 -> +0x490
 *   branch +0x47c -> +0x490
 *   branch +0x480 -> +0x490
 *   branch +0x484 -> +0x548
 *   branch +0x488 -> +0x548
 *   branch +0x48c -> +0x490
 *   branch +0x498 -> +0x4ac
 *   branch +0x4b8 -> +0x548
 *   branch +0x4d0 -> +0x53c
 *   branch +0x4f0 -> +0x524
 *   back edge +0x538 -> +0x4e4
 *   branch +0x55c -> +0x598
 *   branch +0x570 -> +0x57c
 *   branch +0x578 -> +0x580
 *   branch +0x5a8 -> +0x5b4
 *   back edge +0x5ac -> +0x00
 *   test +0x28 cmp r0, #11
 *   test +0x68 cmp r0, #1
 *   test +0x114 cmp r0, #0
 *   test +0x120 cmp r0, #1
 *   test +0x170 cmp r0, #1
 *   test +0x19c cmp r0, #1
 *   test +0x1b0 cmp r0, #5
 *   test +0x1e4 cmp r4, #37
 *   test +0x20c cmp r0, #1
 *   test +0x224 cmp r0, #255
 *   test +0x24c cmp r0, #0
 *   test +0x26c cmp r0, #1
 *   test +0x2a8 cmp r0, #1
 *   test +0x2b4 cmp r0, #0
 *   test +0x2d4 cmp r0, #3
 *   test +0x31c cmp r0, #255
 *   test +0x3a8 cmp r0, #1
 *   test +0x3fc cmp r0, #1
 *   test +0x438 cmp r0, #1
 *   test +0x464 cmp r1, #7
 *   test +0x494 cmp r0, #0
 *   test +0x4b4 cmp r0, #0
 *   test +0x4cc cmp r0, #0
 *   test +0x4ec cmp r0, r4
 *   test +0x530 cmp r1, r0, asr #24
 *   test +0x550 cmp r0, #2
 *   test +0x554 cmpne r0, #3
 *   test +0x558 cmpne r0, #5
 *   test +0x56c cmp r0, #0
 *   test +0x5a4 cmp r8, #0
 *   35 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02218d30; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the meaning of the fields, blocks and callee contracts the body touches is not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_0202a634(void);
extern void native_fn_020404e0(void);
extern void native_fn_022187b8(void);
extern u8 native_data27_02245e54[];
extern void native_fn_02214ff0(void);
extern u8 native_data3_02245f74[];
extern void native_fn_0221930c(void);
extern void native_fn_0221938c(void);
extern void native_fn_0205fc10(void);
extern void native_fn_0205fd0c(void);
extern u8 native_data8_0222fa08[];
extern void native_fn_022189e4(void);
extern void native_fn_02218b4c(void);
extern void native_fn_02218b60(void);
extern void native_fn_0205fd60(void);
extern void native_fn_02041538(void);
extern void native_fn_02041814(void);
extern void native_fn_02219494(void);
extern void native_fn_020406b8(void);
extern void native_fn_02214fc8(void);
extern void native_fn_020418b0(void);
extern void native_fn_02214fe0(void);
extern void native_fn_021df3bc(void);
extern void native_fn_02003edc(void);
extern void native_fn_02008c58(void);
extern void native_fn_02003f80(void);
extern void native_fn_02004078(void);
extern void native_fn_0204820c(void);
extern void native_fn_02048308(void);
extern void native_fn_02218960(void);
extern void native_fn_02218330(void);
extern void native_fn_022188cc(void);
extern void native_fn_022199b8(void);
extern void native_fn_02219c6c(void);
extern void native_fn_02045680(void);
extern void native_fn_022188ac(void);
extern void native_fn_022185b4(void);
extern void native_fn_02068ae8(void);
extern void native_fn_021f7f9c(void);
extern void native_fn_02218b74(void);
extern void native_fn_02063e38(void);
extern void native_fn_0204aeb4(void);
extern void native_fn_02219ba4(void);
extern u8 native_data_02245e94[];
extern void native_fn_02219ce4(void);
extern void native_fn_02219c88(void);
extern void native_fn_02219728(void);
extern void native_fn_022198e0(void);
extern void native_fn_0221994c(void);


asm u32 native_ov000_02218d30 (register u32 a0)
{
ov000_02218d30_L0:
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #20
    bl native_fn_0202a634
    mov r11, #0
    mov r8, r11
    bl native_fn_020404e0
    mov r4, r0
    bl native_fn_022187b8
    ldr r0, =native_data27_02245e54
    ldrb r0, [r0, #0x3]
    cmp r0, #11
    addls pc, pc, r0, lsl #2
    b ov000_02218d30_L45c
    b ov000_02218d30_L64
    b ov000_02218d30_L110
    b ov000_02218d30_L194
    b ov000_02218d30_L14c
    b ov000_02218d30_L16c
    b ov000_02218d30_L268
    b ov000_02218d30_L290
    b ov000_02218d30_L378
    b ov000_02218d30_L3a4
    b ov000_02218d30_L3d8
    b ov000_02218d30_L3f8
    b ov000_02218d30_L434
ov000_02218d30_L64:
    bl native_fn_02214ff0
    cmp r0, #1
    bne ov000_02218d30_Ld4
    mov r0, #18
    str r0, [sp]
    mov r0, #8192
    str r0, [sp, #0x4]
    mov r3, #2
    str r3, [sp, #0x8]
    mov r3, r11
    ldr r0, =native_data3_02245f74
    ldr r1, =native_fn_0221930c
    ldr r2, =native_fn_0221938c
    str r3, [sp, #0xc]
    bl native_fn_0205fc10
    ldr r5, =native_data3_02245f74
    mov r6, r0
    mov r4, #13
ov000_02218d30_Lac:
    ldmia r6!, {r0, r1, r2, r3}
    stmia r5!, {r0, r1, r2, r3}
    subs r4, r4, #1
    bne ov000_02218d30_Lac
    ldr r0, =native_data3_02245f74
    bl native_fn_0205fd0c
    ldr r0, =native_data27_02245e54
    mov r1, #1
    strb r1, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_Ld4:
    mov r0, r11
    bl native_fn_0221930c
    ldr r1, =native_data8_0222fa08
    mov r0, #255
    ldrb r1, [r1, #0x1]
    bl native_fn_022189e4
    bl native_fn_02218b4c
    bl native_fn_02218b60
    ldr r0, =native_data27_02245e54
    mov r1, r11
    str r1, [r0, #0x3c]
    str r1, [r0, #0x30]
    mov r1, #2
    strb r1, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_L110:
    bl native_fn_0205fd60
    cmp r0, #0
    bne ov000_02218d30_L45c
    bl native_fn_02214ff0
    cmp r0, #1
    ldreq r0, =native_data27_02245e54
    moveq r1, #3
    beq ov000_02218d30_L140
    ldr r0, =native_data27_02245e54
    mov r1, r11
    str r1, [r0, #0x3c]
    mov r1, #2
ov000_02218d30_L140:
    strb r1, [r0, #0x3]
    mov r8, #1
    b ov000_02218d30_L45c
ov000_02218d30_L14c:
    mov r0, r11
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, =native_data27_02245e54
    mov r1, #4
    strb r1, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_L16c:
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_02218d30_L45c
    ldr r0, =native_data27_02245e54
    mov r1, r11
    str r1, [r0, #0x3c]
    mov r1, #2
    strb r1, [r0, #0x3]
    mov r8, #1
    b ov000_02218d30_L45c
ov000_02218d30_L194:
    bl native_fn_02219494
    bl native_fn_020406b8
    cmp r0, #1
    bne ov000_02218d30_L1ac
    mov r0, #1
    bl native_fn_02214fc8
ov000_02218d30_L1ac:
    sub r0, r4, #22
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b ov000_02218d30_L1e4
    b ov000_02218d30_L1d4
    b ov000_02218d30_L1d4
    b ov000_02218d30_L1d4
    b ov000_02218d30_L1d4
    b ov000_02218d30_L1d4
    b ov000_02218d30_L1d4
ov000_02218d30_L1d4:
    mov r0, #2
    bl native_fn_02214fc8
    mov r0, #2
    bl native_fn_020418b0
ov000_02218d30_L1e4:
    cmp r4, #37
    bne ov000_02218d30_L204
    mov r0, #2
    bl native_fn_02214fc8
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
ov000_02218d30_L204:
    ldr r0, =native_data27_02245e54
    ldr r0, [r0, #0x3c]
    cmp r0, #1
    bne ov000_02218d30_L21c
    mov r0, #2
    bl native_fn_02214fc8
ov000_02218d30_L21c:
    ldr r0, =native_data8_0222fa08
    ldrb r0, [r0, #0x4]
    cmp r0, #255
    beq ov000_02218d30_L248
    mov r0, #1
    mov r1, #2
    mov r2, #30
    bl native_fn_02041538
    ldr r0, =native_data27_02245e54
    mov r1, #5
    strb r1, [r0, #0x3]
ov000_02218d30_L248:
    bl native_fn_02214fe0
    cmp r0, #0
    beq ov000_02218d30_L45c
    ldr r0, =native_data27_02245e54
    mov r1, #8
    strb r1, [r0, #0x3]
    mov r8, #1
    b ov000_02218d30_L45c
ov000_02218d30_L268:
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_02218d30_L45c
    ldr r1, =native_data8_0222fa08
    ldr r0, =native_data27_02245e54
    ldrb r3, [r1, #0x4]
    mov r2, #6
    strb r3, [r1, #0x1]
    strb r2, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_L290:
    ldr r0, =native_data8_0222fa08
    ldrb r0, [r0, #0x4]
    bl native_fn_021df3bc
    ldr r1, =native_data27_02245e54
    mov r4, r0
    ldr r0, [r1, #0x3c]
    cmp r0, #1
    bne ov000_02218d30_L2d0
    bl native_fn_02214fe0
    cmp r0, #0
    beq ov000_02218d30_L2d0
    ldr r0, =native_data27_02245e54
    mov r1, #8
    strb r1, [r0, #0x3]
    mov r8, #1
    b ov000_02218d30_L45c
ov000_02218d30_L2d0:
    bl native_fn_020404e0
    cmp r0, #3
    bne ov000_02218d30_L45c
    bl native_fn_02003edc
    mov r1, r0
    mov r0, #0
    mov r2, #8192
    bl native_fn_02008c58
    bl native_fn_02003f80
    mov r1, r0
    mov r0, #0
    mov r2, #8192
    bl native_fn_02008c58
    bl native_fn_02004078
    mov r1, r0
    mov r0, #0
    mov r2, #8192
    bl native_fn_02008c58
    ldrb r0, [r4, #0x3]
    cmp r0, #255
    bne ov000_02218d30_L340
    mov r1, #0
    add r0, sp, #16
    mov r2, #2
    strh r1, [sp, #16]
    bl native_fn_0204820c
    bl native_fn_02048308
    b ov000_02218d30_L368
ov000_02218d30_L340:
    bl native_fn_02218960
    ldr r0, =native_data8_0222fa08
    ldrb r0, [r0, #0x4]
    bl native_fn_02218330
    ldr r0, =native_data8_0222fa08
    ldrb r0, [r0, #0x4]
    bl native_fn_022188cc
    bl native_fn_02218b4c
    bl native_fn_022199b8
    bl native_fn_02219c6c
ov000_02218d30_L368:
    ldr r0, =native_data27_02245e54
    mov r1, #7
    strb r1, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_L378:
    ldr r3, =native_data8_0222fa08
    mov r4, #255
    mov r0, r11
    mov r1, #2
    mov r2, #30
    strb r4, [r3, #0x4]
    bl native_fn_02041538
    ldr r0, =native_data27_02245e54
    mov r1, #2
    strb r1, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_L3a4:
    bl native_fn_02214fe0
    cmp r0, #1
    ldrne r0, =native_data27_02245e54
    movne r1, #11
    strneb r1, [r0, #0x3]
    bne ov000_02218d30_L3d0
    ldr r1, =native_data27_02245e54
    mov r2, #9
    mov r0, r11
    strb r2, [r1, #0x3]
    bl native_fn_02045680
ov000_02218d30_L3d0:
    mov r8, #1
    b ov000_02218d30_L45c
ov000_02218d30_L3d8:
    mov r0, #1
    mov r1, #2
    mov r2, #10
    bl native_fn_02041538
    ldr r0, =native_data27_02245e54
    mov r1, #10
    strb r1, [r0, #0x3]
    b ov000_02218d30_L45c
ov000_02218d30_L3f8:
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_02218d30_L45c
    bl native_fn_022188ac
    bl native_fn_022185b4
    bl native_fn_02068ae8
    bl native_fn_021f7f9c
    ldr r1, =native_data27_02245e54
    mov r3, #11
    ldr r0, =native_data8_0222fa08
    mov r2, #16
    strb r3, [r1, #0x3]
    strb r2, [r0, #0x2]
    mov r8, #1
    b ov000_02218d30_L45c
ov000_02218d30_L434:
    bl native_fn_02041814
    cmp r0, #1
    beq ov000_02218d30_L45c
    bl native_fn_022188ac
    bl native_fn_022185b4
    ldr r0, =native_data27_02245e54
    mov r1, #12
    strb r1, [r0, #0x3]
    bl native_fn_02214fe0
    mov r11, r0
ov000_02218d30_L45c:
    ldr r0, =native_data27_02245e54
    ldrb r1, [r0, #0x3]
    cmp r1, #7
    addls pc, pc, r1, lsl #2
    b ov000_02218d30_L548
    b ov000_02218d30_L548
    b ov000_02218d30_L548
    b ov000_02218d30_L490
    b ov000_02218d30_L490
    b ov000_02218d30_L490
    b ov000_02218d30_L548
    b ov000_02218d30_L548
    b ov000_02218d30_L490
ov000_02218d30_L490:
    ldr r0, [r0, #0x18]
    cmp r0, #0
    beq ov000_02218d30_L4ac
    bl native_fn_02218b74
    ldr r0, =native_data27_02245e54
    mov r1, #0
    str r1, [r0, #0x18]
ov000_02218d30_L4ac:
    ldr r0, =native_data27_02245e54
    ldr r0, [r0, #0x14]
    cmp r0, #0
    beq ov000_02218d30_L548
    bl native_fn_02063e38
    mov r10, r0
    ldrsh r0, [r10, #100]
    mov r9, #0
    cmp r0, #0
    ble ov000_02218d30_L53c
    ldr r5, =native_data27_02245e54
    mov r7, #1
    mov r6, #2
    mvn r4, #0
ov000_02218d30_L4e4:
    add r1, r10, r9
    ldrb r0, [r1, #0x68]
    cmp r0, r4
    beq ov000_02218d30_L524
    mov r0, r0, lsl #24
    str r7, [sp]
    mov r0, r0, asr #24
    str r0, [sp, #0x4]
    ldrsb r0, [r1, #112]
    mov r1, r7
    mov r2, r6
    str r0, [sp, #0x8]
    str r7, [sp, #0xc]
    ldr r0, [r5, #0x4]
    mov r3, r7
    bl native_fn_0204aeb4
ov000_02218d30_L524:
    ldrsh r1, [r10, #100]
    add r0, r9, #1
    mov r0, r0, lsl #24
    cmp r1, r0, asr #24
    mov r9, r0, asr #24
    bgt ov000_02218d30_L4e4
ov000_02218d30_L53c:
    ldr r0, =native_data27_02245e54
    mov r1, #0
    str r1, [r0, #0x14]
ov000_02218d30_L548:
    ldr r0, =native_data27_02245e54
    ldrb r0, [r0, #0x3]
    cmp r0, #2
    cmpne r0, #3
    cmpne r0, #5
    bne ov000_02218d30_L598
    bl native_fn_022199b8
    ldr r0, =native_data27_02245e54
    ldrb r0, [r0, #0x3]
    cmp r0, #0
    beq ov000_02218d30_L57c
    bl native_fn_02219ba4
    b ov000_02218d30_L580
ov000_02218d30_L57c:
    bl native_fn_02219c6c
ov000_02218d30_L580:
    ldr r0, =native_data_02245e94
    bl native_fn_02219ce4
    bl native_fn_02219c88
    bl native_fn_02219728
    bl native_fn_022198e0
    bl native_fn_0221994c
ov000_02218d30_L598:
    ldr r0, =0x02101ae8
    mov r1, #1
    str r1, [r0, #0xc84]
    cmp r8, #0
    beq ov000_02218d30_L5b4
    bl ov000_02218d30_L0
    mov r11, r0
ov000_02218d30_L5b4:
    mov r0, r11
    add sp, sp, #20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
