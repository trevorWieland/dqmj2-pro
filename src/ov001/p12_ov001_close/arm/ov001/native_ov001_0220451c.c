/* ov001 row 0x0220451c: 60 bytes.
 *
 * What it does: 14 instructions; 1 call(s) to 0x0204b53c; loops (back edge at +0x30); returns through pop {r3, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (14 instructions, 1 call, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x38 -> native_data_0222e060 (image word 0x0222e060)
 *   0 block transfer(s), 3 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x0220451c; the literal pool and
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

extern u8 native_data_0222e060[];
extern void native_fn_0204b53c(void);


asm u32 native_ov001_0220451c (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, =native_data_0222e060
    add lr, sp, #0
    ldrh r3, [r2, #6]
    ldrh r12, [r2, #4]
    add r2, r1, r1, lsl #1
    strh r3, [sp, #2]
    ldrsh r3, [sp, #2]
    mov r1, lr
    strh r12, [sp]
    add r2, r3, r2, lsl #3
    strh r2, [sp, #2]
    bl native_fn_0204b53c
    ldmia sp!, {r3, pc}
}
