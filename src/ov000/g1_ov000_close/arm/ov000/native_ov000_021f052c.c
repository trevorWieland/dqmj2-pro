/* ov000 row 0x021f052c: 236 bytes.
 *
 * What it does: 58 instructions; 7 call(s) to 0x02049ad0, 0x0206db90, 0x021efca0, +4 more; loops (back edge at +0x1c); returns through pop {r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0xe8 -> constant 0x02236c98 (image word 0x02236c98)
 *   branch +0x2c -> +0xc8
 *   branch +0x40 -> +0xc8
 *   branch +0x54 -> +0xc8
 *   branch +0x60 -> +0x74
 *   branch +0x70 -> +0xc8
 *   branch +0x80 -> +0xac
 *   branch +0xa8 -> +0xc8
 *   back edge +0xd8 -> +0x18
 *   test +0x28 cmp r9, #0
 *   test +0x3c cmp r0, #2
 *   test +0x50 cmp r10, #127
 *   test +0x5c cmp r0, #6
 *   test +0x6c cmp r0, #0
 *   test +0x7c cmp r0, #127
 *   test +0xd4 cmp r7, #36
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f052c; the literal pool and
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

extern void native_fn_02049ad0(void);
extern void native_fn_0206db90(void);
extern void native_fn_021efca0(void);
extern void native_fn_02045dc4(void);
extern void native_fn_0206006c(void);
extern void native_fn_020851d4(void);


asm u32 native_ov000_021f052c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #8
    ldr r5, =0x02236c98
    mov r7, #0
    mov r6, #1
    mov r4, #12
ov000_021f052c_L18:
    mov r0, r7
    bl native_fn_02049ad0
    mov r8, r0
    ldr r9, [r8]
    cmp r9, #0
    beq ov000_021f052c_Lc8
    ldr r0, [r9, #0x4]
    ldr r0, [r0, #0x18]
    and r0, r0, #2
    cmp r0, #2
    bne ov000_021f052c_Lc8
    ldrsb r0, [r8, #5]
    bl native_fn_0206db90
    mov r10, r0
    cmp r10, #127
    beq ov000_021f052c_Lc8
    ldrsb r0, [r8, #4]
    cmp r0, #6
    bne ov000_021f052c_L74
    mov r0, r7
    bl native_fn_021efca0
    cmp r0, #0
    beq ov000_021f052c_Lc8
ov000_021f052c_L74:
    ldrsb r0, [r8, #5]
    ldr r3, [r9, #0x4]
    cmp r0, #127
    bne ov000_021f052c_Lac
    ldrb r2, [r3, #0x5e]
    mov r0, r6
    mov r1, r6
    str r2, [sp]
    ldrb r2, [r3, #0x5f]
    str r2, [sp, #0x4]
    ldrb r2, [r3, #0x5c]
    ldrb r3, [r3, #0x5d]
    bl native_fn_02045dc4
    b ov000_021f052c_Lc8
ov000_021f052c_Lac:
    ldrsb r1, [r3, #95]
    mla r0, r10, r4, r5
    str r1, [sp]
    ldrsb r1, [r3, #92]
    ldrsb r2, [r3, #93]
    ldrsb r3, [r3, #94]
    bl native_fn_0206006c
ov000_021f052c_Lc8:
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #36
    blt ov000_021f052c_L18
    bl native_fn_020851d4
    add sp, sp, #8
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, pc}
}
