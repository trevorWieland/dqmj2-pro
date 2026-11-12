/* ov001 row 0x021fd140: 56 bytes.
 *
 * What it does: 11 instructions; no calls; no back edge; returns through bx lr; 3 literal slot(s) in the extent
 *
 * Decoded shape: straight-line scalar (11 instructions, 0 calls, 0 branches, 0 back edges, 3 literal slots).
 *
 *   pool +0x2c -> constant 0x02239d70 (image word 0x02239d70)
 *   pool +0x30 -> constant 0x02239d74 (image word 0x02239d74)
 *   pool +0x34 -> constant 0x02239d78 (image word 0x02239d78)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021fd140; the literal pool and
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



asm u32 native_ov001_021fd140 (register u32 a0)
{
    mov r1, #12
    mul r3, r0, r1
    ldr r0, =0x02239d70
    sub r2, r1, #13
    ldr r1, =0x02239d74
    str r2, [r0, r3]
    mov r2, #0
    ldr r0, =0x02239d78
    str r2, [r1, r3]
    str r2, [r0, r3]
    bx lr
}
