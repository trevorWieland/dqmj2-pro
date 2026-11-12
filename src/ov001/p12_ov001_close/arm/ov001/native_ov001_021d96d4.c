/* ov001 row 0x021d96d4: 60 bytes.
 *
 * What it does: 14 instructions; 1 call(s) to 0x02042c0c; loops (back edge at +0x10); returns through pop {r3, r4, r5, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: loop with 1 call (14 instructions, 1 call, 0 branches, 1 back edge, 1 literal slot).
 *
 *   pool +0x38 -> constant 0x84210843 (image word 0x84210843)
 *   0 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov001.bin at 0x021d96d4; the literal pool and
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

extern void native_fn_02042c0c(void);


asm u32 native_ov001_021d96d4 (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r1
    and r1, r5, #255
    mov r4, r0
    bl native_fn_02042c0c
    mov r1, #10
    mul r12, r5, r1
    ldr r3, =0x84210843
    mov r1, r12, lsr #31
    smull r2, r14, r3, r12
    add lr, r12, lr
    add lr, r1, lr, asr #4
    strb lr, [r4, #0x10d]
    ldmia sp!, {r3, r4, r5, pc}
}
