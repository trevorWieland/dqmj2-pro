/* ov006 row 0x02206b24: 1216 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x4a4 -> native_data_0221c27c (image word 0x0221c27c)
 *   pool +0x4a8 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x4ac -> constant 0x66666667 (image word 0x66666667)
 *   pool +0x4b0 -> constant 0x2aaaaaab (image word 0x2aaaaaab)
 *   pool +0x4b4 -> native_data_0221c290 (image word 0x0221c290)
 *   pool +0x4b8 -> native_data_0220bc10 (image word 0x0220bc10)
 *   pool +0x4bc -> native_data_0220bc18 (image word 0x0220bc18)
 *   branch +0x08 -> +0x484
 *   branch +0x9c -> +0xec
 *   branch +0xa8 -> +0x484
 *   branch +0xe8 -> +0x484
 *   branch +0xf8 -> +0x1a0
 *   branch +0x100 -> +0x484
 *   branch +0x114 -> +0x190
 *   branch +0x124 -> +0x180
 *   branch +0x134 -> +0x180
 *   branch +0x17c -> +0x484
 *   branch +0x18c -> +0x484
 *   branch +0x19c -> +0x484
 *   branch +0x1a4 -> +0x1dc
 *   branch +0x1b8 -> +0x1cc
 *   branch +0x1e0 -> +0x268
 *   branch +0x20c -> +0x484
 *   branch +0x264 -> +0x484
 *   branch +0x270 -> +0x334
 *   branch +0x27c -> +0x2f8
 *   branch +0x2b0 -> +0x2dc
 *   branch +0x2d8 -> +0x484
 *   branch +0x2e4 -> +0x484
 *   branch +0x2f4 -> +0x484
 *   branch +0x2fc -> +0x484
 *   branch +0x330 -> +0x484
 *   branch +0x338 -> +0x400
 *   branch +0x344 -> +0x3c4
 *   branch +0x37c -> +0x3a8
 *   branch +0x3a4 -> +0x484
 *   branch +0x3b0 -> +0x484
 *   branch +0x3c0 -> +0x484
 *   branch +0x3c8 -> +0x484
 *   branch +0x3fc -> +0x484
 *   branch +0x404 -> +0x444
 *   branch +0x440 -> +0x484
 *   branch +0x448 -> +0x484
 *   branch +0x490 -> +0x498
 *   test +0x98 cmp r0, #0
 *   test +0xa4 cmp r8, r4
 *   test +0xf4 tst r1, #1
 *   test +0xfc cmp r7, #4
 *   test +0x110 cmp r4, #0
 *   test +0x120 cmp r0, #0
 *   test +0x130 cmp r0, #0
 *   test +0x1a0 tst r1, #2
 *   test +0x1b0 cmp r0, #100
 *   test +0x1dc tst r1, #4
 *   test +0x208 cmp r0, #0
 *   test +0x26c tst r0, #64
 *   test +0x274 cmp r6, #0
 *   test +0x278 cmpne r7, #4
 *   test +0x280 cmp r6, #0
 *   test +0x28c cmp r4, #0
 *   test +0x2ac cmp r9, r4
 *   test +0x2dc cmp r8, r6
 *   test +0x2e0 cmpne r7, #4
 *   test +0x2f8 cmp r6, #0
 *   test +0x334 tst r0, #128
 *   test +0x33c cmp r6, #2
 *   test +0x340 cmpne r7, #4
 *   test +0x348 cmp r6, #2
 *   test +0x354 cmp r4, r9
 *   test +0x378 cmp r9, r4
 *   test +0x3a8 cmp r8, r6
 *   test +0x3ac cmpne r7, #4
 *   test +0x3c4 cmp r6, #3
 *   test +0x400 tst r0, #32
 *   test +0x408 cmp r7, #0
 *   test +0x444 tst r0, #16
 *   test +0x44c cmp r7, #4
 *   test +0x48c cmp r0, #1
 *   11 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov006.bin at 0x02206b24; the literal pool and
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

extern u8 native_data13_0221c27c[];
extern void native_fn_020c1a04(void);
extern void native_fn_02206374(void);
extern void native_fn_022061e8(void);
extern void native_fn_02206328(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_0202a634(void);
extern u8 native_data_0221c290[];
extern void native_fn_02063fa0(void);
extern void native_fn_02063fac(void);
extern void native_fn_02062a10(void);
extern void native_fn_021e7a60(void);
extern u8 native_data_0220bc10[];
extern void native_fn_021e7e90(void);
extern void native_fn_021e7d98(void);
extern void native_fn_02049e0c(void);
extern void native_fn_0207ca3c(void);
extern u8 native_data_0220bc18[];
extern void native_fn_021e7e78(void);
extern void native_fn_0220692c(void);
extern void native_fn_021e648c(void);


asm u32 native_ov006_02206b24 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, lr}
    movs r5, r0
    beq ov006_02206b24_L484
    ldr r1, =native_data13_0221c27c
    ldr r0, =0x88888889
    ldr r3, [r1]
    ldr r6, [r1, #0x10]
    smull r1, r2, r0, r3
    mov r7, r3, lsr #31
    add r2, r3, r2
    add r2, r7, r2, asr #3
    mov r4, #15
    smull r1, r2, r4, r2
    sub r2, r3, r1
    add r12, r6, #11
    smull r6, r4, r0, r3
    add r4, r3, r4
    add r4, r7, r4, asr #3
    ldr r1, =0x66666667
    ldr r8, =0x2aaaaaab
    smull r0, r7, r1, r2
    smull r0, r6, r1, r2
    mov r3, r2, lsr #31
    smull r0, r1, r8, r12
    mov r0, r12, lsr #31
    add r1, r0, r1, asr #1
    add r7, r3, r7, asr #1
    add r6, r3, r6, asr #1
    mov r3, #5
    sub r9, r1, #1
    smull r0, r1, r3, r7
    sub r7, r2, r0
    mov r0, #208
    mov r1, #40
    add r2, sp, #0
    add r3, r9, #1
    str r4, [sp]
    bl native_fn_020c1a04
    cmp r0, #0
    beq ov006_02206b24_Lec
    ldr r8, [sp]
    cmp r8, r4
    beq ov006_02206b24_L484
    add r0, r6, r6, lsl #2
    add r2, r7, r0
    rsb r1, r8, r8, lsl #4
    ldr r0, =native_data13_0221c27c
    add r1, r2, r1
    str r1, [r0]
    bl native_fn_02206374
    mov r0, r8
    bl native_fn_022061e8
    mov r0, r7
    mov r1, r6
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #86
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_Lec:
    bl native_fn_0202a634
    ldrh r1, [r0, #2]
    tst r1, #1
    beq ov006_02206b24_L1a0
    cmp r7, #4
    bge ov006_02206b24_L484
    ldr r0, =native_data_0221c290
    add r1, r7, r6, lsl #2
    ldr r4, [r0, r1, lsl #2]
    cmp r4, #0
    beq ov006_02206b24_L190
    mov r0, r4
    bl native_fn_02063fa0
    cmp r0, #0
    bne ov006_02206b24_L180
    mov r0, r4
    bl native_fn_02063fac
    cmp r0, #0
    bne ov006_02206b24_L180
    mov r0, r4
    bl native_fn_02062a10
    mov r1, r0
    mov r0, #0
    bl native_fn_021e7a60
    ldr r0, =native_data_0220bc10
    bl native_fn_021e7e90
    mov r0, #1
    bl native_fn_021e7d98
    mov r0, #0
    bl native_fn_02049e0c
    mov r2, #3
    ldr r1, =native_data13_0221c27c
    sub r0, r2, #4
    str r2, [r1, #0x8]
    mov r1, #82
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L180:
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L190:
    mvn r0, #0
    mov r1, #84
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L1a0:
    tst r1, #2
    beq ov006_02206b24_L1dc
    ldr r0, =native_data13_0221c27c
    ldr r0, [r0, #0x10]
    cmp r0, #100
    mvn r0, #0
    bge ov006_02206b24_L1cc
    mov r1, #82
    bl native_fn_0205e7a8
    mvn r0, #1
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov006_02206b24_L1cc:
    mov r1, #83
    bl native_fn_0205e7a8
    mvn r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
ov006_02206b24_L1dc:
    tst r1, #4
    beq ov006_02206b24_L268
    ldr r0, =native_data13_0221c27c
    ldr r0, [r0, #0x4]
    add r0, r0, #1
    mov r1, r0, lsr #31
    rsb r0, r1, r0, lsl #30
    adds r8, r1, r0, ror #30
    addeq r8, r8, #1
    mov r0, r8
    bl native_fn_0207ca3c
    cmp r0, #0
    beq ov006_02206b24_L484
    mvn r0, #0
    mov r1, #87
    bl native_fn_0205e7a8
    bl native_fn_02206374
    mov r0, r4
    bl native_fn_022061e8
    mov r0, r7
    mov r1, r6
    bl native_fn_02206328
    ldr r1, =native_data_0220bc18
    sub r0, r8, #1
    add r0, r1, r0, lsl #2
    bl native_fn_021e7e90
    mov r0, #1
    bl native_fn_021e7d98
    mov r0, #1
    bl native_fn_021e7e78
    ldr r0, =native_data13_0221c27c
    mov r1, #2
    str r1, [r0, #0x8]
    str r8, [r0, #0x4]
    b ov006_02206b24_L484
ov006_02206b24_L268:
    ldrh r0, [r0, #6]
    tst r0, #64
    beq ov006_02206b24_L334
    cmp r6, #0
    cmpne r7, #4
    bne ov006_02206b24_L2f8
    cmp r6, #0
    moveq r8, #2
    movne r8, r6
    cmp r4, #0
    subne r9, r4, #1
    add r0, r8, r8, lsl #2
    add r2, r7, r0
    rsb r1, r9, r9, lsl #4
    ldr r0, =native_data13_0221c27c
    add r1, r2, r1
    str r1, [r0]
    cmp r9, r4
    beq ov006_02206b24_L2dc
    bl native_fn_02206374
    mov r0, r9
    bl native_fn_022061e8
    mov r0, r7
    mov r1, r8
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #86
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L2dc:
    cmp r8, r6
    cmpne r7, #4
    beq ov006_02206b24_L484
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L2f8:
    cmp r6, #0
    ble ov006_02206b24_L484
    sub r1, r6, #1
    add r0, r1, r1, lsl #2
    add r3, r7, r0
    rsb r0, r4, r4, lsl #4
    ldr r2, =native_data13_0221c27c
    add r3, r3, r0
    mov r0, r7
    str r3, [r2]
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L334:
    tst r0, #128
    beq ov006_02206b24_L400
    cmp r6, #2
    cmpne r7, #4
    bne ov006_02206b24_L3c4
    cmp r6, #2
    moveq r8, #0
    movne r8, r6
    cmp r4, r9
    moveq r9, #0
    addne r9, r4, #1
    add r0, r8, r8, lsl #2
    add r2, r7, r0
    rsb r1, r9, r9, lsl #4
    ldr r0, =native_data13_0221c27c
    add r1, r2, r1
    str r1, [r0]
    cmp r9, r4
    beq ov006_02206b24_L3a8
    bl native_fn_02206374
    mov r0, r9
    bl native_fn_022061e8
    mov r0, r7
    mov r1, r8
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #86
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L3a8:
    cmp r8, r6
    cmpne r7, #4
    beq ov006_02206b24_L484
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L3c4:
    cmp r6, #3
    bge ov006_02206b24_L484
    add r1, r6, #1
    add r0, r1, r1, lsl #2
    add r3, r7, r0
    rsb r0, r4, r4, lsl #4
    ldr r2, =native_data13_0221c27c
    add r3, r3, r0
    mov r0, r7
    str r3, [r2]
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L400:
    tst r0, #32
    beq ov006_02206b24_L444
    cmp r7, #0
    subgt r0, r7, #1
    movle r0, #4
    add r1, r6, r6, lsl #2
    add r3, r0, r1
    rsb r1, r4, r4, lsl #4
    add r3, r3, r1
    ldr r2, =native_data13_0221c27c
    mov r1, r6
    str r3, [r2]
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
    b ov006_02206b24_L484
ov006_02206b24_L444:
    tst r0, #16
    beq ov006_02206b24_L484
    cmp r7, #4
    addlt r0, r7, #1
    movge r0, #0
    add r1, r6, r6, lsl #2
    add r3, r0, r1
    rsb r1, r4, r4, lsl #4
    add r3, r3, r1
    ldr r2, =native_data13_0221c27c
    mov r1, r6
    str r3, [r2]
    bl native_fn_02206328
    mvn r0, #0
    mov r1, #85
    bl native_fn_0205e7a8
ov006_02206b24_L484:
    ldr r0, =native_data13_0221c27c
    ldr r0, [r0, #0x8]
    cmp r0, #1
    bne ov006_02206b24_L498
    bl native_fn_0220692c
ov006_02206b24_L498:
    mov r0, r5
    bl native_fn_021e648c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, pc}
}
