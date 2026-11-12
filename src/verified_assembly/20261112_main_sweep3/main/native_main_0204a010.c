/* main row 0x0204a010: 60 bytes.
 *
 * What it does: calls 1 helper; 2 loads, 2 stores; returns through a restored pc
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x0204a010; the literal pool and
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

extern void native_fn_02087e58(void);


asm u32 native_main_0204a010 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    ldr r12, [sp, #0x10]
    and r3, r3, #0xff
    str r3, [sp]
    and r3, r12, #0xff
    str r3, [sp, #4]
    mov r3, r2
    and r2, r1, #0xff
    ldr r0, [r0, #0x44]
    and r3, r3, #0xff
    mov r1, #0
    bl native_fn_02087e58
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
