/* ov001 row 0x0221bed0: 152 bytes.
 *
 * What it does: 38 instructions; 4 call(s) to 0x021db8d0, 0x021f07dc, 0x021dbd24, +1 more; loops (back edge at +0x30); returns through pop {r4, r5, r6, r7, r8, r9, pc}
 *
 * Decoded shape: block fill (38 instructions, 4 calls, 1 branch, 4 back edges, 0 literal slots).
 *
 *   branch +0x38 -> +0x7c
 *   back edge +0x88 -> +0x2c
 *   test +0x1c cmp r0, #0
 *   test +0x34 cmp r0, #0
 *   test +0x6c cmp r1, r0
 *   test +0x80 cmp r8, #3
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221bed0; the literal pool and
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
extern void native_fn_021f07dc(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221bed0 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, r7, r8, r9, lr}
    sub sp, sp, #12
    ldr r4, [r0]
    ldr r5, [r0, #0x8]
    ldrb r0, [r4, #0x356]
    mov r8, #0
    mov r7, r8
    cmp r0, #0
    moveq r0, #1
    streqb r0, [r4, #0x356]
    mov r6, #1
ov001_0221bed0_L2c:
    mov r0, r5
    bl native_fn_021db8d0
    cmp r0, #0
    beq ov001_0221bed0_L7c
    str r7, [sp]
    stmib sp, {r6, r7}
    mov r0, r4
    mov r1, r5
    mov r2, r7
    mov r3, r7
    bl native_fn_021f07dc
    ldrb r1, [r4, #0x356]
    mul r9, r1, r0
    mov r0, r5
    bl native_fn_021dbd24
    add r1, r9, r9, lsl #1
    cmp r1, r0
    addge sp, sp, #12
    movge r0, #1
    ldmgeia sp!, {r4, r5, r6, r7, r8, r9, pc}
ov001_0221bed0_L7c:
    add r8, r8, #1
    cmp r8, #3
    add r5, r5, #1088
    blt ov001_0221bed0_L2c
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r4, r5, r6, r7, r8, r9, pc}
}
