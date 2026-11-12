/* main row 0x0203d25c: 56 bytes.
 *
 * What it does: calls 3 helpers; 2 loads, 2 stores; 1 local pool word (0x020f6044); returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   pool +0x34 -> constant 0x020f6044 (image word 0x020f6044)
 *   2 block transfer(s), 1 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0203d25c; the literal pool and
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

extern void native_fn_0200f3e0(void);
extern void native_fn_0200f48c(void);
extern void native_fn_0200fc74(void);


asm u32 native_main_0203d25c (register u32 a0)
{
    stmdb sp!, {lr}
    sub sp, sp, #0x1c
    add r0, sp, #0xc
    bl native_fn_0200f3e0
    add r0, sp, #0
    bl native_fn_0200f48c
    add r0, sp, #0xc
    add r1, sp, #0
    bl native_fn_0200fc74
    ldr r1, =0x020f6044
    str r0, [r1]
    add sp, sp, #0x1c
    ldmia sp!, {pc}
}
