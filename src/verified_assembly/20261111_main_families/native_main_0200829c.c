/* Count leading zeros (0x0200829c, 8 bytes).
 *
 * Counts the leading zero bits of the argument with the ARM CLZ
 * instruction, returning 32 for a zero argument.
 *
 * Unknowns: the caller's use of the count.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; mwccarm exposes no CLZ intrinsic; __builtin_clz, __clz and __cntlzw all
 * become library calls.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm u32 native_main_0200829c (register u32 value)
{
    clz r0, r0
    bx lr
}
