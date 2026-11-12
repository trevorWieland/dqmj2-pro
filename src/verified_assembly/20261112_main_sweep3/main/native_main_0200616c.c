/* main row 0x0200616c: 40 bytes.
 *
 * What it does: Variadic forwarder: pushes the four argument registers, builds a pointer to the stacked arguments (sp + 0xc aligned down to 4, plus 4) and calls 0x02006194 with it, then drops the argument block.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0200616c; the literal pool and
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

extern void native_fn_02006194(void);


asm u32 native_main_0200616c (register u32 a0)
{
    stmdb sp!, {r0, r1, r2, r3}
    stmdb sp!, {r3, lr}
    add r2, sp, #0xc
    bic r2, r2, #3
    ldr r1, [sp, #0xc]
    add r2, r2, #4
    bl native_fn_02006194
    ldmia sp!, {r3, lr}
    add sp, sp, #0x10
    bx lr
}
