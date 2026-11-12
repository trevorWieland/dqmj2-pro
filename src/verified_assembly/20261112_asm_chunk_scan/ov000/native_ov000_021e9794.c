/* ov000 row 0x021e9794: 780 bytes.
 *
 * What it does: Copies a 5-register block to an optional destination under a condition in one predicated move.
 *
 * Decoded shape: predicated block copy.
 *
 *   pool +0x2f4 -> constant 0x02236900 (image word 0x02236900)
 *   pool +0x2f8 -> constant 0x88888889 (image word 0x88888889)
 *   pool +0x2fc -> constant 0x02236938 (image word 0x02236938)
 *   pool +0x300 -> constant 0x02236944 (image word 0x02236944)
 *   pool +0x304 -> constant 0x0b60b60b (image word 0x0b60b60b)
 *   pool +0x308 -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   branch +0x14 -> +0x50
 *   branch +0x1c -> +0x34
 *   branch +0x5c -> +0x78
 *   branch +0x74 -> +0x154
 *   branch +0x7c -> +0x94
 *   branch +0x90 -> +0x154
 *   branch +0x98 -> +0xe8
 *   branch +0xc4 -> +0x154
 *   branch +0xe4 -> +0x154
 *   branch +0xec -> +0x154
 *   branch +0x160 -> +0x188
 *   branch +0x194 -> +0x2a4
 *   branch +0x2b0 -> +0x2dc
 *   test +0x10 cmp r1, #0
 *   test +0x18 cmp r0, #0
 *   test +0x58 cmp r1, #0
 *   test +0x78 cmp r1, #1
 *   test +0x94 cmp r1, #10
 *   test +0xc0 cmp r0, #45
 *   test +0xe8 cmp r1, #15
 *   test +0x140 cmp r5, #0
 *   test +0x144 cmple r6, #0
 *   test +0x15c cmp r0, #0
 *   test +0x190 cmp r0, #10
 *   test +0x2ac cmp r0, #20
 *   12 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e9794; the literal pool and
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
extern void native_fn_02041898(void);


asm u32 native_ov000_021e9794 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    ldr r1, =0x02236900
    mov r4, #0
    ldrb r1, [r1]
    cmp r1, #0
    bne ov000_021e9794_L50
    cmp r0, #0
    bne ov000_021e9794_L34
    mov r0, #147
    bl native_fn_0205e73c
    mvn r0, #0
    mov r1, #147
    bl native_fn_0205e7a8
ov000_021e9794_L34:
    ldr r0, =0x02236900
    mov r2, #0
    str r2, [r0, #0x1c]
    mov r1, #10
    strb r1, [r0]
    strb r2, [r0, #0x5]
    strb r2, [r0, #0x4]
ov000_021e9794_L50:
    ldr r0, =0x02236900
    ldrb r1, [r0, #0x5]
    cmp r1, #0
    bne ov000_021e9794_L78
    bl native_fn_02003ba0
    bl native_fn_021e8ec8
    ldr r0, =0x02236900
    mov r1, #1
    strb r1, [r0, #0x5]
    b ov000_021e9794_L154
ov000_021e9794_L78:
    cmp r1, #1
    bne ov000_021e9794_L94
    bl native_fn_021e8ec8
    ldr r0, =0x02236900
    mov r1, #10
    strb r1, [r0, #0x5]
    b ov000_021e9794_L154
ov000_021e9794_L94:
    cmp r1, #10
    bne ov000_021e9794_Le8
    mov r0, #10
    mov r1, #4
    mov r2, #1
    bl native_fn_02002c98
    mov r0, #2
    mov r1, #14
    bl native_fn_021e8ef0
    ldr r0, =0x02236900
    ldr r0, [r0, #0x1c]
    cmp r0, #45
    ble ov000_021e9794_L154
    mov r0, #1
    mov r1, #2
    mov r2, #15
    bl native_fn_02041510
    ldr r0, =0x02236900
    mov r1, #15
    strb r1, [r0, #0x5]
    b ov000_021e9794_L154
ov000_021e9794_Le8:
    cmp r1, #15
    bne ov000_021e9794_L154
    ldr r1, [r0, #0x1c]
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
    strleb r1, [r0]
ov000_021e9794_L154:
    ldr r0, =0x02236900
    ldrb r0, [r0, #0x4]
    cmp r0, #0
    bne ov000_021e9794_L188
    ldr r1, =0x02236938
    mov r0, #0
    bl native_fn_021e6a40
    ldr r1, =0x02236944
    mov r0, #0
    bl native_fn_021e6a70
    ldr r0, =0x02236900
    mov r1, #10
    strb r1, [r0, #0x4]
ov000_021e9794_L188:
    ldr r3, =0x02236900
    ldrb r0, [r3, #0x4]
    cmp r0, #10
    bne ov000_021e9794_L2a4
    ldr r2, [r3, #0x1c]
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
    ldrsh r5, [r1, r2]
    mov r2, #80
    smulbb r2, r5, r2
    umull r6, r5, r2, r12
    mla r5, r2, r14, r5
    mov r2, r2, asr #31
    mla r5, r2, r12, r5
    adds r2, r6, r0
    adc r2, r5, #2048
    mov r2, r2, lsl #4
    mov r2, r2, lsr #16
    mov r2, r2, asr #4
    mov r2, r2, lsl #2
    ldrsh r1, [r1, r2]
    rsb lr, r1, #4096
    str lr, [r3, #0x14]
    ldr r1, [r3, #0x44]
    ldr r6, [r3, #0x38]
    ldr r2, [r3, #0x48]
    ldr r5, [r3, #0x3c]
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
    ldr r12, [r3, #0x4c]
    ldr r3, [r3, #0x40]
    sub r3, r3, r12
    smull r5, r3, r14, r3
    adds r5, r5, #2048
    adc r3, r3, r0
    mov r5, r5, lsr #12
    orr r5, r5, r3, lsl #20
    add r3, r5, r12
    bl native_fn_021e6b1c
ov000_021e9794_L2a4:
    ldr r0, =0x02236900
    ldrb r0, [r0]
    cmp r0, #20
    bne ov000_021e9794_L2dc
    mov r0, #2
    bl native_fn_02041898
    mov r0, #1
    mov r2, r0
    mov r1, #0
    bl native_fn_02002c98
    ldr r0, =0x02236900
    mov r1, #0
    strb r1, [r0]
    mov r4, #1
ov000_021e9794_L2dc:
    ldr r1, =0x02236900
    mov r0, r4
    ldr r2, [r1, #0x1c]
    add r2, r2, #1
    str r2, [r1, #0x1c]
    ldmia sp!, {r4, r5, r6, pc}
}
