/* ov000 row 0x021d8ccc: 488 bytes.
 *
 * What it does: 119 instructions; 18 call(s) to 0x021d8ce8, 0x021d8ea0, 0x02025a28, +15 more; loops (back edge at +0x54); returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1dc -> constant 0x02230318 (image word 0x02230318)
 *   pool +0x1e0 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x1e4 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x08 -> +0x1c
 *   branch +0x40 -> +0x1d4
 *   branch +0x50 -> +0x68
 *   branch +0x64 -> +0x74
 *   branch +0xd0 -> +0xe8
 *   branch +0xe4 -> +0xf4
 *   test +0x04 cmp r0, #0
 *   test +0x1c cmp r1, #0
 *   test +0x28 cmp r2, #0
 *   test +0x3c cmp r5, #0
 *   test +0x48 cmp r4, #0
 *   test +0xc8 cmp r0, #0
 *   test +0x168 cmp r5, #4096
 *   test +0x1c8 cmp r2, r0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021d8ccc; the literal pool and
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

extern void native_fn_02025a28(void);
extern void native_fn_02024e0c(void);
extern void native_fn_02025ca4(void);
extern void native_fn_020259b4(void);
extern void native_fn_02026144(void);
extern void native_fn_0203d294(void);
extern void native_fn_021d8a50(void);
extern void native_fn_021d8aa0(void);


asm u32 native_ov000_021d8ccc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    cmp r0, #0
    blt ov000_021d8ccc_L1c
    ldr r3, =0x02230318
    mov r4, #0
    str r0, [r3, #0xc]
    strh r4, [r3]
ov000_021d8ccc_L1c:
    cmp r1, #0
    ldrgt r0, =0x02230318
    strgt r1, [r0, #0x10]
    cmp r2, #0
    ldrgt r0, =0x02230318
    strgt r2, [r0, #0x14]
    ldr r0, =0x02230318
    ldr r5, [r0, #0xc]
    cmp r5, #0
    ble ov000_021d8ccc_L1d4
    ldrh r4, [r0]
    cmp r4, #0
    mov r0, r4, lsl #12
    beq ov000_021d8ccc_L68
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021d8ccc_L74
ov000_021d8ccc_L68:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021d8ccc_L74:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r12, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r12, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r0, r0, lsl #1
    add r1, r0, #1
    mov r2, #90
    mul r0, r4, r2
    mov r3, r1, lsl #1
    ldr r2, =0x020d3fe0
    mov r1, r5
    ldrsh r4, [r2, r3]
    bl native_fn_02026144
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov000_021d8ccc_Le8
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021d8ccc_Lf4
ov000_021d8ccc_Le8:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021d8ccc_Lf4:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r5, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r5, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r0, r0, lsl #1
    add r2, r0, #1
    ldr r0, =0x02230318
    ldr r1, =0x020d3fe0
    ldr r3, [r0, #0x14]
    mov r2, r2, lsl #1
    ldrsh r0, [r1, r2]
    mov r5, r3, asr #1
    smull r2, r1, r0, r3
    adds r2, r2, #2048
    adc r0, r1, #0
    mov r1, r2, lsr #12
    orr r1, r1, r0, lsl #20
    smull r1, r0, r4, r1
    adds r1, r1, #2048
    adc r0, r0, #0
    mov r4, r1, lsr #12
    cmp r5, #4096
    movlt r5, #4096
    orr r4, r4, r0, lsl #20
    mov r0, r5
    bl native_fn_0203d294
    mov r0, r5
    bl native_fn_0203d294
    mov r0, #0
    bl native_fn_021d8a50
    ldr r1, [r0, #0x4]
    add r1, r1, r4
    str r1, [r0, #0x4]
    mov r0, #0
    bl native_fn_021d8aa0
    ldr r2, [r0, #0x4]
    ldr r1, =0x02230318
    sub r2, r2, r4, asr #1
    str r2, [r0, #0x4]
    ldrh r2, [r1]
    ldr r0, [r1, #0x10]
    add r0, r2, r0
    strh r0, [r1]
    ldrh r2, [r1]
    ldr r0, [r1, #0xc]
    cmp r2, r0
    movgt r0, #0
    strgt r0, [r1, #0xc]
ov000_021d8ccc_L1d4:
    mov r0, #1
    ldmia sp!, {r3, r4, r5, pc}
}
