/* ov001 row 0x022170f4: 1772 bytes.
 *
 * What it does: 440 instructions; 72 call(s) to 0x021f1294, 0x021f1354, 0x021f1438, +69 more; loops (back edge at +0x3c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 72 calls (440 instructions, 72 calls, 56 branches, 72 back edges, 3 literal slots).
 *
 *   pool +0x6e0 -> constant 0x02242bf4 (image word 0x02242bf4)
 *   pool +0x6e4 -> constant 0x02242bf8 (image word 0x02242bf8)
 *   pool +0x6e8 -> constant 0x02242c04 (image word 0x02242c04)
 *   branch +0x30 -> +0x1f4
 *   branch +0x78 -> +0x8c
 *   branch +0x88 -> +0x6d4
 *   branch +0x98 -> +0x114
 *   branch +0xa4 -> +0xb4
 *   branch +0xb0 -> +0xbc
 *   branch +0x110 -> +0x11c
 *   branch +0x12c -> +0x178
 *   branch +0x174 -> +0x6d4
 *   branch +0x184 -> +0x1dc
 *   branch +0x1d8 -> +0x6d4
 *   branch +0x1f0 -> +0x6d4
 *   branch +0x1f8 -> +0x2a0
 *   branch +0x238 -> +0x6d4
 *   branch +0x258 -> +0x270
 *   branch +0x26c -> +0x290
 *   branch +0x278 -> +0x290
 *   branch +0x29c -> +0x6d4
 *   branch +0x2a4 -> +0x308
 *   branch +0x2e4 -> +0x6d4
 *   branch +0x304 -> +0x6d4
 *   branch +0x30c -> +0x444
 *   branch +0x328 -> +0x3a8
 *   branch +0x36c -> +0x384
 *   back edge +0x38c -> +0x350
 *   branch +0x3a4 -> +0x6d4
 *   branch +0x3b0 -> +0x430
 *   branch +0x3f4 -> +0x40c
 *   back edge +0x414 -> +0x3d8
 *   branch +0x42c -> +0x6d4
 *   branch +0x440 -> +0x6d4
 *   branch +0x448 -> +0x510
 *   branch +0x458 -> +0x468
 *   branch +0x464 -> +0x6d4
 *   branch +0x478 -> +0x488
 *   branch +0x484 -> +0x6d4
 *   branch +0x498 -> +0x4a8
 *   branch +0x4a4 -> +0x6d4
 *   branch +0x4c4 -> +0x4d0
 *   back edge +0x4d8 -> +0x4b0
 *   branch +0x4e8 -> +0x4f8
 *   branch +0x4f4 -> +0x500
 *   branch +0x50c -> +0x6d4
 *   branch +0x514 -> +0x65c
 *   branch +0x548 -> +0x608
 *   branch +0x554 -> +0x564
 *   branch +0x560 -> +0x570
 *   branch +0x56c -> +0x578
 *   branch +0x5a0 -> +0x5e0
 *   branch +0x5dc -> +0x608
 *   back edge +0x614 -> +0x53c
 *   branch +0x61c -> +0x62c
 *   branch +0x634 -> +0x644
 *   branch +0x658 -> +0x6d4
 *   branch +0x660 -> +0x684
 *   branch +0x680 -> +0x6d4
 *   branch +0x688 -> +0x6b4
 *   branch +0x6a0 -> +0x6d4
 *   branch +0x6b0 -> +0x6d4
 *   branch +0x6b8 -> +0x6d4
 *   test +0x18 cmp r0, #0
 *   test +0x2c cmp r1, #0
 *   test +0x74 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xa0 cmp r0, #0
 *   test +0xec cmp r0, #0
 *   test +0xf8 cmp r0, #1
 *   test +0x128 cmp r0, #38
 *   test +0x178 cmp r0, #193
 *   test +0x17c cmpne r0, #190
 *   test +0x1f4 cmp r1, #5
 *   test +0x230 cmp r4, r5, asr #12
 *   test +0x234 cmphi r0, r5, asr #12
 *   test +0x254 cmp r1, #38
 *   test +0x270 cmp r1, #193
 *   test +0x274 cmpne r1, #190
 *   test +0x2a0 cmp r1, #10
 *   test +0x2dc cmp r4, r5, asr #12
 *   test +0x2e0 cmphi r0, r5, asr #12
 *   test +0x308 cmp r1, #20
 *   test +0x324 cmp r1, #249
 *   test +0x364 cmp r0, #0
 *   test +0x388 cmp r9, #3
 *   test +0x3a8 cmp r1, #193
 *   test +0x3ac cmpne r1, #190
 *   test +0x3ec cmp r0, #0
 *   test +0x410 cmp r10, #3
 *   test +0x444 cmp r1, #25
 *   test +0x454 cmp r0, r1
 *   test +0x460 cmp r0, #0
 *   test +0x474 cmp r0, r1
 *   test +0x480 cmp r0, #0
 *   test +0x494 cmp r0, r1
 *   test +0x4a0 cmp r0, #0
 *   test +0x4c0 cmp r0, #0
 *   test +0x4d4 cmp r6, #3
 *   test +0x4e4 cmp r0, #249
 *   test +0x510 cmp r1, #30
 *   test +0x544 cmp r0, #0
 *   test +0x550 cmp r0, #0
 *   test +0x55c cmp r0, #0
 *   test +0x59c cmp r0, #0
 *   test +0x610 cmp r7, #3
 *   test +0x618 cmp r11, #0
 *   test +0x630 cmp r0, #0
 *   test +0x65c cmp r1, #40
 *   test +0x674 cmp r1, #30
 *   test +0x684 cmp r1, #50
 *   test +0x69c cmp r0, #0
 *   test +0x6b4 cmp r1, #100
 *   0 block transfer(s), 32 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022170f4; the literal pool and
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

extern void native_fn_021f1294(void);
extern void native_fn_021f1354(void);
extern void native_fn_021f1438(void);
extern void native_fn_0220f9a4(void);
extern void native_fn_021dbaac(void);
extern void native_fn_021d75d4(void);
extern void native_fn_02042c2c(void);
extern void native_fn_021d77b0(void);
extern void native_fn_02041f74(void);
extern void native_fn_021d7814(void);
extern void native_fn_021d94cc(void);
extern void native_fn_021d7e80(void);
extern void native_fn_021d9494(void);
extern void native_fn_022168ac(void);
extern void native_fn_0205d790(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021f94d8(void);
extern void native_fn_021d9534(void);
extern void native_fn_0205d718(void);
extern void native_fn_022168d0(void);
extern void native_fn_021f14a4(void);
extern void native_fn_021d7f54(void);
extern void native_fn_021db438(void);
extern void native_fn_021db8d0(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_020444a8(void);
extern void native_fn_0207b708(void);
extern void native_fn_0207b728(void);
extern void native_fn_021d908c(void);
extern void native_fn_02210ad0(void);
extern void native_fn_021dbf98(void);
extern void native_fn_021e2078(void);
extern void native_fn_021ee7b0(void);
extern void native_fn_021f949c(void);
extern void native_fn_02216ac4(void);
extern void native_fn_021f1324(void);


asm u32 native_ov001_022170f4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #8
    mov r10, r0
    ldrb r0, [r10, #0x31e]
    mov r9, r1
    mov r8, r2
    cmp r0, #0
    ldr r0, =0x02242bf4
    moveq r4, #1
    ldrb r1, [r0, #0x8]
    movne r4, #0
    cmp r1, #0
    bne ov001_022170f4_L1f4
    mov r0, #16
    mov r1, #2
    bl native_fn_021f1294
    ldr r1, =0x02242bf4
    mov r0, #11
    ldrb r2, [r1, #0x9]
    mov r1, #0
    mov r3, #1
    bl native_fn_021f1354
    mov r0, #2
    bl native_fn_021f1438
    ldr r0, [r10, #0x1e8]
    ldr r2, =0x02242bf8
    add r0, r0, #70
    mov r1, #0
    bl native_fn_0220f9a4
    cmp r0, #0
    beq ov001_022170f4_L8c
    ldr r0, =0x02242bf4
    mov r1, #50
    strb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L8c:
    mov r0, r10
    bl native_fn_021dbaac
    cmp r0, #0
    beq ov001_022170f4_L114
    ldrb r0, [r10, #0x31e]
    cmp r0, #0
    bne ov001_022170f4_Lb4
    mov r0, #41
    bl native_fn_021d75d4
    b ov001_022170f4_Lbc
ov001_022170f4_Lb4:
    mov r0, #37
    bl native_fn_021d75d4
ov001_022170f4_Lbc:
    mov r0, r10
    bl native_fn_02042c2c
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d77b0
    mov r0, r10
    mov r1, #0
    bl native_fn_02041f74
    mov r1, r0
    mvn r0, #0
    bl native_fn_021d7814
    ldrb r0, [r10, #0x31e]
    cmp r0, #0
    moveq r1, #1
    movne r1, #0
    cmp r0, #1
    moveq r2, #1
    movne r2, #0
    and r0, r1, #255
    and r1, r2, #255
    bl native_fn_021d94cc
    b ov001_022170f4_L11c
ov001_022170f4_L114:
    mov r0, r10
    bl native_fn_021d7e80
ov001_022170f4_L11c:
    ldr r0, =0x02242bf4
    mov r2, #1
    ldrb r0, [r0, #0x9]
    cmp r0, #38
    bne ov001_022170f4_L178
    mov r0, r10
    mov r1, #2
    bl native_fn_021d9494
    mov r0, #5
    bl native_fn_022168ac
    mov r0, #5
    bl native_fn_0205d790
    mov r2, r0
    mov r1, r10
    mov r0, #5
    bl native_fn_021eec7c
    ldr r1, =0x02242bf4
    mov r2, #5
    str r0, [r1, #0x10]
    strb r2, [r1, #0x8]
    mov r0, #0
    strb r0, [r1]
    b ov001_022170f4_L6d4
ov001_022170f4_L178:
    cmp r0, #193
    cmpne r0, #190
    mov r0, r10
    bne ov001_022170f4_L1dc
    mov r1, #3
    bl native_fn_021d9494
    mov r0, #11
    bl native_fn_022168ac
    mov r0, #11
    bl native_fn_0205d790
    mov r2, r0
    mov r1, r10
    mov r0, #11
    bl native_fn_021eec7c
    ldr r2, =0x02242bf4
    mov r1, #1
    str r0, [r2, #0x10]
    mov r0, #153
    bl native_fn_021f94d8
    ldr r0, =0x02242bf4
    mov r1, #5
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0]
    b ov001_022170f4_L6d4
ov001_022170f4_L1dc:
    mov r1, #2
    bl native_fn_021d9494
    ldr r0, =0x02242bf4
    mov r1, #10
    strb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L1f4:
    cmp r1, #5
    bne ov001_022170f4_L2a0
    ldr r1, [r10, #0x60]
    mov r0, r10
    ldr r5, [r1]
    mvn r1, #0
    mov r2, #6
    mov r3, #0
    bl native_fn_021d9534
    mov r4, r0
    mov r0, r10
    mvn r1, #0
    mov r2, #8
    mov r3, #0
    bl native_fn_021d9534
    cmp r4, r5, asr #12
    cmphi r0, r5, asr #12
    bhi ov001_022170f4_L6d4
    mov r1, #0
    mov r0, r10
    mov r2, r1
    bl native_fn_021d9494
    ldr r0, =0x02242bf4
    ldrb r1, [r0, #0x9]
    cmp r1, #38
    bne ov001_022170f4_L270
    ldr r0, [r0, #0x10]
    bl native_fn_0205d718
    mov r0, #5
    bl native_fn_022168d0
    b ov001_022170f4_L290
ov001_022170f4_L270:
    cmp r1, #193
    cmpne r1, #190
    bne ov001_022170f4_L290
    ldr r0, =0x02242bf4
    ldr r0, [r0, #0x10]
    bl native_fn_0205d718
    mov r0, #11
    bl native_fn_022168d0
ov001_022170f4_L290:
    ldr r0, =0x02242bf4
    mov r1, #20
    strb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L2a0:
    cmp r1, #10
    bne ov001_022170f4_L308
    ldr r1, [r10, #0x60]
    mov r0, r10
    ldr r5, [r1]
    mvn r1, #0
    mov r2, #6
    mov r3, #0
    bl native_fn_021d9534
    mov r4, r0
    mov r0, r10
    mvn r1, #0
    mov r2, #8
    mov r3, #0
    bl native_fn_021d9534
    cmp r4, r5, asr #12
    cmphi r0, r5, asr #12
    bhi ov001_022170f4_L6d4
    mov r1, #0
    mov r0, r10
    mov r2, r1
    bl native_fn_021d9494
    ldr r0, =0x02242bf4
    mov r1, #20
    strb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L308:
    cmp r1, #20
    bne ov001_022170f4_L444
    bl native_fn_021f14a4
    mov r0, r4
    bl native_fn_021d7f54
    ldr r0, =0x02242bf4
    ldrb r1, [r0, #0x9]
    cmp r1, #249
    bne ov001_022170f4_L3a8
    mov r0, #87
    bl native_fn_022168ac
    mov r0, #87
    bl native_fn_0205d790
    ldr r6, =0x02242c04
    mov r10, r0
    mov r9, #0
    mvn r5, #0
    mov r7, #87
ov001_022170f4_L350:
    mov r0, r4
    mov r1, r9
    bl native_fn_021db438
    mov r8, r0
    bl native_fn_021db8d0
    cmp r0, #0
    streq r5, [r6, r9, lsl #2]
    beq ov001_022170f4_L384
    mov r0, r7
    mov r1, r8
    mov r2, r10
    bl native_fn_021eec7c
    str r0, [r6, r9, lsl #2]
ov001_022170f4_L384:
    add r9, r9, #1
    cmp r9, #3
    blt ov001_022170f4_L350
    ldr r0, =0x02242bf4
    mov r1, #25
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0]
    b ov001_022170f4_L6d4
ov001_022170f4_L3a8:
    cmp r1, #193
    cmpne r1, #190
    bne ov001_022170f4_L430
    mov r0, #174
    bl native_fn_022168ac
    mov r0, #174
    bl native_fn_0205d790
    ldr r6, =0x02242c04
    mov r9, r0
    mov r10, #0
    mvn r5, #0
    mov r7, #174
ov001_022170f4_L3d8:
    mov r0, r4
    mov r1, r10
    bl native_fn_021db438
    mov r8, r0
    bl native_fn_021db8d0
    cmp r0, #0
    streq r5, [r6, r10, lsl #2]
    beq ov001_022170f4_L40c
    mov r0, r7
    mov r1, r8
    mov r2, r9
    bl native_fn_021eec7c
    str r0, [r6, r10, lsl #2]
ov001_022170f4_L40c:
    add r10, r10, #1
    cmp r10, #3
    blt ov001_022170f4_L3d8
    ldr r0, =0x02242bf4
    mov r1, #25
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0]
    b ov001_022170f4_L6d4
ov001_022170f4_L430:
    mov r1, #30
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0]
    b ov001_022170f4_L6d4
ov001_022170f4_L444:
    cmp r1, #25
    bne ov001_022170f4_L510
    ldr r0, [r0, #0x10]
    mvn r1, #0
    cmp r0, r1
    beq ov001_022170f4_L468
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_022170f4_L6d4
ov001_022170f4_L468:
    ldr r0, =0x02242bf4
    mvn r1, #0
    ldr r0, [r0, #0x14]
    cmp r0, r1
    beq ov001_022170f4_L488
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_022170f4_L6d4
ov001_022170f4_L488:
    ldr r0, =0x02242bf4
    mvn r1, #0
    ldr r0, [r0, #0x18]
    cmp r0, r1
    beq ov001_022170f4_L4a8
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_022170f4_L6d4
ov001_022170f4_L4a8:
    ldr r5, =0x02242c04
    mov r6, #0
ov001_022170f4_L4b0:
    mov r0, r4
    mov r1, r6
    bl native_fn_021db438
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022170f4_L4d0
    ldr r0, [r5, r6, lsl #2]
    bl native_fn_0205d718
ov001_022170f4_L4d0:
    add r6, r6, #1
    cmp r6, #3
    blt ov001_022170f4_L4b0
    ldr r0, =0x02242bf4
    ldrb r0, [r0, #0x9]
    cmp r0, #249
    bne ov001_022170f4_L4f8
    mov r0, #87
    bl native_fn_022168d0
    b ov001_022170f4_L500
ov001_022170f4_L4f8:
    mov r0, #174
    bl native_fn_022168d0
ov001_022170f4_L500:
    ldr r0, =0x02242bf4
    mov r1, #30
    strb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L510:
    cmp r1, #30
    bne ov001_022170f4_L65c
    mov r11, #0
    mov r0, r4
    mov r1, r11
    str r11, [sp, #0x4]
    bl native_fn_021db438
    ldr r4, =0x02242bf4
    mov r6, r0
    mov r7, r11
    mvn r5, #0
ov001_022170f4_L53c:
    mov r0, r6
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022170f4_L608
    ldrb r0, [r6, #0x31e]
    cmp r0, #0
    beq ov001_022170f4_L564
    bl native_fn_020444a8
    cmp r0, #0
    beq ov001_022170f4_L570
ov001_022170f4_L564:
    ldrb r0, [r4, #0x9]
    bl native_fn_0207b708
    b ov001_022170f4_L578
ov001_022170f4_L570:
    ldrb r0, [r4, #0x9]
    bl native_fn_0207b728
ov001_022170f4_L578:
    ldr r1, [r6, #0x1e8]
    mov r2, #0
    add r1, r8, r1
    ldrb r1, [r1, #0x86]
    bl native_fn_021d908c
    mov r2, r0
    mov r0, r10
    mov r1, #100
    bl native_fn_02210ad0
    cmp r0, #0
    beq ov001_022170f4_L5e0
    mov r0, r6
    mov r1, #4
    mov r2, #1
    bl native_fn_021d9494
    mov r0, #0
    str r0, [sp]
    mov r0, r6
    mov r1, r9
    mov r2, #1
    mov r3, #0
    bl native_fn_021dbf98
    mov r0, r6
    bl native_fn_021e2078
    mov r11, #1
    b ov001_022170f4_L608
ov001_022170f4_L5e0:
    mov r0, #0
    strb r0, [r6, #0x357]
    str r0, [sp]
    mov r0, #1
    str r0, [sp, #0x4]
    mov r0, r6
    mov r1, #0
    mov r2, r5
    mov r3, #1
    bl native_fn_021ee7b0
ov001_022170f4_L608:
    add r6, r6, #1088
    add r7, r7, #1
    cmp r7, #3
    blt ov001_022170f4_L53c
    cmp r11, #0
    beq ov001_022170f4_L62c
    mov r0, #238
    mov r1, #1
    bl native_fn_021f949c
ov001_022170f4_L62c:
    ldr r0, [sp, #0x4]
    cmp r0, #0
    beq ov001_022170f4_L644
    mov r0, #242
    mov r1, #1
    bl native_fn_021f949c
ov001_022170f4_L644:
    ldr r0, =0x02242bf4
    mov r1, #40
    strb r1, [r0, #0x8]
    mov r1, #0
    strb r1, [r0]
    b ov001_022170f4_L6d4
ov001_022170f4_L65c:
    cmp r1, #40
    bne ov001_022170f4_L684
    ldrsb r1, [r0]
    add r1, r1, #1
    strb r1, [r0]
    ldrsb r1, [r0]
    cmp r1, #30
    movgt r1, #100
    strgtb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L684:
    cmp r1, #50
    bne ov001_022170f4_L6b4
    ldrb r1, [r0, #0x4]
    mov r0, r10
    mov r2, #1
    bl native_fn_02216ac4
    cmp r0, #0
    beq ov001_022170f4_L6d4
    ldr r0, =0x02242bf4
    mov r1, #100
    strb r1, [r0, #0x8]
    b ov001_022170f4_L6d4
ov001_022170f4_L6b4:
    cmp r1, #100
    bne ov001_022170f4_L6d4
    mov r1, #0
    strb r1, [r0, #0x8]
    bl native_fn_021f1324
    add sp, sp, #8
    mov r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov001_022170f4_L6d4:
    mov r0, #0
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
