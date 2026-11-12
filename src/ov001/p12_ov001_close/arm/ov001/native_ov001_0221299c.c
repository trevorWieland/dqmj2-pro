/* ov001 row 0x0221299c: 48 bytes.
 *
 * What it does: 11 instructions; no calls; no back edge; returns through bx lr; 1 literal slot(s) in the extent
 *
 * Decoded shape: straight-line scalar (11 instructions, 0 calls, 0 branches, 0 back edges, 1 literal slot).
 *
 *   pool +0x2c -> constant 0x020d3fe0 (image word 0x020d3fe0)
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0221299c; the literal pool and
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



asm u32 native_ov001_0221299c (register u32 a0)
{
    mov r2, #182
    mul r2, r0, r2
    mov r0, r2, asr #4
    mov r0, r0, lsl #1
    add r2, r0, #1
    ldr r0, =0x020d3fe0
    mov r2, r2, lsl #1
    ldrsh r0, [r0, r2]
    mul r0, r1, r0
    mov r0, r0, asr #12
    bx lr
}
