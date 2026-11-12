/* ov001 row 0x022027c0: 48 bytes.
 *
 * What it does: 9 instructions; 1 call(s) to 0x0220468c; no back edge; returns through pop {r3, pc}; 3 literal slot(s) in the extent
 *
 * Decoded shape: call sequence (9 instructions, 1 call, 0 branches, 0 back edges, 3 literal slots).
 *
 *   pool +0x24 -> constant 0x0223a244 (image word 0x0223a244)
 *   pool +0x28 -> constant 0x0223a248 (image word 0x0223a248)
 *   pool +0x2c -> constant 0x0223a249 (image word 0x0223a249)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x022027c0; the literal pool and
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

extern void native_fn_0220468c(void);


asm u32 native_ov001_022027c0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r12, =0x0223a244
    ldr lr, =0x0223a248
    str r0, [r12, r1, lsl #3]
    ldr r12, =0x0223a249
    strb r2, [lr, r1, lsl #3]
    strb r3, [r12, r1, lsl #3]
    bl native_fn_0220468c
    ldmia sp!, {r3, pc}
}
