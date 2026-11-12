/* Thirty-two-byte block copy (0x02008cf0, 28 bytes).
 *
 * Copies 12 + 12 + 8 bytes with three- and two-register block moves, each
 * store advancing the destination and each load the source.
 *
 * Unknowns: the source and destination records.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the same 32 bytes as one struct assignment make mwcc build a counted
 * loop with a frame; the unrolled 12 + 12 + 8 split is the original.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008cf0 (register u32 *src, register u32 *dst)
{
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2, r3}
    stmia r1 !, {r2, r3}
    bx lr
}
