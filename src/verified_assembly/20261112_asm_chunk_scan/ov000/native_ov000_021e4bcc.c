/* ov000 row 0x021e4bcc: 312 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x130 -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x134 -> native_data_0222ebf4 (image word 0x0222ebf4)
 *   branch +0x28 -> +0x11c
 *   branch +0x44 -> +0x11c
 *   branch +0xa8 -> +0x11c
 *   branch +0xe8 -> +0x10c
 *   back edge +0x128 -> +0x20
 *   test +0x24 cmp r1, #0
 *   test +0x30 cmp r1, #4
 *   test +0x38 cmpeq r1, #0
 *   test +0x40 cmpeq r1, #0
 *   test +0xe4 cmp r6, #0
 *   test +0x120 cmp r4, #64
 *   2 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4bcc; the literal pool and
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

extern void native_fn_021e47cc(void);
extern void native_fn_021e02b0(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e4bcc (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    mov r7, r0
    mov r0, #0
    ldr r5, =0x02234388
    mov r6, r1
    mov r4, r0
    mov r9, r0
    mov r8, #2048
ov000_021e4bcc_L20:
    ldrb r1, [r5, #0x1c]
    cmp r1, #0
    beq ov000_021e4bcc_L11c
    ldrb r1, [r5, #0x1d]
    cmp r1, #4
    ldreqsb r1, [r5, #40]
    cmpeq r1, #0
    ldreqsb r1, [r5, #32]
    cmpeq r1, #0
    bne ov000_021e4bcc_L11c
    ldr r3, [r7, #0x74]
    ldr r2, [r5, #0x4]
    ldr r1, [r5, #0x18]
    sub r10, r3, r2
    smull r3, r2, r10, r10
    ldr lr, [r7, #0x70]
    ldr r10, [r5]
    mov r12, r1, lsl #1
    sub r1, lr, r10
    smlal r3, r2, r1, r1
    smull r1, r10, r12, r12
    adds r1, r1, r8
    ldr lr, [r7, #0x78]
    ldr r12, [r5, #0x8]
    adc r10, r10, r9
    sub r12, lr, r12
    smlal r3, r2, r12, r12
    mov r12, r3, lsr #12
    mov r1, r1, lsr #12
    orr r1, r1, r10, lsl #20
    orr r12, r12, r2, lsl #20
    mov r3, r1, asr #31
    subs r1, r12, r1
    rscs r1, r3, r2, asr #12
    bge ov000_021e4bcc_L11c
    ldrsb r1, [r5, #30]
    mov r0, #4
    mov r2, #2
    bl native_fn_021e47cc
    mov r8, r0
    ldrsb r1, [r5, #30]
    mov r0, #4
    mov r2, #1
    bl native_fn_021e47cc
    mov r3, r0
    mov r0, r7
    mov r2, r8
    mov r1, r5
    bl native_fn_021e02b0
    cmp r6, #0
    beq ov000_021e4bcc_L10c
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldr r0, [r5]
    str r0, [r6]
ov000_021e4bcc_L10c:
    ldr r1, =native_data_0222ebf4
    mov r0, #1
    strh r4, [r1]
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
ov000_021e4bcc_L11c:
    add r4, r4, #1
    cmp r4, #64
    add r5, r5, #52
    blt ov000_021e4bcc_L20
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
