/* ov000 row 0x021f9898: 176 bytes.
 *
 * What it does: 44 instructions; 4 call(s) to 0x021f9484, 0x021f9914, 0x021f98bc, +1 more; loops (back edge at +0x30); returns through pop {r3, r4, r5, r6, r7, r8, r9, r10, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   branch +0x58 -> +0x7c
 *   branch +0x60 -> +0x7c
 *   branch +0x68 -> +0x7c
 *   back edge +0x8c -> +0x24
 *   back edge +0xa0 -> +0x20
 *   test +0x4c cmp r3, r10
 *   test +0x5c cmp r3, r10
 *   test +0x64 cmp r2, r9
 *   test +0x6c cmp r0, r9
 *   test +0x88 cmp r6, #4
 *   test +0x9c cmp r7, #3
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x021f9898; the literal pool and
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

extern void native_fn_021f9484(void);


asm u32 native_ov000_021f9898 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, r6, r7, r8, r9, r10, lr}
    sub sp, sp, #4
    mov r7, #0
    mov r10, r0
    mov r9, r1
    mov r8, r2
    add r4, sp, #0
    mov r5, r7
ov000_021f9898_L20:
    mov r6, r5
ov000_021f9898_L24:
    mov r0, r4
    mov r1, r6
    mov r2, r7
    bl native_fn_021f9484
    ldrsh r3, [sp]
    ldrsh r2, [sp, #2]
    add r0, r3, #40
    add r1, r2, #40
    mov r0, r0, lsl #16
    mov r1, r1, lsl #16
    cmp r3, r10
    mov r3, r0, asr #16
    mov r0, r1, asr #16
    bgt ov000_021f9898_L7c
    cmp r3, r10
    blt ov000_021f9898_L7c
    cmp r2, r9
    bgt ov000_021f9898_L7c
    cmp r0, r9
    addge sp, sp, #4
    addge r0, r6, r7, lsl #2
    ldmgeia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
ov000_021f9898_L7c:
    add r0, r6, #1
    mov r0, r0, lsl #24
    mov r6, r0, asr #24
    cmp r6, #4
    blt ov000_021f9898_L24
    add r0, r7, #1
    mov r0, r0, lsl #24
    mov r7, r0, asr #24
    cmp r7, #3
    blt ov000_021f9898_L20
    mov r0, r8
    add sp, sp, #4
    ldmia sp!, {r3, r4, r5, r6, r7, r8, r9, r10, pc}
}
