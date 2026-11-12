/* ov000 row 0x02213b68: 372 bytes.
 *
 * What it does: 91 instructions; 5 call(s) to 0x02213a4c, 0x0202818c, 0x02028158, +2 more; loops (back edge at +0x4c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: chunk loop.
 *
 *   pool +0x16c -> constant 0x02243e3c (image word 0x02243e3c)
 *   pool +0x170 -> native_data_0222f850 (image word 0x0222f850)
 *   branch +0x3c -> +0x150
 *   branch +0x54 -> +0x150
 *   branch +0xac -> +0x150
 *   branch +0xd8 -> +0x150
 *   branch +0xe8 -> +0xf8
 *   branch +0x100 -> +0x150
 *   branch +0x114 -> +0x128
 *   branch +0x130 -> +0x144
 *   branch +0x14c -> +0x160
 *   back edge +0x15c -> +0x34
 *   test +0x38 cmp r0, #0
 *   test +0x50 cmp r0, #0
 *   test +0xd4 cmp r0, r1, lsl #1
 *   test +0xe0 cmp r0, #5
 *   test +0xfc cmp r0, #573440
 *   test +0x110 cmp r0, #0
 *   test +0x12c cmp r0, #0
 *   test +0x154 cmp r7, #16
 *   6 block transfer(s), 5 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02213b68; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: byte identity fixes the instruction stream, not the field, block and callee semantics behind the addresses and strides it touches.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02213a4c(void);
extern void native_fn_0202818c(void);
extern void native_fn_02028158(void);
extern u8 native_data_0222f850[];


asm u32 native_ov000_02213b68 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #32
    mov r4, #0
    ldr r8, =0x02243e3c
    str r4, [sp, #0x8]
    mov r10, r0
    mov r9, r1
    str r2, [sp]
    str r3, [sp, #0x4]
    mov r7, r4
    add r5, sp, #20
    add r6, sp, #16
    add r11, sp, #12
ov000_02213b68_L34:
    ldrb r0, [r8, #0x105]
    cmp r0, #0
    beq ov000_02213b68_L150
    ldrb r0, [r8, #0x106]
    mov r1, r6
    mov r2, r11
    bl native_fn_02213a4c
    cmp r0, #0
    beq ov000_02213b68_L150
    add r0, r8, #112
    ldmia r0, {r0, r1, r2}
    stmia r5, {r0, r1, r2}
    ldr r2, [r10, #0x4]
    ldr r1, [sp, #0x18]
    ldr r0, [sp, #0xc]
    sub r1, r2, r1
    smull r3, r2, r1, r1
    ldr r4, [r10]
    ldr r1, [sp, #0x14]
    ldr r12, [r10, #0x8]
    sub r1, r4, r1
    smlal r3, r2, r1, r1
    ldr r4, [sp, #0x1c]
    mov r1, r0, asr #31
    sub r4, r12, r4
    smlal r3, r2, r4, r4
    mov r3, r3, lsr #12
    orr r3, r3, r2, lsl #20
    subs r0, r3, r0
    rscs r0, r1, r2, asr #12
    bge ov000_02213b68_L150
    mov r0, r5
    mov r1, r10
    bl native_fn_0202818c
    ldr r1, [r8, #0x8c]
    mov r4, r0
    sub r0, r4, r1
    bl native_fn_02028158
    ldr r1, [sp, #0x10]
    add r0, r0, r1
    cmp r0, r1, lsl #1
    bhi ov000_02213b68_L150
    ldrb r0, [r8, #0x106]
    cmp r0, #5
    moveq r0, #0
    beq ov000_02213b68_Lf8
    add r0, r4, #737280
    sub r0, r0, r9
    bl native_fn_02028158
ov000_02213b68_Lf8:
    add r0, r0, #286720
    cmp r0, #573440
    bhi ov000_02213b68_L150
    ldr r1, =native_data_0222f850
    ldr r0, [sp]
    strb r7, [r1]
    cmp r0, #0
    beq ov000_02213b68_L128
    ldr r3, [sp]
    add r0, r8, #112
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_02213b68_L128:
    ldr r0, [sp, #0x4]
    cmp r0, #0
    beq ov000_02213b68_L144
    ldr r3, [sp, #0x4]
    add r0, r8, #136
    ldmia r0, {r0, r1, r2}
    stmia r3, {r0, r1, r2}
ov000_02213b68_L144:
    mov r0, #1
    str r0, [sp, #0x8]
    b ov000_02213b68_L160
ov000_02213b68_L150:
    add r7, r7, #1
    cmp r7, #16
    add r8, r8, #268
    blt ov000_02213b68_L34
ov000_02213b68_L160:
    ldr r0, [sp, #0x8]
    add sp, sp, #32
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
