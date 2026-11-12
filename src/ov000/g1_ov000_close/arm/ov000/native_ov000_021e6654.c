/* ov000 row 0x021e6654: 488 bytes.
 *
 * What it does: 113 instructions; 14 call(s) to 0x02025a28, 0x02024e0c, 0x02025a28, +11 more; loops (back edge at +0x2c); returns through pop {r4, r5, r6, r7, r8, pc}; 9 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x1c4 -> constant 0x022351c4 (image word 0x022351c4)
 *   pool +0x1c8 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x1cc -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x1d0 -> constant 0x02235110 (image word 0x02235110)
 *   pool +0x1d4 -> constant 0x02235114 (image word 0x02235114)
 *   pool +0x1d8 -> constant 0x02235118 (image word 0x02235118)
 *   pool +0x1dc -> constant 0x0223511c (image word 0x0223511c)
 *   pool +0x1e0 -> constant 0x02235120 (image word 0x02235120)
 *   pool +0x1e4 -> constant 0x02235124 (image word 0x02235124)
 *   branch +0x28 -> +0x40
 *   branch +0x3c -> +0x4c
 *   branch +0xa8 -> +0xc0
 *   branch +0xbc -> +0xcc
 *   test +0x14 cmp r1, #0
 *   test +0x20 cmp r4, #0
 *   test +0xa0 cmp r0, #0
 *   test +0x1b4 cmp r1, r0
 *   0 block transfer(s), 8 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e6654; the literal pool and
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


asm u32 native_ov000_021e6654 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r6, =0x022351c4
    mov r8, r0
    ldrb r1, [r6]
    mov r0, #0
    cmp r1, #0
    ldmeqia sp!, {r4, r5, r6, r7, r8, pc}
    ldrh r4, [r6, #4]
    cmp r4, #0
    mov r0, r4, lsl #12
    beq ov000_021e6654_L40
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021e6654_L4c
ov000_021e6654_L40:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021e6654_L4c:
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
    add r3, r0, #1
    mov r2, #90
    mul r0, r4, r2
    ldrh r1, [r6, #6]
    ldr r2, =0x020d3fe0
    mov r3, r3, lsl #1
    ldrsh r4, [r2, r3]
    bl native_fn_02026144
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov000_021e6654_Lc0
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov000_021e6654_Lcc
ov000_021e6654_Lc0:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov000_021e6654_Lcc:
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
    add r1, r0, #1
    ldr r2, [r6, #0x8]
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #1
    ldrsh r1, [r0, r1]
    mov r7, r2, asr #1
    mov r0, r7
    smull r3, r2, r1, r2
    adds r3, r3, #2048
    adc r1, r2, #0
    mov r2, r3, lsr #12
    orr r2, r2, r1, lsl #20
    smull r2, r1, r4, r2
    adds r2, r2, #2048
    adc r1, r1, #0
    mov r4, r2, lsr #12
    orr r4, r4, r1, lsl #20
    bl native_fn_0203d294
    sub r5, r0, r7, asr #1
    mov r0, r7
    bl native_fn_0203d294
    sub r12, r0, r7, asr #1
    mov r1, #156
    mul r7, r8, r1
    ldr r1, =0x02235110
    mov r2, r4, asr #1
    str r5, [r1, r7]
    ldr r0, =0x02235114
    ldr r1, =0x02235118
    str r4, [r0, r7]
    mov r3, #0
    str r3, [r1, r7]
    ldr r0, =0x0223511c
    ldr r1, =0x02235120
    str r12, [r0, r7]
    rsb r2, r2, #0
    ldr r0, =0x02235124
    str r2, [r1, r7]
    str r3, [r0, r7]
    ldrh r2, [r6, #4]
    ldrb r1, [r6, #0x1]
    ldrh r0, [r6, #6]
    add r1, r2, r1
    strh r1, [r6, #4]
    ldrh r1, [r6, #4]
    cmp r1, r0
    strhib r3, [r6]
    mov r0, #1
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
