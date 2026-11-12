/* ov000 row 0x0221ebe0: 20 bytes.
 *
 * What it does: 5 instructions; 1 call(s) to 0x0221e8c8; loops (back edge at +0x0c); returns through pop {r3, pc}
 *
 * Decoded shape: aggregate copy.
 *
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x0221ebe0; the literal pool and
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

extern void native_fn_0221e8c8(void);


asm u32 native_ov000_0221ebe0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    mov r12, #1
    str r12, [sp]
    bl native_fn_0221e8c8
    ldmia sp!, {r3, pc}
}
