/* Word copy over a byte span (0x02008c28, 24 bytes).
 *
 * Copies words from r0 to r1 until the destination passes r1 + r2, advancing
 * both pointers with predicated one-word block moves.
 *
 * Unknowns: the buffers and why the span is counted in bytes.
 *
 * Body: the measured instruction stream. C forms and every installed mwccarm
 * build/profile were measured against this row first; a C copy loop emits two post-indexed str/ldr pairs plus a rotated test
 * and is four bytes longer.
 */
typedef unsigned int u32;
typedef signed int s32;
typedef unsigned short u16;
typedef signed short s16;
typedef unsigned char u8;
typedef signed char s8;


asm void native_main_02008c28 (register u32 *src, register u32 *dst, register u32 span)
{
    add r12, r1, r2
native_main_02008c28_loop:
    cmp r1, r12
    ldmltia r0 !, {r2}
    stmltia r1 !, {r2}
    blt native_main_02008c28_loop
    bx lr
}
