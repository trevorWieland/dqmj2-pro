/* ov001 row 0x022114c0: 76 bytes.
 *
 * What it does: 17 instructions; 2 call(s) to 0x022114e0, 0x022114d8; loops (back edge at +0x2c); returns through pop {r4, pc}; 2 literal slot(s) in the extent
 *
 * Decoded shape: loop with 2 calls (17 instructions, 2 calls, 0 branches, 2 back edges, 2 literal slots).
 *
 *   pool +0x44 -> constant 0x0223e124 (image word 0x0223e124)
 *   pool +0x48 -> constant 0x0223e130 (image word 0x0223e130)
 *   back edge +0x2c -> +0x20
 *   back edge +0x3c -> +0x18
 *   test +0x28 cmp lr, #8
 *   test +0x34 cmp r12, #3
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022114c0; the literal pool and
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



asm u32 native_ov001_022114c0 (register u32 a0)
{
    stmdb sp!, {r4, lr}
    mov r12, #0
    ldr r4, =0x0223e124
    ldr r1, =0x0223e130
    mov r2, r12
    mov r3, r12
ov001_022114c0_L18:
    mov lr, r3
    add r0, r1, r12, lsl #5
ov001_022114c0_L20:
    str r2, [r0, lr, lsl #2]
    add lr, lr, #1
    cmp lr, #8
    blt ov001_022114c0_L20
    add r12, r12, #1
    cmp r12, #3
    strb r2, [r4], #1
    blt ov001_022114c0_L18
    ldmia sp!, {r4, pc}
}
