/* main row 0x02019dd4: 40 bytes.
 *
 * What it does: The same variadic-forwarder body as 0x0200616c with its own callee: aligns the stacked argument pointer at sp + 0xc and calls 0x02019e78.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02019dd4; the literal pool and
 * every branch target are read from the image, not guessed.
 *
 * Unknowns: the field meanings and the callee contracts are not established by byte identity.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;

extern void native_fn_02019e78(void);


asm u32 native_main_02019dd4 (register u32 a0)
{
    stmdb sp!, {r0, r1, r2, r3}
    stmdb sp!, {r3, lr}
    add r2, sp, #0xc
    bic r2, r2, #3
    ldr r1, [sp, #0xc]
    add r2, r2, #4
    bl native_fn_02019e78
    ldmia sp!, {r3, lr}
    add sp, sp, #0x10
    bx lr
}
