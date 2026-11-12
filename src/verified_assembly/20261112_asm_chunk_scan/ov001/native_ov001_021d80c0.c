/* ov001 row 0x021d80c0: 924 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x380 -> constant 0x0222fd20 (image word 0x0222fd20)
 *   pool +0x384 -> constant 0x0222fd6c (image word 0x0222fd6c)
 *   pool +0x388 -> constant 0x0222fd78 (image word 0x0222fd78)
 *   pool +0x38c -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x390 -> constant 0x0222fd50 (image word 0x0222fd50)
 *   pool +0x394 -> constant 0xb60b60b7 (image word 0xb60b60b7)
 *   pool +0x398 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x18 -> +0x64
 *   branch +0x74 -> +0x164
 *   branch +0x78 -> +0x88
 *   branch +0x7c -> +0xa0
 *   branch +0x80 -> +0xb4
 *   branch +0x84 -> +0x100
 *   branch +0x9c -> +0x164
 *   branch +0xb0 -> +0x164
 *   branch +0xdc -> +0x164
 *   branch +0xfc -> +0x164
 *   branch +0x170 -> +0x188
 *   branch +0x178 -> +0x20c
 *   branch +0x180 -> +0x218
 *   branch +0x184 -> +0x350
 *   branch +0x208 -> +0x350
 *   branch +0x214 -> +0x350
 *   test +0x14 cmp r0, #0
 *   test +0x6c cmp r1, #3
 *   test +0xd8 cmp r0, #30
 *   test +0x150 cmp r5, #0
 *   test +0x154 cmple r6, #0
 *   test +0x16c cmp r1, #0
 *   test +0x174 cmp r1, #1
 *   test +0x17c cmp r1, #2
 *   test +0x2dc cmp r1, #4096
 *   test +0x314 cmp r0, #4096
 *   test +0x364 cmp r1, #2
 *   20 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d80c0; the literal pool and
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

extern void native_fn_0205e73c(void);
extern void native_fn_0205e7a8(void);
extern void native_fn_021d7d58(void);
extern void native_fn_021d7dc4(void);
extern void native_fn_02003ba0(void);
extern void native_fn_021d8068(void);
extern void native_fn_02002c98(void);
extern void native_fn_021d808c(void);
extern void native_fn_02041510(void);
extern void native_fn_0200285c(void);
extern void native_fn_021d736c(void);


asm u32 native_ov001_021d80c0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #24
    ldr r0, =0x0222fd20
    mov r4, #0
    ldrb r0, [r0, #0x2]
    cmp r0, #0
    bne ov001_021d80c0_L64
    mov r0, #147
    bl native_fn_0205e73c
    mvn r0, #0
    mov r1, #147
    bl native_fn_0205e7a8
    ldr r2, =0x0222fd20
    mov r3, r4
    str r3, [r2, #0x8]
    mov r0, #1
    strb r0, [r2, #0x2]
    strb r3, [r2, #0x1]
    ldr r1, =0x0222fd6c
    mov r0, #46
    strb r3, [r2]
    bl native_fn_021d7d58
    ldr r1, =0x0222fd78
    mov r0, #46
    bl native_fn_021d7dc4
ov001_021d80c0_L64:
    ldr r0, =0x0222fd20
    ldrb r1, [r0, #0x1]
    cmp r1, #3
    addls pc, pc, r1, lsl #2
    b ov001_021d80c0_L164
    b ov001_021d80c0_L88
    b ov001_021d80c0_La0
    b ov001_021d80c0_Lb4
    b ov001_021d80c0_L100
ov001_021d80c0_L88:
    bl native_fn_02003ba0
    bl native_fn_021d8068
    ldr r0, =0x0222fd20
    mov r1, #1
    strb r1, [r0, #0x1]
    b ov001_021d80c0_L164
ov001_021d80c0_La0:
    bl native_fn_021d8068
    ldr r0, =0x0222fd20
    mov r1, #2
    strb r1, [r0, #0x1]
    b ov001_021d80c0_L164
ov001_021d80c0_Lb4:
    mov r0, #10
    mov r1, #4
    mov r2, #1
    bl native_fn_02002c98
    mov r0, #2
    mov r1, #14
    bl native_fn_021d808c
    ldr r0, =0x0222fd20
    ldr r0, [r0, #0x8]
    cmp r0, #30
    ble ov001_021d80c0_L164
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    ldr r0, =0x0222fd20
    mov r1, #3
    strb r1, [r0, #0x1]
    b ov001_021d80c0_L164
ov001_021d80c0_L100:
    ldr r1, [r0, #0x8]
    mvn r0, #13
    sub r1, r1, #30
    mul r2, r1, r0
    mov r0, r1, lsl #1
    ldr r1, =0x88888889
    rsb r5, r0, #0
    smull r0, r12, r1, r5
    smull r0, r3, r1, r2
    add r12, r5, r12
    mov r0, r5, lsr #31
    add r12, r0, r12, asr #3
    add r3, r2, r3
    mov r0, r2, lsr #31
    add r3, r0, r3, asr #3
    add r5, r12, #2
    add r6, r3, #14
    mov r0, r5
    mov r1, r6
    bl native_fn_021d808c
    cmp r5, #0
    cmple r6, #0
    ldrle r0, =0x0222fd20
    movle r1, #2
    strleb r1, [r0, #0x2]
ov001_021d80c0_L164:
    ldr r0, =0x0222fd20
    ldrb r1, [r0]
    cmp r1, #0
    beq ov001_021d80c0_L188
    cmp r1, #1
    beq ov001_021d80c0_L20c
    cmp r1, #2
    beq ov001_021d80c0_L218
    b ov001_021d80c0_L350
ov001_021d80c0_L188:
    ldr r0, =0x0222fd78
    ldr r5, =0x0222fd6c
    add r12, sp, #12
    ldmia r0, {r0, r1, r2}
    stmia r12, {r0, r1, r2}
    add r3, sp, #0
    ldmia r5, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r2, #0
    mov r0, r3
    mov r1, r12
    str r2, [sp, #0x4]
    str r2, [sp, #0x8]
    bl native_fn_0200285c
    ldr r2, =0x0222fd20
    ldr r1, =0x0222fd50
    str r0, [r2, #0x24]
    ldr r0, [r1, #0x20]
    add r3, sp, #0
    str r0, [r2, #0x28]
    ldmia r5, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
    mov r1, #0
    mov r0, r3
    str r1, [sp]
    str r1, [sp, #0x4]
    add r1, sp, #12
    bl native_fn_0200285c
    ldr r1, =0x0222fd20
    mov r2, #1
    str r0, [r1, #0x2c]
    strb r2, [r1]
    b ov001_021d80c0_L350
ov001_021d80c0_L20c:
    mov r1, #2
    strb r1, [r0]
    b ov001_021d80c0_L350
ov001_021d80c0_L218:
    ldr r3, [r0, #0x8]
    ldr r2, =0xb60b60b7
    mov r5, r3, lsl #12
    smull r1, r12, r2, r5
    add r12, r12, r3, lsl #12
    mov r1, r5, lsr #31
    add r12, r1, r12, asr #5
    mov r1, #90
    mul r3, r12, r1
    mov r1, r2, lsr #4
    mov r12, #182
    umull r14, r5, r3, r1
    mla r5, r3, r12, r5
    mov r3, r3, asr #31
    mla r5, r3, r1, r5
    adds r1, lr, #0
    adc r1, r5, #2048
    mov r1, r1, lsl #4
    mov r1, r1, lsr #16
    mov r3, r1, asr #4
    ldr r1, =0x020d3fe0
    mov r3, r3, lsl #2
    ldrsh r5, [r1, r3]
    mov r3, #80
    mov r2, r2, lsr #4
    smulbb r3, r5, r3
    umull r5, r14, r3, r2
    mla r14, r3, r12, r14
    mov r3, r3, asr #31
    mla r14, r3, r2, r14
    adds r2, r5, #0
    adc r2, lr, #2048
    mov r2, r2, lsl #4
    mov r2, r2, lsr #16
    mov r2, r2, asr #4
    mov r2, r2, lsl #2
    ldrsh r2, [r1, r2]
    str r2, [r0, #0x4]
    ldr r12, [r0, #0x24]
    mov r0, r2, asr #31
    smull r3, r1, r12, r2
    adds r3, r3, #2048
    adc r1, r1, #0
    mov r3, r3, lsr #12
    orr r3, r3, r1, lsl #20
    sub r1, r12, r3
    ldr r3, =0x0222fd20
    add r1, r1, #4096
    ldr lr, [r3, #0x2c]
    cmp r1, #4096
    umull r12, r3, r14, r2
    mla r3, r14, r0, r3
    mov r0, lr, asr #31
    mla r3, r0, r2, r3
    movlt r1, #4096
    adds r12, r12, #2048
    adc r0, r3, #0
    mov r3, r12, lsr #12
    orr r3, r3, r0, lsl #20
    sub r0, lr, r3
    ldr r3, =0x0222fd20
    add r2, r2, r2, lsr #31
    add r0, r0, #4096
    cmp r0, #4096
    ldr r12, [r3, #0x28]
    mov r2, r2, asr #1
    smull r3, r2, r12, r2
    movlt r0, #4096
    adds r3, r3, #2048
    adc r2, r2, #0
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    subs r2, r12, r3
    mov r3, #0
    movmi r2, r3
    rsb r3, r0, #0
    mov r0, #46
    bl native_fn_021d736c
ov001_021d80c0_L350:
    ldr r0, =0x0222fd20
    ldr r1, [r0, #0x8]
    add r1, r1, #1
    str r1, [r0, #0x8]
    ldrb r1, [r0, #0x2]
    cmp r1, #2
    moveq r1, #0
    moveq r4, #1
    streqb r1, [r0, #0x2]
    mov r0, r4
    add sp, sp, #24
    ldmia sp!, {r4, r5, r6, pc}
}
