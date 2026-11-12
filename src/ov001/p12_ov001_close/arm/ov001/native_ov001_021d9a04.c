/* ov001 row 0x021d9a04: 776 bytes.
 *
 * What it does: 194 instructions; 39 call(s) to 0x02008d78, 0x02008e0c, 0x0207b674, +36 more; loops (back edge at +0x24); returns through pop {r4, r5, r6, r7, r8, pc}
 *
 * Decoded shape: loop with 39 calls (194 instructions, 39 calls, 12 branches, 33 back edges, 0 literal slots).
 *
 *   branch +0x30 -> +0x48
 *   branch +0x58 -> +0x88
 *   branch +0x98 -> +0xc8
 *   branch +0xd8 -> +0x108
 *   branch +0x118 -> +0x148
 *   branch +0x158 -> +0x188
 *   branch +0x198 -> +0x1c8
 *   branch +0x1d8 -> +0x218
 *   branch +0x228 -> +0x268
 *   branch +0x280 -> +0x2d0
 *   branch +0x28c -> +0x2cc
 *   branch +0x2b0 -> +0x2cc
 *   branch +0x2e4 -> +0x300
 *   test +0x2c cmp r0, #0
 *   test +0x54 cmp r0, #0
 *   test +0x94 cmp r0, #0
 *   test +0xd4 cmp r0, #0
 *   test +0x114 cmp r0, #0
 *   test +0x154 cmp r0, #0
 *   test +0x194 cmp r0, #0
 *   test +0x1d4 cmp r0, #0
 *   test +0x224 cmp r0, #0
 *   test +0x27c cmp r1, #0
 *   test +0x284 cmp r6, #0
 *   test +0x2a8 cmp r0, #1
 *   0 block transfer(s), 14 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d9a04; the literal pool and
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

extern void native_fn_02008d78(void);
extern void native_fn_02008e0c(void);
extern void native_fn_0207b674(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0203d294(void);
extern void native_fn_0207c3d8(void);
extern void native_fn_0207c424(void);
extern void native_fn_0207c52c(void);
extern void native_fn_0207c634(void);
extern void native_fn_0207c73c(void);
extern void native_fn_021dbcbc(void);
extern void native_fn_021dbcf0(void);
extern void native_fn_02026144(void);


asm u32 native_ov001_021d9a04 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    mov r7, r1
    add r6, r7, #540
    mov r8, r0
    mov r0, r6
    mov r1, #0
    mov r2, #16
    add r5, r7, #492
    ldr r4, [r7, #0x1e8]
    bl native_fn_02008d78
    ldrb r0, [r8, #0x202]
    cmp r0, #0
    beq ov001_021d9a04_L48
    add r0, r8, #436
    mov r1, r6
    mov r2, #16
    bl native_fn_02008e0c
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
ov001_021d9a04_L48:
    add r1, r4, #70
    mov r0, #79
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L88
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c2b8
    bl native_fn_0203d294
    mov r8, r0
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c2b8
    add r0, r0, r0, lsr #31
    sub r0, r8, r0, asr #1
    strh r0, [r6]
ov001_021d9a04_L88:
    add r1, r4, #70
    mov r0, #80
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_Lc8
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c3d8
    bl native_fn_0203d294
    mov r8, r0
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c3d8
    add r0, r0, r0, lsr #31
    sub r0, r8, r0, asr #1
    strh r0, [r6, #2]
ov001_021d9a04_Lc8:
    add r1, r4, #70
    mov r0, #81
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L108
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c424
    bl native_fn_0203d294
    mov r8, r0
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c424
    add r0, r0, r0, lsr #31
    sub r0, r8, r0, asr #1
    strh r0, [r6, #4]
ov001_021d9a04_L108:
    add r1, r4, #70
    mov r0, #82
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L148
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c52c
    bl native_fn_0203d294
    mov r8, r0
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c52c
    add r0, r0, r0, lsr #31
    sub r0, r8, r0, asr #1
    strh r0, [r6, #6]
ov001_021d9a04_L148:
    add r1, r4, #70
    mov r0, #83
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L188
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c634
    bl native_fn_0203d294
    mov r8, r0
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c634
    add r0, r0, r0, lsr #31
    sub r0, r8, r0, asr #1
    strh r0, [r6, #8]
ov001_021d9a04_L188:
    add r1, r4, #70
    mov r0, #84
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L1c8
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c73c
    bl native_fn_0203d294
    mov r8, r0
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c73c
    add r0, r0, r0, lsr #31
    sub r0, r8, r0, asr #1
    strh r0, [r6, #10]
ov001_021d9a04_L1c8:
    add r1, r4, #70
    mov r0, #85
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L218
    mov r0, r7
    bl native_fn_021dbcbc
    add r0, r0, r0, lsr #31
    ldrsh r1, [r6]
    mov r0, r0, lsl #15
    add r0, r1, r0, asr #16
    strh r0, [r6]
    ldrsh r0, [r5, #10]
    sub r0, r0, #1
    rsb r0, r0, #0
    strh r0, [r6, #6]
    ldrsh r0, [r5, #8]
    sub r0, r0, #1
    rsb r0, r0, #0
    strh r0, [r6, #4]
ov001_021d9a04_L218:
    add r1, r4, #70
    mov r0, #86
    bl native_fn_0207b674
    cmp r0, #0
    beq ov001_021d9a04_L268
    mov r0, r7
    bl native_fn_021dbcf0
    add r0, r0, r0, lsr #31
    ldrsh r1, [r6, #2]
    mov r0, r0, lsl #15
    add r0, r1, r0, asr #16
    strh r0, [r6, #2]
    ldrsh r0, [r5, #8]
    sub r0, r0, #1
    rsb r0, r0, #0
    strh r0, [r6, #4]
    ldrsh r0, [r5, #14]
    sub r0, r0, #1
    rsb r0, r0, #0
    strh r0, [r6, #10]
ov001_021d9a04_L268:
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c2b8
    ldrsh r1, [r5, #4]
    mov r6, r0
    cmp r1, #0
    beq ov001_021d9a04_L2d0
    cmp r6, #0
    moveq r0, #0
    beq ov001_021d9a04_L2cc
    mov r0, r7
    bl native_fn_021dbcbc
    ldrsh r2, [r5, #4]
    mov r1, r6
    mul r0, r2, r0
    bl native_fn_02026144
    cmp r0, #1
    movlt r0, #1
    blt ov001_021d9a04_L2cc
    mov r0, r7
    bl native_fn_021dbcbc
    ldrsh r2, [r5, #4]
    mov r1, r6
    mul r0, r2, r0
    bl native_fn_02026144
ov001_021d9a04_L2cc:
    strh r0, [r5, #4]
ov001_021d9a04_L2d0:
    mov r0, r5
    add r1, r4, #70
    bl native_fn_0207c3d8
    movs r4, r0
    moveq r0, #0
    beq ov001_021d9a04_L300
    mov r0, r7
    bl native_fn_021dbcf0
    ldrsh r2, [r5, #6]
    mov r1, r4
    mul r0, r2, r0
    bl native_fn_02026144
ov001_021d9a04_L300:
    strh r0, [r5, #6]
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
