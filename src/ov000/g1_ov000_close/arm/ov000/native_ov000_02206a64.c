/* ov000 row 0x02206a64: 84 bytes.
 *
 * What it does: 20 instructions; 2 call(s) to 0x02046af4, 0x02206a20; loops (back edge at +0x30); returns through pop {r4, r5, r6, pc}; 1 literal slot(s) in the extent
 *
 * Decoded shape: aggregate copy.
 *
 *   pool +0x50 -> constant 0x021c9698 (image word 0x021c9698)
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * ov000.bin at 0x02206a64; the literal pool and
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

extern void native_fn_02046af4(void);
extern void native_fn_02206a20(void);


asm u32 native_ov000_02206a64 (register u32 a0)
{
    stmdb sp!, {r4, r5, r6, lr}
    sub sp, sp, #72
    add r12, sp, #8
    mov r6, r0
    mov r5, r2
    str r12, [sp]
    mov r12, #255
    ldr r0, =0x021c9698
    mov r2, #0
    mov r4, r3
    mov r3, r2
    str r12, [sp, #0x4]
    bl native_fn_02046af4
    add r1, sp, #8
    mov r0, r6
    mov r2, r5
    mov r3, r4
    bl native_fn_02206a20
    add sp, sp, #72
    ldmia sp!, {r4, r5, r6, pc}
}
