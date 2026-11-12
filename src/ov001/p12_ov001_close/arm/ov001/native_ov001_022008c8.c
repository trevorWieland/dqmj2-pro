/* ov001 row 0x022008c8: 1164 bytes.
 *
 * What it does: 289 instructions; 57 call(s) to 0x02202360, 0x02202360, 0x021db438, +54 more; loops (back edge at +0x64); returns through pop {r3, r4, r5, r6, r7, r8, r9, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 57 calls (289 instructions, 57 calls, 33 branches, 34 back edges, 2 literal slots).
 *
 *   pool +0x484 -> constant 0x02239c10 (image word 0x02239c10)
 *   pool +0x488 -> native_data_0222edc8 (image word 0x0222edc8)
 *   branch +0x38 -> +0x444
 *   branch +0x3c -> +0x444
 *   branch +0x40 -> +0x50
 *   branch +0x44 -> +0x2e4
 *   branch +0x48 -> +0x330
 *   branch +0x4c -> +0x230
 *   branch +0x5c -> +0xc4
 *   branch +0x74 -> +0x88
 *   branch +0x84 -> +0x90
 *   branch +0x8c -> +0x444
 *   branch +0xc0 -> +0x444
 *   branch +0xd8 -> +0xec
 *   branch +0xe8 -> +0xf8
 *   branch +0x124 -> +0x17c
 *   branch +0x138 -> +0x444
 *   branch +0x150 -> +0x190
 *   branch +0x170 -> +0x190
 *   branch +0x178 -> +0x444
 *   branch +0x18c -> +0x444
 *   branch +0x1b0 -> +0x1e4
 *   branch +0x1e0 -> +0x210
 *   branch +0x22c -> +0x444
 *   branch +0x26c -> +0x444
 *   branch +0x2e0 -> +0x444
 *   branch +0x300 -> +0x444
 *   branch +0x32c -> +0x444
 *   branch +0x354 -> +0x444
 *   branch +0x374 -> +0x398
 *   branch +0x380 -> +0x398
 *   branch +0x394 -> +0x444
 *   branch +0x3bc -> +0x3d4
 *   branch +0x3d0 -> +0x444
 *   branch +0x3dc -> +0x3f8
 *   back edge +0x3f4 -> +0x3e0
 *   branch +0x448 -> +0x478
 *   branch +0x460 -> +0x478
 *   test +0x30 cmp r0, #4
 *   test +0x54 cmp r0, #1
 *   test +0x70 cmp r0, #0
 *   test +0x80 cmp r0, #0
 *   test +0xd4 cmp r1, #0
 *   test +0x11c cmp r0, #3
 *   test +0x128 cmp r0, #0
 *   test +0x130 cmpne r0, #0
 *   test +0x160 cmp r0, #2
 *   test +0x16c cmpeq r1, r0
 *   test +0x17c cmp r0, #0
 *   test +0x184 cmpne r0, #0
 *   test +0x1ac cmp r0, #0
 *   test +0x248 cmp r0, #0
 *   test +0x264 cmp r0, #0
 *   test +0x2f8 cmp r0, #0
 *   test +0x350 cmp r0, #0
 *   test +0x370 cmp r0, #7
 *   test +0x378 cmp r8, #3
 *   test +0x37c cmpne r8, #7
 *   test +0x39c cmp r8, #3
 *   test +0x3a4 cmpne r8, #7
 *   test +0x3b8 cmp r0, #0
 *   test +0x3d4 cmp r5, #0
 *   test +0x3f0 cmp r8, r5
 *   test +0x444 cmp r6, #1
 *   test +0x45c cmp r0, #3
 *   0 block transfer(s), 12 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022008c8; the literal pool and
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
extern void native_fn_021db8d0(void);
extern void native_fn_021dc1c0(void);
extern void native_fn_021fe2b8(void);
extern void native_fn_02202478(void);
extern void native_fn_0207afec(void);
extern void native_fn_022028c8(void);
extern void native_fn_021fddb4(void);
extern void native_fn_022027c0(void);
extern u8 native_data_0222edc8[];
extern void native_fn_021fd10c(void);
extern void native_fn_022023c4(void);
extern void native_fn_02213b4c(void);
extern void native_fn_02200824(void);
extern void native_fn_02202218(void);
extern void native_fn_0220473c(void);
extern void native_fn_021ff050(void);
extern void native_fn_02049748(void);
extern void native_fn_0220451c(void);
extern void native_fn_021fe3dc(void);
extern void native_fn_021db530(void);
extern void native_fn_020443ec(void);
extern void native_fn_02044dc4(void);
extern void native_fn_020450b4(void);
extern void native_fn_021fdd74(void);
extern void native_fn_02202824(void);
extern void native_fn_021e13a8(void);
extern void native_fn_021f9510(void);
extern void native_fn_021ff238(void);
extern void native_fn_022042c4(void);
extern void native_fn_02204590(void);
extern void native_fn_021feeb4(void);


asm u32 native_ov001_022008c8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    ldr r1, =0x02239c10
    mov r7, r0
    ldrsb r0, [r1, #12]
    bl native_fn_02202360
    mov r4, r0
    mov r0, #0
    bl native_fn_02202360
    ldr r1, =0x02239c10
    mov r5, r0
    ldrsb r0, [r1, #12]
    mov r6, #1
    cmp r0, #4
    addls pc, pc, r0, lsl #2
    b ov001_022008c8_L444
    b ov001_022008c8_L444
    b ov001_022008c8_L50
    b ov001_022008c8_L2e4
    b ov001_022008c8_L330
    b ov001_022008c8_L230
ov001_022008c8_L50:
    ldrb r0, [r4, #0x13]
    cmp r0, #1
    mov r0, #0
    bne ov001_022008c8_Lc4
    ldrsb r1, [r4, #8]
    bl native_fn_021db438
    mov r5, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022008c8_L88
    mov r0, r5
    bl native_fn_021dc1c0
    cmp r0, #0
    bne ov001_022008c8_L90
ov001_022008c8_L88:
    mov r6, #0
    b ov001_022008c8_L444
ov001_022008c8_L90:
    mov r0, #0
    mov r1, r6
    bl native_fn_021fe2b8
    ldr r0, =0x02239c10
    mov r1, #4
    strb r1, [r0, #0xa]
    ldrb r0, [r4, #0x14]
    ldrsb r1, [r4, #8]
    mov r2, #109
    bl native_fn_02202478
    ldrsb r0, [r4, #8]
    strb r0, [r4, #0x12]
    b ov001_022008c8_L444
ov001_022008c8_Lc4:
    ldrsb r1, [r4, #18]
    bl native_fn_021db438
    ldrb r1, [r4, #0x14]
    mov r5, r0
    cmp r1, #0
    bne ov001_022008c8_Lec
    ldrsb r1, [r4, #8]
    mov r0, #0
    bl native_fn_021db438
    b ov001_022008c8_Lf8
ov001_022008c8_Lec:
    ldrsb r1, [r4, #10]
    mov r0, r6
    bl native_fn_021db438
ov001_022008c8_Lf8:
    mov r7, r0
    ldr r0, [r4]
    add r0, r5, r0
    ldrb r5, [r0, #0x35e]
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #20
    mov r0, r0, lsr #28
    cmp r0, #3
    ldrb r0, [r7, #0x31c]
    beq ov001_022008c8_L17c
    cmp r0, #0
    ldrneb r0, [r7, #0x1ff]
    cmpne r0, #0
    movne r6, #0
    bne ov001_022008c8_L444
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #24
    movs r0, r0, lsr #28
    bne ov001_022008c8_L190
    mov r0, r5
    bl native_fn_0207afec
    ldrb r0, [r0, #0x1e]
    cmp r0, #2
    ldreqsb r1, [r4, #8]
    ldreqsb r0, [r4, #18]
    cmpeq r1, r0
    bne ov001_022008c8_L190
    mov r6, #0
    b ov001_022008c8_L444
ov001_022008c8_L17c:
    cmp r0, #0
    ldrneb r0, [r7, #0x1ff]
    cmpne r0, #0
    moveq r6, #0
    beq ov001_022008c8_L444
ov001_022008c8_L190:
    ldrsb r0, [r4, #18]
    bl native_fn_022028c8
    ldrsb r0, [r4, #18]
    ldrb r1, [r4, #0x9]
    bl native_fn_021fddb4
    ldrb r0, [r4, #0x14]
    mov r3, #0
    cmp r0, #0
    bne ov001_022008c8_L1e4
    ldrsb r1, [r4, #18]
    ldrsb r2, [r4, #8]
    bl native_fn_022027c0
    ldrsb r3, [r4, #18]
    ldr r2, =native_data_0222edc8
    mov r1, r5
    strb r0, [r2, r3]
    ldrsb r0, [r4, #18]
    ldrb r2, [r4, #0x14]
    ldrsb r3, [r4, #8]
    bl native_fn_021fd10c
    b ov001_022008c8_L210
ov001_022008c8_L1e4:
    ldrsb r1, [r4, #8]
    ldrsb r2, [r4, #10]
    bl native_fn_022027c0
    ldrsb r3, [r4, #18]
    ldr r2, =native_data_0222edc8
    mov r1, r5
    strb r0, [r2, r3]
    ldrsb r0, [r4, #18]
    ldrb r2, [r4, #0x14]
    ldrsb r3, [r4, #10]
    bl native_fn_021fd10c
ov001_022008c8_L210:
    mov r0, #64
    bl native_fn_022023c4
    mov r1, #1
    ldr r0, =0x02239c10
    strb r1, [r4, #0x13]
    mov r1, #6
    strb r1, [r0, #0xa]
    b ov001_022008c8_L444
ov001_022008c8_L230:
    ldr r0, [r4]
    mov r0, r0, lsl #16
    mov r0, r0, asr #16
    bl native_fn_02213b4c
    mov r8, r0
    ldrb r0, [r4, #0x14]
    cmp r0, #0
    ldreqsb r1, [r4, #8]
    ldrnesb r1, [r4, #10]
    bl native_fn_021db438
    mov r1, r0
    mov r0, r8
    bl native_fn_02200824
    cmp r0, #0
    moveq r6, #0
    beq ov001_022008c8_L444
    mov r0, #0
    bl native_fn_02202218
    mov r1, r7, lsl #24
    ldrsb r0, [r4, #20]
    mov r1, r1, asr #24
    bl native_fn_0220473c
    mov r0, r8
    and r1, r7, #255
    bl native_fn_021ff050
    mov r0, r4
    bl native_fn_02049748
    mov r0, #133
    bl native_fn_022023c4
    mov r0, #2
    mov r1, #1
    bl native_fn_021fe2b8
    ldr r0, =0x02239c10
    mov r2, #3
    strb r2, [r0, #0xa]
    mov r1, #0
    add r0, r5, #24
    str r1, [r5]
    bl native_fn_0220451c
    mov r0, #1
    mov r1, #0
    bl native_fn_021fe3dc
    mov r0, #8
    bl native_fn_022023c4
    b ov001_022008c8_L444
ov001_022008c8_L2e4:
    ldrsb r1, [r4, #8]
    mov r0, #0
    bl native_fn_021db438
    add r0, r0, #512
    ldrsb r0, [r0, #88]
    cmp r0, #0
    movne r6, #0
    bne ov001_022008c8_L444
    mov r0, #0
    mov r1, r6
    bl native_fn_021fe2b8
    ldr r0, =0x02239c10
    mov r1, #4
    strb r1, [r0, #0xa]
    ldrsb r1, [r4, #8]
    mov r0, #0
    mov r2, #109
    bl native_fn_02202478
    b ov001_022008c8_L444
ov001_022008c8_L330:
    mov r0, #0
    bl native_fn_021db530
    mov r5, r0
    ldrsb r1, [r4, #10]
    mov r0, r6
    bl native_fn_021db438
    mov r9, r0
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_022008c8_L444
    bl native_fn_020443ec
    ldr r1, [r9, #0x1e8]
    mov r8, r0
    ldrsh r0, [r1, #42]
    ldrb r1, [r1, #0x2c]
    bl native_fn_02044dc4
    cmp r0, #7
    blo ov001_022008c8_L398
    cmp r8, #3
    cmpne r8, #7
    bne ov001_022008c8_L398
    ldr r0, =0x02239c10
    mov r1, #8
    strb r1, [r0, #0xa]
    mov r6, #0
    b ov001_022008c8_L444
ov001_022008c8_L398:
    ldr r1, [r9, #0x1e8]
    cmp r8, #3
    ldrsh r0, [r1, #42]
    cmpne r8, #7
    moveq r2, #1
    ldrb r1, [r1, #0x2c]
    movne r2, #0
    bl native_fn_020450b4
    cmp r0, #0
    beq ov001_022008c8_L3d4
    ldr r0, =0x02239c10
    mov r1, #8
    strb r1, [r0, #0xa]
    mov r6, #0
    b ov001_022008c8_L444
ov001_022008c8_L3d4:
    cmp r5, #0
    mov r8, #0
    ble ov001_022008c8_L3f8
ov001_022008c8_L3e0:
    mov r0, r8, lsl #24
    mov r0, r0, asr #24
    bl native_fn_022028c8
    add r8, r8, #1
    cmp r8, r5
    blt ov001_022008c8_L3e0
ov001_022008c8_L3f8:
    bl native_fn_021fdd74
    mov r0, r7, lsl #24
    mov r0, r0, asr #24
    bl native_fn_02202824
    mov r0, r4
    bl native_fn_02049748
    mov r0, #143
    bl native_fn_022023c4
    mov r0, #0
    bl native_fn_02202218
    mov r0, #3
    bl native_fn_021e13a8
    ldr r1, =0x02239c10
    mov r2, #1
    mov r0, r7
    strb r2, [r1]
    bl native_fn_021f9510
    mov r0, #1
    bl native_fn_021ff238
ov001_022008c8_L444:
    cmp r6, #1
    bne ov001_022008c8_L478
    add r0, r4, #168
    bl native_fn_022042c4
    ldr r0, =0x02239c10
    ldrb r0, [r0, #0xa]
    cmp r0, #3
    bne ov001_022008c8_L478
    mov r0, #0
    bl native_fn_02202360
    add r0, r0, #24
    mov r1, #123
    bl native_fn_02204590
ov001_022008c8_L478:
    bl native_fn_021feeb4
    mov r0, r6
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
