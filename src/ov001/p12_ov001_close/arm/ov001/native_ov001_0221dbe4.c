/* ov001 row 0x0221dbe4: 212 bytes.
 *
 * What it does: 53 instructions; 6 call(s) to 0x021db8d0, 0x021dbd24, 0x021f07dc, +3 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: block fill (53 instructions, 6 calls, 3 branches, 6 back edges, 0 literal slots).
 *
 *   branch +0x3c -> +0xb0
 *   branch +0x74 -> +0xb0
 *   branch +0x8c -> +0xb0
 *   back edge +0xbc -> +0x30
 *   test +0x1c cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x70 cmp r8, r0
 *   test +0x80 cmp r1, #0
 *   test +0x88 cmpeq r0, #0
 *   test +0xa8 cmp r8, r0
 *   test +0xb4 cmp r5, #3
 *   test +0xc0 cmp r6, #2
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221dbe4; the literal pool and
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


asm u32 native_ov001_0221dbe4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    ldr r4, [r0]
    ldr r7, [r0, #0x8]
    ldrb r0, [r4, #0x356]
    mov r5, #0
    mov r6, #0
    cmp r0, #0
    moveq r0, #1
    streqb r0, [r4, #0x356]
    mov r10, r5
    mov r9, #1
ov001_0221dbe4_L30:
    mov r0, r7
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221dbe4_Lb0
    mov r0, r7
    bl native_fn_021dbd24
    str r10, [sp]
    mov r8, r0
    stmib sp, {r9, r10}
    mov r0, r4
    mov r1, r7
    mov r2, r10
    mov r3, r10
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mul r0, r1, r0
    cmp r8, r0
    bgt ov001_0221dbe4_Lb0
    add r0, r7, #512
    ldrsb r1, [r0, #77]
    cmp r1, #0
    ldreqsb r0, [r0, #75]
    cmpeq r0, #0
    bne ov001_0221dbe4_Lb0
    mov r0, r4
    bl native_fn_021dbe5c
    mov r8, r0
    mov r0, r7
    bl native_fn_021dbe5c
    sub r0, r0, #300
    cmp r8, r0
    addge r6, r6, #1
ov001_0221dbe4_Lb0:
    add r5, r5, #1
    cmp r5, #3
    add r7, r7, #1088
    blt ov001_0221dbe4_L30
    cmp r6, #2
    movge r0, #1
    movlt r0, #0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
