/* ov001 row 0x021fa430: 1148 bytes.
 *
 * What it does: 281 instructions; 32 call(s) to 0x021fa164, 0x0202ac08, 0x0207b674, +29 more; loops (back edge at +0x24); returns through pop {r4, r5, pc}; 6 literal slot(s) in the extent
 *
 * Decoded shape: loop with 32 calls (281 instructions, 32 calls, 17 branches, 27 back edges, 6 literal slots).
 *
 *   pool +0x464 -> constant 0x02239a14 (image word 0x02239a14)
 *   pool +0x468 -> constant 0x02239a5c (image word 0x02239a5c)
 *   pool +0x46c -> native_data_0222ed28 (image word 0x0222ed28)
 *   pool +0x470 -> constant 0x00000438 (image word 0x00000438)
 *   pool +0x474 -> constant 0x00000ccd (image word 0x00000ccd)
 *   pool +0x478 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x18 -> +0xa4
 *   branch +0x4c -> +0x5c
 *   branch +0x68 -> +0x80
 *   branch +0xb0 -> +0x2a0
 *   branch +0xfc -> +0x278
 *   branch +0x114 -> +0x128
 *   branch +0x124 -> +0x268
 *   branch +0x1b8 -> +0x1e0
 *   branch +0x204 -> +0x238
 *   branch +0x250 -> +0x260
 *   branch +0x274 -> +0x284
 *   branch +0x2ac -> +0x30c
 *   branch +0x318 -> +0x3a0
 *   branch +0x370 -> +0x3a0
 *   branch +0x3ac -> +0x3c0
 *   branch +0x3cc -> +0x3fc
 *   branch +0x3e0 -> +0x3f0
 *   branch +0x3ec -> +0x3fc
 *   branch +0x408 -> +0x458
 *   branch +0x444 -> +0x450
 *   test +0x10 cmp r0, #0
 *   test +0x14 cmpne r0, #5
 *   test +0x48 cmp r0, #0
 *   test +0x64 cmp r0, #0
 *   test +0xac cmp r0, #10
 *   test +0xf4 cmp r4, r2, asr #12
 *   test +0x110 cmp r0, #0
 *   test +0x1b0 cmp r5, #0
 *   test +0x200 cmp r0, #0
 *   test +0x23c cmp r5, #20
 *   test +0x254 cmp r5, #0
 *   test +0x278 cmp r4, r0
 *   test +0x294 cmp r4, r0
 *   test +0x2a8 cmp r1, #20
 *   test +0x314 cmp r1, #30
 *   test +0x340 cmp r0, #10
 *   test +0x368 cmp r0, #1000
 *   test +0x36c cmple r1, r3
 *   test +0x378 cmp r0, #1000
 *   test +0x3a8 cmp r1, #40
 *   test +0x3c8 cmp r0, #50
 *   test +0x3dc cmp r0, r1
 *   test +0x3e8 cmp r0, #0
 *   test +0x404 cmp r1, #100
 *   test +0x440 cmp r0, #0
 *   0 block transfer(s), 25 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fa430; the literal pool and
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

extern void native_fn_021fa164(void);
extern void native_fn_0202ac08(void);
extern void native_fn_0207b674(void);
extern void native_fn_021eea10(void);
extern u8 native_data_0222ed28[];
extern void native_fn_021d9534(void);
extern void native_fn_021e1468(void);
extern void native_fn_021f949c(void);
extern void native_fn_021e9b84(void);
extern void native_fn_021eec7c(void);
extern void native_fn_021d9494(void);
extern void native_fn_021f07dc(void);
extern void native_fn_02041510(void);
extern void native_fn_021d78a4(void);
extern void native_fn_021dc59c(void);
extern void native_fn_0205d790(void);
extern void native_fn_021fa290(void);
extern void native_fn_02212aac(void);
extern void native_fn_0205d6f4(void);
extern void native_fn_021dc940(void);
extern void native_fn_021eeb70(void);
extern void native_fn_0202ac4c(void);


asm u32 native_ov001_021fa430 (register u32 a0)
{
    stmdb sp!, {r4, r5, lr}
    sub sp, sp, #12
    ldr r0, =0x02239a14
    ldrb r0, [r0, #0x17]
    cmp r0, #0
    cmpne r0, #5
    bne ov001_021fa430_La4
    ldr r0, =0x02239a14
    ldrb r0, [r0, #0xc]
    bl native_fn_021fa164
    ldr r0, =0x02239a5c
    bl native_fn_0202ac08
    ldr r1, =0x02239a14
    mov r0, #48
    ldr r1, [r1, #0x40]
    ldr r1, [r1, #0x1e8]
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_021fa430_L5c
    mov r0, #180
    mov r1, #0
    bl native_fn_021eea10
ov001_021fa430_L5c:
    ldr r1, =0x02239a14
    ldrb r0, [r1, #0x17]
    cmp r0, #0
    bne ov001_021fa430_L80
    mov r3, #0
    ldr r0, =native_data_0222ed28
    sub r2, r3, #1
    str r3, [r1, #0x30]
    strb r2, [r0, #0x2]
ov001_021fa430_L80:
    ldr r1, =0x02239a14
    mov r2, #10
    ldr r0, [r1, #0x34]
    ldr r0, [r0, #0x60]
    ldr r0, [r0]
    mov r0, r0, lsl #4
    mov r0, r0, asr #16
    str r0, [r1, #0x44]
    strb r2, [r1, #0x17]
ov001_021fa430_La4:
    ldr r1, =0x02239a14
    ldrb r0, [r1, #0x17]
    cmp r0, #10
    bne ov001_021fa430_L2a0
    ldr r0, [r1, #0x34]
    ldr r3, [r1, #0x44]
    mvn r1, #0
    mov r2, #1
    bl native_fn_021d9534
    ldr r1, =0x02239a14
    mov r4, r0
    ldr r0, [r1, #0x34]
    ldr r3, [r1, #0x44]
    mvn r1, #0
    mov r2, #6
    bl native_fn_021d9534
    ldr r1, =0x02239a14
    ldr r3, [r1, #0x34]
    ldr r2, [r3, #0x60]
    ldr r2, [r2]
    cmp r4, r2, asr #12
    mov r4, r2, asr #12
    bne ov001_021fa430_L278
    ldr r1, [r1, #0x40]
    mov r0, r3
    mov r2, #0
    bl native_fn_021e1468
    cmp r0, #0
    beq ov001_021fa430_L128
    mov r0, #228
    mov r1, #1
    bl native_fn_021f949c
    b ov001_021fa430_L268
ov001_021fa430_L128:
    ldr r0, =0x02239a14
    mov r1, #0
    ldr r0, [r0, #0x34]
    bl native_fn_021e9b84
    ldr r1, =0x02239a14
    mov r5, r0
    ldr r1, [r1, #0x40]
    mov r0, #60
    mov r2, #1
    bl native_fn_021eec7c
    ldr r1, =0x02239a14
    mov r0, #61
    ldr r1, [r1, #0x40]
    mov r2, #1
    bl native_fn_021eec7c
    mov r0, #62
    ldr r1, =0x02239a14
    mov r2, #1
    ldr r1, [r1, #0x40]
    bl native_fn_021eec7c
    ldr r0, =0x02239a14
    mov r1, #4
    ldr r0, [r0, #0x40]
    mov r2, #1
    bl native_fn_021d9494
    mov r2, #0
    str r2, [sp]
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    ldr r1, =0x02239a14
    mov r3, r5
    ldr r0, [r1, #0x34]
    ldr r1, [r1, #0x40]
    bl native_fn_021f07dc
    cmp r5, #0
    mov r5, r0
    beq ov001_021fa430_L1e0
    mov r0, #0
    mov r1, #3
    mov r2, #20
    bl native_fn_02041510
    ldr r1, =0x00000438
    ldr r3, =0x00000ccd
    mov r0, #0
    mov r2, #100
    bl native_fn_021d78a4
ov001_021fa430_L1e0:
    ldr r0, =0x02239a14
    mov r1, #0
    ldr r0, [r0, #0x40]
    bl native_fn_021dc59c
    ldr r0, =0x02239a14
    ldr r0, [r0, #0x40]
    add r0, r0, #768
    ldrh r0, [r0, #76]
    cmp r0, #0
    beq ov001_021fa430_L238
    bl native_fn_0205d790
    ldr r1, =0x02239a14
    mov r2, r0
    ldr r1, [r1, #0x40]
    add r0, r1, #768
    ldrh r0, [r0, #76]
    bl native_fn_021eec7c
    ldr r0, =0x02239a14
    mov r1, #0
    ldr r0, [r0, #0x40]
    add r0, r0, #768
    strh r1, [r0, #76]
ov001_021fa430_L238:
    ldr r0, =0x02239a14
    cmp r5, #20
    ldr r1, [r0, #0x30]
    add r1, r1, r5
    str r1, [r0, #0x30]
    movge r0, #239
    bge ov001_021fa430_L260
    cmp r5, #0
    movgt r0, #238
    movle r0, #242
ov001_021fa430_L260:
    mov r1, #1
    bl native_fn_021f949c
ov001_021fa430_L268:
    ldr r0, =0x02239a14
    add r1, r4, #1
    str r1, [r0, #0x44]
    b ov001_021fa430_L284
ov001_021fa430_L278:
    cmp r4, r0
    moveq r0, #40
    streqb r0, [r1, #0x17]
ov001_021fa430_L284:
    ldr r1, =0x02239a14
    ldr r0, [r1, #0x34]
    add r0, r0, #768
    ldrh r0, [r0, #70]
    cmp r4, r0
    movge r0, #20
    strgeb r0, [r1, #0x17]
ov001_021fa430_L2a0:
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x17]
    cmp r1, #20
    bne ov001_021fa430_L30c
    ldr r1, [r0, #0x40]
    mov r0, #63
    mov r2, #1
    bl native_fn_021eec7c
    ldr r2, =0x02239a14
    ldr r3, =native_data_0222ed28
    ldr r1, [r2, #0x40]
    strb r0, [r3, #0x2]
    ldr r0, [r2, #0x34]
    ldr r2, [r2, #0x30]
    bl native_fn_021fa290
    ldr r2, =0x02239a14
    ldr r1, =0x66666667
    strh r0, [r2, #30]
    ldrsh r5, [r2, #30]
    mov r4, #0
    mov r3, #30
    smull r0, r12, r1, r5
    mov r0, r5, lsr #31
    add r12, r0, r12, asr #2
    strh r12, [r2, #34]
    strh r4, [r2, #28]
    strb r3, [r2, #0x17]
ov001_021fa430_L30c:
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x17]
    cmp r1, #30
    bne ov001_021fa430_L3a0
    ldrsh r2, [r0, #38]
    ldrsh r1, [r0, #28]
    ldrsb r0, [r0, #16]
    add r1, r2, r1
    bl native_fn_02212aac
    ldr r0, =0x02239a14
    ldrsh r3, [r0, #30]
    ldrsh r0, [r0, #28]
    sub r0, r3, r0
    cmp r0, #10
    ldr r0, =0x02239a14
    movgt r2, #11
    ldrsh r1, [r0, #28]
    movle r2, #1
    add r1, r1, r2
    strh r1, [r0, #28]
    ldrsh r1, [r0, #28]
    ldrsh r2, [r0, #38]
    add r0, r2, r1
    cmp r0, #1000
    cmple r1, r3
    ble ov001_021fa430_L3a0
    add r0, r2, r3
    cmp r0, #1000
    ldr r1, =0x02239a14
    movge r0, #1000
    strh r0, [r1, #38]
    ldrsb r0, [r1, #16]
    ldrsh r1, [r1, #38]
    bl native_fn_02212aac
    ldr r0, =0x02239a14
    mov r1, #50
    strb r1, [r0, #0x17]
ov001_021fa430_L3a0:
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x17]
    cmp r1, #40
    bne ov001_021fa430_L3c0
    mov r1, #5
    strb r1, [r0, #0x17]
    mov r1, #6
    strb r1, [r0, #0xa]
ov001_021fa430_L3c0:
    ldr r0, =0x02239a14
    ldrb r0, [r0, #0x17]
    cmp r0, #50
    bne ov001_021fa430_L3fc
    ldr r0, =native_data_0222ed28
    mvn r1, #0
    ldrsb r0, [r0, #2]
    cmp r0, r1
    beq ov001_021fa430_L3f0
    bl native_fn_0205d6f4
    cmp r0, #0
    bne ov001_021fa430_L3fc
ov001_021fa430_L3f0:
    ldr r0, =0x02239a14
    mov r1, #100
    strb r1, [r0, #0x17]
ov001_021fa430_L3fc:
    ldr r0, =0x02239a14
    ldrb r1, [r0, #0x17]
    cmp r1, #100
    bne ov001_021fa430_L458
    ldr r0, [r0, #0x34]
    mov r1, #8
    bl native_fn_021dc940
    ldr r0, =0x02239a14
    mov r1, #0
    strb r1, [r0, #0x17]
    mov r1, #9
    strb r1, [r0, #0xa]
    ldr r1, [r0, #0x40]
    mov r0, #48
    ldr r1, [r1, #0x1e8]
    add r1, r1, #70
    bl native_fn_0207b674
    cmp r0, #0
    ble ov001_021fa430_L450
    mov r0, #180
    bl native_fn_021eeb70
ov001_021fa430_L450:
    ldr r0, =0x02239a5c
    bl native_fn_0202ac4c
ov001_021fa430_L458:
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, pc}
}
