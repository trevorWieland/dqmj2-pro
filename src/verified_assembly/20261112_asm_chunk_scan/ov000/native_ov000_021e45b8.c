/* ov000 row 0x021e45b8: 308 bytes.
 *
 * What it does: Moves 4-register chunks between two pointers with writeback block moves (3 loads, 3 stores).
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x128 -> constant 0x02234388 (image word 0x02234388)
 *   pool +0x12c -> constant 0x0223255c (image word 0x0223255c)
 *   pool +0x130 -> native_data_0222ebf4 (image word 0x0222ebf4)
 *   branch +0x2c -> +0x110
 *   branch +0x38 -> +0x110
 *   branch +0x98 -> +0x110
 *   branch +0xb4 -> +0x110
 *   branch +0xd8 -> +0xfc
 *   branch +0x10c -> +0x120
 *   back edge +0x11c -> +0x24
 *   test +0x28 cmp r0, #0
 *   test +0x34 cmp r0, #5
 *   test +0xb0 cmp r0, #245760
 *   test +0xd4 cmp r6, #0
 *   test +0x114 cmp r4, #64
 *   6 store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021e45b8; the literal pool and
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
extern void native_fn_020c40f4(void);
extern u8 native_data_0222ebf4[];


asm u32 native_ov000_021e45b8 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    mov r3, #0
    ldr r5, =0x02234388
    str r3, [sp]
    mov r7, r0
    mov r6, r2
    mov r4, r3
    mov r8, r3
    mov r11, #2048
ov000_021e45b8_L24:
    ldrb r0, [r5, #0x1c]
    cmp r0, #0
    beq ov000_021e45b8_L110
    ldrb r0, [r5, #0x1d]
    cmp r0, #5
    bne ov000_021e45b8_L110
    ldr r2, [r7, #0x4]
    ldr r0, [r5, #0x4]
    ldr lr, [r5, #0x18]
    sub r0, r2, r0
    smull r12, r3, r0, r0
    ldr r10, [r7]
    ldr r9, [r5]
    smull r2, r0, r14, r14
    sub r9, r10, r9
    smlal r12, r3, r9, r9
    adds r2, r2, r11
    ldr r10, [r7, #0x8]
    ldr r9, [r5, #0x8]
    adc r0, r0, r8
    sub r9, r10, r9
    smlal r12, r3, r9, r9
    mov r10, r12, lsr #12
    mov r9, r2, lsr #12
    orr r9, r9, r0, lsl #20
    orr r10, r10, r3, lsl #20
    mov r2, r9, asr #31
    subs r0, r10, r9
    rscs r0, r2, r3, asr #12
    bge ov000_021e45b8_L110
    ldr r0, [r5, #0x10]
    sub r0, r1, r0
    bl native_fn_02028158
    movs r1, r0
    rsbmi r0, r1, #0
    cmp r0, #245760
    bge ov000_021e45b8_L110
    ldrb r0, [r5, #0x21]
    bl native_fn_020c40f4
    ldrb r1, [r5, #0x22]
    ldr r0, =0x0223255c
    mov r2, #0
    strb r2, [r0]
    strb r1, [r0, #0x1]
    cmp r6, #0
    beq ov000_021e45b8_Lfc
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldmia r5!, {r0, r1, r2, r3}
    stmia r6!, {r0, r1, r2, r3}
    ldr r0, [r5]
    str r0, [r6]
ov000_021e45b8_Lfc:
    ldr r1, =native_data_0222ebf4
    mov r0, #1
    str r0, [sp]
    strh r4, [r1]
    b ov000_021e45b8_L120
ov000_021e45b8_L110:
    add r4, r4, #1
    cmp r4, #64
    add r5, r5, #52
    blt ov000_021e45b8_L24
ov000_021e45b8_L120:
    ldr r0, [sp]
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
