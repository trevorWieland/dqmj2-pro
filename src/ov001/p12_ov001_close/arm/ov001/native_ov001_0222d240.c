/* ov001 row 0x0222d240: 1696 bytes.
 *
 * What it does: 405 instructions; 106 call(s) to 0x02008d78, 0x02008d78, 0x0222d8e0, +103 more; loops (back edge at +0x1c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 19 literal slot(s) in the extent
 *
 * Decoded shape: loop with 106 calls (405 instructions, 106 calls, 7 branches, 84 back edges, 19 literal slots).
 *
 *   pool +0x654 -> constant 0x0224992c (image word 0x0224992c)
 *   pool +0x658 -> constant 0x022498fc (image word 0x022498fc)
 *   pool +0x65c -> constant 0x02249830 (image word 0x02249830)
 *   pool +0x660 -> constant 0x3fa00000 (image word 0x3fa00000)
 *   pool +0x664 -> constant 0x3f266666 (image word 0x3f266666)
 *   pool +0x668 -> constant 0x3f933333 (image word 0x3f933333)
 *   pool +0x66c -> constant 0x42b40000 (image word 0x42b40000)
 *   pool +0x670 -> constant 0x42c80000 (image word 0x42c80000)
 *   pool +0x674 -> constant 0x3c449ba6 (image word 0x3c449ba6)
 *   pool +0x678 -> constant 0x0000270f (image word 0x0000270f)
 *   pool +0x67c -> constant 0x0224991c (image word 0x0224991c)
 *   pool +0x680 -> constant 0x02249920 (image word 0x02249920)
 *   pool +0x684 -> constant 0x0224991e (image word 0x0224991e)
 *   pool +0x688 -> constant 0x02249922 (image word 0x02249922)
 *   pool +0x68c -> constant 0x02249924 (image word 0x02249924)
 *   pool +0x690 -> constant 0x02249926 (image word 0x02249926)
 *   pool +0x694 -> constant 0x02249928 (image word 0x02249928)
 *   pool +0x698 -> constant 0x0224992a (image word 0x0224992a)
 *   pool +0x69c -> constant 0x0224983c (image word 0x0224983c)
 *   branch +0x38 -> +0x1a8
 *   branch +0x54 -> +0x1a4
 *   back edge +0x1a0 -> +0x70
 *   branch +0x1b8 -> +0x1d8
 *   branch +0x1c0 -> +0x1e4
 *   branch +0x1d4 -> +0x1f0
 *   branch +0x1e0 -> +0x1f0
 *   branch +0x3f0 -> +0x4a8
 *   branch +0x4bc -> +0x4d8
 *   branch +0x4d4 -> +0x4f4
 *   branch +0x500 -> +0x51c
 *   branch +0x518 -> +0x538
 *   branch +0x550 -> +0x560
 *   branch +0x578 -> +0x588
 *   branch +0x5a0 -> +0x5b0
 *   branch +0x5c8 -> +0x5d8
 *   test +0x34 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0x19c cmp r7, r0
 *   test +0x1b4 cmp r0, #0
 *   test +0x1bc cmp r0, #1
 *   test +0x1c4 cmp r0, #2
 *   test +0x3ec cmp r0, #40
 *   test +0x4b8 cmp r1, r3
 *   test +0x4fc cmp r1, r3
 *   test +0x540 cmp r2, r1
 *   test +0x568 cmp r2, r1
 *   test +0x590 cmp r2, r1
 *   test +0x5b8 cmp r2, r1
 *   0 block transfer(s), 44 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0222d240; the literal pool and
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
extern void native_fn_0222d8e0(void);
extern void native_fn_02044a14(void);
extern void native_fn_0222d91c(void);
extern void native_fn_0222d964(void);
extern void native_fn_02044a58(void);
extern void native_fn_02044a9c(void);
extern void native_fn_02044ae0(void);
extern void native_fn_02044b24(void);
extern void native_fn_02044b68(void);
extern void native_fn_0222d93c(void);
extern void native_fn_02044cdc(void);
extern void native_fn_0203d294(void);
extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025578(void);
extern void native_fn_020449d4(void);
extern void native_fn_02025ab8(void);
extern void native_fn_02025a70(void);
extern void native_fn_020259b4(void);
extern void native_fn_0207c2b8(void);
extern void native_fn_0207c3d8(void);
extern void native_fn_0207c424(void);
extern void native_fn_0207c52c(void);
extern void native_fn_0207c634(void);
extern void native_fn_0207c73c(void);


asm u32 native_ov001_0222d240 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #72
    mov r10, r0
    str r1, [sp]
    add r0, sp, #40
    mov r1, #0
    mov r2, #32
    bl native_fn_02008d78
    add r0, sp, #8
    mov r1, #0
    mov r2, #32
    bl native_fn_02008d78
    bl native_fn_0222d8e0
    cmp r0, #0
    beq ov001_0222d240_L1a8
    mov r0, #132
    mul r1, r10, r0
    ldr r0, =0x0224992c
    mov r7, #0
    ldrb r0, [r0, r1]
    cmp r0, #0
    bls ov001_0222d240_L1a4
    ldr r0, =0x022498fc
    ldr r6, =0x02249830
    add r9, r0, r1
    mov r5, r7
    mov r4, r7
    mov r11, r7
ov001_0222d240_L70:
    ldr r0, [r6, r10, lsl #2]
    mov r1, r5
    mov r2, r7
    bl native_fn_02044a14
    mov r1, r7
    bl native_fn_0222d91c
    mov r1, r0
    ldrb r0, [r9, #0x1a]
    bl native_fn_0222d964
    ldr r2, [sp, #0x28]
    mov r1, r4
    add r0, r2, r0
    str r0, [sp, #0x28]
    ldr r0, [r6, r10, lsl #2]
    mov r2, r7
    bl native_fn_02044a58
    mov r1, r7
    bl native_fn_0222d91c
    mov r1, r0
    ldrb r0, [r9, #0x1a]
    bl native_fn_0222d964
    ldr r2, [sp, #0x2c]
    mov r1, r11
    add r0, r2, r0
    str r0, [sp, #0x2c]
    ldr r0, [r6, r10, lsl #2]
    mov r2, r7
    bl native_fn_02044a9c
    mov r1, r7
    bl native_fn_0222d91c
    mov r1, r0
    ldrb r0, [r9, #0x1a]
    bl native_fn_0222d964
    ldr r2, [sp, #0x38]
    mov r1, #0
    add r0, r2, r0
    str r0, [sp, #0x38]
    ldr r0, [r6, r10, lsl #2]
    mov r2, r7
    bl native_fn_02044ae0
    mov r1, r7
    bl native_fn_0222d91c
    mov r1, r0
    ldrb r0, [r9, #0x1a]
    bl native_fn_0222d964
    ldr r2, [sp, #0x3c]
    mov r1, #0
    add r0, r2, r0
    str r0, [sp, #0x3c]
    ldr r0, [r6, r10, lsl #2]
    mov r2, r7
    bl native_fn_02044b24
    mov r1, r7
    bl native_fn_0222d91c
    mov r1, r0
    ldrb r0, [r9, #0x1a]
    bl native_fn_0222d964
    ldr r2, [sp, #0x40]
    mov r1, #0
    add r0, r2, r0
    str r0, [sp, #0x40]
    ldr r0, [r6, r10, lsl #2]
    mov r2, r7
    bl native_fn_02044b68
    mov r1, r7
    bl native_fn_0222d91c
    mov r1, r0
    ldrb r0, [r9, #0x1a]
    bl native_fn_0222d964
    ldr r2, [sp, #0x44]
    add r1, r7, #1
    add r0, r2, r0
    str r0, [sp, #0x44]
    ldrb r0, [r9, #0x30]
    and r7, r1, #255
    cmp r7, r0
    blo ov001_0222d240_L70
ov001_0222d240_L1a4:
    bl native_fn_0222d93c
ov001_0222d240_L1a8:
    ldr r0, =0x02249830
    ldr r0, [r0, r10, lsl #2]
    bl native_fn_02044cdc
    cmp r0, #0
    beq ov001_0222d240_L1d8
    cmp r0, #1
    beq ov001_0222d240_L1e4
    cmp r0, #2
    moveq r0, #1065353216
    ldreq r8, =0x3fa00000
    streq r0, [sp, #0x4]
    b ov001_0222d240_L1f0
ov001_0222d240_L1d8:
    mov r8, #1065353216
    str r8, [sp, #0x4]
    b ov001_0222d240_L1f0
ov001_0222d240_L1e4:
    ldr r0, =0x3f266666
    ldr r8, =0x3f933333
    str r0, [sp, #0x4]
ov001_0222d240_L1f0:
    mov r0, #20
    bl native_fn_0203d294
    bl native_fn_02025a28
    mov r1, r0
    ldr r0, =0x42b40000
    bl native_fn_02024e0c
    ldr r1, =0x42c80000
    bl native_fn_02025578
    ldr r1, =0x02249830
    mov r4, r0
    ldr r0, [r1, r10, lsl #2]
    bl native_fn_020449d4
    mov r6, r0
    ldr r0, [sp, #0x28]
    bl native_fn_02025a28
    mov r1, r8
    bl native_fn_02025ab8
    mov r5, r0
    ldrh r0, [r6, #28]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x10]
    ldr r0, =0x02249830
    ldr r0, [r0, r10, lsl #2]
    bl native_fn_020449d4
    mov r6, r0
    ldr r0, [sp, #0x2c]
    bl native_fn_02025a28
    mov r1, r8
    bl native_fn_02025ab8
    mov r5, r0
    ldrh r0, [r6, #30]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x14]
    ldr r0, =0x02249830
    ldr r0, [r0, r10, lsl #2]
    bl native_fn_020449d4
    mov r6, r0
    ldr r0, [sp, #0x38]
    bl native_fn_02025a28
    mov r1, r8
    bl native_fn_02025ab8
    mov r5, r0
    ldrh r0, [r6, #32]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    mov r1, r0
    ldr r0, [sp, #0x4]
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x18]
    ldr r0, =0x02249830
    ldr r0, [r0, r10, lsl #2]
    bl native_fn_020449d4
    mov r6, r0
    ldr r0, [sp, #0x3c]
    bl native_fn_02025a28
    mov r1, r8
    bl native_fn_02025ab8
    mov r5, r0
    ldrh r0, [r6, #34]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x1c]
    ldr r0, =0x02249830
    ldr r0, [r0, r10, lsl #2]
    bl native_fn_020449d4
    mov r6, r0
    ldr r0, [sp, #0x40]
    bl native_fn_02025a28
    mov r1, r8
    bl native_fn_02025ab8
    mov r5, r0
    ldrh r0, [r6, #36]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    ldr r1, =0x02249830
    str r0, [sp, #0x20]
    ldr r0, [r1, r10, lsl #2]
    bl native_fn_020449d4
    mov r6, r0
    ldr r0, [sp, #0x44]
    bl native_fn_02025a28
    mov r1, r8
    bl native_fn_02025ab8
    mov r5, r0
    ldrh r0, [r6, #38]
    bl native_fn_02025a70
    mov r1, r0
    mov r0, r5
    bl native_fn_02024e0c
    mov r1, r0
    mov r0, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x24]
    ldr r0, [sp]
    cmp r0, #40
    blo ov001_0222d240_L4a8
    sub r0, r0, #40
    bl native_fn_02025a28
    mov r1, r0
    ldr r0, =0x3c449ba6
    bl native_fn_02025ab8
    mov r1, r0
    mov r0, #1065353216
    bl native_fn_02024e0c
    mov r4, r0
    ldr r0, [sp, #0x10]
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x10]
    ldr r0, [sp, #0x14]
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x14]
    ldr r0, [sp, #0x18]
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x18]
    ldr r0, [sp, #0x1c]
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x1c]
    ldr r0, [sp, #0x20]
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x20]
    ldr r0, [sp, #0x24]
    bl native_fn_02025a28
    mov r1, r4
    bl native_fn_02025ab8
    bl native_fn_020259b4
    str r0, [sp, #0x24]
ov001_0222d240_L4a8:
    mov r0, #132
    mul r0, r10, r0
    ldr r1, [sp, #0x10]
    ldr r3, =0x0000270f
    cmp r1, r3
    ble ov001_0222d240_L4d8
    ldr r2, =0x0224991c
    ldr r1, =0x02249920
    strh r3, [r2, r0]
    strh r3, [r1, r0]
    add r11, r1, r0
    b ov001_0222d240_L4f4
ov001_0222d240_L4d8:
    mov r1, r1, lsl #16
    ldr r2, =0x02249920
    ldr r3, =0x0224991c
    mov r1, r1, asr #16
    strh r1, [r3, r0]
    strh r1, [r2, r0]
    add r11, r2, r0
ov001_0222d240_L4f4:
    ldr r1, [sp, #0x14]
    ldr r3, =0x0000270f
    cmp r1, r3
    ble ov001_0222d240_L51c
    ldr r2, =0x0224991e
    ldr r1, =0x02249922
    strh r3, [r2, r0]
    strh r3, [r1, r0]
    add r5, r1, r0
    b ov001_0222d240_L538
ov001_0222d240_L51c:
    mov r1, r1, lsl #16
    ldr r2, =0x02249922
    ldr r3, =0x0224991e
    mov r1, r1, asr #16
    strh r1, [r3, r0]
    strh r1, [r2, r0]
    add r5, r2, r0
ov001_0222d240_L538:
    ldr r2, [sp, #0x18]
    ldr r1, =0x0000270f
    cmp r2, r1
    ldrle r1, =0x02249924
    strleh r2, [r1, r0]
    addle r6, r1, r0
    ble ov001_0222d240_L560
    ldr r2, =0x02249924
    strh r1, [r2, r0]
    add r6, r2, r0
ov001_0222d240_L560:
    ldr r2, [sp, #0x1c]
    ldr r1, =0x0000270f
    cmp r2, r1
    ldrle r1, =0x02249926
    strleh r2, [r1, r0]
    addle r7, r1, r0
    ble ov001_0222d240_L588
    ldr r2, =0x02249926
    strh r1, [r2, r0]
    add r7, r2, r0
ov001_0222d240_L588:
    ldr r2, [sp, #0x20]
    ldr r1, =0x0000270f
    cmp r2, r1
    ldrle r1, =0x02249928
    strleh r2, [r1, r0]
    addle r8, r1, r0
    ble ov001_0222d240_L5b0
    ldr r2, =0x02249928
    strh r1, [r2, r0]
    add r8, r2, r0
ov001_0222d240_L5b0:
    ldr r2, [sp, #0x24]
    ldr r1, =0x0000270f
    cmp r2, r1
    ldrle r1, =0x0224992a
    strleh r2, [r1, r0]
    addle r9, r1, r0
    ble ov001_0222d240_L5d8
    ldr r2, =0x0224992a
    strh r1, [r2, r0]
    add r9, r2, r0
ov001_0222d240_L5d8:
    ldr r1, =0x022498fc
    mov r0, #132
    mla r4, r10, r0, r1
    ldr r1, =0x0224983c
    add r0, r4, #32
    add r10, r1, r10, lsl #6
    mov r1, r10
    bl native_fn_0207c2b8
    strh r0, [r11]
    mov r1, r10
    add r0, r4, #32
    bl native_fn_0207c3d8
    strh r0, [r5]
    mov r1, r10
    add r0, r4, #32
    bl native_fn_0207c424
    strh r0, [r6]
    mov r1, r10
    add r0, r4, #32
    bl native_fn_0207c52c
    strh r0, [r7]
    mov r1, r10
    add r0, r4, #32
    bl native_fn_0207c634
    strh r0, [r8]
    mov r1, r10
    add r0, r4, #32
    bl native_fn_0207c73c
    strh r0, [r9]
    add sp, sp, #72
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
