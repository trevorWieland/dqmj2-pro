/* ov000 row 0x021e925c: 1076 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x41c -> constant 0x022368cc (image word 0x022368cc)
 *   pool +0x420 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x424 -> constant 0xb60b60b7 (image word 0xb60b60b7)
 *   pool +0x428 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   pool +0x42c -> constant 0x000006db (image word 0x000006db)
 *   pool +0x430 -> constant 0x00001666 (image word 0x00001666)
 *   branch +0x18 -> +0x50
 *   branch +0x5c -> +0x80
 *   branch +0x7c -> +0x16c
 *   branch +0x84 -> +0xac
 *   branch +0xa8 -> +0x16c
 *   branch +0xb0 -> +0x100
 *   branch +0xcc -> +0x16c
 *   branch +0xfc -> +0x16c
 *   branch +0x104 -> +0x16c
 *   branch +0x178 -> +0x208
 *   branch +0x1ec -> +0x1f8
 *   branch +0x204 -> +0x398
 *   branch +0x20c -> +0x398
 *   branch +0x310 -> +0x320
 *   branch +0x31c -> +0x350
 *   branch +0x34c -> +0x37c
 *   branch +0x3a4 -> +0x3e0
 *   branch +0x3f8 -> +0x400
 *   test +0x14 cmp r0, #0
 *   test +0x58 cmp r1, #0
 *   test +0x80 cmp r1, #5
 *   test +0xac cmp r1, #10
 *   test +0xc8 cmp r0, #30
 *   test +0x100 cmp r1, #15
 *   test +0x158 cmp r5, #0
 *   test +0x15c cmple r6, #0
 *   test +0x174 cmp r1, #0
 *   test +0x1e8 cmp r0, #0
 *   test +0x208 cmp r1, #10
 *   test +0x2d0 cmp r5, #4096
 *   test +0x30c cmp r0, #0
 *   test +0x318 cmp r0, #3
 *   test +0x344 cmp r7, #4096
 *   test +0x374 cmp r7, r0
 *   test +0x3a0 cmp r0, #20
 *   test +0x3f4 cmp r0, #20
 *   test +0x400 cmp r4, #0
 *   26 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e925c; the literal pool and
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
extern void native_fn_0205e814(void);
extern void native_fn_0200285c(void);
extern void native_fn_021d8a18(void);
extern void native_fn_021d8a08(void);
extern void native_fn_021d8a28(void);
extern void native_fn_021e7a4c(void);
extern void native_fn_02040434(void);


asm u32 native_ov000_021e925c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #24
    ldr r0, =0x022368cc
    mov r4, #0
    ldrb r0, [r0, #0x4]
    cmp r0, #0
    bne ov000_021e925c_L50
    mov r0, #147
    bl native_fn_021e7b9c
    ldr r1, =0x022368cc
    str r0, [r1, #0x24]
    bl native_fn_021d8a44
    mov r2, r4
    strb r2, [r0, #0xa8]
    ldr r1, =0x022368cc
    mov r0, #10
    str r2, [r1, #0x14]
    strb r0, [r1, #0x4]
    strb r2, [r1]
    strb r2, [r1, #0x3]
ov000_021e925c_L50:
    ldr r0, =0x022368cc
    ldrb r1, [r0]
    cmp r1, #0
    bne ov000_021e925c_L80
    mov r0, #2
    bl native_fn_020418b0
    bl native_fn_02003ba0
    bl native_fn_021e8ec8
    ldr r0, =0x022368cc
    mov r1, #5
    strb r1, [r0]
    b ov000_021e925c_L16c
ov000_021e925c_L80:
    cmp r1, #5
    bne ov000_021e925c_Lac
    mov r0, #10
    mov r1, #4
    mov r2, #1
    bl native_fn_02002c98
    bl native_fn_021e8ec8
    ldr r0, =0x022368cc
    mov r1, #10
    strb r1, [r0]
    b ov000_021e925c_L16c
ov000_021e925c_Lac:
    cmp r1, #10
    bne ov000_021e925c_L100
    mov r0, #2
    mov r1, #14
    bl native_fn_021e8ef0
    ldr r0, =0x022368cc
    ldr r0, [r0, #0x14]
    cmp r0, #30
    ble ov000_021e925c_L16c
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    mov r0, #0
    mov r1, r0
    mov r2, #19
    bl native_fn_0205e814
    ldr r0, =0x022368cc
    mov r1, #15
    strb r1, [r0]
    b ov000_021e925c_L16c
ov000_021e925c_L100:
    cmp r1, #15
    bne ov000_021e925c_L16c
    ldr r1, [r0, #0x14]
    mvn r0, #13
    sub r1, r1, #30
    mul r2, r1, r0
    mov r0, r1, lsl #1
    ldr r1, =0x88888889
    rsb r5, r0, #0
    smull r0, r6, r1, r5
    smull r0, r3, r1, r2
    add r6, r5, r6
    mov r0, r5, lsr #31
    add r6, r0, r6, asr #3
    add r3, r2, r3
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #3
    add r5, r6, #2
    add r6, r3, #14
    mov r0, r5
    mov r1, r6
    bl native_fn_021e8ef0
    cmp r5, #0
    cmple r6, #0
    ldrle r0, =0x022368cc
    movle r1, #20
    strleb r1, [r0, #0x4]
ov000_021e925c_L16c:
    ldr r0, =0x022368cc
    ldrb r1, [r0, #0x3]
    cmp r1, #0
    bne ov000_021e925c_L208
    bl native_fn_021d8a44
    add r0, r0, #28
    add r3, sp, #0
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    bl native_fn_021d8a44
    add r0, r0, #40
    add r3, sp, #12
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r0, #0
    mov r1, r3
    str r0, [sp, #0x4]
    str r0, [sp, #0x10]
    add r0, sp, #0
    bl native_fn_0200285c
    ldr r1, =0x022368cc
    str r0, [r1, #0x10]
    bl native_fn_021d8a44
    ldr r1, [r0, #0xa0]
    ldr r0, =0x022368cc
    str r1, [r0, #0xc]
    bl native_fn_021d8a44
    ldr r1, [r0, #0xa4]
    ldr r0, =0x022368cc
    str r1, [r0, #0x8]
    bl native_fn_021d8a18
    cmp r0, #0
    bne ov000_021e925c_L1f8
    mov r0, #3
    bl native_fn_021d8a08
ov000_021e925c_L1f8:
    ldr r0, =0x022368cc
    mov r1, #10
    strb r1, [r0, #0x3]
    b ov000_021e925c_L398
ov000_021e925c_L208:
    cmp r1, #10
    bne ov000_021e925c_L398
    ldr r3, [r0, #0x14]
    ldr r2, =0xb60b60b7
    mov r5, r3, lsl #12
    smull r1, r6, r2, r5
    mov r1, r5, lsr #31
    add r6, r6, r3, lsl #12
    add r6, r1, r6, asr #5
    mov r1, #90
    mul r3, r6, r1
    mov r1, r2, lsr #4
    mov r5, #182
    umull r7, r6, r3, r1
    mla r6, r3, r5, r6
    mov r3, r3, asr #31
    mla r6, r3, r1, r6
    adds r1, r7, #0
    adc r1, r6, #2048
    mov r1, r1, lsl #4
    mov r1, r1, lsr #16
    mov r3, r1, asr #4
    ldr r1, =0x020d3fe0
    mov r3, r3, lsl #2
    ldrsh r6, [r1, r3]
    mov r3, #80
    mov r2, r2, lsr #4
    smulbb r3, r6, r3
    umull r7, r6, r3, r2
    mla r6, r3, r5, r6
    mov r3, r3, asr #31
    mla r6, r3, r2, r6
    adds r2, r7, #0
    adc r2, r6, #2048
    mov r2, r2, lsl #4
    mov r2, r2, lsr #16
    mov r2, r2, asr #4
    mov r2, r2, lsl #2
    ldrsh r1, [r1, r2]
    str r1, [r0, #0x18]
    ldr r5, [r0, #0x10]
    mov r0, r1, asr #31
    smull r3, r2, r5, r1
    adds r3, r3, #2048
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    sub r2, r5, r3
    add r5, r2, #4096
    ldr r3, =0x022368cc
    cmp r5, #4096
    ldr r7, [r3, #0xc]
    movlt r5, #4096
    umull r6, r3, r7, r1
    mla r3, r7, r0, r3
    mov r0, r7, asr #31
    mla r3, r0, r1, r3
    adds r6, r6, #2048
    adc r0, r3, #0
    mov r1, r6, lsr #12
    orr r1, r1, r0, lsl #20
    mov r2, #0
    subs r6, r7, r1
    movmi r6, r2
    bl native_fn_021d8a18
    cmp r0, #0
    beq ov000_021e925c_L320
    bl native_fn_021d8a18
    cmp r0, #3
    bne ov000_021e925c_L350
ov000_021e925c_L320:
    ldr r0, =0x022368cc
    ldr r2, [r0, #0x8]
    ldr r0, [r0, #0x18]
    smull r1, r0, r2, r0
    adds r1, r1, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    sub r7, r2, r1
    cmp r7, #4096
    movlt r7, #4096
    b ov000_021e925c_L37c
ov000_021e925c_L350:
    ldr r0, =0x022368cc
    ldr r7, [r0, #0x8]
    ldr r0, [r0, #0x18]
    smull r1, r0, r7, r0
    adds r1, r1, #2048
    adc r0, r0, #0
    mov r1, r1, lsr #12
    orr r1, r1, r0, lsl #20
    sub r0, r7, r1
    cmp r7, r0
    movle r7, r0
ov000_021e925c_L37c:
    bl native_fn_021d8a44
    str r5, [r0, #0x9c]
    bl native_fn_021d8a44
    str r6, [r0, #0xa0]
    bl native_fn_021d8a44
    str r7, [r0, #0xa4]
    bl native_fn_021d8a28
ov000_021e925c_L398:
    ldr r0, =0x022368cc
    ldrb r0, [r0, #0x4]
    cmp r0, #20
    bne ov000_021e925c_L3e0
    bl native_fn_021e7a4c
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
ov000_021e925c_L3e0:
    ldr r0, =0x022368cc
    ldr r1, [r0, #0x14]
    add r1, r1, #1
    str r1, [r0, #0x14]
    ldrb r0, [r0, #0x4]
    cmp r0, #20
    bhs ov000_021e925c_L400
    bl native_fn_02040434
ov000_021e925c_L400:
    cmp r4, #0
    ldrne r0, =0x022368cc
    movne r1, #0
    strneb r1, [r0, #0x4]
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
