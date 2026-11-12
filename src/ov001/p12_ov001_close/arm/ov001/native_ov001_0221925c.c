/* ov001 row 0x0221925c: 312 bytes.
 *
 * What it does: 78 instructions; 8 call(s) to 0x021dbd30, 0x0207b244, 0x021db8d0, +5 more; loops (back edge at +0x20); returns through pop {r4, r5, r6, r7, r8, r9, r10, r11, pc}
 *
 * Decoded shape: block fill (78 instructions, 8 calls, 3 branches, 8 back edges, 0 literal slots).
 *
 *   branch +0x60 -> +0x114
 *   branch +0xb8 -> +0xec
 *   branch +0xe8 -> +0x10c
 *   back edge +0x120 -> +0x54
 *   test +0x44 cmp r1, #0
 *   test +0x5c cmp r0, #0
 *   test +0x90 cmp r6, r0
 *   test +0xac cmp r0, #1
 *   test +0x10c cmp r7, r0
 *   test +0x118 cmp r8, #3
 *   test +0x124 cmp r6, r7
 *   1 block transfer(s), 7 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221925c; the literal pool and
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

extern void native_fn_021dbd30(void);
extern void native_fn_0207b244(void);
extern void native_fn_021db8d0(void);
extern void native_fn_021f07dc(void);
extern void native_fn_0207afec(void);
extern void native_fn_021f0858(void);


asm u32 native_ov001_0221925c (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, r10, r11, lr}
    sub sp, sp, #12
    ldr r4, [r0]
    mov r6, #0
    ldr r10, [r0, #0x8]
    ldr r5, [r0, #0xc]
    mov r0, r4
    mov r7, r6
    bl native_fn_021dbd30
    ldr r2, [r4, #0x1e8]
    mov r1, r0
    mov r0, r5
    add r2, r2, #70
    bl native_fn_0207b244
    ldrb r1, [r4, #0x356]
    mov r9, r0
    mov r8, #0
    cmp r1, #0
    moveq r0, #1
    streqb r0, [r4, #0x356]
    mov r11, #2
ov001_0221925c_L54:
    mov r0, r10
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221925c_L114
    mov r0, #0
    stmia sp, {r0, r11}
    mov r1, #0
    mov r2, #0
    str r1, [sp, #0x8]
    mov r0, r4
    mov r1, r10
    mov r3, r2
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mul r0, r1, r0
    cmp r6, r0
    movlt r6, r0
    mov r0, r5
    bl native_fn_0207afec
    ldrh r0, [r0, #8]
    mov r0, r0, lsl #28
    mov r0, r0, lsr #28
    cmp r0, #1
    mov r0, #0
    str r0, [sp]
    bne ov001_0221925c_Lec
    mov r0, #2
    str r0, [sp, #0x4]
    mov r1, #0
    str r1, [sp, #0x8]
    mov r0, r4
    mov r1, r10
    mov r2, r5
    mov r3, #0
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mul r0, r1, r0
    b ov001_0221925c_L10c
ov001_0221925c_Lec:
    str r0, [sp, #0x4]
    mov r1, #2
    str r1, [sp, #0x8]
    mov r0, r4
    mov r1, r10
    mov r2, r9
    mov r3, r5
    bl native_fn_021f0858
ov001_0221925c_L10c:
    cmp r7, r0
    movlt r7, r0
ov001_0221925c_L114:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_0221925c_L54
    cmp r6, r7
    movgt r0, #1
    movle r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, r10, r11, pc}
}
