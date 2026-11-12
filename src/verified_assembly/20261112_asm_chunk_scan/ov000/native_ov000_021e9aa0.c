/* ov000 row 0x021e9aa0: 800 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x308 -> constant 0x02236900 (image word 0x02236900)
 *   pool +0x30c -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x310 -> constant 0x02236920 (image word 0x02236920)
 *   pool +0x314 -> constant 0x0223692c (image word 0x0223692c)
 *   pool +0x318 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x31c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x14 -> +0x48
 *   branch +0x54 -> +0x70
 *   branch +0x6c -> +0x14c
 *   branch +0x74 -> +0x8c
 *   branch +0x88 -> +0x14c
 *   branch +0x90 -> +0xe0
 *   branch +0xbc -> +0x14c
 *   branch +0xdc -> +0x14c
 *   branch +0xe4 -> +0x14c
 *   branch +0x158 -> +0x180
 *   branch +0x18c -> +0x2b8
 *   branch +0x2c4 -> +0x2f0
 *   test +0x10 cmp r0, #0
 *   test +0x50 cmp r1, #0
 *   test +0x70 cmp r1, #1
 *   test +0x8c cmp r1, #10
 *   test +0xb8 cmp r0, #45
 *   test +0xe0 cmp r1, #15
 *   test +0x138 cmp r5, #0
 *   test +0x13c cmple r6, #0
 *   test +0x154 cmp r0, #0
 *   test +0x188 cmp r0, #10
 *   test +0x2c0 cmp r0, #20
 *   13 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e9aa0; the literal pool and
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
extern void native_fn_02003ba0(void);
extern void native_fn_021e8ec8(void);
extern void native_fn_02002c98(void);
extern void native_fn_021e8ef0(void);
extern void native_fn_02041510(void);
extern void native_fn_021e6a40(void);
extern void native_fn_021e6a70(void);
extern void native_fn_021e6b1c(void);
extern void native_fn_021e71c8(void);
extern void native_fn_02041898(void);


asm u32 native_ov000_021e9aa0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    ldr r0, =0x02236900
    mov r4, #0
    ldrb r0, [r0, #0x8]
    cmp r0, #0
    bne ov000_021e9aa0_L48
    mov r0, #215
    bl native_fn_0205e73c
    mvn r0, #0
    mov r1, #215
    bl native_fn_0205e7a8
    ldr r0, =0x02236900
    mov r2, r4
    str r2, [r0, #0x18]
    mov r1, #10
    strb r1, [r0, #0x8]
    strb r2, [r0, #0x1]
    strb r2, [r0, #0x3]
ov000_021e9aa0_L48:
    ldr r0, =0x02236900
    ldrb r1, [r0, #0x1]
    cmp r1, #0
    bne ov000_021e9aa0_L70
    bl native_fn_02003ba0
    bl native_fn_021e8ec8
    ldr r0, =0x02236900
    mov r1, #1
    strb r1, [r0, #0x1]
    b ov000_021e9aa0_L14c
ov000_021e9aa0_L70:
    cmp r1, #1
    bne ov000_021e9aa0_L8c
    bl native_fn_021e8ec8
    ldr r0, =0x02236900
    mov r1, #10
    strb r1, [r0, #0x1]
    b ov000_021e9aa0_L14c
ov000_021e9aa0_L8c:
    cmp r1, #10
    bne ov000_021e9aa0_Le0
    mov r0, #10
    mov r1, #4
    mov r2, #1
    bl native_fn_02002c98
    mov r0, #2
    mov r1, #14
    bl native_fn_021e8ef0
    ldr r0, =0x02236900
    ldr r0, [r0, #0x18]
    cmp r0, #45
    ble ov000_021e9aa0_L14c
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    ldr r0, =0x02236900
    mov r1, #15
    strb r1, [r0, #0x1]
    b ov000_021e9aa0_L14c
ov000_021e9aa0_Le0:
    cmp r1, #15
    bne ov000_021e9aa0_L14c
    ldr r1, [r0, #0x18]
    mvn r0, #13
    sub r1, r1, #45
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
    ldrle r0, =0x02236900
    movle r1, #20
    strleb r1, [r0, #0x8]
ov000_021e9aa0_L14c:
    ldr r0, =0x02236900
    ldrb r0, [r0, #0x3]
    cmp r0, #0
    bne ov000_021e9aa0_L180
    ldr r1, =0x02236920
    mov r0, #0
    bl native_fn_021e6a40
    ldr r1, =0x0223692c
    mov r0, #0
    bl native_fn_021e6a70
    ldr r0, =0x02236900
    mov r1, #10
    strb r1, [r0, #0x3]
ov000_021e9aa0_L180:
    ldr r3, =0x02236900
    ldrb r0, [r3, #0x3]
    cmp r0, #10
    bne ov000_021e9aa0_L2b8
    ldr r2, [r3, #0x18]
    ldr r1, =0x88888889
    mov r5, r2, lsl #12
    smull r0, r6, r1, r5
    add r6, r6, r2, lsl #12
    mov r0, r5, lsr #31
    add r6, r0, r6, asr #5
    mov r0, #90
    mul r1, r6, r0
    ldr r12, =0x0b60b60b
    mov lr, #182
    umull r5, r2, r1, r12
    mov r0, #0
    mla r2, r1, r14, r2
    mov r1, r1, asr #31
    mla r2, r1, r12, r2
    adds r1, r5, r0
    adc r1, r2, #2048
    mov r1, r1, lsl #4
    mov r1, r1, lsr #16
    mov r2, r1, asr #4
    ldr r1, =0x020d3fe0
    mov r2, r2, lsl #2
    ldrsh r6, [r1, r2]
    mov r2, #80
    mov r5, #360
    smulbb r2, r6, r2
    umull r7, r6, r2, r12
    adds r7, r7, r0
    mla r6, r2, r14, r6
    mov r2, r2, asr #31
    mla r6, r2, r12, r6
    adc r2, r6, #2048
    mov r2, r2, lsl #4
    mov r2, r2, lsr #16
    mov r2, r2, asr #4
    mov r2, r2, lsl #2
    ldrsh r1, [r1, r2]
    rsb lr, r1, #4096
    mul r1, r14, r5
    str lr, [r3, #0x10]
    str r1, [r3, #0xc]
    ldr r1, [r3, #0x2c]
    ldr r6, [r3, #0x20]
    ldr r2, [r3, #0x30]
    ldr r5, [r3, #0x24]
    sub r12, r6, r1
    sub r6, r5, r2
    smull r12, r5, r14, r12
    adds r12, r12, #2048
    adc r5, r5, r0
    mov r12, r12, lsr #12
    orr r12, r12, r5, lsl #20
    add r1, r12, r1
    smull r12, r5, r14, r6
    adds r12, r12, #2048
    adc r5, r5, r0
    mov r12, r12, lsr #12
    orr r12, r12, r5, lsl #20
    add r2, r12, r2
    ldr r12, [r3, #0x34]
    ldr r3, [r3, #0x28]
    sub r3, r3, r12
    smull r5, r3, r14, r3
    adds r5, r5, #2048
    adc r3, r3, r0
    mov r5, r5, lsr #12
    orr r5, r5, r3, lsl #20
    add r3, r5, r12
    bl native_fn_021e6b1c
    ldr r1, =0x02236900
    mov r0, #0
    ldr r1, [r1, #0xc]
    bl native_fn_021e71c8
ov000_021e9aa0_L2b8:
    ldr r0, =0x02236900
    ldrb r0, [r0, #0x8]
    cmp r0, #20
    bne ov000_021e9aa0_L2f0
    mov r0, #2
    bl native_fn_02041898
    mov r0, #1
    mov r2, r0
    mov r1, #0
    bl native_fn_02002c98
    ldr r0, =0x02236900
    mov r1, #0
    strb r1, [r0, #0x8]
    mov r4, #1
ov000_021e9aa0_L2f0:
    ldr r1, =0x02236900
    mov r0, r4
    ldr r2, [r1, #0x18]
    add r2, r2, #1
    str r2, [r1, #0x18]
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
