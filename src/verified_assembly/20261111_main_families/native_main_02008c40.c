/* Word gather into one destination word (0x02008c40, 24 bytes).
 *
 * Walks r0 over [r0, r0 + r2) and keeps overwriting the single word at r1,
 * so the last source word wins; the destination does not advance.
 *
 * Unknowns: why the same destination is rewritten rather than accumulated.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; the C form of the same walk keeps the destination pointer in another
 * register and does not reproduce the block-move loads.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008c40 (register u32 *src, register u32 *dst, register u32 span)
{
    add r12, r0, r2
native_main_02008c40_loop:
    cmp r0, r12
    ldmltia r0 !, {r2}
    strlt r2, [r1]
    blt native_main_02008c40_loop
    bx lr
}
