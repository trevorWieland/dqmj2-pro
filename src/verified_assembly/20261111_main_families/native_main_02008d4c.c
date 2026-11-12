/* Sixty-four-byte block copy (0x02008d4c, 44 bytes).
 *
 * Copies 12 bytes four times and then 16 bytes; the last load has no
 * writeback and also loads into r0, because the source pointer is dead and r0
 * supplies the fourth free register.
 *
 * Unknowns: the source and destination records and why the tail is 16 bytes.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the 16-byte tail with r0 reused as a temporary is the signature of the
 * original copy; a C struct assignment cannot keep r0/r1 as pointers.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008d4c (register u32 *src, register u32 *dst)
{
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0, {r0, r2, r3, r12}
    stmia r1 !, {r0, r2, r3, r12}
    bx lr
}
