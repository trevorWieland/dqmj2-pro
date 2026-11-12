/* ov001 row 0x02200d54: 1132 bytes.
 *
 * What it does: 280 instructions; 48 call(s) to 0x02202360, 0x02202360, 0x021db438, +45 more; loops (back edge at +0x60); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: loop with 48 calls (280 instructions, 48 calls, 28 branches, 26 back edges, 3 literal slots).
 *
 *   pool +0x460 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x464 -> native_data_0222edc8 (image word 0x0222edc8)
 *   pool +0x468 -> native_data_0222edcc (image word 0x0222edcc)
 *   branch +0x3c -> +0x458
 *   branch +0x40 -> +0x458
 *   branch +0x44 -> +0x58
 *   branch +0x48 -> +0x3bc
 *   branch +0x4c -> +0x458
 *   branch +0x50 -> +0x274
 *   branch +0x54 -> +0x440
 *   branch +0xa4 -> +0x458
 *   branch +0xdc -> +0x160
 *   branch +0xfc -> +0x118
 *   branch +0x114 -> +0x12c
 *   branch +0x15c -> +0x458
 *   branch +0x170 -> +0x188
 *   branch +0x184 -> +0x1a4
 *   branch +0x1a0 -> +0x240
 *   branch +0x1c8 -> +0x1e8
 *   branch +0x23c -> +0x458
 *   branch +0x270 -> +0x458
 *   branch +0x2b4 -> +0x2dc
 *   branch +0x2d8 -> +0x3ac
 *   branch +0x2f8 -> +0x458
 *   branch +0x310 -> +0x380
 *   branch +0x330 -> +0x35c
 *   branch +0x344 -> +0x35c
 *   branch +0x360 -> +0x374
 *   back edge +0x37c -> +0x318
 *   branch +0x3b8 -> +0x458
 *   branch +0x43c -> +0x458
 *   branch +0x450 -> +0x458
 *   test +0x34 cmp r0, #5
 *   test +0x9c cmp r0, #0
 *   test +0xd8 cmp r0, #0
 *   test +0x16c cmp r0, #1
 *   test +0x180 cmp r0, #0
 *   test +0x194 cmp r0, #1
 *   test +0x198 cmpne r10, #3
 *   test +0x19c cmpne r10, #4
 *   test +0x1a8 cmp r10, #0
 *   test +0x1bc cmp r0, #1
 *   test +0x1c4 cmp r10, #0
 *   test +0x1e0 cmp r0, #10
 *   test +0x290 cmp r0, #0
 *   test +0x2b0 cmp r0, #0
 *   test +0x2f0 cmp r0, #0
 *   test +0x308 cmp r8, #0
 *   test +0x340 cmp r0, #3
 *   test +0x34c cmp r0, #0
 *   test +0x354 cmpne r0, #0
 *   test +0x35c cmp r7, #0
 *   test +0x378 cmp r6, r8
 *   test +0x400 cmp r0, r7
 *   test +0x44c cmp r1, #0
 *   0 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x02200d54; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_021db438(void);
extern void native_fn_0207b244(void);
extern void native_fn_021fcb64(void);
extern void native_fn_0207afec(void);
extern void native_fn_021fe74c(void);
extern void native_fn_021fd0bc(void);
extern void native_fn_022028c8(void);
extern void native_fn_022027c0(void);
extern u8 native_data_0222edc8[];
extern void native_fn_022027f0(void);
extern void native_fn_021fd10c(void);
extern void native_fn_022023c4(void);
extern void native_fn_02201350(void);
extern void native_fn_021dba14(void);
extern void native_fn_021fe2b8(void);
extern void native_fn_02213b4c(void);
extern void native_fn_02065d88(void);
extern void native_fn_02049748(void);
extern void native_fn_021db530(void);
extern void native_fn_022007f0(void);
extern void native_fn_021ff050(void);
extern void native_fn_021db8d0(void);
extern void native_fn_0220473c(void);
extern void native_fn_0220451c(void);
extern void native_fn_021fe3dc(void);
extern u8 native_data_0222edcc[];
extern void native_fn_022022fc(void);


asm u32 native_ov001_02200d54 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    ldr r1, =0x02239c10
    mov r7, r0
    ldrsb r0, [r1, #12]
    bl native_fn_02202360
    mov r4, r0
    mov r0, #0
    bl native_fn_02202360
    ldr r1, =0x02239c10
    mov r11, r0
    ldrsb r0, [r1, #12]
    mov r5, #1
    mov r8, #0
    cmp r0, #5
    addls pc, pc, r0, lsl #2
    b ov001_02200d54_L458
    b ov001_02200d54_L458
    b ov001_02200d54_L58
    b ov001_02200d54_L3bc
    b ov001_02200d54_L458
    b ov001_02200d54_L274
    b ov001_02200d54_L440
ov001_02200d54_L58:
    ldrsb r1, [r4, #8]
    mov r0, r8
    bl native_fn_021db438
    mov r7, r0
    ldr r1, [r4]
    ldr r2, [r7, #0x1e8]
    add r1, r7, r1
    add r0, r7, #256
    ldrb r6, [r1, #0x35e]
    ldrsh r1, [r0, #242]
    add r2, r2, #70
    mov r0, r6
    bl native_fn_0207b244
    mov r2, r0
    mov r0, r7
    mov r1, r6
    bl native_fn_021fcb64
    cmp r0, #0
    moveq r5, r8
    beq ov001_02200d54_L458
    mov r0, r6
    bl native_fn_0207afec
    mov r9, r0
    ldrh r1, [r9, #8]
    ldr r0, =0x02239c10
    mov r1, r1, lsl #24
    mov r1, r1, lsr #28
    ldrsb r0, [r0, #12]
    and r10, r1, #255
    bl native_fn_021fe74c
    mov r0, r6
    bl native_fn_021fd0bc
    cmp r0, #0
    beq ov001_02200d54_L160
    ldrsb r0, [r4, #8]
    bl native_fn_022028c8
    ldrh r0, [r9, #8]
    ldrsb r1, [r4, #8]
    mov r0, r0, lsl #16
    movs r0, r0, lsr #28
    mov r0, r8
    bne ov001_02200d54_L118
    mov r3, r0
    mov r2, r1
    bl native_fn_022027c0
    ldrsb r2, [r4, #8]
    ldr r1, =native_data_0222edc8
    b ov001_02200d54_L12c
ov001_02200d54_L118:
    mov r3, r0
    mov r2, r5
    bl native_fn_022027f0
    ldrsb r2, [r4, #8]
    ldr r1, =native_data_0222edc8
ov001_02200d54_L12c:
    strb r0, [r1, r2]
    ldrsb r0, [r4, #8]
    mov r1, r6
    mov r2, #0
    mov r3, r0
    bl native_fn_021fd10c
    mov r0, #64
    bl native_fn_022023c4
    bl native_fn_02201350
    ldrsb r1, [r4, #18]
    mov r5, r0
    strb r1, [r4, #0x8]
    b ov001_02200d54_L458
ov001_02200d54_L160:
    ldrh r0, [r9, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    bne ov001_02200d54_L188
    mov r0, r7
    mov r1, r6
    bl native_fn_021dba14
    cmp r0, #0
    bne ov001_02200d54_L1a4
ov001_02200d54_L188:
    ldrh r0, [r9, #8]
    mov r0, r0, lsl #16
    mov r0, r0, lsr #28
    cmp r0, #1
    cmpne r10, #3
    cmpne r10, #4
    bne ov001_02200d54_L240
ov001_02200d54_L1a4:
    add r0, r10, #253
    cmp r10, #0
    moveq r7, #0
    and r0, r0, #255
    movne r7, #1
    mov r5, #1
    cmp r0, #1
    movls r8, r5
    cmp r10, #0
    bne ov001_02200d54_L1e8
    mov r0, r6
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #10
    moveq r5, #0
ov001_02200d54_L1e8:
    ldrsb r0, [r4, #8]
    bl native_fn_022028c8
    ldrsb r1, [r4, #8]
    mov r0, r7
    mov r2, r5
    mov r3, r8
    bl native_fn_022027f0
    ldrsb r3, [r4, #8]
    ldr r2, =native_data_0222edc8
    mov r1, r6
    strb r0, [r2, r3]
    ldrsb r0, [r4, #8]
    mov r2, r7
    mov r3, #4
    bl native_fn_021fd10c
    mov r0, #64
    bl native_fn_022023c4
    bl native_fn_02201350
    ldrsb r1, [r4, #18]
    mov r5, r0
    strb r1, [r4, #0x8]
    b ov001_02200d54_L458
ov001_02200d54_L240:
    mov r0, #1
    mov r1, r0
    bl native_fn_021fe2b8
    ldr r0, =0x02239c10
    mov r1, #6
    strb r1, [r0, #0xa]
    ldrh r0, [r9, #8]
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    moveq r0, #0
    movne r0, #1
    strb r0, [r4, #0x14]
    b ov001_02200d54_L458
ov001_02200d54_L274:
    ldr r0, [r4]
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_02213b4c
    mov r9, r0
    bl native_fn_02065d88
    ldrb r0, [r0, #0x2f]
    cmp r0, #0
    moveq r0, r8
    movne r0, r5
    mov r1, r0, lsl #24
    mov r0, r9
    mov r10, r1, asr #24
    bl native_fn_02065d88
    ldrb r0, [r0, #0x30]
    cmp r0, #0
    bne ov001_02200d54_L2dc
    mov r0, #133
    bl native_fn_022023c4
    mov r0, r4
    bl native_fn_02049748
    ldr r0, =0x02239c10
    strb r10, [r4, #0x14]
    mov r1, #6
    strb r1, [r0, #0xa]
    b ov001_02200d54_L3ac
ov001_02200d54_L2dc:
    mov r0, r10
    bl native_fn_021db530
    mov r8, r0
    mov r0, r9
    bl native_fn_022007f0
    cmp r0, #0
    moveq r5, #0
    beq ov001_02200d54_L458
    mov r0, r9
    mov r1, #4
    bl native_fn_021ff050
    cmp r8, #0
    mov r6, #0
    ble ov001_02200d54_L380
    mov r4, #1
ov001_02200d54_L318:
    mov r0, r10
    mov r1, r6
    bl native_fn_021db438
    mov r5, r0
    bl native_fn_021db8d0
    movs r7, r0
    bne ov001_02200d54_L35c
    mov r0, r9
    bl native_fn_02065d88
    ldrb r0, [r0, #0x28]
    cmp r0, #3
    bne ov001_02200d54_L35c
    ldrb r0, [r5, #0x31c]
    cmp r0, #0
    ldrneb r0, [r5, #0x1ff]
    cmpne r0, #0
    movne r7, r4
ov001_02200d54_L35c:
    cmp r7, #0
    beq ov001_02200d54_L374
    mov r1, r6, lsl #24
    mov r0, r10
    mov r1, r1, asr #24
    bl native_fn_0220473c
ov001_02200d54_L374:
    add r6, r6, #1
    cmp r6, r8
    blt ov001_02200d54_L318
ov001_02200d54_L380:
    bl native_fn_02201350
    mov r1, #0
    mov r5, r0
    add r0, r11, #24
    str r1, [r11]
    bl native_fn_0220451c
    mov r0, #1
    mov r1, #0
    bl native_fn_021fe3dc
    mov r0, #141
    bl native_fn_022023c4
ov001_02200d54_L3ac:
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_021fe74c
    b ov001_02200d54_L458
ov001_02200d54_L3bc:
    ldrsb r1, [r4, #8]
    mov r0, r8
    bl native_fn_021db438
    ldrsb r2, [r4, #8]
    ldr r1, =native_data_0222edcc
    mov r6, r0
    strb r7, [r1, r2]
    ldrsb r0, [r4, #8]
    ldrb r7, [r1, r0]
    strb r0, [r4, #0x12]
    ldrsb r0, [r4, #8]
    bl native_fn_022028c8
    ldr r0, =0x02239c10
    ldrsb r0, [r0, #12]
    bl native_fn_021fe74c
    strb r7, [r6, #0x1fe]
    ldrb r0, [r6, #0x35c]
    cmp r0, r7
    ldrb r0, [r6, #0x35d]
    orrne r0, r0, #4
    biceq r0, r0, #4
    strb r0, [r6, #0x35d]
    mov r0, #1
    mov r1, r0
    bl native_fn_021fe2b8
    ldr r0, =0x02239c10
    mov r1, #6
    strb r1, [r0, #0xa]
    mov r1, #1
    mov r0, #64
    strb r1, [r4, #0x13]
    bl native_fn_022023c4
    b ov001_02200d54_L458
ov001_02200d54_L440:
    bl native_fn_02201350
    ldr r1, [r4]
    mov r5, r0
    cmp r1, #0
    bne ov001_02200d54_L458
    bl native_fn_022022fc
ov001_02200d54_L458:
    mov r0, r5
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
