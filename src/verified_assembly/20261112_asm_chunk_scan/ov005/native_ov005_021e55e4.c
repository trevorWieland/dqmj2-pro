/* ov005 row 0x021e55e4: 1192 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x450 -> constant 0x021ed438 (image word 0x021ed438)
 *   pool +0x454 -> native_fn_021e54e4 (image word 0x021e54e4)
 *   pool +0x458 -> constant 0x021ed698 (image word 0x021ed698)
 *   pool +0x45c -> constant 0x021ed4a4 (image word 0x021ed4a4)
 *   pool +0x460 -> native_data_021e786c (image word 0x021e786c)
 *   pool +0x464 -> constant 0x80001224 (image word 0x80001224)
 *   pool +0x468 -> native_fn_021e54e8 (image word 0x021e54e8)
 *   pool +0x46c -> constant 0x021edd5c (image word 0x021edd5c)
 *   pool +0x470 -> constant 0x021ede04 (image word 0x021ede04)
 *   pool +0x474 -> constant 0x021ede0c (image word 0x021ede0c)
 *   pool +0x478 -> constant 0x021ede20 (image word 0x021ede20)
 *   pool +0x47c -> constant 0x000003e7 (image word 0x000003e7)
 *   pool +0x480 -> constant 0x021edf5c (image word 0x021edf5c)
 *   pool +0x484 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x488 -> constant 0x001fffff (image word 0x001fffff)
 *   pool +0x48c -> constant 0x021edd74 (image word 0x021edd74)
 *   pool +0x490 -> constant 0x021eddec (image word 0x021eddec)
 *   pool +0x494 -> constant 0x021edaf4 (image word 0x021edaf4)
 *   pool +0x498 -> native_data_021e7874 (image word 0x021e7874)
 *   pool +0x49c -> constant 0x80001517 (image word 0x80001517)
 *   pool +0x4a0 -> constant 0x021ed88c (image word 0x021ed88c)
 *   pool +0x4a4 -> native_data_021e787c (image word 0x021e787c)
 *   branch +0x4c -> +0xc0
 *   branch +0xfc -> +0x178
 *   branch +0x11c -> +0x178
 *   back edge +0x174 -> +0x110
 *   branch +0x284 -> +0x3a8
 *   branch +0x2d4 -> +0x310
 *   back edge +0x308 -> +0x2e8
 *   branch +0x3c8 -> +0x3f0
 *   branch +0x3ec -> +0x410
 *   test +0x44 cmp r0, #1
 *   test +0xf4 cmp r1, #0
 *   test +0x118 cmp r0, #0
 *   test +0x170 cmp r7, r0
 *   test +0x18c cmp r2, r0
 *   test +0x274 tst r1, #1
 *   test +0x280 cmpne r1, r0
 *   test +0x2c8 cmp r1, #7
 *   test +0x300 cmp r6, #6
 *   test +0x398 cmp r0, #2
 *   test +0x3c4 cmp r0, #0
 *   29 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov005.bin at 0x021e55e4; the literal pool and
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

extern void native_fn_020633b0(void);
extern void native_fn_02008c58(void);
extern void native_fn_021e54e4(void);
extern void native_fn_021d8edc(void);
extern u8 native_data_021e786c[];
extern void native_fn3_021e54e8(void);
extern void native_fn_021d9158(void);
extern void native_fn_0203d294(void);
extern void native_fn_021d8ff0(void);
extern void native_fn_020081fc(void);
extern void native_fn_02008e0c(void);
extern void native_fn_02062aa0(void);
extern void native_fn_02062a50(void);
extern void native_fn_0207b460(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c3d8(void);
extern void native_fn_020633bc(void);
extern void native_fn_0206434c(void);
extern void native_fn_0206442c(void);
extern void native_fn_02063f6c(void);
extern void native_fn_021e1014(void);
extern u8 native_data_021e7874[];
extern u8 native_data_021e787c[];


asm u32 native_ov005_021e55e4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #76
    bl native_fn_020633b0
    mov r8, r0
    ldr r1, =0x021ed438
    mov r0, #0
    str r0, [r1, #0x34]
    ldr r1, [r1, #0x28]
    mov r2, #4
    bl native_fn_02008c58
    ldr r0, =0x021ed438
    ldr r1, =native_fn_021e54e4
    ldr r0, [r0, #0x28]
    mov r2, #2
    bl native_fn_021d8edc
    ldr r0, =0x021ed438
    ldrb r0, [r0, #0x9]
    cmp r0, #1
    mov r0, #0
    bne ov005_021e55e4_Lc0
    ldr r1, =0x021ed698
    mov r2, #500
    bl native_fn_02008c58
    ldr r1, =0x021ed4a4
    mov r0, #0
    mov r2, #500
    bl native_fn_02008c58
    ldr r0, =0x021ed4a4
    ldr r4, =native_data_021e786c
    str r0, [sp]
    mov r3, #500
    ldr r0, =0x80001224
    ldr r1, =native_fn3_021e54e8
    ldr r2, =0x021ed698
    stmib sp, {r3, r4}
    bl native_fn_021d9158
    mov r0, #2
    bl native_fn_0203d294
    add r1, r0, #5
    mov r0, #60
    mul r0, r1, r0
    add r0, r0, r0, lsr #31
    ldr r1, =0x021ed438
    mov r0, r0, asr #1
    str r0, [r1, #0x24]
    bl native_fn_021d8ff0
    add sp, sp, #76
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
ov005_021e55e4_Lc0:
    ldr r1, =0x021edd5c
    mov r2, #616
    bl native_fn_02008c58
    ldr r0, =0x021ede04
    bl native_fn_020081fc
    ldr r1, =0x021ede0c
    mov r0, r8
    mov r2, #20
    bl native_fn_02008e0c
    bl native_fn_02062aa0
    ldr r10, =0x021edd5c
    and r1, r0, #255
    strb r0, [r10, #0xae]
    cmp r1, #0
    mov r7, #0
    ble ov005_021e55e4_L178
    ldr r9, =0x021ede20
    mov r6, #132
    add r5, sp, #12
    mov r4, r7
ov005_021e55e4_L110:
    mov r0, r7
    bl native_fn_02062a50
    cmp r0, #0
    beq ov005_021e55e4_L178
    mov r1, r9
    mov r2, r6
    bl native_fn_02008e0c
    ldrsh r0, [r9, #24]
    ldrb r1, [r9, #0x1a]
    mov r3, r5
    add r2, r9, #122
    bl native_fn_0207b460
    mov r1, r5
    add r0, r9, #32
    bl native_fn_0207c2b8
    strh r0, [r9, #36]
    add r0, r9, #32
    mov r1, r5
    bl native_fn_0207c3d8
    strh r0, [r9, #38]
    strb r4, [r9, #0x33]
    add r9, r9, #132
    add r7, r7, #1
    ldrb r0, [r10, #0xae]
    cmp r7, r0
    blt ov005_021e55e4_L110
ov005_021e55e4_L178:
    ldr r1, =0x021ed438
    ldr r0, =0x000003e7
    ldr r3, [r1, #0x40]
    mov r1, #0
    ldr r2, [r3, #0x44]
    cmp r2, r0
    movhi r2, r0
    ldr r0, =0x021edf5c
    strh r2, [r0, #86]
    strh r1, [r0, #84]
    strh r1, [r0, #88]
    ldr r1, [r3, #0x40]
    ldr r0, =0x021edd5c
    str r1, [r0, #0x250]
    bl native_fn_020633bc
    ldr r2, [r0]
    ldr r0, =0x88888889
    ldr r1, =0x021edd5c
    umull r0, r3, r2, r0
    mov r3, r3, lsr #4
    str r3, [r1, #0x25c]
    bl native_fn_0206434c
    ldr r1, =0x021edf5c
    strh r0, [r1, #96]
    bl native_fn_0206442c
    ldrh r2, [r0]
    ldr r0, =0x021edf5c
    ldr r1, =0x021edd5c
    strh r2, [r0, #100]
    mov r0, r8
    mov r2, #20
    bl native_fn_02008e0c
    ldr r1, =0x021ed438
    ldr r2, =0x021edd5c
    mov r0, #4096
    ldr r3, [r2, #0x14]
    rsb r0, r0, #0
    and r5, r3, r0
    ldr r4, [r1, #0x4c]
    ldr r3, [r1, #0x50]
    and r0, r4, r0, lsr #20
    orr r0, r5, r0
    bic r4, r0, #61440
    mov r0, r3, lsl #28
    orr r0, r4, r0, lsr #16
    str r0, [r2, #0x14]
    bic r3, r0, #2031616
    ldr r0, [r1, #0x54]
    mov r0, r0, lsl #27
    orr r0, r3, r0, lsr #11
    str r0, [r2, #0x14]
    bl native_fn_0206442c
    ldr r1, =0x021edd5c
    ldrh r3, [r0]
    ldr r0, =0x001fffff
    ldr r4, [r1, #0x14]
    mov r2, #1
    and r0, r4, r0
    orr r0, r0, r3, lsl #21
    str r0, [r1, #0x14]
    ldr r0, =0x021ed438
    strb r2, [r1, #0xaf]
    ldrb r1, [r0, #0x7]
    tst r1, #1
    ldrnesb r1, [r0]
    subne r0, r2, #2
    cmpne r1, r0
    beq ov005_021e55e4_L3a8
    bl native_fn_02063f6c
    ldr r1, =0x021ed438
    mov r5, r0
    ldrsb r1, [r1]
    add r0, r5, #80
    mov r2, #616
    mla r0, r1, r2, r0
    ldr r1, =0x021edd5c
    bl native_fn_02008e0c
    ldr r4, =0x021edd5c
    mov r0, #0
    strb r0, [r4, #0x25b]
    ldrb r0, [r4, #0x262]
    add r0, r0, #1
    and r1, r0, #255
    strb r0, [r4, #0x262]
    cmp r1, #7
    movlo r0, #24
    mlacc r4, r1, r0, r4
    blo ov005_021e55e4_L310
    mov r10, #24
    ldr r7, =0x021edd74
    mov r6, #1
    mov r9, r10
ov005_021e55e4_L2e8:
    add r1, r6, #1
    mla r0, r1, r9, r4
    mov r1, r7
    mov r2, r10
    bl native_fn_02008e0c
    add r6, r6, #1
    cmp r6, #6
    add r7, r7, #24
    blt ov005_021e55e4_L2e8
    ldr r4, =0x021eddec
ov005_021e55e4_L310:
    mov r0, r8
    mov r1, r4
    mov r2, #20
    bl native_fn_02008e0c
    ldr r1, =0x021ed438
    mov r0, #4096
    ldr r6, [r4, #0x14]
    rsb r0, r0, #0
    ldr r3, [r1, #0x4c]
    and r6, r6, r0
    and r0, r3, r0, lsr #20
    orr r6, r6, r0
    ldr r2, [r1, #0x50]
    bic r3, r6, #61440
    mov r0, r2, lsl #28
    orr r2, r3, r0, lsr #16
    str r2, [r4, #0x14]
    ldr r0, [r1, #0x54]
    bic r1, r2, #2031616
    mov r0, r0, lsl #27
    orr r0, r1, r0, lsr #11
    str r0, [r4, #0x14]
    bl native_fn_0206442c
    ldr r1, =0x021ed438
    mov r2, #616
    ldrsb r3, [r1]
    ldr r6, [r4, #0x14]
    ldr r1, =0x001fffff
    mla r2, r3, r2, r5
    ldrh r0, [r0]
    and r1, r6, r1
    orr r0, r1, r0, lsl #21
    str r0, [r4, #0x14]
    ldrb r0, [r2, #0xff]
    cmp r0, #2
    ldreq r0, =0x021edd5c
    moveq r1, #2
    streqb r1, [r0, #0xaf]
ov005_021e55e4_L3a8:
    ldr r0, =0x021edd5c
    bl native_fn_021e1014
    ldr r2, =0x021edf5c
    ldr r1, =0x021ed438
    strh r0, [r2, #102]
    ldr r0, [r1, #0x2c]
    mov r3, #616
    cmp r0, #0
    bne ov005_021e55e4_L3f0
    ldr r0, =0x021edaf4
    ldr r4, =native_data_021e7874
    str r0, [sp]
    ldr r0, =0x80001517
    ldr r1, =native_fn3_021e54e8
    ldr r2, =0x021edd5c
    stmib sp, {r3, r4}
    bl native_fn_021d9158
    b ov005_021e55e4_L410
ov005_021e55e4_L3f0:
    ldr r0, =0x021ed88c
    ldr r4, =native_data_021e787c
    str r0, [sp]
    ldr r0, =0x80001517
    ldr r1, =native_fn3_021e54e8
    ldr r2, =0x021edd5c
    stmib sp, {r3, r4}
    bl native_fn_021d9158
ov005_021e55e4_L410:
    mov r0, #2
    bl native_fn_0203d294
    add r1, r0, #5
    mov r0, #60
    mul r0, r1, r0
    add r0, r0, r0, lsr #31
    ldr r1, =0x021ed438
    mov r0, r0, asr #1
    str r0, [r1, #0x24]
    bl native_fn_021d8ff0
    ldr r0, =0x021ed438
    ldrb r1, [r0, #0x7]
    add r1, r1, #1
    strb r1, [r0, #0x7]
    add sp, sp, #76
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
