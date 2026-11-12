/* ov001 row 0x0220b0f0: 300 bytes.
 *
 * What it does: 75 instructions; 8 call(s) to 0x02202360, 0x0220aba0, 0x0220b1e4, +5 more; loops (back edge at +0x2c); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (75 instructions, 8 calls, 0 branches, 7 back edges, 0 literal slots).
 *
 *   branch +0x70 -> +0xf4
 *   back edge +0xf0 -> +0x7c
 *   test +0x10 cmp r10, #2
 *   test +0x68 cmp r10, #0
 *   test +0xec cmp r4, r10
 *   1 block transfer(s), 15 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220b0f0; the literal pool and
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

extern void native_fn_02202360(void);
extern void native_fn_0220aba0(void);
extern void native_fn_0220ac58(void);
extern void native_fn_02049008(void);


asm u32 native_ov001_0220b0f0 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #24
    mov r10, r1
    str r0, [sp, #0x14]
    cmp r10, #2
    moveq r4, #4
    mov r0, #6
    mov r9, r2
    mov r8, r3
    ldr r7, [sp, #0x44]
    movne r4, #12
    bl native_fn_02202360
    ldrb r3, [sp, #0x40]
    mov r2, #32
    and r1, r4, #255
    str r3, [sp]
    str r2, [sp, #0x4]
    str r1, [sp, #0x8]
    mov r1, #1
    str r1, [sp, #0xc]
    mov r3, #0
    str r3, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, #10
    mov r2, #12
    bl native_fn_0220aba0
    cmp r10, #0
    mov r4, #0
    bls ov001_0220b0f0_Lf4
    ldrb r5, [sp, #0x40]
    mov r11, #1
ov001_0220b0f0_L7c:
    mov r0, #6
    add r6, r4, #12
    bl native_fn_02202360
    add r1, r5, r4, lsl #1
    and r1, r1, #255
    stmia sp, {r1, r7}
    mov r1, #2
    str r1, [sp, #0x8]
    mov r1, #0
    str r1, [sp, #0xc]
    str r11, [sp, #0x10]
    ldrsb r1, [r0, #16]
    mov r0, r6, lsl #24
    mov r0, r0, asr #24
    mov r2, r11
    mov r3, r8
    bl native_fn_0220aba0
    mov r1, #16
    str r1, [sp]
    mov r3, r4, lsl #1
    mov r0, r6, lsl #24
    ldrh r3, [r9, r3]
    mov r0, r0, asr #24
    mov r1, #5
    mov r2, #4
    bl native_fn_0220ac58
    add r0, r4, #1
    and r4, r0, #255
    cmp r4, r10
    blo ov001_0220b0f0_L7c
ov001_0220b0f0_Lf4:
    ldr r0, [sp, #0x14]
    mov r2, #0
    strh r10, [r0, #14]
    strh r10, [r0, #12]
    str r2, [r0]
    mov r1, r0
    str r2, [r1, #0x4]
    mov r4, #4
    mov r1, #12
    mov r3, #1
    str r4, [sp]
    bl native_fn_02049008
    add sp, sp, #24
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
