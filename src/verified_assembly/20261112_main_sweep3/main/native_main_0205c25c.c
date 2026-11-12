/* main row 0x0205c25c: 28 bytes.
 *
 * What it does: Per-index flag probe: returns the word at +0x18 of the object 0x02063e80 returns, masked with 1 << index.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 0 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0205c25c; the literal pool and
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

extern void native_fn_02063e80(void);


asm u32 native_main_0205c25c (register u32 a0)
{
    stmdb sp!, {r3, r4, r5, lr}
    mov r5, r0
    mov r4, #1
    bl native_fn_02063e80
    ldr r0, [r0, #0x18]
    and r0, r0, r4, lsl r5
    ldmia sp!, {r3, r4, r5, pc}
}
