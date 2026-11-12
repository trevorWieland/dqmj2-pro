/* ov001 row 0x0221db14: 208 bytes.
 *
 * What it does: 52 instructions; 6 call(s) to 0x021db8d0, 0x021dbd24, 0x021f07dc, +3 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: block fill (52 instructions, 6 calls, 3 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0xb4
 *   branch +0x70 -> +0xb4
 *   branch +0x88 -> +0xb4
 *   back edge +0xc0 -> +0x2c
 *   test +0x1c cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x6c cmp r6, r0
 *   test +0x7c cmp r1, #0
 *   test +0x84 cmpeq r0, #0
 *   test +0xa4 cmp r6, r0
 *   test +0xb8 cmp r8, #3
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221db14; the literal pool and
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

extern void native_fn_021db8d0(void);
extern void native_fn_021dbd24(void);
extern void native_fn_021f07dc(void);
extern void native_fn_021dbe5c(void);


asm u32 native_ov001_0221db14 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    ldr r7, [r0]
    ldr r9, [r0, #0x8]
    ldrb r0, [r7, #0x356]
    mov r8, #0
    mov r5, r8
    cmp r0, #0
    moveq r0, #1
    streqb r0, [r7, #0x356]
    mov r4, #1
ov001_0221db14_L2c:
    mov r0, r9
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221db14_Lb4
    mov r0, r9
    bl native_fn_021dbd24
    str r5, [sp]
    mov r6, r0
    stmib sp, {r4, r5}
    mov r0, r7
    mov r1, r9
    mov r2, r5
    mov r3, r5
    bl native_fn_021f07dc
    ldrb r1, [r7, #0x356]
    mul r0, r1, r0
    cmp r6, r0
    bgt ov001_0221db14_Lb4
    add r0, r9, #512
    ldrsb r1, [r0, #77]
    cmp r1, #0
    ldreqsb r0, [r0, #75]
    cmpeq r0, #0
    bne ov001_0221db14_Lb4
    mov r0, r7
    bl native_fn_021dbe5c
    mov r6, r0
    mov r0, r9
    bl native_fn_021dbe5c
    sub r0, r0, #300
    cmp r6, r0
    addge sp, sp, #12
    movge r0, #1
    ldmgeia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov001_0221db14_Lb4:
    add r8, r8, #1
    cmp r8, #3
    add r9, r9, #1088
    blt ov001_0221db14_L2c
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
