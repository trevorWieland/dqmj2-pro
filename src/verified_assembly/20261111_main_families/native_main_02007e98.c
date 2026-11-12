/* Argument-preserving call trampoline (0x02007e98, 16 bytes).
 *
 * Saves r0 and lr, calls the function that starts immediately after this one
 * (0x02007ea8), restores r0 and returns, so the caller's first argument survives
 * whatever the callee leaves in it.
 *
 * Unknowns: the callee's role and why its address is the next function.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; mwcc spills r0 to a callee-saved register instead of pushing it, which adds
 * four bytes and moves the call.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;
extern void native_fn_02007ea8(void);


asm void native_main_02007e98 (void)
{
    stmdb sp !, {r0, lr}
    bl native_fn_02007ea8
    ldmia sp !, {r0, lr}
    bx lr
}
