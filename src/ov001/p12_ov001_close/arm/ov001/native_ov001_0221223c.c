/* ov001 row 0x0221223c: 84 bytes.
 *
 * What it does: 18 instructions; no calls; no back edge; returns through pop {r3, r4, r5, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: straight-line scalar (18 instructions, 0 calls, 0 branches, 0 back edges, 3 literal slots).
 *
 *   pool +0x48 -> constant 0x0223e124 (image word 0x0223e124)
 *   pool +0x4c -> constant 0x0223e128 (image word 0x0223e128)
 *   pool +0x50 -> constant 0x0223e130 (image word 0x0223e130)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221223c; the literal pool and
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



asm u32 native_ov001_0221223c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    ldr r5, [r0, #0x2c]
    ldr lr, =0x0223e124
    ldr r2, =0x0223e128
    ldrb r12, [lr, r5]
    ldr r4, [r2]
    ldr r3, =0x0223e130
    add r0, r12, #1
    mov r1, r0, lsr #31
    rsb r0, r1, r0, lsl #29
    sub r4, r4, #1
    add r0, r1, r0, ror #29
    add r1, r3, r5, lsl #5
    mov r3, #0
    str r4, [r2]
    str r3, [r1, r12, lsl #2]
    strb r0, [lr, r5]
    ldmia sp!, {r3, r4, r5, pc}
}
