/* Word fill over a byte span (0x02008c14, 20 bytes).
 *
 * Stores r0 across [r1, r1 + r2) one word at a time, with the test rotated
 * in front of a predicated block store. r2 counts bytes, so the loop stores
 * ceil(r2 / 4) words.
 *
 * Unknowns: the buffers and why the span is counted in bytes.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; mwcc emits `str r0, [r1], #4` with the test at the top and four more
 * bytes; the one-word block store is the original author's choice.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008c14 (register u32 value, register u32 *dst, register u32 span)
{
    add r12, r1, r2
native_main_02008c14_loop:
    cmp r1, r12
    stmltia r1 !, {r0}
    blt native_main_02008c14_loop
    bx lr
}
