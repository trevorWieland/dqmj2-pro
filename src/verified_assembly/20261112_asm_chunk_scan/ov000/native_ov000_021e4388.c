/* ov000 row 0x021e4388: 288 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x118 -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x11c -> native_data_0222ebf4 (image word 0x0222ebf4)
 *   branch +0x28 -> +0x100
 *   branch +0x3c -> +0x100
 *   branch +0x9c -> +0x100
 *   branch +0xa8 -> +0x110
 *   branch +0xc8 -> +0xec
 *   branch +0xfc -> +0x110
 *   back edge +0x10c -> +0x20
 *   test +0x24 cmp r3, #0
 *   test +0x30 cmp r3, #0
 *   test +0x38 cmpeq r3, r1
 *   test +0xa4 cmp r0, #0
 *   test +0xc4 cmp r6, #0
 *   test +0x104 cmp r4, #64
 *   4 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4388; the literal pool and
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

extern void native_fn_0205bdfc(void);
extern void native_fn_0205be4c(void);
extern void native_fn_0205bf04(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e4388 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r3, #0
    mov r6, r2
    ldr r5, =0x02234388
    str r3, [sp]
    mov r4, r3
    mov r2, r3
    mov r11, #2048
ov000_021e4388_L20:
    ldrb r3, [r5, #0x1c]
    cmp r3, #0
    beq ov000_021e4388_L100
    ldrb r3, [r5, #0x1d]
    cmp r3, #0
    ldreqsb r3, [r5, #44]
    cmpeq r3, r1
    bne ov000_021e4388_L100
    ldr r7, [r0, #0x4]
    ldr r3, [r5, #0x4]
    ldr r8, [r5, #0x18]
    sub r3, r7, r3
    smull r7, r14, r3, r3
    ldr r10, [r0]
    ldr r9, [r5]
    smull r12, r3, r8, r8
    sub r8, r10, r9
    smlal r7, r14, r8, r8
    adds r8, r12, r11
    ldr r10, [r0, #0x8]
    ldr r9, [r5, #0x8]
    adc r3, r3, r2
    sub r9, r10, r9
    smlal r7, r14, r9, r9
    mov r9, r7, lsr #12
    mov r8, r8, lsr #12
    orr r8, r8, r3, lsl #20
    orr r9, r9, lr, lsl #20
    mov r7, r8, asr #31
    subs r3, r9, r8
    rscs r3, r7, lr, asr #12
    bge ov000_021e4388_L100
    ldrsb r0, [r5, #45]
    cmp r0, #0
    bne ov000_021e4388_L110
    ldrb r0, [r5, #0x1f]
    bl native_fn_0205bdfc
    ldrsb r0, [r5, #30]
    bl native_fn_0205be4c
    ldrsb r0, [r5, #42]
    bl native_fn_0205bf04
    cmp r6, #0
    beq ov000_021e4388_Lec
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldr r0, [r5]
    str r0, [r6]
ov000_021e4388_Lec:
    ldr r1, =native_data_0222ebf4
    mov r0, #1
    str r0, [sp]
    strh r4, [r1]
    b ov000_021e4388_L110
ov000_021e4388_L100:
    add r4, r4, #1
    cmp r4, #64
    add r5, r5, #52
    blt ov000_021e4388_L20
ov000_021e4388_L110:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
