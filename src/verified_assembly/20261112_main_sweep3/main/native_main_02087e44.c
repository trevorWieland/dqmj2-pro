/* main row 0x02087e44: 20 bytes.
 *
 * What it does: Calls the function pointer at +4 of the object at +0x14 of its argument, inside a one-word frame.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02087e44; the literal pool and
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



asm u32 native_main_02087e44 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    ldr r2, [r0, #0x14]
    ldr r2, [r2, #4]
    blx r2
    ldmia sp!, {r3, pc}
}
