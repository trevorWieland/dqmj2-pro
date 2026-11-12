/* main row 0x020061ac: 40 bytes.
 *
 * What it does: Variadic forwarder one stack slot higher than 0x0200616c: pushes the four argument registers, builds the pointer to the fifth argument at sp + 0x10 and calls 0x020061d4 with it.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020061ac; the literal pool and
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

extern void native_fn_020061d4(void);


asm u32 native_main_020061ac (register u32 a0)
{
    stmdb sp!, {r0, r1, r2, r3}
    stmdb sp!, {r3, lr}
    add r3, sp, #0x10
    bic r3, r3, #3
    ldr r2, [sp, #0x10]
    add r3, r3, #4
    bl native_fn_020061d4
    ldmia sp!, {r3, lr}
    add sp, sp, #0x10
    bx lr
}
