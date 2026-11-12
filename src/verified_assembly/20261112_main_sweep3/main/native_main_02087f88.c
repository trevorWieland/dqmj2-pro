/* main row 0x02087f88: 32 bytes.
 *
 * What it does: calls 1 helper; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x02087f88; the literal pool and
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

extern void native_fn_0202a498(void);


asm u32 native_main_02087f88 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    movs r1, r0
    moveq r0, #0
    ldmeqia sp!, {r3, pc}
    mov r0, #6
    bl native_fn_0202a498
    mov r0, #1
    ldmia sp!, {r3, pc}
}
