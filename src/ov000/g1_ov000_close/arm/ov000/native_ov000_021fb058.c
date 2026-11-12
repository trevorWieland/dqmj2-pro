/* ov000 row 0x021fb058: 504 bytes.
 *
 * What it does: 123 instructions; 21 call(s) to 0x02215d94, 0x021fb8f8, 0x02215d94, +18 more; loops (back edge at +0x6c); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1ec -> constant 0x02237170 (image word 0x02237170)
 *   pool +0x1f0 -> constant 0x51eb851f (image word 0x51eb851f)
 *   pool +0x1f4 -> constant 0x0223716c (image word 0x0223716c)
 *   branch +0x3c -> +0x1e0
 *   branch +0xa8 -> +0x1c0
 *   branch +0x128 -> +0x178
 *   branch +0x130 -> +0x150
 *   branch +0x14c -> +0x178
 *   branch +0x198 -> +0x1a4
 *   branch +0x1bc -> +0x1e0
 *   back edge +0x1dc -> +0x48
 *   test +0x38 cmp r6, #255
 *   test +0xa4 cmp r0, r7
 *   test +0x120 cmp r0, r7
 *   test +0x12c cmp r0, r9
 *   test +0x184 cmp r0, r4
 *   test +0x190 cmp r1, #1
 *   test +0x19c cmp r0, r4
 *   test +0x1d8 cmp r6, #255
 *   0 block transfer(s), 9 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021fb058; the literal pool and
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

extern void native_fn_02215d94(void);
extern void native_fn_021fb8f8(void);
extern void native_fn_021fb97c(void);
extern void native_fn_0207b244(void);
extern void native_fn_0207afec(void);
extern void native_fn_0203d294(void);
extern void native_fn_02210f74(void);
extern void native_fn_0207b460(void);
extern void native_fn_0207c73c(void);
extern void native_fn_02026144(void);
extern void native_fn_0207d198(void);
extern void native_fn_021fbc9c(void);


asm u32 native_ov000_021fb058 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    mov r10, r0
    mov r9, r1
    mov r1, #0
    and r0, r2, #255
    str r3, [sp]
    str r1, [sp, #0x8]
    bl native_fn_02215d94
    str r0, [sp, #0x4]
    mov r0, r10
    mov r1, r9
    bl native_fn_021fb8f8
    mov r6, r0
    cmp r6, #255
    beq ov000_021fb058_L1e0
    ldr r4, =0x02237170
    mov r11, #52
ov000_021fb058_L48:
    and r0, r6, #255
    bl native_fn_02215d94
    mov r8, r0
    and r0, r6, #255
    bl native_fn_021fb97c
    mov r5, r0
    ldrsh r1, [r5, #38]
    mov r0, r10
    mov r2, r8
    bl native_fn_0207b244
    ldrsh r1, [r5, #38]
    sub r0, r1, r0
    strh r0, [r5, #38]
    mov r0, r10
    bl native_fn_0207afec
    ldrsh r7, [r0, #16]
    mov r0, r10
    bl native_fn_0207afec
    mla r1, r6, r11, r4
    ldrsh r2, [r5, #38]
    mov r0, #100
    str r2, [r1, #0xc]
    bl native_fn_0203d294
    cmp r0, r7
    bge ov000_021fb058_L1c0
    ldr r0, [sp]
    ldr r1, [sp, #0x4]
    mov r3, #0
    mov r2, r0
    strb r3, [r2, #0x33]
    bl native_fn_02210f74
    mov r4, r0
    mov r0, r10
    bl native_fn_0207afec
    ldrsh r1, [r0, #18]
    ldr r2, =0x51eb851f
    mov r0, r10
    mul r3, r4, r1
    smull r1, r6, r2, r3
    mov r1, r3, lsr #31
    add r6, r1, r6, asr #5
    bl native_fn_0207afec
    ldrsh r7, [r0, #24]
    mov r0, r10
    bl native_fn_0207afec
    ldrsh r9, [r0, #26]
    ldrsh r0, [r5, #24]
    ldrb r1, [r5, #0x1a]
    add r2, r5, #122
    mov r3, r8
    bl native_fn_0207b460
    add r0, r5, #32
    mov r1, r8
    bl native_fn_0207c73c
    cmp r0, r7
    movle r2, #1
    ble ov000_021fb058_L178
    cmp r0, r9
    blt ov000_021fb058_L150
    mov r0, #100
    mul r1, r6, r0
    ldr r3, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r2, r3, r1
    add r2, r0, r2, asr #5
    b ov000_021fb058_L178
ov000_021fb058_L150:
    sub r0, r0, r7
    mul r0, r6, r0
    sub r1, r9, r7
    bl native_fn_02026144
    mov r1, #100
    mul r1, r0, r1
    ldr r3, =0x51eb851f
    mov r0, r1, lsr #31
    smull r1, r2, r3, r1
    add r2, r0, r2, asr #5
ov000_021fb058_L178:
    mov r0, r8
    mov r1, r10
    bl native_fn_0207d198
    cmp r0, r4
    movlt r1, r0
    movge r1, r4
    cmp r1, #1
    movlt r0, #1
    blt ov000_021fb058_L1a4
    cmp r0, r4
    movge r0, r4
ov000_021fb058_L1a4:
    ldr r1, [sp]
    ldr r2, =0x0223716c
    strh r0, [r1, #36]
    mov r0, #1
    str r0, [sp, #0x8]
    strb r0, [r2]
    b ov000_021fb058_L1e0
ov000_021fb058_L1c0:
    mov r0, r9
    bl native_fn_021fbc9c
    mov r0, r10
    mov r1, r9
    bl native_fn_021fb8f8
    mov r6, r0
    cmp r6, #255
    bne ov000_021fb058_L48
ov000_021fb058_L1e0:
    ldr r0, [sp, #0x8]
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
