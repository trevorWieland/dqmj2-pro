/* ov000 row 0x021e8f28: 820 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x320 -> constant 0x022368cc (image word 0x022368cc)
 *   pool +0x324 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x328 -> constant 0xb60b60b7 (image word 0xb60b60b7)
 *   pool +0x32c -> constant 0x000006db (image word 0x000006db)
 *   pool +0x330 -> constant 0x00001666 (image word 0x00001666)
 *   branch +0x18 -> +0x48
 *   branch +0x54 -> +0x78
 *   branch +0x74 -> +0x154
 *   branch +0x7c -> +0xa4
 *   branch +0xa0 -> +0x154
 *   branch +0xa8 -> +0xe8
 *   branch +0xc4 -> +0x154
 *   branch +0xe4 -> +0x154
 *   branch +0xec -> +0x154
 *   branch +0x160 -> +0x19c
 *   branch +0x1a8 -> +0x28c
 *   branch +0x298 -> +0x2e0
 *   branch +0x2f4 -> +0x308
 *   branch +0x300 -> +0x308
 *   test +0x14 cmp r0, #0
 *   test +0x50 cmp r1, #0
 *   test +0x78 cmp r1, #1
 *   test +0xa4 cmp r1, #10
 *   test +0xc0 cmp r0, #60
 *   test +0xe8 cmp r1, #15
 *   test +0x140 cmp r5, #0
 *   test +0x144 cmple r6, #0
 *   test +0x15c cmp r0, #0
 *   test +0x1a4 cmp r0, #10
 *   test +0x294 cmp r0, #20
 *   test +0x2e4 cmp r7, #0
 *   test +0x2fc cmp r0, #20
 *   test +0x308 cmp r4, #0
 *   23 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e8f28; the literal pool and
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

extern void native_fn_021e7b9c(void);
extern void native_fn_021d8a44(void);
extern void native_fn_020418b0(void);
extern void native_fn_02003ba0(void);
extern void native_fn_021e8ec8(void);
extern void native_fn_02002c98(void);
extern void native_fn_021e8ef0(void);
extern void native_fn_02041510(void);
extern void native_fn_0202841c(void);
extern void native_fn_021d8a28(void);
extern void native_fn_02040434(void);


asm u32 native_ov000_021e8f28 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, lr}
    ldr r1, =0x022368cc
    mov r7, r0
    ldrb r0, [r1, #0x1]
    mov r4, #0
    cmp r0, #0
    bne ov000_021e8f28_L48
    mov r0, #215
    bl native_fn_021e7b9c
    bl native_fn_021d8a44
    mov r2, r4
    strb r2, [r0, #0xa8]
    ldr r1, =0x022368cc
    mov r0, #10
    str r2, [r1, #0x30]
    strb r0, [r1, #0x1]
    strb r2, [r1, #0x2]
    strb r2, [r1, #0x5]
ov000_021e8f28_L48:
    ldr r0, =0x022368cc
    ldrb r1, [r0, #0x2]
    cmp r1, #0
    bne ov000_021e8f28_L78
    mov r0, #2
    bl native_fn_020418b0
    bl native_fn_02003ba0
    bl native_fn_021e8ec8
    ldr r0, =0x022368cc
    mov r1, #1
    strb r1, [r0, #0x2]
    b ov000_021e8f28_L154
ov000_021e8f28_L78:
    cmp r1, #1
    bne ov000_021e8f28_La4
    mov r0, #10
    mov r1, #4
    mov r2, #1
    bl native_fn_02002c98
    bl native_fn_021e8ec8
    ldr r0, =0x022368cc
    mov r1, #10
    strb r1, [r0, #0x2]
    b ov000_021e8f28_L154
ov000_021e8f28_La4:
    cmp r1, #10
    bne ov000_021e8f28_Le8
    mov r0, #2
    mov r1, #14
    bl native_fn_021e8ef0
    ldr r0, =0x022368cc
    ldr r0, [r0, #0x30]
    cmp r0, #60
    ble ov000_021e8f28_L154
    mov r0, #1
    mov r1, #2
    mov r2, #30
    bl native_fn_02041510
    ldr r0, =0x022368cc
    mov r1, #15
    strb r1, [r0, #0x2]
    b ov000_021e8f28_L154
ov000_021e8f28_Le8:
    cmp r1, #15
    bne ov000_021e8f28_L154
    ldr r1, [r0, #0x30]
    mvn r0, #13
    sub r1, r1, #60
    mul r2, r1, r0
    mov r0, r1, lsl #1
    ldr r1, =0x88888889
    rsb r5, r0, #0
    smull r0, r6, r1, r5
    smull r0, r3, r1, r2
    add r6, r5, r6
    mov r0, r5, lsr #31
    add r6, r0, r6, asr #4
    add r3, r2, r3
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #4
    add r5, r6, #2
    add r6, r3, #14
    mov r0, r5
    mov r1, r6
    bl native_fn_021e8ef0
    cmp r5, #0
    cmple r6, #0
    ldrle r0, =0x022368cc
    movle r1, #20
    strleb r1, [r0, #0x1]
ov000_021e8f28_L154:
    ldr r0, =0x022368cc
    ldrb r0, [r0, #0x5]
    cmp r0, #0
    bne ov000_021e8f28_L19c
    bl native_fn_021d8a44
    ldr r1, [r0, #0x9c]
    ldr r0, =0x022368cc
    str r1, [r0, #0x2c]
    bl native_fn_021d8a44
    ldr r1, [r0, #0xa0]
    ldr r0, =0x022368cc
    str r1, [r0, #0x28]
    bl native_fn_021d8a44
    ldr r2, [r0, #0xa4]
    ldr r0, =0x022368cc
    mov r1, #10
    str r2, [r0, #0x1c]
    strb r1, [r0, #0x5]
ov000_021e8f28_L19c:
    ldr r3, =0x022368cc
    ldrb r0, [r3, #0x5]
    cmp r0, #10
    bne ov000_021e8f28_L28c
    ldr r5, [r3, #0x30]
    ldr r2, =0xb60b60b7
    mov r6, r5, lsl #12
    smull r0, r1, r2, r6
    add r1, r1, r5, lsl #12
    mov r0, r6, lsr #31
    add r1, r0, r1, asr #6
    str r1, [r3, #0x20]
    ldr r5, [r3, #0x2c]
    mov r0, r1, asr #31
    smull r3, r2, r5, r1
    adds r3, r3, #2048
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    subs r5, r5, r3
    ldr r3, =0x022368cc
    mov r2, #0
    ldr lr, [r3, #0x28]
    movmi r5, r2
    umull r12, r6, r14, r1
    mla r6, r14, r0, r6
    mov r3, lr, asr #31
    mla r6, r3, r1, r6
    adds r12, r12, #2048
    adc r3, r6, #0
    mov r6, r12, lsr #12
    orr r6, r6, r3, lsl #20
    mov r2, #0
    subs r6, lr, r6
    movmi r6, r2
    umull r3, r2, r1, r1
    mla r2, r1, r0, r2
    mla r2, r0, r1, r2
    adds r3, r3, #2048
    adc r0, r2, #0
    mov r2, r3, lsr #12
    orr r2, r2, r0, lsl #20
    smull r0, r1, r2, r2
    adds r2, r0, #2048
    mov r0, #2048
    adc r1, r1, #0
    mov r2, r2, lsr #12
    orr r2, r2, r1, lsl #20
    sub r0, r0, #968
    ldr r1, =0x022368cc
    mul r8, r2, r0
    str r2, [r1, #0x20]
    bl native_fn_021d8a44
    str r5, [r0, #0x9c]
    bl native_fn_021d8a44
    str r6, [r0, #0xa0]
    bl native_fn_021d8a44
    mov r1, r8
    bl native_fn_0202841c
    bl native_fn_021d8a28
ov000_021e8f28_L28c:
    ldr r0, =0x022368cc
    ldrb r0, [r0, #0x1]
    cmp r0, #20
    bne ov000_021e8f28_L2e0
    mov r0, #1
    mov r2, r0
    mov r1, #0
    bl native_fn_02002c98
    bl native_fn_021d8a44
    mov r1, #1
    strb r1, [r0, #0xa8]
    bl native_fn_021d8a44
    mov r1, #24576
    str r1, [r0, #0x9c]
    bl native_fn_021d8a44
    ldr r1, =0x000006db
    str r1, [r0, #0xa0]
    bl native_fn_021d8a44
    ldr r1, =0x00001666
    mov r4, #1
    str r1, [r0, #0xa4]
ov000_021e8f28_L2e0:
    ldr r0, =0x022368cc
    cmp r7, #0
    ldr r1, [r0, #0x30]
    add r1, r1, #1
    str r1, [r0, #0x30]
    beq ov000_021e8f28_L308
    ldrb r0, [r0, #0x1]
    cmp r0, #20
    bhs ov000_021e8f28_L308
    bl native_fn_02040434
ov000_021e8f28_L308:
    cmp r4, #0
    ldrne r0, =0x022368cc
    movne r1, #0
    strneb r1, [r0, #0x1]
    mov r0, r4
    ldmia sp!, {r4, r5, r6, r7, r8, pc}
}
