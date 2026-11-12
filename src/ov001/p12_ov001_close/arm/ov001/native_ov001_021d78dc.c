/* ov001 row 0x021d78dc: 1060 bytes.
 *
 * What it does: 261 instructions; 32 call(s) to 0x02025a28, 0x02024e0c, 0x02025a28, +29 more; loops (back edge at +0x38); returns through pop {r3, r4, r5, r6, r7, r8, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: loop with 32 calls (261 instructions, 32 calls, 11 branches, 29 back edges, 4 literal slots).
 *
 *   pool +0x414 -> constant 0x022314b0 (image word 0x022314b0)
 *   pool +0x418 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x41c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x420 -> constant 0x0222fd50 (image word 0x0222fd50)
 *   branch +0x18 -> +0x408
 *   branch +0x24 -> +0x218
 *   branch +0x34 -> +0x4c
 *   branch +0x48 -> +0x58
 *   branch +0xb4 -> +0xcc
 *   branch +0xc8 -> +0xd8
 *   branch +0x1c8 -> +0x1e8
 *   branch +0x204 -> +0x408
 *   branch +0x214 -> +0x408
 *   branch +0x21c -> +0x408
 *   branch +0x22c -> +0x244
 *   branch +0x240 -> +0x250
 *   branch +0x2a4 -> +0x2bc
 *   branch +0x2b8 -> +0x2c8
 *   test +0x14 cmp r0, #0
 *   test +0x20 cmp r0, #0
 *   test +0x2c cmp r4, #0
 *   test +0xac cmp r0, #0
 *   test +0x1c0 cmp r0, r8
 *   test +0x1c4 cmpeq r7, r4
 *   test +0x200 cmp r1, r0
 *   test +0x218 cmp r0, #1
 *   test +0x224 cmp r4, #0
 *   test +0x29c cmp r0, #0
 *   test +0x3f8 cmp r1, r0
 *   0 block transfer(s), 10 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d78dc; the literal pool and
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
extern void native_fn_021d7874(void);
extern void native_fn_021d788c(void);
extern void native_fn_02002618(void);


asm u32 native_ov001_021d78dc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, lr}
    sub sp, sp, #12
    ldr r6, =0x022314b0
    mov r5, #0
    ldrb r0, [r6]
    cmp r0, #0
    beq ov001_021d78dc_L408
    ldrb r0, [r6, #0x1]
    cmp r0, #0
    bne ov001_021d78dc_L218
    ldrh r4, [r6, #4]
    cmp r4, #0
    mov r0, r4, lsl #12
    beq ov001_021d78dc_L4c
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021d78dc_L58
ov001_021d78dc_L4c:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021d78dc_L58:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r7, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r7, #0
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
    ble ov001_021d78dc_Lcc
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021d78dc_Ld8
ov001_021d78dc_Lcc:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021d78dc_Ld8:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r7, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r7, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r0, r0, lsl #1
    add r1, r0, #1
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #1
    ldrsh r2, [r0, r1]
    ldr r1, [r6, #0x8]
    mov r0, #4096
    smull r3, r1, r2, r1
    adds r2, r3, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    smull r2, r1, r4, r2
    adds r2, r2, #2048
    adc r1, r1, #0
    mov r7, r2, lsr #12
    orr r7, r7, r1, lsl #20
    bl native_fn_0203d294
    sub r4, r0, #2048
    mov r0, #4096
    bl native_fn_0203d294
    sub r0, r0, #2048
    add r2, r4, r4, lsl #2
    add r3, r0, r0, lsl #2
    ldr r0, [r6, #0x8]
    mov r1, r2, asr #1
    add r1, r2, r1, lsr #30
    mov r2, r3, asr #1
    add r0, r0, r0, lsr #31
    add r2, r3, r2, lsr #30
    rsb r3, r7, #0
    add r3, r3, r3, lsr #31
    mov r12, r1, asr #2
    mov r0, r0, asr #1
    mov r1, r2, asr #2
    mov r4, r3, asr #1
    smull r12, r3, r0, r12
    smull r2, r1, r0, r1
    adds r0, r12, #2048
    adc r3, r3, #0
    adds r2, r2, #2048
    mov r0, r0, lsr #12
    adc r1, r1, #0
    mov r8, r2, lsr #12
    orr r0, r0, r3, lsl #20
    orr r8, r8, r1, lsl #20
    cmp r0, r8
    cmpeq r7, r4
    beq ov001_021d78dc_L1e8
    mov r1, r7
    mov r2, #0
    bl native_fn_021d7874
    mov r0, r8
    mov r1, r4
    mov r2, #0
    bl native_fn_021d788c
ov001_021d78dc_L1e8:
    ldrh r2, [r6, #4]
    ldrb r1, [r6, #0x2]
    ldrh r0, [r6, #6]
    add r1, r2, r1
    strh r1, [r6, #4]
    ldrh r1, [r6, #4]
    cmp r1, r0
    bls ov001_021d78dc_L408
    mov r0, #0
    strb r0, [r6]
    mov r5, #1
    b ov001_021d78dc_L408
ov001_021d78dc_L218:
    cmp r0, #1
    bne ov001_021d78dc_L408
    ldrh r4, [r6, #4]
    cmp r4, #0
    mov r0, r4, lsl #12
    beq ov001_021d78dc_L244
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021d78dc_L250
ov001_021d78dc_L244:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021d78dc_L250:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r7, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r7, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r3, r0, asr #4
    mov r2, #90
    mul r0, r4, r2
    ldrh r1, [r6, #6]
    ldr r2, =0x020d3fe0
    mov r3, r3, lsl #2
    ldrsh r4, [r2, r3]
    bl native_fn_02026144
    cmp r0, #0
    mov r0, r0, lsl #12
    ble ov001_021d78dc_L2bc
    bl native_fn_02025a28
    mov r1, r0
    mov r0, #1056964608
    bl native_fn_02024e0c
    b ov001_021d78dc_L2c8
ov001_021d78dc_L2bc:
    bl native_fn_02025a28
    mov r1, #1056964608
    bl native_fn_02025ca4
ov001_021d78dc_L2c8:
    bl native_fn_020259b4
    ldr r1, =0x0b60b60b
    mov r2, #182
    umull r7, r3, r0, r1
    mla r3, r0, r2, r3
    mov r0, r0, asr #31
    mla r3, r0, r1, r3
    adds r0, r7, #0
    adc r0, r3, #2048
    mov r0, r0, lsl #4
    mov r0, r0, lsr #16
    mov r0, r0, asr #4
    mov r0, r0, lsl #1
    add r1, r0, #1
    ldr r0, =0x020d3fe0
    mov r1, r1, lsl #1
    ldrsh r2, [r0, r1]
    ldr r0, [r6, #0x8]
    ldr r1, =0x0222fd50
    smull r0, r3, r2, r0
    adds r7, r0, #2048
    adc r2, r3, #0
    mov r3, r7, lsr #12
    orr r3, r3, r2, lsl #20
    smull r2, r7, r4, r3
    adds r4, r2, #2048
    ldr r3, [r1, #0x28]
    ldr r2, [r1, #0x1c]
    add r0, sp, #0
    sub r2, r3, r2
    str r2, [sp]
    ldr r3, [r1, #0x2c]
    ldr r2, [r1, #0x20]
    adc r7, r7, #0
    sub r2, r3, r2
    str r2, [sp, #0x4]
    mov r4, r4, lsr #12
    ldr r3, [r1, #0x30]
    ldr r2, [r1, #0x24]
    mov r1, r0
    sub r2, r3, r2
    orr r4, r4, r7, lsl #20
    str r2, [sp, #0x8]
    bl native_fn_02002618
    ldr r0, [sp]
    ldr r1, [sp, #0x4]
    smull r2, r0, r4, r0
    adds r3, r2, #2048
    adc r2, r0, #0
    mov r0, r3, lsr #12
    orr r0, r0, r2, lsl #20
    smull r2, r1, r4, r1
    adds r3, r2, #2048
    adc r2, r1, #0
    mov r1, r3, lsr #12
    orr r1, r1, r2, lsl #20
    ldr r2, [sp, #0x8]
    str r0, [sp]
    smull r3, r2, r4, r2
    adds r4, r3, #2048
    adc r3, r2, #0
    mov r2, r4, lsr #12
    orr r2, r2, r3, lsl #20
    str r1, [sp, #0x4]
    str r2, [sp, #0x8]
    bl native_fn_021d7874
    mov r0, #0
    mov r1, r0
    mov r2, r0
    bl native_fn_021d788c
    ldrh r2, [r6, #4]
    ldrb r1, [r6, #0x2]
    ldrh r0, [r6, #6]
    add r1, r2, r1
    strh r1, [r6, #4]
    ldrh r1, [r6, #4]
    cmp r1, r0
    movhi r0, #0
    strhib r0, [r6]
    movhi r5, #1
ov001_021d78dc_L408:
    mov r0, r5
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, pc}
}
