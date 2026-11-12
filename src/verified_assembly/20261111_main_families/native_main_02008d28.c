/* Forty-eight-byte block copy (0x02008d28, 36 bytes).
 *
 * Copies 12 bytes four times with three-register block moves.
 *
 * Unknowns: the source and destination records.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; a 48-byte struct assignment becomes a three-iteration loop (36 bytes plus
 * a frame); the unrolled form is the original.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008d28 (register u32 *src, register u32 *dst)
{
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    bx lr
}
