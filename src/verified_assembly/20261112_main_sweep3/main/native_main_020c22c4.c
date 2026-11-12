/* main row 0x020c22c4: 44 bytes.
 *
 * What it does: Relays the two stack words at sp + 0x10 and sp + 0x14 into 0x02217bdc, then calls 0x020414c8 with 0x2a.
 *
 * Decoded shape: no aggregate-copy shape (an ordinary instruction run).
 *
 *   0 block transfer(s), 2 word store instruction(s)
 *
 * Body: the measured instruction stream transcribed from
 * arm9.bin at 0x020c22c4; the literal pool and
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

extern void native_fn_02217bdc(void);
extern void native_fn_020414c8(void);


asm u32 native_main_020c22c4 (register u32 a0)
{
    stmdb sp!, {r3, lr}
    sub sp, sp, #8
    ldr lr, [sp, #0x10]
    ldr r12, [sp, #0x14]
    str lr, [sp]
    str r12, [sp, #4]
    bl native_fn_02217bdc
    mov r0, #0x2a
    bl native_fn_020414c8
    add sp, sp, #8
    ldmia sp!, {r3, pc}
}
