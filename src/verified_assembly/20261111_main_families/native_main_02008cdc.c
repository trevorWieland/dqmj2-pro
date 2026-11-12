/* Sixteen-byte block copy (0x02008cdc, 20 bytes).
 *
 * Copies 12 bytes as three registers and then one trailing word. The split is
 * forced: r0 and r1 hold the two pointers, so only r2, r3 and r12 are free
 * for the move.
 *
 * Unknowns: the two structures and why the copy is inlined rather than a call.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; a 16-byte struct assignment makes mwcc clobber r0/r1 as copy registers
 * (four-register move) or wrap the copy in a loop.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008cdc (register u32 *src, register u32 *dst)
{
    ldmia r0 !, {r2, r3, r12}
    stmia r1 !, {r2, r3, r12}
    ldmia r0 !, {r2}
    stmia r1 !, {r2}
    bx lr
}
