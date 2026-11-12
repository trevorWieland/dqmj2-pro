/* ov000 row 0x02219728: 440 bytes.
 *
 * What it does: Copies a 8-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x1a4 -> constant 0x02245ee4 (image word 0x02245ee4)
 *   pool +0x1a8 -> constant 0xb60b60b7 (image word 0xb60b60b7)
 *   pool +0x1ac -> constant 0x02245e54 (image word 0x02245e54)
 *   pool +0x1b0 -> constant 0x9999999a (image word 0x9999999a)
 *   pool +0x1b4 -> constant 0x3fe99999 (image word 0x3fe99999)
 *   branch +0x70 -> +0xb0
 *   branch +0xac -> +0x194
 *   test +0x6c cmp r0, #0
 *   0 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02219728; the literal pool and
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

extern void native_fn_0205f98c(void);
extern void native_fn_021d8a44(void);
extern void native_fn_02028158(void);
extern void native_fn_0203517c(void);
extern void native_fn_021df1f0(void);
extern void native_fn_021df3bc(void);
extern void native_fn_021e07ac(void);
extern void native_fn_02041f74(void);
extern void native_fn_020244c4(void);
extern void native_fn_02024540(void);
extern void native_fn_02023f78(void);
extern void native_fn_02024394(void);
extern void native_fn_02048a60(void);


asm u32 native_ov000_02219728 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #12
    ldr r5, =0x02245ee4
    mov r1, #0
    ldr r0, [r5, #0x1c]
    bl native_fn_0205f98c
    mov r6, r0
    bl native_fn_021d8a44
    ldr r0, [r0, #0x4c]
    add r0, r0, #737280
    bl native_fn_02028158
    add r0, r0, #43008
    add r3, r0, #786432
    ldr r2, =0xb60b60b7
    mov r0, r3, lsr #31
    smull r1, r4, r2, r3
    add r4, r3, r4
    add r4, r0, r4, asr #17
    and r0, r4, #7
    mov r0, r0, lsl #24
    mov r0, r0, asr #24
    mov r1, r0, lsl #16
    add r0, r6, #8
    mov r1, r1, lsr #16
    bl native_fn_0203517c
    ldr r1, =0x02245e54
    ldr r0, [r1, #0x20]
    cmp r0, #0
    bne ov000_02219728_Lb0
    ldrsh r3, [r5, #20]
    ldr r2, [r1, #0x4c]
    ldr r0, [r1, #0x40]
    ldrsh r4, [r5, #22]
    sub r0, r2, r0
    add r0, r3, r0, asr #12
    mov r0, r0, lsl #16
    ldr r3, [r1, #0x54]
    ldr r2, [r1, #0x48]
    mov r1, r0, asr #16
    sub r0, r3, r2
    add r0, r4, r0, asr #12
    mov r0, r0, lsl #16
    mov r2, r0, asr #16
    b ov000_02219728_L194
ov000_02219728_Lb0:
    bl native_fn_021df1f0
    bl native_fn_021df3bc
    ldrsh r1, [r0, #4]
    ldrsh r0, [r0, #6]
    mov r4, r1, lsl #12
    mov r7, r0, lsl #12
    bl native_fn_021e07ac
    add r1, sp, #0
    bl native_fn_02041f74
    mov r0, r4
    bl native_fn_020244c4
    mov r4, r0
    ldr r0, [sp]
    mov r8, r1
    bl native_fn_020244c4
    mov r2, r0
    mov r3, r1
    ldr r0, =0x9999999a
    ldr r1, =0x3fe99999
    bl native_fn_02024540
    mov r2, r0
    mov r3, r1
    mov r0, r4
    mov r1, r8
    bl native_fn_02023f78
    bl native_fn_02024394
    mov r4, r0
    mov r0, r7
    bl native_fn_020244c4
    mov r7, r0
    ldr r0, [sp, #0x8]
    mov r8, r1
    bl native_fn_020244c4
    mov r2, r0
    mov r3, r1
    ldr r0, =0x9999999a
    ldr r1, =0x3fe99999
    bl native_fn_02024540
    mov r2, r0
    mov r3, r1
    mov r0, r7
    mov r1, r8
    bl native_fn_02023f78
    bl native_fn_02024394
    ldr r1, =0x02245e54
    ldrsh r12, [r5, #20]
    ldr r3, [r1, #0x40]
    ldr r2, [r1, #0x48]
    sub r1, r4, r3
    add r1, r12, r1, asr #12
    mov r1, r1, lsl #16
    ldrsh r3, [r5, #22]
    sub r0, r0, r2
    mov r1, r1, asr #16
    add r0, r3, r0, asr #12
    mov r0, r0, lsl #16
    mov r2, r0, asr #16
ov000_02219728_L194:
    mov r0, r6
    bl native_fn_02048a60
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
