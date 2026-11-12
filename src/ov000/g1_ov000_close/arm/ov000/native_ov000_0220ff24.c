/* ov000 row 0x0220ff24: 228 bytes.
 *
 * What it does: 57 instructions; 5 call(s) to 0x021dd440, 0x0221394c, 0x021e59e4, +2 more; loops (back edge at +0x20); returns through pop {r3, r4, r5, r6, r7, pc}
 *
 * Decoded shape: chunk loop.
 *
 *   branch +0x2c -> +0x40
 *   branch +0x44 -> +0x5c
 *   branch +0x60 -> +0x7c
 *   branch +0x80 -> +0xd0
 *   branch +0x94 -> +0xa8
 *   branch +0xa4 -> +0xb8
 *   branch +0xc0 -> +0xd0
 *   test +0x28 cmp r4, #1
 *   test +0x40 cmp r4, #0
 *   test +0x54 cmp r0, #0
 *   test +0x5c cmp r4, #0
 *   test +0x74 cmp r0, #0
 *   test +0x7c cmp r4, #0
 *   test +0x8c tst r0, #1
 *   test +0xb8 cmp r0, #0
 *   test +0xd0 cmp r4, #0
 *   4 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0220ff24; the literal pool and
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

extern void native_fn_021dd440(void);
extern void native_fn_0221394c(void);
extern void native_fn_021e59e4(void);
extern void native_fn_021dc374(void);
extern void native_fn_021dbc18(void);


asm u32 native_ov000_0220ff24 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, lr}
    sub sp, sp, #16
    mov r7, r0
    mov r6, r1
    mov r5, r2
    add r2, sp, #4
    mov r0, r6
    add r1, r7, #184
    bl native_fn_021dd440
    mov r4, r0
    cmp r4, #1
    bne ov000_0220ff24_L40
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
    mov r4, #0
ov000_0220ff24_L40:
    cmp r4, #0
    bne ov000_0220ff24_L5c
    mov r0, r6
    mov r1, #0
    bl native_fn_0221394c
    cmp r0, #0
    movne r4, #2
ov000_0220ff24_L5c:
    cmp r4, #0
    bne ov000_0220ff24_L7c
    mov r1, #0
    mov r0, r6
    mov r2, r1
    bl native_fn_021e59e4
    cmp r0, #0
    movne r4, #2
ov000_0220ff24_L7c:
    cmp r4, #0
    bne ov000_0220ff24_Ld0
    ldrb r0, [r7, #0x162]
    add r2, sp, #4
    tst r0, #1
    mov r0, r6
    beq ov000_0220ff24_La8
    mov r3, r5
    add r1, r7, #528
    bl native_fn_021dc374
    b ov000_0220ff24_Lb8
ov000_0220ff24_La8:
    add r1, r7, #528
    mov r3, #1
    str r5, [sp]
    bl native_fn_021dbc18
ov000_0220ff24_Lb8:
    cmp r0, #0
    moveq r4, #3
    beq ov000_0220ff24_Ld0
    add r0, sp, #4
    ldmia r0, {r0, r1, r2}
    stmia r6, {r0, r1, r2}
ov000_0220ff24_Ld0:
    cmp r4, #0
    moveq r0, #1
    movne r0, #0
    add sp, sp, #16
    ldmia sp!, {r3, r4, r5, r6, r7, pc}
}
