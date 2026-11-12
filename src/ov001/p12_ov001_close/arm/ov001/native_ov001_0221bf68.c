/* ov001 row 0x0221bf68: 172 bytes.
 *
 * What it does: 42 instructions; 4 call(s) to 0x021db8d0, 0x021f07dc, 0x021dbd24, +1 more; loops (back edge at +0x34); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: block fill (42 instructions, 4 calls, 1 branch, 4 back edges, 1 literal slot).
 *
 *   pool +0xa8 -> constant 0x66666667 (image word 0x66666667)
 *   branch +0x3c -> +0x8c
 *   back edge +0x98 -> +0x30
 *   test +0x1c cmp r0, #0
 *   test +0x38 cmp r0, #0
 *   test +0x7c cmp r3, r0
 *   test +0x90 cmp r8, #3
 *   1 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221bf68; the literal pool and
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

extern void ov001_record_is_active_021db8d0(void);
extern void native_fn_021f07dc(void);
extern void native_fn_021dbd24(void);


asm u32 native_ov001_0221bf68 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #12
    ldr r7, [r0]
    ldr r10, [r0, #0x8]
    ldrb r0, [r7, #0x356]
    mov r8, #0
    ldr r4, =0x66666667
    cmp r0, #0
    moveq r0, #1
    streqb r0, [r7, #0x356]
    mov r6, r8
    mov r5, #1
ov001_0221bf68_L30:
    mov r0, r10
    bl ov001_record_is_active_021db8d0
    cmp r0, #0
    beq ov001_0221bf68_L8c
    str r6, [sp]
    stmib sp, {r5, r6}
    mov r0, r7
    mov r1, r10
    mov r2, r6
    mov r3, r6
    bl native_fn_021f07dc
    ldrb r1, [r7, #0x356]
    mul r9, r1, r0
    mov r0, r10
    bl native_fn_021dbd24
    add r2, r9, r9, lsl #1
    smull r1, r3, r4, r2
    mov r1, r2, lsr #31
    add r3, r1, r3, asr #2
    cmp r3, r0
    addge sp, sp, #12
    movge r0, #1
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
ov001_0221bf68_L8c:
    add r8, r8, #1
    cmp r8, #3
    add r10, r10, #1088
    blt ov001_0221bf68_L30
    mov r0, #0
    add sp, sp, #12
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
