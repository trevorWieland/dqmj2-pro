/* main row 0x020c22f0: 44 bytes.
 *
 * What it does: Wrapper around the neighbouring relay 0x020c22c4: forwards the same two stack words to it, then calls 0x02049e0c with 0.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020c22f0; the literal pool and
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

extern void native_fn_020c22c4(void);
extern void native_fn_02049e0c(void);


asm u32 native_main_020c22f0 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    ldr lr, [sp, #0x10]
    ldr r12, [sp, #0x14]
    str lr, [sp]
    str r12, [sp, #4]
    bl native_fn_020c22c4
    mov r0, #0
    bl native_fn_02049e0c
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
