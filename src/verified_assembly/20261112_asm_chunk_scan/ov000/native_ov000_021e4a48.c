/* ov000 row 0x021e4a48: 388 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x17c -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x180 -> native_data_0222ebf4 (image word 0x0222ebf4)
 *   branch +0x24 -> +0x168
 *   branch +0x30 -> +0x168
 *   branch +0xa0 -> +0xb0
 *   branch +0xac -> +0x168
 *   branch +0xd0 -> +0x168
 *   branch +0xe4 -> +0xfc
 *   branch +0xf8 -> +0x10c
 *   branch +0x11c -> +0x144
 *   back edge +0x174 -> +0x1c
 *   test +0x20 cmp r1, #0
 *   test +0x2c cmp r1, #6
 *   test +0x54 cmp r3, #0
 *   test +0xdc cmp r0, #0
 *   test +0x118 cmp r11, #0
 *   test +0x150 cmp r0, #2
 *   test +0x158 cmpne r0, r1
 *   test +0x16c cmp r4, #64
 *   3 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e4a48; the literal pool and
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
extern void native_fn_021e031c(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e4a48 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r6, r0
    mov r0, #0
    ldr r5, =0x02234388
    str r1, [sp]
    mov r11, r2
    mov r4, r0
ov000_021e4a48_L1c:
    ldrb r1, [r5, #0x1c]
    cmp r1, #0
    beq ov000_021e4a48_L168
    ldrb r1, [r5, #0x1d]
    cmp r1, #6
    bne ov000_021e4a48_L168
    ldr r7, [r5, #0x4]
    ldr r2, [r6, #0xbc]
    ldr r1, [r6, #0x74]
    sub r2, r2, r7
    sub r1, r1, r7
    smull r9, r8, r2, r2
    smull r14, r12, r1, r1
    ldr r2, [r5]
    cmp r3, #0
    ldr r7, [r6, #0xb8]
    ldr r1, [r5, #0x8]
    sub r7, r7, r2
    smlal r9, r8, r7, r7
    ldr r10, [r6, #0xc0]
    ldr r7, [r6, #0x70]
    sub r10, r10, r1
    smlal r9, r8, r10, r10
    sub r2, r7, r2
    smlal r14, r12, r2, r2
    mov r2, r9, lsr #12
    orr r2, r2, r8, lsl #20
    ldr r7, [r6, #0x78]
    sub r1, r7, r1
    smlal r14, r12, r1, r1
    mov r7, lr, lsr #12
    mov r1, r12, asr #12
    orr r7, r7, r12, lsl #20
    beq ov000_021e4a48_Lb0
    subs r2, r7, r2
    sbcs r2, r1, r8, asr #12
    bge ov000_021e4a48_L168
ov000_021e4a48_Lb0:
    ldr r2, [r5, #0x18]
    smull r9, r8, r2, r2
    adds r9, r9, #2048
    adc r2, r8, #0
    mov r8, r9, lsr #12
    orr r8, r8, r2, lsl #20
    subs r2, r7, r8
    sbcs r2, r1, r8, asr #31
    bge ov000_021e4a48_L168
    ldrsb r0, [r5, #32]
    ldrsb r1, [r5, #30]
    cmp r0, #0
    mov r0, #6
    bne ov000_021e4a48_Lfc
    mov r2, #1
    mov r7, r5
    bl native_fn_021e47cc
    mov r2, r0
    b ov000_021e4a48_L10c
ov000_021e4a48_Lfc:
    mov r2, #0
    bl native_fn_021e47cc
    mov r7, r0
    mov r2, r5
ov000_021e4a48_L10c:
    mov r0, r6
    mov r1, r7
    bl native_fn_021e031c
    cmp r11, #0
    beq ov000_021e4a48_L144
    mov r6, r5
    ldmia r6!, {r0, r1, r2, r3}
    stmia r11!, {r0, r1, r2, r3}
    ldmia r6!, {r0, r1, r2, r3}
    stmia r11!, {r0, r1, r2, r3}
    ldmia r6!, {r0, r1, r2, r3}
    stmia r11!, {r0, r1, r2, r3}
    ldr r0, [r6]
    str r0, [r11]
ov000_021e4a48_L144:
    ldr r1, =native_data_0222ebf4
    ldr r0, [sp]
    strh r4, [r1]
    cmp r0, #2
    ldrnesb r1, [r5, #32]
    cmpne r0, r1
    moveq r0, #1
    movne r0, #0
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021e4a48_L168:
    add r4, r4, #1
    cmp r4, #64
    add r5, r5, #52
    blt ov000_021e4a48_L1c
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
