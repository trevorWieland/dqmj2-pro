/* ov001 row 0x021f153c: 156 bytes.
 *
 * What it does: 35 instructions; 1 call(s) to 0x021f18d8; no back edge; returns through pop {r3, r4, r5, pc}; 4 literal slot(s) in the extent
 *
 * Decoded shape: call sequence (35 instructions, 1 call, 0 branches, 0 back edges, 4 literal slots).
 *
 *   pool +0x8c -> constant 0x02238f58 (image word 0x02238f58)
 *   pool +0x90 -> constant 0x02238f84 (image word 0x02238f84)
 *   pool +0x94 -> constant 0x02238f88 (image word 0x02238f88)
 *   pool +0x98 -> constant 0x02238f8a (image word 0x02238f8a)
 *   test +0x0c cmp r1, #0
 *   test +0x24 cmp r3, #32
 *   0 block transfer(s), 6 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021f153c; the literal pool and
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

extern void native_fn_021f18d8(void);


asm u32 native_ov001_021f153c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    sub sp, sp, #8
    ldr r3, =0x02238f58
    cmp r1, #0
    ldr r3, [r3, #0x24]
    movlt r1, #0
    mov r3, r3, lsl #24
    mov r5, r3, asr #24
    add r3, r1, #16
    cmp r3, #32
    ldr r3, =0x02238f58
    ldr lr, =0x02238f84
    ldr r4, [r3, #0x24]
    movgt r1, #16
    add r4, r4, #1
    str r4, [r3, #0x24]
    str r0, [lr, r5, lsl #3]
    add r12, r5, #3
    mov r0, r12, lsl #24
    ldr r3, =0x02238f88
    mov lr, r5, lsl #3
    strh r1, [r3, lr]
    ldr r3, =0x02238f8a
    mov r12, #0
    strh r2, [r3, lr]
    mov r3, #2
    str r3, [sp]
    mov r0, r0, asr #24
    and r1, r1, #255
    and r2, r2, #255
    mov r3, #16
    str r12, [sp, #0x4]
    bl native_fn_021f18d8
    add sp, sp, #8
    ldmia sp!, {r3, r4, r5, pc}
}
