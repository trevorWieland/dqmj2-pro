/* ov000 row 0x021e44a8: 272 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x108 -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x10c -> native_data_0222ebf4 (image word 0x0222ebf4)
 *   branch +0x20 -> +0xf0
 *   branch +0x34 -> +0xf0
 *   branch +0x94 -> +0xf0
 *   branch +0xb8 -> +0xdc
 *   branch +0xec -> +0x100
 *   back edge +0xfc -> +0x18
 *   test +0x1c cmp r3, #0
 *   test +0x28 cmp r3, #1
 *   test +0x30 cmpeq r3, r1
 *   test +0xb4 cmp r6, #0
 *   test +0xf4 cmp r4, #64
 *   4 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e44a8; the literal pool and
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

extern void native_fn_02028158(void);
extern void native_fn_0205be4c(void);
extern void native_fn_0205bf04(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e44a8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r4, #0
    ldr r5, =0x02234388
    str r4, [sp]
    mov r6, r3
    mov r11, r4
ov000_021e44a8_L18:
    ldrb r3, [r5, #0x1c]
    cmp r3, #0
    beq ov000_021e44a8_Lf0
    ldrb r3, [r5, #0x1d]
    cmp r3, #1
    ldreqsb r3, [r5, #44]
    cmpeq r3, r1
    bne ov000_021e44a8_Lf0
    ldr r7, [r0, #0x4]
    ldr r3, [r5, #0x4]
    ldr r8, [r5, #0x18]
    sub r3, r7, r3
    smull r7, r14, r3, r3
    smull r12, r3, r8, r8
    ldr r10, [r0]
    ldr r9, [r5]
    sub r8, r10, r9
    adds r9, r12, #2048
    smlal r7, r14, r8, r8
    adc r3, r3, r11
    mov r10, r9, lsr #12
    orr r10, r10, r3, lsl #20
    ldr r8, [r0, #0x8]
    ldr r3, [r5, #0x8]
    mov r9, r10, asr #31
    sub r3, r8, r3
    smlal r7, r14, r3, r3
    mov r3, r7, lsr #12
    orr r3, r3, lr, lsl #20
    subs r3, r3, r10
    rscs r3, r9, lr, asr #12
    bge ov000_021e44a8_Lf0
    ldr r0, [r5, #0x10]
    sub r0, r2, r0
    bl native_fn_02028158
    ldrsb r0, [r5, #30]
    bl native_fn_0205be4c
    mov r0, #0
    bl native_fn_0205bf04
    cmp r6, #0
    beq ov000_021e44a8_Ldc
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldr r0, [r5]
    str r0, [r6]
ov000_021e44a8_Ldc:
    ldr r1, =native_data_0222ebf4
    mov r0, #1
    str r0, [sp]
    strh r4, [r1]
    b ov000_021e44a8_L100
ov000_021e44a8_Lf0:
    add r4, r4, #1
    cmp r4, #64
    add r5, r5, #52
    blt ov000_021e44a8_L18
ov000_021e44a8_L100:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
