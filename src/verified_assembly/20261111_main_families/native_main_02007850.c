/* Two-call wrapper that returns its first argument (0x02007850, 20 bytes).
 *
 * Saves r0, calls 0x02007864 and 0x020078f4, then restores r0 and returns it, so
 * the caller's first argument is the result regardless of the callees.
 *
 * Unknowns: the two callees' roles and why the first argument is passed through.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; mwcc copies r0 into r4 and emits push {r4, lr} / pop {r4, pc}: four bytes more
 * than the measured push/pop of r0.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;
extern void native_fn_02007864(void);
extern void native_fn_020078f4(void);


asm u32 native_main_02007850 (void)
{
    stmdb sp !, {r0, lr}
    bl native_fn_02007864
    bl native_fn_020078f4
    ldmia sp !, {r0, lr}
    bx lr
}
