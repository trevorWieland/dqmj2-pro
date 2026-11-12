/* ov000 row 0x021e48dc: 364 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x164 -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x168 -> native_data_0222ebf4 (image word 0x0222ebf4)
 *   branch +0x2c -> +0x150
 *   branch +0x38 -> +0x150
 *   branch +0x98 -> +0x150
 *   branch +0xac -> +0xc4
 *   branch +0xc0 -> +0xd4
 *   branch +0xe4 -> +0x10c
 *   back edge +0x15c -> +0x24
 *   test +0x28 cmp r3, #0
 *   test +0x34 cmp r3, #2
 *   test +0xa4 cmp r0, #0
 *   test +0xe0 cmp r11, #0
 *   test +0x118 cmp r0, #2
 *   test +0x120 cmpne r0, r1
 *   test +0x12c cmp r0, #0
 *   test +0x138 cmp r1, #0
 *   test +0x154 cmp r4, #64
 *   5 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e48dc; the literal pool and
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
extern void native_fn_021e02f0(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e48dc (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r6, r0
    mov r0, #0
    str r1, [sp]
    mov r11, r2
    ldr r5, =0x02234388
    mov r4, r0
    mov r2, r0
    mov r1, #2048
ov000_021e48dc_L24:
    ldrb r3, [r5, #0x1c]
    cmp r3, #0
    beq ov000_021e48dc_L150
    ldrb r3, [r5, #0x1d]
    cmp r3, #2
    bne ov000_021e48dc_L150
    ldr r7, [r6, #0x74]
    ldr r3, [r5, #0x4]
    ldr r8, [r5, #0x18]
    sub r3, r7, r3
    smull r7, r14, r3, r3
    ldr r10, [r6, #0x70]
    ldr r9, [r5]
    smull r12, r3, r8, r8
    sub r8, r10, r9
    smlal r7, r14, r8, r8
    adds r8, r12, r1
    ldr r10, [r6, #0x78]
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
    bge ov000_021e48dc_L150
    ldrsb r0, [r5, #32]
    ldrsb r1, [r5, #30]
    cmp r0, #0
    mov r0, #2
    bne ov000_021e48dc_Lc4
    mov r2, #1
    mov r7, r5
    bl native_fn_021e47cc
    mov r2, r0
    b ov000_021e48dc_Ld4
ov000_021e48dc_Lc4:
    mov r2, #0
    bl native_fn_021e47cc
    mov r7, r0
    mov r2, r5
ov000_021e48dc_Ld4:
    mov r0, r6
    mov r1, r7
    bl native_fn_021e02f0
    cmp r11, #0
    beq ov000_021e48dc_L10c
    mov r7, r5
    ldmia r7!, {r0, r1, r2, r3}
    stmia r11!, {r0, r1, r2, r3}
    ldmia r7!, {r0, r1, r2, r3}
    stmia r11!, {r0, r1, r2, r3}
    ldmia r7!, {r0, r1, r2, r3}
    stmia r11!, {r0, r1, r2, r3}
    ldr r0, [r7]
    str r0, [r11]
ov000_021e48dc_L10c:
    ldr r1, =native_data_0222ebf4
    ldr r0, [sp]
    strh r4, [r1]
    cmp r0, #2
    ldrnesb r1, [r5, #32]
    cmpne r0, r1
    moveq r0, #1
    movne r0, #0
    cmp r0, #0
    ldmeqia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
    ldrsb r1, [r5, #32]
    cmp r1, #0
    moveq r1, #5
    streqb r1, [r6, #0x1e0]
    movne r1, #6
    strneb r1, [r6, #0x1e0]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
ov000_021e48dc_L150:
    add r4, r4, #1
    cmp r4, #64
    add r5, r5, #52
    blt ov000_021e48dc_L24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
